# Runtime Component Cache

Generated at: `2026-06-12T17:00:38Z`
Cache root: `/src/ModSecurity-conector-cache`

## Prepare Phases
- 1. validate safe paths
- 2. prepare git/source/archive cache recursively
- 3. prepare/build expat local prefix
- 4. prepare/build local Apache/httpd using local expat if needed
- 5. prepare/build local NGINX + ngx_http_modsecurity_module.so
- 6. prepare/build go-ftw from latest release tag
- 7. prepare/build albedo from latest release tag
- 8. write manifests/reports

## Apache httpd
- Status: `present`
- Blocker: `-`
- Source: `connector-local-build`
- Expected ref/version: `2.4.67`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/tmp/modsec-native-100003-debug/apache-build`
- apachectl/APACHECTL_BIN: `/tmp/modsec-native-100003-debug/apache-runtime/httpd/bin/apachectl-mrts`
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

## NGINX
- Status: `present`
- Blocker: `-`
- Source: `connector-local-build`
- Expected ref/version: `latest`
- Cache path: `/src/ModSecurity-conector-cache/archives/nginx`
- Build path: `/tmp/modsec-native-100003-debug/nginx-build`
- MRTS_NATIVE_NGINX_BIN: `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/modules`
- Module file: `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

## Expat
- Status: `present`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_1`
- Actual head: `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19`
- Prefix: `/src/ModSecurity-conector-cache/prefix/expat`
- expat.h: `/src/ModSecurity-conector-cache/prefix/expat/include/expat.h`
- lib dir: `/src/ModSecurity-conector-cache/prefix/expat/lib`
- Recursive submodules: `-`

## go-ftw / albedo
| Dependency | Status | Env override | Source | Release tag | Head | Binary | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `/src/ModSecurity-conector-cache/bin/go-ftw` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `/src/ModSecurity-conector-cache/bin/albedo` | `-` | - | - |

## Git Components
| Name | Status | Ref | Head | Submodules | fsck | Blocker |
|---|---|---|---|---:|---|---|
| modsecurity-v3 | present | `v3/master` | `2fd49292d751fc383b8faf7da6a8d480904774d0` | 8 | PASS | - |
| coreruleset | present | `v4.26.0` | `955649c1221633cc3ea63674904e94fbc5fb6356` | 0 | PASS | - |
| go-ftw | present | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | 0 | PASS | - |
| albedo | present | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | 0 | PASS | - |
| expat | present | `R_2_8_1` | `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19` | 0 | PASS | - |

## Archives
| Name | Status | Checksum | Path | Blocker |
|---|---|---|---|---|
| httpd | present | PASS | `/src/ModSecurity-conector-cache/archives/apache/httpd-2.4.67.tar.bz2` | - |
| apr | present | PASS | `/src/ModSecurity-conector-cache/archives/apache/apr-1.7.6.tar.bz2` | - |
| apr-util | present | PASS | `/src/ModSecurity-conector-cache/archives/apache/apr-util-1.6.3.tar.bz2` | - |
| pcre2 | present | checksum_unavailable | `/src/ModSecurity-conector-cache/archives/apache/pcre2-10.47.tar.bz2` | - |
| haproxy | present | PASS | `/src/ModSecurity-conector-cache/archives/haproxy/haproxy-3.2.19.tar.gz` | - |
| nginx | present | checksum_unavailable | `/src/ModSecurity-conector-cache/archives/nginx/release-1.31.1.tar.gz` | - |

## Local Dependencies
| Name | Status | Env | Path | Access |
|---|---|---|---|---|
| go-ftw | present | `GO_FTW_BIN` | `/src/ModSecurity-conector-cache/bin/go-ftw` | read-only/executable |
| albedo | present | `ALBEDO_BIN` | `/src/ModSecurity-conector-cache/bin/albedo` | read-only/executable |
| expat | present | `EXPAT_PREFIX` | `/src/ModSecurity-conector-cache/prefix/expat` | local-prefix/read-only |
| apachectl | present | `APACHECTL_BIN` | `/tmp/modsec-native-100003-debug/apache-runtime/httpd/bin/apachectl-mrts` | local-wrapper/read-only-executable |
| nginx | present | `MRTS_NATIVE_NGINX_BIN` | `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/sbin/nginx` | local-build/read-only-executable |
| ngx_http_modsecurity_module.so | present | `MRTS_NATIVE_NGINX_MODULE_DIR` | `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so` | local-build/module-reference |

## Guardrails
- System paths are not used for runtime component writes.
- Runtime writes are constrained to cache/build/runtime roots.
- Native Apache and NGINX use local prepared components when env overrides are absent.
- go-ftw, albedo, and expat are prepared from explicit release-tag sources.
- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `present`
- Blocker: `-`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/tmp/modsec-native-100003-debug/apache-build`
- apachectl/APACHECTL_BIN: `/tmp/modsec-native-100003-debug/apache-runtime/httpd/bin/apachectl-mrts`
- Module file: `/tmp/modsec-native-100003-debug/apache-build/output/apache/mod_security3.so`
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
- Status: `present`
- Blocker: `-`
- Cache path: `/src/ModSecurity-conector-cache/archives/nginx`
- Build path: `/tmp/modsec-native-100003-debug/nginx-build`
- MRTS_NATIVE_NGINX_BIN: `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/modules`
- Module file: `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so`
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

