from __future__ import annotations

import contextlib
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import urlunsplit
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str, module_name: str):
    specification = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    return module


AUDIT = load_module(
    "ci/evidence/reports/audit-full-lifecycle-runtime-roots.py",
    "evidence_output_security_audit",
)
CAPABILITIES = load_module(
    "ci/evidence/collectors/connector_capabilities.py",
    "evidence_output_security_capabilities",
)
SYSTEM_PROOF = load_module(
    "ci/evidence/reports/generate-system-environment-proof.py",
    "evidence_output_security_system_proof",
)
CRITICAL_BATCH = load_module(
    "ci/evidence/reports/generate-remaining-critical-batch-analysis.py",
    "evidence_output_security_critical_batch",
)
PATH_SAFETY = sys.modules["report_path_safety"]


class EvidenceOutputSecurityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.safe_roots = set(PATH_SAFETY.SAFE_ROOTS)
        PATH_SAFETY.SAFE_ROOTS.clear()

    def tearDown(self) -> None:
        PATH_SAFETY.SAFE_ROOTS.clear()
        PATH_SAFETY.SAFE_ROOTS.update(self.safe_roots)

    def test_audit_writes_only_within_current_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            run_root = workspace / "run"
            argv = [
                "audit",
                "--verified-run-root",
                str(run_root),
                "--run-id",
                "valid-run",
                "--output-json",
                "output/audit.json",
                "--output-md",
                "output/audit.md",
                "--output-md-de",
                "output/audit.de.md",
            ]
            with contextlib.chdir(workspace), mock.patch.object(sys, "argv", argv):
                self.assertEqual(AUDIT.main(), 0)
            self.assertTrue((workspace / "output/audit.json").is_file())
            self.assertTrue((workspace / "output/audit.md").is_file())
            self.assertTrue((workspace / "output/audit.de.md").is_file())

    def test_audit_rejects_output_outside_current_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            outside = workspace.parent / "outside-audit.json"
            argv = [
                "audit",
                "--verified-run-root",
                str(workspace / "run"),
                "--run-id",
                "valid-run",
                "--output-json",
                str(outside),
                "--output-md",
                "output/audit.md",
                "--output-md-de",
                "output/audit.de.md",
            ]
            with contextlib.chdir(workspace), mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "output paths must remain"):
                    AUDIT.main()
            self.assertFalse(outside.exists())

    def test_audit_rejects_symlinked_output_outside_current_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary) / "workspace"
            outside = Path(temporary) / "outside"
            workspace.mkdir()
            outside.mkdir()
            (workspace / "escape").symlink_to(outside, target_is_directory=True)
            argv = [
                "audit",
                "--verified-run-root",
                str(workspace / "run"),
                "--run-id",
                "valid-run",
                "--output-json",
                "escape/audit.json",
                "--output-md",
                "output/audit.md",
                "--output-md-de",
                "output/audit.de.md",
            ]
            with contextlib.chdir(workspace), mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "output paths must remain"):
                    AUDIT.main()
            self.assertFalse((outside / "audit.json").exists())

    def test_capability_output_is_owner_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "capabilities.json"
            CAPABILITIES._atomic_write(output, "{}\n")
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)

    def test_repository_url_policy_rejects_non_https_github_url(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            unsafe_url = urlunsplit(("http", "github.com", "/owner/repository", "", ""))
            (root / "README.md").write_text(f"source {unsafe_url}\n", encoding="utf-8")
            policy = SYSTEM_PROOF.https_repo_url_policy(root, root)
            self.assertEqual(policy["status"], "FAIL")
            self.assertEqual(policy["findings"][0]["pattern"], "http")

            (root / "README.md").write_text("source https://github.com/owner/repository\n", encoding="utf-8")
            policy = SYSTEM_PROOF.https_repo_url_policy(root, root)
            self.assertEqual(policy["status"], "PASS")

    def test_critical_batch_rejects_output_outside_generated_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            argv = [
                "critical-batch",
                "--connector-root",
                str(root),
                "--output-dir",
                str(root.parent / "outside-generated-reports"),
            ]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(ValueError, "output directory must be inside"):
                    CRITICAL_BATCH.main()


if __name__ == "__main__":
    unittest.main()
