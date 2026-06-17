> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T15:48:04Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
> Input status: `blocked`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3092 FAIL=788 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=836 critical=264 categories={'connector_capability_gap': 63, 'expected_status_mismatch': 51, 'framework_expected_behavior_gap': 24, 'known_not_next': 102, 'runtime_regression': 66, 'timeout_or_incomplete': 48, 'unknown': 12, 'with_mrts_detection_only_overlay': 470} |
| Final Consistency Audit | PASS | unknown |
| Missing Inputs / Skipped Reports | PASS | none |
| Optional Producer Evidence | WARN | native_mrts_reports |
| Stale Reports | PASS | none |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | WARN | final_consistency_audit, merge_readiness_dashboard, report_refresh_manifest |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent, framework_submodule |

## Decision

Merge readiness: `FAIL`

Reason: Full-Matrix runtime completed with critical mismatches; downstream reports remain blocked, stale, or unknown.

## Evidence

- Verified run id: `2026-06-16T19-12-00Z-614c8049`
- Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
- Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
- Primary blocker: `unknown`
- Recommended next fix cluster: `unknown`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `836` / `264`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3092` / `788` / `0` / `48`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `dd6e0455c4838949ce86cff81ce89dccd4e524f8` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `ee23a10d5224401d9e63f28ad374969ac129e5f0` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `b73e9279de250d71c12b771bc4c24bb4b712dac0fed0008c60f6075116916797` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `6bc04b7e3157faa5f7d32e333051db6fe568b604eef038f0706c32d1f2028cac` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `702781e5bf78f77097a22e2e367dca491d4489a30e161182f9f298823200008b` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `18f53c9539c3c8d74bd89e6549062846275bbb678857522f3f76ab99af603989` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `df41566492fb236cb03508161261b1eedb8745fc8aa07feff56de02969cb50fb` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `0c036a4c26146a877bf7071392cd519df44326eea28d9fd2ff1dfb6d2a2822f5` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
