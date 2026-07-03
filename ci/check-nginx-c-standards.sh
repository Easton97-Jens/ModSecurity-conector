#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
CC_BIN=${CC:-cc}
PROFILE=${NGINX_C_STD_PROFILE:-all}
OUT=${BUILD_ROOT:-${TMPDIR:-/tmp}/modsecurity-conector-nginx-c-standards}/nginx-c-standards
mkdir -p "$OUT"
command -v "$CC_BIN" >/dev/null 2>&1 || { echo "BLOCKED: nginx_c_standards missing C compiler: $CC_BIN"; exit 77; }
NGINX_SOURCE_DIR=${NGINX_SOURCE_DIR:-${NGINX_SRC:-${MODSECURITY_NGINX_SOURCE_DIR:-}}}
NGINX_INCLUDE_DIR=${NGINX_INCLUDE_DIR:-${NGINX_INCLUDE:-}}
incs="-I$ROOT/common/include -I$ROOT/connectors/nginx/src"
found_nginx=0
if [ -n "$NGINX_INCLUDE_DIR" ] && [ -d "$NGINX_INCLUDE_DIR" ]; then incs="$incs -I$NGINX_INCLUDE_DIR"; found_nginx=1; fi
if [ -n "$NGINX_SOURCE_DIR" ] && [ -d "$NGINX_SOURCE_DIR" ]; then
  incs="$incs -I$NGINX_SOURCE_DIR/src/core -I$NGINX_SOURCE_DIR/src/http -I$NGINX_SOURCE_DIR/src/event -I$NGINX_SOURCE_DIR/src/os/unix -I$NGINX_SOURCE_DIR/objs"; found_nginx=1
fi
for d in /usr/include/nginx /usr/local/include/nginx; do [ -d "$d" ] && { incs="$incs -I$d"; found_nginx=1; }; done
[ "$found_nginx" = 1 ] || { echo "BLOCKED: nginx_c_standards missing nginx headers/source"; exit 77; }
found_modsec=0
for d in ${MODSECURITY_INCLUDE:-} ${V3INCLUDE:-} /usr/include /usr/local/include; do
  [ -n "$d" ] && [ -f "$d/modsecurity/modsecurity.h" ] && { incs="$incs -I$d"; found_modsec=1; break; }
done
[ "$found_modsec" = 1 ] || { echo "BLOCKED: nginx_c_standards missing libmodsecurity headers"; exit 77; }
compile_profile() {
  prof=$1
  case "$prof" in
    c17) std='-std=c17' ;;
    c23) std=$(python3 "$ROOT/ci/detect-c-standard.py" --profile c23 --compiler "$CC_BIN") || { rc=$?; [ "$rc" = 77 ] && { echo "SKIPPED: optional C23 check unsupported"; return 0; }; return "$rc"; } ;;
    c2y) std=$(python3 "$ROOT/ci/detect-c-standard.py" --profile c2y --compiler "$CC_BIN") || { rc=$?; [ "$rc" = 77 ] && { echo "SKIPPED: optional future-C check unsupported"; return 0; }; return "$rc"; } ;;
    *) echo "unknown profile $prof"; return 2 ;;
  esac
  files="connectors/nginx/src/ngx_http_modsecurity_module.c connectors/nginx/src/ngx_http_modsecurity_access.c connectors/nginx/src/ngx_http_modsecurity_header_filter.c connectors/nginx/src/ngx_http_modsecurity_body_filter.c connectors/nginx/src/ngx_http_modsecurity_mapper.c common/src/config.c common/src/config_parser.c common/src/directive_spec.c common/src/directive_adapter.c common/src/request_helpers.c common/src/response_helpers.c common/src/request_mapper_contract.c common/src/response_mapper_contract.c common/src/headers.c common/src/event.c common/src/transaction_state.c common/src/event_jsonl.c common/src/json_escape.c common/src/rule_id.c common/src/log_sanitize.c common/src/redaction.c common/src/resource_limits.c common/src/dos_guard.c common/src/error.c common/src/status.c common/src/body_policy.c common/src/crs.c common/src/block_statuses.c common/src/http_status.c"
  for f in $files; do [ -f "$ROOT/$f" ] || continue; obj="$OUT/$(echo "$prof-$f" | tr '/.' '__').o"; "$CC_BIN" $std -Wall -Wextra -Werror $incs -c "$ROOT/$f" -o "$obj"; done
  echo "PASS: nginx_c_standards $prof compile completed"
}
case "$PROFILE" in c17|c23|c2y) compile_profile "$PROFILE";; all) compile_profile c17; compile_profile c23; compile_profile c2y;; *) echo "unknown NGINX_C_STD_PROFILE=$PROFILE"; exit 2;; esac
