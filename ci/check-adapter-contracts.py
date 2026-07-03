#!/usr/bin/env python3
"""Check global common adapter contracts for new connectors."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HEADERS = [
    "adapter.h", "adapter_contract.h", "adapter_metadata.h", "config.h",
    "directive_spec.h", "directive_adapter.h", "request.h",
    "request_mapper_contract.h", "response.h", "response_mapper_contract.h",
    "decision.h", "event.h", "event_jsonl.h", "capabilities.h",
    "body_policy.h", "resource_limits.h", "dos_guard.h", "flow_guard.h",
    "integrity_event.h", "crs.h",
]
SOURCES = [
    "adapter.c", "adapter_contract.c", "adapter_metadata.c", "config.c",
    "directive_spec.c", "directive_adapter.c", "body_policy.c",
    "resource_limits.c", "dos_guard.c", "flow_guard.c", "integrity_event.c",
    "request_mapper_contract.c", "response_mapper_contract.c", "crs.c",
    "decision.c", "event.c", "event_jsonl.c", "capabilities.c",
]
SERVER_TOKENS = ["ngx_", "httpd", "apr_", "haproxy", "envoy", "lighttpd", "traefik"]
SERVER_INCLUDES = re.compile(r'#\s*include\s+[<"]([^>"]*(?:nginx|ngx_|httpd|http_config|apr_|haproxy|envoy|lighttpd|traefik)[^>"]*)[>"]')

ok = True
for name in HEADERS:
    path = ROOT / "common/include/msconnector" / name
    if not path.exists():
        print(f"missing common header: {path.relative_to(ROOT)}")
        ok = False
for name in SOURCES:
    path = ROOT / "common/src" / name
    if not path.exists():
        print(f"missing common source: {path.relative_to(ROOT)}")
        ok = False

adapter_h = (ROOT / "common/include/msconnector/adapter.h").read_text() if (ROOT / "common/include/msconnector/adapter.h").exists() else ""
for token in ("metadata", "init", "process", "finish"):
    if token not in adapter_h:
        print(f"adapter.h missing callback-like token: {token}")
        ok = False
metadata_h = (ROOT / "common/include/msconnector/adapter_metadata.h").read_text() if (ROOT / "common/include/msconnector/adapter_metadata.h").exists() else ""
for token in ("connector_name", "server_family", "source_kind", "build_status", "runtime_status", "verification_status"):
    if token not in metadata_h:
        print(f"adapter_metadata.h missing field: {token}")
        ok = False

for rel in ("common/include/msconnector/request_mapper_contract.h", "common/include/msconnector/response_mapper_contract.h", "common/src/request_mapper_contract.c", "common/src/response_mapper_contract.c"):
    path = ROOT / rel
    if path.exists():
        text = path.read_text().lower()
        for token in SERVER_TOKENS:
            if token in text:
                print(f"server token in mapper contract: {rel}: {token}")
                ok = False

for path in list((ROOT / "common/include/msconnector").glob("*.h")) + list((ROOT / "common/src").glob("*.c")):
    text = path.read_text(errors="ignore")
    match = SERVER_INCLUDES.search(text)
    if match:
        print(f"server-specific include in common: {path.relative_to(ROOT)}: {match.group(1)}")
        ok = False

print("adapter-contracts: common contracts present; connector runtime adoption not claimed")
if not ok:
    sys.exit(1)
