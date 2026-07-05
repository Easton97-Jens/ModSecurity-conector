#!/bin/sh
set -eu

profile="${CONNECTOR_C_STD_PROFILE:-c17}"
cc="${CC:-cc}"
repo_root=$(CDPATH= cd "$(dirname "$0")/.." && pwd)
case "$profile" in
  c17) std=c17 ;;
  c23) std=c2x ;;
  c2y|future-c)
    if "$cc" -std=c2y -E -x c /dev/null >/dev/null 2>&1; then
      std=c2y
    elif "$cc" -std=gnu2y -E -x c /dev/null >/dev/null 2>&1; then
      std=gnu2y
    else
      echo "BLOCKED: remaining_connectors_c_standards compiler lacks c2y/gnu2y"
      exit 77
    fi
    ;;
  *)
    echo "ERROR: unknown remaining connector C standard profile: $profile" >&2
    exit 2
    ;;
esac

files="common/src/config.c common/src/generic_mapper.c common/src/request_helpers.c common/src/response_helpers.c common/src/request_mapper_contract.c common/src/response_mapper_contract.c common/src/headers.c common/src/block_statuses.c common/src/http_status.c common/src/resource_limits.c common/src/error.c"
headers="connectors/envoy/src/envoy_modsecurity_mapper.h connectors/traefik/src/traefik_modsecurity_mapper.h connectors/lighttpd/src/lighttpd_modsecurity_mapper.h"
for f in $files $headers; do
  [ -f "$repo_root/$f" ] || { echo "BLOCKED: remaining_connectors_c_standards missing headers/source: $f"; exit 77; }
done
tmp="${TMPDIR:-/tmp}/remaining-connectors-standards-$$"
mkdir -p "$tmp"
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT HUP INT TERM
compile_one() {
  src=$1
  obj=$2
  set +e
  "$cc" -std="$std" -Wall -Wextra -Werror -I"$repo_root/common/include" -I"$repo_root" -I"$repo_root/connectors/envoy/src" -I"$repo_root/connectors/traefik/src" -I"$repo_root/connectors/lighttpd/src" -c "$src" -o "$obj" >"$obj.out" 2>"$obj.err"
  rc=$?
  set -e
  if [ "$rc" -eq 0 ]; then
    return 0
  fi
  cat "$obj.err" >&2
  case "$profile" in
    c23|c2y|future-c)
      echo "BLOCKED: remaining_connectors_c_standards compiler/header profile $profile failed for $src"
      return 77
      ;;
  esac
  echo "FAIL: remaining connectors C standard check failed ($profile): $src" >&2
  return "$rc"
}
for f in $files; do
  compile_one "$repo_root/$f" "$tmp/$(echo "$f" | tr '/.' '__').o"
done
for header in $headers; do
  smoke="$tmp/$(basename "$header").smoke.c"
  obj="$tmp/$(basename "$header").smoke.o"
  cat > "$smoke" <<EOF
#include "$repo_root/$header"
int main(void) { return 0; }
EOF
  compile_one "$smoke" "$obj"
done
echo "PASS: remaining connectors C standard check ($profile)"
