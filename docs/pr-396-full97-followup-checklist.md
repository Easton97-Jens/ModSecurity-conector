# PR #396 — Full97 follow-up

**Language:** English | [Deutsch](pr-396-full97-followup-checklist.de.md)

Updated 2026-10-10. The fresh local standard Full97 R17 meets its declared acceptance criteria: **Canonical PASS, 97/97 Required-PASS**, including directly measured generic Strict-client completion. The [public R17 report](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396#issuecomment-6101794434) was published before this documentation change. [Parent PR #396](https://github.com/Easton97-Jens/ModSecurity-conector/pull/396) was OPEN/DRAFT at documentation preparation; its actual Ready transition and current state are recorded in PR metadata and the public delivery readback; [Framework PR #137](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/137) is CLOSED/MERGED. This is local NGINX-H1 proof, not Protected verification or a merge. The [overarching PR #382 checklist](https://github.com/Easton97-Jens/ModSecurity-conector/blob/fix/unified-native-results-events-20260921/docs/pr-382-checklist.md) and I09–I12 remain separately open; the [current remaining-work matrix](https://github.com/Easton97-Jens/ModSecurity-conector/blob/fix/unified-native-results-events-20260921/docs/pr-382-i09-i12-rest-matrix.md) is likewise on the authorized #382 branch.

## Revision and evidence contract

| Binding | Tested Parent | Tested Framework | Meaning |
| --- | --- | --- | --- |
| R | `dca17fd5690c2ec2b8806024d1061744db8c3ad8` | `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9` | Immutable historical R13; initial RED tests used explicitly identified working test/source overlays on these bases. |
| G | `b4044d10682cb2881c218fe84cebe41e61b235c2` | `3a1932ef9060103d3a63b47d87c36006af954ee6` | Historical tested source; fresh Parent 345 / Framework 413 / namespace61 tests and Parent native lint/docs. |
| L | `2686b07aaf64b0541d743b53970008bd86caa91f` | `3a1932ef9060103d3a63b47d87c36006af954ee6` | Actual complete Framework native lint: 604 test executions / 19 suites, exit 0; not relabelled onto later Parent G. |
| N | `ff162ecb11217320a81829169a72ca4a5a4081f9` | `1bfc4f8e8e4aa9d618c4cfb2205badd5008d8f75` | Removal integration checkpoint; Parent native lint300/no SKIPs/exit 0 and Framework 415/no SKIPs/exit 0. Two config launch attempts exited137 before NGINX. |
| C | `4423e13e7fb26285a93b0c08323a37491e5941a2` | `1bfc4f8e8e4aa9d618c4cfb2205badd5008d8f75` | Historical completed bounded AB/CD checkpoint: configPASS, AB16PASS2FAIL79NE/CD6PASS2FAIL89NE; former B pairing defect. Tests/lint only at this binding. |
| T | `34127a6a462ec448b6b1d0c1d7cf16541c8ab55f` | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` | Historical bounded runtime-tested source: readyAB and readyCD scoped PASS; original aggregates remain FAIL. |
| U / R17 | `2f02370b07149265841411894f1a2cf7f1e978ff` | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` | Actual tested source of the single fresh standard Full97; Canonical PASS with complete declared direct completion measurements. |

R/G/L/N/C/T are historical bindings; their original failures and limits remain unchanged. U is the actual runtime-tested head. MRTS remains `8a6bb546c4c81d8ffc7be801dceac60c6925685f`, NGINX remains 1.31.6. A later documentation commit requires its own CI and remote readbacks and inherits no runtime PASS. Actual PR status and documentation head are reported separately in PR metadata.

| Fix key | Separate commit | Responsibility |
| --- | --- | --- |
| A | `b0d75ef6bbc33228423aef65d8ea3409387ab30f` | Parent identity-bound intervention outcomes. |
| AF | `7672340c57b3f7c80f4f5c68fc55fecca2ae4af8` | Parent preserves explicitly positive fault contracts. |
| B | `58d07970b755d7435c23030e844a32e2f6b6b583` | Parent pre-release First-Byte snapshot and unique byte-bound receipt. |
| C | `e8a8f98a4c24958616b15b98aadedcc73345a786` | Framework observed native H1 protocol/event binding. |
| D | `0c7f224731cda059decee026c7bd32e58bf9aa21` | Framework narrowly constrained existing MIME-Allow aggregate schema. |
| I | `2686b07aaf64b0541d743b53970008bd86caa91f` | Separate Parent Framework-Gitlink integration. |
| S | `b4044d10682cb2881c218fe84cebe41e61b235c2` | Two behavior-preserving helpers for actual `python:S3776` findings; no suppression. |
| Rm | `41eaa6c7` | Parent repository-wide removal of the body-limit API; historical/negative fixtures retained. |
| Rf | `1bfc4f8e8e4aa9d618c4cfb2205badd5008d8f75` | Framework same-ID Required `invalid_size` migration to genuine removed-directive rejection. |
| Ri | `ff162ecb11217320a81829169a72ca4a5a4081f9` | Separate Parent Framework-Gitlink integration; MRTS unchanged. |
| Rc | `4423e13e7fb26285a93b0c08323a37491e5941a2` | Separate relevant checker/CI follow-up with regression controls; no suppression. |
| Bp | `873e51fbebbedb163a5c75a22a7abe0158861a40` | Separate Framework two-original-event pairing fix. |
| Bq | `9f41f80db7bf53b57429457bce0dda675d2ec5d7` | Minimal task-relevant S3776/S107quality follow-up, no suppression. |
| Pi | `34127a6a462ec448b6b1d0c1d7cf16541c8ab55f` | Separate Parentgitlinkcommit; MRTSunchanged. |

## Current local Full97 — U / R17

Run ID: `nginx_full97_2f02_20261010_r17`. The single authorized fresh `make full-lifecycle-nginx` completed with actual Make/supervisor exit 0 in 554.091s; original validator exit 0, schema error list empty. Unchanged selection:14 YAML +42 native +10 configtests +31 explicit derivations =97 Required-PASS. The full 166 inventory contains97 PASS,34 unselected NOT_EXECUTED and35 NOT_APPLICABLE. The collector source separately remains PASS with 31 PASS/42 NOT_EXECUTED placeholders; specialized original receipts and Canonical close actual operations without relabeling those placeholders.

The external hash-bound client meter preserves arguments/streams and distinguishes actual normal exits from signals.34 actual curl start/completion pairs:16 primary requests +1 First-Byte +17 readiness. Generic Strict client: **normal exit 52**, no signal, invocation `669ba1b19fc340618d62148d715e5fc3`, child PID 10440; Rule 1100301, Phase 4, strict abort. Curl HTTP 000 and already visible producer HTTP 200 are separate observations. First-Byte writer: normal exit 0, invocation `1515086ec928494aafd0b0a0fceab107`, child PID 12514. All 16 declared direct program receipts across 11 classes have normal exit 0. Diagnostic parsing never substitutes for child measurement.

Actual 79 non-readiness HTTP operations, including four positive controls;31 derivations are not additional requests.61 actual Root-master/nobody-worker lifecycles with cleanup,57 distinct fresh root-owned direct projection children. Test system: Ubuntu 26.04.1 LTS, kernel 7.0.0-38, KVM; isolated loopback runtime. NGINX binary/module were freshly built for this source; Engine cache reuse was identity-verified.2589 final runtime hashes checked, exit 0; ledger SHA256 `b79fbe3e2b7cf2806c8698f2a6fd7f1f1a4c4f06aed8075924311d4d1c27d97a`.

Quality at U: 14 curl/8 Python recorder controls, 71 focused and 61 namespace tests without SKIPs passed. Actual CI22 SUCCESS/2 intentional H2/H3 SKIPs; fresh Sonar GateOK, all five conditions passed. Additional product ShellCheck:7 warnings/7 infos unchanged. Complete additional local lint was not rerun; historical16 Apache/MRTS diagnostics were not retested. H2/H3 SKIP is not PASS.

Local originals: `nginx-strict-client-full97-r17-20261010T193127Z`, including `postrun-v3/`, `operations-audit-r17.md` and runtime ledger; these are not public downloads. The first frozen analyzer exit 1 is retained: raw `phase4.log` was intentionally scrubbed after allowlist normalization. Only new read-only v2/v3 analysis follows original normalized TX and scrub log; instruments/runtime originals remain unchanged. Historical R15/R16 results remain unchanged; R16 still had the generic completion measurement gap.

## Historical bounded evidence — T

- readyAB: five genuineH1operations, driver/supervisor0/255.841s/runtime0/finalize1/validator0. All sevenA/BIDs and eight historicalNE-derivedIDs individuallyoriginalPASS; originalCanonicalFAIL18PASS79NE97Required. Rootmasters5/nobodyWorkers10/freshprojections5/cleanup5/59hash-inodebindings/311ledgervalid.
- readyCD: fouroperations (threeNative + FirstByte, readinessprobe counted separately), driver/supervisor0/237.518s/nativeHost0/FirstByte0/runtime0/finalize1/validator0. SixscopedIDsPASS, originalCanonicalFAIL8PASS89NE97Required. NativeMIME2 GET200/27bytes; StrictH1.1chunked200/10428bytes/incomplete_read/connection_aborted. FourRootmasters/fiveWorkers/fourfreshrootownednonsymlinkdirectprojections, nativecleanupseparatelyverified,219ledger0/taskhostLingering[]. Genericcounts not applied to all nativecases.
- CurrentFreshInputOffline C8+D16revalidation0/5.790s: H1/nativeauthority/canonicalevent/schema0, all 24mismatches rejected; originalbundle/fiveDocs/status unchanged. Not a newruntimeinvocation.
- invalid_size: sameRequiredrecord, genuineunknownDirective rejection of formerlyvalid1048576, NGINX-t1/driver0/70.97s/noHTTP. Repository-wide modsecurity_phase4_body_limit APIremoved; noalias/deprecatedregistration. SecResponseBodyLimit/fourEngineLimitCases/independent1MiBdefaults/hardcaps/invalidmode/overflowguard retained.

AB/CD **not combined into Full97PASS**. At historical T all 97fresh_full97 were NOTRUN/approvalrequired. readyAB/CDaudits VERIFIED_BOUNDED_ONLY/errors[]/incomplete[]; Rootfullreadonlyaudit0. Guardedagentrawlogreadlimit remains explicit; RootcheckedNativeReceipts and actualLoader/hash-inodebindings separately.

## Historical quality, evidence and limitations — T

Tested sourcebindingT: ParentnativeLint0/171.913s; cleanFrameworkfullLint604tests19suites0SKIPexit 0/1234.301s; cleanNoCRS4230SKIPexit 0/188.042s; namespace610SKIPexit 0/5.884s. CIParent 22SUCCESS2SKIP/Framework 11SUCCESS3advisorySKIP0pending; exactParentSonar 14:24:46 andFramework 14:23:39 GateOK/0OPEN-CONFIRMEDfindings. HostedCI notProtected. TwoParenteventgatedpreflightSKIPs prove noH2/H3; FrameworkOSV/Scorecard/fullhistorysecretscanadvisorySKIPs are notexecutedPASS.

SevenNGINXauxiliary and16Apache/MRTSParentShellCheckbaseline diagnostics/Python3.14.7≠CI3.14.8 and twoindependentlyreproduced113-baselinetestfailures remain explicit, notsuppressed. Historicalworkingtree604runs notrelabeledascleancommit. EarlierfailedRuntime/config137/V3adapter/Sonar 873twofindings/HTTP 400-502/Vortex403 remain in completeexternalreport/originalreceipts; notactivecheckpointclaims.

Local evidence under nginx-full97-followup-20261010T084822Z: removal-focus-audit/r14-ready-ab-v4/audit.json,r14-ready-cd-v4/audit.json; fresh-cd-revalidation-34127a6a/offline-revalidation.json; artifact-audit-r14-ready-ab/; namespace-quality-34127a6a/; r14-framework-final-readback.json/r14-parent-pre-docs-readback.json. Localpaths are notpublicGitHubdownloads.

HistoricalR13 remains97Required=80CasePASS/9FAIL/8NE plusfour nestedSchemaerrors in twoMIMEPASS; Make/supervisor2/validator1/CanonicalFAIL and79genuineRequests retained. All 80controls remain baseline, not a newFull97run;19A-D+invalid_size scopedrowscurrent,77controlsunchanged.

## Baseline

- [x] B0: Verify baseline revisions, branches/Gitlinks and preserved R13. Binding R; original comparison/readback passed; fix none; `baseline-reconciliation.json`, `checks/baseline_pr396.log`, `checks/baseline_pr137.log`; historical only.
- [x] B1: Map all nine original FAIL records. Binding R; deterministic original matrix/result reconciliation passed; fix none; `baseline-reconciliation.json`, `issue-record-matrix.csv`; no new runtime status.
- [x] B2: Map all eight original NOT_EXECUTED to their first missing boundary. Binding R; original record/basis comparison passed; fix none; same reconciliation/matrix; explicit derivations, not assumed missing drivers.
- [x] B3: Map four nested errors to two MIME-Allow Case-PASS. Binding R; original JSON/schema paths reconciled; fix none; `baseline-reconciliation.json`; two cases, not four additional runtime FAILs.

## A — Intervention

- [x] A1: Reproduce the overwritten intervention sequence. Binding R working regression, confirmed at G; `tests.test_no_crs_outcome_projection`, RED exit 1 / G group exit 0; fixes A+AF+S; `parent-ab/a-red.log`, `parent-quality-b4044d10/native-selection-snapshot-authority.log`; unit evidence only.
- [x] A2: Identify Parent projector, overwritten decision fields and observation time. Bindings R/G; trace plus completion/technical-fault tests passed at G; fixes A+AF+S; A Change Record and the same unit logs. Matching rule/phase/TX decision is separate from later lifecycle state; genuine technical faults remain visible.
- [x] A3: Demonstrate RED before the repair. Binding R working tests; four valid failure controls, exit 1; fix A; `parent-ab/a-red.log`. One invalid nonintervention fixture was corrected openly; it is not counted as a product defect.
- [x] A4: Implement the minimal identity-bound repair. Binding G; Parent outcome/collector regression groups exit 0; fixes A+AF+S; `parent-quality-b4044d10/run-checks.sh`, `results.md`; no product/validator/Required change.
- [x] A5: Pass positive, technical-fault, cross-TX and priority controls. Binding G; Parent 345 including affected normal and positive-fault paths, exit 0; fixes A+AF+S; `parent-quality-b4044d10/results.md`, `parent-sonar-followup/results.md`; no global nonzero=PASS or technical-error veto.
- [x] A6: Binding T; genuine fourA basis requests/originalCanonicalPASS atP341/F9f. Root/nobody/freshness/cleanup/artifacts311ledgervalid; ready-AB-v4 VERIFIED_BOUNDED_ONLY. NotFull97.
- [x] A7: Historical binding T341/9f integrated/clean/published, exactgitlinksM8aunchanged. Historical Parent native302/FrameworkNoCRS423/fullLint60419/namespace61exit 0; actualAbasisPASS. OriginalG/Lproofs retained historically, notFull97.
- [x] A8: Original statuses confirmed at U/R17: all 97 Required-PASS with unchanged contracts and real invocations; public R17 reference.

## B — First-Byte

- [x] B4: Determine invocation/time/counter contract. Bindings R/G; capture-before-release ordering regression passes at G; fix B; `parent-ab/b-red.log`, B Change Record, `parent-quality-b4044d10/native-selection-snapshot-authority.log`. Snapshot is measured while upstream is paused, not after response completion.
- [x] B5: Reproduce post-release capture and missing unique bound merge. Binding R working tests; RED exit 1; fix B; `parent-ab/b-red.log`; historical/test input, not new requests.
- [x] B6: Correct binding and retain mismatch controls. Binding G; `tests.test_nginx_first_byte_binding` and collector/Framework suites exit 0; fixes B+S; `parent-quality-b4044d10/run-checks.sh`, `framework-quality-b4044d10/no-crs-suite.json`. Wrong invocation/TX/time, stale or tampered snapshot, duplicate event and equal counters without provenance remain rejected; later cumulative counters remain intact.
- [x] B7: Binding T; genuine synchronizedFirstByte/bothBoriginalCanonicalPASS; closed17append/44Ruleinterventionpair, snapshot/order/identity/SafeResponse verified. ready-AB-v4/errors[]/incomplete[], driver0; originaloverallFAIL79missingRequired retained. Bounded only, notFull97.
- [x] B8: Historical binding T; Frameworkpairing873+minimalquality9f and Parentgitlink341 integrated, genuineAB/CDfirstbyte/nobufferPASS, legacy/mixedTXmismatchcontrols andNoCRS4230. No ruleinjection/eventmerge/counterserialization/guardweakening. BpairingfixdoesnotalterApache; repository-wideAPIremoval changedApache separately.
- [x] B9: Confirmed at U/R17: synchronized First-Byte and directly measured writer exit 0; no post-release snapshot relabeling.

## C — Native H1

- [x] C1: Trace real observation → operation/receipt → canonical protocol/event. Binding R input plus G contracts; original native bytes reopened in explicit current-validator replay, exit 0; fix C; `framework-cd/c-historical-replay-v3.log`, C Change Record. H1 derives from observed HTTP version11 and matching URI/TX/case/run/phase/Rule, never an environment default.
- [x] C2: Reproduce the first missing canonical binding. Binding R working regression; C RED exit 1; fix C; `framework-cd/c-red.log`, `baseline-reconciliation.json`; original runtime operation existed, canonical protocol fields/event did not.
- [x] C3: Implement strict binding and retain negative controls. Binding G; Framework 413 exit 0 and explicitly historical C replay exit 0; fix C; `framework-quality-b4044d10/no-crs-suite.json`, `framework-cd/c-historical-replay-v3.log`. Wrong protocol/invocation/TX/case, missing observation, stale receipt, wrong module/bytes and canonical tampering stay rejected; no H1→H2/H3 relabelling.
- [x] C4: BindingT341/9f; genuine readyCDStrictH1CasePASS/nativeHost0, freshretainedC8negatives0/H1-canonicalevent-authorityreopened. Rootauditv4VERIFIED_BOUNDED_ONLY/219ledger0/cleanup/freshness; nativecaseidentities separate. NotFull97.
- [x] C5: Historical binding T cleanintegrated/published, exactgitlinksP341/F9f/M8a/remoteOPEN-DRAFT, cleanNoCRS423/fullLint60419/CI-Sonar 0; genuineCD/retainedCnegativesverified, MRTSunchanged. No historyrewrite.
- [x] C6: Confirmed at U/R17: actual native H1 operations and bound original receipts; no H2/H3 proof.

## D — MIME

- [x] D1: Identify four schema errors separately from two Case-PASS. Binding R; exact original JSON paths/type/value reconciled; fix none; `baseline-reconciliation.json`; original nested action enum rejected string `allow`.
- [x] D2: Trace reader/normalizer → actual aggregate projection → nested schema. Binding R input and G tests; historical actual full producer replay schema-valid, exit 0, overall still FAIL; fix D; `framework-cd/d-historical-replay.log`, D Change Record; no new runtime result.
- [x] D3: Demonstrate RED through actual dynamic aggregation. Binding R working test; two subtests reproduce four enum errors, exit 1; fix D; `framework-cd/d-red.log`; not a hand-written schema-only substitute.
- [x] D4: Implement the narrowly justified schema contract. Binding G; Framework 413 exit 0; fix D; `framework-quality-b4044d10/no-crs-suite.json`, `framework-cd/d-green.log`. Only the two exact existing case/result pairs allow `allow/allow`, with no Rule, late intervention or abort; required fields, closure and real null/completed transport remain intact. Eight mismatch controls per MIME case remain negative.
- [x] D5: BindingT341/9f; both genuine readyCDMIMECasePASS, fresh aggregateSchemaErrors[]/validator0, currentfreshD16negatives0. OriginalCanonicalFAIL8PASS89NE retained. Evidence currentCDauditv4/freshOfflineJSON, boundedonly.
- [x] D6: Historical binding T schema/producer/sourcehashes/gitlinksbound, cleanNoCRS423/fullLint60419/CI0 and actualMIME+freshD16negatives0. Historicalfour schemaerrors in twoCasePASS unchanged.
- [x] D7: Whole fresh U/R17 aggregate validated: empty schema error list, original validator exit 0.

## E — Derivations

- [x] E1: Map every record to its first blocked boundary. Binding R; original deterministic basis/record reconciliation passed; fix none; `baseline-reconciliation.json`, `issue-record-matrix.csv`; see exact mapping below.
- [x] E2: Distinguish A–D dependencies from independent causes. Bindings R/G; closed derivation/selection contracts and Framework 413 exit 0; fixes A+AF+B+C+D+I where applicable; same matrix and `framework-quality-b4044d10/no-crs-suite.json`; no unnecessary new driver or invented evidence.
- [x] E3: Binding T; all eight historicalNE-derived IDs individually newreadyABCanonicalPASS atP341/F9f, no extraRequests/syntheticEvidence. OriginalABCanonicalFAIL/79NE retained; notFull97.
- [x] E4: All 97 fresh original statuses measured at U/R17:97 PASS;31 explicit derivations, not 31 additional requests.

## Q — Quality / integration

- [x] Q1: Current binding U: 14 curl/8 Python recorder controls, 71 focused tests and 61 namespace tests without SKIPs passed. Historical G/L/T suites retain separate bindings.
- [x] Q2: Current binding U: mandatory CI lint/docs/contracts succeeded; additional complete local lint rerun not performed. ShellCheck 7 warnings/7 infos unchanged; 16 historical Apache/MRTS diagnostics not retested. Documentation successor requires its own checks.
- [x] Q3: Runtime-tested head U=2f02370b07149265841411894f1a2cf7f1e978ff; gitlinks F9f/M8a unchanged. Framework PR137 CLOSED/MERGED; pin remains9f. Later documentation head/readback separate, no inherited runtime PASS.
- [x] Q4: Exact tested binding U: 22 CI SUCCESS/2 intentional H2/H3 SKIPs; fresh Sonar GateOK/all five conditions passed. Evaluate documentation-successor CI separately; hosted CI is not Protected.
- [ ] Q5: At documentation preparation final EN/DE validation, publication and remote readback remained outstanding. Check actual closure of this item and the Ready transition against public delivery/PR metadata; no future status is preclaimed here.

## F — Full97

- [x] F1: Explicit authorization received for exactly one fresh local standard Full97; attachment f3e597f0.
- [x] F2: The single fresh standard Full97 executed on frozen U tuple: Make/supervisor 0, 554.091s.
- [x] F3: Whole fresh aggregate schema checked by original Framework validator: exit 0, empty error list.
- [x] F4: All 97 unchanged Required records PASS with genuine identity-bound evidence.
- [x] F5: Canonical PASS; actual lifecycle/supervisor/collector/writer/validator completions measured. Generic Strict has measured normal exit 52 under the specific Strict-abort oracle; 52 is an observation, not a required numeric contract or global nonzero=PASS.
- [x] F6: 61 lifecycle cleanups and 57 fresh projection children verified; 2589 final runtime hashes, check exit 0.

## P — Protected

- [ ] P1: Independently approve Trusted Base.
- [ ] P2: Verify admissible base/Gitlink/workflow binding.
- [ ] P3: Administratively approve runner and environment.
- [ ] P4: Verify Exact-Base host gate.
- [ ] P5: Start/evaluate an admissible protected run only after those prerequisites.

## Record status — historical T and current Full97 U

All rows below now have original Full97 PASS at U/R17; the table preserves their historical R13 statuses and earlier T evidence. The historical issue-record-matrix.csv is not relabeled; current postrun-v3/required-records97.json maps all 97 actual records. Derivations are not additional requests.

| Record ID | Historical R13 | Historical bounded T evidence |
| --- | --- | --- |
| phase3_deny_before_commit | FAIL | readyAB A request |
| phase3_redirect_before_commit | FAIL | readyAB A request |
| phase4_deny_after_commit_log_only | FAIL | readyAB A request |
| phase4_deny_after_commit_abort | FAIL | readyAB A request |
| phase4_deny_after_commit_log_only_safe | FAIL | readyAB explicit safe basis derivation |
| phase4_rule_observed | FAIL | readyAB/readyCD real FirstByte rule witness |
| phase4_no_full_response_buffering | FAIL | readyAB/readyCD FirstByte |
| phase4_first_byte_before_response_end | FAIL | readyAB/readyCD FirstByte |
| phase4_strict_http1_client_abort | FAIL | readyCD actual Strict-H1 |
| phase4_event_contains_original_status | NOT_EXECUTED | readyAB explicit A basis derivation |
| phase4_event_contains_late_intervention_action | NOT_EXECUTED | readyAB explicit A basis derivation |
| event_has_no_response_body_payload | NOT_EXECUTED | readyAB explicit A/B basis derivation |
| phase3_original_and_visible_status | NOT_EXECUTED | readyAB explicit A basis derivation |
| phase4_deny_after_commit_abort_strict | NOT_EXECUTED | readyAB explicit A basis derivation |
| phase4_status_metadata | NOT_EXECUTED | readyAB explicit A basis derivation |
| phase4_action_metadata | NOT_EXECUTED | readyAB explicit A basis derivation |
| phase4_no_payload_event | NOT_EXECUTED | readyAB explicit A/B basis derivation |
| phase4_out_of_scope_content_type | CasePASS; two schema errors | readyCD real MIME; schema valid |
| phase4_missing_content_type | CasePASS; two schema errors | readyCD real MIME; schema valid |
| invalid_size | PASS; old API contract | actual removed-API configtest |

## Closing boundary

R17 local Full97: **PASS**, under the frozen local acceptance list and public R17 report. No second Full97 was executed or newly authorized. Protected **BLOCKED / NOT RUN**: independent Trusted-Base/runner/host-gate prerequisites remain separate; no candidate checker as trusted root checker. PR #396: at documentation preparation the Ready transition and documentation successor remained Root-owned; actual closure is recorded in public delivery/PR metadata. PR #382 remains OPEN/DRAFT, I09–I12 open. No merge, retarget, Protected dispatch or general all-profile PASS.
