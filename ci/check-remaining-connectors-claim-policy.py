#!/usr/bin/env python3
"""Keep remaining-connector status claims aligned with executable evidence."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CONNECTORS = ("envoy", "traefik", "lighttpd")
REPORTS = tuple(
    f"reports/{name}-connector-readiness{suffix}.md"
    for name in CONNECTORS
    for suffix in ("", ".de")
) + (
    "reports/remaining-connectors-readiness.md",
    "reports/remaining-connectors-readiness.de.md",
)
ALLOWED = (
    "compile_verified",
    "link_verified",
    "config_load_verified",
    "start_smoke_verified",
    "minimal_runtime_smoke",
    "partial_runtime_path",
    "requires_runtime_evidence",
    "connector-gap",
    "not_verified",
)
POSITIVE_FORBIDDEN = (
    r"production[-_ ]ready\s*[:=]\s*(?:true|yes|verified)",
    r"security[-_ ]verified\s*[:=]\s*(?:true|yes)",
    r"crs[-_ ]verified\s*[:=]\s*(?:true|yes)",
    r"full[-_ ]matrix[-_ ]verified\s*[:=]\s*(?:true|yes)",
    r"response[-_ ]body[-_ ]verified\s*[:=]\s*(?:true|yes)",
    r"all[-_ ]connectors[-_ ]verified\s*[:=]\s*(?:true|yes)",
)

errors: list[str] = []
for relative in REPORTS:
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"readiness report missing: {relative}")
        continue
    content = path.read_text(encoding="utf-8", errors="replace")
    if not any(status in content for status in ALLOWED):
        errors.append(f"readiness report has no allowed evidence status: {relative}")
    for pattern in POSITIVE_FORBIDDEN:
        if re.search(pattern, content, flags=re.IGNORECASE):
            errors.append(f"forbidden positive claim in {relative}: {pattern}")
    if "Claims deliberately not made" not in content and "Bewusst nicht erhobene Claims" not in content:
        errors.append(f"claim-boundary section missing: {relative}")

for connector in CONNECTORS:
    metadata_path = ROOT / "connectors" / connector / "metadata.c"
    metadata = metadata_path.read_text(encoding="utf-8", errors="replace")
    english_path = ROOT / "reports" / f"{connector}-connector-readiness.md"
    if not english_path.is_file():
        continue
    report = english_path.read_text(encoding="utf-8", errors="replace")
    metadata_statuses = {status for status in ALLOWED if f'"{status}"' in metadata}
    if not metadata_statuses:
        errors.append(f"{connector}: metadata has no allowed status")
    elif not any(status in report for status in metadata_statuses):
        errors.append(f"{connector}: report status does not match metadata {sorted(metadata_statuses)}")
    runtime_paths = {
        "envoy": ROOT / "connectors/envoy/harness/run_envoy_connector_runtime.sh",
        "traefik": ROOT / "connectors/traefik/scripts/runtime-smoke.sh",
        "lighttpd": ROOT / "connectors/lighttpd/harness/runtime_lighttpd_smoke.sh",
    }
    if "minimal_runtime_smoke" in metadata and not runtime_paths[connector].is_file():
        errors.append(f"{connector}: runtime status promoted without executable evidence producer")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("remaining connectors claim policy: ok")
