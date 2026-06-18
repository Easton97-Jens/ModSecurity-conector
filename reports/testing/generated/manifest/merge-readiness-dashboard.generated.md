> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T16:15:42Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
> Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3141 FAIL=775 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=787 critical=107 categories={'connector_capability_gap': 27, 'expected_status_mismatch': 43, 'framework_expected_behavior_gap': 1, 'known_not_next': 102, 'libmodsecurity_collection_name_case_semantics': 36, 'libmodsecurity_collection_semantics': 24, 'nolog_expected_no_audit': 6, 'runtime_regression': 18, 'timeout_or_incomplete': 12, 'unknown': 6, 'with_mrts_detection_only_overlay': 512} |
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
- Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
- Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
- Primary blocker: `multipart_files`
- Recommended next fix cluster: `multipart_files`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `787` / `107`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3141` / `775` / `0` / `12`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `93172ef0f7d4e3fc4a10e97d63aefe982a593b55` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `131fdad6974cf0f67a874f7c1b1a118c4b25f303` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `94ef7376661e451a7c3a25bd98cb9b769096cd64fe85684fa62e6cef951a017e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `509bc6777259ded64851696daa44ebc1785e6850d74245f62002fca00b89d4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `1f770179e24029f85d2b7b994d225a2f66512e10e22ce854ad80379ecb7381dc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `05bc958c83d0fba9f7991380580343ddbe984c2e25b5cd856adc79de70f55828` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `4aec42cd1ad41e7d8f3aeff9311774b32f29c12aca6fccc73468054dd890c6a2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `d95b56797386aba3174e29391dae144e15462dcd9397c4b066a49c4fa170f000` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
