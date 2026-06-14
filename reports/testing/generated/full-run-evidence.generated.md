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
- Report generated at: `2026-06-13T11:32:41Z`
- Native MRTS evidence is separate from connector runtime matrix evidence.

| Target | Status | Exit code | Attempted | PASS | FAIL | BLOCKED | Reason | Run log | Summary |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| apache2_ubuntu | FAIL | 1 | 13 | 12 | 1 | 0 | native MRTS go-ftw run failed | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json` |
| nginx-pr24 | FAIL | 1 | 13 | 12 | 1 | 0 | native MRTS go-ftw run failed | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `$MRTS_NATIVE_ROOT/nginx-pr24/job.json` |

<!-- mrts-native-infrastructure-evidence:start -->
## MRTS Native Infrastructure Evidence

- Apache native: `reports/testing/generated/mrts-native-apache.generated.md`
- NGINX PR24 native: `reports/testing/generated/mrts-native-nginx.generated.md`
- Native summary: `reports/testing/generated/mrts-native-summary.generated.md`
- Combined native report: `reports/testing/generated/mrts-native-full.generated.md`

These native MRTS reports are separate from connector full-matrix evidence.
<!-- mrts-native-infrastructure-evidence:end -->

## External Blockers
- apache: `expat.h` missing; Provide local CPPFLAGS/LDFLAGS for expat headers/libs or install the matching system development package outside this run.
- haproxy: `crypt.h` missing; Provide local CPPFLAGS/LDFLAGS for crypt headers/libs or install the matching system development package outside this run.

<!-- no-mrts-intervention-nomatch-analysis:start -->
## No-MRTS Intervention No-Match Analysis
- Report: `reports/testing/generated/no-mrts-intervention-nomatch-analysis.generated.md`
- Scope: 105 no-MRTS expected 403 / actual 200 rows where the rule is loaded but no match evidence is visible.
- This is analysis-only evidence; Expected statuses and runtime PASS/FAIL values remain unchanged.
<!-- no-mrts-intervention-nomatch-analysis:end -->

<!-- remaining-failure-analysis:start -->
## Remaining Failure Analysis
- Remaining failure analysis: `reports/testing/generated/remaining-failure-analysis.generated.md`
- Next fix plan: `reports/testing/generated/next-fix-plan.generated.md`
- Phase 4 hard-abort capability: `reports/testing/generated/phase4-hard-abort-capability.generated.md`
- Nolog audit evidence: `reports/testing/generated/nolog-audit-evidence.generated.md`
- Response header hook analysis: `reports/testing/generated/response-header-hook-analysis.generated.md`
- These reports analyze connector Full-Matrix leftovers and keep Native MRTS evidence separate.
<!-- remaining-failure-analysis:end -->

<!-- phase4-hard-abort-capability:start -->
## Phase 4 Hard Abort Capability
- Report: `reports/testing/generated/phase4-hard-abort-capability.generated.md`
- Hard-abort evidence rows: **2**
- Full-delivery-without-abort rows: **842**
- The report keeps Expected status and runtime PASS/FAIL unchanged while adding hard-abort classifications.
<!-- phase4-hard-abort-capability:end -->

<!-- nolog-audit-evidence:start -->
## Nolog Audit Evidence Analysis
- Nolog audit evidence: `reports/testing/generated/nolog-audit-evidence.generated.md`
- Case `v3_action_nolog_pass_no_audit` is classified as `nolog_expected_no_audit` when rule 3326 is absent from runtime logs.
<!-- nolog-audit-evidence:end -->

<!-- response-header-hook-analysis:start -->
## Response Header Hook Analysis
- Response header hook analysis: `reports/testing/generated/response-header-hook-analysis.generated.md`
- The former monolithic `response_header_hook` cluster is split into backend header setup, multi-value header, and MRTS DetectionOnly overlay buckets.
<!-- response-header-hook-analysis:end -->

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
- Status: `reused`
- Blocker: `-`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/src/ModSecurity-conector-cache/builds/connectors/apache/58c954452223f16d5838aa48a8e7210e020be124368f3cb24d299287387f315d/build`
- apachectl/APACHECTL_BIN: `/src/ModSecurity-conector-cache/builds/connectors/apache/58c954452223f16d5838aa48a8e7210e020be124368f3cb24d299287387f315d/httpd/bin/apachectl-mrts`
- Module file: `/src/ModSecurity-conector-cache/builds/connectors/apache/58c954452223f16d5838aa48a8e7210e020be124368f3cb24d299287387f315d/build/output/apache/mod_security3.so`
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
- Build path: `/src/ModSecurity-conector-cache/builds/connectors/nginx/60761dd3e66ea96c75c56558a47c548c4f42284f90bffed507b63d21ecfd57d8/build`
- MRTS_NATIVE_NGINX_BIN: `/src/ModSecurity-conector-cache/builds/connectors/nginx/60761dd3e66ea96c75c56558a47c548c4f42284f90bffed507b63d21ecfd57d8/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/src/ModSecurity-conector-cache/builds/connectors/nginx/60761dd3e66ea96c75c56558a47c548c4f42284f90bffed507b63d21ecfd57d8/nginx/modules`
- Module file: `/src/ModSecurity-conector-cache/builds/connectors/nginx/60761dd3e66ea96c75c56558a47c548c4f42284f90bffed507b63d21ecfd57d8/nginx/modules/ngx_http_modsecurity_module.so`
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

