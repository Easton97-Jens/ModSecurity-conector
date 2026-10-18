# Change Record: CR-20261018-haproxy-physical-common-sinks

**Language:** English | [Deutsch](CR-20261018-haproxy-physical-common-sinks.de.md)

Product follow-up on existing #382; integrated host acceptance on #415.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-haproxy-physical-common-sinks |
| Date (UTC) | 2026-10-18 |
| Base revision | `29b42a469d4273661bcda5e917db62d9de21a06b` |

## Motivation and problem statement

Native HTX had no configured physical Common decision sink. Stdio close/write failures and companion OUTCOME event provenance needed explicit shared handling. A CI binding fixture also omitted the newly required request HTTP-version field.

## Acceptance criteria

Write bounded physical native metadata through secure private descriptors; check serialization and all stdio stages; preserve first cause and exact observed phase; reject mismatched companion events; retain native Allow and once-only close/free behavior. Fresh host lifecycle acceptance remains separate.

## Implementation decision and rationale

Add three checked Common FILE helpers and optional HTX events-file with a mutex and sticky first error. Reuse the existing no-follow private-file opener for SPOP logs. Emit companion events after accepted OUTCOME and before RELEASE using an owner snapshot and copied queue metadata. Valid P4 Allow in COMPLETED is accepted without an event; non-Allow decisions with false disruptive flags are rejected. Omit unknown companion late_intervention_mode rather than copying the owner engine default.

## Changed files

common/include/msconnector/event_jsonl.h, common/src/event_jsonl.c; HAProxy filter/binding/header/SPOP runtime; native Common-stream/physical-event/companion-event tests and existing I10/sink fixtures. Root updates tests/test_haproxy_binding_refactor.py with http_version and an assertion that native URI processing receives 1.1. Documentation: connectors/haproxy/README.md and README.de.md, plus this Change Record pair.

## Commands executed

RTK-wrapped focused CPython3.14.7 tests, compiled fault cookies, ASan/UBSan, native SDK P3/P4 physical event readback, seven owner mutations, four shared-helper mutations, omitted-native-write mutation, and HAProxy3.2.25/binding/SPOP builds passed. Exact argv, exits, raw hashes and retained failing-before attempts are indexed by external run i12-haproxy-415-acceptance-20261015/product-spop/physical-sink-review.json. The Root binding-refactor regression passed in commands/binding-refactor-current-version-20261018. Later integrated suite results are recorded separately.

Root broader regression: 276 tests and 249 subtests passed, 12 skipped, four failures. Two stale extracted/native security fixtures were corrected and their 14-test suite passed. The other two failures are the old upload-artifact pin already corrected on #410; validation after normal integration must use that current test, without changing the workflow pin. Paired README/Change Record and documentation-link checks passed.

## Security impact

No payload/header/URI/native-log data enters Common metadata. Secure path admission, ownership and mode checks remain active; no symlink or stdout fallback. A poisoned configured sink rejects later Allow. Queue metadata has bounded owned lifetime. No dependency, Framework/MRTS gitlink, gate, warning or security-policy change.

## Runtime evidence

Real libModSecurity3.0.14 produces physical P3/P4 decision records; concurrent controls preserve 32 correlated native records. Stdio controls exercise prior ferror, serialization no-write, fputs/fflush/fclose failure, sticky retry prevention and consumed ownership. These are actual component executions and do not constitute a complete HAProxy host lifecycle PASS.

## Known limitations

Flush is not durability or client delivery. Native filter deinit is void and cannot report a process exit failure. Companion host phase4-mode remains unknown in its physical event because current OUTCOME carries no mode; the optional field is omitted. A sandbox UID-map-dependent opener control explicitly skipped; ordinary private-file smoke passed.

## Remaining risks

Fresh Direct/SPOP/Companion builds and isolated host tests must bind the integrated revision. Requirements needing physical observed host-mode metadata remain open until separately implemented and measured. Historical raw evidence and failures remain unchanged.

## Checks not run and rationale

Full current integrated I12 host qualification and final-head CI/Sonar await publication through #382→#410→#415 and fresh builds. Historical #382 Gitleaks is an independent release blocker with no waiver or history rewrite.

## Final diff and review status

Independent source review found incorrect P1/P3 attribution on sink failure; the owning fix uses the actual decision phase and preserves earlier causes. Final frozen source identity and focused regression results are retained in the external review packet. Root integrated review, documentation checks and delivery are required before publishing this follow-up.
