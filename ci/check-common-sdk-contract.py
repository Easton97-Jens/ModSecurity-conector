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

print("common-sdk-contract: pass")
