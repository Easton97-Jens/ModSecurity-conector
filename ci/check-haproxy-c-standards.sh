#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
CC_BIN=${CC:-cc}
PROFILE=${HAPROXY_C_STD_PROFILE:-all}
OUT=${BUILD_ROOT:-${TMPDIR:-/tmp}/modsecurity-conector-haproxy-c-standards}/haproxy-c-standards
mkdir -p "$OUT"
command -v "$CC_BIN" >/dev/null 2>&1 || { echo "BLOCKED: haproxy_c_standards missing C compiler: $CC_BIN"; exit 77; }
HAPROXY_SOURCE_DIR="${HAPROXY_SOURCE_DIR:-${HAPROXY_SRC:-${MODSECURITY_HAPROXY_SOURCE_DIR:-}}}"
HAPROXY_INCLUDE_DIR="${HAPROXY_INCLUDE_DIR:-${HAPROXY_INCLUDE:-}}"
incs="-I$ROOT/common/include -I$ROOT/connectors/haproxy/src"
found_haproxy=0
if [ -n "$HAPROXY_INCLUDE_DIR" ] && [ -d "$HAPROXY_INCLUDE_DIR" ]; then incs="$incs -I$HAPROXY_INCLUDE_DIR"; found_haproxy=1; fi
if [ -n "$HAPROXY_SOURCE_DIR" ] && [ -d "$HAPROXY_SOURCE_DIR" ]; then incs="$incs -I$HAPROXY_SOURCE_DIR/include -I$HAPROXY_SOURCE_DIR/src"; found_haproxy=1; fi
for d in /usr/include/haproxy /usr/local/include/haproxy; do [ -d "$d" ] && { incs="$incs -I$d"; found_haproxy=1; }; done
[ "$found_haproxy" = 1 ] || { echo "BLOCKED: haproxy_c_standards missing haproxy headers/source"; exit 77; }
MODSECURITY_INCLUDE="${MODSECURITY_INCLUDE:-${MODSECURITY_INCLUDE_DIR:-${MODSECURITY_INC:-${V3INCLUDE:-}}}}"
MODSECURITY_INCLUDE_FLAG=
found_modsec=0
if [ -n "$MODSECURITY_INCLUDE" ]; then
  for include_item in $MODSECURITY_INCLUDE; do
    case "$include_item" in
      -I*) MODSECURITY_INCLUDE_FLAG="$include_item"; MODSECURITY_INCLUDE_PATH=${include_item#-I} ;;
      "") MODSECURITY_INCLUDE_FLAG=""; MODSECURITY_INCLUDE_PATH="" ;;
      *) MODSECURITY_INCLUDE_FLAG="-I$include_item"; MODSECURITY_INCLUDE_PATH="$include_item" ;;
    esac
    if [ -n "$MODSECURITY_INCLUDE_PATH" ] && [ -f "$MODSECURITY_INCLUDE_PATH/modsecurity/modsecurity.h" ]; then incs="$incs $MODSECURITY_INCLUDE_FLAG"; found_modsec=1; fi
  done
fi
if [ "$found_modsec" != 1 ]; then
  for d in /usr/include /usr/local/include; do [ -f "$d/modsecurity/modsecurity.h" ] && { incs="$incs -I$d"; found_modsec=1; break; }; done
fi
[ "$found_modsec" = 1 ] || { echo "BLOCKED: haproxy_c_standards missing libmodsecurity headers"; exit 77; }
compile_profile() {
  prof=$1
  case "$prof" in
    c17) std='-std=c17' ;;
    c23) std=$(python3 "$ROOT/ci/detect-c-standard.py" --profile c23 --compiler "$CC_BIN") || { rc=$?; [ "$rc" = 77 ] && { echo "SKIPPED: optional C23 check unsupported"; return 0; }; return "$rc"; } ;;
    c2y) std=$(python3 "$ROOT/ci/detect-c-standard.py" --profile c2y --compiler "$CC_BIN") || { rc=$?; [ "$rc" = 77 ] && { echo "SKIPPED: optional future-C check unsupported"; return 0; }; return "$rc"; } ;;
    *) echo "unknown profile $prof"; return 2 ;;
  esac
  files=""
  for dir in connectors/haproxy/src connectors/haproxy/runtime connectors/haproxy/spoa connectors/haproxy/harness; do
    if [ -d "$ROOT/$dir" ]; then
      for f in "$ROOT"/$dir/*.c; do [ -f "$f" ] && files="$files ${f#$ROOT/}"; done
    fi
  done
  files="$files common/src/config.c common/src/config_parser.c common/src/directive_spec.c common/src/directive_adapter.c common/src/request_helpers.c common/src/response_helpers.c common/src/request_mapper_contract.c common/src/response_mapper_contract.c common/src/headers.c common/src/event.c common/src/event_jsonl.c common/src/json_escape.c common/src/rule_id.c common/src/log_sanitize.c common/src/redaction.c common/src/resource_limits.c common/src/dos_guard.c common/src/error.c common/src/status.c common/src/body_policy.c common/src/crs.c common/src/transaction_state.c common/src/decision.c common/src/decision_action.c common/src/late_intervention.c common/src/flow_guard.c common/src/integrity_event.c common/src/rule_loader.c common/src/rule_merge.c common/src/test_result.c common/src/test_result_json.c common/src/artifacts.c common/src/artifact_layout.c common/src/block_statuses.c common/src/http_status.c common/src/path_policy.c common/src/intervention.c common/src/rule_error.c common/src/rule_event.c"
  for f in $files; do [ -f "$ROOT/$f" ] || continue; obj="$OUT/$(echo "$prof-$f" | tr '/.' '__').o"; "$CC_BIN" $std -Wall -Wextra -Werror $incs -c "$ROOT/$f" -o "$obj"; done
  echo "PASS: haproxy_c_standards $prof compile completed"
}
case "$PROFILE" in c17|c23|c2y) compile_profile "$PROFILE";; all) compile_profile c17; compile_profile c23; compile_profile c2y;; *) echo "unknown HAPROXY_C_STD_PROFILE=$PROFILE"; exit 2;; esac
