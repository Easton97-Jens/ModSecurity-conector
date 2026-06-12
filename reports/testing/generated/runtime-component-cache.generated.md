# Runtime Component Cache

Generated at: `2026-06-12T13:52:55Z`
Cache root: `/src/ModSecurity-conector-cache`

## Prepare Phases
- 1. validate safe paths
- 2. prepare git/source/archive cache recursively
- 3. prepare/build local ModSecurity if required
- 4. prepare/build local Apache/httpd for Apache connector/native
- 5. prepare/build local NGINX + ngx_http_modsecurity_module.so for NGINX connector/native
- 6. inventory go-ftw/albedo
- 7. write manifests/reports

## Apache httpd
- Status: `blocked`
- Blocker: `missing_expat_headers`
- Source: `connector-local-build`
- Expected ref/version: `2.4.67`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/tmp/modsec-native-local-build/apache-build`
- apachectl/APACHECTL_BIN: `/tmp/modsec-native-local-build/mrts-native/apache2_ubuntu/bin/apachectl`
- Missing file: `expat.h`
- Build component: `apache_httpd_source_build`
- Env variable to set: `CPPFLAGS/LDFLAGS`

## NGINX
- Status: `present`
- Blocker: `-`
- Source: `connector-local-build`
- Expected ref/version: `latest`
- Cache path: `/src/ModSecurity-conector-cache/archives/nginx`
- Build path: `/tmp/modsec-native-local-build/nginx-build`
- MRTS_NATIVE_NGINX_BIN: `/tmp/modsec-native-local-build/nginx-runtime/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/tmp/modsec-native-local-build/nginx-runtime/nginx/modules`
- Module file: `/tmp/modsec-native-local-build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

## go-ftw / albedo
| Dependency | Status | Env override | Known source | Known ref | Can build locally | Blocker |
|---|---|---|---|---|---|---|
| go-ftw | blocked | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `-` | no | missing_go_ftw_source_ref |
| albedo | blocked | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `-` | no | missing_albedo_source_ref |

## Git Components
| Name | Status | Ref | Head | Submodules | fsck | Blocker |
|---|---|---|---|---:|---|---|
| modsecurity-v3 | present | `v3/master` | `2fd49292d751fc383b8faf7da6a8d480904774d0` | 8 | SKIPPED_CACHED_PASS | - |
| coreruleset | present | `v4.26.0` | `955649c1221633cc3ea63674904e94fbc5fb6356` | 0 | SKIPPED_CACHED_PASS | - |

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
| go-ftw | missing | `GO_FTW_BIN` | `-` | read-only/executable |
| albedo | missing | `ALBEDO_BIN` | `-` | read-only/executable |
| apachectl | missing | `APACHECTL_BIN` | `/tmp/modsec-native-local-build/mrts-native/apache2_ubuntu/bin/apachectl` | local-wrapper/read-only-executable |
| nginx | present | `MRTS_NATIVE_NGINX_BIN` | `/tmp/modsec-native-local-build/nginx-runtime/nginx/sbin/nginx` | local-build/read-only-executable |
| ngx_http_modsecurity_module.so | present | `MRTS_NATIVE_NGINX_MODULE_DIR` | `/tmp/modsec-native-local-build/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so` | local-build/module-reference |

## Guardrails
- System paths are not used for runtime component writes.
- Runtime writes are constrained to cache/build/runtime roots.
- Native Apache and NGINX use local prepared components when env overrides are absent.
- go-ftw and albedo are inventoried only; no source/ref is guessed.
- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.
