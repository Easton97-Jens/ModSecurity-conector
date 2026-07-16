"""Focused static contracts for the repository's CI-security workflows."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
SHA_PIN = re.compile(r"^[a-z\d_.-]+(?:/[a-z\d_.-]+)+@[a-f\d]{40}\s+# v\d", re.MULTILINE)


class CiSecurityWorkflowTest(unittest.TestCase):
    def workflow(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding="utf-8")

    def test_all_remote_actions_are_immutable_sha_pins(self) -> None:
        lock_text = (ROOT / "ci" / "tooling" / "security-tools.lock.yml").read_text(encoding="utf-8")
        recorded_shas = set(re.findall(r"commit_sha: ([a-f\d]{40})", lock_text))
        for path in sorted(WORKFLOWS.glob("*.yml")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if "uses:" not in line or "@" not in line or "./" in line:
                    continue
                reference = line.split("uses:", 1)[1].strip()
                self.assertRegex(reference, SHA_PIN, f"{path}: {line}")
                self.assertIn(reference.split("@", 1)[1].split()[0], recorded_shas, f"{path}: {line}")

    def test_secret_scan_uses_exact_pr_range_and_advisory_history(self) -> None:
        text = self.workflow("ci-security-secrets.yml")
        self.assertIn("github.event.pull_request.base.sha", text)
        self.assertIn("github.event.pull_request.head.sha", text)
        self.assertIn('git merge-base "$BASE_SHA" "$HEAD_SHA"', text)
        self.assertIn("--redact=100", text)
        self.assertIn("continue-on-error: true", text)

    def test_osv_uses_the_pr_head_not_merge_sha(self) -> None:
        text = self.workflow("ci-security-osv.yml")
        self.assertIn("OSV_HEAD_SHA: ${{ github.event.pull_request.head.sha }}", text)
        self.assertNotIn("OSV_HEAD_SHA: ${{ github.sha }}", text)
        self.assertIn("old-results.json", text)
        self.assertIn("new-results.json", text)
        self.assertNotIn("fix", text.lower())

    def test_codeql_has_fixed_go_and_bounded_cpp_scope(self) -> None:
        text = self.workflow("ci-security-codeql.yml")
        self.assertEqual(text.count("go-version: '1.24.0'"), 2)
        self.assertIn("connectors/envoy/ext_proc", text)
        self.assertIn("connectors/traefik/native_middleware", text)
        self.assertIn("make check-common-helpers-c17", text)

    def test_security_tool_lock_has_provenance_and_digests(self) -> None:
        text = (ROOT / "ci" / "tooling" / "security-tools.lock.yml").read_text(encoding="utf-8")
        for tool in ("actionlint", "zizmor", "gitleaks"):
            self.assertIn(f"  {tool}:", text)
        self.assertGreaterEqual(text.count("sha256:"), 3)
        self.assertIn("full_history_gitleaks: advisory_until_historical_findings_are_triaged", text)


if __name__ == "__main__":
    unittest.main()
