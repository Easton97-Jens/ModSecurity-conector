# FND-PARENT-0073 — HAProxy HTX metadata-event test failed before its path and TLS control

## Classification

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0073 |
| Category | test_failure |
| Repository / ownership | parent / parent |
| Priority | P1 |
| Severity | not_applicable |
| Confidence | confirmed |
| Status | verified |
| Feasibility | feasible_now |
| Release blocker | false |
| Candidate-integration blocker | false |
| Security relevant | false |
| Connector / profile | haproxy / PR #182 exact current-master hosted head `76644bfe832d1530704ca2ae0f2182338949ead5` |

## Summary

At PR #182's exact previous head `d79750b4869080ab04137d1c3eff7a9c751af760`,
`HAProxyHTXSmokeHelperTest.test_event_contains_only_metadata` loaded `root` in
helper calls but never bound it. The complete helper suite cannot currently
reach discovery because the Framework fixture is deliberately uninitialized,
but retained static AST evidence confirms the source defect.

The exact current-master hosted head assigns `root = Path(temporary)` before each affected
path and helper call and centralizes the duplicated HAProxy/Envoy descriptor-
safe artifact protocol. Its 42 focused common/HAProxy/Envoy/runtime-path
controls plus recorded static, direct private-root metadata-event,
transaction-ID/TLS, shell, HTX-overlay, Common-adoption, bilingual, and
whitespace controls pass. Required GitHub contexts pass, Sonar has Quality
Gate `OK` with zero open issues and zero New-Code duplication, and review/
thread readbacks are empty. The candidate blocker is cleared; protected merge
and resulting-master validation remain required.

## Impact and scope

The intended path/TLS-sensitive test control stopped before its metadata-only,
private-root, and host-evidence assertions. This is a test-control failure;
there is no evidence of a production HTX path, TLS, or metadata security
defect.

Affected source and symbol:

- `connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py`
- `HAProxyHTXSmokeHelperTest.test_event_contains_only_metadata`

## Root cause and remediation

The test made individual `Path(temporary)` values but never assigned the shared
`root` required by the helper confinement contract. The repair assigns
`root = Path(temporary)` once and derives the event and log paths from it.

The complete Framework-backed helper suite and live HAProxy/libmodsecurity
runtime remain unavailable in this task clone. Framework/MRTS must not be
initialized or changed merely to bypass that missing fixture.

## Evidence and validation

| Stage | Artifact | SHA-256 | Result |
| --- | --- | --- | --- |
| Exact pre-fix static analysis | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-unbound-root-static.md` | `82ff93736e180b8d17c2499661ffd04bd4c48edbded48a18c5cda83a0c286d05` | `root` was loaded but never locally bound. |
| Local post-fix focused controls | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-root-binding-postfix.md` | `b74d25130e749b4c58a5c42966f58d441bcedc9bcb0810f2952abc5dbea15668` | Binding, direct metadata-event, transaction-ID/TLS, shell, static, bilingual, and diff controls passed. |
| Committed shared-artifact remedy | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-shared-artifact-remediation-local.md` | `a9066f4f4420f1ac53a366bae14f563228560b14f80efcb6da64d5dba1747648` | The workspace tree later committed as `c15092f2bf05d5281f0976e87450bb79e6ea9e65` passed 42 focused common/HAProxy/Envoy/runtime-path controls; fresh pushed-head hosted evidence remains required. |
| Exact hosted readiness | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-c798-exact-head-hosted.md` | `f02e5612bb3394387d349aec72da4025a130f6e84d71b8aae76ae32ad5271add` | Historical exact head `c798334f9e6ddb5f2f4385e66779aba55be06156` was clean, mergeable, required-context clean, Sonar clean, and had zero review threads/reviews. |
| Exact current-master hosted readiness | `/var/tmp/codex/ModSecurity-conector/runs/merge-prs-181-182-master-20260729.nq2EeI/evidence/pr182-766-current-master-exact-head-hosted.md` | `e306a4e68c3c91b623f9e8851df00f37fc1a84b3cc76fc3ffa0a7e3e177bb7bc` | Current head `76644bfe832d1530704ca2ae0f2182338949ead5`, produced by normal base update, is clean, mergeable, required-context clean, Sonar clean, and has zero review threads/reviews. |

Acceptance requires a bound source root, passing focused controls on the
committed candidate, and fresh exact-head GitHub Actions, SonarQube Cloud,
review/thread, and mergeability evidence after push.

## Residual state

The local repair is `fixed`, but the whole Framework-backed helper test and
live HTX runtime are blocked by absent authorized prerequisites. No runtime
security finding is asserted. The exact current-master PR head has fresh hosted evidence;
protected merge and resulting-master validation remain required before closure.
