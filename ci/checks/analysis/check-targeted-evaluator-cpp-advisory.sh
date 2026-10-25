#!/bin/sh
# Compile the real evaluator against real ModSecurity headers. The caller owns
# advisory/nonblocking policy; compiler failures remain failures here.
set -eu

SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
ROOT=$(CDPATH='' cd -- "$ROOT" && pwd -P)
CXX_BIN=${CXX:-c++}

block() {
    echo "BLOCKED: $*" >&2
    exit 77
}

case "${CPP_STANDARD:-}" in
    c++20|c++23) ;;
    *) echo 'FAIL: CPP_STANDARD must be c++20 or c++23' >&2; exit 2 ;;
esac

[ -n "${CPP_BUILD_ROOT:-}" ] || {
    echo 'FAIL: CPP_BUILD_ROOT is required' >&2
    exit 2
}
case "$CPP_BUILD_ROOT" in
    /*) ;;
    *) echo 'FAIL: CPP_BUILD_ROOT must be absolute' >&2; exit 2 ;;
esac
command -v realpath >/dev/null 2>&1 || block 'missing realpath utility'
CPP_BUILD_ROOT=$(realpath -m -- "$CPP_BUILD_ROOT") || block 'cannot resolve CPP_BUILD_ROOT'
case "$CPP_BUILD_ROOT" in
    "$ROOT"|"$ROOT"/*)
        echo 'FAIL: CPP_BUILD_ROOT must be outside the checkout' >&2
        exit 2
        ;;
esac

command -v "$CXX_BIN" >/dev/null 2>&1 || block "missing C++ compiler: $CXX_BIN"
case "${MODSECURITY_INCLUDE_DIR:-}" in
    /*) ;;
    *) block 'MODSECURITY_INCLUDE_DIR must be an absolute directory' ;;
esac
[ -d "$MODSECURITY_INCLUDE_DIR" ] || block 'MODSECURITY_INCLUDE_DIR is not a directory'
MODSECURITY_INCLUDE_DIR=$(CDPATH='' cd -- "$MODSECURITY_INCLUDE_DIR" && pwd -P)
for header in modsecurity/modsecurity.h modsecurity/rules_set.h modsecurity/transaction.h; do
    [ -f "$MODSECURITY_INCLUDE_DIR/$header" ] || block "missing libmodsecurity header: $header"
done

SOURCE=$ROOT/common/scripts/modsecurity_targeted_eval.cc
[ -f "$SOURCE" ] || {
    echo "FAIL: missing tracked evaluator source: $SOURCE" >&2
    exit 1
}
mkdir -p "$CPP_BUILD_ROOT" || block 'cannot create CPP_BUILD_ROOT'
OUTPUT=$CPP_BUILD_ROOT/modsecurity_targeted_eval.$CPP_STANDARD.o
TEMP_OUTPUT=$(mktemp "$CPP_BUILD_ROOT/.modsecurity_targeted_eval.$CPP_STANDARD.XXXXXX") || \
    block 'cannot create evaluator temporary output'
trap 'rm -f "$TEMP_OUTPUT"' EXIT HUP INT TERM

"$CXX_BIN" "-std=$CPP_STANDARD" -Wall -Wextra -Werror \
    -isystem "$MODSECURITY_INCLUDE_DIR" \
    -c "$SOURCE" -o "$TEMP_OUTPUT"
mv -f "$TEMP_OUTPUT" "$OUTPUT"
trap - EXIT HUP INT TERM

printf 'PASS (advisory): targeted evaluator compiled in %s mode at %s (compile only; not linked or executed)\n' \
    "$CPP_STANDARD" "$OUTPUT"
