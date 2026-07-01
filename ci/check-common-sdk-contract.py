#!/usr/bin/env python3
"""Static contract checks for connector-neutral common SDK files."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "common"
CHECK_COMMON_HELPERS = ROOT / "ci" / "check-common-helpers.sh"
MAKEFILE = ROOT / "Makefile"
SEARCH_ROOTS = [COMMON / "include", COMMON / "src"]
FORBIDDEN_INCLUDES = (
    "#include <ngx_",
    "#include \"ngx_",
    "#include <httpd.h>",
    "#include \"httpd.h\"",
    "#include <haproxy",
    "#include \"haproxy",
    "#include <envoy",
    "#include \"envoy",
    "#include <traefik",
    "#include \"traefik",
    "#include <lighttpd",
    "#include \"lighttpd",
)
SERVER_TOKENS = ("nginx", "apache", "haproxy", "envoy", "traefik", "lighttpd")
NON_INTEGRATION_TERMS = ("not integrate", "not imply", "future", "separately", "no connector")


def fail(message: str) -> None:
    print(f"common-sdk-contract: {message}", file=sys.stderr)
    sys.exit(1)


def text_without_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//.*", "", text)


for header in (COMMON / "include" / "msconnector").glob("*.h"):
    text = header.read_text(encoding="utf-8")
    guard = "MSCONNECTOR_" + header.stem.upper() + "_H"
    if f"#ifndef {guard}" not in text or f"#define {guard}" not in text:
        fail(f"missing include guard {guard} in {header.relative_to(ROOT)}")

for source in (COMMON / "src").glob("*.c"):
    text = source.read_text(encoding="utf-8")
    expected = f'#include "msconnector/{source.stem}.h"'
    if expected not in text:
        fail(f"missing matching header include {expected} in {source.relative_to(ROOT)}")

for root in SEARCH_ROOTS:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        uncommented = text_without_comments(text).lower()
        lowered = text.lower()
        for token in FORBIDDEN_INCLUDES:
            if token in lowered:
                fail(f"forbidden connector-specific include {token!r} in {path.relative_to(ROOT)}")
        for token in SERVER_TOKENS:
            if token in uncommented:
                fail(f"server-specific token {token!r} outside comments in {path.relative_to(ROOT)}")
            if token in lowered and not any(term in lowered for term in NON_INTEGRATION_TERMS):
                fail(f"server-specific token {token!r} lacks non-integration context in {path.relative_to(ROOT)}")

helper_text = CHECK_COMMON_HELPERS.read_text(encoding="utf-8")
makefile_text = MAKEFILE.read_text(encoding="utf-8")
combined_check_text = helper_text + "\n" + makefile_text
if "common/src/*.c" not in helper_text:
    fail("check-common-helpers.sh does not compile all common/src/*.c files")
if "-std=c99" in helper_text:
    fail("hardcoded -std=c99 remains in check-common-helpers.sh")
if "MSCONNECTOR_C_STD" not in helper_text or "MSCONNECTOR_CFLAGS" not in helper_text:
    fail("check-common-helpers.sh does not expose configurable common C standard flags")
if "MSCONNECTOR_C_STD ?= c17" not in makefile_text:
    fail("Makefile does not define c17 as the default common C standard")
if "-std=c20" in combined_check_text:
    fail("common C checks must not use -std=c20")
if "-std=c26" in combined_check_text:
    fail("common C checks must not use -std=c26")
if "--profile c23" not in makefile_text or "c2x" not in makefile_text:
    fail("optional c23/c2x common helper check is not wired")
if "--profile c2y" not in makefile_text or "gnu2y" not in makefile_text:
    fail("optional future-C c2y/gnu2y common helper check is not wired")


detect_text = (ROOT / "ci" / "detect-c-standard.py").read_text(encoding="utf-8")
if "args.cc" in detect_text or 'parser.add_argument("--cc"' in detect_text:
    fail("detect-c-standard.py must not accept or use raw --cc command paths")
if "shell=True" in detect_text:
    fail("detect-c-standard.py must not use shell=True")
if "[0-9]" in detect_text:
    fail("detect-c-standard.py compiler regex must not use [0-9]")
if detect_text.count('"-std=c17"') > 1:
    fail("detect-c-standard.py duplicates the -std=c17 literal outside its constant")
if detect_text.count('"-std=c2x"') > 1:
    fail("detect-c-standard.py duplicates the -std=c2x literal outside its constant")
if "--compiler" not in detect_text or "choices=sorted(ALLOWED_COMPILER_IDS)" not in detect_text:
    fail("detect-c-standard.py must expose only an allow-listed compiler selector")
if detect_text.count("subprocess.run(") != 1 or "def compiler_supports" not in detect_text:
    fail("detect-c-standard.py subprocess.run must appear only in the compiler probe helper")


def extract_http_status_table_statuses(source_text: str) -> set[int]:
    table_match = re.search(
        r"static\s+const\s+msconnector_http_status_info\s+http_statuses\[\]\s*=\s*\{(?P<body>.*?)\};",
        source_text,
        flags=re.S,
    )
    if table_match is None:
        fail("common/src/http_status.c does not expose a parseable http_statuses table")
    return {
        int(match.group(1))
        for match in re.finditer(r"\{\s*(\d{3})\s*,[^{}]*,\s*1\s*\}", table_match.group("body"))
    }


def extract_generator_statuses(source_text: str) -> set[int]:
    list_match = re.search(
        r"ALLOWED_BLOCK_STATUSES\s*=\s*\((?P<body>.*?)\)",
        source_text,
        flags=re.S,
    )
    if list_match is None:
        fail("ci/generate-block-status-config.py does not expose a parseable ALLOWED_BLOCK_STATUSES tuple")
    return {int(value) for value in re.findall(r"\b(\d{3})\b", list_match.group("body"))}


http_status_source = (ROOT / "common" / "src" / "http_status.c").read_text(encoding="utf-8")
block_status_source = (ROOT / "common" / "src" / "block_statuses.c").read_text(encoding="utf-8")
generator_source = (ROOT / "ci" / "generate-block-status-config.py").read_text(encoding="utf-8")
http_statuses = extract_http_status_table_statuses(http_status_source)
generator_statuses = extract_generator_statuses(generator_source)
if http_statuses != generator_statuses:
    fail(
        "HTTP status metadata and generator ALLOWED_BLOCK_STATUSES drift: "
        f"http_status.c={sorted(http_statuses)} generator={sorted(generator_statuses)}"
    )
if "case 400:" in block_status_source or "case 403:" in block_status_source:
    fail("common/src/block_statuses.c must delegate block status decisions instead of keeping a divergent switch list")
if "msconnector_http_status_is_block_response" not in block_status_source:
    fail("common/src/block_statuses.c does not delegate block status allow checks to HTTP status metadata")

event_header = (ROOT / "common" / "include" / "msconnector" / "event.h").read_text(encoding="utf-8")
event_source = (ROOT / "common" / "src" / "event.c").read_text(encoding="utf-8")
if "message_id" not in event_header or "message;" not in event_header:
    fail("common event model must contain message_id and message fields")
if "requested_action" not in event_header or "actual_action" not in event_header:
    fail("common event model must contain requested_action and actual_action fields")
if "msconnector_event_set_phase4_hard_abort_after_200" not in event_header or "MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200" not in event_source:
    fail("common event model must expose the Phase 4 hard-abort-after-200 helper")
if "body_payload" in event_source or "request_body" in event_source or "response_body" in event_source:
    fail("common event JSON writer must not include request/response body payload fields")
if "truncated" not in event_header or "truncated" not in event_source:
    fail("common event JSON writer must expose truncation")
if '{200, "OK", "Request succeeded", MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS, 0}' not in http_status_source:
    fail("common HTTP status metadata must include non-blocking 200 OK metadata")

print("common-sdk-contract: pass")
