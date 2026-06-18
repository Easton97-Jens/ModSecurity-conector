> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T11:26:39Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `1ed85089212c791958b5f09abf7b17d73bdfde91`
> Framework SHA: `9e2c82b829036d28f54459814773b92c801b6e24`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3120 FAIL=760 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=808 critical=152 categories={'connector_capability_gap': 51, 'expected_status_mismatch': 29, 'known_not_next': 102, 'libmodsecurity_collection_name_case_semantics': 24, 'libmodsecurity_collection_semantics': 24, 'nolog_expected_no_audit': 6, 'runtime_regression': 18, 'timeout_or_incomplete': 48, 'unknown': 6, 'with_mrts_detection_only_overlay': 500} |
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
- Connector SHA: `1ed85089212c791958b5f09abf7b17d73bdfde91`
- Framework SHA: `9e2c82b829036d28f54459814773b92c801b6e24`
- Primary blocker: `multipart_files`
- Recommended next fix cluster: `multipart_files`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `808` / `152`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3120` / `760` / `0` / `48`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `1ed85089212c791958b5f09abf7b17d73bdfde91` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `9e2c82b829036d28f54459814773b92c801b6e24` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `151fed6d47dda6380e0ece49684d4a9c333f464846e3810c5466cbdab5f72950` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `f0b86c64ce32e2bd1ff2a56c6242f01f8d01f8fa4af0fd2801772622c3b62d4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `98790eeffd8d0ed96137ec3247f6c13ad3e70470df24bbb873030c5ba6d6eb41` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `8cbf4ad7816be93d057616a8e2dba7146906c56f5e93e4202318b78607b91781` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `8199f2813c853163a3eddd848421bb327eacf6d75cc1a9e032d1943f5a2112fb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `62da18c8edc7e0c5554733cd3541f6dba2b7f0a223115531b66c5ee20b000978` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
