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
check_cmd() { cmd=$1; if command -v "$cmd" >/dev/null 2>&1; then say "toolchain: $cmd ok"; else blocked "toolchain missing: $cmd"; fi; }

find_bin() {
  command -v "$1" 2>/dev/null || true
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


APACHE_BIN=${APACHE_BIN:-$(find_bin httpd)}
[ -n "$APACHE_BIN" ] || APACHE_BIN=${APACHE_BIN:-$(find_bin apache2)}
APXS_BIN=${APXS_BIN:-$(find_bin apxs)}
[ -n "$APXS_BIN" ] || APXS_BIN=${APXS_BIN:-$(find_bin apxs2)}
NGINX_BIN=${NGINX_BIN:-$(find_bin nginx)}
show_component apache_bin "$APACHE_BIN"
show_component apxs_bin "$APXS_BIN"
show_component nginx_bin "$NGINX_BIN"
if command -v pkg-config >/dev/null 2>&1; then
  if pkg-config --exists libmodsecurity; then
    say "runtime: pkg-config libmodsecurity -> available"
  else
    say "runtime: pkg-config libmodsecurity -> not found"
  fi
fi

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
  echo "Suggested fixes:"; echo "- export MODSECURITY_V3_SOURCE_DIR=/path/to/ModSecurity_V3"; echo "- OR run: make fetch-deps"
fi

if command -v git >/dev/null 2>&1; then
  if git ls-remote --heads https://github.com/owasp-modsecurity/ModSecurity.git >/dev/null 2>&1; then
    say "github reachability: ok"
  else
    blocked "github unreachable for ModSecurity fetch"
  fi
fi

if [ -d "$SOURCE_ROOT/ModSecurity_V3" ]; then say "sources: BUILD_ROOT-aligned ModSecurity_V3 present"; else
  if [ "$DOCTOR_MODE" = "quick" ]; then
    warn "sources missing under BUILD_ROOT (quick mode): $SOURCE_ROOT/ModSecurity_V3"
  else
    blocked "sources missing under BUILD_ROOT: $SOURCE_ROOT/ModSecurity_V3"
  fi
fi

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
