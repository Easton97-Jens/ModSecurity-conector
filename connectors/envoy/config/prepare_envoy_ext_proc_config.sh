#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
CONNECTOR_DIR=$(CDPATH= cd "$SCRIPT_DIR/.." && pwd)
REPO_ROOT=$(CDPATH= cd "$CONNECTOR_DIR/../.." && pwd)
. "$SCRIPT_DIR/lib/tls_yaml_render.sh"
BUILD_ROOT=${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}
TEMPLATE=${TEMPLATE:-$SCRIPT_DIR/envoy-ext-proc-streaming.yaml.in}
VERSION_LOCK=${VERSION_LOCK:-$SCRIPT_DIR/envoy-ext-proc-versions.env}
OUTPUT_CONFIG=${OUTPUT_CONFIG:-$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml}
LISTEN_PORT=${LISTEN_PORT:-18080}
UPSTREAM_PORT=${UPSTREAM_PORT:-18081}
EXT_PROC_PORT=${EXT_PROC_PORT:-18083}
ADMIN_PORT=${ADMIN_PORT:-19001}
TLS_CERTIFICATE=${TLS_CERTIFICATE:-}
TLS_PRIVATE_KEY=${TLS_PRIVATE_KEY:-}
DOWNSTREAM_PROTOCOL=${EXT_PROC_DOWNSTREAM_PROTOCOL:-http1}

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
    input_path=$1
    case "$input_path" in
        /*) printf '%s\n' "$input_path" ;;
        *) printf '%s/%s\n' "$(pwd)" "$input_path" ;;
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
case "$DOWNSTREAM_PROTOCOL" in
    http1)
        DOWNSTREAM_ALPN_PROTOCOL=http/1.1
        DOWNSTREAM_CODEC_TYPE=HTTP1
        DOWNSTREAM_HTTP2_PROTOCOL_OPTIONS=
        ;;
    h2)
        DOWNSTREAM_ALPN_PROTOCOL=h2
        DOWNSTREAM_CODEC_TYPE=HTTP2
        DOWNSTREAM_HTTP2_PROTOCOL_OPTIONS='          http2_protocol_options: {}'
        ;;
    *)
        echo "envoy_ext_proc_config: unsupported downstream protocol profile: $DOWNSTREAM_PROTOCOL" >&2
        exit 2
        ;;
esac
if [ -z "$TLS_CERTIFICATE" ] || [ -z "$TLS_PRIVATE_KEY" ]; then
    echo "envoy_ext_proc_config: TLS certificate and private key paths are required" >&2
    exit 2
fi
TLS_CERTIFICATE=$(absolute_path "$TLS_CERTIFICATE")
TLS_PRIVATE_KEY=$(absolute_path "$TLS_PRIVATE_KEY")
set +e
TLS_CERTIFICATE_ESCAPED=$(render_yaml_path_for_sed_replacement "$TLS_CERTIFICATE")
TLS_CERTIFICATE_RENDER_STATUS=$?
set -e
if [ "$TLS_CERTIFICATE_RENDER_STATUS" -ne 0 ]; then
    echo "envoy_ext_proc_config: TLS certificate path contains an unsupported control character" >&2
    exit 2
fi
set +e
TLS_PRIVATE_KEY_ESCAPED=$(render_yaml_path_for_sed_replacement "$TLS_PRIVATE_KEY")
TLS_PRIVATE_KEY_RENDER_STATUS=$?
set -e
if [ "$TLS_PRIVATE_KEY_RENDER_STATUS" -ne 0 ]; then
    echo "envoy_ext_proc_config: TLS private key path contains an unsupported control character" >&2
    exit 2
fi

case "$OUTPUT_CONFIG" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "envoy_ext_proc_config: generated configuration must not be inside the checkout: $OUTPUT_CONFIG" >&2
        exit 2
        ;;
    *) ;;
esac

for port in "$LISTEN_PORT" "$UPSTREAM_PORT" "$EXT_PROC_PORT" "$ADMIN_PORT"; do
    case "$port" in
        *[!0-9]*|'') echo "envoy_ext_proc_config: invalid port: $port" >&2; exit 2 ;;
        *) ;;
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
    -e "s|@DOWNSTREAM_PROTOCOL@|$DOWNSTREAM_PROTOCOL|g" \
    -e "s|@DOWNSTREAM_ALPN_PROTOCOL@|$DOWNSTREAM_ALPN_PROTOCOL|g" \
    -e "s|@DOWNSTREAM_CODEC_TYPE@|$DOWNSTREAM_CODEC_TYPE|g" \
    -e "s|@DOWNSTREAM_HTTP2_PROTOCOL_OPTIONS@|$DOWNSTREAM_HTTP2_PROTOCOL_OPTIONS|g" \
    -e "s|@LISTEN_PORT@|$LISTEN_PORT|g" \
    -e "s|@UPSTREAM_PORT@|$UPSTREAM_PORT|g" \
    -e "s|@EXT_PROC_PORT@|$EXT_PROC_PORT|g" \
    -e "s|@ADMIN_PORT@|$ADMIN_PORT|g" \
    -e "s|@TLS_CERTIFICATE@|$TLS_CERTIFICATE_ESCAPED|g" \
    -e "s|@TLS_PRIVATE_KEY@|$TLS_PRIVATE_KEY_ESCAPED|g" \
    "$TEMPLATE" > "$OUTPUT_CONFIG"
chmod 600 "$OUTPUT_CONFIG"

if grep -q '@[A-Z_][A-Z_]*@' "$OUTPUT_CONFIG"; then
    echo "envoy_ext_proc_config: unresolved placeholder in $OUTPUT_CONFIG" >&2
    exit 2
fi

printf '%s\n' "$OUTPUT_CONFIG"
