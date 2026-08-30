#!/bin/sh
# Resolve a header/library pair for the native HAProxy HTX overlay.
# Resolution order is explicit paths, pkg-config, then known distro paths.
set -eu

OUTPUT_FILE=${1:?usage: resolve-modsecurity.sh OUTPUT_FILE}

blocked_sentinel() {
    case "$1" in
        invalid_path_syntax)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=invalid_path_syntax' >&2
            ;;
        output_path_not_absolute)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=output_path_not_absolute' >&2
            ;;
        output_path_symlink)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=output_path_symlink' >&2
            ;;
        path_contains_whitespace)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=path_contains_whitespace' >&2
            ;;
        headers_not_found)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=headers_not_found' >&2
            ;;
        library_not_found)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=library_not_found' >&2
            ;;
        headers_missing)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=headers_missing' >&2
            ;;
        library_missing)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=library_missing' >&2
            ;;
        readlink_missing)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=readlink_missing' >&2
            ;;
        library_target_unresolved)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=library_target_unresolved' >&2
            ;;
        library_target_not_regular)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=library_target_not_regular' >&2
            ;;
        file_missing)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=file_missing' >&2
            ;;
        architecture_mismatch)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=architecture_mismatch' >&2
            ;;
        ldd_missing)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=ldd_missing' >&2
            ;;
        unresolved_runtime_dependencies)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: sentinel=unresolved_runtime_dependencies' >&2
            ;;
        *)
            printf '%s\n' 'BLOCKED: HAProxy libModSecurity resolver: internal diagnostic code rejected' >&2
            exit 77
            ;;
    esac
}

blocked() {
    blocked_sentinel "$1"
    shift
    printf 'BLOCKED: HAProxy libModSecurity resolver: %s\n' "$*" >&2
    exit 77
}

validate_path_syntax() {
    path_value=$1
    path_label=$2
    case "$path_value" in
        ''|*[!A-Za-z0-9_./+-]*)
            blocked invalid_path_syntax "$path_label contains unsupported shell/path metacharacters"
            ;;
        *)
            ;;
    esac
}

case "$OUTPUT_FILE" in
    /*) ;;
    *) blocked output_path_not_absolute "resolution output path must be absolute" ;;
esac
validate_path_syntax "$OUTPUT_FILE" MODSECURITY_RESOLUTION_FILE
[ ! -L "$OUTPUT_FILE" ] || blocked output_path_symlink "resolution output path must not be a symbolic link"

valid_include() {
    [ -f "$1/modsecurity/modsecurity.h" ] &&
        [ -f "$1/modsecurity/rules_set.h" ] &&
        [ -f "$1/modsecurity/transaction.h" ]
}

find_library() {
    for candidate in "$1"/libmodsecurity.so "$1"/libmodsecurity.so.* "$1"/libmodsecurity.a; do
        library_name=${candidate##*/}
        case "$library_name" in
            libmodsecurity.so|libmodsecurity.a)
                ;;
            libmodsecurity.so.[0-9]*)
                version=${library_name#libmodsecurity.so.}
                case "$version" in
                    *[!0-9.]*|.*|*.) continue ;;
                    *..*) continue ;;
                esac
                ;;
            *)
                continue
                ;;
        esac
        if [ -f "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done
    return 1
}

reject_whitespace() {
    case "$1" in
        *[[:space:]]*) blocked path_contains_whitespace "paths containing whitespace are not supported: $2" ;;
        *) ;;
    esac
}

include_dir=${MODSECURITY_INCLUDE_DIR:-}
lib_dir=${MODSECURITY_LIB_DIR:-}
resolution=explicit

[ -z "$include_dir" ] || validate_path_syntax "$include_dir" MODSECURITY_INCLUDE_DIR
[ -z "$lib_dir" ] || validate_path_syntax "$lib_dir" MODSECURITY_LIB_DIR

