> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:53:02Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `WARN`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3157 FAIL=771 BLOCKED=0 |
| Runtime Mismatch Analysis | PASS | mismatches=771 critical=0 categories={'known_not_next': 102, 'libmodsecurity_collection_name_case_semantics': 36, 'libmodsecurity_collection_semantics': 24, 'libmodsecurity_transformation_semantics': 24, 'libmodsecurity_xml_parser_semantics': 12, 'nginx_phase4_response_body_enforcement_gap': 22, 'nolog_expected_no_audit': 6, 'phase4_rule_match_no_disruptive_intervention': 6, 'secaction_detection_only_overlay': 6, 'with_mrts_detection_only_overlay': 533} |
| Final Consistency Audit | PASS | needs_attention |
| Missing Inputs / Skipped Reports | PASS | none |
| Optional Producer Evidence | PASS | available/not required |
| Stale Reports | PASS | none |
| Report Refresh | PASS | completed/no timeout recorded |
| Critical Input Freshness | PASS | fresh |
| Verified Run Consistency | PASS | consistent |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent |

## Decision

Merge readiness: `WARN`

Reason: Core canonical reports are generated; warning conditions are documented.

## Evidence

- Verified run id: `2026-06-16T19-12-00Z-614c8049`
- Connector SHA: `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199`
- Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
- Primary blocker: `unknown`
- Recommended next fix cluster: `multipart_files`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `771` / `0`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3157` / `771` / `0` / `0`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `6e5fba8960f4cf3e8cb38bb870c2a15c271dd199` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `dc19582d89bd8ef50463c5a9c5a0271cc37bb958` | `master` | clean | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `d31fb8c743fe579a70cd77d1d455f749b99e3682d1737d2751c70f3b46c520a8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `a8909f651e4e60be0c10c6cb24a1c11f98b9e99845a47a31c42aa64a727c0e65` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `9e5065e706377fbcc774d1dc719a4d21a6b89df3253a5152bafb7ebb98047657` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `67eae92c2d1fde007978f559f16c43598eb52d2c4a80fd0bd171c4748cfb62ff` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `6d5df1521cb6cfe501824c42c2268704efba9b4f8650b1a3b7f5e118a95fdeda` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `e856939760c5a09019bf18123407cd8ed5cbb49d80c2f011ee9a2d1e1501d1bc` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
