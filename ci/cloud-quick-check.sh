#!/bin/sh
set -eu

PYTHON_BIN="${PYTHON:-.venv/bin/python}"
status=0

run_required() {
  label=$1
  shift
  echo "cloud-quick-check: running $label"
  if "$@"; then
    echo "cloud-quick-check: PASS $label"
    return
  fi
  rc=$?
  echo "cloud-quick-check: FAIL $label (exit=$rc)"
  status=1
}

run_required "make setup-dev" make setup-dev
run_required "make lint" make lint
run_required "make generate-test-matrix" make generate-test-matrix
run_required "make check-test-matrix" make check-test-matrix
run_required "make quick-check" make quick-check
run_required "$PYTHON_BIN -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py" \
  "$PYTHON_BIN" -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py
run_required "git diff --check" git diff --check

if [ "$status" -eq 0 ]; then
  echo "cloud-quick-check: PASS (framework/generator only; not runtime compatibility evidence)"
else
  echo "cloud-quick-check: FAIL"
fi

exit "$status"
