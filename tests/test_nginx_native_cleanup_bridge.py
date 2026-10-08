"""Exercise actual module cleanup ordering with real Common state/JSONL.

Native void cleanup and NGINX host calls are controlled seams; this is a C17
source-bound regression, not live process or runtime cleanup evidence.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tests.c_source_contract import function_definition

ROOT = Path(__file__).resolve().parents[1]
PREAMBLE = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "msconnector/event_jsonl.h"
#include "msconnector/transaction_state.h"
#include "connectors/profile_registry.h"
#include "ngx_http_modsecurity_cleanup_observation.h"
typedef long ngx_int_t;
typedef unsigned char u_char;
typedef struct { size_t len; u_char *data; } ngx_str_t;
typedef struct { int fd; } ngx_open_file_t;
typedef struct { void *log; } connection_t;
typedef struct { connection_t *connection; } ngx_http_request_t;
typedef struct { ngx_open_file_t *phase4_log_file; } ngx_http_modsecurity_conf_t;
typedef struct {
    msconnector_transaction_contract contract;
    int contract_initialized;
    void *modsec_transaction;
    ngx_http_request_t *r;
    ngx_str_t event_transaction_id;
} ngx_http_modsecurity_ctx_t;
typedef struct { const char *method, *uri, *content_type; }
    ngx_http_modsecurity_event_request_metadata_t;
enum { NGX_OK=0, NGX_ERROR=-1, NGX_LOG_WARN=5, NGX_INVALID_FILE=-1 };
static int ngx_http_modsecurity_module, native_calls, writes, errors;
static ngx_http_modsecurity_ctx_t context;
static ngx_http_modsecurity_conf_t config;
static char jsonl[4096];
static void msc_transaction_cleanup(void *native) {
    if (!native || context.contract.cleanup_complete != 1) abort();
    ++native_calls;
}
static void ngx_log_error(int level, void *log, int number, const char *format, ...) {
    (void)level; (void)log; (void)number; (void)format; ++errors;
}
static ngx_http_modsecurity_conf_t *ngx_http_get_module_loc_conf(ngx_http_request_t *r, int module) {
    (void)r; (void)module; return &config;
}
static ngx_http_modsecurity_event_request_metadata_t
ngx_http_modsecurity_event_request_metadata(ngx_http_request_t *r) {
    (void)r; return (ngx_http_modsecurity_event_request_metadata_t){"GET", "/cleanup-control", "text/plain"};
}
static ngx_int_t ngx_http_modsecurity_write_phase_event_jsonl(ngx_http_request_t *r,
    ngx_http_modsecurity_conf_t *conf, const msconnector_event *event, const char *phase) {
    int truncated=0;
    (void)r; (void)conf;
    if (strcmp(phase,"cleanup") != 0 || context.modsec_transaction != NULL) abort();
    ++writes;
    return msconnector_event_write_jsonl_line(event,jsonl,sizeof(jsonl),&truncated) && !truncated
        ? NGX_OK : NGX_ERROR;
}
'''
MAIN = r'''
int main(int argc,char **argv) {
    connection_t connection={0};
    ngx_http_request_t request={&connection};
    ngx_open_file_t file={7};
    static u_char transaction[]="actual-cleanup-tx";
    int mode;
    if (argc != 2) return 2;
    mode=atoi(argv[1]);
    context.r=&request; config.phase4_log_file=&file;
    context.event_transaction_id=(ngx_str_t){sizeof(transaction)-1,transaction};
    if (msconnector_transaction_contract_init(&context.contract,
        msconnector_profile_registry_find("nginx"),"cleanup-control","nginx","actual-cleanup-tx",
        MSCONNECTOR_TRANSACTION_MODE_SAFE,100U) != 0) return 3;
    context.contract_initialized=1;
    context.modsec_transaction=mode == 3 ? NULL : &request;
    if (mode == 2) {
        if (msconnector_transaction_contract_begin_phase(&context.contract,MSCONNECTOR_PHASE_REQUEST_HEADERS,0U) != 0) return 4;
    } else if (mode == 4) {
        if (msconnector_transaction_contract_fail(&context.contract,MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT,0U) != 0) return 5;
    } else {
        for (enum msconnector_phase phase=MSCONNECTOR_PHASE_REQUEST_HEADERS;phase<=MSCONNECTOR_PHASE_RESPONSE_BODY;++phase) {
            if (msconnector_transaction_contract_begin_phase(&context.contract,phase,0U) != 0 ||
                msconnector_transaction_contract_complete_phase(&context.contract,phase,0U) != 0) return 6;
        }
        if (msconnector_transaction_contract_finish(&context.contract,0U) != 0) return 7;
    }
    ngx_http_modsecurity_cleanup(&context);
    if (mode == 1) ngx_http_modsecurity_cleanup(&context);
    printf("%d %d %d %d %d\n",native_calls,writes,errors,context.contract_initialized,context.modsec_transaction == NULL);
    fputs(jsonl,stdout);
    return 0;
}
'''


class NativeCleanupBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler = shutil.which(os.environ.get("CC", "cc"))
        if compiler is None:
            raise RuntimeError("real C17 compiler is required")
        temporary = tempfile.TemporaryDirectory(prefix="nginx-cleanup-bridge-", dir=os.environ.get("RUNNER_TEMP"))
        cls.addClassCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        source = (ROOT / "connectors/nginx/src/ngx_http_modsecurity_module.c").read_text()
        fixture = directory / "cleanup.c"
        fixture.write_text(PREAMBLE + "static void\n" + function_definition(source, "ngx_http_modsecurity_cleanup_log_event")
                           + "\nvoid\n" + function_definition(source, "ngx_http_modsecurity_cleanup") + MAIN)
        cls.binary = directory / "cleanup"
        command = [compiler, "-std=c17", "-Wall", "-Wextra", "-Werror", "-pthread",
                   "-I", str(ROOT / "connectors/nginx/src"), "-I", str(ROOT), "-I", str(ROOT / "common/include"), str(fixture)]
        command += [str(ROOT / "common/src" / name) for name in
                    ("transaction_state.c", "decision_action.c", "intervention.c", "block_statuses.c", "http_status.c",
                     "late_intervention.c", "event.c", "event_jsonl.c", "json_escape.c", "status.c")]
        command += [str(ROOT / "connectors/profile_registry.c"), "-o", str(cls.binary)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
        if result.returncode:
            raise AssertionError(result.stderr[-7000:])

    def observe(self, mode):
        result = subprocess.run([str(self.binary), str(mode)], capture_output=True, text=True, timeout=5, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        state, _, raw = result.stdout.partition("\n")
        return list(map(int, state.split())), json.loads(raw)

    def test_normal_cleanup_is_emitted_after_actual_native_cleanup(self):
        state, event = self.observe(0)
        self.assertEqual(state, [1, 1, 0, 0, 1])
        self.assertEqual(event["reason"], "common_return=0;common_complete=1;native_cleanup_completed=1;error_class=none")
        self.assertEqual(event["phase"], "logging")
        self.assertEqual(event["transaction_id"], "actual-cleanup-tx")
        self.assertEqual(event["cleanup_reason"], "normal")
        self.assertEqual(event["actual_action"], "allow")

    def test_reentry_does_not_duplicate_cleanup_or_observation(self):
        state, _ = self.observe(1)
        self.assertEqual(state, [1, 1, 0, 0, 1])

    def test_incomplete_common_cleanup_is_not_relabelled_success(self):
        state, event = self.observe(2)
        self.assertEqual(state[:2], [1, 1])
        self.assertEqual(event["reason"], "common_return=-8;common_complete=1;native_cleanup_completed=1;error_class=cleanup_incomplete")
        self.assertEqual(event["status"], "error")

    def test_absent_native_pointer_is_recorded_not_fabricated(self):
        state, event = self.observe(3)
        self.assertEqual(state[:2], [0, 1])
        self.assertIn("native_cleanup_completed=0", event["reason"])

    def test_terminal_engine_error_survives_real_cleanup(self):
        state, event = self.observe(4)
        self.assertEqual(state[:2], [1, 1])
        self.assertEqual(event["reason"], "common_return=0;common_complete=1;native_cleanup_completed=1;error_class=engine_timeout")
        self.assertEqual(event["cleanup_reason"], "engine_timeout")