<!-- post-libcrypt-native:start -->
## Post-libcrypt Native Rerun
- Scope: requested native rerun after external `libcrypt-dev` availability; the earlier full-matrix sections in this file remain historical evidence from their original generation time.
- Command: `FRAMEWORK_ROOT=/root/git/ModSecurity-test-Framework BUILD_ROOT=/tmp/modsec-native-after-libcrypt MRTS_NATIVE_TARGETS="apache2_ubuntu nginx-pr24" CONNECTOR_COMPONENT_CACHE=/src/ModSecurity-conector-cache PYTHONDONTWRITEBYTECODE=1 make mrts-native-full-run`
- BUILD_ROOT: `/src/ModSecurity-conector-cache/builds/connectors/apache/58c954452223f16d5838aa48a8e7210e020be124368f3cb24d299287387f315d`
- Apache wrapper: `/src/ModSecurity-conector-cache/builds/connectors/apache/58c954452223f16d5838aa48a8e7210e020be124368f3cb24d299287387f315d/httpd/bin/apachectl-mrts`
- Apache module: `/src/ModSecurity-conector-cache/builds/connectors/apache/58c954452223f16d5838aa48a8e7210e020be124368f3cb24d299287387f315d/build/output/apache/mod_security3.so`
- Apache native result: `-`; attempted `-`, passed `-`, failed cases `-`
- NGINX binary: `/src/ModSecurity-conector-cache/builds/connectors/nginx/60761dd3e66ea96c75c56558a47c548c4f42284f90bffed507b63d21ecfd57d8/nginx/sbin/nginx`
- NGINX module: `/src/ModSecurity-conector-cache/builds/connectors/nginx/60761dd3e66ea96c75c56558a47c548c4f42284f90bffed507b63d21ecfd57d8/nginx/modules/ngx_http_modsecurity_module.so`
- NGINX native result: `-`; attempted `-`, passed `-`, failed cases `-`
<!-- post-libcrypt-native:end -->

<!-- runtime-build-cache:start -->
## Runtime Build Cache
- Shared ModSecurity status: `reused`
- Shared ModSecurity source ref/SHA: `v3/master` / `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Shared ModSecurity build ID: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Shared ModSecurity prefix: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Build reuse summary: rebuilt `0`, reused `3`, blocked `0`, saved rebuilds estimate `3`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | reused | `58c954452223f16d5838aa48a8e7210e020be124368f3cb24d299287387f315d` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - |
| nginx | reused | `60761dd3e66ea96c75c56558a47c548c4f42284f90bffed507b63d21ecfd57d8` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - |
| haproxy | reused | `51072bb48ca39c69d26183d95707220277293c25f13852b0309cd79bc2038f8d` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - |
<!-- runtime-build-cache:end -->
