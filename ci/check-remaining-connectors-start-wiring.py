#!/usr/bin/env python3
"""Verify config, request-free start and request runtime stages remain distinct."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = (ROOT / "Makefile").read_text(encoding="utf-8")
errors: list[str] = []

for connector in ("envoy", "traefik", "lighttpd"):
    for prefix in ("check", "start-smoke", "runtime-smoke"):
        target = f"{prefix}-{connector}" if prefix != "check" else f"check-{connector}-config"
        if re.search(rf"^{re.escape(target)}\s*:", MAKEFILE, flags=re.MULTILINE) is None:
            errors.append(f"root Makefile missing {target}")

start_scripts = {
    "envoy": ROOT / "connectors/envoy/harness/start_envoy_connector.sh",
    "traefik": ROOT / "connectors/traefik/scripts/start-smoke.sh",
    "lighttpd": ROOT / "connectors/lighttpd/harness/start_lighttpd_smoke.sh",
}
for connector, path in start_scripts.items():
    if not path.is_file():
        errors.append(f"{connector}: start-smoke script missing")
        continue
    content = path.read_text(encoding="utf-8", errors="replace")
    for request_token in ("curl ", "urllib.request", "X-Modsec-Smoke", "/blocked"):
        if request_token in content:
            errors.append(f"{connector}: request-free start smoke contains {request_token!r}")
    if not any(token in content for token in ("kill -0", "process.poll")):
        errors.append(f"{connector}: start smoke does not check process liveness")
    if not any(token in content for token in ("wait ", ".wait(")):
        errors.append(f"{connector}: start smoke does not wait for clean shutdown")

if "start-smoke-remaining-connectors" not in MAKEFILE:
    errors.append("aggregate start smoke target missing")
if "runtime-smoke-remaining-connectors" not in MAKEFILE:
    errors.append("aggregate runtime smoke target missing")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print("remaining connectors start wiring: ok")
