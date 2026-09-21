# PR #382: shared connector behavior checklist

**Language:** English | [Deutsch](pr-382-checklist.de.md)

[Draft PR #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382)
works on `fix/unified-native-results-events-20260921`, based on
`5170d24801243cdcd7bf1bca6123bf8cb2c72386`. Updated: 2026-09-21.

**State: implementation in progress; not ready to merge.** A checked item in
Implementation means the described code is present, not that every host has
passed an integration test. Verification has its own checklist. Never check an
item merely because a job exists, a build starts, or another connector passed.
Every test result below belongs only to its named revision and test layer.

## 1. Implementation

- [x] I01: Add `common/include/msconnector/native_result.h`: direct byte-append results `0` and `1` may continue; other results fail. Phase evaluation succeeds only on `1`. Do not apply the append rule to APR/NGINX/HTTP/Common return values or file-loading APIs.
- [x] I02: Use the shared append/finish predicates in the affected Apache body filters, HAProxy binding, Common Runtime, and NGINX response-body path.
- [x] I03: Reject undocumented `msc_intervention()` return values in the Common Runtime and HAProxy binding, retaining cleanup and failure propagation.
- [x] I04: Keep a HAProxy response-header binding failure a failure even when the decision is also disruptive.
- [x] I05: Add `event_protocol.h` and use the same canonical event view in the JSONL writer and integrity hash. Preserve original source validation, query redaction, byte counts, status observations, and transport flags.
- [x] I06: Distinguish technical errors from rule blocks in the changed Apache/Common event paths; remove Apache's separate handcrafted JSON fallback records.
- [x] I07: Add typed NGINX response-body failure events. Do not infer successful EOS from a flag set before native evaluation.
- [x] I08: Map `MSCONNECTOR_ERROR_MODSECURITY_FAILURE` to `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE` in `common/src/modsecurity_engine.c`; retain distinct host, timeout, unavailable-engine, protocol, and body-limit classes.
- [ ] I09: Complete the NGINX request-body/file and remaining native API paths without mistaking an I/O failure for `ProcessPartial`.
- [ ] I10: Finish the cross-profile `off`/`safe`/`strict` comparison. In particular, no technical failure may become a successful Safe `log_only` decision.
- [ ] I11: Complete the producer-to-sink error/logging comparison: event IDs, causes, requested versus observed actions, duplicate terminal events, and log-open/write/short-write/serialization failures. Treat `not_observable` as missing transport evidence, not proof of an executed block.
- [ ] I12: Review all direct, companion, middleware, and sidecar paths separately; do not infer support from a shared parser or a connector family name.

## 2. Verification

- [x] V01: Fix duplicate C return types in generated test fixtures. `function_definition()` already includes the return type for the extracted Common definitions.
- [x] V02: Observe a successful `Verify native results and common event protocol` CI step at `4f94f33d852f026e703f3237ed98826ae305719a`, [run 35627469389](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35627469389). This exercises compiled helpers, real serializer/hash code, extracted Runtime callbacks, and source wiring, not six running hosts.
- [x] V03: Add `tests/test_native_error_classification.py` and wire it into the existing focused lint step. The compiled fixture tests the real classifier with recording clock/contract collaborators.
- [x] V04: Update NGINX upstream source assertions for the shared predicates while retaining explicit checks for terminal failure, abort-before-return, no post-commit replacement response, and no success accounting on append failure.
- [x] V05: Observe successful focused Common and Phase-4/NGINX security steps at implementation revision `10b3379561de81a8018467b724b4edb8c8742ef2`, [run 35628608293, job 106429001084](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35628608293/job/106429001084). Commands and evidence scope appear below. Later checklist/Change Record commits are documentation only; final-head CI remains a separate requirement.
- [ ] V06: Repair and rerun Apache adoption checks and NGINX adoption/mutation tests. Retain negative mutation coverage; do not disable the checks to obtain a pass.
- [ ] V07: Pass all required current-head CI and resolve actionable review/Sonar findings. Earlier green checks are not current-head evidence.
- [ ] V08: Run identical real-host cases for engine `ProcessPartial`, engine Reject/interventions, empty response, multiple chunks and one EOS, selected CSV MIME type, optional connector budget, and engine failures.
- [ ] V09: Validate late Safe/Strict outcomes and failures before/after commitment per supported transport. Observe client bytes, abort/reset, neighboring-stream survival, cleanup, and matching JSONL events rather than HTTP status alone.
- [ ] V10: Compare metadata-only log records from each real integration route, including malformed/oversized metadata, failed sinks, and absent transport observations.

## 3. Per-family status

| Family | Implemented portion | Still required |
| --- | --- | --- |
| Apache | Body append/finish predicates and changed failure/event handling | Adoption checks, full native build and host/log regression tests |
| NGINX | Response-body predicates and typed failure event | Remaining request/file paths, adoption mutations, host/transport regressions |
| HAProxy | Direct binding predicates and error/intervention propagation | Separate HTX and SPOE/SPOP/companion behavior and event verification |
| Envoy | Native return fix through Common Runtime | Separate ext_proc and ext_authz/response-companion verification |
| Traefik | Native return fix through Common Runtime | Native middleware/UDS and forwardAuth/response-companion verification |
| lighttpd | Native return fix through Common Runtime | Separate sidecar and native/patched-profile verification |

Unsupported Strict profiles remain unsupported unless an actual host capability
is implemented and tested. Identical semantics do not mean identical host API
return integers, log destination prefixes, or fabricated abort capabilities.

## 4. Documentation and delivery

- [x] D01: Keep the work in Draft PR #382; do not merge or push directly to `master`.
- [x] D02: Add this English/German checklist with reciprocal links and separate implementation/verification status.
- [ ] D03: Complete the shared contract/migration documentation, log examples, and affected connector EN/DE guides.
- [x] D04: Add the bilingual [Change Record](../reports/audits/change-records/CR-20260921-pr382-native-results-events.md) with actual results. The PR description links the checklist rather than treating the initial single-header commit as the current scope.
- [ ] D05: Complete final new-documentation/link validation, scoped whitespace check, and required final-head checks. Record branch/PR head equality at handoff.

## Observed commands and results

Both commands below passed as GitHub CI steps at
`10b3379561de81a8018467b724b4edb8c8742ef2`, in the run linked under V05.

```sh
python -m unittest -v tests.test_native_result_event_protocol tests.test_native_error_classification
python -m unittest -v tests.test_phase4_migration_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract
```

These are compiled helper/callback/classifier and source-contract tests. The
first group uses actual serializer/hash code and the extracted Runtime/classifier
functions; surrounding native APIs or contract sinks are controlled fixtures.
They do not prove the full native host lifecycle or transport behavior.

## Known blockers and evidence limits

The original fixture compilation defect and the two outdated NGINX upstream
assertions are repaired. The NGINX adoption checker/mutations and Apache
adoption checks still need updates for the changed paths. Related `test-common`,
`test-apache`, `test-nginx`, and `quick-framework-check` workflows failed at
`10b3379561de81a8018467b724b4edb8c8742ef2`. They remain open, not accepted failures.

No local native host build or full six-family HTTP matrix was performed during
this continuation. The local project execution wrapper was unavailable; GitHub
CI is the execution evidence. Do not interpret a fixture using six connector
names as six host integrations, or a successful quality gate as runtime proof.

## Update rule

Before changing a verification box to `[x]`, record the exact commit, command,
run/job link, and successful terminal result. Keep the German companion equivalent.
A subsequent behavioral change requires new validation; historical evidence
must remain labeled historical. Changes to Framework/MRTS, dependencies,
security gates, or merge state are outside this PR continuation's scope.
