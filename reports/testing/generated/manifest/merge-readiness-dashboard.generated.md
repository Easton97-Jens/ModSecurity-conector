> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:58:49Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
> Input status: `blocked`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=2046 FAIL=534 BLOCKED=4 |
| Runtime Mismatch Analysis | FAIL | mismatches=586 critical=524 categories={'connector_capability_gap': 80, 'expected_status_mismatch': 256, 'framework_expected_behavior_gap': 16, 'known_not_next': 62, 'runtime_regression': 110, 'timeout_or_incomplete': 52, 'unknown': 10} |
| Final Consistency Audit | PASS | unknown |
| Missing Inputs / Skipped Reports | WARN | intervention_blocking_analysis, body_processor_analysis, rule_chain_semantics_analysis |
| Optional Producer Evidence | PASS | available/not required |
| Stale Reports | WARN | intervention_blocking_analysis, no_mrts_intervention_nomatch_analysis, body_processor_analysis, rule_chain_semantics_analysis, final_consistency_audit |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | WARN | final_consistency_audit, merge_readiness_dashboard, report_refresh_manifest |
| Verified Run Consistency | WARN | system_environment_proof |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent, framework_submodule |

## Decision

Merge readiness: `FAIL`

Reason: Full-Matrix runtime completed with critical mismatches; downstream refresh timed out or stale reports remain.

## Evidence

- Verified run id: `2026-06-16T16-57-44Z-b53340a8`
- Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
- Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
- Primary blocker: `none`
- Recommended next fix cluster: `none`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `586` / `524`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `2046` / `534` / `4` / `48`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `b53340a84f9acd5fbc3aff3de136c92ac122c3fa` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `2b2e402708fca5ff40664926ff01c2c5e520a48a` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `f2c570c502a53acd154797e1b2b9bc6d6b2b49f76de90402a9a13b3d47d5077d` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `5a46b78e9b0b07805bfa70305a7f2fb7f907511087e8952d7ee18b91f6e9f5bb` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `8086864d8051f96776b54d45482eaf4b02e220dedc3ca191547c119ecfc4419b` | `2026-06-16T16-57-44Z-b53340a8` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f6134d5f7cc94e181c222e627cd7b4f3bb0a95a9ef85e0b63fb5b55b85268560` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `dd74444ee2dda65ac29c6c32ad15aa9592fbb95ad095f607e1b02e03b309e6d4` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `42ce0a3c896d910b3661dc67f79c957486c9e774d37b7adfa7eaca3c6edd143d` | `2026-06-16T16-57-44Z-b53340a8` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
