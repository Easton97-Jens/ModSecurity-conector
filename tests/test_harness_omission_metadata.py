"""Explicit optional response omission survives only the closed fixture seam."""
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("omission_case_metadata", Path(__file__).resolve().parents[1] / "ci/runtime/common/harness-case-metadata.py")
META = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(META)


class HarnessOmissionMetadataTest(unittest.TestCase):
    def test_closed_explicit_omission_is_forwarded(self):
        fixture = META.response_fixture({"response": {"content_type": None, "omit_headers": ["Content-Type"]}})
        self.assertEqual(fixture, {"status": 200, "headers": [], "omit_headers": ["Content-Type"]})

    def test_default_fixture_shape_and_other_headers_are_unchanged(self):
        self.assertEqual(META.response_fixture({}), {"status": 200, "headers": []})
        self.assertEqual(META.response_fixture({"response": {"content_type": "text/plain"}}),
                         {"status": 200, "headers": [["Content-Type", "text/plain"]]})

    def test_invalid_or_conflicting_omission_does_not_reach_backend(self):
        for response in ({"omit_headers": ["Content-Length"]},
                         {"content_type": "", "omit_headers": ["Content-Type"]},
                         {"headers": {"content-type": ""}, "omit_headers": ["Content-Type"]}):
            with self.subTest(response=response), self.assertRaises(ValueError):
                META.response_fixture({"response": response})

# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)
