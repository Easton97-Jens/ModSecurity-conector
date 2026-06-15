> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:39:57Z`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Make target: `mrts-native-full-run`
> Owner: `mrts`
> Severity: `optional`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `missing`

# MRTS Native Infrastructure Report

Generated at: `2026-06-15T10:39:57Z`

## Executive Summary
- PASS: **0**
- FAIL: **0**
- BLOCKED: **0**
- NOT_RUN: **2**

## Split Native Reports
- Apache native: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

These native MRTS reports are separate from connector full-matrix evidence.

## Native Target Summary
| Target | Status | Attempted | PASS | FAIL | BLOCKED | Reason | Run log | Summary |
|---|---|---:|---:|---:|---:|---|---|---|
| apache2_ubuntu | NOT_RUN | 0 | 0 | 0 | 0 | native target job.json not found | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `-` |
| nginx-pr24 | NOT_RUN | 0 | 0 | 0 | 0 | native target job.json not found | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `-` |

## Apache2 Ubuntu Native Infra
- Source: `$MRTS_ROOT/config_infra/apache2_ubuntu` staged under `MRTS_NATIVE_ROOT`.
- Evidence is native MRTS infrastructure evidence and does not replace connector smoke evidence.

## NGINX PR24 Native Infra
- PR URL: https://github.com/owasp-modsecurity/MRTS/pull/24
- PR number: 24
- PR head SHA: `134ea7e35d72e7d72294b66d80dafa07daa5fc92`
- Captured at UTC: `2026-06-09T15:18:21Z`
- Upstream status: `open-pr`
- Stability: `experimental`
- Replacement note: replace with $MRTS_ROOT/config_infra/nginx_linux once merged upstream

## Known Limitations
- Phase 4 and RESPONSE_BODY native evidence remains non-promoted.
- Missing native binaries, modules, go-ftw, or backend tooling is reported as BLOCKED.

## Missing Dependency Remediation
- No missing native dependencies were reported in this run.

## Comparison Hints
- Compare native MRTS results with connector smoke evidence by target and corpus.
- Classification metadata explains gaps but never changes runtime PASS/FAIL/BLOCKED.

## Guardrails
- Native staging happens under `MRTS_NATIVE_ROOT`; repository sources are read-only inputs.
- `tools/MRTS` and MRTS definitions are not edited by native report generation.
- Generated MRTS rules, go-ftw YAML, load files, logs, and native results are not committed.

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/mrts-native/apache2_ubuntu/job.json` | missing | input file missing |
| `/root/.local/state/ModSecurity-conector-build/mrts-native/nginx-pr24/job.json` | missing | input file missing |
