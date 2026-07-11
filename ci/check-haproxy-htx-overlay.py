#!/usr/bin/env python3
"""Static contract checks for the version-pinned HAProxy HTX overlay.

The overlay is intentionally optional until a host runtime verifies it.  These
checks prevent an apparently incremental implementation from regressing back
to a buffered SPOE sample or from evaluating Phase 4 before HTTP EOS.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "connectors/haproxy/htx-overlay"
SOURCE = OVERLAY / "haproxy_modsecurity_htx_filter.c"
PATCH = OVERLAY / "haproxy-3.2.21-makefile.patch"
BUILD = OVERLAY / "build-overlay.sh"


def function_body(text: str, signature: str) -> str:
    start = text.index(signature)
    open_brace = text.index("{", start)
    depth = 0
    for position in range(open_brace, len(text)):
        if text[position] == "{":
            depth += 1
        elif text[position] == "}":
            depth -= 1
            if depth == 0:
                return text[start : position + 1]
    raise ValueError(f"unterminated function: {signature}")


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    makefile_patch = PATCH.read_text(encoding="utf-8")
    build = BUILD.read_text(encoding="utf-8")
    response_payload = function_body(
        source, "static int haproxy_modsecurity_htx_filter_http_payload(")
    response_append = function_body(
        source, "static int haproxy_modsecurity_htx_append_response_payload(")
    response_end = function_body(
        source, "static int haproxy_modsecurity_htx_filter_http_end(")
    checks: list[tuple[bool, str]] = [
        ("haproxy_modsecurity_htx_filter_http_payload" in source and
         "haproxy_modsecurity_htx_filter_http_end" in source,
         "HAProxy 3.2.21 filter exposes http_payload and http_end hooks"),
        ("HTX_BLK_DATA" in source and "htx_find_offset" in source and
         "htx_get_blk_value" in source,
         "response hook walks current HTX DATA slices instead of materializing a body"),
        ("haproxy_modsecurity_transaction_append_response_body_chunk" in response_append and
         "return (int)len;" in response_payload,
         "response payload forwards borrowed chunks and never holds HAProxy output"),
        ("ctx->response_finished = 1;" in response_end and
         "haproxy_modsecurity_transaction_finish_response_body" in response_end and
         response_end.index("ctx->response_finished = 1;") <
         response_end.index("haproxy_modsecurity_transaction_finish_response_body"),
         "response Phase 4 finalization is guarded before the sole EOS call"),
        (source.count("haproxy_modsecurity_transaction_finish_response_body(") == 1,
         "source has one binding finish_response_body callsite"),
        ("no late HAProxy action is attempted" in source and
         "response-body (late)" in source,
         "late Phase 4 interventions are explicitly observer-only"),
        (all(token not in source for token in ("wait-for-body", "res.body", "chunk_memcat")),
         "overlay does not reintroduce a wait-for-body or connector-owned response buffer"),
        ("register_data_filter" in source and "unregister_data_filter" in source,
         "overlay registers only the active HAProxy data callbacks"),
        ("expected HAProxy 3.2.21" in build and
         "haproxy_modsecurity_htx_filter.c" in build and
         "haproxy-3.2.21-makefile.patch" in build,
         "build script is pinned to HAProxy 3.2.21 and stages a separate worktree"),
        ("canonical_path()" in build and
         "HAPROXY_HTX_BUILD_DIR must be outside the verified source tree" in build and
         '"$SOURCE_DIR"/*' in build and
         "patch --dry-run -p1" in build,
         "build script rejects source-tree output and validates the disposable patch"),
        ("haproxy_modsecurity_htx_filter.o" in makefile_patch and
         "haproxy_modsecurity_binding.o" in makefile_patch,
         "source-linked Makefile patch includes the HTX filter and binding"),
    ]
    ok = True
    for condition, message in checks:
        print(f"{'PASS' if condition else 'FAIL'}: {message}")
        ok = ok and condition
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
