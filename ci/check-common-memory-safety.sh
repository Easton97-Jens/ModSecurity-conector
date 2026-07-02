#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-${TMPDIR:-/var/tmp}/ModSecurity-conector-verified/build}"
case "$BUILD_ROOT" in
    /*)
        ;;
    *)
        echo "BLOCKED: memory_safety BUILD_ROOT must be absolute"
        exit 77
        ;;
esac
case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "BLOCKED: memory_safety BUILD_ROOT inside checkout"
        exit 77
        ;;
    *)
        ;;
esac
CC_BIN="${CC:-cc}"
command -v "$CC_BIN" >/dev/null 2>&1 || { echo "BLOCKED: memory_safety missing compiler: $CC_BIN"; exit 77; }
OUT="$BUILD_ROOT/common-memory-safety"; mkdir -p "$OUT"
cat > "$OUT/smoke.c" <<'C'
#include "msconnector/memory.h"
#include <assert.h>
int main(void){ msconnector_allocator a; void *p=0,*q=0; msconnector_allocator_init(&a, 8); assert(msconnector_alloc_checked(&a, 4, &p)); assert(p!=0); assert(a.bytes_allocated==4); assert(!msconnector_alloc_checked(&a, 9, &q)); assert(q==0); msconnector_free_checked(&a, &p, 4); assert(p==0); assert(a.bytes_allocated==0); msconnector_free_checked(&a, &p, 4); assert(p==0); assert(a.bytes_allocated==0); assert(msconnector_allocator_within_limit(&a)); return 0; }
C
FLAGS="${MSCONNECTOR_CFLAGS:--std=c17 -Wall -Wextra -Werror}"
"$CC_BIN" $FLAGS -I"$REPO_ROOT/common/include" "$OUT/smoke.c" "$REPO_ROOT/common/src/memory.c" -o "$OUT/smoke"
"$OUT/smoke"
if "$CC_BIN" $FLAGS -fsanitize=address,undefined -I"$REPO_ROOT/common/include" "$OUT/smoke.c" "$REPO_ROOT/common/src/memory.c" -o "$OUT/smoke-asan" >/dev/null 2>&1; then
    "$OUT/smoke-asan"
else
    echo "SKIPPED: optional sanitizer build unavailable; base memory_safety smoke passed"
fi
