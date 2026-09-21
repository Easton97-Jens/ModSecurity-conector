"""Cross-connector P4 budget units and wiring checks; no hosted runtime claim."""

from __future__ import annotations

import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest

from tests.c_source_contract import function_definition, matching_delimiter

ROOT = Path(__file__).resolve().parents[1]
BODY = ROOT / "connectors/nginx/src/ngx_http_modsecurity_body_filter.c"
APACHE = ROOT / "connectors/apache/src/msc_filters.c"
RUNTIME = ROOT / "common/runtime/msconnector_runtime.c"
BINDING = ROOT / "connectors/haproxy/src/haproxy_modsecurity_binding.c"
HTX = ROOT / "connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c"

PREAMBLE = r"""
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "msconnector/body_policy.h"
#include "msconnector/options.h"
#include "msconnector/phase4_budget.h"

typedef int ngx_int_t;
typedef struct { unsigned int phase4_mode; } ngx_http_modsecurity_conf_t;
typedef struct { int dummy; } ngx_http_request_t;
#define NGX_HTTP_INTERNAL_SERVER_ERROR 500
static int ngx_http_modsecurity_module;
static int finalized;
static int final_status;
static int ngx_http_filter_finalize_request(ngx_http_request_t *r,
    int *module, int status)
{
    (void)r;
    (void)module;
    ++finalized;
    final_status = status;
    return 719;
}
#define CHECK(c) do { if (!(c)) { \
    fprintf(stderr, "line %d: %s\n", __LINE__, #c); return 1; \
} } while (0)
"""
CASES = r"""
int main(int argc, char **argv)
{
    msconnector_body_limit_plan plan;
    size_t limit = 1048576U;
    enum msconnector_phase4_mode modes[] = {
        MSCONNECTOR_PHASE4_MODE_SAFE, MSCONNECTOR_PHASE4_MODE_STRICT
    };
    size_t i;
    CHECK(argc == 2);
    if (strcmp(argv[1], "off-large") == 0) {
        size_t effective = msconnector_phase4_effective_body_limit(
            MSCONNECTOR_PHASE4_MODE_OFF, limit);
        CHECK(effective == SIZE_MAX);
        CHECK(msconnector_body_limit_plan_chunk(0, 0, effective,
            MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, limit + 1, &plan));
        CHECK(plan.append_size == limit + 1);
        CHECK(plan.bytes_seen == limit + 1 && !plan.truncated);
        CHECK(msconnector_body_limit_plan_chunk(plan.bytes_seen, plan.append_size,
            effective, MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, limit + 1, &plan));
        CHECK(plan.bytes_seen == 2 * (limit + 1));
    } else if (strcmp(argv[1], "enabled-limits") == 0) {
        for (i = 0; i < sizeof(modes)/sizeof(modes[0]); ++i) {
            size_t effective = msconnector_phase4_effective_body_limit(modes[i], limit);
            CHECK(effective == limit);
            CHECK(msconnector_body_limit_plan_chunk(0, 0, effective,
                MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, limit, &plan));
            CHECK(plan.append_size == limit);
            CHECK(!msconnector_body_limit_plan_chunk(limit, limit, effective,
                MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, 1, &plan));
            CHECK(plan.append_size == 0);
            CHECK(!msconnector_body_limit_plan_chunk(0, 0, effective,
                MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, limit + 1, &plan));
        }
    } else if (strcmp(argv[1], "invalid-modes") == 0) {
        CHECK(msconnector_phase4_effective_body_limit(
            MSCONNECTOR_PHASE4_MODE_UNSET, limit) == 0);
        CHECK(msconnector_phase4_effective_body_limit(
            (enum msconnector_phase4_mode)77, limit) == 0);
        CHECK(msconnector_phase4_effective_body_limit(
            MSCONNECTOR_PHASE4_MODE_SAFE, 0) == 0);
        CHECK(msconnector_phase4_effective_body_limit(
            MSCONNECTOR_PHASE4_MODE_STRICT, 0) == 0);
    } else if (strcmp(argv[1], "off-overflow") == 0) {
        size_t effective = msconnector_phase4_effective_body_limit(
            MSCONNECTOR_PHASE4_MODE_OFF, limit);
        CHECK(!msconnector_body_limit_plan_chunk(SIZE_MAX - 1, 0, effective,
            MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, 2, &plan));
        CHECK(!msconnector_body_limit_plan_chunk(1, 2, effective,
            MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, 1, &plan));
    } else if (strcmp(argv[1], "native-negative") == 0) {
        CHECK(native_off_result(-1) == 719);
        CHECK(finalized == 1 && final_status == 500);
        CHECK(native_off_result(-7) == 719);
        CHECK(finalized == 2 && final_status == 500);
    } else if (strcmp(argv[1], "native-positive") == 0) {
        CHECK(native_off_result(403) == 403);
        CHECK(native_off_result(302) == 302);
        CHECK(finalized == 0);
    } else if (strcmp(argv[1], "native-zero") == 0) {
        CHECK(native_off_result(0) == 0);
        CHECK(finalized == 0);
    } else {
        return 2;
    }
    return 0;
}
"""


