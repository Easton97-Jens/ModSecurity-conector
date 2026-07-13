#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
ROOT=$(CDPATH= cd -- "$ROOT" && pwd -P)
PYTHON_BIN=${PYTHON:-python3}

block() {
    echo "BLOCKED: $*" >&2
    exit 77
}

[ -n "${COMPDB_OUTPUT:-}" ] || {
    echo "FAIL: COMPDB_OUTPUT is required" >&2
    exit 2
}
case "$COMPDB_OUTPUT" in
    /*) ;;
    *) echo "FAIL: COMPDB_OUTPUT must be absolute: $COMPDB_OUTPUT" >&2; exit 2 ;;
esac

command -v "$PYTHON_BIN" >/dev/null 2>&1 || block "missing Python interpreter: $PYTHON_BIN"
command -v clangd >/dev/null 2>&1 || block "missing clangd"

OUTPUT_PARENT=$(dirname -- "$COMPDB_OUTPUT")
OUTPUT_NAME=$(basename -- "$COMPDB_OUTPUT")
[ -f "$COMPDB_OUTPUT" ] || {
    echo "FAIL: compilation database is missing: $COMPDB_OUTPUT" >&2
    exit 1
}
OUTPUT_PARENT=$(CDPATH= cd -- "$OUTPUT_PARENT" && pwd -P) || {
    echo "FAIL: cannot resolve compilation database parent: $OUTPUT_PARENT" >&2
    exit 1
}
OUTPUT=$OUTPUT_PARENT/$OUTPUT_NAME

"$PYTHON_BIN" "$SCRIPT_DIR/compile_database.py" \
    --repo-root "$ROOT" \
    --output "$OUTPUT" \
    --verify-only \
    --require nginx \
    --require cpp

STAGE=$(mktemp -d "$OUTPUT_PARENT/.clangd-c17.XXXXXX") || block "cannot create external clangd staging directory"
trap 'rm -rf "$STAGE"' EXIT HUP INT TERM
cp "$OUTPUT" "$STAGE/compile_commands.json"

for source in \
    connectors/nginx/src/ngx_http_modsecurity_module.c \
    common/src/late_intervention.c \
    common/scripts/modsecurity_targeted_eval.cc
do
    clangd \
        --check="$ROOT/$source" \
        --compile-commands-dir="$STAGE" \
        --background-index=false \
        --clang-tidy=false \
        --enable-config=false \
        --tweaks= \
        --compile_args_from=filesystem \
        --log=error
done

echo "PASS: clangd checked representative NGINX, Common, and C++17 translation units"
