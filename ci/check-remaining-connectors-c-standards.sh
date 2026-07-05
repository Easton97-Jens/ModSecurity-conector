#!/bin/sh
set -eu
profile="${CONNECTOR_C_STD_PROFILE:-c17}"
cc="${CC:-cc}"
case "$profile" in
  c17) std=c17 ;;
  c23) std=c2x ;;
  c2y|future-c)
    if "$cc" -std=c2y -E -x c /dev/null >/dev/null 2>&1; then std=c2y; elif "$cc" -std=gnu2y -E -x c /dev/null >/dev/null 2>&1; then std=gnu2y; else echo "BLOCKED: remaining_connectors_c_standards compiler lacks c2y/gnu2y"; exit 77; fi ;;
  *) std="$profile" ;;
esac
files="common/src/config.c common/src/generic_mapper.c common/src/request_helpers.c common/src/response_helpers.c common/src/request_mapper_contract.c common/src/response_mapper_contract.c common/src/headers.c common/src/block_statuses.c common/src/http_status.c common/src/resource_limits.c common/src/error.c"
for f in $files; do
  [ -f "$f" ] || { echo "BLOCKED: remaining_connectors_c_standards missing headers/source: $f"; exit 77; }
done
tmp="${TMPDIR:-/tmp}/remaining-connectors-standards-$$"
mkdir -p "$tmp"
for f in $files; do
  obj="$tmp/$(echo "$f" | tr '/.' '__').o"
  if ! "$cc" -std="$std" -Wall -Wextra -Werror -Icommon/include -Iconnectors/envoy/src -Iconnectors/traefik/src -Iconnectors/lighttpd/src -c "$f" -o "$obj"; then
    rc=$?
    case "$profile" in c23|c2y|future-c) echo "BLOCKED: remaining_connectors_c_standards compiler/header profile $profile failed for $f"; rm -rf "$tmp"; exit 77;; esac
    rm -rf "$tmp"; exit "$rc"
  fi
done
rm -rf "$tmp"
echo "remaining connector C standard check ok ($profile)"
