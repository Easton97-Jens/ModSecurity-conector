#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
EXT_PROC_ROOT="$CONNECTOR_DIR/ext_proc"

command -v go >/dev/null 2>&1 || {
    echo "envoy_ext_proc_test: missing Go toolchain" >&2
    exit 77
}
[ -f "$EXT_PROC_ROOT/go.mod" ] || {
    echo "envoy_ext_proc_test: missing pinned Go module: $EXT_PROC_ROOT/go.mod" >&2
    exit 77
}

(
    cd "$EXT_PROC_ROOT"
    GOWORK=off go test -mod=readonly ./...
)
