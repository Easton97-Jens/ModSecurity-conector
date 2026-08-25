#!/bin/sh
# A verified fresh CRS checkout starts outside the component cache so the
# Framework fetch cannot reuse a cache-owned source. The HAProxy lifecycle
# subsequently requires CRS_SOURCE_DIR below its private component cache.
# The Python helper performs a no-replace rename anchored to checked directory
# descriptors; this wrapper then revalidates the moved Git checkout.

set -eu

: "${CELL_ROOT:?CELL_ROOT must be set}"
: "${VERIFIED_RUN_ROOT:?VERIFIED_RUN_ROOT must be set}"
: "${CACHE_ROOT:?CACHE_ROOT must be set}"
: "${CONNECTOR_COMPONENT_CACHE:?CONNECTOR_COMPONENT_CACHE must be set}"
: "${SOURCE_ROOT:?SOURCE_ROOT must be set}"
: "${CRS_SOURCE_DIR:?CRS_SOURCE_DIR must be set}"
: "${FRAMEWORK_ROOT:?FRAMEWORK_ROOT must be set}"
: "${CONNECTOR_REPOSITORY_ROOT:?CONNECTOR_REPOSITORY_ROOT must be set}"

case "$CONNECTOR_REPOSITORY_ROOT" in
    /*) ;;
    *) ci_blocked "Connector repository root must be absolute for CRS promotion"; exit 77 ;;
esac
PROMOTION_HELPER="$CONNECTOR_REPOSITORY_ROOT/ci/runtime/lifecycle/promote-fresh-crs-source-to-component-cache.py"
if [ ! -f "$PROMOTION_HELPER" ] || [ -L "$PROMOTION_HELPER" ]; then
    ci_blocked "CRS promotion helper is missing or unsafe"
    exit 77
fi

python3 "$PROMOTION_HELPER" \
    --cell-root "$CELL_ROOT" \
    --verified-run-root "$VERIFIED_RUN_ROOT" \
    --cache-root "$CACHE_ROOT" \
    --component-cache "$CONNECTOR_COMPONENT_CACHE" \
    --source-root "$SOURCE_ROOT" \
    --crs-source-dir "$CRS_SOURCE_DIR" || exit $?

SOURCE_ROOT="$CONNECTOR_COMPONENT_CACHE/sources"
CRS_SOURCE_DIR="$SOURCE_ROOT/coreruleset"
export SOURCE_ROOT CRS_SOURCE_DIR

case "$FRAMEWORK_ROOT" in
    /*) ;;
    *) ci_blocked "Framework root must be absolute for CRS post-promotion verification"; exit 77 ;;
esac
if [ ! -f "$FRAMEWORK_ROOT/ci/provisioning/crs-provenance.sh" ] || [ -L "$FRAMEWORK_ROOT/ci/provisioning/crs-provenance.sh" ]; then
    ci_blocked "Framework CRS provenance verifier is missing or unsafe"
    exit 77
fi

CRS_PROVENANCE_CONTEXT=promote_fresh_crs_source
# shellcheck disable=SC1090
. "$FRAMEWORK_ROOT/ci/provisioning/crs-provenance.sh"
crs_verify_checked_out_provenance || exit 77
ci_info "promoted and reverified fresh CRS source=$CRS_SOURCE_DIR"