def function(path: Path, name: str) -> str:
    return function_definition(path.read_text(encoding="utf-8"), name)


class Phase4BudgetCUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler or shutil.which(compiler[0]) is None:
            raise unittest.SkipTest("C compiler unavailable")
        cls.directory = tempfile.TemporaryDirectory(prefix="phase4-mode-units-")
        cls.addClassCleanup(cls.directory.cleanup)
        directory = Path(cls.directory.name)
        final = function(BODY, "ngx_http_modsecurity_process_final_response_body")
        marker = "if (mcf != NULL && mcf->phase4_mode == MSCONNECTOR_PHASE4_MODE_OFF)"
        start = final.index(marker)
        opening = final.index("{", start)
        end = matching_delimiter(final, opening, "{", "}") + 1
        branch = final[start:end]
        wrapper = (
            "static int native_off_result(int ret) {\n"
            "ngx_http_request_t request = {0};\n"
            "ngx_http_request_t *r = &request;\n"
            "ngx_http_modsecurity_conf_t conf = {MSCONNECTOR_PHASE4_MODE_OFF};\n"
            "ngx_http_modsecurity_conf_t *mcf = &conf;\n"
            "(void)r; (void)&ngx_http_filter_finalize_request;\n"
            "(void)&ngx_http_modsecurity_module;\n"
            + branch + "\nreturn 0;\n}\n"
        )
        source = directory / "phase4_mode_units.c"
        source.write_text(PREAMBLE + wrapper + CASES, encoding="utf-8")
        cls.binary = directory / "phase4_mode_units"
        command = compiler + [
            "-std=c17", "-Wall", "-Wextra", "-Werror",
            "-I", str(ROOT / "common/include"),
            str(source), str(ROOT / "common/src/body_policy.c"),
            "-o", str(cls.binary),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)

    def run_case(self, name: str) -> None:
        result = subprocess.run([str(self.binary), name], capture_output=True,
                                text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_off_allows_multiple_chunks_above_configured_budget(self) -> None:
        self.run_case("off-large")

    def test_safe_strict_accept_exact_boundary_and_reject_overflowing_chunk(self) -> None:
        self.run_case("enabled-limits")

    def test_unset_unknown_and_zero_enabled_limits_are_not_unlimited(self) -> None:
        self.run_case("invalid-modes")

    def test_off_still_rejects_overflow_and_inconsistent_counters(self) -> None:
        self.run_case("off-overflow")

    def test_nginx_negative_native_result_uses_legacy_finalizer(self) -> None:
        self.run_case("native-negative")

    def test_nginx_positive_native_result_is_not_remapped(self) -> None:
        self.run_case("native-positive")

    def test_nginx_zero_native_result_is_not_finalized(self) -> None:
        self.run_case("native-zero")


class Phase4BudgetWiringTests(unittest.TestCase):
    def test_apache_planner_and_secondary_contract_use_same_mode(self) -> None:
        for name in ("apache_phase4_append_bucket", "apache_output_filter_process_headers"):
            with self.subTest(function=name):
                text = function(APACHE, name)
                self.assertIn("msconnector_phase4_effective_body_limit(", text)
                self.assertIn("conf->common_config.phase4_mode", text)
                self.assertIn("conf->common_config.phase4_body_limit", text)
        append = function(APACHE, "apache_phase4_append_bucket")
        self.assertLess(append.index("msconnector_body_limit_plan_chunk("),
                        append.index("msc_append_response_body("))
        self.assertIn("MSCONNECTOR_BODY_LIMIT_ACTION_REJECT", append)

    def test_native_haproxy_budget_is_consistent_across_all_three_checks(self) -> None:
        for path, name in (
            (BINDING, "response_body_phase"),
            (BINDING, "haproxy_modsecurity_transaction_process_response_headers"),
            (HTX, "haproxy_modsecurity_htx_filter_attach"),
        ):
            with self.subTest(function=name):
                self.assertIn("msconnector_phase4_effective_body_limit(", function(path, name))

    def test_common_direct_and_companion_share_the_budget_gate(self) -> None:
        for name in ("validate_and_record_response_headers", "append_response_body_chunk_internal"):
            with self.subTest(function=name):
                text = function(RUNTIME, name)
                self.assertIn("msconnector_phase4_effective_body_limit(", text)
                self.assertIn("runtime->config.phase4_mode", text)
        self.assertIn("append_response_body_chunk_internal(", function(
            RUNTIME, "msconnector_runtime_transaction_append_response_body_chunk"))
        self.assertIn("append_response_body_chunk_internal(", function(
            RUNTIME, "append_companion_response_body_chunk"))
        text = function(RUNTIME, "append_response_body_chunk_internal")
        start = text.index("if (runtime->config.phase4_mode == MSCONNECTOR_PHASE4_MODE_OFF)")
        self.assertIn("MSCONNECTOR_BODY_LIMIT_ACTION_REJECT",
                      text[start:text.index("if (!apply_body_limit_plan", start)])

    def test_host_allocation_limit_getter_is_not_unlimited(self) -> None:
        text = function(RUNTIME, "msconnector_runtime_response_body_limit")
        self.assertIn("runtime->limits.max_response_body_bytes", text)
        self.assertNotIn("SIZE_MAX", text)
        self.assertNotIn("msconnector_phase4_effective_body_limit", text)

    def test_envoy_traefik_lighttpd_route_body_to_common_runtime(self) -> None:
        paths = (
            "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c",
            "connectors/traefik/src/traefik_engine_service.c",
            "connectors/lighttpd/module/mod_msconnector.c",
            "connectors/lighttpd/stock_sidecar/stock_sidecar.c",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertIn("msconnector_runtime_transaction_append_response_body_chunk(",
                              (ROOT / path).read_text(encoding="utf-8"))

    def test_lighttpd_streaming_header_precheck_uses_mode_but_buffer_capacity_remains(self) -> None:
        text = (ROOT / "connectors/lighttpd/stock_sidecar/stock_sidecar.c").read_text()
        self.assertRegex(text, r"content_length\s*>\s*msconnector_phase4_effective_body_limit\(")
        self.assertIn("if (response_headers.content_length > response_limit)", text)

    def test_nginx_null_guards_precede_configuration_use(self) -> None:
        for name in ("ngx_http_modsecurity_phase4_log_event",
                     "ngx_http_modsecurity_phase4_handle_intervention"):
            text = function(BODY, name)
            self.assertLess(text.index("if (mcf == NULL)"), text.index("mcf->"))
            guard = text[text.index("if (mcf == NULL)"):text.index("mcf->")]
            self.assertIn("return NGX_ERROR;", guard)

    def test_apache_null_guards_precede_bucket_and_request_use(self) -> None:
        text = function(APACHE, "apache_phase4_append_bucket")
        self.assertLess(text.index("msr == NULL"), text.index("APR_BUCKET_IS_EOS"))
        for token in ("conf == NULL", "bucket == NULL", "msr->t == NULL"):
            self.assertIn(token, text[:text.index("APR_BUCKET_IS_EOS")])
        text = function(APACHE, "apache_phase4_handle_intervention")
        self.assertLess(text.index("conf == NULL"), text.index("conf->"))
        self.assertLess(text.index("f == NULL"), text.index("r = f->r;"))
        text = function(APACHE, "apache_phase4_log_event")
        self.assertLess(text.index("r == NULL"), text.index("r->status"))

    def test_shared_event_writer_guards_before_dereference(self) -> None:
        text = function(RUNTIME, "write_event_jsonl")
        self.assertLess(text.index("runtime == NULL"), text.index("runtime->"))
        self.assertLess(text.index("event == NULL"), text.index("msconnector_allocator_init"))
        self.assertIn("runtime->event_file == NULL", text)
        self.assertIn("SIZE_MAX - 2U", text)

    def test_traefik_checks_service_before_policy(self) -> None:
        path = ROOT / "connectors/traefik/src/traefik_engine_service.c"
        text = function(path, "traefik_engine_handle_response_chunk")
        self.assertLess(text.index("session->service == NULL"),
                        text.index("session->service->response_body_mode"))

    def test_existing_envoy_body_bridge_null_checks_remain(self) -> None:
        path = ROOT / "connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c"
        text = function(path, "msc_envoy_ext_proc_transaction_process_body")
        self.assertLess(text.index("transaction == NULL"), text.index("transaction->"))
        self.assertLess(text.index("body == NULL"), text.index("body->"))


if __name__ == "__main__":
    unittest.main()
