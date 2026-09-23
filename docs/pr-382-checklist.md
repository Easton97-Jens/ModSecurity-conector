# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
branch `fix/unified-native-results-events-20260921`, base
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-09-23.

**I09 and I10 are not yet reduced to live-host proof alone.** Completed code,
executed compiled tests, pending native tests and actual host evidence remain
separate. The Apache module subset is now implemented and must not remain
listed as an untouched intervention/initialization/audit defect.

Latest published test repair: `7d05e89fc12dca64c7129553d0c83157e956e0f3`.
Its Sonar analysis confirms zero findings and displayed 0.0% new duplication.
The fresh native Envoy job was still running at this checklist's preparation.
This documentation update also repairs the two missing Apache Change Record
date fields that blocked bilingual validation; its own checks are still required.

Evidence correction: `a6898480` was never published. Its claimed results are not
used. Historical test claims apply only to the referenced revision and test layer.
The six host-action tests were actually delivered in `5a696b7c`.

References: [contract/migration](pr-382-event-contract.md),
[main Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md),
[Apache lifecycle](../reports/audits/change-records/CR-20260923-pr382-apache-native-lifecycle.md),
[Apache adoption](../reports/audits/change-records/CR-20260923-pr382-apache-adoption.md),
[Envoy native test repair](../reports/audits/change-records/CR-20260923-pr382-envoy-test-boundaries.md).

## 1. Implementation

- [x] I01: Native byte append accepts 0/1, phase success only 1. APR, NGINX, HTTP, Common and file-loading contracts remain distinct.
- [x] I02: Shared predicates in affected Apache, HAProxy, Common Runtime and NGINX body paths.
- [x] I03: Common/HAProxy intervention validation, cleanup and failure propagation.
- [x] I04: HAProxy response-header binding errors survive disruptive decisions.
- [x] I05: Common JSONL/hash view preserves input validation, redaction, counters and actual observations.
- [x] I06: Technical Apache/Common errors remain distinct from rule blocks; handwritten Apache JSON fallbacks removed.
- [x] I07: Typed NGINX response errors; no successful EOS inferred before evaluation.
- [x] I08: Native engine failure maps to invalid-engine-response; other classes stay distinct.
- [ ] I09: Complete the remaining route-by-route native/API and typed-error audit and resolve any resulting implementation gaps; obtain combined native verification.
- [x] I09a: NGINX byte/file separation, cumulative bounds, success-only completion and terminal failed re-entry (`fcbaca03`; V13).
- [x] I09b: Typed NGINX request errors, exact intervention collection, first cause/status and one event attempt; empty bodies remain valid (`7fe606c5`; V17).
- [x] I09c: Checked, once-only NGINX native audit completion with retained failure (`47714de0`; V17).
- [x] I09d: Envoy ext_proc retains the first Common error, seals failed header/body/EOS callbacks, clears pending rule state and bounds canonical failure reporting (`31200e8c`; V22).
- [x] I09e: Shared NGINX connection/URI result helper retains strict success, PCRE/phase brackets and host statuses without duplicate implementation (`bced5ce7`; V23).
- [x] I09f: Apache module now checks exact intervention results, releases buffers on every post-call outcome, checks retained copies, separates native/host error causes, checks initialization and binds engine cleanup to its configuration generation. Present and tested at `3c29004b`; V24.
- [ ] I10: Complete actual cross-route off/safe/strict error handling and its native integration verification, not merely shared policy tests.
- [x] I10a: NGINX late technical errors precede Safe/Strict rule policy (`52445b18`; V14).
- [x] I10b: Actual Common policy tests cover five error classes, ten profiles, two contract modes and both commitment states; technical failure never becomes Safe log-only. Not host-I/O proof.
- [x] I10c: Real NGINX collector/dispatcher/P4 chain tests retain late rules, Off behavior and cleanup (`1ce569e1`; V17).
- [x] I10d: Envoy commitment failure stops before append; empty EOS does not invent body-started state. Checked C ABI propagates errors through Go while retaining the compatibility ABI (`31200e8c`, `81e53a94`). Native verification is V20.
- [x] I10e: Apache's checked collector cannot mutate committed Location headers or reuse stale rule metadata on a technical failure. Audit claims its attempt before callbacks and never dispatches an actionable logging-phase intervention. Present at `3c29004b`; V24 is compiled APR/native-boundary evidence, not live httpd.
- [ ] I11: Complete producer/physical-sink parity, identifiers/causes, observed actions, duplicate terminal events and open/write/short-write/serialization failures.
- [x] I11a: Missing transport observations do not prove rule/error enforcement; custom records and actual evidence remain preserved.
- [x] I11b: Mandatory NGINX Phase-4 log failures remain terminal; invalid sinks and repeated terminal writes are bounded.
- [x] I11c: Missing-observation handling covers body limits, unsupported capabilities, cancellation and upstream disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime retains original event errors with NULL output, prevents failed-write retry and completion/snapshot masking, and preserves hash advancement rules (`68f78e07`; V21).
- [ ] I12: Verify each direct, companion, middleware and sidecar route separately, including actual host/transport/log results.
- [x] I12a: Ten separate ext_proc C-bridge failure/re-entry/empty-response scenarios pass (V22); not ext_authz/companion or live gRPC completion.
- [x] I13: Bounded HAProxy Rule-ID decoder and ordered cleanup extracted without changing phase/ownership semantics.
- [x] I14: All 96 original NGINX adoption cases plus four regressions retained.
- [x] I15: HAProxy helper/callsite adoption checks and eight isolated regressions retained.

