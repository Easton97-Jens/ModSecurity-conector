> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:40:14Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `58b2135bb8adf12a4cad8afb448d1156e801cc00`
> Framework SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
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
| Submodule Status | WARN | parent, framework_submodule |

## Decision

Merge readiness: `WARN`

Reason: Core canonical reports are generated; warning conditions are documented.

## Evidence

- Verified run id: `2026-06-16T19-12-00Z-614c8049`
- Connector SHA: `58b2135bb8adf12a4cad8afb448d1156e801cc00`
- Framework SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
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
| parent | `.` | `58b2135bb8adf12a4cad8afb448d1156e801cc00` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `8e2d2ac2aff46856cd32e419ff73f333ce37a5321b15fad5f8b93bff85c1f16e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `682daa5f4a31c9630b61a6bb5cc29090283acfdbfe6c37a3da83ce0008e437e1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `d31ab608dc993cfc14d4e8f35efb90bf8b05b7525aece85acac725e5232bca68` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `cde00865dd00752f1a857c92f0f9db74adaa032921c7619bec174a9371034d23` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `2db466da1006f40605c3fbf9be46e8f370d486be124f3e288e573a1cff96a29f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `e422a08561f2a79a4298b4c89b237d4fefe174c373758ed8df5978f516326468` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
