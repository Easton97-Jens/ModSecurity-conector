#!/usr/bin/env python3
"""Create canonical EN/DE Change Records, or check the record archive early."""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from contextlib import contextmanager, ExitStack
from datetime import date, datetime, timezone
import importlib.util
import os
from pathlib import Path
import re
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[2]
RECORDS = Path("reports/audits/change-records")
LANGUAGES = ("English", "Deutsch")
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
BASE_PATTERN = re.compile(r"[0-9a-f]{40}")


def load_contract() -> ModuleType:
    """Load the repository-owned checker, never code from a caller's directory."""
    path = ROOT / "ci/checks/documentation/check-bilingual-docs.py"
    spec = importlib.util.spec_from_file_location("change_record_bilingual_contract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the repository documentation contract")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTRACT = load_contract()


def render_pair(name: str, date_utc: str, base_revision: str) -> dict[str, str]:
    """Derive every required heading and identity label from the existing checker."""
    if len(name) > 80 or NAME_PATTERN.fullmatch(name) is None:
        raise ValueError("Name must be a lowercase hyphen-separated slug of at most 80 characters")
    if date.fromisoformat(date_utc).isoformat() != date_utc:
        raise ValueError("Date must use YYYY-MM-DD")
    if BASE_PATTERN.fullmatch(base_revision) is None:
        raise ValueError("Base revision must be a full lowercase 40-character Git commit SHA")
    record_id = f"CR-{date_utc.replace('-', '')}-{name}"
    values = (record_id, date_utc, f"`{base_revision}`")
    rendered: dict[str, str] = {}
    for index, language in enumerate(LANGUAGES):
        filename = record_id + (".md" if index == 0 else ".de.md")
        rendered[filename] = render_record(record_id, values, language, index)
    english, german = (RECORDS / filename for filename in rendered)
    english_text, german_text = rendered.values()
    errors = CONTRACT.check_change_record_pair(english, german, english_text, german_text)
    errors.extend(CONTRACT.structural_pair_errors(english, german, english_text, german_text))
    if errors:
        raise ValueError("\n".join(errors))
    return rendered


def render_record(record_id: str, values: tuple[str, ...], language: str, index: int) -> str:
    if language == "English":
        switch = f"**Language:** English | [Deutsch]({record_id}.de.md)"
        notice = "Scaffold only. Replace every pending section with actual facts; no validation is claimed."
        table_header = "| Field | Value |\n| --- | --- |\n"
        pending = "Pending: document the actual scope, result, or reason this section does not apply."
    else:
        switch = f"**Sprache:** [English]({record_id}.md) | Deutsch"
        notice = "Nur eine Vorlage. Alle offenen Abschnitte mit tatsächlichen Fakten ausfüllen; keine Validierung wird behauptet."
        table_header = "| Feld | Wert |\n| --- | --- |\n"
        pending = "Offen: tatsächlichen Umfang, Ergebnis oder Grund für die Nichtanwendbarkeit dieses Abschnitts dokumentieren."
    headings = CONTRACT.CHANGE_RECORD_REQUIRED_HEADINGS[language]
    chunks = [f"# Change Record: {record_id}\n\n{switch}\n\n{notice}\n"]
    for heading in headings:
        chunks.append(f"\n{heading}\n\n")
        if heading == headings[0]:
            chunks.append(table_header)
            for labels, value in zip(CONTRACT.CHANGE_RECORD_IDENTITY_LABELS, values, strict=True):
                chunks.append(f"| {labels[index]} | {value} |\n")
        else:
            chunks.append(pending + "\n")
    return "".join(chunks)


@contextmanager
def record_directory(root: Path) -> Iterator[int]:
    """Anchor writes to existing real directories below the selected checkout."""
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    with ExitStack() as stack:
        descriptor = os.open(root, flags)
        stack.callback(os.close, descriptor)
        for part in RECORDS.parts:
            descriptor = os.open(part, flags, dir_fd=descriptor)
            stack.callback(os.close, descriptor)
        yield descriptor


def remove_created_files(descriptor: int, created: list[tuple[str, int, int]]) -> None:
    """On failure, remove only outputs whose identity still matches our creation."""
    for filename, device, inode in reversed(created):
        try:
            current = os.stat(filename, dir_fd=descriptor, follow_symlinks=False)
            if (current.st_dev, current.st_ino) == (device, inode):
                os.unlink(filename, dir_fd=descriptor)
        except FileNotFoundError:
            continue


def create_pair(root: Path, name: str, date_utc: str, base_revision: str) -> tuple[str, ...]:
    records = render_pair(name, date_utc, base_revision)
    created: list[tuple[str, int, int]] = []
    with record_directory(root) as directory:
        try:
            with ExitStack() as stack:
                for filename, text in records.items():
                    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
                    descriptor = os.open(filename, flags, 0o644, dir_fd=directory)
                    stack.callback(os.close, descriptor)
                    metadata = os.fstat(descriptor)
                    created.append((filename, metadata.st_dev, metadata.st_ino))
                    with os.fdopen(os.dup(descriptor), "w", encoding="utf-8", newline="") as output:
                        output.write(text)
        except BaseException:
            remove_created_files(directory, created)
            raise
    return tuple(records)


def check_records(root: Path) -> list[str]:
    """Check only the small record archive; do not traverse submodules or call Git."""
    directory = root / RECORDS
    if not directory.is_dir() or directory.is_symlink():
        return [f"{RECORDS}: missing or symlinked Change Record directory"]
    errors: list[str] = []
    sources = sorted(directory.glob("*.md"))
    if not sources:
        return [f"{RECORDS}: no Change Records found"]
    for path in sources:
        if path.is_symlink() or not path.is_file():
            errors.append(f"{path.relative_to(root)}: expected a regular non-symlink file")
        elif path.name.endswith(".de.md"):
            if not CONTRACT.english_counterpart(path).is_file():
                errors.append(f"{path.relative_to(root)}: missing English companion")
        elif CONTRACT.german_counterpart(path).is_symlink():
            errors.append(f"{path.relative_to(root)}: symlinked German companion")
        else:
            errors.extend(CONTRACT.ordinary_pair_errors(root, path))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Read-only early archive check; does not replace the full docs check")
    create = commands.add_parser("create", help="Create both language scaffolds without overwriting files")
    create.add_argument("--name", required=True)
    create.add_argument("--base-revision", required=True)
    create.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            errors = check_records(ROOT)
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print("Change Record contract: PASS (structure only, not evidence validation)")
        else:
            filenames = create_pair(ROOT, args.name, args.date, args.base_revision)
            for filename in filenames:
                print(f"Created scaffold: {RECORDS / filename}")
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Change Record: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
