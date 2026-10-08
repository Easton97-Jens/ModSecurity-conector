"""Controlled subprocess controls; these do not claim genuine NGINX evidence."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "ci/runtime/lifecycle/run-nginx-configtest.py"


class NginxConfigtestDriverTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="nginx-configtest-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.module = self.root / "module.so"
        self.module.write_bytes(b"controlled module identity")
        self.binary = self.root / "nginx"

    def invoke(self, diagnostic='"modsecurity" directive invalid boolean value', exit_code=1,
               extra_script="", case_id="invalid_boolean", output_name="attempt"):
        self.binary.write_text(
            "#!/bin/sh\n"
            "[ \"$1\" = '-e' ] || exit 91\n"
            "[ \"$2\" = 'stderr' ] || exit 92\n"
            "[ \"$3\" = '-t' ] || exit 93\n"
            "[ \"$4\" = '-c' ] || exit 94\n"
            "[ -f \"$5\" ] || exit 95\n"
            "[ \"$0\" = \"${5%/*}/nginx-binary\" ] || exit 96\n"
            f"{extra_script}\nprintf '%s\\n' '{diagnostic}' >&2\nexit {exit_code}\n",
            encoding="utf-8",
        )
        self.binary.chmod(0o700)
        args = [sys.executable, str(DRIVER), "--case-id", case_id,
                "--nginx-binary", str(self.binary), "--module", str(self.module),
                "--output-root", str(self.root / output_name), "--run-id", "unit-control",
                "--parent-sha", "a" * 40, "--framework-sha", "b" * 40,
                "--mrts-sha", "c" * 40]
        return subprocess.run(args, capture_output=True, text=True, timeout=15)

    def test_invalid_size_executes_its_exact_configuration_contract(self):
        result = self.invoke(
            diagnostic='"modsecurity_phase4_body_limit" directive invalid value for modsecurity_phase4_body_limit',
            case_id="invalid_size",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.root / "attempt"
        record = json.loads((output / "source-result.json").read_text())["cases"][0]
        receipt = record["configtest_receipt"]
        self.assertEqual(record["case_id"], "invalid_size")
        self.assertEqual(receipt["directive"], "modsecurity_phase4_body_limit")
        self.assertEqual(receipt["value"], "maybe")
        self.assertEqual(receipt["error_class"], "invalid_size")
        self.assertEqual(receipt["observed_exit_code"], 1)
        self.assertFalse(receipt["process_started"])
        self.assertFalse(receipt["listener_created"])
        self.assertIn("  modsecurity_phase4_body_limit maybe;", (output / "nginx.conf").read_text())

    def test_target_rejections_execute_closed_native_parser_contracts(self):
        cases = {
            "missing_rules_file": ('modsecurity_rules_file', 'missing-rules.conf',
                                   '\"modsecurity_rules_file\" directive Failed to open the file'),
            "invalid_rule_syntax": ('modsecurity_rules', 'SecRule REQUEST_URI',
                                    '\"modsecurity_rules\" directive syntax error'),
            "unknown_config_key": ('modsecurity_unknown_config_key', 'on',
                                   'unknown directive \"modsecurity_unknown_config_key\"'),
            "unsafe_event_path": ('modsecurity_phase4_log', 'unsafe-event-directory',
                                  'is not a secure private event file'),
        }
        for case_id, (directive, value, diagnostic) in cases.items():
            with self.subTest(case_id=case_id):
                output = self.root / case_id
                if case_id == "missing_rules_file":
                    diagnostic += f" {output}/{value}"
                elif case_id == "unsafe_event_path":
                    diagnostic = f'modsecurity_phase4_log "{output}/{value}" {diagnostic}'
                result = self.invoke(diagnostic=diagnostic, case_id=case_id, output_name=case_id)
                self.assertEqual(result.returncode, 0, result.stderr)
                record = json.loads((output / "source-result.json").read_text())["cases"][0]
                receipt = record["configtest_receipt"]
                self.assertEqual(receipt["directive"], directive)
                self.assertEqual(receipt["value"], value)
                self.assertEqual(receipt["error_class"], case_id)
                self.assertFalse(receipt["process_started"])
                self.assertFalse(receipt["listener_created"])
                rendered = value
                if case_id in {"missing_rules_file", "unsafe_event_path"}:
                    rendered = f'"{output}/{value}"'
                    self.assertEqual(receipt["fixture_leaf"], value)
                    state = "absent" if case_id == "missing_rules_file" else "directory"
                    self.assertEqual(receipt["fixture_state"], state)
                    if state == "absent":
                        self.assertFalse((output / value).exists())
                    else:
                        self.assertEqual((output / value).stat().st_mode & 0o777, 0o700)
                        self.assertEqual(list((output / value).iterdir()), [])
                elif case_id == "invalid_rule_syntax":
                    rendered = f'"{value}"'
                self.assertIn(f"  {directive} {rendered};", (output / "nginx.conf").read_text())

    def test_target_rejections_reject_wrong_exit_and_other_error_reason(self):
        for case_id in ("missing_rules_file", "invalid_rule_syntax", "unknown_config_key", "unsafe_event_path"):
            for exit_code in (0, 1, 2):
                with self.subTest(case_id=case_id, exit_code=exit_code):
                    name = f"{case_id}-{exit_code}"
                    result = self.invoke(diagnostic="module missing", exit_code=exit_code,
                                         case_id=case_id, output_name=name)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    record = json.loads((self.root / name / "source-result.json").read_text())["cases"][0]
                    self.assertEqual(record["status"], "FAIL")

    def test_path_fixture_diagnostics_must_name_exact_owned_target(self):
        cases = {
            "missing_rules_file": '"modsecurity_rules_file" directive Failed to open the file /elsewhere/missing-rules.conf',
            "unsafe_event_path": 'modsecurity_phase4_log "/elsewhere/unsafe-event-directory" is not a secure private event file',
        }
        for case_id, diagnostic in cases.items():
            with self.subTest(case_id=case_id):
                result = self.invoke(diagnostic=diagnostic, case_id=case_id, output_name=case_id)
                self.assertEqual(result.returncode, 1, result.stderr)

    def test_target_parser_diagnostics_do_not_promote_wrong_exit_codes(self):
        for case_id in ("missing_rules_file", "invalid_rule_syntax", "unknown_config_key", "unsafe_event_path"):
            for exit_code in (0, 2):
                with self.subTest(case_id=case_id, exit_code=exit_code):
                    name = f"wrong-exit-{case_id}-{exit_code}"
                    output = self.root / name
                    diagnostics = {
                        "missing_rules_file": f'"modsecurity_rules_file" directive Failed to open the file: {output}/missing-rules.conf',
                        "invalid_rule_syntax": '"modsecurity_rules" directive syntax error',
                        "unknown_config_key": 'unknown directive "modsecurity_unknown_config_key"',
                        "unsafe_event_path": f'modsecurity_phase4_log "{output}/unsafe-event-directory" is not a secure private event file',
                    }
                    result = self.invoke(diagnostic=diagnostics[case_id], exit_code=exit_code,
                                         case_id=case_id, output_name=name)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    record = json.loads((output / "source-result.json").read_text())["cases"][0]
                    self.assertEqual(record["status"], "FAIL")

    def test_unsafe_fixture_symlink_substitution_is_not_followed(self):
        target = self.root / "other-private-directory"
        target.mkdir(mode=0o700)
        output = self.root / "unsafe-event-path"
        diagnostic = f'modsecurity_phase4_log "{output}/unsafe-event-directory" is not a secure private event file'
        mutation = (f'rmdir "${{5%/*}}/unsafe-event-directory"\n'
                    f'ln -s "{target}" "${{5%/*}}/unsafe-event-directory"')
        result = self.invoke(diagnostic=diagnostic, case_id="unsafe_event_path",
                             output_name=output.name, extra_script=mutation)
        self.assertEqual(result.returncode, 1, result.stderr)
        receipt = json.loads((output / "source-result.json").read_text())["cases"][0]["configtest_receipt"]
        self.assertEqual(receipt["error_class"], "configtest_fixture_changed")
        self.assertEqual(list(target.iterdir()), [])

    def test_path_fixture_state_mutation_is_not_a_parser_rejection_pass(self):
        cases = {
            "missing_rules_file": ('"modsecurity_rules_file" directive Failed to open the file',
                                   'touch "${5%/*}/missing-rules.conf"'),
            "unsafe_event_path": ('modsecurity_phase4_log',
                                  'touch "${5%/*}/unsafe-event-directory/unexpected"'),
        }
        for case_id, (diagnostic, mutation) in cases.items():
            with self.subTest(case_id=case_id):
                leaf = "missing-rules.conf" if case_id == "missing_rules_file" else "unsafe-event-directory"
                target = self.root / case_id / leaf
                if case_id == "missing_rules_file":
                    diagnostic += f" {target}"
                else:
                    diagnostic += f' "{target}" is not a secure private event file'
                result = self.invoke(diagnostic=diagnostic, case_id=case_id,
                                     output_name=case_id, extra_script=mutation)
                self.assertEqual(result.returncode, 1, result.stderr)
                receipt = json.loads((self.root / case_id / "source-result.json").read_text())["cases"][0]["configtest_receipt"]
                self.assertEqual(receipt["error_class"], "configtest_fixture_changed")

    def test_invalid_size_wrong_diagnostic_and_exit_controls_remain_fail(self):
        controls = [
            ('"modsecurity" directive invalid boolean value', 1),
            ('"other" directive invalid value for modsecurity_phase4_body_limit', 1),
            ('"modsecurity_phase4_body_limit" directive wrong value', 1),
            ('invalid value for modsecurity_phase4_body_limit', 1),
            ('"modsecurity_phase4_body_limit" directive invalid value for modsecurity_phase4_body_limit', 0),
        ]
        for index, (diagnostic, exit_code) in enumerate(controls):
            with self.subTest(diagnostic=diagnostic, exit_code=exit_code):
                output_name = f"control-{index}"
                result = self.invoke(diagnostic=diagnostic, exit_code=exit_code,
                                     case_id="invalid_size", output_name=output_name)
                self.assertEqual(result.returncode, 1, result.stderr)
                record = json.loads((self.root / output_name / "source-result.json").read_text())["cases"][0]
                self.assertEqual(record["status"], "FAIL")
                self.assertEqual(record["configtest_receipt"]["observed_exit_code"], exit_code)

    def test_expected_rejection_requires_both_diagnostic_fragments(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads((self.root / "attempt/source-result.json").read_text())["cases"][0]
        receipt = record["configtest_receipt"]
        self.assertEqual(receipt["observed_exit_code"], 1)
        self.assertEqual(receipt["error_class"], "invalid_boolean")
        self.assertFalse(receipt["process_started"])
        self.assertFalse(receipt["listener_created"])
        self.assertEqual(record["status"], "PASS")
        self.assertTrue(record["live_executed"])
        self.assertTrue(receipt["timestamp"].endswith("Z"))
        output = self.root / "attempt"
        self.assertEqual(record.get("artifacts"), {"configtest_dir": str(output)})
        self.assertEqual((output / "nginx-binary").read_bytes(), self.binary.read_bytes())
        self.assertEqual((output / "nginx-module.so").read_bytes(), self.module.read_bytes())
        self.assertIn(f'load_module "{output}/nginx-module.so";',
                      (output / "nginx.conf").read_text())
        lines = (output / "source-result.jsonl").read_text().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0]), record)
        self.assertEqual(receipt["config_path_identity"], "sha256:" + hashlib.sha256(
            (output / "nginx.conf").read_bytes()).hexdigest())
        for key, path in [("binary_sha256", self.binary), ("module_sha256", self.module),
                          ("stdout_sha256", output / "stdout.log"),
                          ("stderr_sha256", output / "stderr.log")]:
            self.assertEqual(receipt[key], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertIn(f'error_log "{output}/nginx-error.log";',
                      (output / "nginx.conf").read_text())

    def test_unrelated_error_is_not_an_expected_rejection(self):
        for diagnostic in ["missing module", '"other" directive invalid boolean value',
                           '"modsecurity" directive wrong value', "invalid boolean value"]:
            with self.subTest(diagnostic=diagnostic):
                output = self.root / "attempt"
                if output.exists():
                    # Separate fresh invocation; never delete and reuse output roots.
                    self.root = self.root / "next"
                    self.root.mkdir()
                    self.module = self.root / "module.so"
                    self.module.write_bytes(b"controlled module identity")
                    self.binary = self.root / "nginx"
                self.assertEqual(self.invoke(diagnostic).returncode, 1)
                record = json.loads((self.root / "attempt/source-result.json").read_text())["cases"][0]
                self.assertEqual(record["status"], "FAIL")

    def test_wrong_exit_is_not_pass(self):
        self.assertEqual(self.invoke(exit_code=0).returncode, 1)

    def test_bootstrap_diagnostic_is_bounded_captured_stderr(self):
        result = self.invoke(extra_script="printf '%s\\n' 'early bootstrap diagnostic' >&2")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(b"early bootstrap diagnostic", (self.root / "attempt/stderr.log").read_bytes())

    def test_bounded_capture_overflow_is_not_pass(self):
        script = f"exec {sys.executable} -c 'import sys; sys.stderr.write(\"x\" * 70000)'"
        self.assertEqual(self.invoke(extra_script=script).returncode, 1)
        output = self.root / "attempt"
        self.assertLessEqual((output / "stderr.log").stat().st_size, 65536)
        receipt = json.loads((output / "source-result.json").read_text())["cases"][0]["configtest_receipt"]
        self.assertEqual(receipt["error_class"], "configtest_capture_limit")

    def test_timeout_is_not_pass(self):
        script = f"exec {sys.executable} -c 'import time; time.sleep(12)'"
        self.assertEqual(self.invoke(extra_script=script).returncode, 1)
        receipt = json.loads((self.root / "attempt/source-result.json").read_text())["cases"][0]["configtest_receipt"]
        self.assertEqual(receipt["error_class"], "configtest_timeout")

    def test_output_root_must_be_fresh(self):
        (self.root / "attempt").mkdir()
        self.assertNotEqual(self.invoke().returncode, 0)
        self.assertFalse((self.root / "attempt/source-result.json").exists())

    def test_writable_output_parent_is_rejected_before_invocation(self):
        for mode in (0o770, 0o777):
            with self.subTest(mode=oct(mode)):
                parent = self.root / f"writable-{mode:o}"
                parent.mkdir(mode=mode)
                parent.chmod(mode)
                result = self.invoke(output_name=f"{parent.name}/attempt")
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertFalse((parent / "attempt").exists())

    def test_writable_output_ancestor_is_rejected_before_invocation(self):
        ancestor = self.root / "untrusted-ancestor"
        ancestor.mkdir()
        ancestor.chmod(0o777)
        parent = ancestor / "owned-parent"
        parent.mkdir(mode=0o700)
        result = self.invoke(output_name="untrusted-ancestor/owned-parent/attempt")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((parent / "attempt").exists())

    def test_owned_nonwritable_worker_readable_parent_remains_supported(self):
        parent = self.root / "readable-parent"
        parent.mkdir(mode=0o755)
        result = self.invoke(output_name="readable-parent/attempt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(parent.stat().st_mode & 0o777, 0o755)
        self.assertEqual((parent / "attempt").stat().st_mode & 0o777, 0o700)

    def test_symlink_module_is_rejected_before_invocation(self):
        original = self.module
        self.module = self.root / "link.so"
        self.module.symlink_to(original)
        self.assertNotEqual(self.invoke().returncode, 0)
        self.assertFalse((self.root / "attempt/source-result.json").exists())

    def test_missing_module_is_rejected_before_invocation(self):
        self.module = self.root / "missing.so"
        self.assertEqual(self.invoke().returncode, 2)
        self.assertFalse((self.root / "attempt").exists())

    def test_oversized_module_is_rejected_without_a_receipt(self):
        with self.module.open("r+b") as stream:
            stream.truncate(64 * 1024 * 1024 + 1)
        self.assertEqual(self.invoke().returncode, 2)
        self.assertFalse((self.root / "attempt/source-result.json").exists())
        self.assertFalse((self.root / "attempt/nginx-module.so").exists())

    def test_checkout_output_is_rejected_before_invocation(self):
        # Worktree Git marker, not the sandbox's protected empty placeholder.
        (self.root / ".git").write_text("gitdir: /nonexistent-unit-control\n")
        self.assertEqual(self.invoke().returncode, 2)
        self.assertFalse((self.root / "attempt").exists())

    def test_relative_binary_is_rejected(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0)
        args = [sys.executable, str(DRIVER), "--case-id", "invalid_boolean",
                "--nginx-binary", "nginx", "--module", str(self.module),
                "--output-root", str(self.root / "second"), "--run-id", "unit-control",
                "--parent-sha", "a" * 40, "--framework-sha", "b" * 40,
                "--mrts-sha", "c" * 40]
        result = subprocess.run(args, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "second").exists())


if __name__ == "__main__":
    unittest.main()