### Apache 100003-1
- Status: `fail`
- Target: `apache2_ubuntu`
- Run counts: attempted `13`, passed `12`, failed cases `100003-1`
- Diagnosis: Apache/httpd started and reached go-ftw; expected phase 4 rule id 100003 was not logged.
- Classification: `native_modsecurity_semantics`; secondary `phase4_native_limitation`; unresolved `False`
- Classification reason: Rule 100003 is loaded and its target/operator match the same POST query argument in phases 1-3, but no phase:4 ARGS/ARGS_GET rule is logged in either native target.
- Generated YAML: `/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/ftw/100003_MRTS_002_ARGS_A-GET.yaml`
- Generated rule file: `/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_002_ARGS_A-GET.conf`
- Source definition: `config_tests/CONF_002_TARGET_ARGS_A-GET.yaml`
- Generated rule line: `SecRule ARGS "@contains attack" "id:100003, phase:4, deny, t:none, log"`
- Rule 100003: variable `ARGS`, phase `4`, operator `@contains attack`, transform `t:none`
- Request: `POST /?foo=attack HTTP/1.1` on port `19080`; body `none`
- Generated test headers: `User-Agent: OWASP MRTS test agent, Host: localhost, Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5`
- Log matching: marker header `X-MRTS-TEST`, target log `/tmp/modsec-native-100003-debug/mrts-native/apache2_ubuntu/stage/infra/log/error.log`
- Expected status/result: `not specified in FTW YAML` / `log id 100003`
- Actual status/result: `HTTP 200 observed in Apache access log` / `missing expected log id 100003`
- Actual logged IDs: `10002, 100028, 100029, 100030, 100000, 100032, 100001, 100016, 100033, 100002, 100017, 100034`
- Phase 4 evidence: match seen `False`, peer IDs in case window `-`, peer IDs anywhere `-`
- Request collection evidence: POST query as ARGS `True`, as ARGS_GET `True`
- Excluded causes: response-body target `False`, operator case/transform issue `False` / `False`, skip/ctl/chain interference `False`, go-ftw log matching issue `False`
- Parse/phase warnings: `0`
- Loaded MRTS includes checked: `Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_001_INIT.conf", Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_002_ARGS_A-GET.conf", Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_003_ARGS_COMBINED_SIZE.conf", Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_004_ARGS_GET.conf"`
- Module loaded: `True` from `/tmp/modsec-native-100003-debug/apache-build/output/apache/mod_security3.so`
- mrts.load included: `True`
- Request reached Apache/ModSecurity/Albedo: `True` / `True` / `True`
- Audit/debug evidence: audit log `empty`, error log `/tmp/modsec-native-100003-debug/mrts-native/apache2_ubuntu/stage/infra/log/error.log`, go-ftw log `/tmp/modsec-native-100003-debug/mrts-native/apache2_ubuntu/run.log`
- Single-case rerun: attempted `1`, failed cases `100003-1`, exit `1`, log `/tmp/modsec-native-100003-debug/single-case/apache2_ubuntu-single.log`
- Why not logged: Native ModSecurity reached the request and logged ARGS/ARGS_GET matches through phase 3; the phase:4 request-collection rule did not emit a ModSecurity log entry. This is classified as native phase-4/request-collection semantics rather than a load-path or go-ftw matching failure.
- Action: No MRTS definition/result rewrite was made; keep 100003-1 as a native phase-4/request-collection limitation until native phase 4 semantics change.

