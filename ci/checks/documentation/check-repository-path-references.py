#!/usr/bin/env python3
"""Validate portable repository documentation references after reorganization."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN_ABSOLUTE = re.compile(r"(?:/root/(?:git|conecter)(?:/|\b)|file:///|[A-Za-z]:\\Users\\)")
OLD_COMPILE_RE = re.compile(r"\bCOMPILE_[A-Z_]+(?:\.de)?\.md\b")
DOC_ROOTS = (
    ROOT / "README.md",
    ROOT / "README.de.md",
    ROOT / "ci" / "README.md",
    ROOT / "ci" / "README.de.md",
    ROOT / "examples",
    ROOT / "reports" / "current",
)
CURRENT_DOC_PREFIXES = (
    "docs/README",
    "docs/architecture",
    "docs/build/",
    "docs/configuration",
    "docs/reference/",
    "docs/testing-and-evidence",
    "docs/operations-and-security",
    "docs/connectors/",
)
IGNORED_PREFIXES = ("docs/generated/", "reports/testing/generated/")


def markdown_files() -> list[Path]:
    files: set[Path] = set()
    for root in DOC_ROOTS:
        if root.is_file():
            files.add(root)
        elif root.is_dir():
            files.update(root.rglob("*.md"))
    return sorted(files)


def current_document_files() -> list[Path]:
    files = markdown_files()
    docs_root = ROOT / "docs"
    if docs_root.is_dir():
        files.extend(
            path
            for path in docs_root.rglob("*.md")
            if path.relative_to(ROOT).as_posix().startswith(CURRENT_DOC_PREFIXES)
        )
    return sorted(set(files))


def local_target(source: Path, raw_target: str) -> Path | None:
    target = unquote(raw_target.strip()).strip("<>")
    if not target or target.startswith("#"):
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    target = target.split("#", 1)[0]
    if not target:
        return None
    return (source.parent / target).resolve()


def is_ignored(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    return relative.startswith(IGNORED_PREFIXES)


def main() -> int:
    errors: list[str] = []
    for path in current_document_files():
        if is_ignored(path):
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        if FORBIDDEN_ABSOLUTE.search(text):
            errors.append(f"{relative}: contains a local developer path")
        if OLD_COMPILE_RE.search(text):
            errors.append(f"{relative}: references a pre-reorganization COMPILE_* guide")
        for raw_target in LINK_RE.findall(text):
            if raw_target in {"file.md", "file.de.md"}:
                continue
            target = local_target(path, raw_target)
            if target is not None and not target.exists():
                errors.append(f"{relative}: missing link target {raw_target!r}")
    if errors:
        print("repository path references: FAIL", file=sys.stderr)
        print("\n".join(sorted(set(errors))), file=sys.stderr)
        return 2
    print("repository path references: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
