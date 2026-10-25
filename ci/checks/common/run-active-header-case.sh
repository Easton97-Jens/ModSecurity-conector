#!/bin/sh
set -eu
case "${1:-}" in
    valid-length|duplicate-length|overflow-length) ;;
    *) echo 'active header case: unknown case' >&2; exit 2 ;;
esac
root=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
: "${BUILD_ROOT:?active header case requires an external BUILD_ROOT}"
case "$BUILD_ROOT" in
    /*) ;;
    *) echo 'active header case: BUILD_ROOT must be absolute' >&2; exit 2 ;;
esac
case "$BUILD_ROOT/" in
    "$root/"*) echo 'active header case: BUILD_ROOT must be external' >&2; exit 2 ;;
esac
directory=$(mktemp -d "$BUILD_ROOT/active-header.XXXXXXXX")
trap 'rm -rf -- "$directory"' EXIT HUP INT TERM
"${CC:-cc}" -std=c17 -Wall -Wextra -Werror -I"$root/common/include" \
    "$root/tests/active_header_case.c" "$root/common/src/headers.c" -o "$directory/header-case"
"$directory/header-case" "$1"
