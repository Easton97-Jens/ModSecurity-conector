#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
CONFIG_FILE=${CONFIG_FILE:-$SCRIPT_DIR/envoy-ext-authz.conf}
RULES_FILE=${RULES_FILE:-$REPO_ROOT/common/rules/modsecurity_targeted_smoke.conf}
EVENT_LOG_PATH=${EVENT_LOG_PATH:-$BUILD_ROOT/envoy-connector/events.jsonl}
OUTPUT_CONFIG=${OUTPUT_CONFIG:-$BUILD_ROOT/envoy-connector/config/envoy-ext-authz.runtime.conf}

absolute_existing_file() {
    input=$1
    case "$input" in
        /*) candidate=$input ;;
        *) candidate=$(CDPATH= cd "$(dirname "$input")" && pwd)/$(basename "$input") ;;
    esac
    [ -f "$candidate" ] || return 1
    printf '%s\n' "$candidate"
}

absolute_path() {
    input=$1
    case "$input" in
        /*) printf '%s\n' "$input" ;;
        *) printf '%s/%s\n' "$(pwd)" "$input" ;;
    esac
}

CONFIG_FILE=$(absolute_existing_file "$CONFIG_FILE") || {
    echo "envoy_config: config template is not a file: $CONFIG_FILE" >&2
    exit 2
}
RULES_FILE=$(absolute_existing_file "$RULES_FILE") || {
    echo "envoy_config: rules file is not a file: $RULES_FILE" >&2
    exit 2
}
EVENT_LOG_PATH=$(absolute_path "$EVENT_LOG_PATH")
OUTPUT_CONFIG=$(absolute_path "$OUTPUT_CONFIG")

case "$OUTPUT_CONFIG" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_config: generated config must not be inside the checkout: $OUTPUT_CONFIG" >&2
        exit 2
        ;;
esac
case "$EVENT_LOG_PATH" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_config: event log must not be inside the checkout: $EVENT_LOG_PATH" >&2
        exit 2
        ;;
esac

escape_replacement() {
    printf '%s' "$1" | sed 's/[\\&|]/\\&/g'
}

rules_replacement=$(escape_replacement "$RULES_FILE")
event_replacement=$(escape_replacement "$EVENT_LOG_PATH")
mkdir -p "$(dirname "$OUTPUT_CONFIG")" "$(dirname "$EVENT_LOG_PATH")"
sed \
    -e "s|@RULES_FILE@|$rules_replacement|g" \
    -e "s|@EVENT_PATH@|$event_replacement|g" \
    "$CONFIG_FILE" > "$OUTPUT_CONFIG"
chmod 600 "$OUTPUT_CONFIG"

if grep -q '@RULES_FILE@\|@EVENT_PATH@' "$OUTPUT_CONFIG"; then
    echo "envoy_config: unresolved placeholder in $OUTPUT_CONFIG" >&2
    exit 2
fi

printf '%s\n' "$OUTPUT_CONFIG"
