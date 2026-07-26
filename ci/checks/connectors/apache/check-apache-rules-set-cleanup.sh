#!/bin/sh
set -efu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
REPO_ROOT=$(CDPATH= cd -- "$REPO_ROOT" && pwd -P)
DEFAULT_BUILD_ROOT=${BUILD_ROOT:-/var/tmp/ModSecurity-conector-verified/build}
OUT=${APACHE_RULES_SET_CLEANUP_OUT:-"$DEFAULT_BUILD_ROOT/apache-rules-set-cleanup"}
CC_BIN=${CC:-cc}
APXS_BIN=${APXS_BIN:-${APXS:-}}

blocked() {
    echo "BLOCKED: apache_rules_set_cleanup $*" >&2
    exit 77
}


fail() {
    echo "FAIL: apache_rules_set_cleanup $*" >&2
    exit 2
}


reject_symlink_components() {
    output_remainder=${1#/}
    output_component_path=

    while [ -n "$output_remainder" ]; do
        case "$output_remainder" in
            */*)
                output_component=${output_remainder%%/*}
                output_remainder=${output_remainder#*/}
                ;;
            *)
                output_component=$output_remainder
                output_remainder=
                ;;
        esac
        if [ -z "$output_component" ]; then
            continue
        fi

        output_component_path=$output_component_path/$output_component
        if [ -L "$output_component_path" ]; then
            fail "output path must not traverse a symbolic link: $output_component_path"
        fi
        if [ ! -e "$output_component_path" ]; then
            return 0
        fi
    done
}


