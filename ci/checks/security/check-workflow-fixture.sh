#!/bin/sh
# Four separately inventoried scanner contract scenarios; never discover fixtures.
set -eu
SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
fixture=${1:?an inventoried fixture identifier is required}
case "$fixture" in
    insecure) path=ci/fixtures/zizmor/insecure.yml; expected=reject ;;
    safe) path=ci/fixtures/zizmor/safe.yml; expected=accept ;;
    permission-unsafe) path=ci/fixtures/workflow-permission-contract/unsafe.yml; expected=reject ;;
    permission-safe) path=ci/fixtures/workflow-permission-contract/safe.yml; expected=accept ;;
    *) echo "FAIL: unknown workflow fixture" >&2; exit 2 ;;
esac
: "${RUNNER_TEMP:?RUNNER_TEMP must select the existing checksum-verified scanner}"
scanner="$RUNNER_TEMP/security-tools/zizmor"
[ -f "$scanner" ] && [ ! -L "$scanner" ] && [ -x "$scanner" ] || {
    echo "FAIL: checksum-verified zizmor executable is unavailable" >&2
    exit 2
}
if "$scanner" --offline "$REPO_ROOT/$path"; then
    observed=accept
else
    observed=reject
fi
[ "$observed" = "$expected" ] || {
    echo "FAIL: scanner fixture result did not match its requirement" >&2
    exit 1
}
printf 'workflow fixture %s: %s
' "$fixture" "$observed"
