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
OBJECT_DIR="$OUT_DIR/common-runtime-objects"
COMMON_ARCHIVE="$OUT_DIR/libmsconnector_envoy_ext_proc_common.a"
CC_BIN=${CC:-cc}
AR_BIN=${AR:-ar}

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
command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "envoy_ext_proc: missing C compiler: $CC_BIN" >&2
    exit 77
}
command -v "$AR_BIN" >/dev/null 2>&1 || {
    echo "envoy_ext_proc: missing archive tool: $AR_BIN" >&2
    exit 77
}

MODSECURITY_INCLUDE_DIR=${MODSECURITY_INCLUDE_DIR:-${MODSECURITY_PREFIX:+$MODSECURITY_PREFIX/include}}
MODSECURITY_LIB_DIR=${MODSECURITY_LIB_DIR:-${MODSECURITY_PREFIX:+$MODSECURITY_PREFIX/lib}}
MODSECURITY_LIB_FILE=${MODSECURITY_LIB_FILE:-}

[ -n "$MODSECURITY_INCLUDE_DIR" ] || {
    echo "envoy_ext_proc: MODSECURITY_INCLUDE_DIR or MODSECURITY_PREFIX is required for the Common/libmodsecurity bridge" >&2
    exit 77
}
[ -f "$MODSECURITY_INCLUDE_DIR/modsecurity/modsecurity.h" ] || {
    echo "envoy_ext_proc: missing modsecurity/modsecurity.h under $MODSECURITY_INCLUDE_DIR" >&2
    exit 77
}
for required_header in modsecurity/rules_set.h modsecurity/transaction.h; do
    [ -f "$MODSECURITY_INCLUDE_DIR/$required_header" ] || {
        echo "envoy_ext_proc: missing libmodsecurity header: $MODSECURITY_INCLUDE_DIR/$required_header" >&2
        exit 77
    }
done
if [ -n "$MODSECURITY_LIB_FILE" ]; then
    [ -f "$MODSECURITY_LIB_FILE" ] || {
        echo "envoy_ext_proc: MODSECURITY_LIB_FILE is not a file: $MODSECURITY_LIB_FILE" >&2
        exit 77
    }
    MODSECURITY_RUNTIME_LIB_DIR=$(CDPATH= cd "$(dirname "$MODSECURITY_LIB_FILE")" && pwd)
    MODSECURITY_LINK_INPUT=$MODSECURITY_LIB_FILE
else
    [ -n "$MODSECURITY_LIB_DIR" ] || {
        echo "envoy_ext_proc: MODSECURITY_LIB_DIR, MODSECURITY_LIB_FILE, or MODSECURITY_PREFIX is required" >&2
        exit 77
    }
    [ -d "$MODSECURITY_LIB_DIR" ] || {
        echo "envoy_ext_proc: MODSECURITY_LIB_DIR is not a directory: $MODSECURITY_LIB_DIR" >&2
        exit 77
    }
    [ -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] || {
        echo "envoy_ext_proc: missing libmodsecurity.so under $MODSECURITY_LIB_DIR" >&2
        exit 77
    }
    MODSECURITY_RUNTIME_LIB_DIR=$(CDPATH= cd "$MODSECURITY_LIB_DIR" && pwd)
    MODSECURITY_LINK_INPUT="-L$MODSECURITY_RUNTIME_LIB_DIR -lmodsecurity"
fi

for required_source in \
    "$REPO_ROOT/common/runtime/msconnector_runtime.c" \
    "$EXT_PROC_ROOT/internal/processor/common_runtime_bridge.c" \
    "$EXT_PROC_ROOT/internal/processor/common_runtime_bridge.h"
do
    [ -f "$required_source" ] || {
        echo "envoy_ext_proc: missing Common bridge source: $required_source" >&2
        exit 77
    }
done

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
rm -rf "$OBJECT_DIR" "$COMMON_ARCHIVE"
mkdir -p "$OBJECT_DIR"

objects=
compile_common_source() {
    source=$1
    relative=${source#"$REPO_ROOT"/}
    object_name=$(printf '%s' "$relative" | tr '/.' '__')
    object="$OBJECT_DIR/$object_name.o"
    # CFLAGS is additive; the warning and language policy remains fixed for
    # this bridge. The Common archive is linked only into the ext_proc binary.
    # shellcheck disable=SC2086
    "$CC_BIN" ${CFLAGS:-} -std=c17 -Wall -Wextra -Werror -fPIC \
        -I "$REPO_ROOT" \
        -I "$REPO_ROOT/common/include" \
        -I "$REPO_ROOT/common/runtime" \
        -I "$MODSECURITY_INCLUDE_DIR" \
        -c "$source" -o "$object"
    objects="$objects $object"
}

for source in "$REPO_ROOT"/common/src/*.c "$REPO_ROOT"/common/runtime/*.c; do
    [ -f "$source" ] || continue
    compile_common_source "$source"
done
# shellcheck disable=SC2086
"$AR_BIN" rcs "$COMMON_ARCHIVE" $objects

# _DEFAULT_SOURCE keeps Go's own cgo runtime declarations visible when the
# connector requests a strict C17 mode for its bridge source.
cgo_cflags="-D_DEFAULT_SOURCE -std=c17 -I$REPO_ROOT -I$REPO_ROOT/common/include -I$REPO_ROOT/common/runtime -I$MODSECURITY_INCLUDE_DIR"
cgo_ldflags="$COMMON_ARCHIVE $MODSECURITY_LINK_INPUT -Wl,-rpath,$MODSECURITY_RUNTIME_LIB_DIR -lstdc++ -pthread"
(
    cd "$EXT_PROC_ROOT"
    # -mod=readonly prevents accidental module graph edits during a build.
    GOWORK=off go mod verify
    CGO_ENABLED=1 CGO_CFLAGS="$cgo_cflags" CGO_LDFLAGS="$cgo_ldflags" \
        GOWORK=off go build -mod=readonly -tags libmodsecurity -trimpath -buildvcs=false \
        -o "$OUT_BIN" ./cmd/msconnector-envoy-ext-proc
    if [ "${ENVOY_EXT_PROC_COMMON_TEST:-0}" = "1" ]; then
        CGO_ENABLED=1 CGO_CFLAGS="$cgo_cflags" CGO_LDFLAGS="$cgo_ldflags" \
            GOWORK=off go test -mod=readonly -tags libmodsecurity -count=1 ./...
    fi
)

printf 'envoy_ext_proc: build-pass output=%s envoy_release=%s bridge=common_libmodsecurity\n' \
    "$OUT_BIN" "$pinned_envoy_version"
