# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
branch `fix/unified-native-results-events-20260921`, base
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-09-22.

**The overall implementation is not complete; the PR is not ready to merge.**
A checked implementation subset is not a claim that all ten logical routes ran.
Latest inspected code checkpoint: `bced5ce78c62b7665730d2e81b307a3676da42f3`.
Its focused tests and both Sonar gates passed; one stale source assertion failed.
This checklist update also repairs that assertion; fresh combined CI is required.

**Evidence correction:** the previously reported `a6898480` commit was not
published. No result is attributed to it. The six host-action tests were actually
published in `5a696b7c` and passed together with the eight runtime sink tests.
Concurrent Envoy changes `31200e8c` and `81e53a94` were preserved and inspected.

References: [contract/migration](pr-382-event-contract.md),
[main Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md),
[route continuation](../reports/audits/change-records/CR-20260922-pr382-route-completion.md),
[NGINX shared tail](../reports/audits/change-records/CR-20260922-pr382-nginx-result-tail.md).

## 1. Implementation

- [x] I01: Operation-specific native predicates: byte append accepts 0/1, phase success only 1. Preserve distinct APR, NGINX, HTTP, Common and file-loading contracts.
- [x] I02: Shared predicates in affected Apache, HAProxy, Common Runtime and NGINX body paths.
- [x] I03: Common/HAProxy native intervention validation, cleanup and failure propagation.
- [x] I04: HAProxy response-header binding errors survive disruptive decisions.
- [x] I05: Common JSONL/hash event view preserves original-input validation, redaction, counters and actual observations.
- [x] I06: Technical Apache/Common errors remain distinct from rule blocks; handwritten Apache JSON fallbacks removed.
- [x] I07: Typed NGINX response errors; no successful EOS inferred from a pre-evaluation flag.
- [x] I08: Native engine failure maps to invalid-engine-response; other error classes remain distinct.
- [ ] I09: Complete all remaining native/API exits and typed request-error producers across the supported routes.
- [x] I09a: NGINX byte/file separation, cumulative bounds, success-only completion and terminal failed re-entry (`fcbaca03`; V13).
- [x] I09b: Typed NGINX request errors, exact intervention collection, first cause/status and one event attempt; legitimate empty bodies remain valid (`7fe606c5`; V17).
- [x] I09c: Checked, once-only NGINX native audit completion and retained failure (`47714de0`; V17).
- [x] I09d: Envoy ext_proc bridge retains its first Common error, seals failed body/header/EOS callbacks, clears pending rule state and bounds canonical failure reporting (`31200e8c`; V22).
- [x] I09e: One NGINX connection/URI result helper replaces duplicate code while retaining strict phase success, PCRE/phase brackets and unchanged host statuses (`bced5ce7`; V23).
- [ ] I10: Complete cross-route off/safe/strict consistency, including actual native and host failures.
- [x] I10a: NGINX late technical errors are handled before Safe/Strict rule policy (`52445b18`; V14).
- [x] I10b: Actual Common policy tests cover five error classes, ten registered profiles, two contract modes and both commitment states; technical failure never becomes successful Safe log-only. This is not host-I/O proof.
- [x] I10c: Real NGINX collector/dispatcher/P4 chain tests retain valid late rules, Off behavior and cleanup (`1ce569e1`; V17).
- [x] I10d: Envoy commitment failure stops before response append; empty EOS does not fabricate body-started state. Checked C ABI now propagates commit errors through the Go receiver; compatibility ABI retained (`31200e8c`, `81e53a94`). C-boundary tests passed; native Go tests remain V20.
- [ ] I11: Complete all event producers and physical sinks: identifiers/causes, observed actions, duplicate terminal events and open/write/short-write/serialization errors.
- [x] I11a: NULL/empty/not_observable transport values do not prove rule/error enforcement; unknown/custom records and actual evidence are preserved.
- [x] I11b: Mandatory NGINX Phase-4 log failures remain terminal; invalid sinks and repeated terminal writes are bounded.
- [x] I11c: Shared missing-observation handling also covers body limits, unsupported capabilities, client cancellation and upstream disconnect (`3730eaa0`; V18).
- [x] I11d: Runtime retains the original event error code even with NULL error output, does not retry failed writes or hide them behind completion/snapshot shortcuts, and preserves hash advancement rules (`68f78e07`; V21).
- [ ] I12: Verify each direct, companion, middleware and sidecar route separately, including actual host/transport/log outcomes.
- [x] I12a: Separate ext_proc C-bridge callback tests cover ten failure/re-entry/empty-response scenarios (`31200e8c`, refreshed at `bced5ce7`; V22). This does not mark ext_authz/companion or live gRPC complete.
- [x] I13: Bounded HAProxy Rule-ID decoder and ordered cleanup extracted without changing phase/ownership semantics.
- [x] I14: NGINX adoption tests retain all 96 original cases plus four regressions.
- [x] I15: HAProxy helper/callsite adoption checks and eight isolated regressions retained.

