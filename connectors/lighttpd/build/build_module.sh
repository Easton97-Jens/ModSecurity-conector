#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH='' cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH='' cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
OUT_DIR=$BUILD_ROOT/lighttpd-connector
OBJ_DIR=$OUT_DIR/objects
MODULE_DIR=${LIGHTTPD_MODULE_DIR:-$OUT_DIR/modules}
CC_BIN=${CC:-cc}
MSCONNECTOR_C_STD=${MSCONNECTOR_C_STD:-c17}

blocked() {
    printf 'lighttpd_connector_build: BLOCKED: %s\n' "$1"
    exit 77
}

case "$BUILD_ROOT" in
    /*) ;;
    *) blocked "BUILD_ROOT must be absolute: $BUILD_ROOT" ;;
esac
case "$MODULE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_MODULE_DIR must be absolute: $MODULE_DIR" ;;
esac

case "$(CDPATH='' cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        blocked "BUILD_ROOT must not be inside the checkout: $BUILD_ROOT"
        ;;
    *) ;;
esac
case "$(CDPATH='' cd "$MODULE_DIR" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$MODULE_DIR")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        blocked "LIGHTTPD_MODULE_DIR must not be inside the checkout: $MODULE_DIR"
        ;;
    *) ;;
esac

[ -n "${LIGHTTPD_SOURCE_DIR:-}" ] || blocked "LIGHTTPD_SOURCE_DIR is required"
[ -n "${MODSECURITY_INCLUDE_DIR:-}" ] || blocked "MODSECURITY_INCLUDE_DIR is required"
[ -n "${MODSECURITY_LIB_DIR:-}" ] || blocked "MODSECURITY_LIB_DIR is required"
command -v "$CC_BIN" >/dev/null 2>&1 || blocked "missing C compiler: $CC_BIN"

case "$LIGHTTPD_SOURCE_DIR" in
    /*) ;;
    *) blocked "LIGHTTPD_SOURCE_DIR must be absolute: $LIGHTTPD_SOURCE_DIR" ;;
esac
case "$MODSECURITY_INCLUDE_DIR" in
    /*) ;;
    *) blocked "MODSECURITY_INCLUDE_DIR must be absolute: $MODSECURITY_INCLUDE_DIR" ;;
esac
case "$MODSECURITY_LIB_DIR" in
    /*) ;;
    *) blocked "MODSECURITY_LIB_DIR must be absolute: $MODSECURITY_LIB_DIR" ;;
esac

if [ -f "$LIGHTTPD_SOURCE_DIR/src/plugin.h" ]; then
    LIGHTTPD_HEADER_DIR=$LIGHTTPD_SOURCE_DIR/src
elif [ -f "$LIGHTTPD_SOURCE_DIR/plugin.h" ]; then
    LIGHTTPD_HEADER_DIR=$LIGHTTPD_SOURCE_DIR
else
    blocked "pinned lighttpd plugin.h not found below LIGHTTPD_SOURCE_DIR"
fi

[ -f "$LIGHTTPD_HEADER_DIR/request.h" ] || blocked "pinned lighttpd request.h is missing"
[ -f "$MODSECURITY_INCLUDE_DIR/modsecurity/modsecurity.h" ] || \
    blocked "modsecurity/modsecurity.h is missing below MODSECURITY_INCLUDE_DIR"
[ -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] || \
    blocked "libmodsecurity.so is missing below MODSECURITY_LIB_DIR"

LIGHTTPD_CONFIG_DIR_FOUND=
CONFIG_CANDIDATES="$LIGHTTPD_SOURCE_DIR
$LIGHTTPD_SOURCE_DIR/src"
if [ -n "${LIGHTTPD_BUILD_ROOT:-}" ]; then
    CONFIG_CANDIDATES="$LIGHTTPD_BUILD_ROOT
$LIGHTTPD_BUILD_ROOT/src
$CONFIG_CANDIDATES"
fi
if [ -n "${LIGHTTPD_BUILD_DIR:-}" ]; then
    CONFIG_CANDIDATES="$LIGHTTPD_BUILD_DIR
$LIGHTTPD_BUILD_DIR/src
$CONFIG_CANDIDATES"
fi
if [ -n "${LIGHTTPD_CONFIG_DIR:-}" ]; then
    CONFIG_CANDIDATES="$LIGHTTPD_CONFIG_DIR
$CONFIG_CANDIDATES"
fi
LIGHTTPD_CONFIG_DIR_FOUND=$(printf '%s\n' "$CONFIG_CANDIDATES" | while IFS= read -r candidate; do
    if [ -n "$candidate" ] && [ -f "$candidate/config.h" ]; then
        printf '%s\n' "$candidate"
        break
    fi
done)
[ -n "$LIGHTTPD_CONFIG_DIR_FOUND" ] || blocked \
    "generated lighttpd config.h is required; set LIGHTTPD_BUILD_ROOT, LIGHTTPD_BUILD_DIR or LIGHTTPD_CONFIG_DIR"

rm -rf "$OBJ_DIR"
mkdir -p "$OBJ_DIR" "$MODULE_DIR"

compile_common() {
    source_file=$1
    object_file=$2
    "$CC_BIN" \
        -std="$MSCONNECTOR_C_STD" \
        -fPIC \
        -Wall \
        -Wextra \
        -Werror \
        -I "$REPO_ROOT/common/include" \
        -I "$REPO_ROOT/common/runtime" \
        -I "$MODSECURITY_INCLUDE_DIR" \
        -c "$source_file" \
        -o "$object_file"
}

for source_file in "$REPO_ROOT"/common/src/*.c; do
    object_file=$OBJ_DIR/common_$(basename "$source_file" .c).o
    compile_common "$source_file" "$object_file"
done

RUNTIME_OBJECT=$OBJ_DIR/msconnector_runtime.o
compile_common "$REPO_ROOT/common/runtime/msconnector_runtime.c" "$RUNTIME_OBJECT"

"$CC_BIN" \
    -std="$MSCONNECTOR_C_STD" \
    -fPIC \
    -Wall \
    -Wextra \
    -Werror \
    -DHAVE_CONFIG_H \
    -DMSCONNECTOR_LIGHTTPD_HOST_API \
    -I "$LIGHTTPD_CONFIG_DIR_FOUND" \
    -I "$LIGHTTPD_HEADER_DIR" \
    -I "$REPO_ROOT" \
    -I "$REPO_ROOT/common/include" \
    -I "$REPO_ROOT/common/runtime" \
    -c "$CONNECTOR_DIR/src/lighttpd_modsecurity_mapper.c" \
    -o "$OBJ_DIR/lighttpd_modsecurity_mapper.o"

"$CC_BIN" \
    -std="$MSCONNECTOR_C_STD" \
    -fPIC \
    -Wall \
    -Wextra \
    -Werror \
    -DHAVE_CONFIG_H \
    -I "$LIGHTTPD_CONFIG_DIR_FOUND" \
    -I "$LIGHTTPD_HEADER_DIR" \
    -I "$REPO_ROOT" \
    -I "$REPO_ROOT/common/include" \
    -I "$REPO_ROOT/common/runtime" \
    -c "$CONNECTOR_DIR/module/mod_msconnector.c" \
    -o "$OBJ_DIR/mod_msconnector.o"

# Unresolved lighttpd host symbols are intentional and are resolved by the
# pinned lighttpd binary when it loads the module.
"$CC_BIN" \
    -std="$MSCONNECTOR_C_STD" \
    -fPIC \
    -Wall \
    -Wextra \
    -Werror \
    -shared \
    "$OBJ_DIR"/common_*.o \
    "$RUNTIME_OBJECT" \
    "$OBJ_DIR/lighttpd_modsecurity_mapper.o" \
    "$OBJ_DIR/mod_msconnector.o" \
    -L "$MODSECURITY_LIB_DIR" \
    "-Wl,-rpath,$MODSECURITY_LIB_DIR" \
    -lmodsecurity \
    -o "$MODULE_DIR/mod_msconnector.so"

{
    printf 'c_standard=%s\n' "$MSCONNECTOR_C_STD"
    printf 'lighttpd_source_dir=%s\n' "$LIGHTTPD_SOURCE_DIR"
    printf 'lighttpd_header_dir=%s\n' "$LIGHTTPD_HEADER_DIR"
    printf 'lighttpd_config_dir=%s\n' "$LIGHTTPD_CONFIG_DIR_FOUND"
    printf 'modsecurity_include_dir=%s\n' "$MODSECURITY_INCLUDE_DIR"
    printf 'modsecurity_lib_dir=%s\n' "$MODSECURITY_LIB_DIR"
    printf 'module=%s\n' "$MODULE_DIR/mod_msconnector.so"
} > "$OUT_DIR/build-info.txt"

printf 'lighttpd_connector_build: PASS output=%s\n' "$MODULE_DIR/mod_msconnector.so"
