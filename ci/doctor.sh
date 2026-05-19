#!/bin/sh
set -eu

REPO_ROOT=$(CDPATH= cd "$(dirname "$0")/.." && pwd)
PYTHON_BIN="${PYTHON:-python3}"
BUILD_ROOT="${BUILD_ROOT:-/src/ModSecurity-conector-build}"
SOURCE_ROOT="${SOURCE_ROOT:-$BUILD_ROOT/sources}"
status=0
DOCTOR_MODE="${DOCTOR_MODE:-full}"

say() { echo "doctor: $*"; }
blocked() { echo "BLOCKED: $*"; status=77; }
warn() { echo "WARN: $*"; }
check_cmd() {
  cmd_name=$1
  if command -v "$cmd_name" >/dev/null 2>&1; then
    say "toolchain: $cmd_name ok"
  else
    blocked "toolchain missing: $cmd_name"
  fi
}

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

show_component() {
  label=$1
  value=$2
  if [ -n "$value" ]; then
    say "runtime: $label -> $value"
  else
    say "runtime: $label -> not found"
  fi
}

say "python interpreter: $PYTHON_BIN"
"$PYTHON_BIN" --version || blocked "python executable failed: $PYTHON_BIN"
if [ -x "$REPO_ROOT/.venv/bin/python" ]; then say "venv: detected $REPO_ROOT/.venv/bin/python"; else blocked "venv missing (.venv/bin/python); run make setup-dev"; fi
if ! "$PYTHON_BIN" "$REPO_ROOT/ci/check-python-deps.py"; then blocked "missing Python dependencies for selected interpreter"; fi

for tool in git make gcc autoconf automake libtool pkg-config; do check_cmd "$tool"; done
if command -v clang >/dev/null 2>&1; then say "toolchain: clang ok (optional)"; else say "toolchain: clang missing (optional)"; fi

APXS_BIN="${APXS_BIN:-$(find_bin_multi apxs apxs2 2>/dev/null || true)}"
APACHE_BIN="${APACHE_BIN:-$(find_bin_multi apache2 httpd apachectl 2>/dev/null || true)}"
if [ -z "$APACHE_BIN" ] && [ -n "$APXS_BIN" ]; then
  APACHE_BIN=$(resolve_apache_from_apxs "$APXS_BIN" 2>/dev/null || true)
fi
NGINX_BIN="${NGINX_BIN:-$(find_bin_multi nginx 2>/dev/null || true)}"
MODSECURITY_PKG_CONFIG="${MODSECURITY_PKG_CONFIG:-}"
MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-}"
MODSECURITY_INCLUDE_DIR="${MODSECURITY_INCLUDE_DIR:-}"

show_component apache_bin "$APACHE_BIN"
show_component apxs_bin "$APXS_BIN"
show_component nginx_bin "$NGINX_BIN"

if [ -z "$MODSECURITY_PKG_CONFIG" ] && command -v pkg-config >/dev/null 2>&1; then
  for pkg in modsecurity libmodsecurity; do
    if pkg-config --exists "$pkg"; then
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

if [ -n "$MODSECURITY_PKG_CONFIG" ]; then
  say "runtime: modsecurity pkg-config -> $MODSECURITY_PKG_CONFIG"
else
  say "runtime: modsecurity pkg-config -> not found"
fi
show_component modsecurity_lib_dir "$MODSECURITY_LIB_DIR"
show_component modsecurity_include_dir "$MODSECURITY_INCLUDE_DIR"

say "build root: $BUILD_ROOT"
mkdir -p "$BUILD_ROOT" || blocked "cannot create BUILD_ROOT: $BUILD_ROOT"
say "source root: $SOURCE_ROOT"

if detected=$(BUILD_ROOT="$BUILD_ROOT" MODSECURITY_V3_SOURCE_DIR="${MODSECURITY_V3_SOURCE_DIR:-}" sh "$REPO_ROOT/ci/find-modsecurity-v3.sh"); then
  say "detected MODSECURITY_V3_SOURCE_DIR=$detected"
else
  if [ "$DOCTOR_MODE" = "quick" ]; then
    warn "missing ModSecurity_V3 source tree (quick mode)"
  else
    blocked "missing ModSecurity_V3 source tree"
  fi
  echo "Suggested fixes:"
  echo "- export MODSECURITY_V3_SOURCE_DIR=/path/to/ModSecurity_V3"
  echo "- OR run: make fetch-deps"