### Concrete remaining boundaries

| Item | Remaining work, not a missing checkmark |
| --- | --- |
| I09 | Apache `process_intervention()` still requires exact native-result validation and cleanup on every outcome; inspect the remaining initialization, audit and host-only diagnostic exits and their typed events. |
| I10 | Verify actual control flow through remaining Apache/HAProxy/direct/companion/middleware adapters. Do not infer enforcement from Common policy or a parsed strict setting. Execute the added native Go commitment tests. |
| I11 | Apache's void event writer/callers still do not propagate physical sink failure through the complete host path. HAProxy SPOP still ignores its Common-event `fputs()` result. The old Runtime error-class replay defect is fixed and is no longer listed as open. |
| I12 | Complete separate live host, commitment, client-byte/reset and physical-log evidence for every route. A request-only route needs its actual response companion; a compiled bridge is not a live host. |

## 2. Verification

- [x] V01: Generated C return types repaired without disabling warnings/assertions.
- [x] V02: Original native/event step passed at `4f94f33d`, [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Compiled native error-classifier regressions and CI wiring.
- [x] V04: Terminal-error, no-second-response and failed-append accounting assertions retained.
- [x] V05: Historical focused suites passed at `092dfd1c`; evidence retained below.
- [ ] V06: Complete all adoption/mutation checks together on the final release head.
- [x] V06a: Apache helper checks and 16 negative mutations passed at `1709e1de`, [job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579).
- [x] V06b: All 100 NGINX adoption/mutation tests passed at `f7aa2f2c`, `092dfd1c` and `bced5ce7`.
- [ ] V07: All final-release checks/review; no full green release claim.
- [ ] V07a: Resolve the independent secret-scan failure without an unsupported false-positive disposition or exception; original [job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952).
- [ ] V08: Equal real-host ProcessPartial/Reject, MIME/CSV, empty/multiple-chunk/EOS, budget and native-error cases.
- [ ] V09: Supported late Safe/Strict behavior, pre/post-commit failures, client bytes, reset scope, neighboring streams and cleanup.
- [ ] V10: Actual route log comparison, invalid/oversized metadata, missing observations and failed physical sinks.
- [x] V11: Real Common JSONL/hash observation tests retain evidence/redaction; family labels are not host runs.
- [x] V12: Eight compiled HAProxy helper tests and binding compile/link checks passed at `039b7f12`, [job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Nine NGINX request/file tests; controlled native/host boundaries, not full file-reader integration.
- [x] V14: Nine NGINX late-error/re-entry tests; not a complete HTTP matrix.
- [x] V15: Eight HAProxy Rule-ID adoption regressions.
- [x] V16: EN/DE Change Record/template checks passed again, including at `bced5ce7`.
- [x] V17: NGINX request/native group: 43 tests, including ten collector-chain and eight audit tests; passed at `bced5ce7`.
- [x] V18: Common/native/event/profile group: 55 tests, including observation negative control and duplication-gate unit tests; passed at `bced5ce7`.
- [ ] V19: Verify the helper-aware source-assertion repair in this checklist delivery. At `bced5ce7` the old connection/URI assertion failed; it was not disabled.
- [ ] V20: Execute the two native Go/CGo commitment tests introduced by `81e53a94`; checked ABI/source presence is not execution evidence.
- [x] V21: Eight runtime physical-write/error-replay tests plus six host-action validation tests passed at `bced5ce7` (14 total).
- [x] V22: Ten complete ext_proc C-bridge regression cases passed at `bced5ce7`; Common/native boundaries are controlled and real network delivery is not tested.
- [x] V23: Six new compiled connection/URI caller and helper regressions passed at `bced5ce7`.

## 3. Sonar zero findings and zero duplication

- [x] S01: Exact-head/provider-checked read-only finding gate rejects missing/stale/unfinished/ambiguous results.
- [x] S02: Negative tests, bounded diagnostics and scoped read permissions retained. No scanner exclusions, accepted findings or weakened rules.
- [x] S03: Historical zero-finding results remain valid only for their own revisions: `039b7f12`, `91f07e12`, `47714de0`.
- [x] S03a: Exact-head gate passed at `f7aa2f2c`.
- [x] S03b: `91f07e12`, [check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571): zero new/accepted issues, hotspots and annotations.
- [x] S03c: `47714de0`, [check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312): same four zero counts.
- [x] S03d: `bced5ce7`, [check 106898325037](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106898325037): zero new/accepted issues, hotspots and annotations; displayed duplication 0.0%.
- [ ] S04: Confirm all final-release-head quality evidence after the last delivery; earlier results never substitute for a later SHA.
- [x] S05: Required duplication gate checks exact zero new duplicated lines, blocks and density, not rounded display alone. Both unambiguous period formats are supported; seven negative/format unit tests pass.
- [x] S06: Exact duplication gate passed at `bced5ce7` in the evidence job below. The actual duplicate connection/URI tails were shared, not excluded from analysis.

These are PR new-code metrics. Zero findings/duplication does not prove zero
historical repository debt or clear the independent secret-scanning failure.
Coverage is a separate metric and is not represented as improved by this change.

## 4. Route-specific state

| Family / route | Implemented or tested boundary | Remaining evidence |
| --- | --- | --- |
| NGINX native | Request/response predicates, typed errors, audit latch, actual connection/URI callers, 100 adoption cases | Complete live host/transport/physical-log matrix |
| Apache native | Body predicates and typed errors | Exact intervention result/cleanup, complete physical sink propagation, live host matrix |
| HAProxy HTX | Binding predicates and helper/adoption tests | Direct host control, reset/abort and log failures |
| HAProxy SPOE/SPOP + companion | Common/native body result contracts | SPOP physical write result and separate companion/transport proof |
| Envoy ext_proc | C-bridge first-error latch, checked commitment, empty-body metadata; Go receiver uses checked ABI | Native Go tests and live gRPC/host/log outcomes |
| Envoy ext_authz + companion | Shared Runtime predicate/error replay fixes | Separate request/response-companion and log/transport evidence |
| Traefik middleware/UDS | Shared Runtime predicate/error replay fixes | Middleware/UDS host error and physical sink cases |
| Traefik forwardAuth + companion | Shared Runtime predicate/error replay fixes | Separate companion lifecycle/control/log evidence |
| lighttpd sidecar | Shared Runtime predicate/error replay fixes | Physical sink and actual socket/host behavior |
| lighttpd native/patched profiles | Shared contracts where routed through Runtime | Separate hook availability, unsupported strict admission and native host proof |

Unsupported strict profiles are not silently enabled or treated as successful
log-only. Shared semantics do not imply equal host integers or invented capabilities.

## 5. Documentation and delivery

- [x] D01: Existing Draft PR only; no merge/master/force push.
- [x] D02: Paired EN/DE checklist with separate implementation and verification.
- [ ] D03: Complete all connector guides/examples and compatibility/version review.
- [x] D03a: Paired contract/consumer/hash migration warnings retained.
- [x] D04: Reconcile current source, tests and remaining boundaries; remove the fixed Runtime replay defect from open work and correct unpublished-commit claims.
- [ ] D05: Final release-head document/link/diff/CI and PR/branch reconciliation.

## Revision-scoped evidence

[Job 106897813154](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35772630849/job/106897813154)
for `bced5ce78c62b7665730d2e81b307a3676da42f3` passed the 55/14/10/6/43/9
focused test groups, all 100 NGINX and eight HAProxy adoption cases, configuration
checks, bilingual validation and both exact-head Sonar gates. The old source
assertion expected inline connection/URI branches and failed. This delivery
checks the shared native-failure branch, host-result branch and both caller
orderings explicitly; the original other negative paths remain checked.
The combined source group and lightweight lint therefore need a fresh run (V19).

Earlier evidence is retained in [the checklist at 0532b5eb](https://github.com/Easton97-Jens/ModSecurity-conector/blob/0532b5eb6dac5840b482dbc936ae1cf7a7ccbeb9/docs/pr-382-checklist.md),
[historical job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
and the linked Change Records. Preparation-time pending statements are superseded
only for the revision/test layer explicitly identified here.

No local project commands/builds or local git diff check ran without the required
RTK wrapper. Actual GitHub CI and per-commit comparisons provide the stated evidence.
