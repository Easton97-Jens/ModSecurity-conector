> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:48:43Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3141 FAIL=775 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=787 critical=83 categories={'connector_capability_gap': 27, 'expected_status_mismatch': 31, 'framework_expected_behavior_gap': 1, 'known_not_next': 102, 'libmodsecurity_collection_name_case_semantics': 36, 'libmodsecurity_collection_semantics': 24, 'libmodsecurity_transformation_semantics': 24, 'nolog_expected_no_audit': 6, 'runtime_regression': 6, 'timeout_or_incomplete': 12, 'unknown': 6, 'with_mrts_detection_only_overlay': 512} |
| Final Consistency Audit | PASS | needs_attention |
| Missing Inputs / Skipped Reports | PASS | none |
| Optional Producer Evidence | PASS | available/not required |
| Stale Reports | PASS | none |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | PASS | fresh |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent, framework_submodule |

## Decision

Merge readiness: `FAIL`

Reason: Full-Matrix completed and critical runtime mismatches are present.

## Evidence

- Verified run id: `2026-06-16T19-12-00Z-614c8049`
- Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
- Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
- Primary blocker: `multipart_files`
- Recommended next fix cluster: `multipart_files`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `787` / `83`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3141` / `775` / `0` / `12`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `2334d31b942fd79770c7381b02fcaf031cccc4d2` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `890da243b91305746a7f8658e29fd2e9f814b10a001885be834c69bed542dba2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `06ccc48b304f836f75d06b5343edae8e966492cdc91bb13e3cfef4f62159bc49` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `31a8d27c3d070d7f919fd623d79f5be158e4a46a578fc526db20142a23b80a95` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `23d490410f677c4d0c3705b1a2315860fbb6c1275c94a8c085bc4c23c3918ca8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `dc80194255be5520bb8d5768e95f9b0990ae0256bf9264458ac1b5449be5e600` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `61c0a9c5f0bea6171e8d1bd48e35873d594e48aa76cb05f1b54b11b7d28b514e` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
