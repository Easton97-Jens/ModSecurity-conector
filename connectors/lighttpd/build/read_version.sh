#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH='' cd "$(dirname "$0")" && pwd)
CONTRACT=$SCRIPT_DIR/../lighttpd-version.contract
KEY=${1:-LIGHTTPD_VERSION}

case "$KEY" in
    LIGHTTPD_SERIES|LIGHTTPD_VERSION|LIGHTTPD_SOURCE_URL|LIGHTTPD_DOWNLOAD_URL|LIGHTTPD_SHA256|LIGHTTPD_PATCH_FILENAME) ;;
    *) printf 'unsupported Lighttpd contract key: %s\n' "$KEY" >&2; exit 2 ;;
esac

awk -v key="$KEY" '
    /^[[:space:]]*#/ || /^[[:space:]]*$/ { next }
    {
        field_count = split($0, fields, "=")
        if (field_count != 2) exit 1
        if (fields[1] == key) { value=fields[2]; count++ }
    }
    END {
        if (count != 1) exit 1
        if (key == "LIGHTTPD_SERIES") valid = value ~ /^[0-9]+\.[0-9]+$/
        else if (key == "LIGHTTPD_VERSION") valid = value ~ /^[0-9]+\.[0-9]+\.[0-9]+$/
        else if (key == "LIGHTTPD_SOURCE_URL") valid = value ~ /^https:\/\/download\.lighttpd\.net\/lighttpd\/releases-[0-9]+\.[0-9]+\.x\/$/
        else if (key == "LIGHTTPD_DOWNLOAD_URL") valid = value ~ /^https:\/\/download\.lighttpd\.net\/lighttpd\/releases-[0-9]+\.[0-9]+\.x\/lighttpd-[0-9]+\.[0-9]+\.[0-9]+\.tar\.xz$/
        else if (key == "LIGHTTPD_SHA256") valid = length(value) == 64 && value ~ /^[0-9A-Fa-f]+$/
        else valid = value ~ /^[A-Za-z0-9_.-]+\.patch$/
        if (!valid) exit 1
        print value
    }
' "$CONTRACT"