if [ -z "$include_dir" ] || [ -z "$lib_dir" ]; then
    pkg_name=
    if command -v pkg-config >/dev/null 2>&1; then
        for candidate in libmodsecurity modsecurity; do
            if pkg-config --exists "$candidate" 2>/dev/null; then
                pkg_name=$candidate
                break
            fi
        done
    fi
    if [ -n "$pkg_name" ]; then
        [ -n "$include_dir" ] || include_dir=$(pkg-config --variable=includedir "$pkg_name" 2>/dev/null || true)
        [ -n "$lib_dir" ] || lib_dir=$(pkg-config --variable=libdir "$pkg_name" 2>/dev/null || true)
        resolution=pkg-config
    fi
fi

[ -z "$include_dir" ] || validate_path_syntax "$include_dir" MODSECURITY_INCLUDE_DIR
[ -z "$lib_dir" ] || validate_path_syntax "$lib_dir" MODSECURITY_LIB_DIR

if [ -z "$include_dir" ]; then
    for candidate in /usr/include /usr/local/include; do
        if valid_include "$candidate"; then
            include_dir=$candidate
            resolution=distro-default
            break
        fi
    done
fi

if [ -z "$lib_dir" ]; then
    machine=$(uname -m)
    for candidate in \
        /usr/lib \
        /usr/lib64 \
        /usr/local/lib \
        /usr/lib/x86_64-linux-gnu \
        /usr/lib/aarch64-linux-gnu \
        "/usr/lib/$machine-linux-gnu"; do
        if find_library "$candidate" >/dev/null 2>&1; then
            lib_dir=$candidate
            resolution=distro-default
            break
        fi
    done
fi

[ -n "$include_dir" ] || blocked headers_not_found "libModSecurity headers were not found; set MODSECURITY_INCLUDE_DIR"
[ -n "$lib_dir" ] || blocked library_not_found "libModSecurity library was not found; set MODSECURITY_LIB_DIR"
reject_whitespace "$include_dir" MODSECURITY_INCLUDE_DIR
reject_whitespace "$lib_dir" MODSECURITY_LIB_DIR
valid_include "$include_dir" || blocked headers_missing "header/library pairing rejected: required headers missing under $include_dir"
library=$(find_library "$lib_dir" || true)
[ -n "$library" ] || blocked library_missing "header/library pairing rejected: libmodsecurity is missing under $lib_dir"

command -v readlink >/dev/null 2>&1 || blocked readlink_missing "readlink is required for libModSecurity symlink validation"
library_target=$(readlink -f -- "$library" 2>/dev/null || true)
[ -n "$library_target" ] || blocked library_target_unresolved "libModSecurity library symlink target could not be resolved"
[ -f "$library_target" ] || blocked library_target_not_regular "libModSecurity library symlink target is not a regular file"
reject_whitespace "$library_target" MODSECURITY_LIBRARY_TARGET

command -v file >/dev/null 2>&1 || blocked file_missing "file is required for libModSecurity architecture validation"
file_description=$(file -b "$library_target")
case "$(uname -m):$file_description" in
    x86_64:*'x86-64'*) ;;
    amd64:*'x86-64'*) ;;
    aarch64:*'ARM aarch64'*) ;;
    arm64:*'ARM aarch64'*) ;;
    *'statically linked'*|*'current ar archive'*) ;;
    *) blocked architecture_mismatch "libModSecurity architecture does not match host: $(uname -m), $file_description" ;;
esac

case "$library" in
    *.so|*.so.*)
        command -v ldd >/dev/null 2>&1 || blocked ldd_missing "ldd is required for shared libModSecurity dependency validation"
        ldd_output=$(ldd "$library_target" 2>&1 || true)
        case "$ldd_output" in
            *'not found'*) blocked unresolved_runtime_dependencies "libModSecurity has unresolved runtime dependencies" ;;
            *) ;;
        esac
        ;;
    *) ;;
esac

mkdir -p "$(dirname "$OUTPUT_FILE")"
{
    printf "MODSECURITY_INCLUDE_DIR='%s'\n" "$include_dir"
    printf "MODSECURITY_LIB_DIR='%s'\n" "$lib_dir"
    printf "MODSECURITY_LIBRARY='%s'\n" "$library"
    printf "MODSECURITY_RESOLUTION='%s'\n" "$resolution"
} > "$OUTPUT_FILE"
printf 'HAProxy libModSecurity resolver: %s (%s, %s)\n' "$resolution" "$include_dir" "$lib_dir"
