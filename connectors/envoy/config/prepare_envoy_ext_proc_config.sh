#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
TEMPLATE=${TEMPLATE:-$SCRIPT_DIR/envoy-ext-proc-streaming.yaml.in}
VERSION_LOCK=${VERSION_LOCK:-$SCRIPT_DIR/envoy-ext-proc-versions.env}
OUTPUT_CONFIG=${OUTPUT_CONFIG:-$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml}
LISTEN_PORT=${LISTEN_PORT:-18080}
UPSTREAM_PORT=${UPSTREAM_PORT:-18081}
EXT_PROC_PORT=${EXT_PROC_PORT:-18083}
ADMIN_PORT=${ADMIN_PORT:-19001}

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
    case "$1" in
        /*) printf '%s\n' "$1" ;;
        *) printf '%s/%s\n' "$(pwd)" "$1" ;;
    esac
}

TEMPLATE=$(absolute_existing_file "$TEMPLATE") || {
    echo "envoy_ext_proc_config: template is not a file: $TEMPLATE" >&2
    exit 2
}
VERSION_LOCK=$(absolute_existing_file "$VERSION_LOCK") || {
    echo "envoy_ext_proc_config: version lock is not a file: $VERSION_LOCK" >&2
    exit 2
}
OUTPUT_CONFIG=$(absolute_path "$OUTPUT_CONFIG")

case "$OUTPUT_CONFIG" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_ext_proc_config: generated configuration must not be inside the checkout: $OUTPUT_CONFIG" >&2
        exit 2
        ;;
esac

for port in "$LISTEN_PORT" "$UPSTREAM_PORT" "$EXT_PROC_PORT" "$ADMIN_PORT"; do
    case "$port" in
        *[!0-9]*|'') echo "envoy_ext_proc_config: invalid port: $port" >&2; exit 2 ;;
    esac
    [ "$port" -ge 1 ] && [ "$port" -le 65535 ] || {
        echo "envoy_ext_proc_config: port out of range: $port" >&2
        exit 2
    }
done

envoy_release=$(sed -n 's/^ENVOY_RELEASE=//p' "$VERSION_LOCK")
[ -n "$envoy_release" ] || {
    echo "envoy_ext_proc_config: version lock has no ENVOY_RELEASE" >&2
    exit 2
}

mkdir -p "$(dirname "$OUTPUT_CONFIG")"
sed \
    -e "s|@ENVOY_RELEASE@|$envoy_release|g" \
    -e "s|@LISTEN_PORT@|$LISTEN_PORT|g" \
    -e "s|@UPSTREAM_PORT@|$UPSTREAM_PORT|g" \
    -e "s|@EXT_PROC_PORT@|$EXT_PROC_PORT|g" \
    -e "s|@ADMIN_PORT@|$ADMIN_PORT|g" \
    "$TEMPLATE" > "$OUTPUT_CONFIG"
chmod 600 "$OUTPUT_CONFIG"

if grep -q '@[A-Z_][A-Z_]*@' "$OUTPUT_CONFIG"; then
    echo "envoy_ext_proc_config: unresolved placeholder in $OUTPUT_CONFIG" >&2
    exit 2
fi

printf '%s\n' "$OUTPUT_CONFIG"
