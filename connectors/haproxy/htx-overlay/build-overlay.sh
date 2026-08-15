#!/bin/sh
# Build the repository-owned native HTX observer overlay into an isolated
# version-contract-selected HAProxy worktree. It never mutates the source tree.
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
if [ -n "${CONNECTOR_ROOT:-}" ]; then
    CONNECTOR_ROOT=$(CDPATH='' cd "$CONNECTOR_ROOT" && pwd)
else
    CONNECTOR_ROOT=$(CDPATH='' cd "$SCRIPT_DIR/../../.." && pwd)
fi

SOURCE_DIR=${HAPROXY_HTX_SOURCE_DIR:?set HAPROXY_HTX_SOURCE_DIR to a verified HAProxy source tree}
BUILD_DIR=${HAPROXY_HTX_BUILD_DIR:?set HAPROXY_HTX_BUILD_DIR to an empty output directory}
MODSECURITY_INCLUDE_DIR=${MODSECURITY_INCLUDE_DIR:?set MODSECURITY_INCLUDE_DIR}
MODSECURITY_LIB_DIR=${MODSECURITY_LIB_DIR:?set MODSECURITY_LIB_DIR}
HAPROXY_MODSECURITY_BINDING_CPPFLAGS=${HAPROXY_MODSECURITY_BINDING_CPPFLAGS:-}
MAKE_JOBS=${MAKE_JOBS:-2}
CONTRACT_FILE="$SCRIPT_DIR/version-contract.json"
CONTRACT_PARSER="$SCRIPT_DIR/version_contract.py"
contract_field() {
    field_name=$1
    python3 "$CONTRACT_PARSER" --contract "$CONTRACT_FILE" --field "$field_name"
}
HAPROXY_VERSION=$(contract_field version)
MAKEFILE_PATCH=$(contract_field makefile_patch)

die() {
    echo "haproxy-htx-overlay: $*" >&2
    exit 1
}

sha256_of() {
    sha256_input=$1
    sha256sum "$sha256_input" | awk '{print $1}'
}

require_file() {
    required_path=$1
    required_description=$2
    [ -f "$required_path" ] || die "missing $required_description: $required_path"
}

require_dir() {
    required_path=$1
    required_description=$2
    [ -d "$required_path" ] || die "missing $required_description: $required_path"
}

canonical_path() {
    input_path=$1
    python3 - "$input_path" <<'PY'
import os
import sys

print(os.path.realpath(os.path.abspath(sys.argv[1])))
PY
}

