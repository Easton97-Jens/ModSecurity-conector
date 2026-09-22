# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382),
branch `fix/unified-native-results-events-20260921`, base
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-09-22.

**Implementation remains in progress; not ready to merge.** Implementation and
verification are separate. Every result below applies only to its cited revision
and test layer, not to all live hosts or a later commit.

Code/test checkpoint: `47714de09bf1f9326862447f794194045828f29d`.
Latest confirmed Sonar-zero revision: `47714de09bf1f9326862447f794194045828f29d`.
A following documentation commit needs its own CI/Sonar confirmation.
The four parent items I09-I12 remain open: completed subsets are not a claim
that every native API, physical sink and integration route is finished.

References: [contract and migration](pr-382-event-contract.md) and
[Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md).

## 1. Implementation

- [x] I01: Shared native result helpers accept only `0`/`1` for direct byte append and only `1` for phase success. Preserve separate APR, NGINX, HTTP, Common and file-loading contracts.
- [x] I02: Shared predicates in affected Apache body filters, HAProxy binding, Common Runtime and NGINX response paths.
- [x] I03: Validate Common/HAProxy native intervention results with cleanup and error propagation.
- [x] I04: Preserve HAProxy response-header binding failures even when disruptive.
- [x] I05: Canonical event view for JSONL/hash, original-input validation and query redaction; preserve counters and observations.
- [x] I06: Distinguish technical errors from rule blocks in changed Apache/Common events; remove handwritten Apache JSON fallback records.
- [x] I07: Typed NGINX response-body failure events; do not infer successful EOS from a pre-evaluation flag.
- [x] I08: Map native engine failure to invalid-engine-response while retaining other error classes.
- [ ] I09: Complete remaining native/API and typed request-event routes; the NGINX subset below is not full request-event consistency.
- [x] I09a: NGINX partial byte ingestion, separate strict file result handling, cumulative file/body bounds, success-only phase completion and terminal failed request re-entry. Implemented through `fcbaca03`; V13 tests.
- [x] I09b: Typed NGINX request failures retain first cause/status and one event attempt, distinguish host/URI failures from real rules, and tolerate absent storage for a legitimate empty body. Native intervention collection validates exact return values before classification and cleanup. Present at `7fe606c5`; refreshed V17 evidence.
- [x] I09c: Native NGINX audit completion accepts only one, records its attempt before callbacks, retains failed outcomes on re-entry and preserves earlier causes. Missing native state never reaches the engine; canonical completion failure remains failure even if native logging succeeds. Implemented at `47714de0`; V17 evidence.
- [ ] I10: Complete cross-profile `off`/`safe`/`strict` consistency, including native and host failures.
- [x] I10a: NGINX negative late interventions and phase/control failures remain technical errors before Safe/Strict rule policy. Implemented in `52445b18`; V14 tests.
- [x] I10b: Common error-status precedence and technical-failure policy reject before commitment and stop I/O after commitment rather than becoming successful Safe log-only. Real Common tests cover five error classes across ten registered profiles, two contract modes and both commitment states. This does not itself prove adapter I/O.
- [x] I10c: The real NGINX collector/dispatcher/P4 caller distinguishes legitimate late Safe/Strict rules from invalid native results, retains Off's native path and preserves cleanup. Repair the missing real `http_status.c` test dependency at `1ce569e1`, without weakening the ten original assertions.
- [ ] I11: Complete producer/sink parity: event IDs/causes, requested and observed actions, duplicate terminal events and log open/write/short-write/serialization errors.
- [x] I11a: NULL, empty and `not_observable` transport values are missing evidence for known rule/error events. Empty unobserved `actual_action`; neutral `MSCONN_EVENT_ENGINE_DECISION` for unobserved rule interventions; preserve custom events and evidence fields.
- [x] I11b: NGINX mandatory Phase-4 log failures remain terminal; guard disabled/invalid sinks, bound terminal write attempts and synchronous core error-response re-entry. This does not establish global sink equivalence.
- [x] I11c: Apply the missing-observation boundary to body-limit, unsupported-capability, client-cancel and upstream-disconnect events. Retain their category, phase-specific cause, observed controls and source evidence. Real JSONL/hash tests include a compiled guard-removal negative control. Implemented at `3730eaa0`; V18 evidence.
- [ ] I12: Verify direct, companion, middleware and sidecar routes separately; do not infer capability from parser or family name.
- [x] I13: Bounded HAProxy Rule-ID decoder and dependency-ordered cleanup extracted without changing phase order or ownership.
- [x] I14: NGINX checker and isolated fixtures follow the terminal helper; retain 96 tests and add four regressions.
- [x] I15: HAProxy checker follows the actual bounded decoder and callsite; eight isolated regressions added to PR lint. No native runtime change in this slice.

