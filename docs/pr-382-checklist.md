# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
uses `fix/unified-native-results-events-20260921`, based on
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-09-22.

**Status: implementation in progress; not ready to merge.** An implementation
checkbox means that the stated code exists, not that every host passed an
integration test. Verification has separate checkboxes. Evidence applies only
to the cited revision and layer. Do not substitute another connector's success,
an earlier green check, or a generated report for missing runtime evidence.

Contract and migration reference: [native results and events](pr-382-event-contract.md).

## 1. Implementation

- [x] I01: Add `common/include/msconnector/native_result.h`: direct byte-append results `0` and `1` can continue; other results fail. Phase evaluation succeeds only with `1`. Do not apply this to APR/NGINX/HTTP/Common results or file-loading APIs.
- [x] I02: Adopt the shared append/finish predicates in affected Apache body filters, the HAProxy binding, Common Runtime and the NGINX response-body path.
- [x] I03: Reject undocumented `msc_intervention()` results in Common Runtime and the HAProxy binding while retaining cleanup and failure propagation.
- [x] I04: Preserve a HAProxy response-header binding failure even when its decision is also disruptive.
- [x] I05: Use `event_protocol.h` for the same canonical JSONL and integrity-hash view. Keep original-input validation, query redaction, byte counters, status observations and transport flags.
- [x] I06: Distinguish technical failures from rule blocks in changed Apache/Common event paths; remove Apache's separate handwritten JSON fallback records.
- [x] I07: Add typed NGINX response-body failure events. Do not infer successful EOS from a flag set before native evaluation.
- [x] I08: Map `MSCONNECTOR_ERROR_MODSECURITY_FAILURE` to `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE` in `common/src/modsecurity_engine.c`; preserve other failure classes.
- [ ] I09: Complete NGINX request-body/file paths and remaining native API paths without confusing I/O failure with `ProcessPartial`.
- [ ] I10: Complete the cross-profile `off`/`safe`/`strict` comparison. In particular, a technical failure must not become a successful safe `log_only` decision.
- [ ] I11: Complete producer-to-sink consistency: event IDs, causes, requested versus observed actions, duplicate terminal records, and open/write/short-write/serialization failure handling.
- [x] I11a: For known rule/technical-error events, treat NULL, empty and `not_observable` transport results as missing observation. Clear unobserved `actual_action`; use a neutral `MSCONN_EVENT_ENGINE_DECISION` message for unobserved rule interventions. Preserve original evidence fields and custom events.
- [ ] I12: Verify all direct, companion, middleware and sidecar paths separately; do not infer support from a shared parser or family name.
- [x] I13: Reduce HAProxy intervention/evaluation complexity by extracting bounded Rule-ID decoding and dependency-ordered cleanup. Preserve intervention collection, phase order, logging and cleanup ownership.

## 2. Verification

- [x] V01: Repair duplicate C return types in generated fixtures; retain compiler warnings and assertions.
- [x] V02: Establish the original native-result/event-protocol step at `4f94f33d852f026e703f3237ed98826ae305719a` in [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389).
- [x] V03: Add compiled `tests/test_native_error_classification.py` and wire it into the focused CI step.
- [x] V04: Update NGINX upstream source assertions for shared predicates while retaining terminal failure, abort-before-return, no post-commit replacement response, and no success accounting after append failure.
- [x] V05: Confirm the expanded Common/native-result/error/observation/Sonar-gate tests and Phase-4/NGINX source-security tests at `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` in [run 35634888258, job 106449766690](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888258/job/106449766690). These individual steps passed; the overall job failed on NGINX adoption mutations.
- [ ] V06: Complete both Apache and NGINX adoption/mutation remediation.
- [x] V06a: Repair Apache helper-aware adoption checks and preserve existing negative mutations. Add inverted append/phase, missing serialization-return and false technical-rule-block mutations. All 16 mutation tests and scoped guards passed at `1709e1def4706f0124d56fc687b3faf1fd8e2946` in [run 35633647191, job 106445635579](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35633647191/job/106445635579); that job subsequently failed at the NGINX checker. A later source-equivalent linear status check is part of `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` and requires its own full validation.
- [x] V06b: Repair the NGINX chain-error checker and its stale mutation fragments. Copy the actual private Phase-4 error header into isolated fixtures, retain all 96 existing tests, add four regressions, and require exact `FAIL:` diagnostics. The full mutation step passed at `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` in [run 35696836181, job 106645456958](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836181/job/106645456958). The overall lint job failed later; see the dated continuation below.
- [ ] V07: Pass every required check and review for the final PR head. The overall CI is not green.
- [ ] V08: Run identical real-host cases for engine `ProcessPartial`, engine Reject/interventions, empty responses, multiple chunks with one EOS, explicit CSV MIME selection, optional budgets and engine errors.
- [ ] V09: Verify late safe/strict and pre/post-commit errors per supported transport, observing client bytes, abort/reset, neighbor-stream survival, cleanup and JSONL rather than HTTP status alone.
- [ ] V10: Compare metadata logs from every real integration route, including invalid/oversized metadata, failed sinks and missing transport observations.
- [x] V11: Compile and run `tests/test_event_transport_observation.py` against actual Common JSONL/hash code. It checks missing observation, preserved evidence, idempotency, redaction, and observed safe/abort controls. Six family labels are fixture identities, not six running hosts.
- [x] V12: Run all eight extracted HAProxy evaluation/cleanup/Rule-ID tests and the existing binding compile-and-link compatibility check at `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` in [run 35634888103, job 106449767189](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35634888103/job/106449767189).

