#!/bin/sh
set -u

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
. "$SCRIPT_DIR/common.sh"

PYTHON_BIN="${PYTHON:-$(ci_python)}"

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
    --nginx-exit-code "$nginx_rc"
"$PYTHON_BIN" "$REPO_ROOT/ci/generate-case-matrix.py"

if [ "$apache_rc" -ne 0 ] || [ "$nginx_rc" -ne 0 ]; then
    echo "runtime-matrix: one or more runtime smokes failed or blocked; generated docs were still refreshed from available evidence"
    exit 1
fi

echo "runtime-matrix: Apache and NGINX runtime matrix completed"
