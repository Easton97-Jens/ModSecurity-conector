#!/bin/sh
# One named policy boundary/input per admitted behavioral case.
set -eu
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
case "${1:-}" in python-allowed|python-blocked|shell-allowed|shell-blocked) ;; *) echo "FAIL: unknown active runtime-path case" >&2; exit 2 ;; esac
exec "${PYTHON:-python3}" "$SCRIPT_DIR/check-runtime-path-policy.py" --case "$1"
