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


def german_counterpart(path: Path) -> Path:
    return path.with_name(path.name.removesuffix(".md") + ".de.md")


def english_counterpart(path: Path) -> Path:
    return path.with_name(path.name.removesuffix(".de.md") + ".md")


def ensure_switch(path: Path, switch: str, prefix: str) -> bool:
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
    for english_path in GENERATED_TEST_MATRIX_REPORTS:
        if not english_path.is_file():
            continue
        german_path = german_counterpart(english_path)
        english_switch = f"**Language:** English | [Deutsch]({german_path.name})"
        if ensure_switch(english_path, english_switch, "**Language:**"):
            changed += 1
        if german_path.is_file():
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
