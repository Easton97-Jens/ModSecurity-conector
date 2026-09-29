"""Focused B09 regression: compile the actual classifier and P1/P2 result tails.

The shim controls the native return and event sink. It is not live NGINX,
libmodsecurity, error_page-routing, or transport evidence.
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
SOURCE = ROOT / "connectors/nginx/src"


class NginxErrorPageInterventionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        compiler = shlex.split(os.environ.get("CC", "cc"))
        if not compiler or shutil.which(compiler[0]) is None:
            raise RuntimeError("A C17 compiler is required for the B09 regression")
        cls.workspace = tempfile.TemporaryDirectory(prefix="nginx-b09-")
        cls.addClassCleanup(cls.workspace.cleanup)
        directory = Path(cls.workspace.name)
        common = (SOURCE / "ngx_http_modsecurity_common.h").read_text(encoding="utf-8")
        access = (SOURCE / "ngx_http_modsecurity_access.c").read_text(encoding="utf-8")
        enum = re.search(
            r"typedef enum \{\s*MSCONNECTOR_NGINX_INTERVENTION_FAILURE,"
            r".*?\} msconnector_nginx_intervention_disposition;",
            common,
            re.DOTALL,
        )
        if enum is None:
            raise AssertionError("Actual intervention enum was not found")
        classifier = function_definition(
            common, "ngx_http_modsecurity_intervention_disposition"
        )
        body = function_definition(
            access, "ngx_http_modsecurity_inspect_request_body"
        )
        tail = body[body.rindex(
            "ret = ngx_http_modsecurity_process_intervention("
        ):]
        headers = function_definition(
            access, "ngx_http_modsecurity_process_request_headers"
        )
        header_tail = headers[headers.rindex(
            "ret = ngx_http_modsecurity_process_intervention("
        ):]
        code = (
            "#include <stdio.h>\n#include <stdlib.h>\n"
            "typedef long ngx_flag_t;\n"
            + enum.group(0)
            + "\nstatic msconnector_nginx_intervention_disposition\n"
            + classifier
            + r"""
typedef struct { int error_page; } ngx_http_request_t;
typedef struct {
    void *modsec_transaction;
    int intervention_triggered;
} ngx_http_modsecurity_ctx_t;
typedef struct { int unused; } ngx_http_modsecurity_conf_t;
enum {
    NGX_HTTP_INTERNAL_SERVER_ERROR = 500,
    NGX_DECLINED = -5,
    NGX_OK = 0,
    MSCONNECTOR_PHASE_REQUEST_HEADERS = 1,
    MSCONNECTOR_PHASE_REQUEST_BODY = 2
};
static int native_result;
static int event_calls;
static int ngx_http_modsecurity_process_intervention(
    void *transaction, ngx_http_request_t *r, int early_log)
{
    (void)transaction;
    (void)r;
    (void)early_log;
    return native_result;
}
static void ngx_http_modsecurity_request_intervention_log_event(
    ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf,
    int phase, const char *reason)
{
    (void)r;
    (void)mcf;
    (void)phase;
    (void)reason;
    ++event_calls;
}
static int p2_result(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf)
{
    int ret;
"""
            + tail
            + r"""
static int p1_result(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf)
{
    int ret;
    msconnector_nginx_intervention_disposition disposition;
"""
            + header_tail
            + r"""
int main(int argc, char **argv)
{
    ngx_http_request_t request = {0};
    ngx_http_modsecurity_ctx_t ctx = {0};
    ngx_http_modsecurity_conf_t config = {0};
    int result;
    int headers;
    int header_events;
    int header_triggered;
    if (argc != 3) return 2;
    native_result = atoi(argv[1]);
    request.error_page = atoi(argv[2]);
    headers = p1_result(&request, &ctx, &config);
    header_events = event_calls;
    header_triggered = ctx.intervention_triggered;
    event_calls = 0;
    ctx.intervention_triggered = 0;
    result = p2_result(&request, &ctx, &config);
    printf("%d %d %d %d %d %d %d\n",
        (int)ngx_http_modsecurity_intervention_disposition(
            native_result, request.error_page),
        result, ctx.intervention_triggered, event_calls,
        headers, header_triggered, header_events);
    return 0;
}
"""
        )
        source = directory / "regression.c"
        source.write_text(code, encoding="utf-8")
        cls.binary = directory / "regression"
        build = subprocess.run(
            [*compiler, "-std=c17", "-Wall", "-Wextra", "-Werror",
             str(source), "-o", str(cls.binary)],
            capture_output=True, text=True, check=False, timeout=60,
        )
        if build.returncode != 0:
            raise AssertionError(f"C regression build failed:\n{build.stderr}")

    def observe(self, native_result: int, error_page: int) -> tuple[int, ...]:
        result = subprocess.run(
            [str(self.binary), str(native_result), str(error_page)],
            capture_output=True, text=True, check=True, timeout=10,
        )
        return tuple(int(value) for value in result.stdout.split())

    def test_positive_decisions_take_precedence_in_both_paths(self) -> None:
        for status in (302, 403, 451):
            for error_page in (0, 1):
                with self.subTest(status=status, error_page=error_page):
                    self.assertEqual(self.observe(status, error_page),
                                     (3, status, 1, 1, status, 1, 1))

    def test_p1_allow_continues_to_p2_even_on_error_pages(self) -> None:
        for error_page in (0, 1):
            with self.subTest(error_page=error_page):
                self.assertEqual(self.observe(0, error_page),
                                 (2, -5, 0, 0, 0, 0, 0))

    def test_native_error_remains_fail_closed_without_a_success_event(self) -> None:
        for error_page in (0, 1):
            with self.subTest(error_page=error_page):
                self.assertEqual(self.observe(-1, error_page), (0, 500, 1, 0, 500, 1, 0))


if __name__ == "__main__":
    unittest.main()
