"""Reject unreviewed Parent copies of the Framework-owned APR-util tuple."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK_ROOT = ROOT / "modules" / "ModSecurity-test-Framework"
ALLOWLIST_PATH = ROOT / "tests" / "fixtures" / "apr-util-static-allowlist.txt"

STATIC_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "APR_UTIL_VERSION pin",
        re.compile(r"\bAPR_UTIL_VERSION\b\s*(?::=|\?=|\+=|=)\s*['\"]?\d+(?:\.\d+)+", re.IGNORECASE),
    ),
    (
        "APR_UTIL_SHA256 pin",
        re.compile(r"\bAPR_UTIL_SHA256\b\s*(?::=|\?=|\+=|=)\s*['\"]?[0-9a-f]{64}\b", re.IGNORECASE),
    ),
    (
        "APR_UTIL_SOURCE_URL pin",
        re.compile(r"\bAPR_UTIL_SOURCE_URL\b\s*(?::=|\?=|\+=|=)\s*['\"]?https?://", re.IGNORECASE),
    ),
    (
        "APR_UTIL_SHA256_URL pin",
        re.compile(r"\bAPR_UTIL_SHA256_URL\b\s*(?::=|\?=|\+=|=)\s*['\"]?https?://", re.IGNORECASE),
    ),
    (
        "versioned APR-util archive",
        re.compile(r"\bapr-util-\d+(?:\.\d+)+\.tar\.bz2(?:\.sha256)?\b", re.IGNORECASE),
    ),
    (
        "legacy APR-util pin alias",
        re.compile(
            r"\bAPR_UTIL_PINNED_(?:VERSION|URL|SHA256|SHA256_URL)\b",
            re.IGNORECASE,
        ),
    ),
)


def static_hits(text: str) -> list[str]:
    """Return the static APR-util pin categories found in one text payload."""

    return [label for label, pattern in STATIC_PATTERNS if pattern.search(text)]


def approved_paths() -> dict[str, str]:
    """Load exact historical-record exceptions with their review rationale."""

    entries: dict[str, str] = {}
    for raw_line in ALLOWLIST_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        relative_path, separator, rationale = line.partition(" | ")
        if not separator or not rationale.strip():
            raise AssertionError(f"invalid APR-util allowlist entry: {raw_line!r}")
        candidate = Path(relative_path)
        if candidate.is_absolute() or ".." in candidate.parts or any(token in relative_path for token in "*?["):
            raise AssertionError(f"allowlist entry must name one exact Parent file: {relative_path}")
        if relative_path in entries:
            raise AssertionError(f"duplicate APR-util allowlist entry: {relative_path}")
        entries[relative_path] = rationale.strip()
    return entries


def iter_parent_text_files() -> list[Path]:
    """Inspect every deliverable Parent file, including untracked candidates.

    Git's tracked-plus-unignored candidate set keeps machine-local ignored
    control-plane evidence out of the delivery contract without exempting any
    hidden source directory.  Tracked `.github`, `.codex` (if ever versioned),
    and other dotfiles remain subject to the same fail-closed scan.
    """

    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    files: list[Path] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        relative_path = Path(raw_path.decode("utf-8", errors="strict"))
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise AssertionError(f"Git returned unsafe Parent candidate path: {relative_path}")
        path = ROOT / relative_path
        if not path.is_file() or "__pycache__" in relative_path.parts:
            continue
        try:
            path.relative_to(FRAMEWORK_ROOT)
        except ValueError:
            files.append(path)
    return files


class AprUtilStaticContractTests(unittest.TestCase):
    def test_scanner_recognizes_each_prohibited_static_form(self) -> None:
        version = "9.8.7"
        digest = "a" * 64
        sample = "\n".join(
            (
                "APR_UTIL_VERSION = '" + version + "'",
                "APR_UTIL_SHA256 = '" + digest + "'",
                "APR_UTIL_SOURCE_URL = '" + "https://fixture.invalid/apr-util-" + version + ".tar.bz2'",
                "APR_UTIL_SHA256_URL = '" + "https://fixture.invalid/apr-util-" + version + ".tar.bz2.sha256'",
                "https://fixture.invalid/apr-util-" + version + ".tar.bz2.sha256",
                "APR_UTIL_PINNED_" + "VERSION",
            )
        )
        self.assertEqual(
            static_hits(sample),
            [
                "APR_UTIL_VERSION pin",
                "APR_UTIL_SHA256 pin",
                "APR_UTIL_SOURCE_URL pin",
                "APR_UTIL_SHA256_URL pin",
                "versioned APR-util archive",
                "legacy APR-util pin alias",
            ],
        )

    def test_scanner_recognizes_makefile_assignment_variants(self) -> None:
        digest = "b" * 64
        version = "9.8" + ".7"
        for operator in ("=", ":=", "?=", "+="):
            with self.subTest(operator=operator):
                sample = "\n".join(
                    (
                        f"APR_UTIL_VERSION {operator} {version}",
                        f"APR_UTIL_SHA256 {operator} {digest}",
                        f"APR_UTIL_SOURCE_URL {operator} https://fixture.invalid/apr-util-{version}.tar.bz2",
                        f"APR_UTIL_SHA256_URL {operator} https://fixture.invalid/apr-util-{version}.tar.bz2.sha256",
                    )
                )
                self.assertEqual(
                    static_hits(sample),
                    [
                        "APR_UTIL_VERSION pin",
                        "APR_UTIL_SHA256 pin",
                        "APR_UTIL_SOURCE_URL pin",
                        "APR_UTIL_SHA256_URL pin",
                        "versioned APR-util archive",
                    ],
                )

    def test_allowlist_is_exact_existing_historical_evidence(self) -> None:
        for relative_path, rationale in approved_paths().items():
            with self.subTest(path=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.is_file(), f"allowlisted path is missing: {relative_path}")
                self.assertGreaterEqual(len(rationale), 20)
                self.assertTrue(
                    static_hits(path.read_text(encoding="utf-8", errors="replace")),
                    f"allowlisted path no longer contains a static APR-util record: {relative_path}",
                )

    def test_scan_uses_git_delivery_candidates_without_hidden_directory_exemptions(self) -> None:
        candidates = {path.relative_to(ROOT).as_posix() for path in iter_parent_text_files()}
        self.assertIn("tests/test_apr_util_static_contract.py", candidates)
        self.assertIn("tests/fixtures/apr-util-static-allowlist.txt", candidates)
        self.assertIn(".github/workflows/ci-security-workflow-lint.yml", candidates)

    def test_parent_has_no_unapproved_static_apr_util_tuple(self) -> None:
        approved = approved_paths()
        violations: list[str] = []
        for path in iter_parent_text_files():
            relative_path = path.relative_to(ROOT).as_posix()
            hits = static_hits(path.read_text(encoding="utf-8", errors="replace"))
            if hits and relative_path not in approved:
                violations.append(f"{relative_path}: {', '.join(hits)}")
        self.assertEqual(
            violations,
            [],
            "Parent APR-util pins must be Framework-owned; add only an exact historical "
            "record to the reviewed allowlist when retention is required.",
        )


if __name__ == "__main__":
    unittest.main()
