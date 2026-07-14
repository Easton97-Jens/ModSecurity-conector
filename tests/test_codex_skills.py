from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci" / "checks" / "documentation" / "check_codex_skills.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_codex_skills", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_module()


def temporary_parent() -> Path:
    configured = os.environ.get("CODEX_TEMP_ROOT")
    if configured:
        parent = Path(configured) / "tmp"
        parent.mkdir(parents=True, exist_ok=True)
        return parent
    return Path(tempfile.gettempdir())


def required_body(extra: str = "") -> str:
    return "\n".join(
        [
            "# Test skill",
            "## Required inputs",
            "Input.",
            "## Repository boundary",
            "Boundary.",
            "## Workflow",
            "Workflow.",
            "## Status model",
            "Status.",
            "## Expected result",
            "Result.",
            "## Safety and stop conditions",
            "Stop.",
            "## Definition of done",
            "Done.",
            "## References",
            extra,
        ]
    )


def write_skill(root: Path, name: str, body: str) -> Path:
    skill = root / ".agents" / "skills" / name
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                'description: "A focused synthetic test skill."',
                "---",
                "",
                body,
            ]
        ),
        encoding="utf-8",
    )
    (skill / "agents" / "openai.yaml").write_text(
        "\n".join(
            [
                "interface:",
                '  display_name: "Test Skill"',
                '  short_description: "Validate a synthetic test skill"',
                '  default_prompt: "Use $' + name + ' for this test."',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return skill


class CodexSkillsTest(unittest.TestCase):
    def test_repository_skills_validate(self):
        self.assertEqual(validator.validate_skills(ROOT), [])

    def test_rejects_unguarded_destructive_command(self):
        with tempfile.TemporaryDirectory(dir=temporary_parent()) as directory:
            root = Path(directory)
            fence = chr(96) * 3
            skill = write_skill(root, "unsafe-skill", required_body(fence + "sh\n" + "git reset --hard\n" + fence))
            errors, _ = validator.validate_skill(root, skill)
        self.assertTrue(any("destructive command" in message for _, message in errors))

    def test_rejects_user_specific_absolute_path(self):
        with tempfile.TemporaryDirectory(dir=temporary_parent()) as directory:
            root = Path(directory)
            skill = write_skill(root, "path-skill", required_body("Read /root/private/file."))
            errors, _ = validator.validate_skill(root, skill)
        self.assertTrue(any("user-specific absolute path" in message for _, message in errors))

    def test_rejects_insecure_external_link_scheme(self):
        with tempfile.TemporaryDirectory(dir=temporary_parent()) as directory:
            root = Path(directory)
            insecure_url = "".join(("http", ":", "//example.invalid"))
            skill = write_skill(root, "link-skill", required_body(f"[insecure]({insecure_url})"))
            errors, _ = validator.validate_skill(root, skill)
        self.assertTrue(any("unsupported external link scheme" in message for _, message in errors))


if __name__ == "__main__":
    unittest.main()
