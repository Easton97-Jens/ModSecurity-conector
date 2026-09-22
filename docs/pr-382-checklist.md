# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
uses `fix/unified-native-results-events-20260921`, based on
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-09-22.

**Status: implementation in progress; not ready to merge.** Checked implementation
items mean that the stated code exists. Verification is tracked separately and
applies only to the cited revision and layer. Source tests, workflow names and
six fixture identities are not proof of six running hosts.

Latest code/test checkpoint: `092dfd1c8937f9712c03da011e61f1e4eab31840`.
The following documentation commit must obtain its own CI and Sonar results;
it cannot inherit a previous head's success.

References: [contract and migration](pr-382-event-contract.md) and
[Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md).

## 1. Implementation

- [x] I01: Add `common/include/msconnector/native_result.h`: direct byte-append results `0` and `1` can continue; other results fail. Phase evaluation succeeds only with `1`. Preserve separate APR, NGINX, HTTP, Common and file-loading contracts.
- [x] I02: Use shared append/finish predicates in affected Apache body filters, HAProxy binding, Common Runtime and NGINX response-body paths.
- [x] I03: Reject undocumented `msc_intervention()` results in Common Runtime and HAProxy while retaining cleanup and error propagation.
- [x] I04: Preserve a HAProxy response-header binding failure even when its decision is disruptive.
- [x] I05: Use the same `event_protocol.h` view for JSONL and integrity hashing. Retain original-input validation, query redaction, counters, status observations and transport flags.
- [x] I06: Distinguish technical failures from rule blocks in changed Apache/Common events; remove separate handwritten Apache JSON fallback records.
- [x] I07: Add typed NGINX response-body failure events; do not infer successful EOS from a pre-evaluation flag.
- [x] I08: Map `MSCONNECTOR_ERROR_MODSECURITY_FAILURE` to `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE`; preserve other error classes.
- [ ] I09: Finish remaining native/API and request-event routes. The completed NGINX subset below does not establish full request-side event consistency or every integration route.
- [x] I09a: NGINX byte-append accepts valid partial ingestion; file loading keeps its separate strict result check and cumulative limit. Complete request phases only after native success and keep failed request re-entry terminal. Implemented through `fcbaca03`, tested in V13.
- [ ] I10: Complete cross-profile `off`/`safe`/`strict` consistency, including native and host failures.
- [x] I10a: NGINX negative late interventions and phase/control failures remain technical errors before Safe/Strict rule policy. Implemented in `52445b18`, tested in V14.
- [ ] I11: Complete producer-to-sink consistency across routes: event IDs, causes, requested/observed actions, duplicate terminal records and open/write/short-write/serialization failures.
- [x] I11a: Known rule/error events treat NULL, empty and `not_observable` transport values as missing evidence. Leave unobserved `actual_action` empty and use neutral `MSCONN_EVENT_ENGINE_DECISION` for unobserved rule interventions. Preserve evidence fields and custom events.
- [x] I11b: NGINX Phase-4 mandatory log failures remain terminal. Guard disabled/invalid sinks, bound terminal write attempts and permit only the synchronous core-generated error-response re-entry. This is not a claim of global sink equivalence.
- [ ] I12: Verify direct, companion, middleware and sidecar routes separately; do not infer capabilities from the common parser or family name.
- [x] I13: Extract bounded HAProxy Rule-ID decoding and dependency-ordered cleanup without changing phase order, intervention collection or ownership.
- [x] I14: Adapt the NGINX chain checker and isolated mutation fixtures to the actual terminal helper; preserve 96 existing tests and add four regressions.
- [x] I15: Adapt HAProxy Rule-ID adoption checks to the extracted decoder and its callsite; add eight isolated regression tests to PR lint. No native runtime behavior changes in this slice.

## 2. Verification

