"""Compile the actual NGINX request-body functions with controlled host/API seams.

This checks native-result propagation and completion ordering, not a live NGINX
host or a native libModSecurity file reader. File API zero remains an error.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

from tests.c_source_contract import function_definition

ROOT = Path(__file__).resolve().parents[1]
ACCESS = ROOT / "connectors/nginx/src/ngx_http_modsecurity_access.c"
FUNCTIONS = (
    "ngx_http_modsecurity_append_request_body",
    "ngx_http_modsecurity_inspect_request_body_file",
    "ngx_http_modsecurity_inspect_request_body",
)
PREAMBLE = r'''
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include "msconnector/native_result.h"
#include "msconnector/transaction_contract.h"
typedef unsigned char u_char;
typedef int ngx_int_t;
typedef struct { int unused; } ngx_pool_t;
typedef struct { size_t len; u_char *data; } ngx_str_t;
typedef struct { ngx_str_t name; } ngx_file_t;
typedef struct { ngx_file_t file; off_t offset; } ngx_temp_file_t;
typedef struct { u_char *pos; u_char *last; int last_buf; } ngx_buf_t;
typedef struct ngx_chain_s { ngx_buf_t *buf; struct ngx_chain_s *next; } ngx_chain_t;
typedef struct { ngx_chain_t *bufs; ngx_temp_file_t *temp_file; } request_body_t;
typedef struct { void *log; } connection_t;
typedef struct request_s {
    request_body_t *request_body;
    connection_t *connection;
    ngx_pool_t *pool;
    void (*write_event_handler)(struct request_s *);
    int error_page;
} ngx_http_request_t;
typedef struct {
    struct { size_t request_body_limit; } common_config;
} ngx_http_modsecurity_conf_t;
typedef struct {
    msconnector_transaction_contract contract;
    void *modsec_transaction;
    size_t request_body_bytes_seen;
    enum msconnector_phase native_event_phase;
    int native_event_phase_active;
    int intervention_triggered;
    int request_body_processed;
} ngx_http_modsecurity_ctx_t;
typedef struct { off_t size; int regular; } ngx_file_info_t;
enum { NGX_OK = 0, NGX_ERROR = -1, NGX_DECLINED = -5,
       NGX_LOG_ERR = 4, NGX_FILE_ERROR = -1,
       NGX_HTTP_INTERNAL_SERVER_ERROR = 500,
       NGX_HTTP_REQUEST_ENTITY_TOO_LARGE = 413 };
static int append_result = 1, phase_result = 1, file_result = 1;
static int append_calls, phase_calls, file_calls, completion_calls;
static off_t observed_file_size = 3;
static void dd(const char *format, ...) { (void)format; }
static void ngx_log_error(int level, void *log, int error, const char *format, ...) {
    (void)level; (void)log; (void)error; (void)format;
}
static void ngx_http_core_run_phases(ngx_http_request_t *request) { (void)request; }
static ngx_pool_t *ngx_http_modsecurity_pcre_malloc_init(ngx_pool_t *pool) { return pool; }
static void ngx_http_modsecurity_pcre_malloc_done(ngx_pool_t *pool) { (void)pool; }
static char *ngx_str_to_char(ngx_str_t value, ngx_pool_t *pool) {
    (void)pool; return (char *)value.data;
}
static int ngx_file_info(const u_char *name, ngx_file_info_t *info) {
    (void)name; info->size = observed_file_size; info->regular = 1; return 0;
}
static int ngx_is_file(const ngx_file_info_t *info) { return info->regular; }
static off_t ngx_file_size(const ngx_file_info_t *info) { return info->size; }
static int ngx_http_modsecurity_contract_begin(ngx_http_modsecurity_ctx_t *ctx,
        enum msconnector_phase phase) {
    ctx->contract.active_phase = phase; return NGX_OK;
}
static int ngx_http_modsecurity_contract_complete(ngx_http_modsecurity_ctx_t *ctx,
        enum msconnector_phase phase) {
    ++completion_calls; ctx->contract.last_completed_phase = phase;
    ctx->contract.active_phase = -1; return NGX_OK;
}
int msconnector_transaction_contract_record_body(msconnector_transaction_contract *contract,
        int response, size_t bytes) {
    (void)response; contract->request_body_bytes += bytes;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}
int msconnector_transaction_contract_fail(msconnector_transaction_contract *contract,
        msconnector_transaction_error_class cause, uint64_t timestamp) {
    (void)timestamp; contract->error_class = cause;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}
static int msc_append_request_body(void *transaction, const unsigned char *data, size_t bytes) {
    (void)transaction; (void)data; (void)bytes; ++append_calls; return append_result;
}
static int msc_request_body_from_file(void *transaction, const char *name) {
    (void)transaction; (void)name; ++file_calls; return file_result;
}
static int msc_process_request_body(void *transaction) {
    (void)transaction; ++phase_calls; return phase_result;
}
static int ngx_http_modsecurity_process_intervention(void *transaction,
        ngx_http_request_t *request, int early) {
    (void)transaction; (void)request; (void)early; return 0;
}
static void ngx_http_modsecurity_request_intervention_log_event(ngx_http_request_t *request,
        ngx_http_modsecurity_conf_t *config, enum msconnector_phase phase, const char *reason) {
    (void)request; (void)config; (void)phase; (void)reason;
}
'''
MAIN = r'''
int main(int argc, char **argv) {
    u_char data[] = "abc";
    ngx_buf_t buffer = {data, data + 3, 1};
    ngx_chain_t chain = {&buffer, NULL};
    ngx_temp_file_t file = {{{8, (u_char *)"fixture"}}, 3};
    request_body_t body = {&chain, NULL};
    connection_t connection = {NULL};
    ngx_http_request_t request = {&body, &connection, NULL, NULL, 0};
    ngx_http_modsecurity_conf_t config = {{64}};
    ngx_http_modsecurity_ctx_t ctx = {0};
    int result;
    if (argc != 5) { return 2; }
    append_result = (int)strtol(argv[2], NULL, 10);
    phase_result = (int)strtol(argv[3], NULL, 10);
    file_result = (int)strtol(argv[4], NULL, 10);
    ctx.contract.active_phase = MSCONNECTOR_PHASE_REQUEST_BODY;
    ctx.contract.last_completed_phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
    ctx.modsec_transaction = &ctx;
    if (strcmp(argv[1], "file") == 0 || strcmp(argv[1], "changed-file") == 0) {
        body.temp_file = &file;
        if (strcmp(argv[1], "changed-file") == 0) { observed_file_size = 4; }
        result = ngx_http_modsecurity_inspect_request_body(&request, &ctx, &config);
    } else if (strcmp(argv[1], "append") == 0) {
        result = ngx_http_modsecurity_append_request_body(&request, &ctx, &config);
    } else {
        if (strcmp(argv[1], "empty") == 0) { body.bufs = NULL; }
        if (strcmp(argv[1], "limit") == 0) { config.common_config.request_body_limit = 2; }
        result = ngx_http_modsecurity_inspect_request_body(&request, &ctx, &config);
    }
    printf("{\"result\":%d,\"append_calls\":%d,\"phase_calls\":%d,"
           "\"file_calls\":%d,\"completions\":%d,\"processed\":%d,"
           "\"terminal\":%d,\"native_active\":%d,\"bytes_seen\":%zu}\n",
           result, append_calls, phase_calls, file_calls, completion_calls,
           ctx.request_body_processed, ctx.intervention_triggered,
           ctx.native_event_phase_active, ctx.request_body_bytes_seen);
    return 0;
}
'''


class NginxRequestNativeResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler or shutil.which(compiler[0]) is None:
            raise RuntimeError("a C compiler is required for native request regressions")
        cls.temporary = tempfile.TemporaryDirectory(
            prefix="nginx-request-native-", dir=os.environ.get("RUNNER_TEMP")
        )
        cls.addClassCleanup(cls.temporary.cleanup)
        directory = Path(cls.temporary.name)
        cls.binary = directory / "request-contract"
        source = ACCESS.read_text(encoding="utf-8")
        fixture = directory / "request-contract.c"
        fixture.write_text(
            PREAMBLE + "\n" + "\n".join(
                function_definition(source, name) for name in FUNCTIONS
            ) + "\n" + MAIN,
            encoding="utf-8",
        )
        subprocess.run(
            compiler + ["-std=c17", "-Wall", "-Wextra", "-Werror",
                        "-I", str(ROOT / "common/include"), str(fixture),
                        "-o", str(cls.binary)],
            check=True, capture_output=True, text=True, timeout=30,
        )

    def run_case(self, mode: str, append: int = 1, phase: int = 1,
                 file_result: int = 1) -> dict:
        result = subprocess.run(
            [str(self.binary), mode, str(append), str(phase), str(file_result)],
            check=True, capture_output=True, text=True, timeout=5,
        )
        return json.loads(result.stdout)

    def test_memory_partial_and_success_can_reach_phase_evaluation(self) -> None:
        for native in (0, 1):
            with self.subTest(native=native):
                result = self.run_case("memory", append=native)
                self.assertEqual(result["result"], -5)
                self.assertEqual(result["phase_calls"], 1)
                self.assertEqual(result["completions"], 1)
                self.assertEqual(result["processed"], 1)
                self.assertEqual(result["native_active"], 0)

    def test_undocumented_append_results_cannot_complete_phase(self) -> None:
        for native in (-1, -2, 2, 17):
            with self.subTest(native=native):
                result = self.run_case("memory", append=native)
                self.assertEqual(result["result"], 500)
                self.assertEqual(result["phase_calls"], 0)
                self.assertEqual(result["completions"], 0)
                self.assertEqual(result["processed"], 0)
                self.assertEqual(result["terminal"], 1)

    def test_failed_final_evaluation_never_records_successful_eos(self) -> None:
        for native in (-1, 0, 2):
            with self.subTest(native=native):
                result = self.run_case("empty", phase=native)
                self.assertEqual(result["result"], 500)
                self.assertEqual(result["phase_calls"], 1)
                self.assertEqual(result["completions"], 0)
                self.assertEqual(result["processed"], 0)
                self.assertEqual(result["terminal"], 1)

    def test_empty_body_completes_once_without_append(self) -> None:
        result = self.run_case("empty")
        self.assertEqual(result["append_calls"], 0)
        self.assertEqual(result["completions"], 1)
        self.assertEqual(result["processed"], 1)

    def test_file_zero_is_not_mistaken_for_memory_partial(self) -> None:
        for native in (-1, 0, 2):
            with self.subTest(native=native):
                result = self.run_case("file", file_result=native)
                self.assertEqual(result["result"], 500)
                self.assertEqual(result["file_calls"], 1)
                self.assertEqual(result["phase_calls"], 0)
                self.assertEqual(result["completions"], 0)

    def test_file_success_preserves_observed_byte_accounting(self) -> None:
        result = self.run_case("file")
        self.assertEqual(result["result"], -5)
        self.assertEqual(result["bytes_seen"], 3)
        self.assertEqual(result["completions"], 1)

    def test_changed_file_metadata_stops_before_native_reader(self) -> None:
        result = self.run_case("changed-file")
        self.assertEqual(result["result"], 500)
        self.assertEqual(result["file_calls"], 0)
        self.assertEqual(result["phase_calls"], 0)

    def test_host_budget_rejects_before_native_append(self) -> None:
        result = self.run_case("limit")
        self.assertEqual(result["result"], 413)
        self.assertEqual(result["append_calls"], 0)
        self.assertEqual(result["phase_calls"], 0)

    def test_phase_one_checks_native_result_before_canonical_completion(self) -> None:
        source = ACCESS.read_text(encoding="utf-8")
        function = function_definition(source, "ngx_http_modsecurity_process_request_headers")
        result_check = function.index("msconnector_native_phase_succeeded(ret)")
        completion = function.index("ngx_http_modsecurity_contract_complete")
        self.assertLess(result_check, completion)
        self.assertIn("MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE", function)


if __name__ == "__main__":
    unittest.main()
