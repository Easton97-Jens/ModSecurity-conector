#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
CC_BIN="${CC:-cc}"
OUT_DIR="$BUILD_ROOT/adapter-helper-smoke"
SMOKE_C="$OUT_DIR/adapter_helper_smoke.c"
SMOKE_BIN="$OUT_DIR/adapter_helper_smoke"

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "adapter_helper_smoke: BUILD_ROOT must be absolute: $BUILD_ROOT"; exit 77 ;;
esac

case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "adapter_helper_smoke: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT"
        exit 77
        ;;
esac

command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "adapter_helper_smoke: missing C compiler: $CC_BIN"
    exit 77
}

mkdir -p "$OUT_DIR"
cat > "$SMOKE_C" <<'EOF'
#include "connectors/apache/src/metadata.h"
#include "connectors/nginx/src/metadata.h"

#include <assert.h>
#include <string.h>

int main(void) {
    const msconnector_apache_adapter_metadata *apache;
    const msconnector_nginx_adapter_metadata *nginx;
    msconnector_origin apache_origin;
    msconnector_origin nginx_origin;

    apache = msconnector_apache_adapter_metadata_get();
    nginx = msconnector_nginx_adapter_metadata_get();
    apache_origin = msconnector_apache_adapter_origin();
    nginx_origin = msconnector_nginx_adapter_origin();

    assert(apache != 0);
    assert(nginx != 0);
    assert(!msconnector_origin_is_empty(&apache->origin));
    assert(!msconnector_origin_is_empty(&nginx->origin));
    assert(!msconnector_origin_is_empty(&apache_origin));
    assert(!msconnector_origin_is_empty(&nginx_origin));

    assert(strcmp(apache->origin.component, "ModSecurity-apache") == 0);
    assert(strcmp(apache->origin.source_repository,
        "https://github.com/owasp-modsecurity/ModSecurity-apache") == 0);
    assert(strcmp(apache->origin.source_commit,
        "0488c77f69669584324b70460614a382224b4883") == 0);
    assert(strcmp(apache->origin.source_describe,
        "v0.0.9-beta1-26-g0488c77") == 0);
    assert(strcmp(apache->origin.license, "Apache-2.0") == 0);
    assert(strcmp(apache->source_kind, "monorepo-upstream") == 0);
    assert(strcmp(apache->imported_path, "connectors/apache/upstream") == 0);

    assert(strcmp(nginx->origin.component, "ModSecurity-nginx") == 0);
    assert(strcmp(nginx->origin.source_repository,
        "https://github.com/owasp-modsecurity/ModSecurity-nginx") == 0);
    assert(strcmp(nginx->origin.source_commit,
        "9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846") == 0);
    assert(strcmp(nginx->origin.source_describe,
        "v1.0.4-14-g9eb44fd") == 0);
    assert(strcmp(nginx->origin.license, "Apache-2.0") == 0);
    assert(strcmp(nginx->source_kind, "monorepo-upstream") == 0);
    assert(strcmp(nginx->imported_path, "connectors/nginx/upstream") == 0);

    return 0;
}
EOF

"$CC_BIN" -std=c99 -Wall -Wextra -Werror \
    -I "$REPO_ROOT" \
    -I "$REPO_ROOT/common/include" \
    "$REPO_ROOT/common/src/origin.c" \
    "$REPO_ROOT/connectors/apache/src/metadata.c" \
    "$REPO_ROOT/connectors/nginx/src/metadata.c" \
    "$SMOKE_C" \
    -o "$SMOKE_BIN"

"$SMOKE_BIN"
echo "adapter_helper_smoke: pass output=$OUT_DIR"
