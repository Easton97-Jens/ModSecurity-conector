#!/usr/bin/env python3
"""Check bilingual documentation invariants for repository-owned docs."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


REMOTE_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "app://",
    "plugin://",
)

LINK_RE = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s+(\S+)")
FENCE_PREFIXES = ("```", "~~~")
GERMAN_GENERATED_NOTE = "Diese deutsche Datei ist eine übersetzte Begleitdatei"


def is_tools_mrts(path: Path) -> bool:
    text = path.as_posix()
    return text.startswith("tools/MRTS/") or text.startswith("modules/ModSecurity-test-Framework/tools/MRTS/")


def is_ignored(path: Path) -> bool:
    return any(part in {".git", ".venv", "__pycache__"} for part in path.parts) or is_tools_mrts(path)


def german_counterpart(path: Path) -> Path:
    return path.with_name(path.name.removesuffix(".md") + ".de.md")


def english_counterpart(path: Path) -> Path:
    return path.with_name(path.name.removesuffix(".de.md") + ".md")


def pair_required(path: Path) -> bool:
    text = path.as_posix()
    name = path.name
    if name.endswith(".de.md") or is_tools_mrts(path):
        return False
    if text in {"README.md", "actions-update-report.md"}:
        return True
    if name.startswith("COMPILE_") and name.endswith(".md"):
        return True
    if text.startswith("docs/") and not (text.startswith("docs/en/") or text.startswith("docs/de/")):
        return True
    if text.startswith("examples/"):
        return True
    if text.startswith("reports/"):
        return True
    if text.startswith(".github/ISSUE_TEMPLATE/") and name.endswith(".md"):
        return True
    if text in {
        "modules/ModSecurity-test-Framework/README.md",
        "modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md",
        "modules/ModSecurity-test-Framework/ci/README.md",
    }:
        return True
    if text.startswith("modules/ModSecurity-test-Framework/docs/"):
        return True
    if text.startswith("connectors/") and (
        "/reports/" in text
        or "/docs/evidence" in text
        or text.endswith("/docs/coverage-decision-matrix.md")
        or text.endswith("/docs/spoe-external-evidence.md")
    ):
        return True
    return False


def english_sources(repo: Path) -> list[Path]:
    return sorted(path for path in repo.rglob("*.md") if not is_ignored(path) and pair_required(path.relative_to(repo)))


def checked_markdown_files(repo: Path) -> list[Path]:
    files: set[Path] = set()
    for source in english_sources(repo):
        files.add(source)
        companion = german_counterpart(source)
        if companion.exists():
            files.add(companion)
    pr_template = repo / ".github/pull_request_template.md"
    if pr_template.exists():
        files.add(pr_template)
    return sorted(files)


def check_pairs_and_switches(repo: Path) -> list[str]:
    errors: list[str] = []
    for source in english_sources(repo):
        rel_source = source.relative_to(repo)
        companion = german_counterpart(source)
        if not companion.exists():
            errors.append(f"{rel_source}: missing German companion {companion.relative_to(repo)}")
            continue
        rel_companion = companion.relative_to(repo)
        english_switch = f"**Language:** English | [Deutsch]({companion.name})"
        german_switch = f"**Sprache:** [English]({source.name}) | Deutsch"
        source_text = source.read_text(encoding="utf-8", errors="replace")
        companion_text = companion.read_text(encoding="utf-8", errors="replace")
        if english_switch not in source_text:
            errors.append(f"{rel_source}: missing language switch {english_switch!r}")
        if german_switch not in companion_text:
            errors.append(f"{rel_companion}: missing language switch {german_switch!r}")
    pr_template = repo / ".github/pull_request_template.md"
    if pr_template.exists():
        text = pr_template.read_text(encoding="utf-8", errors="replace")
        if "## English" not in text or "## Deutsch" not in text:
            errors.append(".github/pull_request_template.md: missing bilingual English/Deutsch sections")
    return errors


def normalized_targets(line: str) -> list[str]:
    targets = [match.group(1).strip() for match in LINK_RE.finditer(line)]
    reference = REFERENCE_LINK_RE.match(line)
    if reference:
        targets.append(reference.group(1).strip())
    return targets


def normalize_local_target(raw_target: str) -> str:
    target = raw_target.strip().strip("<>")
    if " " in target and not target.startswith("#"):
        target = target.split()[0]
    if not target or target.startswith("#") or target.startswith(REMOTE_PREFIXES):
        return ""
    return unquote(target.split("#", 1)[0].split("?", 1)[0])


def check_links(repo: Path) -> list[str]:
    errors: list[str] = []
    for path in checked_markdown_files(repo):
        rel_path = path.relative_to(repo)
        in_fence = False
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.strip().startswith(FENCE_PREFIXES):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for raw_target in normalized_targets(line):
                target = normalize_local_target(raw_target)
                if not target:
                    continue
                candidate = (path.parent / target).resolve()
                try:
                    rel_candidate = candidate.relative_to(repo)
                except ValueError:
                    errors.append(f"{rel_path}:{line_number}: link escapes repository: {raw_target}")
                    continue
                if not candidate.exists():
                    errors.append(f"{rel_path}:{line_number}: missing local link target: {raw_target}")
                    continue
                if path.name.endswith(".de.md") and target.endswith(".md") and not target.endswith(".de.md"):
                    if "**Sprache:**" in line:
                        continue
                    german_target = german_counterpart(candidate)
                    if german_target.exists():
                        errors.append(
                            f"{rel_path}:{line_number}: German link should prefer "
                            f"{german_target.relative_to(repo)} instead of {raw_target}"
                        )
    return errors


def check_generated_german_notes(repo: Path) -> list[str]:
    errors: list[str] = []
    for source in english_sources(repo):
        if not source.name.endswith(".generated.md") and source.name != "actions-update-report.md":
            continue
        companion = german_counterpart(source)
        if not companion.exists():
            continue
        text = companion.read_text(encoding="utf-8", errors="replace")
        if GERMAN_GENERATED_NOTE not in text:
            errors.append(f"{companion.relative_to(repo)}: missing manual generated-companion note")
    return errors


def git_status(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return result.stderr.strip() or result.stdout.strip()
    return result.stdout.strip()


def check_tools_mrts_clean(repo: Path) -> list[str]:
    errors: list[str] = []
    root_status = git_status(repo, "status", "--short", "--", "tools/MRTS", "modules/ModSecurity-test-Framework/tools/MRTS")
    if root_status:
        errors.append(f"tools/MRTS paths changed in parent repository:\n{root_status}")
    framework_root = repo / "modules/ModSecurity-test-Framework"
    if (framework_root / ".git").exists() or (framework_root / "tools/MRTS").exists():
        framework_status = git_status(framework_root, "status", "--short", "--", "tools/MRTS")
        if framework_status:
            errors.append(f"tools/MRTS paths changed in framework module:\n{framework_status}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    repo = args.repo_root.resolve()

    errors: list[str] = []
    errors.extend(check_pairs_and_switches(repo))
    errors.extend(check_generated_german_notes(repo))
    errors.extend(check_links(repo))
    errors.extend(check_tools_mrts_clean(repo))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("bilingual docs ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
