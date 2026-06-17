> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:40:22Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `FAIL`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | complete=True jobs=12/12 missing=[] runtime_timeout=False refresh_timeout=False PASS=3074 FAIL=782 BLOCKED=0 |
| Runtime Mismatch Analysis | FAIL | mismatches=854 critical=764 categories={'connector_capability_gap': 117, 'expected_status_mismatch': 377, 'framework_expected_behavior_gap': 24, 'known_not_next': 90, 'runtime_regression': 162, 'timeout_or_incomplete': 72, 'unknown': 12} |
| Final Consistency Audit | PASS | ready_with_known_reported_gaps |
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
- Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
- Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
- Primary blocker: `none`
- Recommended next fix cluster: `none`
- Evidence scope: `full`
- Full-Matrix complete: `True`
- Full-Matrix completeness: `12` / `12`
- Missing Full-Matrix jobs: `-`
- Full-Matrix refresh timeout: `False`
- Runtime mismatches / critical: `854` / `764`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3074` / `782` / `0` / `72`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `614c80493b6ebd25a17e1d27979071e5e30584d4` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `24509c107ecf3a22ae9d69875f661690bd6fb95b` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `676cc8d9b51b9294387e0b73fe8a7ff1f78a4fe5ff268f5996cb1967b906c576` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `b6ce3c02e4ed81d078fb8cd9971b03719d558ca1ab79aca20f5d6aada335deee` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `a59343bebc59e34142df37e8f867b013b9185b07889ff9407d7fbed05fa12f53` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `56d43bad850595932f10e7e412d8d7a2a63b60ec8a170535015b7eb12ad7f15d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `6f7c469a2eb7869d6b401cf502cf6195bd3c0efecea4f83192c051a11797dd6a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `a641435cfc5eeaa17ca31ae9d560e1c933286f87c8e6f240d3ae3094afb184aa` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
