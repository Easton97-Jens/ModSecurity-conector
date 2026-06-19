> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:44:38Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3154 FAIL=774 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=774 critical=46 categories={'connector_capability_gap': 15, 'expected_status_mismatch': 19, 'known_not_next': 102, 'libmodsecurity_collection_name_case_semantics': 36, 'libmodsecurity_collection_semantics': 24, 'libmodsecurity_transformation_semantics': 24, 'libmodsecurity_xml_parser_semantics': 12, 'nolog_expected_no_audit': 6, 'runtime_regression': 6, 'unknown': 6, 'with_mrts_detection_only_overlay': 524} |
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
- Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
- Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
- Primary blocker: `multipart_files`
- Recommended next fix cluster: `multipart_files`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `774` / `46`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3154` / `774` / `0` / `0`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `02d952fa8a986ef519c671973809d7634998e961` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `62c5dce8733d77138999bf6054fd4b1ec1712d40` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `fdaa878e3a9e246ae057fe7b46c2208f20c4aa87cc7fbf1e679467bfcfe69d25` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `6934388824f6a335f3ffb3e8282b0c0ec98d28b3e466b9bce7266e9db3b5fcd4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `90c84d11f426f45af700e33fe389db832ba4f8e5da315459af31e5903c0ff77a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f264523d6bb83b4a3382d4871099d221aac496d36dc8697548b4bba10fd2e52a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `e90c02f636c5b356c7db009eb39b4997c83b6db20d64fc90f796fec9ff3083e8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `f2f33b246130a9b3f5821e2fa4158f601590b32ce042f9bedb3e97d5510cd37b` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
