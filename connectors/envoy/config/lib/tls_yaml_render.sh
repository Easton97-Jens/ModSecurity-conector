#!/bin/sh

# Render a path for a YAML double-quoted scalar embedded in a fixed sed
# replacement expression. Callers own the surrounding YAML quotes.
render_yaml_path_for_sed_replacement() {
    input=$1
    case "$input" in
        *'
'*|*''*) return 1 ;;
    esac
    if LC_ALL=C printf '%s' "$input" | LC_ALL=C grep -q '[[:cntrl:]]'; then
        return 1
    fi
    printf '%s' "$input" | sed \
        -e 's/[\\"]/\\&/g' \
        -e 's/[\\&|]/\\&/g'
}

create_private_loopback_tls() {
    certificate=$1
    private_key=$2
    umask 077
    openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 1 \
        -subj /CN=127.0.0.1 -addext subjectAltName=IP:127.0.0.1 \
        -keyout "$private_key" -out "$certificate" >/dev/null 2>&1 || return 1
    chmod 600 "$certificate" "$private_key"
}
