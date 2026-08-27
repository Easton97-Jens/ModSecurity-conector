from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from tests.c_source_contract import function_definition, matching_delimiter


ROOT = Path(__file__).resolve().parents[1]
NGINX_SOURCE = ROOT / "connectors" / "nginx" / "src"
ACCESS = NGINX_SOURCE / "ngx_http_modsecurity_access.c"
BODY = NGINX_SOURCE / "ngx_http_modsecurity_body_filter.c"
COMMON = NGINX_SOURCE / "ngx_http_modsecurity_common.h"
HEADER = NGINX_SOURCE / "ngx_http_modsecurity_header_filter.c"
MODULE = NGINX_SOURCE / "ngx_http_modsecurity_module.c"
CAPABILITIES = ROOT / "connectors" / "nginx" / "capabilities.json"


def conditional_block(source: str, marker: str, start: int = 0) -> str:
    condition = source.index(marker, start)
    opening = source.index("{", condition)
    return source[condition : matching_delimiter(source, opening, "{", "}") + 1]


class NginxUpstreamSecurityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.access = ACCESS.read_text(encoding="utf-8")
        cls.body = BODY.read_text(encoding="utf-8")
        cls.common = COMMON.read_text(encoding="utf-8")
        cls.header = HEADER.read_text(encoding="utf-8")
        cls.module = MODULE.read_text(encoding="utf-8")
        cls.capabilities = json.loads(CAPABILITIES.read_text(encoding="utf-8"))

    def test_context_creation_returns_only_context_or_null(self) -> None:
        create_ctx = function_definition(
            self.module, "ngx_http_modsecurity_create_ctx"
        )
        self.assertNotIn("return NGX_CONF_ERROR;", create_ctx)
        self.assertIn("msc_new_transaction_with_id", create_ctx)
        self.assertIn("msc_new_transaction", create_ctx)
        self.assertIn("if (ctx->modsec_transaction == NULL)", create_ctx)
        self.assertLess(
            create_ctx.index("if (ctx->modsec_transaction == NULL)"),
            create_ctx.index("ngx_http_set_ctx(r, ctx, ngx_http_modsecurity_module);"),
        )
        self.assertIn("ngx_pool_cleanup_add(r->pool, 0)", create_ctx)
        self.assertIn("return ctx;", create_ctx)

    def test_final_body_processing_accepts_only_success_one(self) -> None:
        request = function_definition(
            self.access, "ngx_http_modsecurity_inspect_request_body"
        )
        request_assignment = request.index("ret = msc_process_request_body")
        request_failure = conditional_block(request, "if (ret != 1)", request_assignment)
        self.assertIn("ctx->intervention_triggered = 1;", request_failure)
        self.assertIn("return NGX_HTTP_INTERNAL_SERVER_ERROR;", request_failure)

        response = function_definition(
            self.body, "ngx_http_modsecurity_process_final_response_body"
        )
        response_assignment = response.index("ret = msc_process_response_body")
        response_failure = conditional_block(response, "if (ret != 1)", response_assignment)
        self.assertIn("ctx->intervention_triggered = 1;", response_failure)
        committed_failure = conditional_block(response_failure, "if (r->header_sent)")
        self.assertIn("r->connection->error = 1;", committed_failure)
        self.assertIn("return NGX_ERROR;", committed_failure)
        self.assertNotRegex(
            committed_failure,
            re.compile(r"ngx_http_filter_finalize_request\s*\("),
        )
        self.assertIn("NGX_HTTP_INTERNAL_SERVER_ERROR", response_failure)

    def test_partial_body_append_and_file_paths_remain_nonfatal(self) -> None:
        request_append = function_definition(
            self.access, "ngx_http_modsecurity_append_request_body"
        )
        self.assertRegex(
            request_append,
            re.compile(
                r"msc_append_request_body\s*\(.*?\);\s*"
                r"ctx->native_event_phase_active\s*=\s*0;",
                re.DOTALL,
            ),
        )

        request_file = function_definition(
            self.access, "ngx_http_modsecurity_inspect_request_body"
        )
        self.assertRegex(
            request_file,
            re.compile(
                r"msc_request_body_from_file\s*\(.*?\);\s*"
                r"ctx->native_event_phase_active\s*=\s*0;",
                re.DOTALL,
            ),
        )

        response_append = function_definition(
            self.body, "ngx_http_modsecurity_append_limited_response_body"
        )
        self.assertRegex(
            response_append,
            re.compile(r"msc_append_response_body\s*\(.*?\)\s*<\s*0", re.DOTALL),
        )
        self.assertNotRegex(
            response_append,
            re.compile(r"msc_append_response_body\s*\(.*?\)\s*!=\s*1", re.DOTALL),
        )

    def test_negative_interventions_fail_closed_before_response_commit(self) -> None:
        for name in (
            "ngx_http_modsecurity_process_connection",
            "ngx_http_modsecurity_process_request_uri",
            "ngx_http_modsecurity_process_request_headers",
            "ngx_http_modsecurity_append_request_body",
            "ngx_http_modsecurity_inspect_request_body",
        ):
            with self.subTest(function=name):
                function = function_definition(self.access, name)
                intervention = function.index("ret = ngx_http_modsecurity_process_intervention")
                negative = conditional_block(function, "if (ret < 0)", intervention)
                self.assertIn("ctx->intervention_triggered = 1;", negative)
                self.assertIn("return NGX_HTTP_INTERNAL_SERVER_ERROR;", negative)

        header_filter = function_definition(self.header, "ngx_http_modsecurity_header_filter")
        self.assertIn(
            "ngx_http_modsecurity_handle_response_header_intervention(r, ctx,",
            header_filter,
        )
        header_intervention = function_definition(
            self.header, "ngx_http_modsecurity_handle_response_header_intervention"
        )
        negative = conditional_block(header_intervention, "if (ret < 0)")
        self.assertIn("ctx->intervention_triggered = 1;", negative)
        self.assertIn("return NGX_ERROR;", negative)
        self.assertNotIn("ngx_http_filter_finalize_request", negative)

        body_filter = function_definition(self.body, "ngx_http_modsecurity_body_filter")
        self.assertIn("ngx_http_modsecurity_process_final_response_body", body_filter)
        body_intervention = function_definition(
            self.body, "ngx_http_modsecurity_process_final_response_body"
        )
        normal_intervention = conditional_block(body_intervention, "if (ret == 0)")
        self.assertIn("return NGX_OK;", normal_intervention)
        self.assertIn(
            "ngx_http_modsecurity_phase4_handle_intervention(r, mcf)",
            body_intervention,
        )
        phase4_intervention = body_intervention[
            body_intervention.index("ctx->phase4_intervention = 1;") :
        ]
        self.assertNotRegex(
            phase4_intervention,
            re.compile(r"ngx_http_filter_finalize_request\s*\("),
        )

    def test_precommit_redirect_is_atomic_and_replaces_the_old_body(self) -> None:
        redirect = function_definition(
            self.module, "ngx_http_modsecurity_process_redirect_intervention"
        )
        for required in (
            "ngx_http_clear_content_length(r);",
            "ngx_http_clear_last_modified(r);",
            "ngx_http_clear_etag(r);",
            "ngx_http_clear_accept_ranges(r);",
            "ngx_str_null(&r->headers_out.content_type);",
            "r->headers_out.content_type_len = 0;",
        ):
            with self.subTest(required=required):
                self.assertIn(required, redirect)

        self.assertIn("unsigned response_replaced:1;", self.common)
        self.assertIn(
            "unsigned intervention_redirect_location_installed:1;", self.common
        )
        self.assertEqual(
            (self.access + self.body + self.header + self.module).count(
                "ctx->intervention_redirect_location_installed = 1;"
            ),
            1,
        )
        self.assertIn(
            "ctx->intervention_redirect_location_installed = 1;", redirect
        )
        self.assertLess(
            redirect.index("r->headers_out.location->hash = 1;"),
            redirect.index("ctx->intervention_redirect_location_installed = 1;"),
        )
        header_filter = function_definition(self.header, "ngx_http_modsecurity_header_filter")
        header_intervention = function_definition(
            self.header, "ngx_http_modsecurity_handle_response_header_intervention"
        )
        normal_intervention = conditional_block(
            header_intervention,
            "if (ret == 0)",
        )
        self.assertIn("return ngx_http_next_header_filter(r);", normal_intervention)
        positive_intervention = header_intervention[
            header_intervention.index("mcf = ngx_http_get_module_loc_conf") :
        ]
        redirect_branch = conditional_block(
            positive_intervention,
            "if (ctx->intervention_redirect_location_installed &&",
        )
        self.assertIn("r->headers_out.location != NULL", redirect_branch)
        for required in (
            "ctx->response_replaced = 1;",
            "r->headers_out.content_length_n = 0;",
            "r->header_only = 1;",
            "return ngx_http_next_header_filter(r);",
        ):
            with self.subTest(required=required):
                self.assertIn(required, redirect_branch)
        self.assertIn("ctx->intervention_triggered = 1;", positive_intervention)
        self.assertLess(
            positive_intervention.index("ctx->intervention_triggered = 1;"),
            positive_intervention.index(
                "if (ctx->intervention_redirect_location_installed &&"
            ),
        )
        self.assertNotIn("return ngx_http_filter_finalize_request", redirect_branch)
        self.assertRegex(
            positive_intervention,
            re.compile(
                r"return ngx_http_filter_finalize_request\(r,\s*"
                r"&ngx_http_modsecurity_module,\s*ret\);"
            ),
        )
        self.assertNotIn(
            "if (r->headers_out.location != NULL)", positive_intervention
        )

        body_filter = function_definition(self.body, "ngx_http_modsecurity_body_filter")
        replacement_drain = function_definition(
            self.body, "ngx_http_modsecurity_discard_replaced_response_body"
        )
        response_replaced = conditional_block(body_filter, "if (ctx->response_replaced)")
        self.assertLess(
            body_filter.index("if (ctx->response_replaced)"),
            body_filter.index("if (ctx->intervention_triggered)"),
        )
        self.assertRegex(
            replacement_drain,
            re.compile(r"\w+->buf->pos\s*=\s*\w+->buf->last;"),
        )
        self.assertIn(
            "ngx_http_modsecurity_discard_replaced_response_body(in);",
            response_replaced,
        )
        self.assertIn("return ngx_http_next_body_filter(r, in);", response_replaced)

    def test_response_protocol_metadata_and_transaction_grammar_are_exact(self) -> None:
        content_length = function_definition(
            self.header, "ngx_http_modsecurity_resolv_header_content_length"
        )
        self.assertIn("if (r->headers_out.content_length_n >= 0)", content_length)

        connection = function_definition(
            self.header, "ngx_http_modsecurity_resolv_header_connection"
        )
        h2_guard = conditional_block(connection, "if (r->stream)")
        self.assertIn("return 1;", h2_guard)
        self.assertLess(
            connection.index("if (r->stream)"), connection.index('"Keep-Alive"')
        )
        h3_guard = conditional_block(
            connection, "if (r->http_version == NGX_HTTP_VERSION_30)"
        )
        self.assertIn("return 1;", h3_guard)
        self.assertLess(
            connection.index("if (r->http_version == NGX_HTTP_VERSION_30)"),
            connection.index('"Keep-Alive"'),
        )

        transfer_encoding = function_definition(
            self.header, "ngx_http_modsecurity_resolv_header_transfer_encoding"
        )
        h2_transfer_guard = conditional_block(transfer_encoding, "if (r->stream)")
        self.assertIn("return 1;", h2_transfer_guard)
        self.assertLess(
            transfer_encoding.index("if (r->stream)"),
            transfer_encoding.index("if (r->chunked)"),
        )
        h3_transfer_guard = conditional_block(
            transfer_encoding, "if (r->http_version == NGX_HTTP_VERSION_30)"
        )
        self.assertIn("return 1;", h3_transfer_guard)
        self.assertLess(
            transfer_encoding.index("if (r->http_version == NGX_HTTP_VERSION_30)"),
            transfer_encoding.index("if (r->chunked)"),
        )

        header_filter = function_definition(self.header, "ngx_http_modsecurity_header_filter")
        self.assertIn("NGX_HTTP_VERSION_30", header_filter)
        self.assertIn('http_response_ver = "HTTP 3.0";', header_filter)

        directive = self.module[
            self.module.index("ngx_string(MSCONNECTOR_DIRECTIVE_TRANSACTION_ID)") : self.module.index(
                "ngx_conf_set_transaction_id",
                self.module.index("ngx_string(MSCONNECTOR_DIRECTIVE_TRANSACTION_ID)"),
            )
        ]
        self.assertIn("NGX_CONF_TAKE1", directive)
        self.assertNotIn("NGX_CONF_1MORE", directive)

    def test_header_registration_warnings_are_static_and_value_free(self) -> None:
        warning_calls = []
        for source in (self.access, self.header):
            warning_calls.extend(
                match.group(0)
                for match in re.finditer(
                    r"ngx_log_error\(\s*NGX_LOG_WARN\b.*?\);", source, re.DOTALL
                )
                if "failed to add" in match.group(0)
            )

        self.assertGreaterEqual(len(warning_calls), 3)
        for warning in warning_calls:
            with self.subTest(warning=warning):
                self.assertRegex(
                    warning,
                    re.compile(
                        r'"ModSecurity: failed to add (?:request|synthetic response|response) '
                        r'header for inspection"\s*\);'
                    ),
                )

    def test_phase4_finalization_stops_inspection_but_keeps_forwarding(self) -> None:
        body_filter = function_definition(self.body, "ngx_http_modsecurity_body_filter")
        append = body_filter.index("ngx_http_modsecurity_append_limited_response_body")
        already_finalized = body_filter.index("if (ctx->phase4_processed)")
        self.assertLess(already_finalized, append)
        self.assertIn(
            "return ngx_http_next_body_filter(r, in);",
            conditional_block(body_filter, "if (ctx->phase4_processed)"),
        )

        finalized = body_filter.index("ctx->phase4_processed = 1;")
        tail = body_filter[finalized:]
        self.assertIn("break;", tail)
        self.assertIn("return ngx_http_next_body_filter(r, in);", tail)
        self.assertLess(tail.index("break;"), tail.rindex("return ngx_http_next_body_filter(r, in);"))

    def test_out_of_scope_phase4_body_is_not_exposed_and_is_mapped_log_only(self) -> None:
        append = function_definition(
            self.body, "ngx_http_modsecurity_append_limited_response_body"
        )
        self.assertNotIn("in_scope", append)
        self.assertIn("phase4_body_limit", append)
        self.assertIn("msc_append_response_body", append)

        body_filter = function_definition(self.body, "ngx_http_modsecurity_body_filter")
        self.assertIn(
            "phase4_in_scope = ngx_http_modsecurity_phase4_in_scope(r)",
            body_filter,
        )
        scoped_append = conditional_block(body_filter, "if (phase4_in_scope != 0")
        self.assertIn("ngx_http_modsecurity_append_limited_response_body", scoped_append)

        phase4 = function_definition(
            self.body, "ngx_http_modsecurity_phase4_handle_intervention"
        )
        out_of_scope = conditional_block(phase4, "if (in_scope == 0)")
        self.assertIn('"log_only"', out_of_scope)
        self.assertIn('"content_type_not_in_scope"', out_of_scope)

        scope_reason = self.capabilities["capabilities"]["content_type_scope"][
            "reason"
        ]
        self.assertIn("checks its configured response Content-Type scope", scope_reason)
        self.assertIn("out-of-scope response bodies are not appended", scope_reason)


if __name__ == "__main__":
    unittest.main()
