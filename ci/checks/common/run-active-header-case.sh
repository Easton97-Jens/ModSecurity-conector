#!/bin/sh
set -eu
case "${1:-}" in
    valid-length|duplicate-length|overflow-length) ;;
    *) echo 'active header case: unknown case' >&2; exit 2 ;;
esac
root=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd -P)
output_root=${RUNNER_TEMP:-${TMP_ROOT:-${BUILD_ROOT:-}}}
: "${output_root:?active header case requires an existing external RUNNER_TEMP, TMP_ROOT or BUILD_ROOT}"
"${PYTHON:-python3}" - "$root" "$output_root" <<'ADMITROOT'
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
from ci.lib.active_coverage import external_root
external_root(Path(sys.argv[2]))
ADMITROOT
umask 077
directory=$(mktemp -d "$output_root/active-header.XXXXXXXX")
trap 'rm -rf -- "$directory"' EXIT HUP INT TERM
"${CC:-cc}" -std=c17 -Wall -Wextra -Werror -I"$root/common/include" \
    "$root/tests/active_header_case.c" "$root/common/src/headers.c" -o "$directory/header-case"
"$directory/header-case" "$1"
