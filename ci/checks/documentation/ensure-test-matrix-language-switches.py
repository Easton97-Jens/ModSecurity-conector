#!/usr/bin/env python3
"""Ensure generated test-matrix Markdown keeps bilingual switches."""

from __future__ import annotations

from pathlib import Path


GENERATED_TEST_MATRIX_REPORTS = (
    Path("reports/testing/generated/coverage/case-matrix.generated.md"),
    Path("reports/testing/generated/coverage/connector-gap-summary.generated.md"),
    Path("reports/testing/generated/coverage/coverage-summary.generated.md"),
    Path("reports/testing/generated/coverage/phase-coverage.generated.md"),
    Path("reports/testing/generated/coverage/xfail-summary.generated.md"),
    Path("reports/testing/generated/runtime/apache-runtime-results.generated.md"),
    Path("reports/testing/generated/runtime/haproxy-runtime-results.generated.md"),
    Path("reports/testing/generated/runtime/nginx-runtime-results.generated.md"),
    Path("reports/testing/generated/runtime/runtime-matrix.generated.md"),
    Path("reports/testing/test-coverage-overview.md"),
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def trusted_report_path(relative: Path) -> Path | None:
    """Return a regular report below this checkout, rejecting symlink escapes."""
    candidate = REPOSITORY_ROOT / relative
    if candidate.is_symlink() or not candidate.is_file():
        return None
    try:
        candidate.resolve(strict=True).relative_to(REPOSITORY_ROOT.resolve(strict=True))
    except (OSError, ValueError):
        return None
    return candidate


def german_counterpart(path: Path) -> Path:
    return path.with_name(path.name.removesuffix(".md") + ".de.md")


def english_counterpart(path: Path) -> Path:
    return path.with_name(path.name.removesuffix(".de.md") + ".md")


def ensure_switch(path: Path, switch: str, prefix: str) -> bool:
    if path.is_symlink():
        raise ValueError(f"refusing to rewrite symbolic-link report: {path}")
    try:
        path.resolve(strict=True).relative_to(REPOSITORY_ROOT.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise ValueError(f"refusing to rewrite report outside this checkout: {path}") from exc
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [line for line in text.splitlines() if not line.startswith(prefix)]
    try:
        heading_index = next(index for index, line in enumerate(lines) if line.startswith("# "))
    except StopIteration:
        heading_index = -1

    if heading_index >= 0:
        before = lines[: heading_index + 1]
        after = lines[heading_index + 1 :]
        while after and not after[0].strip():
            after.pop(0)
        updated_lines = before + ["", switch, ""] + after
    else:
        updated_lines = [switch, ""] + lines

    updated = "\n".join(updated_lines).rstrip() + "\n"
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for english_relative in GENERATED_TEST_MATRIX_REPORTS:
        english_path = trusted_report_path(english_relative)
        if english_path is None:
            continue
        german_relative = german_counterpart(english_relative)
        german_path = trusted_report_path(german_relative)
        english_switch = f"**Language:** English | [Deutsch]({german_relative.name})"
        if ensure_switch(english_path, english_switch, "**Language:**"):
            changed += 1
        if german_path is not None:
            source_path = english_counterpart(german_path)
            german_switch = f"**Sprache:** [English]({source_path.name}) | Deutsch"
            if ensure_switch(german_path, german_switch, "**Sprache:**"):
                changed += 1
    if changed:
        print(f"ensure-test-matrix-language-switches: updated {changed} file(s)")
    else:
        print("ensure-test-matrix-language-switches: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
