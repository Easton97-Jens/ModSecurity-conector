#!/usr/bin/env python3
"""Validate repository-scoped Codex skill instructions."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[3]
REQUIRED_SKILLS = {
    "bilingual-change-record",
    "ci-failure-triage",
    "connector-test-matrix",
    "delivery-ci",
    "dependency-security-update",
    "framework-parent-handoff",
    "optional-prerequisite-ci",
    "security-finding-lifecycle",
}
REQUIRED_SECTIONS = {
    "Required inputs",
    "Repository boundary",
    "Workflow",
    "Status model",
    "Expected result",
    "Safety and stop conditions",
    "Definition of done",
    "References",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^]]*\]\(([^)]+)\)")
FENCE = chr(96) * 3
CODE_BLOCK_RE = re.compile("^" + FENCE + r"[^\n]*\n(.*?)^" + FENCE, re.MULTILINE | re.DOTALL)
SECRET_RE = re.compile(
    r"(?i)(?:github_pat_[a-z0-9_]+|gh[pousr]_[a-z0-9]+|sk-[a-z0-9]{12,}|"
    r"AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
)
DESTRUCTIVE_RE = re.compile(
    r"(?m)^\s*(?:sudo\s+)?(?:rm\s+-rf\b|git\s+reset\s+--hard\b|"
    r"git\s+push\s+--force(?:-with-lease)?\b|git\s+add\s+(?:\.|-A)\b)"
)


def error(path: Path, message: str) -> tuple[Path, str]:
    return path, message


def parse_skill(path: Path) -> tuple[dict | None, str, list[tuple[Path, str]]]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text, [error(path, "missing YAML frontmatter")]
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text, [error(path, "unterminated YAML frontmatter")]
    try:
        frontmatter = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        return None, text[end + 5 :], [error(path, f"invalid YAML frontmatter: {exc}")]
    if not isinstance(frontmatter, dict):
        return None, text[end + 5 :], [error(path, "frontmatter must be a mapping")]
    return frontmatter, text[end + 5 :], []


def validate_local_link(root: Path, path: Path, target: str) -> list[tuple[Path, str]]:
    candidate = Path(target)
    if candidate.is_absolute():
        return [error(path, f"absolute local link is forbidden: {target}")]
    resolved = (path.parent / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return [error(path, f"link escapes repository root: {target}")]
    if not resolved.exists():
        return [error(path, f"linked repository path does not exist: {target}")]
    return []


def validate_link_target(root: Path, path: Path, raw_target: str) -> list[tuple[Path, str]]:
    target = raw_target.strip()
    parsed = urlsplit(target)
    if target.startswith("#") or parsed.scheme in {"https", "mailto"}:
        return []
    if parsed.scheme:
        return [error(path, f"unsupported external link scheme: {parsed.scheme}")]
    target = target.split("#", 1)[0]
    if not target:
        return []
    return validate_local_link(root, path, target)


def validate_links(root: Path, path: Path, text: str) -> list[tuple[Path, str]]:
    return [
        issue
        for raw_target in LINK_RE.findall(text)
        for issue in validate_link_target(root, path, raw_target)
    ]


def skill_headings(body: str) -> set[str]:
    return {
        line[3:].rstrip()
        for line in body.splitlines()
        if line.startswith("## ") and line[3:].strip()
    }


def validate_openai_yaml(skill_dir: Path, name: str) -> list[tuple[Path, str]]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        return [error(path, "missing generated agents/openai.yaml")]
    try:
        content = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [error(path, f"invalid YAML: {exc}")]
    interface = content.get("interface") if isinstance(content, dict) else None
    if not isinstance(interface, dict):
        return [error(path, "interface mapping is required")]
    errors: list[tuple[Path, str]] = []
    for key in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            errors.append(error(path, f"interface.{key} must be a non-empty string"))
    prompt = interface.get("default_prompt")
    if isinstance(prompt, str) and ("$" + name) not in prompt:
        errors.append(error(path, "interface.default_prompt must invoke the matching skill"))
    return errors


def validate_skill(root: Path, skill_dir: Path) -> tuple[list[tuple[Path, str]], str | None]:
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return [error(path, "missing SKILL.md")], None
    text = path.read_text(encoding="utf-8")
    frontmatter, body, errors = parse_skill(path)
    if frontmatter is None:
        return errors, None
    if set(frontmatter) != {"name", "description"}:
        errors.append(error(path, "frontmatter may contain only name and description"))
    name = frontmatter.get("name")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name):
        errors.append(error(path, "frontmatter name must be lowercase hyphen-case"))
        name = None
    elif name != skill_dir.name:
        errors.append(error(path, "frontmatter name must match its directory name"))
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip() or "TODO" in description:
        errors.append(error(path, "frontmatter description must be complete and non-empty"))
    headings = skill_headings(body)
    for section in sorted(REQUIRED_SECTIONS - headings):
        errors.append(error(path, f"missing required section: {section}"))
    if "TODO" in body:
        errors.append(error(path, "skill body contains a template TODO"))
    if any(marker in text for marker in ("/root/", "/home/", "/Users/")):
        errors.append(error(path, "contains a user-specific absolute path"))
    if SECRET_RE.search(text):
        errors.append(error(path, "contains a token or private-key-shaped value"))
    if any(DESTRUCTIVE_RE.search(block) for block in CODE_BLOCK_RE.findall(body)):
        errors.append(error(path, "contains an unguarded destructive command in a code block"))
    errors.extend(validate_links(root, path, text))
    if isinstance(name, str):
        errors.extend(validate_openai_yaml(skill_dir, name))
    return errors, name if isinstance(name, str) else None


def validate_skills(root: Path = ROOT) -> list[tuple[Path, str]]:
    skills_root = root / ".agents" / "skills"
    if not skills_root.is_dir():
        return [error(skills_root, "missing repository skill directory")]
    directories = sorted(path for path in skills_root.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not directories:
        return [error(skills_root, "contains no skill directories")]
    errors: list[tuple[Path, str]] = []
    names: dict[str, Path] = {}
    for skill_dir in directories:
        skill_errors, name = validate_skill(root, skill_dir)
        errors.extend(skill_errors)
        if name is None:
            continue
        if name in names:
            errors.append(error(skill_dir / "SKILL.md", f"duplicate skill name also used by {names[name].name}"))
        names[name] = skill_dir
    for name in sorted(REQUIRED_SKILLS - set(names)):
        errors.append(error(skills_root, f"required skill is missing: {name}"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate_skills(root)
    for path, message in errors:
        print(f"{path.relative_to(root)}: {message}", file=sys.stderr)
    if errors:
        return 1
    print("Codex skills: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
