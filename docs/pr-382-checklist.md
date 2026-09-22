# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
branch `fix/unified-native-results-events-20260921`, base
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-09-22.

**Overall implementation is incomplete; not ready to merge.** Implementation,
compiled boundary tests and actual live routes are separate claims.
Latest code/test checkpoint: `b91b68269027a3c5602b5624058df9e1f865535e`.
The repaired source/security group passed there (V19). The following documentation
commit must receive its own checks; no earlier Sonar result substitutes for it.

**Evidence correction:** `a6898480` was not published and carries no test or
Sonar evidence. The six host-action tests were actually published in `5a696b7c`.
Concurrent Envoy changes `31200e8c` and `81e53a94` were preserved and inspected.

References: [contract/migration](pr-382-event-contract.md),
[main Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md),
[route continuation](../reports/audits/change-records/CR-20260922-pr382-route-completion.md),
[NGINX shared tail](../reports/audits/change-records/CR-20260922-pr382-nginx-result-tail.md).

## 1. Implementation

- [x] I01: Native byte append accepts 0/1, phase success only 1. APR, NGINX, HTTP, Common and file-loading contracts remain distinct.
- [x] I02: Shared predicates in affected Apache, HAProxy, Common Runtime and NGINX body paths.
- [x] I03: Common/HAProxy intervention validation, cleanup and failure propagation.
- [x] I04: HAProxy response-header binding errors survive disruptive decisions.
- [x] I05: Common JSONL/hash view preserves input validation, redaction, counters and actual observations.
- [x] I06: Technical Apache/Common errors remain distinct from rule blocks; handwritten Apache JSON fallbacks removed.
- [x] I07: Typed NGINX response errors; no successful EOS inferred before evaluation.
- [x] I08: Native engine failure maps to invalid-engine-response; other classes stay distinct.
- [ ] I09: Complete remaining native/API exits and typed request-error producers across supported routes.
- [x] I09a: NGINX byte/file separation, cumulative bounds, success-only completion and terminal failed re-entry (`fcbaca03`; V13).
- [x] I09b: Typed NGINX request errors, exact intervention collection, first cause/status and one event attempt; empty bodies remain valid (`7fe606c5`; V17).
- [x] I09c: Checked, once-only NGINX native audit completion with retained failure (`47714de0`; V17).
- [x] I09d: Envoy ext_proc retains the first Common error, seals failed header/body/EOS callbacks, clears pending rule state and bounds canonical failure reporting (`31200e8c`; V22).
- [x] I09e: Shared NGINX connection/URI result helper retains strict success, PCRE/phase brackets and host statuses without duplicate implementation (`bced5ce7`; V23).
- [ ] I10: Complete actual cross-route off/safe/strict behavior, including native and host errors.
- [x] I10a: NGINX late technical errors precede Safe/Strict rule policy (`52445b18`; V14).
- [x] I10b: Actual Common policy tests cover five error classes, ten profiles, two contract modes and both commitment states; technical failure never becomes Safe log-only. Not host-I/O proof.
- [x] I10c: Real NGINX collector/dispatcher/P4 chain tests retain late rules, Off behavior and cleanup (`1ce569e1`; V17).
- [x] I10d: Envoy commitment failure stops before append; empty EOS does not invent body-started state. Checked C ABI propagates errors through the Go receiver, retaining compatibility ABI (`31200e8c`, `81e53a94`). C tests passed; native Go execution remains V20.
- [ ] I11: Complete producer/physical-sink parity, identifiers/causes, observed actions, duplicate terminal events and open/write/short-write/serialization failures.
- [x] I11a: Missing transport observations do not prove rule/error enforcement; custom records and actual evidence remain preserved.
- [x] I11b: Mandatory NGINX Phase-4 log failures remain terminal; invalid sinks and repeated terminal writes are bounded.
- [x] I11c: Missing-observation handling covers body limits, unsupported capabilities, cancellation and upstream disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime retains the original event error with NULL output, prevents failed-write retry and completion/snapshot masking, and preserves hash advancement rules (`68f78e07`; V21).
- [ ] I12: Verify every direct, companion, middleware and sidecar route separately, including actual host/transport/log results.
- [x] I12a: Ten separate ext_proc C-bridge failure/re-entry/empty-response scenarios pass (V22). This does not complete ext_authz/companion or live gRPC.
- [x] I13: Bounded HAProxy Rule-ID decoder and ordered cleanup extracted without changing phase/ownership semantics.
- [x] I14: All 96 original NGINX adoption cases plus four regressions retained.
- [x] I15: HAProxy helper/callsite adoption checks and eight isolated regressions retained.

