"""Response-inspection fixtures own both native policy directives explicitly."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ResponseLimitFixtureContract(unittest.TestCase):
    def test_each_inspecting_rule_fixture_has_limit_and_action(self):
        paths = list((ROOT / "common/rules").glob("*.conf"))
        paths += list((ROOT / "examples").glob("*/rules/*.conf"))
        paths += list((ROOT / "ci/runtime/lifecycle/cases/apache-phase4-response").glob("*.yaml"))
        inspecting = 0
        for path in paths:
            text = path.read_text()
            if not re.search(r"^\s*SecResponseBodyAccess On\s*$", text, re.M):
                continue
            inspecting += 1
            with self.subTest(fixture=str(path.relative_to(ROOT))):
                self.assertRegex(text, r"(?m)^\s*SecResponseBodyLimit [1-9][0-9]*\s*$")
                self.assertRegex(text, r"(?m)^\s*SecResponseBodyLimitAction (Reject|ProcessPartial)\s*$")
        self.assertGreater(inspecting, 0)

    def test_examples_do_not_reintroduce_removed_connector_options(self):
        removed = re.compile(r"(?m)^\s*(response_body_limit|response-body-limit)\s*=|\"max_response_body_bytes\"\s*:")
        for path in (ROOT / "examples").rglob("*"):
            if path.is_file() and path.suffix in (".conf", ".json"):
                with self.subTest(example=str(path.relative_to(ROOT))):
                    self.assertIsNone(removed.search(path.read_text()))


if __name__ == "__main__":
    unittest.main()
