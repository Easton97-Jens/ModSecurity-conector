> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:22:44Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `blocked`

# Merge Readiness Dashboard

Merge Readiness: `UNKNOWN`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | UNKNOWN | complete=False jobs=0/0 missing=[] runtime_timeout=False refresh_timeout=False PASS=- FAIL=- BLOCKED=- |
| Runtime Mismatch Analysis | UNKNOWN | mismatches=0 critical=0 categories={} |
| Final Consistency Audit | PASS | unknown |
| Missing Inputs / Skipped Reports | WARN | full_runtime_matrix, full_matrix_job_completeness, verified_runtime_mismatch_analysis |
| Optional Producer Evidence | WARN | native_mrts_reports |
| Stale Reports | WARN | nginx_mrts_http500_cluster_analysis, report_dependency_graph, report_data_lineage |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | WARN | full_runtime_matrix, full_matrix_job_completeness, verified_runtime_mismatch_analysis, nginx_mrts_http500_cluster_analysis, final_consistency_audit, merge_readiness_dashboard, report_refresh_manifest |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent, framework_submodule |

## Decision

Merge readiness: `UNKNOWN`

Reason: Full-Matrix evidence is incomplete; 0/0 jobs complete; missing jobs: unknown.

## Evidence

- Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
- Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
- Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
- Primary blocker: `unknown`
- Recommended next fix cluster: `unknown`
- Evidence scope: `unknown`
- Full-Matrix complete: `False`
- Full-Matrix completeness: `0` / `0`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `0` / `0`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `-` / `-` / `-` / `-`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `efac6d66d0e165af8d6e1b5404083d5f50601327` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `04e31a60676eebba86be2a4c1510ff596e37ba2f` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `74dff241151f409d4a958eff005fd65b7e0dc5e03a886ad44bcfc2084e52585f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `052ecc3d98a7bb1608fdfc517a762d02386ddb4a648c000fdcc54a38fc291d80` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `21f2c11040b4c146bdde0a6edec38176b65393d39e564398a6cc64773ec0855b` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `c27eb0b4dfb6334be9af6aa87597368c2107b924b11689250583fba45df4b7f2` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `99c88712991be652654f3fb3818eec7bc1a0635b1c43fcd0c548a40a00a16133` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `7d4f982b8cc29d3c1b36b372ceaedf66a18ed73e9d0ac3dadae9ba7bd93d3d0f` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
