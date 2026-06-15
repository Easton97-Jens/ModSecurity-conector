> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:40:37Z`
> Generator: `ci/generate-rule-chain-semantics-analysis.py`
> Make target: `generate-rule-chain-semantics-analysis`
> Owner: `connector`
> Severity: `informational`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `complete`

# Rule Chain Semantics Analysis

Generated at: `2026-06-15T10:40:37Z`

## Summary
| Rule-chain rows | Rule-chain groups | Single-connector groups | Single-connector rows | Runtime-fixable candidates | Report-only items | Parent matched | Child matched | Full chain matched | Name-only non-rule-chain rows |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 1 | 7 | 14 | 0 | 13 | 0 | 0 | 0 | 6 |

## Conclusion
- Selected subcluster: with-MRTS DetectionOnly redirect classification and report-only Rule-Chain triage.
- Root cause: Rule-chain semantics are not the active blocker: no-MRTS Rule-Chain rows pass, while with-MRTS failures are non-disruptive DetectionOnly overlay rows. The remaining NGINX-only rows are either Phase-4 not-next evidence or with-MRTS DetectionOnly rows.
- Safe change: metadata/report-only classification; no Expected status, rule, MRTS definition, or connector-core change.

## Rule-Chain Failure Rows
| Connector | Variant | Case | Parent | Children | Expected | Actual | Parent matched | Child matched | Full chain | Classification | Fixability |
|---|---|---|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| nginx | no-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| haproxy | no-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| apache | with-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| nginx | with-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |
| haproxy | with-crs/with-mrts | rule_chain_both_match_block | - | - | 403 | 200 | unknown | unknown | unknown | with_mrts_detection_only_chain_non_disruptive | report_only |

## Chain-Named Non-Rule-Chain Rows
| Connector | Variant | Case | Category | Rules | Expected | Actual | Classification | Root cause |
|---|---|---|---|---|---|---|---|---|
| apache | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| nginx | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| haproxy | no-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| apache | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| nginx | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |
| haproxy | with-crs/with-mrts | tfn_chain_urldecode_compress_whitespace_gap | transformations | - | 403 | 200 | transformation_chain_name_not_secrule_chain | The case name contains chain, but the rules are transformation-chain semantics rather than a SecRule chain construct. |

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
- Recommended next cluster: `none`
- Reason: No remaining runtime-fixable connector Full-Matrix cluster is recommended after report-only and not-next filters.

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
