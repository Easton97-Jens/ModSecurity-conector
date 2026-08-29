"""Focused contracts for the strict HAProxy runtime evidence receipt seam."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors" / "haproxy" / "harness" / "run_haproxy_smoke.sh"


class HaproxyEvidenceHarnessContractTests(unittest.TestCase):
    @staticmethod
    def source() -> str:
        return HARNESS.read_text(encoding="utf-8")

    def test_harness_is_shell_syntax_valid(self) -> None:
        result = subprocess.run(
            ["sh", "-n", str(HARNESS)], check=False, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_receipt_path_starts_and_cleans_up_separate_process_groups(self) -> None:
        source = self.source()
        for name in ("BACKEND_PID", "AGENT_PID", "HAPROXY_PID"):
            self.assertIn(f"{name}=", source)
            self.assertIn(f'cleanup_runtime_process', source)
        self.assertIn("RUNTIME_SETSID_BIN", source)
        self.assertIn("RUNTIME_PGREP_BIN", source)
        self.assertIn("RUNTIME_PS_BIN", source)
        self.assertIn('"$RUNTIME_PGREP_BIN" -g "$process_pid"', source)
        self.assertIn('/bin/kill -TERM -- "-$process_pid"', source)
        self.assertIn('! /bin/kill -TERM "$process_pid"', source)
        self.assertIn('/bin/kill -KILL -- "-$process_pid"', source)
        self.assertIn('if wait "$process_pid" >/dev/null 2>&1; then', source)
        self.assertIn("wait_status", source)
        self.assertIn('trap cleanup_on_exit EXIT', source)
        self.assertIn("trap 'exit 130' INT", source)
        self.assertIn("trap 'exit 143' TERM", source)
        cleanup = source.split("cleanup() {", 1)[1].split("cleanup_on_exit() {", 1)[0]
        self.assertNotIn("|| true", cleanup)
        self.assertIn("RUNTIME_CLEANUP_COMPLETE=1", cleanup)
        self.assertIn("RUNTIME_CLEANUP_COMPLETE=0", cleanup)

    @unittest.skipUnless(
        shutil.which("setsid") and shutil.which("pgrep") and shutil.which("ps"),
        "process-group tools are unavailable",
    )
    def test_cleanup_runtime_process_terminates_and_reaps_a_descendant_group(self) -> None:
        source = self.source()
        cleanup_library = "cleanup_runtime_process() {" + source.split(
            "cleanup_runtime_process() {", 1
        )[1].split("write_haproxy_config() {", 1)[0]
        script = r'''
set -eu
library=$1
RUNTIME_SETSID_BIN=$(command -v setsid)
RUNTIME_PGREP_BIN=$(command -v pgrep)
RUNTIME_PS_BIN=$(command -v ps)
RUNTIME_ROOT=
HAPROXY_PID=
AGENT_PID=
BACKEND_PID=
. "$library"
leader=
test_cleanup() {
    if [ -n "$leader" ]; then
        /bin/kill -TERM -- "-$leader" >/dev/null 2>&1 || :
        wait "$leader" >/dev/null 2>&1 || :
    fi
}
trap test_cleanup EXIT INT TERM
setsid sh -c 'sleep 30 & wait' &
leader=$!
sleep 0.1
cleanup_runtime_process test "$leader"
if kill -0 "$leader" >/dev/null 2>&1; then
    exit 1
fi
if "$RUNTIME_PGREP_BIN" -g "$leader" >/dev/null 2>&1; then
    exit 1
fi
trap - EXIT INT TERM
'''
        with tempfile.TemporaryDirectory(prefix="haproxy-evidence-cleanup-") as directory:
            library = Path(directory) / "cleanup-library.sh"
            library.write_text(cleanup_library, encoding="utf-8")
            result = subprocess.run(
                ["sh", "-eu", "-c", script, "sh", str(library)],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(
        shutil.which("setsid") and shutil.which("pgrep") and shutil.which("ps"),
        "process-group tools are unavailable",
    )
    def test_cleanup_runtime_process_escalates_for_a_term_ignoring_descendant(self) -> None:
        source = self.source()
        cleanup_library = "cleanup_runtime_process() {" + source.split(
            "cleanup_runtime_process() {", 1
        )[1].split("write_haproxy_config() {", 1)[0]
        script = r'''
set -eu
library=$1
RUNTIME_SETSID_BIN=$(command -v setsid)
RUNTIME_PGREP_BIN=$(command -v pgrep)
RUNTIME_PS_BIN=$(command -v ps)
RUNTIME_ROOT=
HAPROXY_PID=
AGENT_PID=
BACKEND_PID=
. "$library"
leader=
test_cleanup() {
    if [ -n "$leader" ]; then
        /bin/kill -KILL -- "-$leader" >/dev/null 2>&1 || :
        wait "$leader" >/dev/null 2>&1 || :
    fi
}
trap test_cleanup EXIT INT TERM
setsid sh -c '(trap "" TERM; while :; do /bin/sleep 1; done) & wait' &
leader=$!
sleep 0.1
cleanup_runtime_process stubborn "$leader"
if kill -0 "$leader" >/dev/null 2>&1; then
    exit 1
fi
if "$RUNTIME_PGREP_BIN" -g "$leader" >/dev/null 2>&1; then
    exit 1
fi
trap - EXIT INT TERM
'''
        with tempfile.TemporaryDirectory(prefix="haproxy-evidence-stubborn-cleanup-") as directory:
            library = Path(directory) / "cleanup-library.sh"
            library.write_text(cleanup_library, encoding="utf-8")
            result = subprocess.run(
                ["sh", "-eu", "-c", script, "sh", str(library)],
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_receipt_is_fixed_post_cleanup_metadata_not_raw_runtime_result(self) -> None:
        source = self.source()
        receipt = source.split("write_haproxy_evidence_receipt() {", 1)[1].split(
            "write_haproxy_config() {", 1
        )[0]
        self.assertIn('source_root="$LOG_DIR/haproxy-runtime-evidence-source"', receipt)
        self.assertIn('"$RUNTIME_CLEANUP_COMPLETE" = "1"', receipt)
        self.assertIn("require_runtime_process_stopped haproxy", receipt)
        self.assertIn("require_runtime_process_stopped spoa", receipt)
        self.assertIn("require_runtime_process_stopped backend", receipt)
        self.assertIn("1:crs_sqli_anomaly_block:with-crs:no-mrts:403:403", receipt)
        self.assertIn("write-source-receipt", receipt)
        self.assertIn("--expected-parent-sha", receipt)
        self.assertIn("--expected-framework-sha", receipt)
        self.assertIn("--expected-mrts-sha", receipt)
        self.assertNotIn("result.json", receipt)
        self.assertNotIn("decision.jsonl", receipt)
        self.assertNotIn("audit", receipt)
        self.assertNotIn("response-body", receipt)
        success = source.split('write_case_result "$TEST_CASE" pass', 1)[1]
        self.assertLess(success.index("if ! cleanup; then"), success.index("write_haproxy_evidence_receipt"))
        self.assertLess(success.index("write_haproxy_evidence_receipt"), success.index("exit 0"))

    def test_receipt_uses_only_the_fixed_unprivileged_projector_and_fails_closed(self) -> None:
        source = self.source()
        receipt = source.split("write_haproxy_evidence_receipt() {", 1)[1].split(
            "write_haproxy_config() {", 1
        )[0]
        self.assertIn("HAPROXY_EVIDENCE_RECEIPT_PROJECTOR", receipt)
        self.assertIn("projector is outside the fixed runtime path", receipt)
        self.assertIn("projector must not be a symlink", receipt)
        self.assertIn(
            '"$PYTHON_BIN" "$HAPROXY_EVIDENCE_RECEIPT_PROJECTOR" write-source-receipt',
            receipt,
        )
        self.assertIn('mkdir -m 700 "$source_root"', receipt)
        self.assertNotIn("HAPROXY_EVIDENCE_RECEIPT_HELPER", receipt)
        self.assertNotIn("seal-helper", receipt)
        self.assertNotIn("sealed helper", receipt)
        self.assertNotIn("sudo", receipt)
        self.assertNotIn("|| true", receipt)
        self.assertNotIn("exit 0", receipt)


if __name__ == "__main__":
    unittest.main()
