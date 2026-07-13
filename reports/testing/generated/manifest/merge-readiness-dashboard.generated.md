> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T20:12:32Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/evidence/reports/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
> Framework SHA: `4e9d4ba616235127b6fc0a2ee87107d93d03f40b`
> Input status: `stale`

# Merge Readiness Dashboard

**Language:** English | [Deutsch](merge-readiness-dashboard.generated.de.md)

Merge Readiness: `UNKNOWN`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3157 FAIL=771 BLOCKED=0 |
| Runtime Mismatch Analysis | PASS | mismatches=771 critical=0 categories={'known_not_next': 102, 'libmodsecurity_collection_name_case_semantics': 36, 'libmodsecurity_collection_semantics': 24, 'libmodsecurity_transformation_semantics': 24, 'libmodsecurity_xml_parser_semantics': 12, 'nginx_phase4_response_body_enforcement_gap': 22, 'nolog_expected_no_audit': 6, 'phase4_rule_match_no_disruptive_intervention': 6, 'secaction_detection_only_overlay': 6, 'with_mrts_detection_only_overlay': 533} |
| Final Consistency Audit | PASS | needs_attention |
| Missing Inputs / Skipped Reports | WARN | full_runtime_matrix, full_matrix_job_completeness, verified_runtime_mismatch_analysis, nginx_mrts_http500_cluster_analysis, connector_work_queue, phase_work_queue, nolog_audit_evidence, response_header_hook_analysis, phase4_hard_abort_capability, remaining_failure_analysis, intervention_blocking_analysis, no_mrts_intervention_nomatch_analysis, body_processor_analysis, rule_chain_semantics_analysis, final_consistency_audit |
| Optional Producer Evidence | WARN | native_mrts_reports, native_semantics_comparison |
| Stale Reports | WARN | nginx_mrts_http500_cluster_analysis, connector_work_queue, phase_work_queue, native_semantics_comparison, nolog_audit_evidence, response_header_hook_analysis, phase4_hard_abort_capability, remaining_failure_analysis, intervention_blocking_analysis, no_mrts_intervention_nomatch_analysis, body_processor_analysis, rule_chain_semantics_analysis, final_consistency_audit, report_dependency_graph, report_data_lineage |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | WARN | full_runtime_matrix, full_matrix_job_completeness, verified_runtime_mismatch_analysis, nginx_mrts_http500_cluster_analysis, final_consistency_audit, merge_readiness_dashboard |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent |

## Decision

Merge readiness: `UNKNOWN`

Reason: Critical producer evidence was not generated in this verified run.

## Evidence

- Verified run id: `2026-06-16T19-12-00Z-614c8049`
- Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
- Framework SHA: `4e9d4ba616235127b6fc0a2ee87107d93d03f40b`
- Primary blocker: `unknown`
- Recommended next fix cluster: `multipart_files`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `771` / `0`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3157` / `771` / `0` / `0`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `9b718cee0523da3e0822754dc4b05f327b6d969d` | `feature/all-connectors-no-crs-baseline` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `4e9d4ba616235127b6fc0a2ee87107d93d03f40b` | `feature/all-connectors-no-crs-baseline` | clean | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `<local-home-root>/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `340546dbab42432eef255f99fda65c0d4301db589d6ac5c9f2a201a94326420e` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `d969736e6a6b68e331b83c17dd8edb8516314b1d78dd5e8c9ab41806bfea1502` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `486d395cbc4da9e489dcc2f81e0fda69c34e66971e03133f02f797570f9a2400` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `6da46416596c15b4128953cdcbdbef2198173ad7537f0e48ba4428767437ba47` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
