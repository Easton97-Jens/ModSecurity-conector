from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "checks" / "security" / "check_security_tools_manifest.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_security_tools_manifest", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_module()


class SecurityToolsManifestTest(unittest.TestCase):
    def test_repository_manifest_and_workflow_pins_validate(self):
        self.assertEqual(checker.validate(ROOT), [])

    def test_rejects_mutable_action_reference(self):
        text = "- uses: actions/checkout@v7\n"
        errors = checker.validate_workflow_text(text, "fixture.yaml")
        self.assertTrue(any("not an immutable SHA" in error for error in errors))

    def test_parses_uses_lines_without_a_backtracking_regular_expression(self):
        action = "actions/checkout@0000000000000000000000000000000000000000"
        self.assertEqual(
            checker.parse_uses_line(f"  - uses: {action} # v7.0.0  "),
            (action, "v7.0.0  "),
        )
        self.assertEqual(checker.parse_uses_line(f"uses: {action} #   "), (action, " "))
        self.assertIsNone(checker.parse_uses_line(f"uses: {action} #"))
        self.assertIsNone(checker.parse_uses_line(f"name: uses: {action}"))

    def test_osv_pr_workflow_avoids_reusable_json_job_outputs(self):
        workflow = (ROOT / ".github" / "workflows" / "ci-security-osv.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("runs-on: ubuntu-latest", workflow)
        self.assertNotIn("osv-scanner-reusable-pr.yml", workflow)
        self.assertIn("osv-reporter-action@9a498708959aeaef5ef730655706c5a1df1edbc2", workflow)
        self.assertIn("--fail-on-vuln=true", workflow)

    def test_rejects_action_sha_that_is_not_the_recorded_release(self):
        pins = checker.pinned_actions_from(checker.load_manifest())
        text = "- uses: actions/checkout@0000000000000000000000000000000000000000 # v7.0.0\n"
        errors = checker.validate_workflow_text(text, "fixture.yaml", pins)
        self.assertTrue(
            any("does not match the recorded release" in error for error in errors)
        )

    def test_rejects_missing_release_version(self):
        manifest = copy.deepcopy(checker.load_manifest())
        manifest["tools"]["actionlint"]["release"]["version"] = ""
        errors = checker.validate_manifest_data(manifest)
        self.assertTrue(any("release version is required" in error for error in errors))

    def test_rejects_unofficial_security_policy_url(self):
        manifest = copy.deepcopy(checker.load_manifest())
        manifest["tools"]["actionlint"]["security_policy"] = "https://example.invalid/policy"
        errors = checker.validate_manifest_data(manifest)
        self.assertTrue(any("security policy must be the official" in error for error in errors))

    def test_check_status_does_not_promote_errors_or_missing_features(self):
        self.assertEqual(checker.check_result_status("tool_error", True), "failed")
        self.assertEqual(
            checker.check_result_status("passed", False),
            "blocked_feature_unavailable",
        )
        self.assertEqual(checker.check_result_status("passed", True), "passed")


if __name__ == "__main__":
    unittest.main()
