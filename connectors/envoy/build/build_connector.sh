#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
CC_BIN=${CC:-cc}
OUT_DIR="$BUILD_ROOT/envoy-connector"
OBJ_DIR="$OUT_DIR/obj"
SERVICE_BIN="$OUT_DIR/msconnector_envoy_ext_authz"

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "envoy_connector: BUILD_ROOT must be absolute: $BUILD_ROOT" >&2; exit 77 ;;
esac

case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_connector: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT" >&2
        exit 77
        ;;
esac

command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "envoy_connector: missing C compiler: $CC_BIN" >&2
    exit 77
}

MODSECURITY_INCLUDE_DIR=${MODSECURITY_INCLUDE_DIR:-${MODSECURITY_PREFIX:+$MODSECURITY_PREFIX/include}}
MODSECURITY_LIB_DIR=${MODSECURITY_LIB_DIR:-${MODSECURITY_PREFIX:+$MODSECURITY_PREFIX/lib}}
MODSECURITY_LIB_FILE=${MODSECURITY_LIB_FILE:-}

[ -n "$MODSECURITY_INCLUDE_DIR" ] || {
    echo "envoy_connector: MODSECURITY_INCLUDE_DIR or MODSECURITY_PREFIX is required" >&2
    exit 77
}
[ -f "$MODSECURITY_INCLUDE_DIR/modsecurity/modsecurity.h" ] || {
    echo "envoy_connector: missing modsecurity/modsecurity.h under $MODSECURITY_INCLUDE_DIR" >&2
    exit 77
}

if [ -n "$MODSECURITY_LIB_FILE" ]; then
    [ -f "$MODSECURITY_LIB_FILE" ] || {
        echo "envoy_connector: MODSECURITY_LIB_FILE is not a file: $MODSECURITY_LIB_FILE" >&2
        exit 77
    }
    MODSECURITY_RUNTIME_LIB_DIR=$(CDPATH= cd "$(dirname "$MODSECURITY_LIB_FILE")" && pwd)
else
    [ -n "$MODSECURITY_LIB_DIR" ] || {
        echo "envoy_connector: MODSECURITY_LIB_DIR, MODSECURITY_LIB_FILE, or MODSECURITY_PREFIX is required" >&2
        exit 77
    }
    [ -d "$MODSECURITY_LIB_DIR" ] || {
        echo "envoy_connector: MODSECURITY_LIB_DIR is not a directory: $MODSECURITY_LIB_DIR" >&2
        exit 77
    }
    MODSECURITY_RUNTIME_LIB_DIR=$(CDPATH= cd "$MODSECURITY_LIB_DIR" && pwd)
fi

for header in \
    "$REPO_ROOT/common/runtime/msconnector_runtime.h" \
    "$REPO_ROOT/common/runtime/http_authorization_service.h"
do
    [ -f "$header" ] || {
        echo "envoy_connector: missing shared runtime header: $header" >&2
        exit 77
    }
done

set -- "$REPO_ROOT"/common/runtime/*.c
[ -f "$1" ] || {
    echo "envoy_connector: no shared runtime C sources found under $REPO_ROOT/common/runtime" >&2
    exit 77
}

rm -rf "$OBJ_DIR"
mkdir -p "$OBJ_DIR"

objects=
compile_source() {
    source=$1
    relative=${source#"$REPO_ROOT"/}
    object_name=$(printf '%s' "$relative" | tr '/.' '__')
    object="$OBJ_DIR/$object_name.o"
    # CFLAGS is additive; required language and warning flags are applied last.
    # shellcheck disable=SC2086
    "$CC_BIN" ${CFLAGS:-} -std=c17 -Wall -Wextra -Werror \
        -I "$REPO_ROOT" \
        -I "$REPO_ROOT/common/include" \
        -I "$MODSECURITY_INCLUDE_DIR" \
        -I "$CONNECTOR_DIR/src" \
        -c "$source" -o "$object"
    objects="$objects $object"
}

for source in \
    "$REPO_ROOT"/common/src/*.c \
    "$REPO_ROOT"/common/runtime/*.c \
    "$CONNECTOR_DIR/metadata.c" \
    "$CONNECTOR_DIR/src/envoy_modsecurity_mapper.c" \
    "$CONNECTOR_DIR/src/envoy_ext_authz_service_main.c"
do
    compile_source "$source"
done

if [ -n "$MODSECURITY_LIB_FILE" ]; then
    # shellcheck disable=SC2086
    "$CC_BIN" ${LDFLAGS:-} $objects "$MODSECURITY_LIB_FILE" \
        "-Wl,-rpath,$MODSECURITY_RUNTIME_LIB_DIR" ${LDLIBS:-} -o "$SERVICE_BIN"
else
    # shellcheck disable=SC2086
    "$CC_BIN" ${LDFLAGS:-} $objects -L "$MODSECURITY_RUNTIME_LIB_DIR" \
        -lmodsecurity "-Wl,-rpath,$MODSECURITY_RUNTIME_LIB_DIR" ${LDLIBS:-} \
        -o "$SERVICE_BIN"
fi

printf 'envoy_connector: build-pass output=%s\n' "$SERVICE_BIN"
