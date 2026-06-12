# Full MRTS Runtime Evidence

Generated at: `2026-06-09T18:40:47Z`

## Source State
- Framework SHA: `d467034cdf3fb28cea5329f90d97eedc22e630cc`
- Connector SHA: `a9969f91ebe908d2440bd8ba296532b924189f62`
- Connector framework gitlink: `d467034cdf3fb28cea5329f90d97eedc22e630cc`
- Framework tools/MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`

## Commands
- Full matrix: `FRAMEWORK_ROOT=/root/git/ModSecurity-test-Framework SOURCE_ROOT=/src BUILD_ROOT=/tmp/modsec-full-run MATRIX_ROOT=/tmp/modsec-full-run/full-matrix PYTHONDONTWRITEBYTECODE=1 make full-matrix-parallel`
- MRTS native: `FRAMEWORK_ROOT=/root/git/ModSecurity-test-Framework BUILD_ROOT=/tmp/modsec-native-full-run MRTS_NATIVE_TARGETS="apache2_ubuntu nginx-pr24" PYTHONDONTWRITEBYTECODE=1 make mrts-native-full-run`

## Full Matrix Summary
- Make exit code: `2`
- BUILD_ROOT: `/tmp/modsec-full-run`
- MRTS_BUILD_ROOT: `/tmp/modsec-full-run/mrts`
- Totals: `{'attempted': 2628, 'blocked': 1304, 'fail': 304, 'not_executable': 24, 'pass': 1000, 'pending': 1532}`

| Connector | Jobs | Outcomes | Attempted | PASS | FAIL | BLOCKED | Not executable | Pending |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| apache | 4 | `{'BLOCKED': 4}` | 0 | 0 | 0 | 4 | 0 | 0 |
| haproxy | 4 | `{'FAIL': 4}` | 1300 | 0 | 0 | 1300 | 0 | 766 |
| nginx | 4 | `{'FAIL': 4}` | 1328 | 1000 | 304 | 0 | 24 | 766 |

## MRTS Native Summary
- Make exit code: `2`; target script exit code: `77`
- BUILD_ROOT: `/tmp/modsec-native-full-run`
- MRTS_BUILD_ROOT: `/tmp/modsec-native-full-run/mrts`
- MRTS_NATIVE_ROOT: `/tmp/modsec-native-full-run/mrts-native`

| Target | Status | Exit code | Reason | Run log | Summary |
|---|---|---:|---|---|---|
| apache2_ubuntu | BLOCKED | 77 | missing native dependencies: go-ftw (set GO_FTW_BIN), albedo (set ALBEDO_BIN), apachectl (set APACHECTL_BIN) | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json` |
| nginx-pr24 | BLOCKED | 77 | missing native dependencies: go-ftw (set GO_FTW_BIN), albedo (set ALBEDO_BIN), nginx (set MRTS_NATIVE_NGINX_BIN), ngx_http_modsecurity_module.so (set MRTS_NATIVE_NGINX_MODULE_DIR) | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `$MRTS_NATIVE_ROOT/nginx-pr24/job.json` |

## External Blockers
- apache: `expat.h` missing; Provide local CPPFLAGS/LDFLAGS for expat headers/libs or install the matching system development package outside this run.
- haproxy: `crypt.h` missing; Provide local CPPFLAGS/LDFLAGS for crypt headers/libs or install the matching system development package outside this run.
- apache2_ubuntu: `go-ftw` missing; set `GO_FTW_BIN`. Scope: native MRTS targets and mrts-ftw-style go-ftw execution.
- apache2_ubuntu: `albedo` missing; set `ALBEDO_BIN`. Scope: native MRTS targets only.
- apache2_ubuntu: `apachectl` missing; set `APACHECTL_BIN`. Scope: apache2_ubuntu native MRTS target only.
- nginx-pr24: `go-ftw` missing; set `GO_FTW_BIN`. Scope: native MRTS targets and mrts-ftw-style go-ftw execution.
- nginx-pr24: `albedo` missing; set `ALBEDO_BIN`. Scope: native MRTS targets only.
- nginx-pr24: `nginx` missing; set `MRTS_NATIVE_NGINX_BIN`. Scope: nginx-pr24 native MRTS target only.
- nginx-pr24: `ngx_http_modsecurity_module.so` missing; set `MRTS_NATIVE_NGINX_MODULE_DIR`. Scope: nginx-pr24 native MRTS target only.

## Reports And Logs
- Full matrix report: `reports/testing/generated/full-runtime-matrix.generated.md`
- Connector work queue: `reports/testing/generated/connector-work-queue.generated.md`
- Phase work queue: `reports/testing/generated/phase-work-queue.generated.md`
- MRTS native report: `reports/testing/generated/mrts-native-full.generated.md`
- Full matrix logs: `/tmp/modsec-full-run/full-matrix/**/run.log`
- MRTS native logs: `/tmp/modsec-native-full-run/mrts-native/*/run.log`

## Fixes Applied
- Allowed connector runtime/log/result roots under the requested BUILD_ROOT for isolated /tmp full-matrix jobs while preserving SOURCE_ROOT guardrails.
- Switched pinned Apache source download default to archive.apache.org after downloads.apache.org returned 404 for the pinned httpd release.
- Added Apache expat.h and HAProxy crypt.h preflight checks with clear local CPPFLAGS/LDFLAGS remediation instead of late compile failure.
- Made full-matrix HAProxy jobs reuse shared build artifacts while keeping per-job tmp/log/result roots isolated.
- Added GO_FTW_BIN and ALBEDO_BIN support plus native report remediation metadata for missing native tools.

## Guardrails
- No push performed.
- No `tools/MRTS` changes.
- No MRTS definition changes.
- No generated MRTS rules, FTW YAML, or `mrts.load` committed.
- No `/tmp`, `/src`, or BUILD_ROOT outputs committed.
- Runtime PASS/FAIL values were not manually changed.

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `blocked`
- Blocker: `missing_crypt_library`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/tmp/modsec-native-local-tools/apache-build`
- apachectl/APACHECTL_BIN: `/tmp/modsec-native-local-tools/mrts-native/apache2_ubuntu/bin/apachectl`
- Module file: `/tmp/modsec-native-local-tools/apache-build/output/apache/mod_security3.so`
- Missing file: `libcrypt.so development link target or explicit -lcrypt linkage`
- Build component: `apache_httpd_source_build`
- Env variable to set: `LIBS/LDFLAGS`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_1`
- CPPFLAGS: `-I/src/ModSecurity-conector-cache/prefix/expat/include`
- LDFLAGS: `-L/src/ModSecurity-conector-cache/prefix/expat/lib`
- LIBS: `/usr/lib/x86_64-linux-gnu/libcrypt.so.1`
- PKG_CONFIG_PATH: `/src/ModSecurity-conector-cache/prefix/expat/lib/pkgconfig`

### NGINX
- Status: `present`
- Blocker: `-`
- Cache path: `/src/ModSecurity-conector-cache/archives/nginx`
- Build path: `/tmp/modsec-native-local-tools/nginx-build`
- MRTS_NATIVE_NGINX_BIN: `/tmp/modsec-native-local-tools/nginx-runtime/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/tmp/modsec-native-local-tools/nginx-runtime/nginx/modules`
- Module file: `/tmp/modsec-native-local-tools/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so`
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
