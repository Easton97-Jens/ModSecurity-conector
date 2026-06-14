# Runtime Component Cache

Generated at: `2026-06-12T17:55:50Z`
Cache root: `/src/ModSecurity-conector-cache`

## Prepare Phases
- 1. validate safe paths
- 2. prepare git/source/archive cache recursively
- 3. prepare/build expat local prefix
- 4. prepare/build shared ModSecurity v3 once per source/ref/build config
- 5. prepare/reuse connector builds keyed by connector inputs and ModSecurity build ID
- 6. prepare/build go-ftw from latest release tag
- 7. prepare/build albedo from latest release tag
- 8. write manifests/reports

## Shared ModSecurity
- Status: `reused`
- Blocker: `-`
- Source ref: `v3/master`
- Actual SHA: `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Build ID: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Prefix: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Include dir: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c/include`
- Lib dir: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c/lib`

## Apache httpd
- Status: `reused`
- Blocker: `-`
- Connector build ID: `030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72`
- Uses ModSecurity build ID: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Source: `connector-local-build`
- Expected ref/version: `2.4.67`
- Cache path: `/src/ModSecurity-conector-cache/archives/apache`
- Build path: `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/build`
- apachectl/APACHECTL_BIN: `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/httpd/bin/apachectl-mrts`
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
- Status: `reused`
- Blocker: `-`
- Connector build ID: `24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71`
- Uses ModSecurity build ID: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Source: `connector-local-build`
- Expected ref/version: `latest`
- Cache path: `/src/ModSecurity-conector-cache/archives/nginx`
- Build path: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/build`
- MRTS_NATIVE_NGINX_BIN: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules`
- Module file: `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

## HAProxy
- Status: `reused`
- Blocker: `-`
- Connector build ID: `8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939`
- Uses ModSecurity build ID: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- HAPROXY_BIN: `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-runtime/haproxy/sbin/haproxy`
- SPOA_RUNTIME_BIN: `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-spoa-runtime/haproxy-modsecurity-spoa`
- MODSECURITY_BINDING_DIR: `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-modsecurity-binding`

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
| libmodsecurity | present | `MODSECURITY_LIB_DIR` | `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c/lib/libmodsecurity.so` | shared-local-prefix/read-only |
| apachectl | present | `APACHECTL_BIN` | `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/httpd/bin/apachectl-mrts` | local-wrapper/read-only-executable |
| nginx | present | `MRTS_NATIVE_NGINX_BIN` | `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/sbin/nginx` | local-build/read-only-executable |
| ngx_http_modsecurity_module.so | present | `MRTS_NATIVE_NGINX_MODULE_DIR` | `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules/ngx_http_modsecurity_module.so` | local-build/module-reference |
| haproxy | present | `HAPROXY_BIN` | `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-runtime/haproxy/sbin/haproxy` | local-build/read-only-executable |
| haproxy-modsecurity-spoa | present | `SPOA_RUNTIME_BIN` | `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | local-build/read-only-executable |

## Guardrails
- System paths are not used for runtime component writes.
- Runtime writes are constrained to cache/build/runtime roots.
- Native Apache and NGINX use local prepared components when env overrides are absent.
- go-ftw, albedo, and expat are prepared from explicit release-tag sources.
- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.

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

<!-- runtime-diagnostics:start -->
## Native Runtime Diagnostics

- No generated native runtime diagnostics were detected.
<!-- runtime-diagnostics:end -->
