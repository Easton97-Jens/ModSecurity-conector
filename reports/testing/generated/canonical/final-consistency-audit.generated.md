> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:40:20Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-final-consistency-audit.py`
> Make target: `generate-final-consistency-audit`
> Owner: `connector`
> Severity: `critical`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
> Input status: `complete`

# Final Consistency Audit

Generated file - do not edit manually.

- Generated at: `2026-06-17T02:40:20Z`
- Release readiness: `ready_with_known_reported_gaps`
- Recommended next fix cluster: `none`
- Recommendation justified: `yes`
- Reason: No remaining runtime-fixable connector Full-Matrix cluster is recommended after report-only and not-next filters.

## Git And Submodules
- Connector HEAD: `614c80493b6ebd25a17e1d27979071e5e30584d4`
- Framework HEAD: `24509c107ecf3a22ae9d69875f661690bd6fb95b`

| Submodule status |
|---|
| 24509c107ecf3a22ae9d69875f661690bd6fb95b modules/ModSecurity-test-Framework (heads/master) |
|  13aa91291adea12d5c607fdd165d010fcfb1da78 modules/ModSecurity-test-Framework/tools/MRTS (heads/main) |

## Full-Matrix Summary
- Attempted: **3928**
- PASS: **3074**
- FAIL: **782**
- BLOCKED: **0**
- NOT_EXECUTABLE: **72**
- Pending: **2298**
- Full-Matrix was not rerun for this audit; counts come from existing evidence.

## Priority Distribution
- P0/P1/P2/P3/report_only non-PASS: **0 / 0 / 60 / 263 / 531**
- Queue totals and recomputed non-PASS priorities match: `yes`
- Queue totals non-PASS: `{'P2': 60, 'P3': 263, 'report_only': 531}`
- Recomputed non-PASS: `{'P2': 60, 'P3': 263, 'report_only': 531}`
- Recomputed FAIL only: `{'P2': 60, 'P3': 191, 'report_only': 531}`
- P0/P1 failing rows: **0**
- P2 rows are response-header DetectionOnly/report-only leftovers: `yes`

## Remaining Categories
- Active runtime-fixable clusters: **0**
- Report-only rows: **603**
- Semantic pending rows: **66**
- Capability-evidence pending rows: **68**
- Connector-gap rows: **45**
| Category | Count | Connectors | Disposition | Recommended next step |
|---|---|---|---|---|
| with_mrts_detection_only_non_disruptive | 495 | apache, haproxy, nginx | report_only | keep with-MRTS request-side DetectionOnly rows report-only; continue intervention analysis on no-MRTS no-match cases |
| phase4_missing_abort_evidence | 68 | apache, nginx | capability_evidence_pending | add real Phase 4 intervention log plus connection-abort evidence before promotion |
| response_header_mrts_detection_only | 60 | apache, haproxy, nginx | report_only | keep with-MRTS DetectionOnly rows classification-only; do not promote to PASS without disruptive runtime evidence |
| phase4_connector_gap | 42 | apache, haproxy, nginx | connector_gap | document connector gap unless implementation can prove a real hard abort |
| transformation_semantics | 36 | apache, haproxy, nginx | semantic_pending_native_or_libmodsecurity_comparison | compare transformation-chain cases against native/libmodsecurity evidence before attempting fixes |
| collection_name_normalization_semantics | 30 | apache, haproxy, nginx | semantic_pending_native_or_libmodsecurity_comparison | compare collection-name normalization semantics against native/libmodsecurity before treating as a runtime fix |
| xml_processor_activation_missing | 24 | apache, haproxy, nginx | report_only | keep XML processor activation-missing rows report-only; do not change rules or Expected statuses |
| multipart_processor_activation_missing | 12 | apache, haproxy, nginx | report_only | keep Multipart processor activation-missing rows report-only; do not change bodies, rules, or Expected statuses |
| nolog_expected_no_audit | 6 | apache, haproxy, nginx | report_only | keep as classification-only evidence; do not add artificial audit logs |
| phase4_log_only_no_abort | 6 | nginx | report_only | keep minimal/safe/content-type rows as log-only, not hard-abort PASS evidence |
| connector_gap | 3 | apache, haproxy, nginx | connector_gap | manual review |

## Stale Cluster Check
| Cluster | Remaining category | FAIL work direction | FAIL classification | Status | Detail |
|---|---|---|---|---|---|
| audit_log_evidence | 0 | 0 | 0 | clear | no active rows |
| intervention_blocking | 0 | 0 | 0 | clear | no active rows |
| request_body_processor | 0 | 3 | 0 | known_connector_gap_not_active_processor_cluster | remaining work-direction rows are classified as phase1 request-body unavailable connector gap |
| multipart_files | 0 | 0 | 0 | clear | no active rows |
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
| transformation_semantics | 36 | large count but likely semantic; needs native/libmodsecurity comparison before fixes |
| nolog_expected_no_audit | 6 | classification-only: explicit nolog means the matching rule should not emit audit evidence |
| response_header_mrts_detection_only | 60 | classification-only: with-MRTS DetectionOnly overlay suppresses disruptive Phase 3 action |
| with_mrts_detection_only_non_disruptive | 495 | classification-only: with-MRTS DetectionOnly overlay suppresses disruptive request-side action |
| xml_processor_activation_missing | 24 | classification-only: XML body and Content-Type exist, but these fixtures do not enable ctl:requestBodyProcessor=XML |
| multipart_processor_activation_missing | 12 | classification-only: multipart body, Content-Type, and boundary exist, but these fixtures do not enable request body access before expecting FILES/ARGS_NAMES collections |
| collection_name_normalization_semantics | 30 | metadata-only: loaded rules have no match evidence; needs native/libmodsecurity comparison before runtime fixes |

## Known Gaps
| Gap | Rows |
|---|---|
| phase4_missing_abort_evidence | 68 |
| phase4_connector_gap | 42 |
| transformation_semantics | 36 |
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
| reports/testing/generated/canonical/full-runtime-matrix.generated.json | yes | 2026-06-17T02:39:19Z |
| reports/testing/generated/work-queues/connector-work-queue.generated.json | yes | 2026-06-17T02:39:27Z |
| reports/testing/generated/work-queues/phase-work-queue.generated.json | yes | 2026-06-17T02:39:34Z |
| reports/testing/generated/canonical/remaining-failure-analysis.generated.json | yes | 2026-06-17T02:39:43Z |
| reports/testing/generated/canonical/next-fix-plan.generated.json | yes | 2026-06-17T02:39:43Z |
| reports/testing/generated/canonical/full-run-evidence.generated.json | yes | 2026-06-17T02:40:01Z |
| reports/testing/generated/mrts-native/mrts-native-summary.generated.json | yes | 2026-06-17T02:39:29Z |
| reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json | yes | 2026-06-17T02:39:40Z |
| reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json | yes | 2026-06-17T02:39:30Z |
| reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json | yes | 2026-06-17T02:39:34Z |
| reports/testing/generated/focused-analysis/body-processor-analysis.generated.json | yes | 2026-06-17T02:40:18Z |
| reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json | yes | 2026-06-17T02:40:07Z |
| reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json | yes | 2026-06-17T02:40:09Z |
| reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json | yes | 2026-06-17T02:40:19Z |

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
| recommended_next_fix_cluster_none | yes |
| blocked_zero | yes |
| queue_totals_consistent | yes |
| p0_p1_failure_rows_zero | yes |
| p2_rows_are_response_header_mrts_detection_only | yes |
| active_runtime_fixable_clusters_zero | yes |
| intervention_blocking_true_candidates_zero | yes |
| audit_log_evidence_after_zero | yes |
| body_processor_active_after_zero | yes |
| response_header_backend_setup_zero | yes |
| rule_chain_runtime_fixable_zero | yes |
| phase4_supported_label_absent | yes |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `676cc8d9b51b9294387e0b73fe8a7ff1f78a4fe5ff268f5996cb1967b906c576` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `7d7a581758867799859f481971e56c0e7da57ca399f5a7e016b2ce839ac83063` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `b21bba0ae1115efd9761ed2317324b8e142f221801b35359b024704fb2e4c657` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `893fb7f44572f7c5b06974f727c4bd5b56ac2b68eeaf50bd2eb287292a85c567` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `56d43bad850595932f10e7e412d8d7a2a63b60ec8a170535015b7eb12ad7f15d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `6f7c469a2eb7869d6b401cf502cf6195bd3c0efecea4f83192c051a11797dd6a` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
