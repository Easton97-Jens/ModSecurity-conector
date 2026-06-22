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

enabled_status() {
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

component_status() {
    enabled=$1
    if [ "$enabled" = "true" ]; then
        printf '%s\n' source_pinned_download_opt_in_required
    else
        printf '%s\n' source_known_pin_missing
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

print_component() {
    name=$1
    version=$2
    source_page=$3
    install_docs=$4
    latest_marker=$5
    download_url=$6
    sha256=$7
    sha256_url=$8
    expected_binary=$9
    integration_mode=${10:-}

    sha_state=$(sha_status "$sha256")
    enabled=$(enabled_status "$version" "$download_url" "$sha256")
    status=$(component_status "$enabled")
    resolved=$(resolved_binary "$expected_binary")

    printf 'name=%s\n' "$name"
    printf 'version=%s\n' "$version"
    printf 'source_page=%s\n' "$source_page"
    if [ -n "$install_docs" ]; then
        printf 'install_docs=%s\n' "$install_docs"
    fi
    if [ -n "$latest_marker" ]; then
        printf 'latest_marker=%s\n' "$latest_marker"
    fi
    printf 'download_url=%s\n' "$download_url"
    printf 'sha256_status=%s\n' "$sha_state"
    printf 'sha256=%s\n' "$sha256"
    printf 'sha256_url=%s\n' "$sha256_url"
    printf 'expected_binary=%s\n' "$expected_binary"
    if [ "$MODE" = "inventory" ]; then
        printf 'resolved_binary=%s\n' "$resolved"
    fi
    printf 'enabled=%s\n' "$enabled"
    printf 'status=%s\n' "$status"
    if [ -n "$integration_mode" ]; then
        printf 'integration_mode=%s\n' "$integration_mode"
    fi
    printf '\n'
}

case "$MODE" in
    inventory|sources) ;;
    *)
        echo "usage: $0 [inventory|sources]" >&2
        exit 2
        ;;
esac

print_component \
    envoy \
    "$ENVOY_VERSION" \
    "$ENVOY_SOURCE_PAGE" \
    "$ENVOY_INSTALL_DOCS_URL" \
    "" \
    "$ENVOY_DOWNLOAD_URL" \
    "$ENVOY_SHA256" \
    "$ENVOY_SHA256_URL" \
    "$ENVOY_BIN" \
    "$ENVOY_INTEGRATION_MODE"

print_component \
    traefik \
    "$TRAEFIK_VERSION" \
    "$TRAEFIK_SOURCE_PAGE" \
    "$TRAEFIK_INSTALL_DOCS_URL" \
    "" \
    "$TRAEFIK_DOWNLOAD_URL" \
    "$TRAEFIK_SHA256" \
    "$TRAEFIK_SHA256_URL" \
    "$TRAEFIK_BIN" \
    "$TRAEFIK_INTEGRATION_MODE"

print_component \
    lighttpd \
    "$LIGHTTPD_VERSION" \
    "$LIGHTTPD_SOURCE_PAGE" \
    "" \
    "$LIGHTTPD_LATEST_MARKER_URL" \
    "$LIGHTTPD_DOWNLOAD_URL" \
    "$LIGHTTPD_SHA256" \
    "$LIGHTTPD_SHA256_URL" \
    "$LIGHTTPD_BIN" \
    "$LIGHTTPD_INTEGRATION_MODE"
