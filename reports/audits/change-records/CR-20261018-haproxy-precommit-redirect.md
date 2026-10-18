# Change Record: CR-20261018-haproxy-precommit-redirect

**Language:** English | [Deutsch](CR-20261018-haproxy-precommit-redirect.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-precommit-redirect |
| Date (UTC) | 2026-10-18 |
| Base revision | `38edee9431192ea8b691a46d37601ecea0915142` |

## Motivation and problem statement

The original Framework P3 rule1100202 requires HTTP302 and
`Location: https://no-crs.invalid/phase3-redirect`. The HTX filter instead
classified redirects as unsupported and replied503. Preserve the original
oracle; apply valid P1/P2/P3 redirects before commit, finish/free once, and
retain fail-closed handling for invalid decisions and technical failures.

## Acceptance criteria

Preserve original302/Location before commit directly and through the companion; own the complete URL, free the native transaction once and fail closed for invalid or technical results. Independent integrated host retests remain required.

## Implementation decision and rationale

The binding owns the complete native URL before intervention cleanup and rejects
overflow, raw control characters and DEL. A small HAProxy-local inline validator
is shared by capture and the HTX caller. The filter uses pinned HAProxy3.2.25
`http_apply_redirect_rule` with literal `REDIRECT_TYPE_LOCATION`, allowed original
status301/302/303/307/308 and `FROM_REQ` only for P1/P2. It finalizes and disables
the native context before the synchronous reply API; only return1 is success.

The companion copies its result-owned URL before reset, performs the host reply,
then records REDIRECT OUTCOME with302 before RELEASE. A failed acknowledgement
after the actual reply aborts without a second HTTP response. Common and MRC1
contracts and layouts are unchanged. Changed code is the HAProxy binding/header,
HTX filter and overlay check; regression files cover redirect capture, native
host callers and existing fail-closed contracts. The HAProxy README pair and this
Change Record pair document the supported path and evidence limits.

## Changed files

HAProxy binding/header, HTX filter, overlay check, new redirect contract test and existing I10 host-caller/security/payload contract tests; HAProxy README pair and this Change Record pair. No Common/MRC1 change.

## Commands executed

RTK-wrapped compiled old-source regressions fail the302 reply and overlong-URL
rejection assertions. Actual libModSecurity3.0.14 canonical P3 direct/companion
and P1/P2 controls passed. Capture sanitizer and three mutation controls passed;
the native host matrix retained19 existing, six Strict and seven new redirect
mutations. Six sanitizer/physical-event/owner checks, five prior request-scope/
version/first-cause/reentry controls,15 source contracts and C17/overlay checks
passed. Fresh complete HAProxy3.2.25, binding selftest and production SPOA builds
passed. Exact argv, exits,147 raw file hashes and frozen nine-file source identity
are retained in run `i12-haproxy-415-acceptance-20261015/product-spop/redirect`.


Additional Root run: declared CPython3.14.7 pytest for the four affected test files passed23 tests/34 subtests. Exact argv/exits are in commands/redirect-root-focused-regression-20261018-v2.json; the earlier invalid interpreter-path attempt exit127 remains retained.

## Security impact

The response uses the public literal header API without log-format evaluation or
silently truncated borrowed text. Unsupported status, invalid URL, prior failure,
finish error and host API errors remain fail-closed; postcommit cannot replace
the response. No dependency, warning, gate, admission or isolation control is
weakened. The work is a bounded defensive correctness repair.

## Runtime evidence

Actual libModSecurity3.0.14 and host API component checks passed. No independent client/backend host run has yet qualified this redirect repair.

## Known limitations

These tests prove native engine and host API behavior. Fresh current-source
capture builds and independent native/companion302 client/backend/transport
retests remain required. No HTTP-only or component result receives lifecycle
credit. The separately observed companion Safe OUTCOME failure remains an open
product issue and does not change its original expectation.

## Remaining risks

The separately observed companion Safe OUTCOME discrepancy requires its own product repair and fresh host runs. Native and companion302 need fresh integrated capture binaries; component PASS is not lifecycle PASS.

## Checks not run and rationale

Integrated redirect hosts and final-head CI/Sonar follow normal #382→#410→#415 delivery. No automatic PR merge or original-oracle rewrite. The historical #382 Gitleaks release blocker remains independent.

## Final diff and review status

Root reviewed the product dispatcher, URL ownership, fail-closed paths and regressions. Separate independent review is recorded with the run handoff; its result will be reported only after receipt.
