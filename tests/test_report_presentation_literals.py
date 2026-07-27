from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_report_module(relative_path: str, module_name: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


BODY_PROCESSOR = load_report_module(
    "ci/evidence/reports/generate-body-processor-analysis.py",
    "body_processor_analysis_presentation_test",
)
RULE_CHAIN = load_report_module(
    "ci/evidence/reports/generate-rule-chain-semantics-analysis.py",
    "rule_chain_semantics_presentation_test",
)
FULL_RUNTIME_MATRIX = load_report_module(
    "ci/evidence/reports/generate-full-runtime-matrix.py",
    "full_runtime_matrix_presentation_test",
)


class DefaultValues(dict[str, object]):
    def __missing__(self, key: str) -> object:
        return 0


def empty_subcluster(distribution_keys: tuple[str, ...]) -> DefaultValues:
    values = DefaultValues()
    values.update({key: {} for key in distribution_keys})
    return values


def empty_body_processor_report() -> dict[str, object]:
    urlencoded = empty_subcluster(
        (
            "connectors",
            "variants",
            "case_ids",
            "rule_ids",
            "targets",
            "operators",
            "body_lengths",
            "request_body_seen",
        )
    )
    xml_activation = empty_subcluster(
        (
            "connectors",
            "variants",
            "case_ids",
            "rule_ids",
            "targets",
            "operators",
            "content_types",
            "body_lengths",
            "body_hashes",
            "request_body_seen",
        )
    )
    multipart_activation = empty_subcluster(
        (
            "connectors",
            "variants",
            "case_ids",
            "rule_ids",
            "targets",
            "operators",
            "content_types",
            "boundaries",
            "boundary_status",
            "part_counts",
            "field_names",
            "filenames",
            "body_lengths",
            "body_hashes",
            "request_body_seen",
        )
    )
    return {
        "generated_at": "2026-07-27T00:00:00Z",
        "summary": DefaultValues(
            {
                "before_metadata_fix": DefaultValues(),
                "after_metadata_fix": DefaultValues(),
            }
        ),
        "selected_subcluster": DefaultValues(),
        "urlencoded_form_subcluster": urlencoded,
        "xml_activation_missing_subcluster": xml_activation,
        "multipart_activation_missing_subcluster": multipart_activation,
        "distribution": {
            "connectors": [],
            "variants": [],
            "body_kinds": [],
            "content_types": [],
            "targets": [],
            "failure_categories": [],
        },
        "groups": [],
        "next_fix_plan": DefaultValues(),
    }


def empty_rule_chain_report() -> dict[str, object]:
    summary_keys = (
        "rule_chain_failure_rows",
        "rule_chain_case_groups",
        "small_single_connector_failure_groups",
        "small_single_connector_failure_rows",
        "runtime_fixable_candidates",
        "report_only_items",
        "chain_parent_matched_rows",
        "chain_child_matched_rows",
        "full_chain_matched_rows",
        "chain_named_non_rule_chain_rows",
    )
    return {
        "generated_at": "2026-07-27T00:00:00Z",
        "summary": {key: 0 for key in summary_keys},
        "conclusion": {
            "selected_subcluster": "report-only",
            "root_cause": "none",
            "safe_change": "none",
        },
        "rule_chain_failures": [],
        "chain_named_non_rule_chain_failures": [],
        "small_single_connector_failures": [],
        "next_recommendation": {},
    }


class ReportPresentationLiteralsTest(unittest.TestCase):
    def test_body_processor_distribution_headers_remain_byte_exact(self) -> None:
        markdown = BODY_PROCESSOR.render_markdown(empty_body_processor_report())

        self.assertEqual(BODY_PROCESSOR.DISTRIBUTION_TABLE_HEADER, "| field | distribution |")
        self.assertEqual(BODY_PROCESSOR.DISTRIBUTION_TABLE_SEPARATOR, "| --- | --- |")
        self.assertEqual(markdown.count(BODY_PROCESSOR.DISTRIBUTION_TABLE_HEADER), 3)
        self.assertEqual(
            markdown.count(
                f"{BODY_PROCESSOR.DISTRIBUTION_TABLE_HEADER}\n"
                f"{BODY_PROCESSOR.DISTRIBUTION_TABLE_SEPARATOR}"
            ),
            3,
        )

    def test_rule_chain_empty_sections_remain_byte_exact(self) -> None:
        markdown = RULE_CHAIN.render_markdown(empty_rule_chain_report())

        self.assertEqual(RULE_CHAIN.NO_ROWS_MARKDOWN, "- None.")
        self.assertEqual(markdown.count(RULE_CHAIN.NO_ROWS_MARKDOWN), 3)

    def test_full_runtime_matrix_utc_offset_remains_parse_compatible(self) -> None:
        self.assertEqual(FULL_RUNTIME_MATRIX._UTC_OFFSET, "+00:00")
        self.assertEqual(
            FULL_RUNTIME_MATRIX.parse_time("2026-07-27T00:00:00Z"),
            datetime(2026, 7, 27, tzinfo=timezone.utc),
        )
        self.assertEqual(
            FULL_RUNTIME_MATRIX.duration_seconds(
                "2026-07-27T00:00:00Z",
                "2026-07-27T00:01:00Z",
            ),
            60,
        )
