#!/bin/sh
# Run exactly one admitted HTTP request deadline through the actual service.
set -eu
[ "$#" -eq 1 ] || { echo 'active authorization timeout requires one case' >&2; exit 2; }
case "$1" in
    incomplete-headers|incomplete-body) ;;
    *) echo 'unknown active authorization timeout case' >&2; exit 2 ;;
esac
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd -P)
OUTPUT_ROOT=${RUNNER_TEMP:-${TMP_ROOT:-}}
: "${OUTPUT_ROOT:?an explicit external RUNNER_TEMP or TMP_ROOT is required}"
"${PYTHON:-python3}" - "$ROOT" "$OUTPUT_ROOT" <<'ADMITROOT'
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
from ci.lib.active_coverage import external_root
external_root(Path(sys.argv[2]))
ADMITROOT
umask 077
case_root=$(mktemp -d "$OUTPUT_ROOT/active-authorization-timeout.XXXXXXXX")
trap 'rm -rf -- "$case_root"' EXIT HUP INT TERM
"${CC:-cc}" -std=c17 -Wall -Wextra -Werror -pthread \
    -I "$ROOT" -I "$ROOT/common/include" -I "$ROOT/common/runtime" \
    "$ROOT/ci/checks/common/http_authorization_service_timeout_smoke.c" \
    "$ROOT/common/runtime/http_authorization_service.c" \
    "$ROOT"/common/src/*.c -o "$case_root/authorization-timeout"
"$case_root/authorization-timeout" --active-case "$1"
