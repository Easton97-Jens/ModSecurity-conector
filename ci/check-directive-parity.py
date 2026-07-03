#!/usr/bin/env python3
"""Check global directive spec/adapter parity without enforcing connector adoption."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC_H = ROOT / "common/include/msconnector/directive_spec.h"
SPEC_C = ROOT / "common/src/directive_spec.c"
ADAPTER_H = ROOT / "common/include/msconnector/directive_adapter.h"
ADAPTER_C = ROOT / "common/src/directive_adapter.c"
DIRECTIVES_H = ROOT / "common/include/msconnector/directives.h"
KNOWN = [
    "modsecurity",
    "modsecurity_rules",
    "modsecurity_rules_file",
    "modsecurity_rules_remote",
    "modsecurity_transaction_id",
    "modsecurity_transaction_id_expr",
    "modsecurity_use_error_log",
    "modsecurity_phase4_mode",
    "modsecurity_phase4_content_types_file",
    "modsecurity_phase4_log",
    "modsecurity_phase4_body_limit",
]
POLICY_FOR_TYPE = {
    "MSCONNECTOR_DIRECTIVE_VALUE_BOOL": {"MSCONNECTOR_DIRECTIVE_ARG_ONE"},
    "MSCONNECTOR_DIRECTIVE_VALUE_STRING": {"MSCONNECTOR_DIRECTIVE_ARG_ONE"},
    "MSCONNECTOR_DIRECTIVE_VALUE_PATH": {"MSCONNECTOR_DIRECTIVE_ARG_ONE"},
    "MSCONNECTOR_DIRECTIVE_VALUE_ENUM": {"MSCONNECTOR_DIRECTIVE_ARG_ONE"},
    "MSCONNECTOR_DIRECTIVE_VALUE_SIZE": {"MSCONNECTOR_DIRECTIVE_ARG_ONE"},
}

missing_files = [p for p in (SPEC_H, SPEC_C, ADAPTER_H, ADAPTER_C) if not p.exists()]
if missing_files:
    for path in missing_files:
        print(f"missing directive file: {path.relative_to(ROOT)}")
    sys.exit(1)

macros = dict(re.findall(r'#define\s+(MSCONNECTOR_DIRECTIVE_[A-Z0-9_]+)\s+"([^"]+)"', DIRECTIVES_H.read_text()))
spec_text = SPEC_C.read_text()
adapter_text = ADAPTER_C.read_text()

specs = {}
for macro, value_type in re.findall(r'\{\s*(MSCONNECTOR_DIRECTIVE_[A-Z0-9_]+)\s*,\s*(MSCONNECTOR_DIRECTIVE_VALUE_[A-Z]+)', spec_text):
    if macro in macros:
        specs[macros[macro]] = value_type

entries = []
for match in re.finditer(r'\{[^{}]*?(MSCONNECTOR_DIRECTIVE_[A-Z0-9_]+)\s*,\s*(MSCONNECTOR_DIRECTIVE_[A-Z0-9_]+)\s*,\s*MSCONNECTOR_DIRECTIVE_SCOPE_[A-Z]+\s*,\s*(MSCONNECTOR_DIRECTIVE_ARG_[A-Z_]+)', adapter_text):
    canonical_macro, host_macro, policy = match.groups()
    entries.append((macros.get(canonical_macro, canonical_macro), macros.get(host_macro, host_macro), policy))

ok = True
canonicals = [entry[0] for entry in entries]
for name in sorted(specs):
    if name not in canonicals:
        print(f"missing directive adapter entry: {name}")
        ok = False
for name in sorted(set(canonicals)):
    if canonicals.count(name) > 1:
        print(f"duplicate canonical_name: {name}")
        ok = False
for canonical, host, policy in entries:
    if not host:
        print(f"empty host_name: {canonical}")
        ok = False
    allowed = POLICY_FOR_TYPE.get(specs.get(canonical), set())
    if canonical == "modsecurity_rules":
        allowed = {"MSCONNECTOR_DIRECTIVE_ARG_RAW", "MSCONNECTOR_DIRECTIVE_ARG_ONE_OR_MORE"}
    if allowed and policy not in allowed:
        print(f"implausible argument policy: {canonical} {policy}")
        ok = False
for name in KNOWN:
    if name not in specs or name not in canonicals:
        print(f"known directive missing: {name}")
        ok = False

print("connector directive adoption: not enforced in this check")
if not ok:
    sys.exit(1)
print("directive-parity: common directive spec/adapter parity present")
