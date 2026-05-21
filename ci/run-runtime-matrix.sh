#!/bin/sh
set -u

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
. "$SCRIPT_DIR/common.sh"

PYTHON_BIN="${PYTHON:-$(ci_python)}"
FORCE_ALL_CASES="${FORCE_ALL_CASES:-0}"
SNAPSHOT_ARGS=""
if [ "$FORCE_ALL_CASES" = "1" ]; then
    SNAPSHOT_ARGS="--force-all"
    echo "runtime-matrix: FORCE_ALL_CASES=1; xfail/pending/future/gap YAML cases will be attempted where applicable"
fi

echo "runtime-matrix: running Apache smoke with REFRESH=1"
set +e
REFRESH=1 make -C "$REPO_ROOT" smoke-apache
apache_rc=$?
set -e
echo "runtime-matrix: Apache smoke exit=$apache_rc"

echo "runtime-matrix: running NGINX smoke with REFRESH=1"
set +e
REFRESH=1 make -C "$REPO_ROOT" smoke-nginx
nginx_rc=$?
set -e
echo "runtime-matrix: NGINX smoke exit=$nginx_rc"

"$PYTHON_BIN" "$REPO_ROOT/ci/update-runtime-snapshot.py" \
    --build-root "$BUILD_ROOT" \
    --apache-exit-code "$apache_rc" \
    --nginx-exit-code "$nginx_rc" \
    $SNAPSHOT_ARGS
"$PYTHON_BIN" "$REPO_ROOT/ci/generate-case-matrix.py"

if [ "$FORCE_ALL_CASES" = "1" ]; then
    if "$PYTHON_BIN" - "$BUILD_ROOT/results/apache-summary.json" "$BUILD_ROOT/results/nginx-summary.json" <<'PY'
import json
import sys
from pathlib import Path

for path_arg, connector in [(sys.argv[1], "apache"), (sys.argv[2], "nginx")]:
    path = Path(path_arg)
    if not path.exists():
        raise SystemExit(f"missing summary: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get(connector, {}).get("cases", {})
    if not isinstance(cases, dict) or not cases:
        raise SystemExit(f"missing per-case runtime evidence in {path}")
PY
    then
        echo "runtime-matrix: force-all completed; observed case failures are recorded as runtime evidence, not command failure"
        exit 0
    fi
    echo "runtime-matrix: force-all did not produce complete per-connector summaries"
    exit 1
fi

if [ "$apache_rc" -ne 0 ] || [ "$nginx_rc" -ne 0 ]; then
    echo "runtime-matrix: one or more runtime smokes failed or blocked; generated docs were still refreshed from available evidence"
    exit 1
fi

echo "runtime-matrix: Apache and NGINX runtime matrix completed"
