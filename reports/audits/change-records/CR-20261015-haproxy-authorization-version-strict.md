# Change Record: CR-20261015-haproxy-authorization-version-strict

**Language:** English | [Deutsch](CR-20261015-haproxy-authorization-version-strict.de.md)

Product repair in existing PR #382; integration and host acceptance in #410/#415.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-haproxy-authorization-version-strict |
| Date (UTC) | 2026-10-15 |
| Base revision | `9980eb049dde0643da6a4f04e3b6712801b670b3` |

## Motivation and problem statement

Finite SPOP P1/P2 Allow incorrectly failed generic full-lifecycle finish. Native URI processing hardcoded HTTP/1.1. Strict retained queued response channel bytes after selecting shutdown.

## Acceptance criteria

Complete declared P1/P2 without synthetic P3/P4; propagate admitted HTTP versions; purge rejected queued response bytes and stop filter advancement. Fresh integrated host verification remains required in #415.

## Implementation decision and rationale

Add a dedicated Common request-authorization finish operation for predeclared direct mask3/no companion; generic finish remains mask15. Require actual request http_version. Strict erases pending HTX/channel output, aborts only the affected stream, and returns a negative filter result.

## Changed files

Common transaction contract/state; HAProxy binding, mapper, SPOP runtime and HTX filter; focused request/version/limit/caller/failure tests; paired Common and HAProxy guides. No Framework/MRTS source or gitlink change.

## Commands executed

Root ran RTK-wrapped CPython3.14.7 pytest for test_haproxy_transaction_contract_binding, test_haproxy_spop_request_target, test_haproxy_native_http_version, test_haproxy_request_authorization_contract, test_haproxy_i10_host_callers, test_haproxy_i10_binding_callers and test_haproxy_spop_event_sink_failures: 69passed,43subtests passed,exit0. Exact argv/cwd/output hashes are in external run i12-haproxy-415-acceptance-20261015/commands/product-targeted-pytest-v2.json. An earlier nonexistent test filename produced exit4 before collection; its receipt is preserved.

## Security impact

Admission stays fail closed. Sample input cannot broaden scope. Unknown/missing/conflicting versions fail before native allocation. Common structure layout is unchanged; all internal HAProxy request-structure consumers require rebuilding. No security exception, gate change or payload log.

## Runtime evidence

Real SDK tests exercise versions1.0/1.1/2.0, Allow/Deny, terminal errors and once-only free. Strict component tests cover direct/companion callbacks, queued0/33/65537 bytes, previously delivered bytes, Safe and neighbor controls. Separate sanitizer and mutation receipts are retained. The actual HAProxy3.2.25 filter translation unit compiles. These observations do not constitute fresh host lifecycle PASS.

## Known limitations

Actual H1 mux output is separate from HTX/channel buffering. This patch does not supply a native Common event sink or establish every HTTP/2 framing mapping.

## Remaining risks

Bytes already delivered cannot be withdrawn. Fresh bounded, empty, large, streaming, cancel and parallel host cases must measure actual commit/decision/client ordering. Historical evidence remains unchanged.

## Checks not run and rationale

Fresh integrated private host runs and final-head CI/Sonar follow normal #382→#410→#415 integration and rebuilding. The historical #382 Gitleaks release blocker remains independent without exemption.

## Final diff and review status

Independent reviews found no material request/version or Strict patch issue. Focused pytest, sanitizer, mutation, SDK and compile receipts are retained. Full I12 acceptance still requires fresh host qualification and current-head gates.
