#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONTRACT=$SCRIPT_DIR/../lighttpd-version.contract
KEY=${1:-LIGHTTPD_VERSION}

case "$KEY" in
    LIGHTTPD_VERSION|LIGHTTPD_SOURCE_URL|LIGHTTPD_DOWNLOAD_URL|LIGHTTPD_SHA256|LIGHTTPD_PATCH_FILENAME) ;;
    *) printf 'unsupported Lighttpd contract key: %s\n' "$KEY" >&2; exit 2 ;;
esac

awk -F= -v key="$KEY" '
    /^[[:space:]]*#/ || /^[[:space:]]*$/ { next }
    $1 == key { value=$2; count++ }
    END {
        if (count != 1 || value !~ /^[A-Za-z0-9_.-]+$/) exit 1
        print value
    }
' "$CONTRACT"
