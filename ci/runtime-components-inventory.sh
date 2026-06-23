#!/bin/sh
set -eu

MODE="${1:-inventory}"
CONNECTOR_ROOT="${CONNECTOR_ROOT:-$(CDPATH= cd "$(dirname "$0")/.." && pwd)}"
FRAMEWORK_ROOT="${FRAMEWORK_ROOT:-$CONNECTOR_ROOT/modules/ModSecurity-test-Framework}"
REPO_ROOT="$CONNECTOR_ROOT"

. "$FRAMEWORK_ROOT/ci/common.sh"
ci_validate_https_runtime_url_config || exit 77

sha_status() {
    value=$1
    if [ -n "$value" ] && [ "$value" != "TODO_PIN_SHA256" ]; then
        printf '%s\n' pinned
    else
        printf '%s\n' missing
    fi
}

can_download_with_opt_in() {
    version=$1
    download_url=$2
    sha256=$3
    if [ -n "$version" ] && [ "$version" != "TODO_PIN_VERSION" ] \
        && [ -n "$download_url" ] && [ -n "$sha256" ] \
        && [ "$sha256" != "TODO_PIN_SHA256" ]; then
        printf '%s\n' true
    else
        printf '%s\n' false
    fi
}

resolved_binary() {
    binary=$1
    if [ -f "$binary" ] && [ -x "$binary" ]; then
        printf '%s\n' "$binary"
    else
        printf '%s\n' '<missing>'
    fi
}

binary_status() {
    binary=$1
    if [ -f "$binary" ] && [ -x "$binary" ]; then
        printf '%s\n' binary_present
    else
        printf '%s\n' binary_missing
    fi
}

source_staged_status() {
    source_dir=$1
    if [ -d "$source_dir" ]; then
        printf '%s\n' true
    else
        printf '%s\n' false
    fi
}

local_status_for_binary() {
    binary=$1
    can_download=$2
    if [ -f "$binary" ] && [ -x "$binary" ]; then
        printf '%s\n' ready
    elif [ "$can_download" = "true" ]; then
        printf '%s\n' missing_download_opt_in_available
    else
        printf '%s\n' blocked_source_pin_missing
    fi
}

print_binary_component() {
    name=$1
    version=$2
    source_url=$3
    install_docs=$4
    download_url=$5
    sha256=$6
    sha256_url=$7
    expected_binary=$8
    integration_mode=$9

    sha_state=$(sha_status "$sha256")
    can_download=$(can_download_with_opt_in "$version" "$download_url" "$sha256")
    resolved=$(resolved_binary "$expected_binary")
    local_status=$(local_status_for_binary "$expected_binary" "$can_download")

    printf 'name=%s\n' "$name"
    printf 'version=%s\n' "$version"
    printf 'source_url=%s\n' "$source_url"
    if [ -n "$install_docs" ]; then
        printf 'install_docs=%s\n' "$install_docs"
    fi
    printf 'download_url=%s\n' "$download_url"
    printf 'sha256_status=%s\n' "$sha_state"
    printf 'sha256=%s\n' "$sha256"
    printf 'sha256_url=%s\n' "$sha256_url"
    printf 'expected_binary=%s\n' "$expected_binary"
    if [ "$MODE" = "inventory" ]; then
        printf 'resolved_binary=%s\n' "$resolved"
    fi
    printf 'can_download_with_opt_in=%s\n' "$can_download"
    printf 'local_status=%s\n' "$local_status"
    printf 'enabled=%s\n' "$can_download"
    printf 'status=source_pinned_download_opt_in_required\n'
    printf 'integration_mode=%s\n' "$integration_mode"
    printf '\n'
}

print_lighttpd_component() {
    source_dir="$LIGHTTPD_COMPONENT_ROOT/src/lighttpd-$LIGHTTPD_VERSION"
    sha_state=$(sha_status "$LIGHTTPD_SHA256")
    can_download=$(can_download_with_opt_in "$LIGHTTPD_VERSION" "$LIGHTTPD_DOWNLOAD_URL" "$LIGHTTPD_SHA256")
    source_staged=$(source_staged_status "$source_dir")
    runtime_binary_status=$(binary_status "$LIGHTTPD_BIN")
    resolved=$(resolved_binary "$LIGHTTPD_BIN")
    if [ "$runtime_binary_status" = "binary_present" ]; then
        local_status=ready
    elif [ "$source_staged" = "true" ]; then
        local_status=source_staged_build_required
    elif [ "$can_download" = "true" ]; then
        local_status=source_missing_download_opt_in_available
    else
        local_status=blocked_source_pin_missing
    fi

    printf 'name=lighttpd\n'
    printf 'version=%s\n' "$LIGHTTPD_VERSION"
    printf 'source_url=%s\n' "$LIGHTTPD_SOURCE_URL"
    printf 'release_index_url=%s\n' "$LIGHTTPD_RELEASE_INDEX_URL"
    printf 'latest_url=%s\n' "$LIGHTTPD_LATEST_URL"
    printf 'download_url=%s\n' "$LIGHTTPD_DOWNLOAD_URL"
    printf 'sha256_status=%s\n' "$sha_state"
    printf 'sha256=%s\n' "$LIGHTTPD_SHA256"
    printf 'sha256_url=%s\n' "$LIGHTTPD_SHA256_URL"
    printf 'expected_binary=%s\n' "$LIGHTTPD_BIN"
    if [ "$MODE" = "inventory" ]; then
        printf 'resolved_binary=%s\n' "$resolved"
    fi
    printf 'can_download_with_opt_in=%s\n' "$can_download"
    printf 'source_staged=%s\n' "$source_staged"
    printf 'source_dir=%s\n' "$source_dir"
    printf 'runtime_binary_status=%s\n' "$runtime_binary_status"
    printf 'integration_mode=%s\n' "$LIGHTTPD_INTEGRATION_MODE"
    printf 'local_status=%s\n' "$local_status"
    printf 'enabled=%s\n' "$can_download"
    printf 'artifact_type=source_tarball\n'
    printf 'runtime_binary_produced=false\n'
    printf 'status=source_pinned_build_required\n'
    printf '\n'
}

case "$MODE" in
    inventory|sources) ;;
    *)
        echo "usage: $0 [inventory|sources]" >&2
        exit 2
        ;;
esac

print_binary_component \
    envoy \
    "$ENVOY_VERSION" \
    "$ENVOY_SOURCE_URL" \
    "$ENVOY_INSTALL_DOCS_URL" \
    "$ENVOY_DOWNLOAD_URL" \
    "$ENVOY_SHA256" \
    "$ENVOY_SHA256_URL" \
    "$ENVOY_BIN" \
    "$ENVOY_INTEGRATION_MODE"

print_binary_component \
    traefik \
    "$TRAEFIK_VERSION" \
    "$TRAEFIK_SOURCE_URL" \
    "$TRAEFIK_INSTALL_DOCS_URL" \
    "$TRAEFIK_DOWNLOAD_URL" \
    "$TRAEFIK_SHA256" \
    "$TRAEFIK_SHA256_URL" \
    "$TRAEFIK_BIN" \
    "$TRAEFIK_INTEGRATION_MODE"

print_lighttpd_component
