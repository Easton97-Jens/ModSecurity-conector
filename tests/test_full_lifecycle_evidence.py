from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SANITIZER_SPEC = importlib.util.spec_from_file_location(
    "sanitize_full_lifecycle_log", ROOT / "ci/sanitize-full-lifecycle-log.py"
)
assert SANITIZER_SPEC is not None and SANITIZER_SPEC.loader is not None
sanitizer = importlib.util.module_from_spec(SANITIZER_SPEC)
SANITIZER_SPEC.loader.exec_module(sanitizer)

CHECKER_SPEC = importlib.util.spec_from_file_location(
    "check_full_lifecycle_evidence", ROOT / "ci/check-full-lifecycle-evidence.py"
)
assert CHECKER_SPEC is not None and CHECKER_SPEC.loader is not None
checker = importlib.util.module_from_spec(CHECKER_SPEC)
CHECKER_SPEC.loader.exec_module(checker)


class FullLifecycleEvidenceTest(unittest.TestCase):
    def test_log_sanitizer_drops_fixture_bodies_and_credentials(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-lifecycle-log-") as temporary:
            root = Path(temporary)
            source = root / "raw.log"
            destination = root / "canonical.log"
            source.write_text(
                "Authorization: Bearer private-token\n"
                "response=no-crs-response-body-marker\n"
                "normal diagnostic\n",
                encoding="utf-8",
            )
            self.assertEqual(0, sanitizer.main([
                "--input", str(source), "--output", str(destination), "--label", "unit",
            ]))
            text = destination.read_text(encoding="utf-8")
            self.assertNotIn("private-token", text)
            self.assertNotIn("no-crs-response-body-marker", text)
            self.assertIn("[body payload line omitted]", text)
            self.assertIn("normal diagnostic", text)

    def test_first_byte_promotion_requires_causal_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-lifecycle-evidence-") as temporary:
            root = Path(temporary)
            run = root / "run"
            run.mkdir()
            (run / "events.jsonl").write_text(
                '{"rule_id":1100301,"phase":4,"first_byte_before_response_end":true,'
                '"upstream_response_finished_at_first_byte":false}\n',
                encoding="utf-8",
            )
            (run / "results.jsonl").write_text(
                '{"case_id":"phase4_first_byte_before_response_end","status":"PASS",'
                '"expected_rule_id":1100301}\n'
                '{"case_id":"phase4_no_full_response_buffering","status":"PASS",'
                '"expected_rule_id":1100301}\n',
                encoding="utf-8",
            )
            manifest = {"capabilities": {"first_byte_before_response_end": {"state": "verified"}}}
            result = {"artifact_profile": "full_lifecycle", "capabilities_verified": ["first_byte_before_response_end"]}
            errors = checker.first_byte_errors(run, manifest, result)
            self.assertEqual(
                [
                    "phase4_first_byte_before_response_end: missing synchronized first-byte event metadata",
                    "phase4_no_full_response_buffering: missing synchronized first-byte event metadata",
                ],
                errors,
            )


if __name__ == "__main__":
    unittest.main()
