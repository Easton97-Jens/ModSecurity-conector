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

# Record the complete incoming state before clearing it.  A caller may carry a
# Framework-approved tuple across a Parent/Child boundary, but it is accepted
# only after this process independently resolves the checked-out Framework
# tuple below and compares all four values byte-for-byte.
if [ "${APR_UTIL_VERSION+x}" = x ]; then
    ci_apr_util_input_version_set=1
    ci_apr_util_input_version=$APR_UTIL_VERSION
else
    ci_apr_util_input_version_set=0
    ci_apr_util_input_version=
fi
if [ "${APR_UTIL_SOURCE_URL+x}" = x ]; then
    ci_apr_util_input_source_url_set=1
    ci_apr_util_input_source_url=$APR_UTIL_SOURCE_URL
else
    ci_apr_util_input_source_url_set=0
    ci_apr_util_input_source_url=
fi
if [ "${APR_UTIL_SHA256+x}" = x ]; then
    ci_apr_util_input_sha256_set=1
    ci_apr_util_input_sha256=$APR_UTIL_SHA256
else
    ci_apr_util_input_sha256_set=0
    ci_apr_util_input_sha256=
fi
if [ "${APR_UTIL_SHA256_URL+x}" = x ]; then
    ci_apr_util_input_sha256_url_set=1
    ci_apr_util_input_sha256_url=$APR_UTIL_SHA256_URL
else
    ci_apr_util_input_sha256_url_set=0
    ci_apr_util_input_sha256_url=
fi

unset APR_UTIL_VERSION APR_UTIL_SOURCE_URL APR_UTIL_SHA256 APR_UTIL_SHA256_URL

export FRAMEWORK_ROOT CONNECTOR_ROOT

if [ ! -f "$FRAMEWORK_ROOT/ci/lib/common.sh" ]; then
    printf '%s\n' "missing Framework common.sh: $FRAMEWORK_ROOT/ci/lib/common.sh" >&2
    exit 77
fi

# The Framework guard establishes the canonical tuple and validates its HTTPS
# inputs before Parent can use any archive or cache path.
# shellcheck disable=SC1091
. "$FRAMEWORK_ROOT/ci/lib/common.sh"
ci_require_apr_util_pinned_provenance || exit 77
ci_validate_https_runtime_url_config || exit 77

case "$ci_apr_util_input_version_set:$ci_apr_util_input_source_url_set:$ci_apr_util_input_sha256_set:$ci_apr_util_input_sha256_url_set" in
    0:0:0:0)
        ;;
    1:1:1:1)
        if [ -z "$ci_apr_util_input_version" ] \
            || [ -z "$ci_apr_util_input_source_url" ] \
            || [ -z "$ci_apr_util_input_sha256" ] \
            || [ -z "$ci_apr_util_input_sha256_url" ] \
            || [ "$ci_apr_util_input_version" != "$APR_UTIL_VERSION" ] \
            || [ "$ci_apr_util_input_source_url" != "$APR_UTIL_SOURCE_URL" ] \
            || [ "$ci_apr_util_input_sha256" != "$APR_UTIL_SHA256" ] \
            || [ "$ci_apr_util_input_sha256_url" != "$APR_UTIL_SHA256_URL" ]; then
            printf '%s\n' 'APR-util inherited tuple is not the canonical Framework tuple' >&2
            exit 77
        fi
        ;;
    *)
        printf '%s\n' 'APR-util inherited tuple must set all four canonical fields or none' >&2
        exit 77
        ;;
esac

# Each value is structurally constrained by the Framework guard and Parent
# revalidates it before use.  Emit assignments only; callers must never eval
# this output.
shell_quote() {
    if [ "$#" -ne 1 ]; then
        return 64
    fi
    ci_apr_util_shell_quote_value=$1
    printf "'"
    printf '%s' "$ci_apr_util_shell_quote_value" | /usr/bin/sed "s/'/'\"'\"'/g"
    printf "'"
}

printf 'APR_UTIL_VERSION='; shell_quote "$APR_UTIL_VERSION"; printf '\n'
printf 'APR_UTIL_SOURCE_URL='; shell_quote "$APR_UTIL_SOURCE_URL"; printf '\n'
printf 'APR_UTIL_SHA256='; shell_quote "$APR_UTIL_SHA256"; printf '\n'
printf 'APR_UTIL_SHA256_URL='; shell_quote "$APR_UTIL_SHA256_URL"; printf '\n'
