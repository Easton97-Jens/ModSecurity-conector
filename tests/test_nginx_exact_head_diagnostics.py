from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci/provisioning/components/nginx_exact_head_diagnostics.py"


def load_diagnostics_module():
    spec = importlib.util.spec_from_file_location("nginx_exact_head_diagnostics_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


DIAGNOSTICS = load_diagnostics_module()


class NginxExactHeadDiagnosticsTest(unittest.TestCase):
    def make_fixture(self, root: Path, *, build_log: str | None = None) -> tuple[Path, Path]:
        report = root / DIAGNOSTICS.REPORT_RELATIVE_PATH
        log = root / DIAGNOSTICS.BUILD_LOG_RELATIVE_PATH
        report.parent.mkdir(parents=True, exist_ok=True)
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text("configure succeeded\ncompiler failure: missing module\n", encoding="utf-8")
        record = {
            "nginx": {
                "status": "failed",
                "blocker_reason": "missing_nginx_modsecurity_module",
                "build_exit_code": 1,
                "missing_files": ["ngx_http_modsecurity_module.so"],
                "build_log": build_log if build_log is not None else str(log),
            }
        }
        report.write_text(json.dumps(record), encoding="utf-8")
        return report, log

    def test_in_root_failure_keeps_useful_bounded_metadata_and_tail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            self.make_fixture(root)

            output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        self.assertIn("status=failed", output)
        self.assertIn("blocker_reason=missing_nginx_modsecurity_module", output)
        self.assertIn("missing_files_count=1", output)
        self.assertIn("build/logs/runtime-components/nginx-build.log", output)
        self.assertIn("compiler failure: missing module", output)
        self.assertNotIn(str(root), output)

    def test_environment_poisoning_cannot_change_the_explicit_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            self.make_fixture(root)
            with mock.patch.dict(
                os.environ,
                {"VERIFIED_RUN_ROOT": "/", "RUNTIME_REPORT_OUTPUT_ROOT": "/etc"},
                clear=False,
            ):
                output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        self.assertIn("status=failed", output)
        self.assertNotIn("/etc", output)
        self.assertNotIn("/etc/passwd", output)

    def test_symlinked_report_and_build_log_are_rejected_without_following_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            outside = parent / "outside"
            outside.write_text("outside-canary", encoding="utf-8")
            root = parent / "run"
            root.mkdir()
            report, log = self.make_fixture(root)
            report.unlink()
            report.symlink_to(outside)
            report_output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))
            report.unlink()
            self.make_fixture(root)
            log.unlink()
            log.symlink_to(outside)
            log_output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        self.assertIn("unavailable=report_symlink", report_output)
        self.assertNotIn("outside-canary", report_output)
        self.assertIn("build_log_unavailable=build_log_symlink", log_output)
        self.assertNotIn("outside-canary", log_output)

    def test_symlinked_run_root_ancestor_is_rejected_without_following_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            outside = parent / "outside"
            outside.mkdir()
            outside_root = outside / "run"
            outside_root.mkdir()
            self.make_fixture(outside_root)
            poisoned_parent = parent / "poisoned-runner-temp"
            poisoned_parent.symlink_to(outside, target_is_directory=True)

            output = "\n".join(DIAGNOSTICS.diagnostic_lines(poisoned_parent / "run"))

        self.assertIn("unavailable=run_root_symlink", output)
        self.assertNotIn("status=failed", output)

    def test_reported_outside_build_log_is_not_opened(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            outside = parent / "outside.log"
            outside.write_text("outside-log-canary", encoding="utf-8")
            root = parent / "run"
            root.mkdir()
            self.make_fixture(root, build_log=str(outside))

            output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        self.assertIn("build_log=untrusted_path", output)
        self.assertNotIn("outside-log-canary", output)

    def test_hardlinked_report_is_rejected_without_reading_the_link_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            outside = parent / "outside-report.json"
            outside.write_text('{"canary":"outside-report-canary"}', encoding="utf-8")
            root = parent / "run"
            root.mkdir()
            report, _ = self.make_fixture(root)
            report.unlink()
            os.link(outside, report)

            output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        self.assertIn("unavailable=report_hardlink", output)
        self.assertNotIn("outside-report-canary", output)

    def test_malformed_or_non_mapping_report_is_fail_soft(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            report, _ = self.make_fixture(root)
            report.write_text("[", encoding="utf-8")
            malformed_output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))
            report.write_text("[]", encoding="utf-8")
            mapping_output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        self.assertEqual(malformed_output, "nginx exact-head diagnostics: unavailable=report_malformed")
        self.assertEqual(mapping_output, "nginx exact-head diagnostics: unavailable=nginx_record_invalid")

    def test_oversized_report_is_rejected_and_oversized_log_has_a_bounded_tail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            report, log = self.make_fixture(root)
            report.write_bytes(b"{" + b"x" * DIAGNOSTICS.MAX_REPORT_BYTES)
            report_output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))
            self.make_fixture(root)
            log.write_text(
                "older-canary\n"
                + ("x" * (DIAGNOSTICS.MAX_LOG_TAIL_BYTES + 2048))
                + "\nfinal-compiler-error\n",
                encoding="utf-8",
            )
            log_output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        self.assertIn("unavailable=report_too_large", report_output)
        self.assertIn("build_log_tail_truncated=true", log_output)
        self.assertIn("final-compiler-error", log_output)
        self.assertNotIn("older-canary", log_output)
        self.assertLessEqual(len(log_output), DIAGNOSTICS.MAX_LOG_LINES * DIAGNOSTICS.MAX_LOG_LINE_CHARS + 4096)

    def test_terminal_controls_and_overlong_lines_cannot_expand_or_control_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            _, log = self.make_fixture(root)
            log.write_bytes(
                b"compiler \x1b[31mfailure\x00\r ::error::spoof \xff "
                + b"z" * 4096
                + b"\n"
            )

            output = "\n".join(DIAGNOSTICS.diagnostic_lines(root))

        rendered_line = next(line for line in output.splitlines() if "compiler" in line)
        self.assertNotIn("\x1b", output)
        self.assertNotIn("\x00", output)
        self.assertNotIn("::error::", output)
        self.assertIn("compiler ?[31mfailure?", rendered_line)
        self.assertIn(": :error: :spoof ?", output)
        self.assertTrue(rendered_line.startswith(DIAGNOSTICS.LOG_LINE_PREFIX))
        self.assertLessEqual(len(rendered_line), DIAGNOSTICS.MAX_LOG_LINE_CHARS)


if __name__ == "__main__":
    unittest.main()
