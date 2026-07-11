#!/bin/sh
# Build the repository-owned native HTX observer overlay into an isolated
# HAProxy 3.2.21 worktree.  It never mutates the verified source tree.
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
if [ -n "${CONNECTOR_ROOT:-}" ]; then
    CONNECTOR_ROOT=$(CDPATH= cd "$CONNECTOR_ROOT" && pwd)
else
    CONNECTOR_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
fi

SOURCE_DIR=${HAPROXY_HTX_SOURCE_DIR:?set HAPROXY_HTX_SOURCE_DIR to HAProxy 3.2.21 source}
BUILD_DIR=${HAPROXY_HTX_BUILD_DIR:?set HAPROXY_HTX_BUILD_DIR to an empty output directory}
MODSECURITY_INCLUDE_DIR=${MODSECURITY_INCLUDE_DIR:?set MODSECURITY_INCLUDE_DIR}
MODSECURITY_LIB_DIR=${MODSECURITY_LIB_DIR:?set MODSECURITY_LIB_DIR}
MAKE_JOBS=${MAKE_JOBS:-2}

die() {
    echo "haproxy-htx-overlay: $*" >&2
    exit 1
}

require_file() {
    [ -f "$1" ] || die "missing $2: $1"
}

require_dir() {
    [ -d "$1" ] || die "missing $2: $1"
}

canonical_path() {
    python3 - "$1" <<'PY'
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
esac
WORKTREE="$BUILD_DIR/worktree"

require_dir "$SOURCE_DIR" "HAProxy source directory"
require_file "$SOURCE_DIR/Makefile" "HAProxy Makefile"
require_file "$SOURCE_DIR/VERSION" "HAProxy VERSION"
require_dir "$MODSECURITY_INCLUDE_DIR/modsecurity" "libmodsecurity headers"
require_dir "$MODSECURITY_LIB_DIR" "libmodsecurity library directory"
require_file "$SCRIPT_DIR/haproxy_modsecurity_htx_filter.c" "HTX filter source"
require_file "$SCRIPT_DIR/haproxy-3.2.21-makefile.patch" "HAProxy Makefile overlay"

version=$(tr -d '[:space:]' < "$SOURCE_DIR/VERSION")
[ "$version" = "3.2.21" ] || die "expected HAProxy 3.2.21, found '$version'"

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

COMMON_SOURCES='config.c config_parser.c directive_spec.c directive_adapter.c request_helpers.c response_helpers.c request_mapper_contract.c response_mapper_contract.c headers.c event.c event_jsonl.c json_escape.c rule_id.c log_sanitize.c redaction.c resource_limits.c dos_guard.c error.c status.c body_policy.c crs.c transaction_state.c decision.c decision_action.c late_intervention.c flow_guard.c integrity_event.c rule_loader.c rule_merge.c http_status.c block_statuses.c path_policy.c intervention.c rule_error.c rule_event.c artifacts.c artifact_layout.c test_result.c test_result_json.c'
for source in $COMMON_SOURCES; do
    require_file "$CONNECTOR_ROOT/common/src/$source" "Common SDK source"
    cp "$CONNECTOR_ROOT/common/src/$source" "$WORKTREE/src/msconnector_$source"
done

(cd "$WORKTREE" && patch --dry-run -p1 < "$SCRIPT_DIR/haproxy-3.2.21-makefile.patch")
(cd "$WORKTREE" && patch -p1 < "$SCRIPT_DIR/haproxy-3.2.21-makefile.patch")

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
    CFLAGS="-I$MODSECURITY_INCLUDE_DIR" \
    ADDLIB="$modsecurity_library -Wl,-rpath,$MODSECURITY_LIB_DIR -lstdc++" \
    haproxy

[ -x "$WORKTREE/haproxy" ] || die "HAProxy build did not produce $WORKTREE/haproxy"
printf '%s\n' "$WORKTREE/haproxy"
