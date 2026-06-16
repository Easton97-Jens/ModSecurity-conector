> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T07:22:12Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `1e0c825de82d1325b5e7b070a4916de2f5af2207`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `blocked`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=2206 FAIL=1650 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=1733 critical=1639 categories={'connector_capability_gap': 117, 'expected_status_mismatch': 244, 'framework_expected_behavior_gap': 68, 'known_not_next': 94, 'runtime_regression': 1123, 'timeout_or_incomplete': 83, 'unknown': 4} |
| Final Consistency Audit | PASS | unknown |
| Missing Inputs / Skipped Reports | WARN | intervention_blocking_analysis, body_processor_analysis, rule_chain_semantics_analysis |
| Optional Producer Evidence | PASS | available/not required |
| Stale Reports | WARN | intervention_blocking_analysis, no_mrts_intervention_nomatch_analysis, body_processor_analysis, rule_chain_semantics_analysis, final_consistency_audit |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | WARN | final_consistency_audit, merge_readiness_dashboard, report_refresh_manifest |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent, framework_sibling_checkout |

## Decision

Merge readiness: `FAIL`

Reason: Full-Matrix runtime completed with critical mismatches; downstream refresh timed out or stale reports remain.

## Evidence

- Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
- Connector SHA: `1e0c825de82d1325b5e7b070a4916de2f5af2207`
- Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
- Primary blocker: `nginx_with_crs_with_mrts_http500_cluster`
- Recommended next fix cluster: `nginx_with_crs_with_mrts_http500_cluster`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `1733` / `1639`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `2206` / `1650` / `0` / `72`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `1e0c825de82d1325b5e7b070a4916de2f5af2207` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `04e31a60676eebba86be2a4c1510ff596e37ba2f` | `master` | clean | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `708183dce7dcd0ad190a5cb5211b1ba3de6a2385` | `master` | clean | differs |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `9ba0e705e79616868c41e57959d7b80963efd1859039704bfa46aab2e9648fe5` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `13a80bd86eb41c43a4567eeae5f18fee50e649bde9f14abefa5416b1a68d7923` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `508928faaf13e7e8f786fc0ff444b0d66c93a791ac2bc43fccb7e2f48764a029` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `ff38f4488db455098e339d2d81c5e3d21d3026bf8669e640a320d362be5ec346` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `17e62a146094e8a9c60599e449527ccf5b2827493236737c5cf145cc14fe0d7f` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `3c7572b01c3ec9f14b168b7ddeedf8ca6c518b519f9d598ae2d229fb50b70feb` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