### NGINX 100003-1
- Status: `fail`
- Target: `nginx-pr24`
- Run counts: attempted `13`, passed `12`, failed cases `100003-1`
- Diagnosis: go-ftw expected phase 4 rule id 100003, but NGINX/ModSecurity logged only earlier phase matches for the request.
- Classification: `native_modsecurity_semantics`; secondary `phase4_native_limitation`; unresolved `False`
- Classification reason: Rule 100003 is loaded and its target/operator match the same POST query argument in phases 1-3, but no phase:4 ARGS/ARGS_GET rule is logged in either native target.
- Generated YAML: `/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/ftw/100003_MRTS_002_ARGS_A-GET.yaml`
- Generated rule file: `/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_002_ARGS_A-GET.conf`
- Source definition: `config_tests/CONF_002_TARGET_ARGS_A-GET.yaml`
- Generated rule line: `SecRule ARGS "@contains attack" "id:100003, phase:4, deny, t:none, log"`
- Rule 100003: variable `ARGS`, phase `4`, operator `@contains attack`, transform `t:none`
- Request: `POST /?foo=attack HTTP/1.1` on port `19081`; body `none`
- Generated test headers: `User-Agent: OWASP MRTS test agent, Host: localhost, Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5`
- Log matching: marker header `X-MRTS-TEST`, target log `/tmp/modsec-native-100003-debug/mrts-native/nginx-pr24/stage/infra/log/error.log`
- Expected status/result: `not specified in FTW YAML` / `log id 100003`
- Actual status/result: `not printed by go-ftw; backend request was observed` / `missing expected log id 100003`
- Actual logged IDs: `10002, 100028, 100029, 100030, 100000, 100032, 100001, 100016, 100033, 100002, 100017, 100034`
- Phase 4 evidence: match seen `False`, peer IDs in case window `-`, peer IDs anywhere `-`
- Request collection evidence: POST query as ARGS `True`, as ARGS_GET `True`
- Excluded causes: response-body target `False`, operator case/transform issue `False` / `False`, skip/ctl/chain interference `False`, go-ftw log matching issue `False`
- Parse/phase warnings: `0`
- Loaded MRTS includes checked: `Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_001_INIT.conf", Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_002_ARGS_A-GET.conf", Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_003_ARGS_COMBINED_SIZE.conf", Include "/tmp/modsec-native-100003-debug/mrts/upstream-config-tests/rules/MRTS_004_ARGS_GET.conf"`
- Module loaded: `True` from `/tmp/modsec-native-100003-debug/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so`
- mrts.load included: `True`
- Request reached NGINX/ModSecurity/Albedo: `True` / `True` / `True`
- Audit/debug evidence: audit log `empty`, error log `/tmp/modsec-native-100003-debug/mrts-native/nginx-pr24/stage/infra/log/error.log`, go-ftw log `/tmp/modsec-native-100003-debug/mrts-native/nginx-pr24/run.log`
- Single-case rerun: attempted `1`, failed cases `100003-1`, exit `1`, log `/tmp/modsec-native-100003-debug/single-case/nginx-pr24-single.log`
- Why not logged: Native ModSecurity reached the request and logged ARGS/ARGS_GET matches through phase 3; the phase:4 request-collection rule did not emit a ModSecurity log entry. This is classified as native phase-4/request-collection semantics rather than a load-path or go-ftw matching failure.
- Action: No MRTS definition/result rewrite was made; keep 100003-1 as a native phase-4/request-collection limitation until native phase 4 semantics change.
<!-- runtime-diagnostics:end -->
