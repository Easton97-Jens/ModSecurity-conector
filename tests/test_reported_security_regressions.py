"""Source-isolated regressions for the reported B09, B13 and C07 findings.

The compiled checks exercise the actual small C helpers extracted from the
checkout. Minimal surrounding types and header lookup are test stubs, not a
real host/parser. C07 and caller-order checks are source contracts only.
These tests do not establish NGINX/lighttpd/Traefik runtime protection.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "common/runtime/http_authorization_service.c"
NGINX = ROOT / "connectors/nginx/src/ngx_http_modsecurity_common.h"
SIDECAR = ROOT / "connectors/lighttpd/stock_sidecar/stock_sidecar.c"


def balanced_block(source: str, opening: int) -> str:
    """Return a C block; ignore brace characters inside comments and strings."""
    if opening >= len(source) or source[opening] != "{":
        raise ValueError("expected opening brace")
    depth = 0
    index = opening
    state = "code"
    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""
        if state == "line":
            if char == "\n":
                state = "code"
        elif state == "comment":
            if char == "*" and following == "/":
                state = "code"
                index += 1
        elif state in ("'", '"'):
            if char == "\\":
                index += 1
            elif char == state:
                state = "code"
        elif char == "/" and following == "/":
            state = "line"
            index += 1
        elif char == "/" and following == "*":
            state = "comment"
            index += 1
        elif char in ("'", '"'):
            state = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[opening:index + 1]
        index += 1
    raise ValueError("unterminated C block")


def function_body(source: str, name: str) -> str:
    match = re.search(r"\b" + re.escape(name) + r"\s*\([^;{}]*\)\s*\{", source)
    if match is None:
        raise ValueError(f"C function definition not found: {name}")
    return balanced_block(source, match.end() - 1)


def macro_line(source: str, name: str) -> str:
    match = re.search(r"^#define[ \t]+" + re.escape(name) + r"[ \t]+[^\n]+", source, re.M)
    if match is None:
        raise ValueError(f"C macro not found: {name}")
    return match.group(0)


class ReportedSecurityRegressions(unittest.TestCase):
    def compile_and_run(self, program: str) -> None:
        compiler = shutil.which("cc")
        if compiler is None:
            self.skipTest("C compiler unavailable; isolated helper regression not executed")
        # The repository's externally configured TMPDIR controls scratch storage.
        with tempfile.TemporaryDirectory(prefix="msconnector-finding-regression-") as temporary:
            root = Path(temporary)
            source = root / "regression.c"
            binary = root / "regression"
            source.write_text(program, encoding="utf-8")
            subprocess.run(
                [compiler, "-std=c11", "-Wall", "-Wextra", "-Werror",
                 str(source), "-o", str(binary)],
                check=True, capture_output=True, text=True, timeout=60,
            )
            subprocess.run(
                [str(binary)], check=True, capture_output=True, text=True, timeout=10,
            )

    def test_b09_active_intervention_survives_error_page(self) -> None:
        source = NGINX.read_text(encoding="utf-8")
        enum = re.search(
            r"typedef enum \{[^}]*\} msconnector_nginx_intervention_disposition;",
            source,
        )
        self.assertIsNotNone(enum)
        assert enum is not None
        body = function_body(source, "ngx_http_modsecurity_intervention_disposition")
        program = "#include <assert.h>\n" + enum.group(0) + "\n"
        program += (
            "static msconnector_nginx_intervention_disposition classify("
            "int ret, int error_page) " + body + "\n"
        )
        program += """
int main(void) {
    assert(classify(-1, 0) == MSCONNECTOR_NGINX_INTERVENTION_FAILURE);
    assert(classify(-1, 1) == MSCONNECTOR_NGINX_INTERVENTION_FAILURE);
    assert(classify(0, 0) == MSCONNECTOR_NGINX_INTERVENTION_ALLOW);
    assert(classify(0, 1) == MSCONNECTOR_NGINX_INTERVENTION_BYPASS);
    assert(classify(403, 0) == MSCONNECTOR_NGINX_INTERVENTION_ACTIVE);
    assert(classify(403, 1) == MSCONNECTOR_NGINX_INTERVENTION_ACTIVE);
    assert(classify(302, 1) == MSCONNECTOR_NGINX_INTERVENTION_ACTIVE);
    return 0;
}
"""
        self.compile_and_run(program)

    def test_b13_authoritative_uri_boundaries_and_no_fallback(self) -> None:
        source = AUTH.read_text(encoding="utf-8")
        limits = (ROOT / "common/include/msconnector/limits.h").read_text(encoding="utf-8")
        program = """
