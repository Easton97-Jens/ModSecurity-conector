# MRTS Native Infrastructure Report

Generated at: `2026-06-09T15:45:28Z`

## Executive Summary
- PASS: **0**
- FAIL: **0**
- BLOCKED: **2**
- NOT_RUN: **0**

## Native Target Summary
| Target | Status | Reason | Run log | Summary |
|---|---|---|---|---|
| apache2_ubuntu | BLOCKED | missing native dependencies: go-ftw, albedo, apachectl | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json` |
| nginx-pr24 | BLOCKED | missing native dependencies: go-ftw, albedo, nginx, ngx_http_modsecurity_module.so | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `$MRTS_NATIVE_ROOT/nginx-pr24/job.json` |

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

## Comparison Hints
- Compare native MRTS results with connector smoke evidence by target and corpus.
- Classification metadata explains gaps but never changes runtime PASS/FAIL/BLOCKED.

## Guardrails
- Native staging happens under `MRTS_NATIVE_ROOT`; repository sources are read-only inputs.
- `tools/MRTS` and MRTS definitions are not edited by native report generation.
- Generated MRTS rules, go-ftw YAML, load files, logs, and native results are not committed.
