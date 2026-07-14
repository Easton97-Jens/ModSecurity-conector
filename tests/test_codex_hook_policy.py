from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "checks" / "security" / "codex_hook_policy.py"


def load_module():
    spec = importlib.util.spec_from_file_location("codex_hook_policy", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


policy = load_module()
TEMP_ROOT = Path("/synthetic/codex-temp-root")


class CodexHookPolicyTest(unittest.TestCase):
    def test_dangerous_git_commands_are_blocked(self):
        commands = {
            "git add .": "broad_git_staging",
            "git add -A": "broad_git_staging",
            "git reset --hard HEAD": "hard_git_reset",
            "git push --force origin topic": "force_push",
            "git push --force-with-lease origin topic": "force_push",
            "git push --force-with-lease=refs/heads/topic origin topic": "force_push",
            "git push origin master": "direct_master_push",
            "git push origin HEAD:master": "direct_master_push",
            "git push origin refs/heads/topic:refs/heads/master": "direct_master_push",
            "rm -rf /unapproved/not-approved": "recursive_removal_outside_temp_root",
        }
        for command, expected in commands.items():
            with self.subTest(command=command):
                self.assertEqual(policy.dangerous_command_reason(command, TEMP_ROOT), expected)

    def test_read_only_commands_remain_allowed(self):
        for command in ("git status --short", "git diff --check", "git show --stat HEAD"):
            with self.subTest(command=command):
                self.assertIsNone(policy.dangerous_command_reason(command, TEMP_ROOT))

    def test_recursive_removal_under_temp_root_is_allowed(self):
        command = f"rm -rf {TEMP_ROOT}/tmp/task-123"
        self.assertIsNone(policy.dangerous_command_reason(command, TEMP_ROOT))

    def test_local_and_secret_paths_are_excluded_from_staging(self):
        paths = {
            "AGENTS.md": "local_codex_instruction_file",
            "RTK.md": "local_codex_instruction_file",
            ".codex/hooks.json": "local_codex_configuration",
            ".rtk/cache.json": "local_codex_configuration",
            "build/output.log": "local_generated_or_analysis_artifact",
            "config/.env.local": "possible_secret_file",
            "keys/service.pem": "possible_secret_file",
        }
        for path, expected in paths.items():
            with self.subTest(path=path):
                self.assertEqual(policy.prohibited_staging_path(path), expected)

    def test_hook_output_never_echoes_command_or_sensitive_value(self):
        sensitive_value = "untrusted-input-marker-that-must-not-be-echoed"
        command = "git add . # " + sensitive_value
        output = policy.pre_tool_hook_output({"tool_input": {"command": command}}, TEMP_ROOT)
        rendered = repr(output)
        self.assertNotIn(command, rendered)
        self.assertNotIn(sensitive_value, rendered)
        self.assertEqual(
            output["hookSpecificOutput"]["permissionDecision"],
            "deny",
        )


if __name__ == "__main__":
    unittest.main()
