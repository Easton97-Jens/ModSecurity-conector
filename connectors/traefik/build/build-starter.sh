#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd "$SCRIPT_DIR/../../.." && pwd)
BUILD_ROOT="${BUILD_ROOT:-${XDG_STATE_HOME:-${HOME:-/tmp}/.local/state}/ModSecurity-conector-build}"
CC_BIN="${CC:-cc}"
MODE="${1:-build-starter}"
OUT_DIR="$BUILD_ROOT/traefik-build-starter"
METADATA_BIN="$OUT_DIR/traefik_build_starter"
DECISION_BIN="$OUT_DIR/traefik_decision_service_starter"
RESULT_TXT="$OUT_DIR/result.txt"
DECISION_RESULT_TXT="$OUT_DIR/decision-service-result.txt"

case "$BUILD_ROOT" in
    /*) ;;
    *) echo "traefik_build_starter: BUILD_ROOT must be absolute: $BUILD_ROOT"; exit 77 ;;
esac

case "$(CDPATH= cd "$BUILD_ROOT" 2>/dev/null && pwd 2>/dev/null || printf '%s' "$BUILD_ROOT")" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
        echo "traefik_build_starter: BUILD_ROOT must not be inside the checkout: $BUILD_ROOT"
        exit 77
        ;;
esac

command -v "$CC_BIN" >/dev/null 2>&1 || {
    echo "traefik_build_starter: missing C compiler: $CC_BIN"
    exit 77
}

mkdir -p "$OUT_DIR"

build_metadata_starter() {
    "$CC_BIN" -std=c99 -Wall -Wextra -Werror \
        -DMSCONNECTOR_TRAEFIK_BUILD_STARTER_MAIN \
        -I "$REPO_ROOT/common/include" \
        -I "$REPO_ROOT/connectors/traefik" \
        "$REPO_ROOT/common/src/origin.c" \
        "$REPO_ROOT/common/src/capabilities.c" \
        "$REPO_ROOT/connectors/traefik/metadata.c" \
        "$REPO_ROOT/connectors/traefik/src/traefik_build_starter.c" \
        -o "$METADATA_BIN"

    "$METADATA_BIN" > "$RESULT_TXT"
    cat "$RESULT_TXT"
    echo "traefik_build_starter: pass artifact=$METADATA_BIN result=$RESULT_TXT"
}

build_decision_service_starter() {
    "$CC_BIN" -std=c99 -Wall -Wextra -Werror \
        -I "$REPO_ROOT/common/include" \
        -I "$REPO_ROOT/connectors/traefik" \
        -I "$REPO_ROOT/connectors/traefik/src" \
        "$REPO_ROOT/common/src/origin.c" \
        "$REPO_ROOT/common/src/capabilities.c" \
        "$REPO_ROOT/common/src/intervention.c" \
        "$REPO_ROOT/common/src/status.c" \
        "$REPO_ROOT/connectors/traefik/metadata.c" \
        "$REPO_ROOT/connectors/traefik/src/traefik_decision_service.c" \
        "$REPO_ROOT/connectors/traefik/src/traefik_decision_service_main.c" \
        -o "$DECISION_BIN"

    echo "traefik_decision_service_starter: pass artifact=$DECISION_BIN"
}

self_test_decision_service_starter() {
    build_decision_service_starter
    "$DECISION_BIN" --self-test > "$DECISION_RESULT_TXT"
    cat "$DECISION_RESULT_TXT"
    echo "traefik_decision_service_self_test: pass result=$DECISION_RESULT_TXT"
}

case "$MODE" in
    build-starter)
        build_metadata_starter
        ;;
    build-decision-service|build-forwardauth-starter)
        build_decision_service_starter
        ;;
    self-test|self-test-decision-service|self-test-forwardauth)
        self_test_decision_service_starter
        ;;
    clean)
        rm -rf "$OUT_DIR"
        echo "traefik_build_starter: clean output=$OUT_DIR"
        ;;
    *)
        echo "usage: $0 [build-starter|build-decision-service|build-forwardauth-starter|self-test|self-test-decision-service|self-test-forwardauth|clean]"
        exit 2
        ;;
esac