## 3. Sonar zero-finding requirement

- [x] S01: Add an exact-head, read-only zero-finding check instead of accepting a green Quality Gate with findings. Missing, stale, ambiguous or unfinished evidence cannot pass.
- [x] S02: Test the guard, including invalid identity before network access, safe bounded annotation output, wrong provider, pending analysis and nonzero findings. Keep `checks: read` at job scope.
- [x] S03: Confirm `039b7f123ff5ce87c033ce805b9f7e07b7d44bb4` has **0 new issues, 0 accepted issues, 0 Security Hotspots and 0 annotations** in [Sonar check 106450287547](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106450287547). The exact-head zero-finding CI step also passed in the V05 job. No issue was accepted, hidden or excluded to obtain this result.
- [x] S03a: Confirm the same four zero counts for `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d` in [Sonar check 106645541548](https://github.com/Easton97-Jens/ModSecurity-conector/runs/106645541548). The exact-head zero-finding step passed in the V06b job.
- [ ] S04: Repeat the exact-head zero check after every later change, including the final documentation commit. Keep final-head evidence separate from S03 and S03a.

This is the PR's new-code finding inventory, not a claim that the complete
historical project inventory or measured test-coverage gap is zero. Sonar
reported 0.0% coverage on new code; compiled test results are separate evidence.

## 4. State by family

| Family | Implemented part | Still required |
| --- | --- | --- |
| Apache | Body predicates, typed events, updated adoption checks and negative mutations | Final-head full checks and native host/log regressions |
| NGINX | Response predicates, typed failure events and repaired adoption/mutation checks | Remaining request/event and cross-route completion, separate syntax guard, host/transport regressions |
| HAProxy | Direct binding predicates, failure propagation, bounded Rule-ID/cleanup refactor | Separate HTX and SPOE/SPOP/companion behavior and event evidence |
| Envoy | Native return correction through Common Runtime | Separate ext_proc and ext_authz/response-companion verification |
| Traefik | Native return correction through Common Runtime | Native middleware/UDS and forwardAuth/response-companion verification |
| lighttpd | Native return correction through Common Runtime | Separate sidecar and native/patched-profile verification |

Unsupported strict profiles stay unsupported until actual host capability is
implemented and tested. Shared semantics do not mean identical host return
integers, log-sink prefixes, or invented abort/reset capabilities.

## 5. Documentation and delivery

- [x] D01: Keep work in Draft PR #382; no merge or direct `master` push.
- [x] D02: Maintain paired EN/DE checklists with separate implementation and verification states.
- [ ] D03: Complete all affected connector guides, examples and compatibility/versioning review before release.
- [x] D03a: Add the paired native-result/event contract guide with missing-observation semantics, consumer migration notes, integrity-hash compatibility warnings and the Sonar-zero requirement.
- [x] D04: Update the bilingual [Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md) and PR progress with actual revision-scoped results.
- [ ] D05: Finish final documentation/link/diff checks and all final-head CI. Reconcile branch and PR heads at handoff.

## Observed commands and results

The following two commands passed as individual CI steps at the V05 revision:

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification tests.test_event_transport_observation tests.test_sonar_zero_gate
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
```

The following commands passed at the V12 revision:

```sh
python3 -m unittest -v tests.test_haproxy_binding_refactor
python3 tests/test_haproxy_libmodsecurity_compat.py
```

The following exact-head check passed at the S03 revision:

```sh
python ci/checks/common/check-sonar-zero.py
```

## 2026-09-22 continuation: NGINX adoption mutations

The tested revision is `f7aa2f2ccf929f226a6b0ad7b9ff0700b71c367d`.
This step changes only the NGINX adoption checker and its mutation tests, not
runtime code, workflows, dependencies or security policy. A concurrent identical
checker correction at `7bd3b2355c84bc6bd630de6b19ea6115b5eb64f2` was preserved;
the fixture commit builds on it without a force push.

In the V06b CI job, `python -m unittest -v tests.test_nginx_common_adoption`
passed. New regressions cover a byte-identical private-header copy, missing
header, a forbidden macro in that header, and discarded terminal-dispatch
results. Negative cases require exit status 1 and their precise `FAIL:` line;
an unrelated failure or a matching `PASS:` label cannot satisfy that assertion.
The request-native, late-error/reentry, Phase-4/security, configuration-reference
and Sonar-zero steps also passed on this revision.

| Evidence layer | Observed result | Limitation |
| --- | --- | --- |
| Full NGINX adoption/mutation step | `passed` in V06b job | Source-contract and isolated mutation evidence, not a live host run |
| NGINX scaffold and Common-contract checks | `passed` in [run 35696836186, job 106645456976](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35696836186/job/106645456976) | Separate native syntax/regression guard subsequently failed |
| NGINX native syntax/regression guard | `failed` in the same NGINX job | A request-body assertion still expects `if (ret != 1)`; its owning source was not repaired in this step |
| Overall lint | `failed` in V06b job | Later `Run lightweight lint` failure; its root cause is not established by the mutation-step pass |
| Exact-head Sonar analysis | `passed`, four zero counts in S03a | Applies only to the tested SHA, not a later documentation head |

V06b is complete at its stated evidence layer. V06 remains open for complete
combined adoption validation; V07 and the runtime/profile criteria remain open.
No complete six-family live HTTP/transport matrix, local native build, or local
`git diff --check` is claimed. The required local RTK execution path was not
available; validation used GitHub CI. A later documentation commit needs its own
fresh checks rather than inheriting this revision's results.
