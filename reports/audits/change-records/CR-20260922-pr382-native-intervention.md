# Change Record: native intervention collection and late dispatch

**Language:** English | [Deutsch](CR-20260922-pr382-native-intervention.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-native-intervention` |
| Date (UTC) | `2026-09-22` |
| Base revision | `7a52a55cfa4eb4c4c85ed44396e7137ef013f5aa` |

## Motivation and problem statement

The NGINX native intervention wrapper accepted every nonzero native return.
It also attempted a committed response replacement for a valid late rule,
returning a negative host result that the P4 caller classified as a technical
failure before the Safe/Strict policy could run. A stubbed caller-result test
could not expose that native-to-host mismatch.

## Acceptance criteria

Only native zero and one are valid. Clear stale rule/status metadata on collection,
release native-owned output once on every exit, and keep nondisruptive results
non-disruptive. Valid late P4 rules must reach their Safe/Strict owner without
attempting a header replacement first. Off and legitimate precommit dispatch
retain their native behavior. Genuine errors never forward the failed body.

## Implementation decision and rationale

Add a small native-result collector and error adapter, then defer only committed
P4 Safe/Strict results after rule-correlation validation. The existing body
filter remains the late-policy owner. The wrapper retains one cleanup tail.
No native APIs are shadowed and no unsupported transport capability is granted.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `tests/test_nginx_native_intervention_chain.py`
- `.github/workflows/lint.yml`
- This record and its German companion.

## Commands executed

The required CI command includes:

```sh
python -m unittest -v tests.test_nginx_native_intervention_chain
```

Ten test methods compile the actual collector, wrapper, status dispatch, P4
caller and late policy with real Common lifecycle/rule correlation. Engine and
final host I/O are controlled test boundaries. Tests are pending at preparation.

## Security impact

Undocumented native results, missing required context and invalid correlation
cannot become successful rule handling. Valid late rules are no longer confused
with technical errors merely because headers were sent. Cleanup ownership,
bounded metadata and mandatory error handling remain active.

## Runtime evidence

This is compiled native call-chain evidence, not a live host, full native engine,
or HTTP/2/HTTP/3 transport proof. The old focused tests remain required as well.

## Known limitations

The full I09-I12 producer/sink and integration-route requirements remain tracked
in the main checklist. Native audit-log returns and independent log sinks still
require their own checks. This change does not make every route complete.

## Remaining risks

A late abort cannot retract already sent bytes. Off intentionally keeps the old
native committed-response path. Host-visible actions must be observed separately.

## Checks not run and rationale

No local project commands ran because RTK is unavailable. The resulting commit
requires its own CI and exact-head Sonar-zero result. The independent secret-scan
finding is not resolved or suppressed by these changes.

## Final diff and review status

Prepared for Draft PR #382 only. No merge, master push, force push, dependency,
Framework/MRTS write or weakened scanner/test policy.
