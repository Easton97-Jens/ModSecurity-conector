#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
MODULE_DIR=$(CDPATH= cd "$SCRIPT_DIR/../response_observer" && pwd)
GO_BIN=${GO:-go}
MODE=${1:-test}
case "$MODE" in test|build) ;; *) echo "usage: $0 [test|build]" >&2; exit 2 ;; esac
command -v "$GO_BIN" >/dev/null 2>&1 || { echo "BLOCKED: missing Go toolchain: $GO_BIN" >&2; exit 77; }
(
    cd "$MODULE_DIR"
    "$GO_BIN" test ./...
    "$GO_BIN" vet ./...
    if [ "$MODE" = build ]; then "$GO_BIN" build ./...; fi
)
printf 'traefik_response_observer_%s=pass\n' "$MODE"
printf 'module=%s\n' "$MODULE_DIR"
printf 'host_runtime_verified=false\n'
