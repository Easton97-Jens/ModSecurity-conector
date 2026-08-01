"""Static and local-contract coverage for the opt-in NGINX Memcheck path."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors/nginx/harness/run_nginx_smoke.sh"
TEMPLATE = ROOT / "connectors/nginx/harness/nginx_smoke.conf"
MAKEFILE = ROOT / "Makefile"
SUMMARIZER = ROOT / "ci/runtime/common/summarize-nginx-memcheck.py"
SUPPRESSIONS = ROOT / "connectors/nginx/harness/valgrind-nginx-core-1.31.2.supp"


class NginxMemcheckHarnessContractTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.harness = HARNESS.read_text(encoding="utf-8")
        cls.template = TEMPLATE.read_text(encoding="utf-8")
        cls.makefile = MAKEFILE.read_text(encoding="utf-8")
        cls.summarizer = SUMMARIZER.read_text(encoding="utf-8")
        cls.suppressions = SUPPRESSIONS.read_text(encoding="utf-8")

    def test_memcheck_is_explicitly_opt_in_and_bounded_to_soak(self) -> None:
        self.assertIn('NGINX_MEMCHECK="${NGINX_MEMCHECK:-0}"', self.harness)
        self.assertIn('VALGRIND_BIN="${VALGRIND_BIN:-valgrind}"', self.harness)
        self.assertIn(
            'NGINX_MEMCHECK_SUPPRESSIONS="$SCRIPT_DIR/valgrind-nginx-core-1.31.2.supp"',
            self.harness,
        )
        self.assertNotIn("${NGINX_MEMCHECK_SUPPRESSIONS:-", self.harness)
        self.assertIn('NGINX_MEMCHECK=1 requires MSCONNECTOR_SMOKE_STAGE=bounded_soak', self.harness)
        self.assertIn('NGINX_MEMCHECK=1 requires NGINX_PROTOCOL_PROFILE=h1', self.harness)
        self.assertIn('NGINX_MEMCHECK=1 requires exactly one canonical NGINX_SOAK_CASES id', self.harness)
        self.assertIn('NGINX_MEMCHECK_WAIT_SECONDS=30', self.harness)
        self.assertIn('validate_nginx_memcheck_mode', self.harness)
        self.assertIn('blocked "missing executable Valgrind;', self.harness)

    def test_memcheck_suppression_is_bound_to_verified_nginx_1_31_2_identity(self) -> None:
        self.assertIn('NGINX_BINARY="${NGINX_BINARY:-$NGINX_PREFIX/sbin/nginx}"', self.harness)
        self.assertIn("NGINX_MEMCHECK_EXPECTED_VERSION=1.31.2", self.harness)
        self.assertIn(
            'NGINX_MEMCHECK_NGINX_BINARY="$NGINX_PREFIX/sbin/nginx"',
            self.harness,
        )
        self.assertIn(
            'NGINX_MEMCHECK_NGINX_ARCHIVE="$NGINX_BUILD_DIR/verified-archives/nginx-1.31.2.tar.gz"',
            self.harness,
        )
        self.assertIn(
            "NGINX_MEMCHECK_NGINX_ARCHIVE_SHA256="
            "af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c",
            self.harness,
        )
        identity = self.harness.split("validate_nginx_memcheck_binary_identity() {", 1)[1].split(
            "\n}\n\nvalidate_nginx_memcheck_mode()", 1
        )[0]
        self.assertIn('[ "$NGINX_BINARY" = "$NGINX_MEMCHECK_NGINX_BINARY" ]', identity)
        self.assertIn('"$NGINX_BINARY" -v 2>&1', identity)
        self.assertIn(
            '"nginx version: nginx/$NGINX_MEMCHECK_EXPECTED_VERSION"', identity
        )
        self.assertIn('command -v sha256sum >/dev/null 2>&1', identity)
        self.assertIn('sha256sum "$NGINX_MEMCHECK_NGINX_ARCHIVE"', identity)
        self.assertIn(
            '[ "$NGINX_MEMCHECK_NGINX_ARCHIVE_ACTUAL_SHA256" = '
            '"$NGINX_MEMCHECK_NGINX_ARCHIVE_SHA256" ]',
            identity,
        )
        mode = self.harness.split("validate_nginx_memcheck_mode() {", 1)[1].split(
            "\n}\n\nvalidate_nginx_protocol_request()", 1
        )[0]
        self.assertIn("validate_nginx_memcheck_binary_identity", mode)
        self.assertLess(
            mode.index("0) return 0 ;;"),
            mode.index("validate_nginx_memcheck_binary_identity"),
        )

    def test_default_harness_parent_is_contained_by_build_root(self) -> None:
        self.assertIn(
            'NGINX_HARNESS_PARENT="${NGINX_HARNESS_PARENT:-$BUILD_ROOT/nginx-harness}"',
            self.harness,
        )
        self.assertIn("NGINX_HARNESS_PARENT ?= $(BUILD_ROOT)/nginx-harness", self.makefile)
        self.assertNotIn('fallback_parent="/var/tmp"', self.harness)
        self.assertIn("not silently reroute the default parent", self.harness)

    def test_configtest_stays_uninstrumented_and_runtime_uses_required_flags(self) -> None:
        configtest = '"$NGINX_BINARY" -t -p "$RUNTIME_ROOT" -c "$CONFIG_FILE"'
        valgrind_start = 'exec "$SETSID_BIN" "$VALGRIND_BIN"'
        self.assertIn(configtest, self.harness)
        self.assertIn(valgrind_start, self.harness)
        start_server = self.harness.split("start_server() {", 1)[1].split(
            "\n}\n\nsend_case_request()", 1
        )[0]
        self.assertLess(start_server.index(configtest), start_server.index("start_nginx_process"))
        for flag in (
            "--trace-children=yes",
            "--vgdb=no",
            "--leak-check=full",
            "--show-leak-kinds=definite,indirect,possible",
            "--errors-for-leak-kinds=definite,indirect",
            "--error-exitcode=99",
            "--num-callers=24",
            '--log-file="$LOG_DIR/valgrind.%p.log"',
        ):
            self.assertIn(flag, self.harness)
        self.assertNotIn("--child-silent-after-fork", self.harness)
        self.assertIn('--suppressions="$NGINX_MEMCHECK_SUPPRESSIONS"', self.harness)
        self.assertIn("daemon off;", self.template)
        self.assertIn("worker_processes 1;", self.template)

    def test_nginx_core_exit_suppression_is_exact_and_definite_only(self) -> None:
        self.assertEqual(
            [line.strip() for line in self.suppressions.splitlines() if line.strip()],
            [
                "{",
                "nginx_1_31_2_worker_environment_exit_lifetime",
                "Memcheck:Leak",
                "match-leak-kinds: definite",
                "fun:malloc",
                "fun:ngx_alloc",
                "fun:ngx_set_environment",
                "fun:ngx_worker_process_init",
                "fun:ngx_worker_process_cycle",
                "fun:ngx_spawn_process",
                "fun:ngx_start_worker_processes",
                "fun:ngx_master_process_cycle",
                "fun:main",
                "}",
            ],
        )
        self.assertNotIn("...", self.suppressions)
        self.assertNotIn("ngx_http_modsecurity", self.suppressions)
        self.assertNotIn("libmodsecurity", self.suppressions)
        self.assertNotIn("Memcheck:Addr", self.suppressions)

    def test_lifecycle_uses_graceful_quit_bounded_wait_and_payload_free_summary(self) -> None:
        self.assertIn('"$NGINX_BINARY" -p "$RUNTIME_ROOT" -c "$CONFIG_FILE" -s quit', self.harness)
        self.assertIn('wait_for_nginx_memcheck_exit "$NGINX_MEMCHECK_WAIT_SECONDS"', self.harness)
        self.assertIn('exec "$SETSID_BIN" "$VALGRIND_BIN"', self.harness)
        self.assertIn("signal_nginx_memcheck_processes TERM", self.harness)
        self.assertIn("signal_nginx_memcheck_processes KILL", self.harness)
        self.assertIn("NGINX_MEMCHECK_CONTAINMENT", self.harness)
        self.assertIn('record_nginx_memcheck_process_group "$NGINX_PID"', self.harness)
        self.assertIn("nginx_memcheck_process_group_alive", self.harness)
        self.assertIn('kill -0 "-$NGINX_MEMCHECK_PROCESS_GROUP"', self.harness)
        self.assertIn("umask 077", self.harness)
        self.assertIn("graceful_shutdown_incomplete", self.summarizer)
        self.assertIn("process_group_unverified", self.summarizer)
        self.assertIn("valgrind_log_permissions_unsafe", self.summarizer)
        self.assertIn("error_incomplete", self.summarizer)
        self.assertIn("possibly_lost_bytes", self.summarizer)
        self.assertIn("still_reachable_bytes", self.summarizer)
        self.assertNotIn("kill -9", self.harness)
        self.assertNotIn("--suppressions", self.summarizer)
        self.assertIn("raw-payload-free", self.summarizer)

    def test_make_target_is_opt_in_h1_and_uses_existing_wrapper(self) -> None:
        self.assertIn(".PHONY: memcheck-nginx", self.makefile)
        target = self.makefile.split("memcheck-nginx: check-framework prepare-runtime-components", 1)[1]
        target = target.split("\n\nsmoke-envoy:", 1)[0]
        self.assertIn("NGINX_MEMCHECK=1", target)
        self.assertIn("MSCONNECTOR_SMOKE_STAGE=bounded_soak", target)
        self.assertIn("NGINX_PROTOCOL_PROFILE=h1", target)
        self.assertIn("NGINX_DOWNSTREAM_PROTOCOL=http1", target)
        self.assertIn("NGINX_SOAK_CONCURRENCY=1", target)
        self.assertIn('sh "$(FRAMEWORK_ROOT)/ci/runtime/run-nginx-smoke.sh"', target)
        self.assertNotIn("memcheck-nginx", self.makefile.split("test:", 1)[1].split("\n", 1)[0])

    def test_summarizer_reports_clean_and_never_copies_log_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            log_dir = Path(temporary)
            roles = log_dir / "nginx-memcheck-roles.txt"
            lifecycle = log_dir / "nginx-memcheck-lifecycle.txt"
            output = log_dir / "nginx-memcheck-summary.json"
            text_output = log_dir / "nginx-memcheck-summary.txt"
            roles.write_text("master_pid=101\nworker_pid=102\n", encoding="utf-8")
            lifecycle.write_text(
                "shutdown=graceful\nwait=exited\nwrapper_exit_code=0\ncontainment=isolated\n",
                encoding="utf-8",
            )
            complete_log = (
                "request-body=must-not-appear-in-summary\n"
                "==101== definitely lost: 0 bytes in 0 blocks\n"
                "==101== indirectly lost: 0 bytes in 0 blocks\n"
                "==101== possibly lost: 0 bytes in 0 blocks\n"
                "==101== still reachable: 0 bytes in 0 blocks\n"
                "==101== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)\n"
            )
            master_log = log_dir / "valgrind.101.log"
            worker_log = log_dir / "valgrind.102.log"
            master_log.write_text(complete_log, encoding="utf-8")
            worker_log.write_text(complete_log, encoding="utf-8")
            master_log.chmod(0o600)
            worker_log.chmod(0o600)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SUMMARIZER),
                    "--log-dir",
                    str(log_dir),
                    "--roles-file",
                    str(roles),
                    "--lifecycle-file",
                    str(lifecycle),
                    "--output",
                    str(output),
                    "--text-output",
                    str(text_output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "clean")
            self.assertEqual(summary["logs_seen"], 2)
            self.assertEqual(summary["private_log_inputs"], 2)
            self.assertNotIn("must-not-appear-in-summary", output.read_text(encoding="utf-8"))
            self.assertNotIn("must-not-appear-in-summary", text_output.read_text(encoding="utf-8"))

    def test_summarizer_marks_missing_worker_evidence_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            log_dir = Path(temporary)
            roles = log_dir / "nginx-memcheck-roles.txt"
            lifecycle = log_dir / "nginx-memcheck-lifecycle.txt"
            output = log_dir / "nginx-memcheck-summary.json"
            text_output = log_dir / "nginx-memcheck-summary.txt"
            roles.write_text("master_pid=201\nworker_pid=202\n", encoding="utf-8")
            lifecycle.write_text(
                "shutdown=graceful\nwait=exited\nwrapper_exit_code=0\ncontainment=isolated\n",
                encoding="utf-8",
            )
            master_log = log_dir / "valgrind.201.log"
            master_log.write_text(
                "==201== ERROR SUMMARY: 0 errors from 0 contexts\n", encoding="utf-8"
            )
            master_log.chmod(0o600)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SUMMARIZER),
                    "--log-dir",
                    str(log_dir),
                    "--roles-file",
                    str(roles),
                    "--lifecycle-file",
                    str(lifecycle),
                    "--output",
                    str(output),
                    "--text-output",
                    str(text_output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 99, result.stderr)
            summary = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "incomplete")
            self.assertIn("worker_log_missing", summary["incomplete_reasons"])

    def test_summarizer_marks_uncontained_or_forced_shutdown_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            log_dir = Path(temporary)
            roles = log_dir / "nginx-memcheck-roles.txt"
            lifecycle = log_dir / "nginx-memcheck-lifecycle.txt"
            output = log_dir / "nginx-memcheck-summary.json"
            text_output = log_dir / "nginx-memcheck-summary.txt"
            roles.write_text("master_pid=251\nworker_pid=252\n", encoding="utf-8")
            lifecycle.write_text(
                "shutdown=forced_kill\nwait=exited\nwrapper_exit_code=0\ncontainment=unverified\n",
                encoding="utf-8",
            )
            complete_log = "==251== ERROR SUMMARY: 0 errors from 0 contexts\n"
            for pid in (251, 252):
                log_path = log_dir / f"valgrind.{pid}.log"
                log_path.write_text(complete_log, encoding="utf-8")
                log_path.chmod(0o600)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SUMMARIZER),
                    "--log-dir",
                    str(log_dir),
                    "--roles-file",
                    str(roles),
                    "--lifecycle-file",
                    str(lifecycle),
                    "--output",
                    str(output),
                    "--text-output",
                    str(text_output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 99, result.stderr)
            summary = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "incomplete")
            self.assertIn("graceful_shutdown_incomplete", summary["incomplete_reasons"])
            self.assertIn("process_group_unverified", summary["incomplete_reasons"])

    def test_summarizer_marks_non_private_raw_log_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            log_dir = Path(temporary)
            roles = log_dir / "nginx-memcheck-roles.txt"
            lifecycle = log_dir / "nginx-memcheck-lifecycle.txt"
            output = log_dir / "nginx-memcheck-summary.json"
            text_output = log_dir / "nginx-memcheck-summary.txt"
            roles.write_text("master_pid=301\nworker_pid=302\n", encoding="utf-8")
            lifecycle.write_text(
                "shutdown=graceful\nwait=exited\nwrapper_exit_code=0\ncontainment=isolated\n",
                encoding="utf-8",
            )
            complete_log = "==301== ERROR SUMMARY: 0 errors from 0 contexts\n"
            master_log = log_dir / "valgrind.301.log"
            worker_log = log_dir / "valgrind.302.log"
            master_log.write_text(complete_log, encoding="utf-8")
            worker_log.write_text(complete_log, encoding="utf-8")
            master_log.chmod(0o600)
            worker_log.chmod(0o644)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SUMMARIZER),
                    "--log-dir",
                    str(log_dir),
                    "--roles-file",
                    str(roles),
                    "--lifecycle-file",
                    str(lifecycle),
                    "--output",
                    str(output),
                    "--text-output",
                    str(text_output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 99, result.stderr)
            summary = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "incomplete")
            self.assertIn("valgrind_log_permissions_unsafe", summary["incomplete_reasons"])


if __name__ == "__main__":
    unittest.main()
