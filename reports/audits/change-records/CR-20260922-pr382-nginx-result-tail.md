# Change Record: Shared connection and URI result boundary

**Language:** English | [Deutsch](CR-20260922-pr382-nginx-result-tail.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-nginx-result-tail` |
| Date (UTC) | `2026-09-22` |
| Base revision | `81e53a943fb149a92eb4214091f81a217c567f8b` |

## Motivation and problem statement

Exact-head Sonar readback at `84c378ac` identified two duplicate blocks in
`ngx_http_modsecurity_access.c`, starting at lines 391 and 469. Six changed
lines were duplicated; new-code density was 0.09965122072745392 percent.
These blocks implemented the same connection/URI result and intervention tail.

## Acceptance criteria

Remove the duplicate implementation by sharing its actual behavior, not by
changing scanner settings or disguising tokens. Native phase success remains
exactly one. Native failure cannot call intervention dispatch. Positive host
statuses remain unchanged; negative dispatch remains terminal HTTP 500.
Both callers must restore PCRE and the URI event bracket before dispatch.

## Implementation decision and rationale

A private `ngx_http_modsecurity_request_native_result()` owns the shared tail.
Native connection and URI calls remain separate, as do metadata conversion and
phase brackets. The diagnostic phase label is a static caller literal, not
request content. Request-body append and strict file-reader contracts are untouched.

## Changed files

NGINX access source, `tests/test_nginx_request_phase_completion.py`, required
lint wiring and this paired Change Record. Concurrent Envoy/CGo work is preserved.

## Commands executed

Required CI invokes `python -m unittest -v tests.test_nginx_request_phase_completion`.
Six tests compile both actual callers and the actual shared helper with
`-std=c17 -Wall -Wextra -Werror`. Results are pending for the new published SHA.
No local project command was executed without the mandatory RTK wrapper.

## Security impact

Strict native success, original canonical failure, terminal host results and
original conversion/buffer limits remain enforced. No exclusions, accepted
findings, increased permissions or unrelated native call changes.

## Runtime evidence

Tests exercise real caller-to-helper code with controlled native, address,
canonical-failure and final host-dispatch boundaries. They check failure/noop,
positive HTTP status, negative dispatcher, first cause and conversion rejection.
Existing broader request, phase and mutation tests remain required.

## Known limitations

This is a behavior-preserving I09 refactor, not proof that all request API exits
or all I10/I12 adapter routes are complete. It is not a live NGINX transport run.

## Remaining risks

Fresh Sonar counts and full affected CI are required; a rounded summary alone
cannot prove zero duplicated lines. Apache and other route gaps remain separate.

## Checks not run and rationale

Local builds and host tests require an unavailable RTK environment. Verification
uses GitHub CI. No result is inherited from an earlier commit.

## Final diff and review status

Draft PR #382 only; no merge, master push, force push or submodule/dependency change.
