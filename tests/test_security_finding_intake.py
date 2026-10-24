"""Consistency checks for the source-ID intake; not security verification."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "reports/audits/findings/20260929-intake.json"


class FindingIntakeTests(unittest.TestCase):
    def test_originals_are_preserved_once_and_dedupe_is_complete(self) -> None:
        intake = json.loads(INTAKE.read_text(encoding="utf-8"))
        rows = intake["originals"]
        expected = {
            f"{prefix}{number:02}"
            for prefix, count in (("A", 21), ("B", 27), ("C", 24))
            for number in range(1, count + 1)
        }
        aliases = [row["alias"] for row in rows]
        self.assertEqual(len(aliases), len(set(aliases)))
        self.assertEqual(set(aliases), expected)
        self.assertEqual(len(rows), intake["source_counts"]["original"])
        mapped = {key for row in rows for key in row["work_items"]}
        self.assertEqual(mapped, set(intake["canonical_work_items"]))
        self.assertEqual(len(mapped), intake["source_counts"]["work_items"])
        self.assertEqual(len(mapped), 59)
        self.assertTrue(all(row["source_id"] for row in rows))
        self.assertTrue(all(row["reported_severity"] in
                            {"high", "medium", "low", "informational"} for row in rows))
        by_alias = {row["alias"]: row for row in rows}
        self.assertEqual(by_alias["A08"]["work_items"], ["B01", "B15"])
        self.assertEqual(by_alias["C20"]["work_items"], ["C19"])

    def test_intake_does_not_claim_unperformed_verification(self) -> None:
        intake = json.loads(INTAKE.read_text(encoding="utf-8"))
        self.assertEqual(set(intake["parent_changes"]), {"B09"})
        self.assertEqual(intake["parent_changes"]["B09"]["implementation"],
                         "candidate_patch")
        self.assertEqual(intake["parent_changes"]["B09"]["verification"], "pending")
        self.assertIn("not_changed_in_this_draft", intake["remaining_work_items"])
        self.assertIn("MRTS root cause unchanged", intake["external_work"]["B03"])


if __name__ == "__main__":
    unittest.main()