fi

if command -v git >/dev/null 2>&1; then
  if git ls-remote --heads https://github.com/owasp-modsecurity/ModSecurity.git >/dev/null 2>&1; then
    say "github reachability: ok"
  else
    blocked "github unreachable for ModSecurity fetch"
  fi
fi

if [ -d "$SOURCE_ROOT/ModSecurity_V3" ]; then
  say "sources: BUILD_ROOT-aligned ModSecurity_V3 present"
else
  if [ "$DOCTOR_MODE" = "quick" ]; then
    warn "sources missing under BUILD_ROOT (quick mode): $SOURCE_ROOT/ModSecurity_V3"
  else
    blocked "sources missing under BUILD_ROOT: $SOURCE_ROOT/ModSecurity_V3"
  fi
fi

apache_ready=BLOCKED
nginx_ready=BLOCKED
full_ready=BLOCKED
[ -n "$APACHE_BIN" ] && [ -n "$APXS_BIN" ] && apache_ready=READY
[ -n "$NGINX_BIN" ] && nginx_ready=READY
if [ "$apache_ready" = "READY" ] && [ "$nginx_ready" = "READY" ]; then
  full_ready=READY
elif [ "$apache_ready" = "READY" ] || [ "$nginx_ready" = "READY" ]; then
  full_ready=PARTIAL
fi
if [ -z "$MODSECURITY_PKG_CONFIG" ] && { [ -z "$MODSECURITY_LIB_DIR" ] || [ -z "$MODSECURITY_INCLUDE_DIR" ]; }; then
  apache_ready=BLOCKED
  nginx_ready=BLOCKED
  full_ready=BLOCKED
fi

echo "INSTALLED COMPONENTS:"
if [ -n "$APACHE_BIN" ]; then echo "  Apache runtime: FOUND ($APACHE_BIN)"; else echo "  Apache runtime: NOT FOUND"; fi
if [ -n "$APXS_BIN" ]; then echo "  APXS (Apache dev): FOUND ($APXS_BIN)"; else echo "  APXS (Apache dev): NOT FOUND"; fi
if [ -n "$NGINX_BIN" ]; then echo "  NGINX: FOUND ($NGINX_BIN)"; else echo "  NGINX: NOT FOUND"; fi
if [ -n "$MODSECURITY_PKG_CONFIG" ]; then
  echo "  libmodsecurity: FOUND (pkg-config:$MODSECURITY_PKG_CONFIG)"
elif [ -n "$MODSECURITY_LIB_DIR" ] && [ -n "$MODSECURITY_INCLUDE_DIR" ]; then
  echo "  libmodsecurity: FOUND (lib:$MODSECURITY_LIB_DIR include:$MODSECURITY_INCLUDE_DIR)"
else
  echo "  libmodsecurity: NOT FOUND"
fi
if [ -z "$APACHE_BIN" ] && [ -n "$APXS_BIN" ]; then
  echo "  note: apache2-dev appears installed without a detected Apache runtime binary"
fi
if [ -z "$APACHE_BIN" ] && [ -n "$APXS_BIN" ]; then
  echo "  hint: Debian/Ubuntu runtime package: apt-get install apache2 or apache2-bin"
fi

echo "SMOKE-INSTALLED READINESS:"
echo "  Apache installed smoke: $apache_ready"
echo "  NGINX installed smoke: $nginx_ready"
echo "  Full installed smoke: $full_ready"

if [ "$status" -eq 0 ]; then
  say "smoke readiness: prerequisites look available; run make smoke-all"
else
  if [ "$DOCTOR_MODE" = "quick" ]; then
    echo "doctor: quick mode completed with runtime warnings"
  else
    echo "doctor: smoke readiness BLOCKED"
  fi
fi
APACHE_CACHED_BIN="$BUILD_ROOT/apache-runtime/httpd/bin/httpd"
NGINX_CACHED_BIN="$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx"
if [ -x "$APACHE_CACHED_BIN" ]; then say "cache: cached apache artifacts present"; else say "cache: cached apache artifacts missing"; fi
if [ -x "$NGINX_CACHED_BIN" ]; then say "cache: cached nginx artifacts present"; else say "cache: cached nginx artifacts missing"; fi

exit "$status"
