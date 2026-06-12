# MRTS Native Infrastructure Report

Generated at: `2026-06-12T13:56:13Z`

## Executive Summary
- PASS: **0**
- FAIL: **0**
- BLOCKED: **1**
- NOT_RUN: **1**

## Native Target Summary
| Target | Status | Reason | Run log | Summary |
|---|---|---|---|---|
| apache2_ubuntu | NOT_RUN | native target job.json not found | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `-` |
| nginx-pr24 | BLOCKED | missing native dependencies: go-ftw (set GO_FTW_BIN), albedo (set ALBEDO_BIN) | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `$MRTS_NATIVE_ROOT/nginx-pr24/job.json` |

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
- nginx-pr24: `go-ftw` missing; set `GO_FTW_BIN`. Scope: native MRTS targets and mrts-ftw-style go-ftw execution. Set GO_FTW_BIN to a local go-ftw binary.
- nginx-pr24: `albedo` missing; set `ALBEDO_BIN`. Scope: native MRTS targets only. Set ALBEDO_BIN to a local albedo backend binary.

## Comparison Hints
- Compare native MRTS results with connector smoke evidence by target and corpus.
- Classification metadata explains gaps but never changes runtime PASS/FAIL/BLOCKED.

## Guardrails
- Native staging happens under `MRTS_NATIVE_ROOT`; repository sources are read-only inputs.
- `tools/MRTS` and MRTS definitions are not edited by native report generation.
- Generated MRTS rules, go-ftw YAML, load files, logs, and native results are not committed.

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `blocked`
- Blocker: `missing_expat_headers`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/tmp/modsec-native-local-build/apache-build`
- apachectl/APACHECTL_BIN: `/tmp/modsec-native-local-build/mrts-native/apache2_ubuntu/bin/apachectl`
- Module file: `/tmp/modsec-native-local-build/apache-build/output/apache/mod_security3.so`
- Missing file: `expat.h`
- Build component: `apache_httpd_source_build`
- Env variable to set: `CPPFLAGS/LDFLAGS`

### NGINX
- Status: `present`
- Blocker: `-`
- Cache path: `/src/ModSecurity-conector-cache/archives/nginx`
- Build path: `/tmp/modsec-native-local-build/nginx-build`
- MRTS_NATIVE_NGINX_BIN: `/tmp/modsec-native-local-build/nginx-runtime/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/tmp/modsec-native-local-build/nginx-runtime/nginx/modules`
- Module file: `/tmp/modsec-native-local-build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

### go-ftw / albedo
| Dependency | Status | Searched paths | Env override | Known source | Known ref | Can build locally | Blocker |
|---|---|---|---|---|---|---|---|
| go-ftw | blocked | `go-ftw`<br>`/src/ModSecurity-conector-cache/bin/go-ftw`<br>`/src/ModSecurity-conector-cache/tools/go-ftw`<br>`/tmp/modsec-native-local-build/bin/go-ftw`<br>`/tmp/modsec-native-local-build/tools/go-ftw`<br>`/tmp/modsec-native-local-build/mrts-native/bin/go-ftw` | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `-` | no | missing_go_ftw_source_ref |
| albedo | blocked | `albedo`<br>`/src/ModSecurity-conector-cache/bin/albedo`<br>`/src/ModSecurity-conector-cache/tools/albedo`<br>`/tmp/modsec-native-local-build/bin/albedo`<br>`/tmp/modsec-native-local-build/tools/albedo`<br>`/tmp/modsec-native-local-build/mrts-native/bin/albedo` | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `-` | no | missing_albedo_source_ref |
<!-- runtime-components:end -->