#include <assert.h>
#include <stddef.h>
#include <string.h>
"""
        program += macro_line(limits, "MSCONNECTOR_MAX_HEADER_VALUE_LENGTH") + "\n"
        program += macro_line(source, "AUTH_URI_SIZE") + "\n"
        bound = re.search(r"char uri_override\[([^\]]+)\];", source)
        self.assertIsNotNone(bound)
        assert bound is not None
        program += """
typedef struct {
    const char *name;
    const char *value;
    size_t value_size;
} msconnector_header;
typedef struct {
    msconnector_header *headers;
    size_t header_count;
    char uri_override[URI_OVERRIDE_BOUND];
    char *uri;
} parsed_http_request;
typedef struct {
    const char *const *original_uri_headers;
    size_t original_uri_header_count;
} msconnector_http_authorization_profile;

/* Lookup stub: the production parser/header library is outside this unit. */
static const msconnector_header *msconnector_headers_find_first(
    const msconnector_header *headers, size_t count, const char *name) {
    for (size_t i = 0; i < count; ++i) {
        if (strcmp(headers[i].name, name) == 0) return &headers[i];
    }
    return NULL;
}
""".replace("URI_OVERRIDE_BOUND", bound.group(1))
        program += (
            "static int copy_slice(const char *value, size_t value_size, "
            "char *destination, size_t destination_size) "
            + function_body(source, "copy_slice") + "\n"
        )
        program += (
            "static const char *request_uri(parsed_http_request *request, "
            "const msconnector_http_authorization_profile *profile) "
            + function_body(source, "request_uri") + "\n"
        )
        program += """
int main(void) {
    const char *const names[] = {"X-Forwarded-Uri", "X-Original-Uri"};
    msconnector_http_authorization_profile profile = {names, 2U};
    char path[8194];
    char fallback[] = "/authorize";
    msconnector_header headers[2] = {
        {"X-Forwarded-Uri", path, 0U},
        {"X-Original-Uri", "/secondary", sizeof("/secondary") - 1U}
    };
    parsed_http_request request = {0};
    request.headers = headers;
    request.header_count = 2U;
    request.uri = fallback;
    memset(path, 'a', sizeof(path));
    path[0] = '/';

    const size_t sizes[] = {8191U, 8192U};
    for (size_t i = 0; i < 2U; ++i) {
        headers[0].value_size = sizes[i];
        const char *result = request_uri(&request, &profile);
        assert(result == request.uri_override);
        assert(strlen(result) == sizes[i]);
        assert(memcmp(result, path, sizes[i]) == 0);
    }
    headers[0].value_size = 8193U;
    assert(request_uri(&request, &profile) == NULL);
    headers[0].value_size = 0U;
    assert(request_uri(&request, &profile) == NULL);
    headers[0].value = "invalid";
    headers[0].value_size = sizeof("invalid") - 1U;
    assert(request_uri(&request, &profile) == NULL);
    headers[0].value = NULL;
    assert(request_uri(&request, &profile) == NULL);

    const char embedded_nul[] = {'/', 'a', '\\0', 'b'};
    headers[0].value = embedded_nul;
    headers[0].value_size = sizeof(embedded_nul);
    assert(request_uri(&request, &profile) == NULL);

    request.headers = &headers[1];
    request.header_count = 1U;
    assert(strcmp(request_uri(&request, &profile), "/secondary") == 0);
    request.header_count = 0U;
    assert(request_uri(&request, &profile) == fallback);
    return 0;
}
"""
        self.compile_and_run(program)

    def test_b13_caller_rejects_missing_resolved_uri_before_runtime(self) -> None:
        body = function_body(AUTH.read_text(encoding="utf-8"), "handle_authorization_request")
        resolution = body.index("source.uri = request_uri(")
        check = body.index("if (source.uri == NULL)", resolution)
        invocation = body.index("authorization_process_runtime_request(", resolution)
        self.assertLess(check, invocation)
        failure = balanced_block(body, body.index("{", check))
        self.assertIn("response.status = 400;", failure)
        self.assertIn('response.decision_name = "invalid_request";', failure)
        self.assertIn("parsed_request_destroy(&parsed);", failure)
        self.assertIn("return 0;", failure)

    def test_c07_off_branch_records_unapplied_action_not_requested_status(self) -> None:
        """Source contract only: the Framework patch covers event normalization."""
        source = SIDECAR.read_text(encoding="utf-8")
        marker = "if (phase4_mode == MSCONNECTOR_PHASE4_MODE_OFF)"
        start = source.index(marker)
        branch = balanced_block(source, source.index("{", start))
        self.assertNotIn("sidecar_record_action(", branch)
        self.assertIn("return msconnector_runtime_transaction_record_host_action(", branch)
        self.assertIn("MSCONNECTOR_DECISION_ACTION_LOG_ONLY", branch)
        self.assertIn('state->payload.response_headers.status_code, "log_only", 0,', branch)


if __name__ == "__main__":
    unittest.main()
