from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "ci" / "evidence" / "reports" / "generate-remaining-failure-analysis.py"
SPEC = importlib.util.spec_from_file_location("remaining_failure_analysis", GENERATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
GENERATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GENERATOR
SPEC.loader.exec_module(GENERATOR)


class RemainingFailureAnalysisTest(unittest.TestCase):
    def test_category_rollup_keeps_typical_examples_without_discarded_summary_reads(self) -> None:
        category = GENERATOR.FAILURE_CATEGORIES[0]
        with (
            mock.patch.object(GENERATOR, "failure_category", return_value=category),
            mock.patch.object(
                GENERATOR,
                "case_group_summary",
                side_effect=AssertionError("discarded summary reads must not run"),
            ),
            mock.patch.object(GENERATOR, "example_entry", return_value={"case_id": "case-1"}),
        ):
            rows = GENERATOR.category_rollup([{"case_id": "case-1", "connector": "apache"}])

        selected = next(row for row in rows if row["category"] == category)
        self.assertEqual(selected["typical_examples"], [{"case_id": "case-1"}])
        self.assertEqual(selected["count"], 1)
