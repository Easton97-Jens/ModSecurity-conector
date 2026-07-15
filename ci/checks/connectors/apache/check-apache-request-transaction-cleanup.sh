#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
FRAMEWORK_ROOT=${FRAMEWORK_ROOT:-"$REPO_ROOT/modules/ModSecurity-test-Framework"}
FRAMEWORK_COMMON="$FRAMEWORK_ROOT/ci/lib/common.sh"
OUT=${APACHE_REQUEST_TRANSACTION_CLEANUP_OUT:-"${BUILD_ROOT:-/var/tmp/ModSecurity-conector-verified/build}/apache-request-transaction-cleanup"}
CC_BIN=${CC:-cc}

if [ ! -f "$FRAMEWORK_COMMON" ]; then
    echo "BLOCKED: apache_request_transaction_cleanup missing framework common.sh: $FRAMEWORK_COMMON" >&2
    exit 77
fi

# shellcheck source=/dev/null
. "$FRAMEWORK_COMMON"

case "$OUT" in
    /*) ;;
    *)
        echo "FAIL: apache_request_transaction_cleanup output must be absolute: $OUT" >&2
        exit 2
        ;;
esac

require_command_or_blocked "$CC_BIN" "apache_request_transaction_cleanup missing compiler: $CC_BIN"

APXS_BIN=$(framework_find_apxs 2>/dev/null || true)
if [ -z "$APXS_BIN" ]; then
    echo "CHECK_STATUS_REASON apache_development_prerequisite" >&2
    skip_blocked "apache_request_transaction_cleanup missing apxs/apxs2 with usable Apache headers"
fi

APXS_CFLAGS=$($APXS_BIN -q CFLAGS 2>/dev/null || true)
APXS_CPPFLAGS=$($APXS_BIN -q CPPFLAGS 2>/dev/null || true)
APXS_INCLUDEDIR=$($APXS_BIN -q INCLUDEDIR 2>/dev/null || true)
APXS_INCLUDES=$($APXS_BIN -q INCLUDES 2>/dev/null || true)
APXS_BINDIR=$($APXS_BIN -q BINDIR 2>/dev/null || true)
APR_CONFIG=
for APR_CONFIG_CANDIDATE in "$APXS_BINDIR/apr-1-config" "$APXS_BINDIR/apr-2-config" apr-1-config apr-2-config; do
    APR_CONFIG=$(ci_command_path "$APR_CONFIG_CANDIDATE" 2>/dev/null || true)
    if [ -n "$APR_CONFIG" ]; then
        break
    fi
done
if [ -z "$APR_CONFIG" ]; then
    skip_blocked "apache_request_transaction_cleanup missing apr-1-config/apr-2-config"
fi

APR_INCLUDES=$($APR_CONFIG --includes 2>/dev/null || true)
APR_CPPFLAGS=$($APR_CONFIG --cppflags 2>/dev/null || true)
APR_LINK_FLAGS=$($APR_CONFIG --link-ld 2>/dev/null || true)
if [ -z "$APR_LINK_FLAGS" ]; then
    APR_LINK_FLAGS=$($APR_CONFIG --libs 2>/dev/null || true)
fi
if [ -z "$APR_LINK_FLAGS" ]; then
    skip_blocked "apache_request_transaction_cleanup could not obtain APR link flags"
fi
APR_LIBDIR=
for APR_LINK_FLAG in $APR_LINK_FLAGS; do
    case "$APR_LINK_FLAG" in
        -L*)
            APR_LIBDIR=${APR_LINK_FLAG#-L}
            break
            ;;
    esac
done

MODSECURITY_INCLUDE_FLAGS=$(modsecurity_include_flags_or_blocked)
APXS_INCLUDEDIR_FLAG=
if [ -n "$APXS_INCLUDEDIR" ]; then
    APXS_INCLUDEDIR_FLAG="-I$APXS_INCLUDEDIR"
fi
INCLUDES="-I$REPO_ROOT/connectors/apache/src -I$REPO_ROOT/common/include $APXS_INCLUDEDIR_FLAG $APXS_INCLUDES $APR_INCLUDES $APR_CPPFLAGS $MODSECURITY_INCLUDE_FLAGS"
APR_RPATH_FLAG=
if [ -n "$APR_LIBDIR" ] && [ -d "$APR_LIBDIR" ]; then
    APR_RPATH_FLAG="-Wl,-rpath,$APR_LIBDIR"
fi

mkdir -p "$OUT"
HARNESS="$SCRIPT_DIR/apache_request_transaction_cleanup.c"
UTILS="$REPO_ROOT/connectors/apache/src/msc_utils.c"
BIN="$OUT/apache-request-transaction-cleanup"

"$CC_BIN" -std=c17 -Wall -Wextra -Werror -ffunction-sections -fdata-sections \
    $APXS_CFLAGS $APXS_CPPFLAGS $INCLUDES "$HARNESS" "$UTILS" \
    -Wl,--gc-sections $APR_RPATH_FLAG $APR_LINK_FLAGS -o "$BIN"
"$BIN"
