#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH='' cd "$SCRIPT_DIR/../../.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-${TMPDIR:-/var/tmp}/ModSecurity-conector-verified/build}"
OUT_DIR="${TRAEFIK_ENGINE_SERVICE_BUILD_DIR:-$BUILD_ROOT/traefik-engine-service}"
OBJECT_DIR="$OUT_DIR/objects"
ENGINE_BIN="${TRAEFIK_ENGINE_SERVICE_BIN:-$OUT_DIR/traefik-engine-service}"
CC_BIN="${CC:-cc}"
CXX_BIN="${CXX:-c++}"
MODE="${1:-build}"

case "$OUT_DIR" in
    /*) ;;
    *) echo "BLOCKED: TRAEFIK_ENGINE_SERVICE_BUILD_DIR must be absolute: $OUT_DIR" >&2; exit 77 ;;
esac
if [ -L "$OUT_DIR" ]; then
    echo "BLOCKED: Traefik engine-service build output must not be a symlink: $OUT_DIR" >&2
    exit 77
fi
case "$OUT_DIR" in
    /|/tmp|/var/tmp)
        echo "BLOCKED: Traefik engine-service build output is too broad: $OUT_DIR" >&2
        exit 77
        ;;
esac
case "$ENGINE_BIN" in
    /*) ;;
    *) echo "BLOCKED: TRAEFIK_ENGINE_SERVICE_BIN must be absolute: $ENGINE_BIN" >&2; exit 77 ;;
esac
case "$OUT_DIR" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "BLOCKED: Traefik engine-service build output must be outside the checkout: $OUT_DIR" >&2
        exit 77
        ;;
esac
case "$ENGINE_BIN" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "BLOCKED: Traefik engine-service binary must be outside the checkout: $ENGINE_BIN" >&2
        exit 77
        ;;
esac

case "$MODE" in
    build|test) ;;
    clean)
        rm -rf "$OUT_DIR"
        printf 'traefik_engine_service_clean=pass\n'
        printf 'output=%s\n' "$OUT_DIR"
        exit 0
        ;;
    *)
        echo "usage: $0 [build|test|clean]" >&2
        exit 2
        ;;
esac

if [ -z "${MODSECURITY_INCLUDE_DIR:-}" ]; then
    echo "BLOCKED: set MODSECURITY_INCLUDE_DIR to a local libmodsecurity include directory" >&2
    exit 77
fi
if [ -z "${MODSECURITY_LIB_DIR:-}" ]; then
    echo "BLOCKED: set MODSECURITY_LIB_DIR to a local libmodsecurity library directory" >&2
    exit 77
fi

case "$MODSECURITY_INCLUDE_DIR" in
    /*) ;;
    *) echo "BLOCKED: MODSECURITY_INCLUDE_DIR must be absolute" >&2; exit 77 ;;
esac
case "$MODSECURITY_LIB_DIR" in
    /*) ;;
    *) echo "BLOCKED: MODSECURITY_LIB_DIR must be absolute" >&2; exit 77 ;;
esac

for header in modsecurity/modsecurity.h modsecurity/rules_set.h modsecurity/transaction.h; do
    if [ ! -f "$MODSECURITY_INCLUDE_DIR/$header" ]; then
        echo "BLOCKED: missing libmodsecurity header: $MODSECURITY_INCLUDE_DIR/$header" >&2
        exit 77
    fi
done

modsecurity_library=""
for candidate in \
    "$MODSECURITY_LIB_DIR/libmodsecurity.so" \
    "$MODSECURITY_LIB_DIR/libmodsecurity.dylib" \
    "$MODSECURITY_LIB_DIR/libmodsecurity.a"
do
    if [ -f "$candidate" ]; then
        modsecurity_library=$candidate
        break
    fi
done
if [ -z "$modsecurity_library" ]; then
    echo "BLOCKED: no linkable libmodsecurity library found under $MODSECURITY_LIB_DIR" >&2
    exit 77
fi

command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "BLOCKED: missing C compiler: $CC_BIN" >&2
    exit 77
}
command -v "$CXX_BIN" >/dev/null 2>&1 || {
    echo "BLOCKED: missing C++ linker: $CXX_BIN" >&2
    exit 77
}

runtime_source_count=0
for source in "$REPO_ROOT"/common/runtime/*.c; do
    if [ -f "$source" ]; then
        runtime_source_count=$((runtime_source_count + 1))
    fi
done
if [ "$runtime_source_count" -eq 0 ]; then
    echo "BLOCKED: common runtime implementation sources are not available" >&2
    exit 77
fi

rm -rf "$OBJECT_DIR"
mkdir -p "$OBJECT_DIR" "$(dirname "$ENGINE_BIN")"

objects=""
compile_source() {
    source=$1
    relative=${source#"$REPO_ROOT"/}
    object_name=$(printf '%s' "$relative" | tr '/.' '__')
    object="$OBJECT_DIR/$object_name.o"
    # TRAEFIK_ENGINE_SERVICE_CFLAGS is intentionally split into compiler args.
    # shellcheck disable=SC2086
    "$CC_BIN" \
        -std=c17 -Wall -Wextra -Werror -pthread \
        ${TRAEFIK_ENGINE_SERVICE_CFLAGS:-} \
        -I "$REPO_ROOT" \
        -I "$REPO_ROOT/common/include" \
        -I "$REPO_ROOT/common/runtime" \
        -I "$REPO_ROOT/connectors/traefik" \
        -I "$REPO_ROOT/connectors/traefik/src" \
        -I "$MODSECURITY_INCLUDE_DIR" \
        -c "$source" \
        -o "$object"
    objects="$objects $object"
}

for source in \
    "$REPO_ROOT"/common/src/*.c \
    "$REPO_ROOT"/common/runtime/*.c \
    "$REPO_ROOT/connectors/traefik/src/traefik_engine_service.c"
do
    [ -f "$source" ] || continue
    compile_source "$source"
done

# C sources are compiled in C17 mode. The final link uses the C++ driver because
# libmodsecurity is a C++ library even though this service consumes its C API.
# shellcheck disable=SC2086
"$CXX_BIN" $objects \
    -L "$MODSECURITY_LIB_DIR" \
    -Wl,-rpath,"$MODSECURITY_LIB_DIR" \
    -lmodsecurity \
    -pthread \
    ${TRAEFIK_ENGINE_SERVICE_LDFLAGS:-} \
    -o "$ENGINE_BIN"

printf 'traefik_engine_service_build=pass\n'
printf 'artifact=%s\n' "$ENGINE_BIN"
printf 'modsecurity_library=%s\n' "$modsecurity_library"

if [ "$MODE" = test ]; then
    "$ENGINE_BIN" --self-test
fi