- [x] V01: Repair generated C fixture return types without disabling compiler warnings or assertions.
- [x] V02: Original native/event step passed at `4f94f33d852f026e703f3237ed98826ae305719a` in [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Add compiled native-error-classifier tests and CI wiring.
- [x] V04: Keep NGINX source assertions for terminal failures, no second post-commit response and no success accounting after a failed append.
- [x] V05: Focused native/event/classifier/observation/Sonar tests and Phase-4/security assertions passed at the latest checkpoint; see the evidence table. Earlier evidence at `039b7f12` remains historical, not final-head proof.
- [ ] V06: Finish final-head combined adoption/mutation verification; the scoped repairs and their evidence are below.
- [x] V06a: Apache helper-aware checks and 16 negative mutations passed at `1709e1de` in [job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579). The `test-apache` and `test-common` workflows also passed at `092dfd1c`; this does not establish live Apache behavior.
- [x] V06b: All 100 NGINX adoption/mutation tests passed at `f7aa2f2c` in [job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958), and the step passed again at `092dfd1c`. Exact `FAIL:` diagnostics and private-header fixture checks remain required.
- [ ] V07: Pass all required checks and reviews on the eventual release head. Pending analysis and runtime jobs are not green evidence.
- [ ] V08: Run identical real-host cases for engine `ProcessPartial`, Reject/interventions, empty responses, multiple chunks/one EOS, explicit CSV MIME selection, optional budgets and engine errors.
- [ ] V09: Verify late safe/strict and pre/post-commit errors per supported transport, including client bytes, abort/reset, neighbor streams, cleanup and JSONL.
- [ ] V10: Compare real-route metadata logs, invalid/oversized inputs, missing observations and failed sinks.
- [x] V11: Compile observation regressions against actual Common JSONL/hash code, including redaction and preserved evidence. Fixture family labels are not independent host runs.
- [x] V12: Eight compiled HAProxy evaluation/cleanup/Rule-ID tests and binding compile/link checks passed at `039b7f12` in [job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).
- [x] V13: Nine NGINX request/file result regressions passed at `092dfd1c`. Controlled native/host seams, not a native file-reader integration test.
- [x] V14: Nine NGINX late-error/re-entry regressions passed at `092dfd1c`. Controlled host/log seams, not a complete HTTP transport matrix.
- [x] V15: Eight HAProxy adoption regressions passed at `092dfd1c`: baseline acceptance, initialization, failed/zero extraction, conversion bounds, comments, early return and missing helper call.

## 3. Sonar zero-finding requirement

- [x] S01: Keep the read-only exact-head zero-finding gate. Stale, missing, ambiguous, unfinished or nonzero results cannot pass.
- [x] S02: Retain negative gate tests and job-scoped `checks: read`; no scanner exclusions, accepted issues or weakened rules.
- [x] S03: Historical `039b7f12` analysis reported 0 new issues, 0 accepted issues, 0 Security Hotspots and 0 annotations in [check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547).
- [x] S03a: The exact-head zero-finding step passed for `f7aa2f2c` in the V06b job.
- [ ] S04: Obtain fresh exact-head Sonar-zero evidence for every later delivery, including the final documentation head. At this documentation checkpoint the latest analysis was not yet confirmed; do not reuse S03/S03a as a later head's result.

Zero findings does not mean zero historical project issues, zero duplication or
measured full test coverage. Report those metrics separately when available.

## 4. State by family

| Family | Implemented part | Still required |
| --- | --- | --- |
| Apache | Body predicates, typed errors, adoption checks and negative mutations | Final-head checks and native host/log regression matrix |
| NGINX | Request/response predicates, separate file result handling, late technical-error/re-entry protection, Phase-4 failure events, repaired adoption tests | Complete typed request-event and other route/sink behavior; live host/transport evidence |
| HAProxy | Binding predicates, preserved failures, bounded Rule-ID/cleanup helpers and helper-aware adoption tests | Separate HTX and SPOE/SPOP/companion behavior and event evidence |
| Envoy | Correct native results through Common Runtime | Separate ext_proc and ext_authz/response-companion validation |
| Traefik | Correct native results through Common Runtime | Native middleware/UDS and forwardAuth/response-companion validation |
| lighttpd | Correct native results through Common Runtime | Separate sidecar and native/patched-profile validation |

Unsupported strict profiles remain unsupported. Shared semantics do not imply
identical host return integers, native log prefixes or invented abort capability.

## 5. Documentation and delivery

- [x] D01: Work remains on Draft PR #382; no merge or direct master push.
- [x] D02: Maintain paired EN/DE checklists and preserve separate implementation/verification status.
- [ ] D03: Finish affected connector guides, examples and compatibility/versioning review before release.
- [x] D03a: Maintain paired native/event contract and migration notes, including consumer and integrity-hash compatibility warnings.
- [x] D04: Reconcile Change Record and checklist with the actual commits and CI; retain revision-scoped historical evidence.
- [ ] D05: Complete all final-head documentation/link/diff/CI checks and reconcile PR/branch heads at handoff.

## Latest observed evidence: 2026-09-22

[Lint job 106648735070](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893254/job/106648735070)
for `092dfd1c8937f9712c03da011e61f1e4eab31840` passed these individual steps:

| Command or group | Result | Layer |
| --- | --- | --- |
| Native results, events, classifier, observations and Sonar-gate unit tests | Passed | 29 focused tests; not the remote analysis itself |
| `python -m unittest -v tests.test_nginx_request_native_results` | Passed | 9 controlled native/host tests |
| `python -m unittest -v tests.test_nginx_late_error_results` | Passed | 9 controlled late-error tests |
| Phase-4 migration and NGINX source-security suites | Passed | 33 source-contract tests |
| `python -m unittest -v tests.test_nginx_common_adoption` | Passed | 100 isolated adoption/mutation tests |
| `python -m unittest -v tests.test_haproxy_adoption_rule_id` | Passed | 8 isolated checker tests |
| Configuration regression/generation/semantics steps | Passed | Source/generated reference validation |

The preceding `f7aa2f2c` lint failure was traced to two obsolete HAProxy Rule-ID
spelling probes. Commit `092dfd1c` repairs those probes and adds negative tests;
it does not suppress the checks. The NGINX syntax/dry-run step in
[job 106648735305](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35697893302/job/106648735305)
and `test-common`, `test-apache` and `quick-framework-check` also passed at that
checkpoint. These results supersede older failure descriptions for those checks,
not the remaining live-host or final-head requirements.

At documentation preparation, remote Sonar confirmation and the overall lint
conclusion were still pending. Later results belong to their actual SHA and
must be read from GitHub rather than inferred here. No local project commands,
local native builds or local `git diff --check` were run because the required
RTK execution wrapper was unavailable. No full six-family runtime matrix is claimed.