SOURCE_DIR=$(canonical_path "$SOURCE_DIR")
BUILD_DIR=$(canonical_path "$BUILD_DIR")
CONNECTOR_ROOT=$(canonical_path "$CONNECTOR_ROOT")
case "$BUILD_DIR" in
    /|"$SOURCE_DIR"|"$SOURCE_DIR"/*)
        die "HAPROXY_HTX_BUILD_DIR must be outside the verified source tree: $BUILD_DIR"
        ;;
    "$CONNECTOR_ROOT"|"$CONNECTOR_ROOT"/*)
        die "HAPROXY_HTX_BUILD_DIR must be outside the connector repository: $BUILD_DIR"
        ;;
    *) ;;
esac
WORKTREE="$BUILD_DIR/worktree"

require_dir "$SOURCE_DIR" "HAProxy source directory"
require_file "$SOURCE_DIR/Makefile" "HAProxy Makefile"
require_file "$SOURCE_DIR/VERSION" "HAProxy VERSION"
require_dir "$MODSECURITY_INCLUDE_DIR/modsecurity" "libmodsecurity headers"
require_dir "$MODSECURITY_LIB_DIR" "libmodsecurity library directory"
require_file "$SCRIPT_DIR/haproxy_modsecurity_htx_filter.c" "HTX filter source"
require_file "$SCRIPT_DIR/$MAKEFILE_PATCH" "HAProxy Makefile overlay"
command -v sha256sum >/dev/null 2>&1 || die "sha256sum is required for overlay build provenance"

version=$(tr -d '[:space:]' < "$SOURCE_DIR/VERSION")
[ "$version" = "$HAPROXY_VERSION" ] || die "expected HAProxy $HAPROXY_VERSION, found '$version'"

if [ -e "$WORKTREE" ]; then
    die "refusing to reuse existing worktree: $WORKTREE (choose a new HAPROXY_HTX_BUILD_DIR)"
fi
mkdir -p "$BUILD_DIR" "$WORKTREE"

(cd "$SOURCE_DIR" && tar -cf - .) | (cd "$WORKTREE" && tar -xf -)

cp "$SCRIPT_DIR/haproxy_modsecurity_htx_filter.c" "$WORKTREE/src/haproxy_modsecurity_htx_filter.c"
cp "$CONNECTOR_ROOT/connectors/haproxy/src/haproxy_modsecurity_binding.c" "$WORKTREE/src/haproxy_modsecurity_binding.c"
cp "$CONNECTOR_ROOT/connectors/haproxy/src/haproxy_modsecurity_binding.h" "$WORKTREE/src/haproxy_modsecurity_binding.h"
cp "$CONNECTOR_ROOT/connectors/haproxy/src/haproxy_modsecurity_mapper.c" "$WORKTREE/src/haproxy_modsecurity_mapper.c"
cp "$CONNECTOR_ROOT/connectors/haproxy/src/haproxy_modsecurity_mapper.h" "$WORKTREE/src/haproxy_modsecurity_mapper.h"
cp -R "$CONNECTOR_ROOT/common/include/msconnector" "$WORKTREE/include/"
require_file "$CONNECTOR_ROOT/common/src/header_validation_internal.h" "Common internal header"
cp "$CONNECTOR_ROOT/common/src/header_validation_internal.h" "$WORKTREE/src/header_validation_internal.h"

COMMON_SOURCES='config.c config_parser.c directive_spec.c directive_adapter.c request_helpers.c response_helpers.c request_mapper_contract.c response_mapper_contract.c headers.c event.c event_jsonl.c json_escape.c rule_id.c log_sanitize.c redaction.c resource_limits.c dos_guard.c error.c status.c body_policy.c crs.c transaction_state.c decision.c decision_action.c late_intervention.c flow_guard.c integrity_event.c rule_loader.c rule_merge.c http_status.c block_statuses.c path_policy.c intervention.c rule_error.c rule_event.c artifacts.c artifact_layout.c test_result.c test_result_json.c'
for source in $COMMON_SOURCES; do
    require_file "$CONNECTOR_ROOT/common/src/$source" "Common SDK source"
    cp "$CONNECTOR_ROOT/common/src/$source" "$WORKTREE/src/msconnector_$source"
done

(cd "$WORKTREE" && patch --dry-run -p1 < "$SCRIPT_DIR/$MAKEFILE_PATCH")
(cd "$WORKTREE" && patch -p1 < "$SCRIPT_DIR/$MAKEFILE_PATCH")

modsecurity_library=
for candidate in "$MODSECURITY_LIB_DIR"/libmodsecurity.so \
                 "$MODSECURITY_LIB_DIR"/libmodsecurity.a \
                 "$MODSECURITY_LIB_DIR"/libmodsecurity.so.*; do
    if [ -f "$candidate" ]; then
        modsecurity_library=$candidate
        break
    fi
done
[ -n "$modsecurity_library" ] || die "no libmodsecurity library found under $MODSECURITY_LIB_DIR"

make -C "$WORKTREE" TARGET=linux-glibc -j "$MAKE_JOBS" \
	USE_OPENSSL=1 \
    CFLAGS="-I$MODSECURITY_INCLUDE_DIR $HAPROXY_MODSECURITY_BINDING_CPPFLAGS" \
    ADDLIB="$modsecurity_library -Wl,-rpath,$MODSECURITY_LIB_DIR -lstdc++" \
    haproxy

[ -x "$WORKTREE/haproxy" ] || die "HAProxy build did not produce $WORKTREE/haproxy"
{
    printf 'haproxy_version=%s\n' "$version"
    printf 'source_dir=%s\n' "$SOURCE_DIR"
    printf 'source_makefile_sha256=%s\n' "$(sha256_of "$SOURCE_DIR/Makefile")"
    printf 'overlay_filter_sha256=%s\n' "$(sha256_of "$SCRIPT_DIR/haproxy_modsecurity_htx_filter.c")"
    printf 'overlay_patch_sha256=%s\n' "$(sha256_of "$SCRIPT_DIR/$MAKEFILE_PATCH")"
    printf 'binding_sha256=%s\n' "$(sha256_of "$CONNECTOR_ROOT/connectors/haproxy/src/haproxy_modsecurity_binding.c")"
    printf 'haproxy_binary=%s\n' "$WORKTREE/haproxy"
    printf 'haproxy_binary_sha256=%s\n' "$(sha256_of "$WORKTREE/haproxy")"
} > "$BUILD_DIR/overlay-build.env"
printf '%s\n' "$WORKTREE/haproxy"
