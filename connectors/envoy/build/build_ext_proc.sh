#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
EXT_PROC_ROOT="$CONNECTOR_DIR/ext_proc"
VERSION_LOCK="$CONNECTOR_DIR/config/envoy-ext-proc-versions.env"
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
OUT_DIR="$BUILD_ROOT/envoy-ext-proc"
OUT_BIN="$OUT_DIR/msconnector_envoy_ext_proc"

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "envoy_ext_proc: BUILD_ROOT must be absolute: $BUILD_ROOT" >&2; exit 77 ;;
esac

case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_ext_proc: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT" >&2
        exit 77
        ;;
esac

[ -f "$EXT_PROC_ROOT/go.mod" ] || {
    echo "envoy_ext_proc: missing pinned Go module: $EXT_PROC_ROOT/go.mod" >&2
    exit 77
}
[ -f "$EXT_PROC_ROOT/go.sum" ] || {
    echo "envoy_ext_proc: missing Go dependency checksums: $EXT_PROC_ROOT/go.sum" >&2
    exit 77
}
[ -f "$VERSION_LOCK" ] || {
    echo "envoy_ext_proc: missing Envoy version lock: $VERSION_LOCK" >&2
    exit 77
}
command -v go >/dev/null 2>&1 || {
    echo "envoy_ext_proc: missing Go toolchain" >&2
    exit 77
}

pinned_envoy_version=$(sed -n 's/^ENVOY_RELEASE=//p' "$VERSION_LOCK")
pinned_proto_module=$(sed -n 's/^ENVOY_GO_PROTO_MODULE=//p' "$VERSION_LOCK")
pinned_proto_version=$(sed -n 's/^ENVOY_GO_PROTO_VERSION=//p' "$VERSION_LOCK")
[ -n "$pinned_envoy_version" ] || {
    echo "envoy_ext_proc: Envoy version lock has no ENVOY_RELEASE" >&2
    exit 77
}
[ -n "$pinned_proto_module" ] && [ -n "$pinned_proto_version" ] || {
    echo "envoy_ext_proc: Envoy version lock has no official Go proto module/version" >&2
    exit 77
}
awk -v module="$pinned_proto_module" -v version="$pinned_proto_version" \
    '$1 == module && $2 == version { found = 1 } END { exit(found ? 0 : 1) }' \
    "$EXT_PROC_ROOT/go.mod" || {
    echo "envoy_ext_proc: go.mod does not match pinned $pinned_proto_module $pinned_proto_version" >&2
    exit 2
}
if [ -n "${ENVOY_EXT_PROC_VERSION:-}" ] && [ "$ENVOY_EXT_PROC_VERSION" != "$pinned_envoy_version" ]; then
    echo "envoy_ext_proc: ENVOY_EXT_PROC_VERSION must match pinned $pinned_envoy_version (got $ENVOY_EXT_PROC_VERSION)" >&2
    exit 2
fi

mkdir -p "$OUT_DIR"
(
    cd "$EXT_PROC_ROOT"
    # -mod=readonly prevents accidental module graph edits during a build.
    GOWORK=off go mod verify
    GOWORK=off go build -mod=readonly -trimpath -buildvcs=false \
        -o "$OUT_BIN" ./cmd/msconnector-envoy-ext-proc
)

printf 'envoy_ext_proc: build-pass output=%s envoy_release=%s\n' \
    "$OUT_BIN" "$pinned_envoy_version"
