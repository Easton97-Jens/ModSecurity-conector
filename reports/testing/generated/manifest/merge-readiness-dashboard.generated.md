> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:58:01Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
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
| Submodule Status | WARN | parent, framework_submodule |

## Decision

Merge readiness: `FAIL`

Reason: Full-Matrix runtime completed with critical mismatches; downstream refresh timed out or stale reports remain.

## Evidence

- Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
- Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
- Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
- Recommended next fix cluster: `nginx_actual_500`
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
| parent | `.` | `9391a8d0d5bf170f8af994c361f0b9fa50015834` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `708183dce7dcd0ad190a5cb5211b1ba3de6a2385` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `708183dce7dcd0ad190a5cb5211b1ba3de6a2385` | `master` | clean | present |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `6ad06c76b68ec65d7a60b26b5409cfa84c7277e45c1c48488bc3c081dec5e49f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `83d51671872ea0d825c2c8cb8b45513768809f0538f240eae04881bbdc7d52c1` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `9e1ead55a10b0f6205588b4c14516da3e47df27279a2062d577d73e9ba53bd2b` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `6a543b34e8941ce08cc523fbb3492eeeeaed4f16ac4b925105f87bdb71c1247d` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `7d6a5dc9ffaf32181caa561e8371b8b73077a42b7350d56dea0c2c497712934d` | `2026-06-15T21-01-39Z-9391a8d0` | stale |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `2807595d703e53d7e3978b755880bd735533d6fcf1ac8d364694e927eae0ca8a` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
