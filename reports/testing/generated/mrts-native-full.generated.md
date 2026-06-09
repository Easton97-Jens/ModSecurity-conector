# MRTS Native Infrastructure Report

Generated at: `2026-06-09T18:33:59Z`

## Executive Summary
- PASS: **0**
- FAIL: **0**
- BLOCKED: **2**
- NOT_RUN: **0**

## Native Target Summary
| Target | Status | Reason | Run log | Summary |
|---|---|---|---|---|
| apache2_ubuntu | BLOCKED | missing native dependencies: go-ftw (set GO_FTW_BIN), albedo (set ALBEDO_BIN), apachectl (set APACHECTL_BIN) | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json` |
| nginx-pr24 | BLOCKED | missing native dependencies: go-ftw (set GO_FTW_BIN), albedo (set ALBEDO_BIN), nginx (set MRTS_NATIVE_NGINX_BIN), ngx_http_modsecurity_module.so (set MRTS_NATIVE_NGINX_MODULE_DIR) | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `$MRTS_NATIVE_ROOT/nginx-pr24/job.json` |

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
- apache2_ubuntu: `go-ftw` missing; set `GO_FTW_BIN`. Scope: native MRTS targets and mrts-ftw-style go-ftw execution. Set GO_FTW_BIN to a local go-ftw binary.
- apache2_ubuntu: `albedo` missing; set `ALBEDO_BIN`. Scope: native MRTS targets only. Set ALBEDO_BIN to a local albedo backend binary.
- apache2_ubuntu: `apachectl` missing; set `APACHECTL_BIN`. Scope: apache2_ubuntu native MRTS target only. Set APACHECTL_BIN to a local apachectl-compatible binary.
- nginx-pr24: `go-ftw` missing; set `GO_FTW_BIN`. Scope: native MRTS targets and mrts-ftw-style go-ftw execution. Set GO_FTW_BIN to a local go-ftw binary.
- nginx-pr24: `albedo` missing; set `ALBEDO_BIN`. Scope: native MRTS targets only. Set ALBEDO_BIN to a local albedo backend binary.
- nginx-pr24: `nginx` missing; set `MRTS_NATIVE_NGINX_BIN`. Scope: nginx-pr24 native MRTS target only. Set MRTS_NATIVE_NGINX_BIN to a local nginx binary.
- nginx-pr24: `ngx_http_modsecurity_module.so` missing; set `MRTS_NATIVE_NGINX_MODULE_DIR`. Scope: nginx-pr24 native MRTS target only. Set MRTS_NATIVE_NGINX_MODULE_DIR to a local directory containing ngx_http_modsecurity_module.so.

## Comparison Hints
- Compare native MRTS results with connector smoke evidence by target and corpus.
- Classification metadata explains gaps but never changes runtime PASS/FAIL/BLOCKED.

## Guardrails
- Native staging happens under `MRTS_NATIVE_ROOT`; repository sources are read-only inputs.
- `tools/MRTS` and MRTS definitions are not edited by native report generation.
- Generated MRTS rules, go-ftw YAML, load files, logs, and native results are not committed.
