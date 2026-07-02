#!/bin/sh
# Common shell helper functions for future connector harnesses.

msconnector_harness_require_absolute() {
    case "$1" in
        /*|\\*) return 0 ;;
        [A-Za-z]:/*|[A-Za-z]:\\*) return 0 ;;
        *) return 1 ;;
    esac
}

msconnector_harness_require_relative_artifact() {
    case "$1" in
        ""|/*|\\*|*../*|*..\\*|[A-Za-z]:/*|[A-Za-z]:\\*) return 1 ;;
        *) return 0 ;;
    esac
}

msconnector_harness_require_under_root() {
    case "$2" in
        "$1"/*|"$1"\\*) return 0 ;;
        *) return 1 ;;
    esac
}

msconnector_harness_status_pass() { printf '%s\n' "PASS: $*"; }
msconnector_harness_status_skip() { printf '%s\n' "SKIPPED: $*"; }
msconnector_harness_status_blocked() { printf '%s\n' "BLOCKED: $*"; }
msconnector_harness_status_fail() { printf '%s\n' "FAIL: $*"; }
