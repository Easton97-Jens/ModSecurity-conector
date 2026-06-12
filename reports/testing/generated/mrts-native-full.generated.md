# MRTS Native Infrastructure Report

Generated at: `2026-06-12T17:00:55Z`

## Executive Summary
- PASS: **0**
- FAIL: **2**
- BLOCKED: **0**
- NOT_RUN: **0**

## Native Target Summary
| Target | Status | Reason | Run log | Summary |
|---|---|---|---|---|
| apache2_ubuntu | FAIL | native MRTS go-ftw run failed | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json` |
| nginx-pr24 | FAIL | native MRTS go-ftw run failed | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `$MRTS_NATIVE_ROOT/nginx-pr24/job.json` |

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
- nginx-pr24: go-ftw is present; native execution reached go-ftw and failed during test execution.

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
- Status: `reused`
- Blocker: `-`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/build`
- apachectl/APACHECTL_BIN: `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/httpd/bin/apachectl-mrts`
- Module file: `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/build/output/apache/mod_security3.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `APACHECTL_BIN`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_1`
- CPPFLAGS: `-I/src/ModSecurity-conector-cache/prefix/expat/include`
- LDFLAGS: `-L/src/ModSecurity-conector-cache/prefix/expat/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `/src/ModSecurity-conector-cache/prefix/expat/lib/pkgconfig`
- crypt.h status: `present`
- crypt.h path: `/usr/include/crypt.h`
- libcrypt status: `present`
- libcrypt paths: `/usr/lib/x86_64-linux-gnu/libcrypt.so, /lib/x86_64-linux-gnu/libcrypt.so, /usr/lib/x86_64-linux-gnu/libcrypt.so.1, /lib/x86_64-linux-gnu/libcrypt.so.1`
- crypt link mode: `compiler:-lcrypt`

### NGINX
- Status: `reused`
- Blocker: `-`
- Cache path: `/src/ModSecurity-conector-cache/archives/nginx`
- Build path: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/build`
- MRTS_NATIVE_NGINX_BIN: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules`
- Module file: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

### Expat
- Status: `present`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_1`
- Actual head: `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19`
- Prefix: `/src/ModSecurity-conector-cache/prefix/expat`
- expat.h: `/src/ModSecurity-conector-cache/prefix/expat/include/expat.h`
- lib dir: `/src/ModSecurity-conector-cache/prefix/expat/lib`
- Recursive submodules: `-`

### go-ftw / albedo
| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `/src/ModSecurity-conector-cache/bin/go-ftw` | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `/src/ModSecurity-conector-cache/bin/albedo` | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `-` | - | - |
<!-- runtime-components:end -->

<!-- runtime-diagnostics:start -->
## Native Runtime Diagnostics

- No generated native runtime diagnostics were detected.
<!-- runtime-diagnostics:end -->

<!-- runtime-build-cache:start -->
## Runtime Build Cache
- Shared ModSecurity status: `reused`
- Shared ModSecurity source ref/SHA: `v3/master` / `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Shared ModSecurity build ID: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Shared ModSecurity prefix: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Build reuse summary: rebuilt `0`, reused `3`, blocked `0`, saved rebuilds estimate `3`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | reused | `030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - |
| nginx | reused | `24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - |
| haproxy | reused | `8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - |
<!-- runtime-build-cache:end -->
