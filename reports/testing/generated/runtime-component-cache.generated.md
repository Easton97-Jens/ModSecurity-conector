# Runtime Component Cache

Generated at: `2026-06-10T08:44:44Z`
Cache root: `/src/ModSecurity-conector-cache`

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
| go-ftw | missing | `GO_FTW_BIN` | `go-ftw` | read-only/executable |
| albedo | missing | `ALBEDO_BIN` | `albedo` | read-only/executable |
| apachectl | missing | `APACHECTL_BIN` | `apachectl` | read-only/executable |
| nginx | missing | `MRTS_NATIVE_NGINX_BIN` | `nginx` | read-only/executable |
| ngx_http_modsecurity_module.so | missing | `MRTS_NATIVE_NGINX_MODULE_DIR` | `ngx_http_modsecurity_module.so` | read-only/module-reference |

## Guardrails
- System paths are read-only dependencies.
- Runtime writes are constrained to cache/build/runtime roots.
- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.
