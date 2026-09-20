"""NGINX Phase-4 budget unit tests and source-wiring contracts.

The compiled test uses the actual planner, header budget expression, and Common
body-policy implementation with small NGINX state doubles. It is not a native
NGINX/libModSecurity integration or HTTP transport test.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest

from tests.c_source_contract import function_definition

ROOT = Path(__file__).resolve().parents[1]
NGINX_SOURCE = ROOT / "connectors" / "nginx" / "src"
BODY = NGINX_SOURCE / "ngx_http_modsecurity_body_filter.c"
HEADER = NGINX_SOURCE / "ngx_http_modsecurity_header_filter.c"
PREAMBLE = r"""
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "msconnector/body_policy.h"
#include "msconnector/options.h"
#include "msconnector/limits.h"

typedef int ngx_int_t;
#define NGX_OK 0
#define NGX_ERROR (-1)
#define MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT 1
#define MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR 2
typedef struct { int error; } test_contract;
typedef struct {
    size_t response_body_bytes_seen;
    size_t response_body_bytes_inspected;
    int response_body_seen;
    int response_body_truncated;
    test_contract contract;
} ngx_http_modsecurity_ctx_t;
typedef struct {
    unsigned long phase4_mode;
    struct { size_t phase4_body_limit; } common_config;
} ngx_http_modsecurity_conf_t;
static int msconnector_transaction_contract_fail(
    test_contract *contract, int error, unsigned long now)
{
    (void)now;
    contract->error = error;
    return 0;
}
#define CHECK(condition) do { \
    if (!(condition)) { \
        fprintf(stderr, "line %d: %s\n", __LINE__, #condition); \
        return 1; \
    } \
} while (0)
"""
CASES = r"""
int main(int argc, char **argv)
{
    ngx_http_modsecurity_ctx_t ctx = {0};
    ngx_http_modsecurity_conf_t conf = {0};
    size_t allowed = 999U;
    const size_t limit = 1048576U;
    unsigned long modes[] = {
        MSCONNECTOR_PHASE4_MODE_SAFE, MSCONNECTOR_PHASE4_MODE_STRICT
    };
    size_t i;
    conf.common_config.phase4_body_limit = limit;
    CHECK(argc == 2);

    if (strcmp(argv[1], "off-large") == 0) {
        conf.phase4_mode = MSCONNECTOR_PHASE4_MODE_OFF;
        CHECK(effective_response_limit(&conf) == SIZE_MAX);
        CHECK(ngx_http_modsecurity_plan_limited_response_body(
            &ctx, &conf, limit + 1U, &allowed) == NGX_OK);
        CHECK(allowed == limit + 1U);
        CHECK(ctx.response_body_bytes_seen == limit + 1U);
        CHECK(ctx.response_body_bytes_seen <= effective_response_limit(&conf));
        CHECK(ctx.response_body_seen && !ctx.response_body_truncated);
        CHECK(ctx.contract.error == 0);
        CHECK(ctx.response_body_bytes_inspected == 0U);
    } else if (strcmp(argv[1], "off-multiple") == 0) {
        conf.phase4_mode = MSCONNECTOR_PHASE4_MODE_OFF;
        for (i = 0U; i < 3U; ++i) {
            CHECK(ngx_http_modsecurity_plan_limited_response_body(
                &ctx, &conf, limit, &allowed) == NGX_OK);
            CHECK(allowed == limit);
            ctx.response_body_bytes_inspected += allowed;
        }
        CHECK(ctx.response_body_bytes_seen == 3U * limit);
        CHECK(ctx.response_body_bytes_seen <= effective_response_limit(&conf));
        CHECK(!ctx.response_body_truncated);
    } else if (strcmp(argv[1], "safe-strict-boundary") == 0) {
        for (i = 0U; i < sizeof(modes) / sizeof(modes[0]); ++i) {
            memset(&ctx, 0, sizeof(ctx));
            conf.phase4_mode = modes[i];
            CHECK(effective_response_limit(&conf) == limit);
            CHECK(ngx_http_modsecurity_plan_limited_response_body(
                &ctx, &conf, limit - 1U, &allowed) == NGX_OK);
            ctx.response_body_bytes_inspected += allowed;
            CHECK(ngx_http_modsecurity_plan_limited_response_body(
                &ctx, &conf, 1U, &allowed) == NGX_OK);
            ctx.response_body_bytes_inspected += allowed;
            CHECK(ctx.response_body_bytes_seen == limit);
            CHECK(!ctx.response_body_truncated);
            CHECK(ngx_http_modsecurity_plan_limited_response_body(
                &ctx, &conf, 1U, &allowed) == NGX_ERROR);
            CHECK(allowed == 0U);
            CHECK(ctx.response_body_bytes_seen == limit + 1U);
            CHECK(ctx.response_body_bytes_inspected == limit);
            CHECK(ctx.response_body_truncated);
            CHECK(ctx.contract.error == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT);
        }
    } else if (strcmp(argv[1], "safe-strict-large") == 0) {
        for (i = 0U; i < sizeof(modes) / sizeof(modes[0]); ++i) {
            memset(&ctx, 0, sizeof(ctx));
            conf.phase4_mode = modes[i];
            CHECK(ngx_http_modsecurity_plan_limited_response_body(
                &ctx, &conf, limit + 1U, &allowed) == NGX_ERROR);
            CHECK(allowed == 0U);
            CHECK(ctx.response_body_bytes_inspected == 0U);
            CHECK(ctx.response_body_truncated);
        }
    } else if (strcmp(argv[1], "off-overflow") == 0) {
        conf.phase4_mode = MSCONNECTOR_PHASE4_MODE_OFF;
        ctx.response_body_bytes_seen = SIZE_MAX - 1U;
        ctx.response_body_bytes_inspected = SIZE_MAX - 1U;
        CHECK(ngx_http_modsecurity_plan_limited_response_body(
            &ctx, &conf, 2U, &allowed) == NGX_ERROR);
        CHECK(allowed == 0U);
        CHECK(ctx.response_body_bytes_seen == SIZE_MAX - 1U);
        CHECK(ctx.response_body_truncated);
        CHECK(ctx.contract.error == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT);
    } else if (strcmp(argv[1], "off-invalid-accounting") == 0) {
        conf.phase4_mode = MSCONNECTOR_PHASE4_MODE_OFF;
        ctx.response_body_bytes_inspected = 1U;
        CHECK(ngx_http_modsecurity_plan_limited_response_body(
            &ctx, &conf, 1U, &allowed) == NGX_ERROR);
        CHECK(allowed == 0U);
        CHECK(ctx.response_body_bytes_seen == 0U);
        CHECK(ctx.response_body_truncated);
    } else if (strcmp(argv[1], "null-inputs") == 0) {
        conf.phase4_mode = MSCONNECTOR_PHASE4_MODE_OFF;
        CHECK(ngx_http_modsecurity_plan_limited_response_body(
            NULL, &conf, 1U, &allowed) == NGX_ERROR);
        CHECK(allowed == 0U);
        allowed = 999U;
        CHECK(ngx_http_modsecurity_plan_limited_response_body(
            &ctx, NULL, 1U, &allowed) == NGX_ERROR);
        CHECK(allowed == 0U);
        CHECK(ngx_http_modsecurity_plan_limited_response_body(
            &ctx, &conf, 1U, NULL) == NGX_ERROR);
        CHECK(!ctx.response_body_seen);
    } else if (strcmp(argv[1], "empty") == 0) {
        for (i = 0U; i < 3U; ++i) {
            memset(&ctx, 0, sizeof(ctx));
            conf.phase4_mode = i;
            CHECK(ngx_http_modsecurity_plan_limited_response_body(
                &ctx, &conf, 0U, &allowed) == NGX_OK);
            CHECK(allowed == 0U);
            CHECK(!ctx.response_body_seen && !ctx.response_body_truncated);
        }
    } else if (strcmp(argv[1], "invalid-mode") == 0) {
        conf.phase4_mode = 99U;
        CHECK(ngx_http_modsecurity_plan_limited_response_body(
            &ctx, &conf, 1U, &allowed) == NGX_ERROR);
        CHECK(allowed == 0U);
        CHECK(ctx.contract.error == MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
    } else {
        return 2;
    }
    return 0;
}
"""


def response_limit_expression(header: str) -> str:
    """Read the real final metadata argument, including nested parentheses."""
    match = re.search(
        r"msconnector_transaction_contract_record_response_metadata\(\s*"
        r"&ctx->contract,\s*\(int\)status,\s*response_content_type,\s*"
        r"response_header_count,\s*response_header_bytes,\s*"
        r"(.*?)\)\s*!=\s*MSCONNECTOR_TRANSACTION_TRANSITION_OK",
        header,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("response metadata body-budget argument not found")
    return match.group(1)


def unit_program(body: str, header: str) -> str:
    planner = function_definition(body, "ngx_http_modsecurity_plan_limited_response_body")
    expression = response_limit_expression(header)
    return (
        PREAMBLE
        + "\nstatic ngx_int_t\n" + planner
        + "\nstatic size_t effective_response_limit("
          "const ngx_http_modsecurity_conf_t *mcf) { return "
        + expression + "; }\n"
        + CASES
    )


class NginxPhase4BudgetUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler or shutil.which(compiler[0]) is None:
            raise RuntimeError("a C compiler is required for Phase-4 budget unit tests")
        temporary = tempfile.TemporaryDirectory(prefix="nginx-phase4-budget-")
        cls.addClassCleanup(temporary.cleanup)
        source = Path(temporary.name) / "budget.c"
        cls.binary = Path(temporary.name) / "budget"
        source.write_text(unit_program(
            BODY.read_text(encoding="utf-8"),
            HEADER.read_text(encoding="utf-8"),
        ), encoding="utf-8")
        result = subprocess.run(
            compiler + [
                "-std=c11", "-Wall", "-Wextra", "-Werror",
                "-I", str(ROOT / "common" / "include"),
                str(source), str(ROOT / "common" / "src" / "body_policy.c"),
                "-o", str(cls.binary),
            ],
            text=True, capture_output=True, timeout=30, check=False,
        )
        if result.returncode:
            raise AssertionError(f"budget unit compilation failed:\n{result.stderr}")

    def run_case(self, name: str) -> None:
        result = subprocess.run(
            [str(self.binary), name], text=True, capture_output=True,
            timeout=10, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_off_allows_large_buffer_and_has_no_secondary_contract_budget(self) -> None:
        self.run_case("off-large")

    def test_off_accounts_for_multiple_buffers_above_configured_budget(self) -> None:
        self.run_case("off-multiple")

    def test_safe_and_strict_allow_exact_limit_then_reject_next_byte(self) -> None:
        self.run_case("safe-strict-boundary")

    def test_safe_and_strict_reject_oversized_first_buffer(self) -> None:
        self.run_case("safe-strict-large")

    def test_off_still_rejects_counter_overflow(self) -> None:
        self.run_case("off-overflow")

    def test_off_still_rejects_inconsistent_accounting(self) -> None:
        self.run_case("off-invalid-accounting")

    def test_null_planner_inputs_fail_without_dereferencing(self) -> None:
        self.run_case("null-inputs")

    def test_empty_buffers_do_not_mark_body_started(self) -> None:
        self.run_case("empty")

    def test_unknown_modes_are_not_an_unlimited_fallback(self) -> None:
        self.run_case("invalid-mode")


class NginxPhase4BudgetWiringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.body = BODY.read_text(encoding="utf-8")

    def test_memory_and_file_buffers_share_mode_aware_planner(self) -> None:
        for name, append_call in (
            ("ngx_http_modsecurity_append_limited_response_body",
             "return ngx_http_modsecurity_append_response_body_chunk"),
            ("ngx_http_modsecurity_append_file_response_body", "ngx_read_file("),
        ):
            with self.subTest(function=name):
                source = function_definition(self.body, name)
                self.assertLess(
                    source.index("ngx_http_modsecurity_plan_limited_response_body("),
                    source.index(append_call),
                )
                self.assertIn("return NGX_ERROR;", source)
        file_source = function_definition(
            self.body, "ngx_http_modsecurity_append_file_response_body"
        )
        self.assertIn("NGX_HTTP_MODSECURITY_PHASE4_FILE_READ_CHUNK", file_source)
        self.assertIn("read_count < 0 || (size_t)read_count != chunk", file_source)

    def test_off_does_not_remove_engine_ingestion_or_finalization(self) -> None:
        append = function_definition(
            self.body, "ngx_http_modsecurity_append_response_body_chunk"
        )
        final = function_definition(
            self.body, "ngx_http_modsecurity_process_final_response_body"
        )
        self.assertIn("msc_append_response_body(", append)
        self.assertIn("msconnector_transaction_contract_record_body(", append)
        self.assertLess(
            final.index("msc_process_response_body("),
            final.index("mcf->phase4_mode == MSCONNECTOR_PHASE4_MODE_OFF"),
        )

    def test_missing_configuration_fails_before_phase4_dereferences(self) -> None:
        for name in (
            "ngx_http_modsecurity_phase4_log_event",
            "ngx_http_modsecurity_phase4_handle_intervention",
        ):
            with self.subTest(function=name):
                source = function_definition(self.body, name)
                match = re.search(
                    r"if\s*\(mcf == NULL\)\s*\{\s*return NGX_ERROR;\s*\}",
                    source,
                )
                self.assertIsNotNone(match)
                self.assertLess(match.end(), source.index("mcf->"))


if __name__ == "__main__":
    unittest.main()
