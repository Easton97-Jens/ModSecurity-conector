> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:40:38Z`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `complete`

# Merge Readiness Dashboard

Merge Readiness: `WARN`

## Summary

| Check | Status | Notes |
|---|---|---|
| Full Runtime Matrix | PASS | PASS=3074 FAIL=782 BLOCKED=0 |
| Final Consistency Audit | PASS | ready_with_known_reported_gaps |
| Missing Inputs / Skipped Reports | WARN | runtime_cache_reports |
| Stale Reports | PASS | none |
| Failed Generators | PASS | none |
| Submodule Status | WARN | parent |

## Decision

Merge readiness: `WARN`

Reason: Core canonical reports are generated; warning conditions are documented.

## Evidence

- Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
- Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
- Recommended next fix cluster: `none`
- Full-Matrix PASS/FAIL/BLOCKED/NOT_EXECUTABLE: `3074` / `782` / `0` / `72`

## Submodules

| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6` | `report-governance-proof-layout` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `61454d23be52e52d9395e6b091c52d651e16f89b` | `runtime-source-https-policy` | clean | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `61454d23be52e52d9395e6b091c52d651e16f89b` | `runtime-source-https-policy` | clean | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
