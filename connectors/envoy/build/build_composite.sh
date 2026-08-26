#!/bin/sh
set -eu

# Build the composite Envoy/Traefik service against the exact Common Runtime
# archive and libmodsecurity bridge used by the existing ext_proc service.
# BUILD_ROOT is deliberately mandatory: generated objects and the executable
# must remain outside the checkout.

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
EXT_PROC_ROOT="$CONNECTOR_DIR/ext_proc"
COMMON_BUILD="$SCRIPT_DIR/build_ext_proc.sh"

: "${BUILD_ROOT:?envoy_composite: BUILD_ROOT must be an explicit absolute directory}"
case "$BUILD_ROOT" in
    /*) ;;
    *) echo "envoy_composite: BUILD_ROOT must be absolute: $BUILD_ROOT" >&2; exit 77 ;;
esac
case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_composite: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT" >&2
        exit 77
        ;;
    *) ;;
esac

[ -x "$COMMON_BUILD" ] || {
    echo "envoy_composite: missing Common bridge build script: $COMMON_BUILD" >&2
    exit 77
}
[ -f "$EXT_PROC_ROOT/go.mod" ] || {
    echo "envoy_composite: missing pinned Go module: $EXT_PROC_ROOT/go.mod" >&2
    exit 77
}
command -v go >/dev/null 2>&1 || {
    echo "envoy_composite: missing Go toolchain" >&2
    exit 77
}

# The existing builder performs the header/library checks and builds the exact
# Common archive.  Its standalone executable is an incidental build artifact;
# this command consumes only its archive, never its request-only runtime path.
BUILD_ROOT="$BUILD_ROOT" \
MODSECURITY_INCLUDE_DIR="${MODSECURITY_INCLUDE_DIR:-}" \
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-}" \
MODSECURITY_LIB_FILE="${MODSECURITY_LIB_FILE:-}" \
MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-}" \
CC="${CC:-cc}" CFLAGS="${CFLAGS:-}" AR="${AR:-ar}" \
sh "$COMMON_BUILD"

COMMON_ARCHIVE="$BUILD_ROOT/envoy-ext-proc/libmsconnector_envoy_ext_proc_common.a"
[ -f "$COMMON_ARCHIVE" ] || {
    echo "envoy_composite: Common bridge archive was not produced" >&2
    exit 1
}

modsecurity_include=${MODSECURITY_INCLUDE_DIR:-}
if [ -z "$modsecurity_include" ] && [ -n "${MODSECURITY_PREFIX:-}" ]; then
    modsecurity_include="$MODSECURITY_PREFIX/include"
fi
[ -f "$modsecurity_include/modsecurity/modsecurity.h" ] || {
    echo "envoy_composite: missing modsecurity/modsecurity.h" >&2
    exit 77
}

modsecurity_file=${MODSECURITY_LIB_FILE:-}
if [ -n "$modsecurity_file" ]; then
    [ -f "$modsecurity_file" ] || {
        echo "envoy_composite: MODSECURITY_LIB_FILE is not a file" >&2
        exit 77
    }
    runtime_lib_dir=$(CDPATH= cd "$(dirname "$modsecurity_file")" && pwd)
    link_input="$modsecurity_file"
else
    modsecurity_dir=${MODSECURITY_LIB_DIR:-}
    if [ -z "$modsecurity_dir" ] && [ -n "${MODSECURITY_PREFIX:-}" ]; then
        modsecurity_dir="$MODSECURITY_PREFIX/lib"
    fi
    [ -f "$modsecurity_dir/libmodsecurity.so" ] || {
        echo "envoy_composite: missing libmodsecurity.so" >&2
        exit 77
    }
    runtime_lib_dir=$(CDPATH= cd "$modsecurity_dir" && pwd)
    link_input="-L$runtime_lib_dir -lmodsecurity"
fi

output_dir="$BUILD_ROOT/envoy-composite"
output_bin="$output_dir/msconnector_composite"
mkdir -p "$output_dir"
cgo_cflags="-D_DEFAULT_SOURCE -std=c17 -I$REPO_ROOT -I$REPO_ROOT/common/include -I$REPO_ROOT/common/runtime -I$modsecurity_include"
cgo_ldflags="$COMMON_ARCHIVE $link_input -Wl,-rpath,$runtime_lib_dir -lstdc++ -pthread"
(
    cd "$EXT_PROC_ROOT"
    GOWORK=off go mod verify
    CGO_ENABLED=1 CGO_CFLAGS="$cgo_cflags" CGO_LDFLAGS="$cgo_ldflags" \
        GOWORK=off go build -mod=readonly -tags libmodsecurity -trimpath -buildvcs=false \
        -o "$output_bin" ./cmd/msconnector-composite
)

printf 'envoy_composite: build-pass output=%s bridge=common_libmodsecurity\n' "$output_bin"
