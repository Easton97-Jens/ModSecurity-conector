import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci/runtime/common/hostruntime_preflight.py"
WORKFLOW_SCRIPT = ROOT / "ci/runtime/common/hostruntime-preflight.py"


class HostruntimePreflightTests(unittest.TestCase):
    def run_preflight(self, tmp_path, *args):
        output = tmp_path / "evidence"
        command = [sys.executable, str(SCRIPT), "--connector", "test", "--profile", "unit", "--output-dir", str(output), *args]
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        result = json.loads((output / "status.json").read_text(encoding="utf-8"))
        return completed, result

    def write_lock(self, path, **overrides):
        profile = {
            "id": "unit",
            "os": "linux",
            "arch": "amd64",
            "version": "9.7",
            "sha256": "a" * 64,
            "asset_name": "runtime-9.7.tar.gz",
            "download_url": "https://example.invalid/runtime-9.7.tar.gz",
            "source_provenance": "unit:test",
        }
        profile.update(overrides)
        path.write_text(json.dumps({"schema_version": 1, "profiles": [profile]}), encoding="utf-8")

    def test_missing_binary_is_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            completed, result = self.run_preflight(tmp_path, "--expected-version", "1.0", "--binary", str(tmp_path / "missing"))
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["reason_code"], "prerequisite_missing")
            self.assertTrue(any(item["reason_code"] == "binary_missing" for item in result["checks"]))
            self.assertTrue((tmp_path / "evidence" / "summary.md").is_file())

    def test_incomplete_identity_evidence_cannot_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            completed, result = self.run_preflight(Path(temporary))
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertTrue(any(item["reason_code"] == "binary_missing" for item in result["checks"]))
            self.assertTrue(any(item["reason_code"] == "expected_version_missing" for item in result["checks"]))

    def test_missing_requested_host_prerequisite_is_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            completed, result = self.run_preflight(tmp_path, "--expected-version", "1.0", "--binary", "/bin/sh", "--header", str(tmp_path / "missing.h"), "--tool", "definitely-not-a-host-tool")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertTrue(any(item["reason_code"] == "header_missing" for item in result["checks"]))
            self.assertTrue(any(item["reason_code"] == "tool_missing" for item in result["checks"]))

    def test_safe_outputs_are_bounded_and_have_exact_statuses(self):
        with tempfile.TemporaryDirectory() as temporary:
            completed, result = self.run_preflight(Path(temporary), "--expected-version", "not-the-shell-version", "--binary", "/bin/sh")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn(result["status"], {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"})
            self.assertTrue(all(len(item["remediation"]) <= 240 for item in result["checks"]))
            self.assertNotIn("not-the-shell-version", (Path(temporary) / "evidence" / "summary.md").read_text(encoding="utf-8"))

    def test_workflow_compatibility_entrypoint_accepts_output_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            output = tmp_path / "status.json"
            completed = subprocess.run(
                [sys.executable, str(WORKFLOW_SCRIPT), "--profile", "nginx", "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            result = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["connector"], "nginx")
            self.assertEqual(result["status"], "BLOCKED")
            self.assertTrue((tmp_path / "summary.md").is_file())

    def test_valid_lock_drives_version_and_safe_artifact_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            lock = tmp_path / "runtime-component-lock.json"
            self.write_lock(lock)
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--binary", "/bin/true")
            self.assertEqual(completed.returncode, 0)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["runtime_lock"]["lock_profile"], "unit")
            self.assertEqual(result["runtime_lock"]["expected_version"], "9.7")
            self.assertEqual(result["runtime_lock"]["actual_version"], "9.7")
            self.assertEqual(result["evidence_kind"], "preflight")
            self.assertEqual(result["runtime_status"], "NOT_RUN")
            self.assertEqual(result["reason_code"], "preflight_pass")
            self.assertNotIn("download_url", json.dumps(result))

    def test_missing_lock_is_blocked_with_stable_reason(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(tmp_path / "missing.json"), "--binary", "/bin/true")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["reason_code"], "runtime_lock_missing")

    def test_bad_lock_shape_is_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            lock = tmp_path / "bad.json"
            lock.write_text(json.dumps({"schema_version": 1, "profiles": [{"id": "unit"}]}), encoding="utf-8")
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--binary", "/bin/true")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["reason_code"], "runtime_lock_invalid")

    def test_lock_platform_and_version_drift_cannot_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            lock = tmp_path / "drift.json"
            self.write_lock(lock, os="windows")
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--binary", "/bin/true")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["reason_code"], "runtime_lock_platform_mismatch")
            self.write_lock(lock, version="99.9")
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--binary", "/bin/true")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertNotEqual(result["status"], "PASS")

    def test_architecture_mismatch_is_blocked_not_product_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            completed, result = self.run_preflight(
                Path(temporary), "--expected-version", "9.7", "--expected-arch", "arm64", "--binary", "/bin/true"
            )
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertTrue(any(item["reason_code"] == "arch_mismatch" for item in result["checks"]))

    def test_lock_asset_sha_and_profile_drift_are_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            lock = tmp_path / "drift.json"
            self.write_lock(lock, asset_name="../escape.tar.gz")
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--binary", "/bin/true")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["reason_code"], "runtime_lock_invalid")
            self.write_lock(lock, sha256="not-a-digest")
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--binary", "/bin/true")
            self.assertEqual(result["reason_code"], "runtime_lock_invalid")
            lock.write_text(json.dumps({"schema_version": 1, "profiles": []}), encoding="utf-8")
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--lock-profile", "unknown", "--binary", "/bin/true")
            self.assertEqual(result["reason_code"], "runtime_lock_invalid")

    def test_port_preflight_checks_free_then_busy_binding(self):
        import socket

        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            probe.bind(("127.0.0.1", 0))
            busy_port = probe.getsockname()[1]
            completed, result = self.run_preflight(tmp_path, "--port", str(busy_port))
            self.assertEqual(completed.returncode, 77)
            self.assertTrue(any(item["reason_code"] == "port_in_use" for item in result["checks"]))
            probe.close()
            completed, result = self.run_preflight(tmp_path, "--port", str(busy_port))
            self.assertTrue(any(item["reason_code"] == "port_free" for item in result["checks"]))

    def test_lock_profile_requirements_are_checked(self):
        with tempfile.TemporaryDirectory() as temporary:
            tmp_path = Path(temporary)
            lock = tmp_path / "requirements.json"
            self.write_lock(lock, requirements={"headers": [str(tmp_path / "missing.h")]})
            completed, result = self.run_preflight(tmp_path, "--runtime-lock", str(lock), "--binary", "/bin/true")
            self.assertEqual(completed.returncode, 77)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertTrue(any(item["reason_code"] == "header_missing" for item in result["checks"]))

    def test_make_target_has_no_raw_preflight_argument_sink(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertNotIn("HOSTRUNTIME_PREFLIGHT_ARGS", makefile)
        for option in (
            "HOSTRUNTIME_HEADER",
            "HOSTRUNTIME_SOURCE",
            "HOSTRUNTIME_TOOL",
            "HOSTRUNTIME_PORT",
            "HOSTRUNTIME_WRITE_DIR",
            "HOSTRUNTIME_DISK_PATH",
            "HOSTRUNTIME_MIN_FREE_BYTES",
            "HOSTRUNTIME_CONFIG",
            "HOSTRUNTIME_FIXTURE",
        ):
            self.assertIn(option, makefile)


if __name__ == "__main__":
    unittest.main()
