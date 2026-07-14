from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_module.c"


def process_intervention_body(source: str) -> str:
    signature = "int\nngx_http_modsecurity_process_intervention "
    start = source.index(signature)
    opening_brace = source.index("{", start)
    depth = 0
    for index in range(opening_brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise AssertionError("ngx_http_modsecurity_process_intervention is incomplete")


class NginxInterventionUrlOwnershipTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = process_intervention_body(MODULE.read_text(encoding="utf-8"))

    def test_intervention_is_initialized_and_cleaned_once(self) -> None:
        self.assertIn("ngx_memzero(&intervention, sizeof(intervention));", self.source)
        self.assertIn("intervention.status = 200;", self.source)
        self.assertNotIn("free(intervention.log)", self.source)
        self.assertEqual(1, self.source.count("msc_intervention_cleanup(&intervention);"))

        cleanup = self.source.index("msc_intervention_cleanup(&intervention);")
        self.assertNotIn("intervention.url", self.source[cleanup:])
        self.assertNotIn("intervention.log", self.source[cleanup:])

        returns = re.findall(r"\breturn\s+[^;]+;", self.source)
        self.assertEqual(["return result;"], returns)

    def test_redirect_url_is_a_request_pool_copy_before_cleanup(self) -> None:
        self.assertIn(
            "if (intervention.url != NULL && intervention.url[0] != '\\0')",
            self.source,
        )
        self.assertIn(
            "location_value.data = ngx_pnalloc(r->pool, location_value.len + 1U);",
            self.source,
        )
        self.assertIn(
            "if (location_value.len > NGX_MAX_SIZE_T_VALUE - 1)",
            self.source,
        )
        self.assertIn(
            "ngx_memcpy(location_value.data, intervention.url, location_value.len);",
            self.source,
        )
        self.assertIn("location_value.data[location_value.len] = '\\0';", self.source)
        self.assertIn("location->value = location_value;", self.source)
        self.assertNotIn("location->value = a;", self.source)
        self.assertNotIn("(unsigned char *)intervention.url", self.source)

        assignment = self.source.index("location->value = location_value;")
        cleanup = self.source.index("msc_intervention_cleanup(&intervention);")
        self.assertLess(assignment, cleanup)

    def test_failure_branches_funnel_through_cleanup(self) -> None:
        for condition in (
            "if (ctx == NULL)",
            "if (mcf == NULL)",
            "if (r->header_sent)",
            "if (location_value.len > NGX_MAX_SIZE_T_VALUE - 1)",
            "if (location_value.data == NULL)",
            "if (location == NULL)",
        ):
            with self.subTest(condition=condition):
                self.assertIn(condition, self.source)
                branch = self.source[self.source.index(condition) :]
                self.assertIn("goto cleanup;", branch.split("}", 1)[0])

        self.assertIn("result = NGX_HTTP_INTERNAL_SERVER_ERROR;", self.source)
        self.assertIn("result = intervention.status;", self.source)


if __name__ == "__main__":
    unittest.main()