### Concrete remaining boundaries

| Item | Required work, not a missing checkmark |
| --- | --- |
| I09 | Apache `process_intervention()` still needs exact native-result validation and cleanup on every outcome. Review remaining initialization/audit/host-diagnostic exits and typed producers. |
| I10 | Verify remaining native, companion and middleware results reach the actual host control path without a successful fallback. Run native Go commitment tests. |
| I11 | Apache's void event writer/callers still lack complete physical failure propagation. HAProxy SPOP still ignores its Common-event `fputs()` result. The old Runtime error-replay defect is fixed, not open. |
| I12 | Complete distinct live host, client-byte/reset and physical-log evidence. A request-only route needs its response companion; a compiled bridge is not a live host. |

## 2. Verification

- [x] V01: Generated C return types repaired without disabling warnings/assertions.
- [x] V02: Original native/event step passed at `4f94f33d`, [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Compiled native error-classifier regressions and required CI wiring.
- [x] V04: Terminal-error, no-second-response and failed-append accounting assertions retained.
- [x] V05: Historical focused suites passed at `092dfd1c`; evidence retained below.
- [ ] V06: Complete all adoption/mutation checks on the final release head.
- [x] V06a: Apache helper checks and 16 negative mutations passed at `1709e1de`, [job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579).
- [x] V06b: All 100 NGINX adoption/mutation cases passed at `f7aa2f2c`, `092dfd1c` and `bced5ce7`.
- [ ] V07: All final-release checks and review; overall release CI is not claimed green.
- [ ] V07a: Resolve independent secret scanning without an unsupported exception; original [job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952). The workflow still fails at `b91b6826`.
- [ ] V08: Real-host ProcessPartial/Reject, MIME/CSV, empty/multiple-chunk/EOS, budgets and native errors.
- [ ] V09: Late Safe/Strict, pre/post-commit failures, client bytes, reset scope, neighboring streams and cleanup.
- [ ] V10: Actual route logs, invalid/oversized metadata, missing observations and failed physical sinks.
- [x] V11: Actual Common JSONL/hash observation tests retain evidence/redaction; family labels are not host runs.
- [x] V12: Eight compiled HAProxy helper tests and binding compile/link checks passed at `039b7f12`, [job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Nine NGINX request/file tests with controlled boundaries, not full file-reader integration.
- [x] V14: Nine NGINX late-error/re-entry tests, not a full HTTP matrix.
- [x] V15: Eight HAProxy Rule-ID adoption regressions.
- [x] V16: Bilingual/template validation passed at `bced5ce7` and `b91b6826`.
- [x] V17: 43 NGINX request/native tests, including ten collector-chain and eight audit cases, passed at `b91b6826`.
- [x] V18: 55 Common/native/event/profile cases, including observation controls and duplication-gate tests, passed at `b91b6826`.
- [x] V19: Helper-aware source/security repair passed at `b91b6826`. Both caller orderings, exact native failure and host-result handling remain checked; the old other negative paths were not removed.
- [ ] V20: Execute the two native Go/CGo commitment tests from `81e53a94`. The `test-envoy` contract workflow does not run them; checked source/ABI presence is not execution proof.
- [x] V21: Eight runtime sink/error-replay plus six host-action tests passed at `b91b6826` (14 total).
- [x] V22: Ten complete ext_proc C-bridge tests passed at `b91b6826`; Common/native boundaries are controlled, not live gRPC or physical-log evidence.
- [x] V23: Six compiled connection/URI caller/helper regressions passed at `b91b6826`.

## 3. Sonar zero findings and zero duplication

- [x] S01: Read-only exact-head/provider gate rejects missing, stale, unfinished and ambiguous findings evidence.
- [x] S02: Negative tests, bounded diagnostics and scoped read permissions retained; no scanner exclusions, accepted findings or weaker rules.
- [x] S03: Historical zero counts remain revision-specific: `039b7f12`, `91f07e12`, `47714de0`.
- [x] S03a: Exact-head gate passed at `f7aa2f2c`.
- [x] S03b: `91f07e12`, [check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571): zero new/accepted issues, hotspots and annotations.
- [x] S03c: `47714de0`, [check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312): same four zero counts.
- [x] S03d: `bced5ce7`, [check 106898325037](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106898325037): same zero counts and displayed duplication 0.0%.
- [ ] S04: Confirm final-release-head quality after the last delivery; no prior analysis substitutes for a later SHA.
- [x] S05: Required duplication gate demands exact zero new duplicated lines, blocks and density; missing/rounded values cannot pass. Seven format/negative unit tests pass.
- [x] S06: Exact duplication gate passed at `bced5ce7` in [job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154). Actual connection/URI logic was shared, not excluded.

These are PR new-code metrics, not proof of zero historical repository debt.
Coverage and the independent secret scan remain separate from Sonar findings/duplication.

## 4. Route-specific state

| Family / route | Implemented or tested boundary | Remaining evidence |
| --- | --- | --- |
| NGINX native | Typed errors, predicates, audit latch, connection/URI callers, adoption cases | Full live host/transport/physical-log matrix |
| Apache native | Body predicates and typed errors | Exact intervention results/cleanup, physical sinks, host matrix |
| HAProxy HTX | Binding predicates, helper/adoption tests | Direct host error/reset/abort/log cases |
| HAProxy SPOE/SPOP + companion | Common/native result contracts | SPOP physical write and separate companion/transport proof |
| Envoy ext_proc | First-error latch, checked commitment, truthful empty-body metadata; Go uses checked ABI | Native Go and live gRPC/host/log proof |
| Envoy ext_authz + companion | Shared Runtime predicate/error replay fixes | Separate request/response-companion, log and transport proof |
| Traefik middleware/UDS | Shared Runtime fixes | Middleware/UDS host errors and physical sinks |
| Traefik forwardAuth + companion | Shared Runtime fixes | Separate companion lifecycle/control/log proof |
| lighttpd sidecar | Shared Runtime fixes | Physical sinks and real socket/host behavior |
| lighttpd native/patched profiles | Shared contracts on Runtime routes | Separate hooks, unsupported strict admission and native host proof |

Unsupported strict profiles remain unsupported. Equal semantics do not imply
equal host integers or invented abort/reset capabilities.

## 5. Documentation and delivery

- [x] D01: Existing Draft PR only; no merge/master/force push.
- [x] D02: Paired EN/DE checklist separates implementation and verification.
- [ ] D03: Complete connector guides/examples and compatibility/version review.
- [x] D03a: Paired contract and consumer/hash migration warnings retained.
- [x] D04: Reconcile source and tests, correct unpublished delivery claims and remove the fixed Runtime replay defect from open work.
- [ ] D05: Final-release document/link/diff/CI and PR/branch reconciliation.

## Revision-scoped evidence

[Job 106900742683](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35773496921/job/106900742683)
for `b91b68269027a3c5602b5624058df9e1f865535e` passed bilingual checks,
55/14/10/6/43/9 focused groups and the repaired source/security step at readback.
Its remaining steps were still running then; this is not a complete-job claim.
The preceding [job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154)
for `bced5ce7` passed 100 NGINX/eight HAProxy adoption cases, configuration checks
and both Sonar gates, but failed the old source assertion. V19 supersedes that
specific failure, not unrelated final-release or live-route requirements.

Historical detail remains in [the checklist at 0532b5eb](https://github.com/Easton97-Jens/ModSecurity-conector/blob/0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9/docs/pr-382-checklist.md),
[historical job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
and linked Change Records. Preparation-time pending notes are superseded only
for the revision and test layer explicitly cited.

No local project command/build or git diff check bypassed the missing mandatory
RTK wrapper. Actual GitHub CI and per-commit comparisons provide this evidence.
