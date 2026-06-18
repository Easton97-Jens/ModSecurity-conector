> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T21:57:19Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-final-consistency-audit.py`
> Make target: `generate-final-consistency-audit`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `29083baa42f7cae3aff7c9f340e2fbe437dd410d`
> Framework SHA: `c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67`
> Input status: `complete`

# Final Consistency Audit

Generated file - do not edit manually.

- Generated at: `2026-06-17T21:57:19Z`
- Release readiness: `needs_attention`
- Recommended next fix cluster: `multipart_files`
- Recommendation justified: `no`
- Reason: remaining active body-processor work is now multipart-only after URL-encoded and XML metadata splits

## Git And Submodules
- Connector HEAD: `29083baa42f7cae3aff7c9f340e2fbe437dd410d`
- Framework HEAD: `c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67`

| Submodule status |
|---|
| c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67 modules/ModSecurity-test-Framework (heads/master) |
|  13aa91291adea12d5c607fdd165d010fcfb1da78 modules/ModSecurity-test-Framework/tools/MRTS (heads/main) |

## Full-Matrix Summary
- Attempted: **3928**
- PASS: **3104**
- FAIL: **776**
- BLOCKED: **0**
- NOT_EXECUTABLE: **48**
- Pending: **2298**
- Full-Matrix was not rerun for this audit; counts come from existing evidence.

## Priority Distribution
- P0/P1/P2/P3/report_only non-PASS: **6 / 0 / 60 / 215 / 543**
- Queue totals and recomputed non-PASS priorities match: `yes`
- Queue totals non-PASS: `{'P0': 6, 'P2': 60, 'P3': 215, 'report_only': 543}`
- Recomputed non-PASS: `{'P0': 6, 'P2': 60, 'P3': 215, 'report_only': 543}`
- Recomputed FAIL only: `{'P0': 6, 'P2': 60, 'P3': 167, 'report_only': 543}`
- P0/P1 failing rows: **6**
- P2 rows are response-header DetectionOnly/report-only leftovers: `yes`

## Remaining Categories
- Active runtime-fixable clusters: **1**
- Report-only rows: **615**
- Semantic pending rows: **42**
- Capability-evidence pending rows: **68**
- Connector-gap rows: **45**
| Category | Count | Connectors | Disposition | Recommended next step |
|---|---|---|---|---|
| with_mrts_detection_only_non_disruptive | 507 | apache, haproxy, nginx | report_only | keep with-MRTS request-side DetectionOnly rows report-only; continue intervention analysis on no-MRTS no-match cases |
| phase4_missing_abort_evidence | 68 | apache, nginx | capability_evidence_pending | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| response_header_mrts_detection_only | 60 | apache, haproxy, nginx | report_only | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| phase4_connector_gap | 42 | apache, haproxy, nginx | connector_gap | document connector gap unless implementation can prove a real hard abort |
| collection_name_normalization_semantics | 30 | apache, haproxy, nginx | semantic_pending_native_or_libmodsecurity_comparison | compare collection-name normalization semantics against native/libmodsecurity before treating as a runtime fix |
| xml_processor_activation_missing | 24 | apache, haproxy, nginx | report_only | keep XML processor activation-missing rows report-only; do not change rules or Expected statuses |
| multipart_processor_activation_missing | 12 | apache, haproxy, nginx | report_only | keep Multipart processor activation-missing rows report-only; do not change bodies, rules, or Expected statuses |
| transformation_semantics | 12 | apache, haproxy, nginx | semantic_pending_native_or_libmodsecurity_comparison | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| multipart_files | 6 | apache, haproxy, nginx | review_required | compare multipart variable population across connectors with one representative request |
| nolog_expected_no_audit | 6 | apache, haproxy, nginx | report_only | keep as classification-only evidence; do not add artificial audit logs |
| phase4_log_only_no_abort | 6 | nginx | report_only | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |
| connector_gap | 3 | apache, haproxy, nginx | connector_gap | manual review |

## Stale Cluster Check
| Cluster | Remaining category | FAIL work direction | FAIL classification | Status | Detail |
|---|---|---|---|---|---|
| audit_log_evidence | 0 | 0 | 0 | clear | no active rows |
| intervention_blocking | 0 | 6 | 0 | review | nonzero remaining, work-direction, or classification count |
| request_body_processor | 0 | 3 | 0 | known_connector_gap_not_active_processor_cluster | remaining work-direction rows are classified as phase1 request-body unavailable connector gap |
| multipart_files | 6 | 0 | 0 | review | nonzero remaining, work-direction, or classification count |
| xml_processor | 0 | 0 | 0 | clear | no active rows |
| phase4_hard_abort_supported | 0 | 0 | 0 | clear | no active rows |
| rule_chain_semantics | 0 | 0 | 0 | clear | runtime_fixable_candidates=0 |
| response_header_backend_setup | 0 | 0 | 0 | clear | no active rows |
| response_header_hook | 0 | 0 | 0 | clear | no active rows |
| response_header_multi_value_gap | 0 | 0 | 0 | clear | no active rows |

## Clusters No Longer Next
| Cluster | Count | Reason |
|---|---|---|
| phase4_hard_abort_capability | 116 | requires transport-abort proof plus Phase 4 intervention logs; do not solve with Expected/PASS changes |
| transformation_semantics | 12 | large count but likely semantic; needs native/libmodsecurity comparison before fixes |
| nolog_expected_no_audit | 6 | classification-only: explicit nolog means the matching rule should not emit audit evidence |
| response_header_mrts_detection_only | 60 | classification-only: with-MRTS DetectionOnly overlay suppresses disruptive Phase 3 action |
| with_mrts_detection_only_non_disruptive | 507 | classification-only: with-MRTS DetectionOnly overlay suppresses disruptive request-side action |
| xml_processor_activation_missing | 24 | classification-only: XML body and Content-Type exist, but these fixtures do not enable ctl:requestBodyProcessor=XML |
| multipart_processor_activation_missing | 12 | classification-only: multipart body, Content-Type, and boundary exist, but these fixtures do not enable request body access before expecting FILES/ARGS_NAMES collections |
| collection_name_normalization_semantics | 30 | metadata-only: loaded rules have no match evidence; needs native/libmodsecurity comparison before runtime fixes |

## Known Gaps
| Gap | Rows |
|---|---|
| phase4_missing_abort_evidence | 68 |
| phase4_connector_gap | 42 |
| transformation_semantics | 12 |
| collection_name_normalization_semantics | 30 |
| connector_gap | 3 |

## User Decisions
| Area | Reason | Safe next |
|---|---|---|
| phase4_hard_abort | Apache has implementation-path evidence but no runtime hard-abort proof; HAProxy remains a connector gap. | collect real transport-abort evidence or keep these rows as capability/gap classifications |
| transformation_and_collection_semantics | remaining no-match rows need native/libmodsecurity comparison before runtime changes. | decide whether to build comparator evidence; do not change Expected statuses or rules. |
| phase1_request_body_connector_gap | three rows remain classified as phase1 request-body unavailable connector gap. | treat as connector capability discussion before core behavior changes. |

## Native MRTS
- Native MRTS evidence remains separate from connector Full-Matrix PASS/FAIL.
| Target | Status | Attempted | PASS | FAIL | BLOCKED | Failed cases | Classification |
|---|---|---|---|---|---|---|---|
| apache2_ubuntu | FAIL | 13 | 12 | 1 | 0 | 100003-1 | native_modsecurity_semantics / phase4_native_limitation |
| nginx-pr24 | FAIL | 13 | 12 | 1 | 0 | 100003-1 | native_modsecurity_semantics / phase4_native_limitation |

## Phase 4 Hard-Abort
- Rows: **868**
- Hard-abort evidence rows: **0**
- Sensitive log leak rows: **0**
| Connector | Capability status | Hard-abort evidence rows |
|---|---|---|
| apache | implementation_path_present_no_runtime_hard_abort_evidence | 0 |
| haproxy | connector_gap_no_hard_abort_evidence | 0 |
| nginx | connector_gap_no_hard_abort_evidence | 0 |

## Freshness
| Input | Present | Generated at |
|---|---|---|
| reports/testing/generated/canonical/full-runtime-matrix.generated.json | yes | 2026-06-17T21:56:12Z |
| reports/testing/generated/work-queues/connector-work-queue.generated.json | yes | 2026-06-17T21:56:23Z |
| reports/testing/generated/work-queues/phase-work-queue.generated.json | yes | 2026-06-17T21:56:30Z |
| reports/testing/generated/canonical/remaining-failure-analysis.generated.json | yes | 2026-06-17T21:56:41Z |
| reports/testing/generated/canonical/next-fix-plan.generated.json | yes | 2026-06-17T21:56:41Z |
| reports/testing/generated/canonical/full-run-evidence.generated.json | yes | 2026-06-17T21:56:56Z |
| reports/testing/generated/mrts-native/mrts-native-summary.generated.json | yes | 2026-06-17T21:56:25Z |
| reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json | yes | 2026-06-17T21:56:37Z |
| reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json | yes | 2026-06-17T21:56:26Z |
| reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json | yes | 2026-06-17T21:56:30Z |
| reports/testing/generated/focused-analysis/body-processor-analysis.generated.json | yes | 2026-06-17T21:57:17Z |
| reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json | yes | 2026-06-17T21:57:04Z |
| reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json | yes | 2026-06-17T21:57:05Z |
| reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json | yes | 2026-06-17T21:57:18Z |

## Guardrails
| Guardrail | Value |
|---|---|
| expected_status_changed | False |
| runtime_pass_fail_manually_changed | False |
| mrt_definitions_changed | False |
| tools_mrts_changed | False |
| rules_changed | False |
| connector_core_changed | False |
| full_matrix_rerun_required | False |
| matrix_counts_source | existing full-runtime-matrix evidence |

## Release Checks
| Check | Pass |
|---|---|
| recommended_next_fix_cluster_none | no |
| blocked_zero | yes |
| queue_totals_consistent | yes |
| p0_p1_failure_rows_zero | no |
| p2_rows_are_response_header_mrts_detection_only | yes |
| active_runtime_fixable_clusters_zero | no |
| intervention_blocking_true_candidates_zero | no |
| audit_log_evidence_after_zero | yes |
| body_processor_active_after_zero | no |
| response_header_backend_setup_zero | yes |
| rule_chain_runtime_fixable_zero | yes |
| phase4_supported_label_absent | yes |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `5eb9a018436e2edd12871ccb50aea3f84e08ae00118acfd315399a8f8f7d0512` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `5af2dd56db978d8414704196dececf85cd691fbbcc654f03c0844c73fb4369a2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `2316fe5b7e70ff986d2616f0528e208983f6a5dd4b2671bf443f865c6ffbf26f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `b237c0433ef2a2d0bf1e4d2bb778d6f7f0501feadebbd3337c99a63d0fe2dd61` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `bf94318ee4981b80cb2d08e43a02a93a0ff4e20ddf22c88e8b79766ac4bb71f7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `15213b816bf77652e20b9699c24773958abed3cfddca3e4e21c02e73296e8f5e` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
