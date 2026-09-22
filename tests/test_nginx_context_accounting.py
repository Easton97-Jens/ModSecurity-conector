"""Compile the actual native context declaration without a running host."""
from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "connectors/nginx/src/ngx_http_modsecurity_common.h"
PREAMBLE = r'''
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include "msconnector/transaction_contract.h"
typedef unsigned char u_char;
typedef intptr_t ngx_int_t;
typedef struct request ngx_http_request_t;
typedef struct transaction Transaction;
typedef struct intervention ModSecurityIntervention;
typedef struct array ngx_array_t;
typedef struct { size_t len; u_char *data; } ngx_str_t;
'''
MAIN = r'''
int main(void) {
    ngx_http_modsecurity_ctx_t ctx = {0};
    if (ctx.request_error_status || ctx.request_error_event_attempted ||
        ctx.request_body_bytes_seen || ctx.response_body_bytes_seen ||
        ctx.response_body_bytes_inspected || ctx.request_header_count ||
        ctx.request_header_bytes || ctx.response_header_count ||
        ctx.response_header_bytes || ctx.phase4_processed) {
        return 1;
    }
    ctx.request_body_bytes_seen = SIZE_MAX;
    ctx.response_body_bytes_seen = 9U;
    ctx.response_body_bytes_inspected = 8U;
    ctx.request_header_count = 7U;
    ctx.request_header_bytes = 6U;
    ctx.response_header_count = 5U;
    ctx.response_header_bytes = 4U;
    ctx.request_error_status = 500;
    ctx.request_error_event_attempted = 1;
    ctx.phase4_processed = 1;
    ctx.last_intervention_status = 403;
    if (ctx.request_body_bytes_seen != SIZE_MAX ||
        ctx.response_body_bytes_seen != 9U || ctx.response_body_bytes_inspected != 8U ||
        ctx.request_header_count != 7U || ctx.request_header_bytes != 6U ||
        ctx.response_header_count != 5U || ctx.response_header_bytes != 4U ||
        ctx.request_error_status != 500 || !ctx.request_error_event_attempted ||
        !ctx.phase4_processed || ctx.last_intervention_status != 403) {
        return 2;
    }
    memset(&ctx, 0, sizeof(ctx));
    return ctx.request_error_status != 0 || ctx.response_body_bytes_seen != 0U;
}
'''


class NginxContextAccountingTests(unittest.TestCase):
    def test_context_accounting_and_terminal_state_remain_independent(self) -> None:
        source = HEADER.read_text(encoding="utf-8")
        end = source.index("} ngx_http_modsecurity_ctx_t;") + len("} ngx_http_modsecurity_ctx_t;")
        start = source.rfind("typedef struct {", 0, end)
        self.assertGreaterEqual(start, 0)
        declaration = source[start:end]
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler or shutil.which(compiler[0]) is None:
            self.fail("a C compiler is required for context accounting tests")
        with tempfile.TemporaryDirectory(prefix="nginx-context-", dir=os.environ.get("RUNNER_TEMP")) as temporary:
            directory = Path(temporary)
            fixture = directory / "context.c"
            fixture.write_text(PREAMBLE + declaration + "\n" + MAIN, encoding="utf-8")
            for sanity in (0, 1):
                with self.subTest(sanity_checks=sanity):
                    binary = directory / ("context-" + str(sanity))
                    command = compiler + ["-std=c17", "-Wall", "-Wextra", "-Werror", "-pedantic-errors",
                                          "-DMODSECURITY_SANITY_CHECKS=" + str(sanity),
                                          "-I", str(ROOT / "common/include"), str(fixture), "-o", str(binary)]
                    compiled = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
                    self.assertEqual(compiled.returncode, 0, compiled.stderr[-6000:])
                    executed = subprocess.run([str(binary)], capture_output=True, text=True, timeout=5, check=False)
                    self.assertEqual(executed.returncode, 0, executed.stderr[-2000:])


if __name__ == "__main__":
    unittest.main()
