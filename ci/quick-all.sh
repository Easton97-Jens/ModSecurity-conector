#!/bin/sh
set -eu

PYTHON_BIN="${PYTHON:-python3}"

status=0

run_pass_fail() {
  label=$1
  shift
  echo "quick-all: running $label"
  if "$@"; then
    echo "quick-all: PASS $label"
    return 0
  fi
  rc=$?
  echo "quick-all: FAIL $label (exit=$rc)"
  status=1
  return 0
}

run_blockable() {
  label=$1
  shift
  echo "quick-all: running $label"
  set +e
  "$@"
  rc=$?
  set -e
  if [ "$rc" -eq 0 ]; then
    echo "quick-all: PASS $label"
    return 0
  fi
  if [ "$rc" -eq 77 ]; then
    echo "quick-all: BLOCKED $label (exit=77)"
    [ "$status" -eq 1 ] || status=77
    return 0
  fi
  echo "quick-all: FAIL $label (exit=$rc)"
  status=1
  return 0
}

run_pass_fail "make lint" make lint
run_blockable "make doctor-quick" make doctor-quick
run_pass_fail "make quick-check" make quick-check
run_blockable "ci/smoke-cached.sh" sh ci/smoke-cached.sh
run_blockable "ci/smoke-installed.sh" sh ci/smoke-installed.sh
run_pass_fail "$PYTHON_BIN -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py" \
  "$PYTHON_BIN" -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py
run_pass_fail "git diff --check" git diff --check

if [ "$status" -eq 0 ]; then
  echo "quick-all: QUICK PASS"
elif [ "$status" -eq 77 ]; then
  echo "quick-all: QUICK BLOCKED"
else
  echo "quick-all: QUICK FAIL"
fi

exit "$status"
