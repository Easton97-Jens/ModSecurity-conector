#!/bin/sh
set -eu

echo "smoke-installed: probing installed/system components (no build triggered)"

find_bin_multi() {
  for name in "$@"; do
    path=$(command -v "$name" 2>/dev/null || true)
    if [ -n "$path" ]; then
      printf '%s\n' "$path"
      return 0
    fi
  done
  return 1
}

resolve_apache_from_apxs() {
  apxs_path=$1
  [ -n "$apxs_path" ] || return 1
  sbin_dir=$($apxs_path -q SBINDIR 2>/dev/null || true)
  target_name=$($apxs_path -q TARGET 2>/dev/null || true)
  if [ -n "$sbin_dir" ] && [ -n "$target_name" ] && [ -x "$sbin_dir/$target_name" ]; then
    printf '%s\n' "$sbin_dir/$target_name"
    return 0
  fi
  if [ -n "$sbin_dir" ] && [ -x "$sbin_dir/apache2" ]; then
    printf '%s\n' "$sbin_dir/apache2"
    return 0
  fi
  if [ -n "$sbin_dir" ] && [ -x "$sbin_dir/httpd" ]; then
    printf '%s\n' "$sbin_dir/httpd"
    return 0
  fi
  return 1
}

APXS_BIN="${APXS_BIN:-$(find_bin_multi apxs apxs2 2>/dev/null || true)}"
HTTPD_BIN="${APACHE_BIN:-$(find_bin_multi apache2 httpd apachectl 2>/dev/null || true)}"
if [ -z "$HTTPD_BIN" ] && [ -n "$APXS_BIN" ]; then
  HTTPD_BIN=$(resolve_apache_from_apxs "$APXS_BIN" 2>/dev/null || true)
fi
NGINX_BIN="${NGINX_BIN:-$(find_bin_multi nginx 2>/dev/null || true)}"
MODSECURITY_PKG_CONFIG="${MODSECURITY_PKG_CONFIG:-}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-}"
MODSECURITY_INCLUDE_DIR="${MODSECURITY_INCLUDE_DIR:-}"
PKG_CONFIG_BIN="${PKG_CONFIG_BIN:-$(find_bin_multi pkg-config 2>/dev/null || true)}"

if [ -z "$MODSECURITY_PKG_CONFIG" ] && [ -n "$PKG_CONFIG_BIN" ]; then
  for pkg in modsecurity libmodsecurity; do
    if "$PKG_CONFIG_BIN" --exists "$pkg"; then
      MODSECURITY_PKG_CONFIG=$pkg
      break
    fi
  done
fi

if [ -z "$MODSECURITY_LIB_DIR" ]; then
  for libdir in /lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu /usr/local/lib /usr/lib64 /usr/lib; do
    if [ -f "$libdir/libmodsecurity.so" ] || [ -f "$libdir/libmodsecurity.so.3" ]; then
      MODSECURITY_LIB_DIR=$libdir
      break
    fi
  done
fi
if [ -z "$MODSECURITY_INCLUDE_DIR" ]; then
  for incdir in /usr/include /usr/local/include /opt/include; do
    if [ -f "$incdir/modsecurity/modsecurity.h" ]; then
      MODSECURITY_INCLUDE_DIR=$incdir
      break
    fi
  done
fi

modsec_ready=0
if [ -n "$MODSECURITY_PKG_CONFIG" ] || { [ -n "$MODSECURITY_LIB_DIR" ] && [ -n "$MODSECURITY_INCLUDE_DIR" ]; }; then
  modsec_ready=1
fi

echo "smoke-installed: detected apache_bin=${HTTPD_BIN:-<missing>}"
echo "smoke-installed: detected apxs_bin=${APXS_BIN:-<missing>}"
echo "smoke-installed: detected nginx_bin=${NGINX_BIN:-<missing>}"
if [ -n "$MODSECURITY_PKG_CONFIG" ]; then
  echo "smoke-installed: detected modsecurity_pkg_config=$MODSECURITY_PKG_CONFIG"
fi
if [ -n "$MODSECURITY_LIB_DIR" ]; then
  echo "smoke-installed: detected modsecurity_lib_dir=$MODSECURITY_LIB_DIR"
fi
if [ -n "$MODSECURITY_INCLUDE_DIR" ]; then
  echo "smoke-installed: detected modsecurity_include_dir=$MODSECURITY_INCLUDE_DIR"
fi

apache_status=BLOCKED
nginx_status=BLOCKED
if [ -n "$HTTPD_BIN" ] && [ -n "$APXS_BIN" ] && [ "$modsec_ready" -eq 1 ]; then
  apache_status=READY
fi
if [ -n "$NGINX_BIN" ] && [ "$modsec_ready" -eq 1 ]; then
  nginx_status=READY
fi

full_status=BLOCKED
if [ "$apache_status" = "READY" ] && [ "$nginx_status" = "READY" ]; then
  full_status=READY
elif [ "$apache_status" = "READY" ] || [ "$nginx_status" = "READY" ]; then
  full_status=PARTIAL
fi

echo "smoke-installed: readiness apache=$apache_status nginx=$nginx_status full=$full_status"

if [ "$apache_status" = "BLOCKED" ]; then
  if [ -n "$APXS_BIN" ] && [ -z "$HTTPD_BIN" ]; then
    echo "blocked: apache runtime binary not found (apache2/httpd/apachectl), although APXS is present: $APXS_BIN"
  else
    echo "blocked: apache installed smoke missing one of: apache/httpd/apachectl, apxs/apxs2, modsecurity runtime"
  fi
fi
if [ "$nginx_status" = "BLOCKED" ]; then
  echo "blocked: nginx installed smoke missing one of: nginx, modsecurity runtime"
fi
if [ "$modsec_ready" -ne 1 ]; then
  echo "blocked: modsecurity runtime not found via pkg-config or include+lib path"
fi

if [ "$full_status" = "READY" ]; then
  echo "blocked: installed-runtime execution wiring is not yet implemented; readiness is READY but smoke execution remains unavailable"
  exit 77
fi

if [ "$full_status" = "PARTIAL" ]; then
  echo "blocked: partial installed readiness detected; full installed smoke requires both Apache and NGINX readiness"
  exit 77
fi

echo "blocked: installed smoke prerequisites incomplete"
exit 77
