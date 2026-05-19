#!/bin/sh
set -eu

PYTHON_BIN="${PYTHON:-python3}"
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

run_blockable_cmd() {
  label=$1
  shift
  echo "cloud-quick-check: running $label"
  set +e
  "$@"
  rc=$?
  set -e
  if [ "$rc" -eq 0 ]; then
    echo "cloud-quick-check: PASS $label"
    return
  fi
  if [ "$rc" -eq 77 ]; then
    echo "cloud-quick-check: BLOCKED $label (exit=77)"
    return
  fi
  echo "cloud-quick-check: FAIL $label (exit=$rc)"
  status=1
}

run_blockable_make() {
  target=$1
  probe_cmd=$2
  echo "cloud-quick-check: running make $target"
  set +e
  make "$target"
  rc=$?
  set -e
  if [ "$rc" -eq 0 ]; then
    echo "cloud-quick-check: PASS make $target"
    return
  fi
  # GNU make returns 2 when a recipe exits non-zero; probe direct command for 77
  if [ "$rc" -eq 2 ]; then
    set +e
    sh -c "$probe_cmd" >/dev/null 2>&1
    probe_rc=$?
    set -e
    if [ "$probe_rc" -eq 77 ]; then
      echo "cloud-quick-check: BLOCKED make $target (wrapped exit=2, probe exit=77)"
      return
    fi
  fi
  if [ "$rc" -eq 77 ]; then
    echo "cloud-quick-check: BLOCKED make $target (exit=77)"
    return
  fi
  echo "cloud-quick-check: FAIL make $target (exit=$rc)"
  status=1
}

run_required "make setup-dev" make setup-dev
run_required "make lint" make lint
run_required "make doctor-quick" make doctor-quick
run_required "make quick-check" make quick-check
run_blockable_make "installed-readiness" "sh ci/smoke-installed.sh"
run_blockable_make "quick-all" "sh ci/quick-all.sh"
run_required "$PYTHON_BIN -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py" \
  "$PYTHON_BIN" -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py
run_required "git diff --check" git diff --check

if [ "$status" -eq 0 ]; then
  echo "cloud-quick-check: PASS (framework green; runtime probes may be BLOCKED)"
else
  echo "cloud-quick-check: FAIL"
fi

exit "$status"