### Concrete remaining implementation boundaries

| Parent item | Remaining boundary |
| --- | --- |
| I09 | Audit the remaining native/host error exits outside the completed NGINX paths, including failures that currently produce only host diagnostics. A checked native predicate is not a typed event at every caller. |
| I10 | Verify each native, companion and middleware error result reaches its actual host control path without a successful policy fallback. Common profile tests alone do not establish this. |
| I11 | Apache `apache_intervention_write_event()` and its void event callers still warn on sink failures without returning them through the complete host flow. HAProxy SPOP's Common-event tail still ignores `fputs()` success. Common Runtime's failed-write latch currently re-reports prior sink failures as serialization/event-size errors rather than retaining the original I/O class. These require source changes and failure-injection tests, not only documentation. |
| I12 | Complete distinct checks for all direct/companion/middleware/sidecar routes, including physical sinks and host commitment/termination. Do not mark a request-only route as response-complete without its companion. |

## 2. Verification

- [x] V01: Repair generated C return types without disabling warnings/assertions.
- [x] V02: Original native/event step passed at `4f94f33d` in [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Compiled native-error-classifier regressions and CI wiring added.
- [x] V04: Preserve source assertions for terminal failures, no second post-commit response and no successful accounting after a failed append.
- [x] V05: Focused native/event/classifier/observation/gate-unit and Phase-4/security suites passed at `092dfd1c`; see historical evidence table.
- [ ] V06: Complete combined final-release-head adoption and mutation verification.
- [x] V06a: Apache helper checks and 16 negative mutations passed at `1709e1de` in [job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579). `test-apache` and `test-common` passed at `092dfd1c`; these are not live Apache evidence.
- [x] V06b: All 100 NGINX adoption tests passed at `f7aa2f2c` in [job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958), and again at `092dfd1c`.
- [ ] V07: Pass every required check and review for the final release head.
- [ ] V07a: Resolve the independent secret-scan finding reported for `91f07e12` by [job 106651564952](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35698779824/job/106651564952). The available log reports one finding without its location; no false-positive disposition or exception is approved. The secret-scan workflow still fails at `47714de0`.
- [ ] V08: Run equal real-host cases for engine ProcessPartial/Reject, empty responses, multiple chunks/one EOS, CSV MIME, budgets and native errors.
- [ ] V09: Verify supported late safe/strict and pre/post-commit failures, client bytes, resets, neighbor streams and cleanup.
- [ ] V10: Compare actual route metadata logs, invalid/oversized input, missing observations and failed sinks.
- [x] V11: Compiled actual Common JSONL/hash observation tests retain redaction/evidence; six fixture names are not six host runs.
- [x] V12: Eight compiled HAProxy helper tests and binding compile/link checks passed at `039b7f12` in [job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Nine NGINX request/file result tests passed at `092dfd1c`, with controlled host/native seams, not a native file-reader integration test.
- [x] V14: Nine NGINX late-error/re-entry tests passed at `092dfd1c`, not a full HTTP transport matrix.
- [x] V15: Eight HAProxy adoption tests passed at `092dfd1c`, including baseline acceptance and unsafe decoder/callsite mutations.
- [x] V16: Bilingual Change Record/template validation passed again at `47714de0` in the current evidence job below; no documentation validator was weakened.
- [x] V17: At `47714de0`, the request/native step passed all five modules: request results, typed request errors, context accounting, ten real intervention-chain tests and eight new native logging tests. The failed native-chain setup at `7fe606c5` was corrected by linking the actual HTTP-status implementation.
- [x] V18: At `47714de0`, the expanded Common/native/event/profile step passed, including ten observation tests and the compiled non-rule guard-removal negative control. The late-error and Phase-4/security steps passed separately.

## 3. Sonar zero-finding requirement

- [x] S01: Retain read-only exact-head/provider-checked zero gate; reject missing, stale, ambiguous, unfinished and nonzero results.
- [x] S02: Preserve negative gate tests and job-scoped `checks: read`; no scanner exclusions, accepted issues or weaker rules.
- [x] S03: Historical `039b7f12` analysis reported 0 new/accepted issues, hotspots and annotations in [check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547).
- [x] S03a: Exact-head zero gate passed for `f7aa2f2c` in V06b's job.
- [x] S03b: [Check 106651947571](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106651947571) confirms 0 new issues, 0 accepted issues, 0 hotspots and 0 annotations for `91f07e124fe09056dc46dc59d65693f406b4b1a1`.
- [x] S03c: [Check 106837589312](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106837589312) confirms the same four zero counts for exactly `47714de09bf1f9326862447f794194045828f29d`.
- [ ] S04: Confirm fresh exact-head Sonar zero for each later delivery, including documentation changes. No earlier analysis satisfies a later SHA.

Sonar at `47714de0` reports 0.1% new-code duplication and 0.0% coverage. Findings,
duplication and coverage are separate metrics. Sonar zero does not clear V07a or
prove the whole project's historical issue inventory is zero.

## 4. State by family

| Family | Implemented subset | Remaining |
| --- | --- | --- |
| Apache | Body predicates, typed errors, helper adoption/negative checks | Propagated physical sink failures and final-head native host/log matrix |
| NGINX | Typed request/response errors, native collector validation, separate file handling, late-error/re-entry protection, once-only native audit completion | Remaining sink/producer comparison and live transport evidence |
| HAProxy | Binding results, error propagation, Rule-ID/cleanup helpers, adoption tests | SPOP event write propagation and separate HTX/SPOE/companion behavior/log evidence |
| Envoy | Correct native results and error policy through Common Runtime | Original sink-error retention and separate ext_proc/ext_authz-companion validation |
| Traefik | Correct native results and error policy through Common Runtime | Original sink-error retention and middleware/UDS/forwardAuth-companion validation |
| lighttpd | Correct native results and error policy through Common Runtime | Original sink-error retention and sidecar/native/patched-profile validation |

Unsupported strict profiles remain unsupported. Shared semantics do not imply
identical host integers, native log prefixes or invented abort capability.

## 5. Documentation and delivery

- [x] D01: Work stays in Draft PR #382; no merge or master push.
- [x] D02: EN/DE checklist maintained with separate implementation and verification.
- [ ] D03: Finish connector guides/examples and compatibility/version review.
- [x] D03a: Paired native/event contract and consumer/hash migration warnings maintained; new continuation records below describe the additional observation and native-audit behavior.
- [x] D04: Reconcile checklist and Change Records with actual commits/results; preserve historical evidence in the record and Git history.
- [ ] D05: Finish final-head document/link/diff/CI checks and PR/branch reconciliation.

## Current continuation evidence

[Lint job 106836835538](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35754528427/job/106836835538)
for `47714de09bf1f9326862447f794194045828f29d` passed bilingual validation and
all focused Common/native/request/logging/late-error/security steps at the last
inspection. That observation did not yet establish the whole job's final status.
The full earlier [lint run 35753875384](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35753875384)
passed at `1ce569e1afce55e17c767e1e06b0266874fe8c3e`; it is not evidence for later
native logging changes. The new physical sink gaps in the implementation table
remain open regardless of green focused tests.

Continuation records:
[observation parity](../reports/audits/change-records/CR-20260922-pr382-nonrule-observation.md),
[native-chain linkage](../reports/audits/change-records/CR-20260922-pr382-chain-link.md),
[native audit logging](../reports/audits/change-records/CR-20260922-pr382-native-logging.md).
Their preparation-time pending statements are superseded only by the specific
revision-scoped results above, not by an unqualified claim of completion.

## Historical revision-scoped evidence

[Lint job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
for `092dfd1c8937f9712c03da011e61f1e4eab31840` passed these individual groups:

| Group | Result | Layer |
| --- | --- | --- |
| Native/event/classifier/observation/Sonar-gate unit tests | 29 passed | Not remote Sonar analysis |
| NGINX request/file results | 9 passed | Controlled host/native tests |
| NGINX late errors/re-entry | 9 passed | Controlled host/log tests |
| Phase-4 and NGINX security contracts | 33 passed | Source contracts |
| NGINX adoption/mutations | 100 passed | Isolated source mutations |
| HAProxy Rule-ID adoption | 8 passed | Isolated checker tests |
| Configuration references | Passed | Regression/generation/semantics |

`test-common`, `test-apache`, `quick-framework-check` and `test-nginx` also passed
at `092dfd1c`; NGINX syntax/dry-run evidence is in
[job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305).
The prior f7aa lint failure came from obsolete HAProxy probes, repaired without
suppressions in `092dfd1c`. The following documentation update exposed V16 and
the separate V07a security finding. Its Sonar result is recorded separately in
S03b; the overall CI is not claimed green.

No local project commands/builds or local `git diff --check` were executed because
the mandatory RTK wrapper was unavailable. Verification uses GitHub CI and remote
commit comparisons. Full six-family live-host/transport verification remains open.
