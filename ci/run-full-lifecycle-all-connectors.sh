#!/bin/sh
# Run every selected connector through the strict, payload-free evidence
# profile.  The individual runner owns host provisioning and finalization;
# this wrapper deliberately continues after a failure so one fresh run ID
# records the outcome for every connector.
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=${CONNECTOR_ROOT:-$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)}
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}
PYTHON=${PYTHON:-python3}
EVIDENCE_ROOT=${EVIDENCE_ROOT:-${BUILD_ROOT:-${VERIFIED_BUILD_ROOT:-/var/tmp/ModSecurity-conector-verified/build}}/no-crs-evidence}
NO_CRS_RUN_ID=${NO_CRS_RUN_ID:-}
CONNECTORS=${NO_CRS_CONNECTORS:-"apache nginx haproxy envoy traefik lighttpd"}

[ -n "$NO_CRS_RUN_ID" ] || {
    echo "FAIL: NO_CRS_RUN_ID is required for a canonical all-connector full-lifecycle run" >&2
    exit 2
}
case "$NO_CRS_RUN_ID" in
    [A-Za-z0-9]* ) ;;
    *) echo "FAIL: unsafe NO_CRS_RUN_ID: $NO_CRS_RUN_ID" >&2; exit 2 ;;
esac
case "$NO_CRS_RUN_ID" in
    *[!A-Za-z0-9._-]*) echo "FAIL: unsafe NO_CRS_RUN_ID: $NO_CRS_RUN_ID" >&2; exit 2 ;;
esac
[ "${#NO_CRS_RUN_ID}" -le 128 ] || {
    echo "FAIL: NO_CRS_RUN_ID is too long" >&2
    exit 2
}

summary_root=$EVIDENCE_ROOT/summary/$NO_CRS_RUN_ID
mkdir -p "$summary_root"
summary_file=$summary_root/full-lifecycle-run.jsonl
: > "$summary_file"

failed=0
blocked=0
for connector in $CONNECTORS; do
    rc=0
    NO_CRS_RUN_ID="$NO_CRS_RUN_ID" \
    NO_CRS_ARTIFACT_PROFILE=full_lifecycle \
    EVIDENCE_ROOT="$EVIDENCE_ROOT" \
    sh "$CONNECTOR_ROOT/ci/run-no-crs-baseline.sh" "$connector" no_crs_baseline || rc=$?
    "$PYTHON" - "$summary_file" "$connector" "$rc" "$EVIDENCE_ROOT/$connector/$NO_CRS_RUN_ID/result.json" <<'PY'
import json
import sys
from pathlib import Path

output, connector, rc, result_path = sys.argv[1:]
record = {"connector": connector, "runner_exit_code": int(rc), "result_path": result_path}
try:
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
except (OSError, ValueError):
    result = {}
record["status"] = result.get("status", "MISSING")
record["artifact_profile"] = result.get("artifact_profile", "")
Path(output).open("a", encoding="utf-8").write(json.dumps(record, sort_keys=True) + "\n")
PY
    if [ "$rc" -eq 77 ]; then
        blocked=1
    elif [ "$rc" -ne 0 ]; then
        failed=1
    fi
done

set +e
"$PYTHON" "$FRAMEWORK_ROOT/ci/no_crs_baseline.py" summarize \
    --evidence-root "$EVIDENCE_ROOT" \
    --run-id "$NO_CRS_RUN_ID" \
    --output-json "$summary_root/all-connectors-no-crs-summary.json" \
    --output-md "$summary_root/all-connectors-no-crs-summary.md" \
    --output-md-de "$summary_root/all-connectors-no-crs-summary.de.md"
summary_rc=$?
set -e
if [ "$summary_rc" -ne 0 ]; then
    failed=1
fi
if [ "$failed" -ne 0 ]; then
    exit 1
fi
if [ "$blocked" -ne 0 ]; then
    exit 77
fi