validate_external_output() {
    output_path=$1
    output_probe=$output_path

    case "$output_path" in
        /*) ;;
        *) fail "output must be absolute: $output_path" ;;
    esac
    case "$output_path" in
        *"/../"*|*/..|..)
            fail "output must not contain parent traversal: $output_path"
            ;;
        *) ;;
    esac
    reject_symlink_components "$output_path"

    while [ ! -e "$output_probe" ]; do
        output_probe=${output_probe%/*}
        if [ -z "$output_probe" ]; then
            output_probe=/
        fi
    done
    if [ ! -d "$output_probe" ]; then
        fail "nearest existing output ancestor is not a directory: $output_probe"
    fi

    output_probe=$(CDPATH= cd -- "$output_probe" && pwd -P) || \
        fail "could not canonicalize output ancestor"
    case "$output_probe" in
        "$REPO_ROOT"|"$REPO_ROOT"/*)
            fail "output must stay outside the checkout: $output_path"
            ;;
        *) ;;
    esac

    mkdir -p "$output_path" || fail "could not create output directory: $output_path"
    reject_symlink_components "$output_path"
    if [ ! -d "$output_path" ]; then
        fail "output path is not a directory: $output_path"
    fi
    OUT=$(CDPATH= cd -- "$output_path" && pwd -P) || \
        fail "could not canonicalize output directory"
    case "$OUT" in
        "$REPO_ROOT"|"$REPO_ROOT"/*)
            fail "output resolved inside the checkout: $OUT"
            ;;
        *) ;;
    esac
}


find_apxs() {
    if [ -n "$APXS_BIN" ]; then
        candidate_path=$(command -v "$APXS_BIN" 2>/dev/null || true)
        if [ -n "$candidate_path" ] && [ -x "$candidate_path" ]; then
            printf '%s\n' "$candidate_path"
            return 0
        fi
        if [ -x "$APXS_BIN" ]; then
            printf '%s\n' "$APXS_BIN"
            return 0
        fi
        return 1
    fi

    for candidate in apxs apxs2; do
        candidate_path=$(command -v "$candidate" 2>/dev/null || true)
        if [ -n "$candidate_path" ] && [ -x "$candidate_path" ]; then
            printf '%s\n' "$candidate_path"
            return 0
        fi
    done
    return 1
}


find_apr_config() {
    apxs_bindir=$1
    for candidate in "$apxs_bindir/apr-1-config" "$apxs_bindir/apr-2-config" \
        apr-1-config apr-2-config; do
        if [ -x "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
        candidate_path=$(command -v "$candidate" 2>/dev/null || true)
        if [ -n "$candidate_path" ] && [ -x "$candidate_path" ]; then
            printf '%s\n' "$candidate_path"
            return 0
        fi
    done
    return 1
}


validate_external_output "$OUT"

if ! command -v "$CC_BIN" >/dev/null 2>&1; then
    blocked "missing C compiler: $CC_BIN"
fi

APXS_BIN=$(find_apxs || true)
if [ -z "$APXS_BIN" ]; then
    blocked "missing apxs/apxs2 with usable Apache headers"
fi

APXS_CFLAGS=$("$APXS_BIN" -q CFLAGS 2>/dev/null || true)
APXS_CPPFLAGS=$("$APXS_BIN" -q CPPFLAGS 2>/dev/null || true)
APXS_INCLUDEDIR=$("$APXS_BIN" -q INCLUDEDIR 2>/dev/null || true)
APXS_INCLUDES=$("$APXS_BIN" -q INCLUDES 2>/dev/null || true)
APXS_BINDIR=$("$APXS_BIN" -q BINDIR 2>/dev/null || true)
if [ -z "$APXS_INCLUDEDIR" ] || [ ! -f "$APXS_INCLUDEDIR/httpd.h" ]; then
    blocked "apxs did not provide an include directory containing httpd.h"
fi

APR_CONFIG=$(find_apr_config "$APXS_BINDIR" || true)
if [ -z "$APR_CONFIG" ]; then
    blocked "missing apr-1-config/apr-2-config"
fi

APR_INCLUDES=$("$APR_CONFIG" --includes 2>/dev/null || true)
APR_CPPFLAGS=$("$APR_CONFIG" --cppflags 2>/dev/null || true)
APR_LINK_FLAGS=$("$APR_CONFIG" --link-ld 2>/dev/null || true)
if [ -z "$APR_LINK_FLAGS" ]; then
    APR_LINK_FLAGS=$("$APR_CONFIG" --libs 2>/dev/null || true)
fi
if [ -z "$APR_LINK_FLAGS" ]; then
    blocked "could not obtain APR link flags"
fi

MODSECURITY_INCLUDE_FLAGS=${MODSECURITY_INCLUDE_FLAGS:-}
if [ -z "$MODSECURITY_INCLUDE_FLAGS" ] && command -v pkg-config >/dev/null 2>&1; then
    for package_name in libmodsecurity modsecurity; do
        if pkg-config --exists "$package_name" 2>/dev/null; then
            MODSECURITY_INCLUDE_FLAGS=$(pkg-config --cflags "$package_name")
            break
        fi
    done
fi

APXS_INCLUDEDIR_FLAG="-I$APXS_INCLUDEDIR"
INCLUDES="-I$REPO_ROOT/connectors/apache/src -I$REPO_ROOT/common/include \
$APXS_INCLUDEDIR_FLAG $APXS_INCLUDES $APR_INCLUDES $APR_CPPFLAGS \
$MODSECURITY_INCLUDE_FLAGS"
HEADER_PROBE_LOG="$OUT/header-probe.err"
if ! printf '%s\n' '#include "mod_security3.h"' | \
    "$CC_BIN" -std=c17 $APXS_CFLAGS $APXS_CPPFLAGS $INCLUDES -E -x c - \
        >/dev/null 2>"$HEADER_PROBE_LOG"; then
    sed -n '1,120p' "$HEADER_PROBE_LOG" >&2
    blocked "missing compatible Apache/APR/libmodsecurity development headers"
fi

APR_LIBDIR=
for apr_link_flag in $APR_LINK_FLAGS; do
    case "$apr_link_flag" in
        -L*)
            APR_LIBDIR=${apr_link_flag#-L}
            break
            ;;
        *) ;;
    esac
done
APR_RPATH_FLAG=
if [ -n "$APR_LIBDIR" ] && [ -d "$APR_LIBDIR" ]; then
    APR_RPATH_FLAG="-Wl,-rpath,$APR_LIBDIR"
fi

HARNESS="$SCRIPT_DIR/apache_rules_set_cleanup.c"
CONFIG="$REPO_ROOT/connectors/apache/src/msc_config.c"
BIN="$OUT/apache-rules-set-cleanup"
COMPILE_LOG="$OUT/compile.err"

if ! "$CC_BIN" -std=c17 -Wall -Wextra -Werror -ffunction-sections \
    -fdata-sections $APXS_CFLAGS $APXS_CPPFLAGS -UNDEBUG $INCLUDES "$HARNESS" \
    "$CONFIG" -Wl,--gc-sections -Wl,--wrap=ap_log_perror_ $APR_RPATH_FLAG \
    $APR_LINK_FLAGS -o "$BIN" \
    >"$OUT/compile.out" 2>"$COMPILE_LOG"; then
    sed -n '1,200p' "$OUT/compile.out" >&2
    sed -n '1,200p' "$COMPILE_LOG" >&2
    echo "FAIL: apache_rules_set_cleanup C17 native harness compilation failed" >&2
    exit 1
fi

if ! "$BIN"; then
    echo "FAIL: apache_rules_set_cleanup native harness failed" >&2
    exit 1
fi

echo "PASS: apache_rules_set_cleanup C17 APR lifecycle harness output=$OUT"
