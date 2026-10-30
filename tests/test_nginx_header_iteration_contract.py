"""Regression contract for shared NGINX header-list traversal."""

from pathlib import Path
import unittest

from tests.c_source_contract import function_definition


ROOT = Path(__file__).resolve().parents[1]
NGINX_SRC = ROOT / "connectors" / "nginx" / "src"
COMMON = NGINX_SRC / "ngx_http_modsecurity_common.h"
ACCESS = NGINX_SRC / "ngx_http_modsecurity_access.c"
HEADER_FILTER = NGINX_SRC / "ngx_http_modsecurity_header_filter.c"


class NginxHeaderIterationContractTest(unittest.TestCase):
    def test_request_and_response_paths_share_chained_list_iterator(self):
        common = COMMON.read_text(encoding="utf-8")
        access = ACCESS.read_text(encoding="utf-8")
        response = HEADER_FILTER.read_text(encoding="utf-8")

        self.assertIn(
            "return &(*data)[(*index)++];",
            function_definition(common, "ngx_http_modsecurity_next_header"),
        )
        self.assertIn(
            "ngx_http_modsecurity_next_header(&part, &data,",
            function_definition(common, "ngx_http_modsecurity_http3_authority"),
        )
        self.assertIn("while ((header = ngx_http_modsecurity_next_header(", access)
        self.assertIn("while ((header = ngx_http_modsecurity_next_header(", response)
        self.assertNotIn("ngx_http_modsecurity_advance_request_header_part", access)
        response_headers = response[
            response.index("ngx_http_modsecurity_add_response_headers") :
        ]
        self.assertNotIn("part = part->next;", response_headers.split(
            "ngx_http_modsecurity_response_header_metrics", 1
        )[0])

    def test_iterator_advances_index_before_chained_parts(self):
        common = COMMON.read_text(encoding="utf-8")

        self.assertIn("return &(*data)[(*index)++];", common)
        self.assertIn("if ((*part)->next == NULL)", common)
        self.assertIn("*data = (*part)->elts;", common)
        self.assertIn("*index = 0U;", common)



# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == "__main__":
    unittest.main()
