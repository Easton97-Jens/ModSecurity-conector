#!/bin/sh
# Compile the complete existing Common helper scope without running a test corpus.
set -eu
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
BUILD_ROOT=${BUILD_ROOT:-${RUNNER_TEMP:-${TMPDIR:-/var/tmp}}/ModSecurity-conector-verified/build}
case "$BUILD_ROOT" in /*) ;; *) echo "FAIL: BUILD_ROOT must be absolute" >&2; exit 2 ;; esac
resolved=$(realpath -m -- "$BUILD_ROOT")
case "$resolved" in "$REPO_ROOT"|"$REPO_ROOT"/*) echo "FAIL: CodeQL output belongs outside the checkout" >&2; exit 2 ;; esac
out="$resolved/codeql-common"
mkdir -p "$out"
for source in "$REPO_ROOT"/common/src/*.c; do
    object="$out/$(basename "$source" .c).o"
    "${CC:-cc}" -std=c17 -Wall -Wextra -Werror -pthread \
        -I "$REPO_ROOT/common/include" -c "$source" -o "$object"
done
printf 'CodeQL Common C17 compilation completed: %s
' "$out"
