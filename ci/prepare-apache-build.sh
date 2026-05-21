#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$(CDPATH= cd "$CONNECTOR_ROOT/../ModSecurity-test-Framework" 2>/dev/null && pwd || printf '')}"
[ -n "$FRAMEWORK_ROOT" ] || { echo "prepare-apache-build: blocked FRAMEWORK_ROOT is not set and ../ModSecurity-test-Framework is missing"; exit 77; }

exec env FRAMEWORK_ROOT="$FRAMEWORK_ROOT" CONNECTOR_ROOT="$CONNECTOR_ROOT" sh "$FRAMEWORK_ROOT/ci/prepare-apache-build.sh" "$@"
