#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
MODULE_DIR="$REPO_ROOT/connectors/traefik/native_middleware"
BUILD_ROOT="${BUILD_ROOT:-${TMPDIR:-/var/tmp}/ModSecurity-conector-verified/build}"
OUT_DIR="${TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR:-$BUILD_ROOT/traefik-native-middleware}"
REPORT="$OUT_DIR/build.txt"
GO_BIN="${GO:-go}"
MODE="${1:-build}"

case "$OUT_DIR" in
    /*) ;;
    *) echo "BLOCKED: TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR must be absolute: $OUT_DIR" >&2; exit 77 ;;
esac
if [ -L "$OUT_DIR" ]; then
    echo "BLOCKED: Traefik native middleware output must not be a symlink: $OUT_DIR" >&2
    exit 77
fi
case "$OUT_DIR" in
    /|/tmp|/var/tmp)
        echo "BLOCKED: Traefik native middleware output is too broad: $OUT_DIR" >&2
        exit 77
        ;;
esac
case "$OUT_DIR" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "BLOCKED: Traefik native middleware output must be outside the checkout: $OUT_DIR" >&2
        exit 77
        ;;
esac

case "$MODE" in
    build|test) ;;
    clean)
        rm -rf "$OUT_DIR"
        printf 'traefik_native_middleware_clean=pass\n'
        printf 'output=%s\n' "$OUT_DIR"
        exit 0
        ;;
    *)
        echo "usage: $0 [build|test|clean]" >&2
        exit 2
        ;;
esac

if [ ! -f "$MODULE_DIR/go.mod" ]; then
    echo "BLOCKED: missing Traefik native middleware Go module: $MODULE_DIR/go.mod" >&2
    exit 77
fi
command -v "$GO_BIN" >/dev/null 2>&1 || {
    echo "BLOCKED: missing Go toolchain: $GO_BIN" >&2
    exit 77
}

mkdir -p "$OUT_DIR"
(
    cd "$MODULE_DIR"
    "$GO_BIN" test ./...
    "$GO_BIN" vet ./...
    if [ "$MODE" = "build" ]; then
        "$GO_BIN" build ./...
    fi
)

{
    printf 'traefik_native_middleware_%s=pass\n' "$MODE"
    printf 'module=%s\n' "$MODULE_DIR"
    printf 'engine_mode=passthrough\n'
    printf 'artifact=go_package_compile_only\n'
    printf 'runtime_verified=false\n'
} > "$REPORT"

printf 'traefik_native_middleware_%s=pass\n' "$MODE"
printf 'report=%s\n' "$REPORT"
