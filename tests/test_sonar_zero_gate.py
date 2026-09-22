"""Offline tests for exact-head, read-only Sonar zero-finding enforcement."""
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sonar_zero_gate", ROOT / "ci/checks/common/check-sonar-zero.py"
)
assert SPEC is not None
assert SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)
HEAD = "a" * 40
REPOSITORY = "example/connector"


def make_check(*, head=HEAD, identifier=1, issues=0, hotspots=0, annotations=0,
               accepted=0, status="completed", conclusion="success"):
    return {"id": identifier, "head_sha": head, "name": GATE.CHECK_NAME,
            "app": {"slug": "sonarqubecloud"}, "status": status,
            "conclusion": conclusion,
            "output": {"summary": f"[{issues} New issues] [{accepted} Accepted issues] [{hotspots} Security Hotspots]",
                       "annotations_count": annotations}}


class SonarZeroGateTests(unittest.TestCase):
    def verify(self, checks, annotations=None, attempts=1):
        calls = []
        def fetch(path):
            calls.append(path)
            if "/annotations?" in path:
                return annotations or []
            return {"check_runs": checks}
        with redirect_stdout(io.StringIO()):
            evidence = GATE.verify(REPOSITORY, HEAD, fetch,
                                   sleep=lambda seconds: None, attempts=attempts)
        return evidence, calls

    def test_explicit_zero_for_exact_head_passes(self):
        evidence, calls = self.verify([make_check()])
        self.assertEqual(evidence["head_sha"], HEAD)
        self.assertEqual(evidence["new_issues"], 0)
        self.assertEqual(evidence["accepted_issues"], 0)
        self.assertEqual(len(calls), 1)

    def test_green_quality_gate_with_new_issues_fails(self):
        checks = [make_check(issues=2)]
        with self.assertRaisesRegex(GATE.GateError, "zero new issues"):
            self.verify(checks)

    def test_hotspots_fail_even_without_issues(self):
        checks = [make_check(hotspots=1)]
        with self.assertRaises(GATE.GateError):
            self.verify(checks)

    def test_annotations_cannot_be_hidden_by_zero_summary(self):
        checks = [make_check(annotations=1)]
        with self.assertRaises(GATE.GateError):
            self.verify(checks)

    def test_old_head_cannot_satisfy_the_gate(self):
        checks = [make_check(head="b" * 40)]
        with self.assertRaisesRegex(GATE.GateError, "exact PR head"):
            self.verify(checks)

    def test_new_pending_analysis_supersedes_old_success(self):
        checks = [make_check(), make_check(identifier=2, status="in_progress")]
        with self.assertRaises(GATE.GateError):
            self.verify(checks)

    def test_missing_analysis_does_not_pass(self):
        with self.assertRaises(GATE.GateError):
            self.verify([])

    def test_wrong_check_provider_cannot_supply_evidence(self):
        check = make_check()
        check["app"]["slug"] = "another-app"
        with self.assertRaises(GATE.GateError):
            self.verify([check])

    def test_failed_analysis_with_zero_findings_still_fails(self):
        checks = [make_check(conclusion="failure")]
        with self.assertRaises(GATE.GateError):
            self.verify(checks)

    def test_missing_or_ambiguous_summary_fails(self):
        for summary in ("Quality Gate passed", "0 New issues 1 New issues 0 Security Hotspots"):
            with self.subTest(summary=summary):
                check = make_check()
                check["output"]["summary"] = summary
                with self.assertRaises(GATE.GateError):
                    self.verify([check])

    def test_invalid_identity_stops_before_network(self):
        def forbidden_fetch(path):
            self.fail("invalid input reached the network")
        for repository, head in (("../foreign", HEAD), ("example/..", HEAD),
                                 ("example/name/extra", HEAD), (REPOSITORY, "branch-name")):
            with self.subTest(repository=repository, head=head):
                with self.assertRaises(GATE.GateError):
                    GATE.verify(repository, head, forbidden_fetch)

    def test_annotation_output_is_bounded_and_command_inert(self):
        output = io.StringIO()
        annotation = {"path": "file.c", "start_line": 9,
                      "title": "issue", "message": "\n::error::" + "x" * 2000,
                      "raw_details": "source-must-not-be-printed"}
        with redirect_stdout(output):
            GATE.report_findings(REPOSITORY, 7, lambda path: [annotation])
        text = output.getvalue()
        self.assertEqual(len(text.splitlines()), 1)
        self.assertTrue(text.startswith("sonar finding: "))
        self.assertNotIn("source-must-not-be-printed", text)
        self.assertLess(len(text), 700)

    def test_singular_finding_is_reported_then_rejected(self):
        check = make_check(issues=1, annotations=1)
        check["output"]["summary"] = "[1 New issue] [0 Accepted issues] [0 Security Hotspots]"
        output = io.StringIO()
        calls = []
        def fetch(path):
            calls.append(path)
            if "/annotations?" in path:
                return [{"path": "file.c", "message": "actual finding"}]
            return {"check_runs": [check]}
        with redirect_stdout(output), self.assertRaisesRegex(GATE.GateError, "zero new issues"):
            GATE.verify(REPOSITORY, HEAD, fetch, attempts=1)
        self.assertEqual(len(calls), 2)
        self.assertIn("actual finding", output.getvalue())
        self.assertIn('"new_issues": 1', output.getvalue())

    def test_accepted_findings_cannot_make_the_gate_green(self):
        for summary in ("[0 New issues] [1 Accepted issue] [0 Security Hotspots]",
                        "[0 New issues] [2 Accepted issues] [0 Security Hotspots]"):
            with self.subTest(summary=summary):
                check = make_check()
                check["output"]["summary"] = summary
                with self.assertRaisesRegex(GATE.GateError, "zero new issues"):
                    self.verify([check])

    def test_singular_and_plural_cannot_hide_ambiguous_counts(self):
        check = make_check()
        check["output"]["summary"] += " [1 New issue]"
        with self.assertRaisesRegex(GATE.GateError, "ambiguous"):
            self.verify([check])

    def test_missing_accepted_count_is_not_assumed_zero(self):
        check = make_check()
        check["output"]["summary"] = "[0 New issues] [0 Security Hotspots]"
        with self.assertRaisesRegex(GATE.GateError, "Accepted issues"):
            self.verify([check])


if __name__ == "__main__":
    unittest.main()
