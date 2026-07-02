#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMON_APIS = ["resource_limits", "memory", "flow_guard", "integrity_event", "dos_guard"]
EVENT_JSON_SOURCES = [
    "common/src/event.c",
    "common/src/event_jsonl.c",
    "common/src/integrity_event.c",
    "common/src/decision.c",
]
FORBIDDEN_PAYLOAD_FIELDS = [
    "request_body",
    "response_body",
    "body_payload",
    "raw_body",
    "payload",
    "body",
    "request_payload",
    "response_payload",
]
FORBIDDEN_COMMON_TOKENS = [
    "#include <httpd",
    "#include <ngx_",
    "#include <haproxy",
    "#include <modsecurity/",
    "#include \"modsecurity/",
    "strcpy(",
    "strcat(",
    "sprintf(",
    "gets(",
]
FORBIDDEN_CLAIM_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"connector is protected",
        r"runtime secure",
        r"production[- ]ready",
        r"security[- ]verified",
        r"verified for (nginx|apache|haproxy|envoy|lighttpd|traefik)",
        r"response_body verified",
        r"crs verified",
        r"full matrix verified",
    ]
]
FORBIDDEN_HASH_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"secure hash",
        r"cryptographic hash",
        r"tamper-proof",
        r"cannot be manipulated",
    ]
]

errors = []

for name in COMMON_APIS:
    for directory, suffix in [("common/include/msconnector", ".h"), ("common/src", ".c")]:
        path = ROOT / directory / f"{name}{suffix}"
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    src = ROOT / "common/src" / f"{name}.c"
    if src.is_file() and f'#include "msconnector/{name}.h"' not in src.read_text():
        errors.append(f"{src.relative_to(ROOT)} missing matching header include")

common_text = "\n".join(path.read_text(errors="ignore") for path in (ROOT / "common").rglob("*.[ch]"))
for token in FORBIDDEN_COMMON_TOKENS:
    if token in common_text:
        errors.append(f"forbidden common token {token}")

for source in EVENT_JSON_SOURCES:
    path = ROOT / source
    if not path.is_file():
        errors.append(f"missing event/decision JSON source {source}")
        continue
    text = path.read_text(errors="ignore")
    for field in FORBIDDEN_PAYLOAD_FIELDS:
        quoted = f'"{field}"'
        escaped = f'\\"{field}\\"'
        if quoted in text or escaped in text:
            errors.append(f"{source} writes forbidden body/payload JSON field {field}")

integrity_api = (ROOT / "common/include/msconnector/integrity_event.h").read_text(errors="ignore") + (ROOT / "common/src/integrity_event.c").read_text(errors="ignore")
if "non_crypto" not in integrity_api:
    errors.append("integrity API must name non-cryptographic hash helpers with non_crypto")

doc_text = "\n".join(path.read_text(errors="ignore") for path in (ROOT / "docs").rglob("common-security-data-flow*.md"))
if "non_crypto" not in doc_text or "CI" not in doc_text or "Smoke" not in doc_text and "smoke" not in doc_text:
    errors.append("common security docs must state non_crypto CI/smoke scope")
for pattern in FORBIDDEN_HASH_PATTERNS:
    if pattern.search(integrity_api + "\n" + doc_text):
        errors.append(f"forbidden hash/integrity claim: {pattern.pattern}")

claim_paths = list((ROOT / "common").rglob("*.[ch]"))
claim_paths += [
    ROOT / "docs/architecture/common-security-data-flow.md",
    ROOT / "docs/architecture/common-security-data-flow.de.md",
    ROOT / "ci/check-common-flow-integrity.py",
    ROOT / "ci/check-common-memory-safety.sh",
    ROOT / "ci/check-common-helpers.sh",
]
changed_scope_text = "\n".join(
    path.read_text(errors="ignore")
    for path in claim_paths
    if path.is_file()
)
for pattern in FORBIDDEN_CLAIM_PATTERNS:
    if pattern.search(changed_scope_text):
        errors.append(f"forbidden runtime/production claim: {pattern.pattern}")

dos = (ROOT / "common/src/dos_guard.c").read_text(errors="ignore")
if "msconnector_resource_limits" not in dos:
    errors.append("DoS guard does not use resource limits")
if "enum msconnector_phase" not in (ROOT / "common/include/msconnector/flow_guard.h").read_text(errors="ignore"):
    errors.append("flow guard lacks enum msconnector_phase")

makefile = (ROOT / "Makefile").read_text(errors="ignore")
for target in ["check-common-security-contract", "check-common-memory-safety", "check-common-flow-integrity"]:
    if not re.search(rf"^{target}:\n\t", makefile, re.MULTILINE):
        errors.append(f"Makefile target {target} is not executable")
    lint_block = makefile[makefile.find("lint: check-framework") : makefile.find("summary: check-framework")]
    if f"$(MAKE) {target}" not in lint_block:
        errors.append(f"lint does not run {target}")
if not re.search(r"^quick-check codex-check: lint", makefile, re.MULTILINE):
    errors.append("quick-check/codex-check must depend on lint")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("common security contract: ok")
