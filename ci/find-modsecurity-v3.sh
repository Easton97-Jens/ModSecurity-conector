#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)

# Priority order:
# 1) explicit MODSECURITY_V3_SOURCE_DIR when valid
# 2) repo-local sibling candidates
# 3) historical default path

if [ "${MODSECURITY_V3_SOURCE_DIR:-}" ] && [ -d "$MODSECURITY_V3_SOURCE_DIR" ]; then
    printf '%s\n' "$MODSECURITY_V3_SOURCE_DIR"
    exit 0
fi

BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"

for candidate in \
    "$REPO_ROOT/../ModSecurity_V3" \
    "$REPO_ROOT/../../ModSecurity_V3" \
    "$REPO_ROOT/.deps/ModSecurity_V3" \
    "$BUILD_ROOT/sources/ModSecurity_V3" \
    "/root/conecter/ModSecurity_V3"
do
    if [ -d "$candidate" ]; then
        printf '%s\n' "$candidate"
        exit 0
    fi
done

exit 1
