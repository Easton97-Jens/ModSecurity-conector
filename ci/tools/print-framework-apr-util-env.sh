#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
    printf '%s\n' 'usage: print-framework-apr-util-env.sh FRAMEWORK_ROOT CONNECTOR_ROOT' >&2
    exit 64
fi

FRAMEWORK_ROOT=$1
CONNECTOR_ROOT=$2
PATH=/usr/bin:/bin
export PATH

# Parent callers must not supply even a matching APR-util tuple.  The
# Framework owns these values; accepting inherited values would make that
# ownership unverifiable.
for ci_apr_util_key in APR_UTIL_VERSION APR_UTIL_SOURCE_URL APR_UTIL_SHA256 APR_UTIL_SHA256_URL; do
    if printenv "$ci_apr_util_key" >/dev/null 2>&1; then
        printf '%s\n' "APR-util inherited Parent override is not permitted: $ci_apr_util_key" >&2
        exit 77
    fi
done

export FRAMEWORK_ROOT CONNECTOR_ROOT

if [ ! -f "$FRAMEWORK_ROOT/ci/lib/common.sh" ]; then
    printf '%s\n' "missing Framework common.sh: $FRAMEWORK_ROOT/ci/lib/common.sh" >&2
    exit 77
fi

# The Framework guard establishes the canonical tuple and validates its HTTPS
# inputs before Parent can use any archive or cache path.
# shellcheck disable=SC1091
. "$FRAMEWORK_ROOT/ci/lib/common.sh"
ci_require_apr_util_pinned_provenance
ci_validate_https_runtime_url_config

# Each value is structurally constrained by the Framework guard and Parent
# revalidates it before use.  Emit assignments only; callers must never eval
# this output.
shell_quote() {
    printf "'"
    printf '%s' "$1" | /usr/bin/sed "s/'/'\"'\"'/g"
    printf "'"
}

printf 'APR_UTIL_VERSION='; shell_quote "$APR_UTIL_VERSION"; printf '\n'
printf 'APR_UTIL_SOURCE_URL='; shell_quote "$APR_UTIL_SOURCE_URL"; printf '\n'
printf 'APR_UTIL_SHA256='; shell_quote "$APR_UTIL_SHA256"; printf '\n'
printf 'APR_UTIL_SHA256_URL='; shell_quote "$APR_UTIL_SHA256_URL"; printf '\n'