### What remains before "only host proof is missing"

| Item | Remaining requirement |
| --- | --- |
| I09 | Review filter/API exits outside the completed Apache module and the remaining HAProxy, direct, companion and middleware producers. Trace each error through the actual caller and cleanup path; shared predicates or diagnostics alone do not prove completion. The Apache collector/init/audit fixes above are no longer open implementation items. |
| I10 | Complete native integration tests and verify each adapter's error-to-host-control path, including failures after commitment. Do not infer missing behavior solely from a helper lacking a guard when the Common state machine may already prevent it. |
| I11 | Apache's void event writer/callers still need complete physical failure propagation; HAProxy SPOP still needs its Common-event fputs result handled. Original Runtime I/O-error retention is fixed. These are implementation work, not just missing live evidence. |
| I12 | Run route-specific host, client-byte/reset, neighbor-stream, cleanup and physical-log cases. Request-only routes require their actual response companion. |

## 2. Verification

- [x] V01: Generated C return types repaired without disabling warnings/assertions.
- [x] V02: Original native/event step passed at `4f94f33d`, [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Compiled native error-classifier regressions and required CI wiring.
- [x] V04: Terminal-error, no-second-response and failed-append accounting assertions retained.
- [x] V05: Historical focused suites passed at `092dfd1c`; evidence retained below.
- [ ] V06: Complete all adoption/mutation checks on the final release head.
- [x] V06a: Historical Apache helper checks and 16 negative mutations passed at `1709e1de`; the current 25-case update is V24.
- [x] V06b: All 100 NGINX adoption/mutation cases passed at `f7aa2f2c`, `092dfd1c` and `bced5ce7`.
- [ ] V07: All final-release checks and review; overall release CI is not claimed green.
- [ ] V07a: Resolve independent secret scanning without an unsupported exception. The [workflow for 7d05e89f](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35896111802) still fails.
- [ ] V08: Real-host ProcessPartial/Reject, MIME/CSV, empty/multiple-chunk/EOS, budgets and native errors.
- [ ] V09: Late Safe/Strict, pre/post-commit failures, client bytes, reset scope, neighboring streams and cleanup.
- [ ] V10: Actual route logs, invalid/oversized metadata, missing observations and failed physical sinks.
- [x] V11: Actual Common JSONL/hash tests retain evidence/redaction; family labels are not host runs.
- [x] V12: Eight compiled HAProxy helper cases and binding compile/link checks passed at `039b7f12`.
- [x] V13: Nine NGINX request/file cases with controlled boundaries, not full file-reader integration.
- [x] V14: Nine NGINX late-error/re-entry cases, not a full HTTP matrix.
- [x] V15: Eight HAProxy Rule-ID adoption cases.
- [x] V16: Historical bilingual/template validation passed at `bced5ce7` and `b91b6826`; the newer Apache report schema repair is V26, not silently inherited.
- [x] V17: 43 NGINX request/native cases, including ten collector-chain and eight audit tests, passed at `b91b6826`.
- [x] V18: 55 Common/native/event/profile cases passed at `b91b6826`.
- [x] V19: Helper-aware source/security repair passed at `b91b6826` without removing other negative paths.
- [ ] V20: Complete the fresh native Go/CGo run. The workflow now really builds Common/libModSecurity and executes libmodsecurity-tagged tests, including both commitment cases. The first run exposed three test defects; repaired in `7d05e89f`. [Fresh job 107300314663](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35896111748/job/107300314663) was still running at preparation.
- [x] V21: Eight runtime sink/error-replay plus six host-action cases passed at `b91b6826` (14 total).
- [x] V22: Ten complete ext_proc C-bridge cases passed at `b91b6826`; controlled Common/native boundaries, not live transport evidence.
- [x] V23: Six compiled connection/URI caller/helper cases passed at `b91b6826`.
- [x] V24: At `3c29004b`, [Apache native job 107137107158](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504774/job/107137107158) passed the 20 compiled lifecycle cases and bootstrap. [Structure job 107137106792](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504774/job/107137106792) passed 25 adoption/mutation cases, then failed the separate missing report-date check.
- [x] V25a: `7d05e89f` contains the native test repair: independent valid-413 and terminal-invalid-acknowledgement cases, explicit unsafe file permissions and retained original inode. Production guards and existing positive controls remain unchanged.
- [ ] V25: Confirm fresh execution of the V25a repairs, including first-error retention and unchanged event bytes after failed retries.
- [ ] V26: Verify this delivery's added Date (UTC)/Datum (UTC) identity rows and paired checklist with the unchanged bilingual validator.

## 3. Sonar zero findings and zero duplication

- [x] S01: Read-only exact-head/provider gate rejects missing, stale, unfinished and ambiguous evidence.
- [x] S02: Negative tests, bounded diagnostics and scoped read permissions retained; no exclusions, accepted findings or weaker rules.
- [x] S03: Historical zero counts remain revision-specific: `039b7f12`, `91f07e12`, `47714de0`.
- [x] S03a: Exact-head gate passed at `f7aa2f2c`.
- [x] S03b: `91f07e12`, [check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571): zero new/accepted issues, hotspots and annotations.
- [x] S03c: `47714de0`, [check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312): same four zero counts.
- [x] S03d: `bced5ce7`, [check 106898325037](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106898325037): same zero counts and displayed 0.0% duplication.
- [x] S03e: Exact `7d05e89f`, [check 107300845580](https://github.com/Easton97-Jens/ModSecurity-conector/runs/107300845580): zero new/accepted issues, hotspots and annotations; displayed new-code duplication 0.0%.
- [ ] S04: Confirm final-release-head quality after the last delivery; earlier analysis cannot prove a later documentation SHA.
- [x] S05: Required duplication gate demands exact zero new duplicated lines, blocks and density, not a rounded percentage alone.
- [x] S06: Exact duplication gate passed at `bced5ce7`, [job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154), and at `b91b6826` in the full lint run below.

These are PR new-code metrics, not claims about all historical repository debt.
Coverage and secret scanning are independent requirements.

## 4. Route-specific state

| Route | Completed subset | Remaining |
| --- | --- | --- |
| NGINX native | Typed errors, predicates, audit latch, caller and adoption tests | Final combined and live transport/log matrix |
| Apache native | Exact collector, copied storage, first errors, checked audit/init/generation cleanup; 20 compiled and 25 adoption cases | Other filter/API exits, physical sink propagation and live host matrix |
| HAProxy HTX | Binding predicates and helper/adoption tests | Caller-level failure/cleanup and host/reset/log verification |
| HAProxy SPOE/SPOP + companion | Native/Common result contracts | SPOP write propagation and distinct companion/control proof |
| Envoy ext_proc | Checked commitment, sticky errors, ten C-bridge cases; native test repairs published | Fresh real CGo pass and live gRPC/host/log cases |
| Envoy ext_authz + companion | Shared Runtime fixes | Separate companion lifecycle and physical output proof |
| Traefik middleware/UDS | Shared Runtime fixes | Adapter-level errors, physical sinks and live host evidence |
| Traefik forwardAuth + companion | Shared Runtime fixes | Separate companion control/log evidence |
| lighttpd sidecar | Shared Runtime fixes | Adapter failure and actual socket/log evidence |
| lighttpd native/patched | Shared contracts on Runtime routes | Separate hooks, strict admission and native host proof |

Unsupported strict profiles remain unsupported. Equal semantics neither require
identical host integers nor grant new reset/abort capabilities.

## 5. Documentation and delivery

- [x] D01: Existing Draft PR only; no merge/master/force push.
- [x] D02: EN/DE checklist distinguishes implemented code from verification.
- [ ] D03: Complete connector guides/examples and compatibility review.
- [x] D03a: Paired contract and consumer/hash migration warnings retained.
- [x] D04: Reconcile actual Apache additions and published Envoy test repair; remove obsolete claims that the Apache module subset is still untouched.
- [ ] D05: Final-release document/link/diff/CI and PR/branch reconciliation.

## Revision-scoped evidence

The full [lint job 106900742683](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35773496921/job/106900742683)
passed for `b91b6826`, including both Sonar gates. That is historical evidence,
not an automatic pass for new Apache source or Envoy tests.
The `3c29004b` Apache structure job reached its final bilingual check before
failing for two missing date fields. Its native/APR job passed independently.
The first real Envoy run [35847504839](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35847504839)
failed three fixture/expectation cases; `7d05e89f` addresses them without changing
production protections. Pending results above must be updated after actual readback.

Earlier evidence remains in [the checklist at ad22918e](https://github.com/Easton97-Jens/ModSecurity-conector/blob/ad22918e92849a10483439d72ac9a50154ec00be/docs/pr-382-checklist.md)
and linked Change Records. The user clarified RTK scope for this continuation;
GitHub API edits do not require a local execution wrapper. Local Go formatting
was performed for the new native fixture and its consumer; full native execution
uses GitHub CI because GitHub DNS/download was unavailable in the editing container.
