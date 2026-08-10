from __future__ import annotations

import unittest

from tests.c_source_contract import function_definition, matching_delimiter


class CSourceContractTests(unittest.TestCase):
    def test_matching_delimiter_supports_nested_pairs(self) -> None:
        source = "call(one, nested(two));"
        self.assertEqual(
            matching_delimiter(source, source.index("("), "(", ")"),
            source.rindex(")"),
        )

    def test_matching_delimiter_reports_unterminated_pair(self) -> None:
        with self.assertRaisesRegex(AssertionError, r"unterminated \{\} pair"):
            matching_delimiter("{ nested", 0, "{", "}")

    def test_function_definition_ignores_prototype_and_call(self) -> None:
        source = """\
int candidate(int value);
int candidate(int value) {
    if (value) {
        return value;
    }
    return 0;
}
void caller(void) {
    candidate(1);
}
"""
        definition = function_definition(source, "candidate")
        self.assertTrue(definition.startswith("int candidate(int value) {"))
        self.assertTrue(definition.endswith("\n}"))
        self.assertIn("if (value) {", definition)

    def test_function_definition_does_not_match_related_names(self) -> None:
        source = """\
int candidate_helper(void) {
    return 1;
}
"""
        with self.assertRaisesRegex(
            AssertionError, r"candidate definition was not found"
        ):
            function_definition(source, "candidate")

    def test_function_definition_reports_missing_definition(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, r"candidate definition was not found"
        ):
            function_definition("void caller(void) { candidate(1); }", "candidate")
