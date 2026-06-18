> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T21:57:21Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `29083baa42f7cae3aff7c9f340e2fbe437dd410d`
> Framework SHA: `c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3104 FAIL=776 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=824 critical=216 categories={'connector_capability_gap': 63, 'expected_status_mismatch': 51, 'known_not_next': 102, 'libmodsecurity_collection_semantics': 24, 'runtime_regression': 42, 'timeout_or_incomplete': 48, 'unknown': 12, 'with_mrts_detection_only_overlay': 482} |
| Final Consistency Audit | PASS | needs_attention |
| Missing Inputs / Skipped Reports | PASS | none |
| Optional Producer Evidence | PASS | available/not required |
| Stale Reports | PASS | none |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | WARN | report_refresh_manifest |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent, framework_submodule |

## Decision

Merge readiness: `FAIL`

Reason: Full-Matrix runtime completed with critical mismatches; downstream reports remain blocked, stale, or unknown.

## Evidence

- Verified run id: `2026-06-16T19-12-00Z-614c8049`
- Connector SHA: `29083baa42f7cae3aff7c9f340e2fbe437dd410d`
- Framework SHA: `c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67`
- Primary blocker: `multipart_files`
- Recommended next fix cluster: `multipart_files`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `824` / `216`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3104` / `776` / `0` / `48`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `29083baa42f7cae3aff7c9f340e2fbe437dd410d` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `5eb9a018436e2edd12871ccb50aea3f84e08ae00118acfd315399a8f8f7d0512` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `0973c2753c21d2085a5724356db258651404510e5297dce370b88760f78871a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `eea11d4e31ff16f2997361464a145d25d7a204249ae38017f4ae4b8be5642949` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `bf94318ee4981b80cb2d08e43a02a93a0ff4e20ddf22c88e8b79766ac4bb71f7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `15213b816bf77652e20b9699c24773958abed3cfddca3e4e21c02e73296e8f5e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `07d223879799a8ef18fa7bc4d755ead0bdb8da8fb735f3b40b1569e57bb13e17` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
