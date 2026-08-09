from __future__ import annotations

from pathlib import Path
import re
import unittest

from tests.c_source_contract import function_definition


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_module.c"


class NginxInterventionUrlOwnershipTests(unittest.TestCase):
    def setUp(self) -> None:
        module = MODULE.read_text(encoding="utf-8")
        self.intervention = function_definition(
            module, "ngx_http_modsecurity_process_intervention"
        )
        self.redirect = function_definition(
            module, "ngx_http_modsecurity_process_redirect_intervention"
        )

    def test_intervention_is_initialized_and_cleaned_once(self) -> None:
        self.assertIn("ngx_memzero(&intervention, sizeof(intervention));", self.intervention)
        self.assertIn("intervention.status = 200;", self.intervention)
        self.assertNotIn("free(intervention.log)", self.intervention)
        self.assertEqual(
            self.intervention.count("msc_intervention_cleanup(&intervention);"), 1
        )

        cleanup = self.intervention.index("msc_intervention_cleanup(&intervention);")
        self.assertNotIn("intervention.url", self.intervention[cleanup:])
        self.assertNotIn("intervention.log", self.intervention[cleanup:])
        self.assertEqual(
            re.findall(r"\breturn\s+[^;]+;", self.intervention),
            ["return result;"],
        )

    def test_redirect_location_is_owned_before_the_wrapper_cleans_up(self) -> None:
        self.assertIn(
            "if (intervention.url != NULL && intervention.url[0] != '\\0')",
            self.intervention,
        )
        call = self.intervention.index(
            "result = ngx_http_modsecurity_process_redirect_intervention"
        )
        cleanup = self.intervention.index("msc_intervention_cleanup(&intervention);")
        self.assertLess(call, cleanup)
        self.assertIn("goto cleanup;", self.intervention[call:cleanup])

        self.assertIn("location_value.len = ngx_strlen(intervention->url);", self.redirect)
        self.assertIn(
            "redirect_url = (const u_char *) intervention->url;", self.redirect
        )
        self.assertIn(
            "if (redirect_url[i] == '\\r' || redirect_url[i] == '\\n')",
            self.redirect,
        )
        self.assertIn("if (location_value.len > NGX_MAX_SIZE_T_VALUE - 1U)", self.redirect)
        self.assertIn(
            "location_value.data = ngx_pnalloc(r->pool, location_value.len + 1U);",
            self.redirect,
        )
        self.assertIn(
            "ngx_memcpy(location_value.data, intervention->url, location_value.len);",
            self.redirect,
        )
        self.assertIn("location_value.data[location_value.len] = '\\0';", self.redirect)
        self.assertIn("location->value = location_value;", self.redirect)
        self.assertNotIn("location->value = a;", self.redirect)
        self.assertNotIn("(unsigned char *)intervention.url", self.redirect)

        self.assertLess(
            self.redirect.index("location_value.data = ngx_pnalloc"),
            self.redirect.index("location->value = location_value;"),
        )
        crlf_rejection = self.redirect.index(
            "if (redirect_url[i] == '\\r' || redirect_url[i] == '\\n')"
        )
        self.assertIn("return NGX_HTTP_BAD_REQUEST;", self.redirect[crlf_rejection:])
        self.assertLess(
            crlf_rejection, self.redirect.index("location_value.data = ngx_pnalloc")
        )
        self.assertLess(
            crlf_rejection, self.redirect.index("location->value = location_value;")
        )

    def test_redirect_helper_reports_failures_to_the_cleanup_wrapper(self) -> None:
        expected_returns = {
            "if (r->header_sent)": "return -1;",
            "if (location_value.len > NGX_MAX_SIZE_T_VALUE - 1U)": (
                "return NGX_HTTP_INTERNAL_SERVER_ERROR;"
            ),
            "if (redirect_url[i] == '\\r' || redirect_url[i] == '\\n')": (
                "return NGX_HTTP_BAD_REQUEST;"
            ),
            "if (location_value.data == NULL)": "return NGX_HTTP_INTERNAL_SERVER_ERROR;",
            "if (location == NULL)": "return NGX_HTTP_INTERNAL_SERVER_ERROR;",
        }
        for condition, result in expected_returns.items():
            with self.subTest(condition=condition):
                start = self.redirect.index(condition)
                self.assertIn(result, self.redirect[start:])

        self.assertIn("ngx_http_clear_location(r);", self.redirect)
        self.assertIn("return intervention->status;", self.redirect)


if __name__ == "__main__":
    unittest.main()
