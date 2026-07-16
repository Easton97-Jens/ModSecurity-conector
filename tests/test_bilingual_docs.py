#!/usr/bin/env python3
"""Unit tests for the repository bilingual-documentation checker."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "ci" / "checks" / "documentation" / "check-bilingual-docs.py"
SPEC = importlib.util.spec_from_file_location("bilingual_docs_checker", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class BilingualDocumentationCheckerTests(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str) -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_docs_require_matching_heading_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write(
                root,
                "docs/example.md",
                "# Example\n\n**Language:** English | [Deutsch](example.de.md)\n\n## Details\n",
            )
            self.write(
                root,
                "docs/example.de.md",
                "# Beispiel\n\n**Sprache:** [English](example.md) | Deutsch\n\n### Details\n",
            )

            errors = CHECKER.check_pairs_and_switches(root)

        self.assertTrue(any("heading-level structure differs" in error for error in errors))

    def test_license_documents_require_german_companions(self) -> None:
        self.assertTrue(CHECKER.pair_required(Path("licenses/README.md")))

    def test_fenced_code_blocks_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write(
                root,
                "docs/example.md",
                "# Example\n\n**Language:** English | [Deutsch](example.de.md)\n\n```sh\necho English\n```\n",
            )
            self.write(
                root,
                "docs/example.de.md",
                "# Beispiel\n\n**Sprache:** [English](example.md) | Deutsch\n\n```sh\necho Deutsch\n```\n",
            )

            errors = CHECKER.check_pairs_and_switches(root)

        self.assertTrue(any("fenced code-block content differs" in error for error in errors))

    def test_rejects_local_german_companions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write(root, "AGENTS.de.md", "# Verboten\n")

            errors = CHECKER.check_forbidden_local_language_companions(root)

        self.assertEqual(
            ["AGENTS.de.md: local Codex configuration must not have a German companion"],
            errors,
        )

    def test_ignored_local_markdown_is_not_repository_owned_documentation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write(root, "local.md", "# Local control file\n")

            with patch.object(
                CHECKER,
                "git_ignored_paths",
                return_value=frozenset({Path("local.md")}),
            ):
                sources = CHECKER.english_sources(root)

        self.assertEqual([], sources)

    def test_agent_referenced_root_markdown_is_not_repository_owned_documentation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write(root, "AGENTS.md", "@local-control.md\n")
            self.write(root, "local-control.md", "# Local control file\n")

            sources = CHECKER.english_sources(root)

        self.assertEqual([], sources)

    def test_pr_template_requires_all_bilingual_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write(root, ".github/pull_request_template.md", "## English\n\n## Deutsch\n")

            errors = CHECKER.check_pr_template(root)

        self.assertTrue(any("English required section" in error for error in errors))
        self.assertTrue(any("Deutsch required section" in error for error in errors))

    def test_change_record_identity_values_must_match(self) -> None:
        english_headings = "\n".join(CHECKER.CHANGE_RECORD_REQUIRED_HEADINGS["English"])
        german_headings = "\n".join(CHECKER.CHANGE_RECORD_REQUIRED_HEADINGS["Deutsch"])
        english = (
            "# Change Record\n\n"
            "**Language:** English | [Deutsch](CR-20260713-example.de.md)\n\n"
            f"{english_headings}\n\n"
            "| Field | Value |\n| --- | --- |\n"
            "| Change ID | CR-20260713-example |\n"
            "| Date (UTC) | 2026-07-13T00:00:00Z |\n"
            "| Base revision | deadbeef |\n"
        )
        german = (
            "# Change Record\n\n"
            "**Sprache:** [English](CR-20260713-example.md) | Deutsch\n\n"
            f"{german_headings}\n\n"
            "| Feld | Wert |\n| --- | --- |\n"
            "| Change-ID | CR-20260713-example |\n"
            "| Datum (UTC) | 2026-07-13T00:00:00Z |\n"
            "| Basis-Revision | differs |\n"
        )

        errors = CHECKER.check_change_record_pair(
            Path("reports/audits/change-records/CR-20260713-example.md"),
            Path("reports/audits/change-records/CR-20260713-example.de.md"),
            english,
            german,
        )

        self.assertTrue(any("Base revision" in error and "differs" in error for error in errors))

    def test_common_design_note_current_contract_passes_for_both_languages(self) -> None:
        self.assertEqual([], CHECKER.check_common_design_note_contract(ROOT))

    def test_common_design_note_rejects_scaffolded_status_and_current_sidecar_route(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            english = (ROOT / "common/docs/design.md").read_text(encoding="utf-8")
            german = (ROOT / "common/docs/design.de.md").read_text(encoding="utf-8")
            self.write(
                root,
                "common/docs/design.md",
                english.replace(
                    "Status: current-boundary reference", "Status: scaffolded"
                ).replace(
                    "| lighttpd | `patched-native-lighttpd` |",
                    "| lighttpd | `sidecar_proxy` |",
                )
                + "\nintegration_mode=sidecar_proxy\n",
            )
            self.write(
                root,
                "common/docs/design.de.md",
                german.replace(
                    "Status: aktuelle Grenzreferenz", "Status: eingerüstet"
                ).replace(
                    "| lighttpd | `patched-native-lighttpd` |",
                    "| lighttpd | `sidecar_proxy` |",
                )
                + "\nintegration_mode=sidecar_proxy\n",
            )

            errors = CHECKER.check_common_design_note_contract(root)

        for relative_path in ("common/docs/design.md", "common/docs/design.de.md"):
            self.assertTrue(
                any(
                    error.startswith(f"{relative_path}:")
                    and "obsolete scaffolded status" in error
                    for error in errors
                )
            )
            self.assertTrue(
                any(
                    error.startswith(f"{relative_path}:")
                    and "selected route for lighttpd" in error
                    for error in errors
                )
            )
            self.assertTrue(
                any(
                    error.startswith(f"{relative_path}:")
                    and "historical integration mode" in error
                    for error in errors
                )
            )

    def test_common_design_note_allows_an_explicitly_historical_compatibility_route(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            english = (ROOT / "common/docs/design.md").read_text(encoding="utf-8")
            german = (ROOT / "common/docs/design.de.md").read_text(encoding="utf-8")
            self.write(
                root,
                "common/docs/design.md",
                english
                + "\nHistorical compatibility material: "
                "integration_mode=sidecar_proxy is compatibility_only.\n",
            )
            self.write(
                root,
                "common/docs/design.de.md",
                german
                + "\nHistorisches Kompatibilitätsmaterial: "
                "integration_mode=sidecar_proxy ist compatibility_only.\n",
            )

            errors = CHECKER.check_common_design_note_contract(root)

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
