> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:52:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-rule-chain-semantics-analysis.py`
> Make target: `generate-rule-chain-semantics-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

# Rule Chain Semantics Analysis

Generated at: `2026-06-19T16:52:57Z`

## Summary
| Rule-chain rows | Rule-chain groups | Single-connector groups | Single-connector rows | Runtime-fixable candidates | Report-only items | Parent matched | Child matched | Full chain matched | Name-only non-rule-chain rows |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 1 | 7 | 14 | 0 | 13 | 3 | 2 | 3 | 6 |

## Conclusion
- Selected subcluster: with-MRTS DetectionOnly redirect classification and report-only Rule-Chain triage.
- Root cause: Rule-chain semantics are not the active blocker: no-MRTS Rule-Chain rows pass, while with-MRTS failures are non-disruptive DetectionOnly overlay rows. The remaining NGINX-only rows are either Phase-4 not-next evidence or with-MRTS DetectionOnly rows.
- Safe change: metadata/report-only classification; no Expected status, rule, MRTS definition, or connector-core change.

## Rule-Chain Failure Rows
| Connector | Variant | Case | Parent | Children | Expected | Actual | Parent matched | Child matched | Full chain | Classification | Fixability |
|---|---|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | yes | yes | yes | with_mrts_detection_only_chain_non_disruptive | report_only |
| nginx | no-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| haproxy | no-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | yes | unknown | yes | with_mrts_detection_only_chain_non_disruptive | report_only |
| apache | with-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | yes | yes | yes | with_mrts_detection_only_chain_non_disruptive | report_only |
| nginx | with-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| haproxy | with-crs/with-mrts | rule_chain_both_match_block | 5801 | 5801/chain-1 | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |

## Chain-Named Non-Rule-Chain Rows
| Connector | Variant | Case | Category | Rules | Expected | Actual | Classification | Root cause |
|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| nginx | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| haproxy | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| apache | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| nginx | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| haproxy | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | 4612 | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |

## Single-Connector Leftovers
| Count | Connector | Case | Variants | Rules | Expected | Actual | Classification | Fixability | Root cause |
|---|---|---|---|---|---|---|---|---|---|
| 2 | nginx | nginx_phase4_content_type_out_of_scope | no-crs/with-mrts, with-crs/with-mrts | - | {'200': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_phase4_minimal_log_only | no-crs/with-mrts, with-crs/with-mrts | - | {'200': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_phase4_safe_log_only | no-crs/with-mrts, with-crs/with-mrts | - | {'200': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_phase4_strict_connection_abort | no-crs/with-mrts, with-crs/with-mrts | - | {'403': 2} | {'200': 2} | phase4_not_next_single_connector_leftover | report_only | Phase-4 hard-abort/log-only evidence is already tracked by the Phase-4 capability report and is not a Rule-Chain runtime fix. |
| 2 | nginx | nginx_redirect_phase1_302 | no-crs/with-mrts, with-crs/with-mrts | - | {'302': 2} | {'200': 2} | with_mrts_detection_only_single_connector_non_disruptive | report_only | with-MRTS DetectionOnly overlay keeps the otherwise disruptive NGINX-specific action non-blocking. |
| 2 | nginx | nginx_tx_scoring_absolute_block | no-crs/with-mrts, with-crs/with-mrts | - | {'403': 2} | {'200': 2} | with_mrts_detection_only_single_connector_non_disruptive | report_only | with-MRTS DetectionOnly overlay keeps the otherwise disruptive NGINX-specific action non-blocking. |
| 2 | nginx | nginx_tx_scoring_iterative_block | no-crs/with-mrts, with-crs/with-mrts | - | {'403': 2} | {'200': 2} | with_mrts_detection_only_single_connector_non_disruptive | report_only | with-MRTS DetectionOnly overlay keeps the otherwise disruptive NGINX-specific action non-blocking. |

## Next Recommendation
- Recommended next cluster: `multipart_files`
- Reason: remaining active body-processor work is now multipart-only after URL-encoded and XML metadata splits

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `06d58887a5b4c5497345a54792d90cfa4c910b3ae1610b2f0efed714c60f3a54` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `3425a08630d7eee65c73745216c902a605453363e9b26c12d62d042fabddf0a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `67eae92c2d1fde007978f559f16c43598eb52d2c4a80fd0bd171c4748cfb62ff` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `d31fb8c743fe579a70cd77d1d455f749b99e3682d1737d2751c70f3b46c520a8` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
