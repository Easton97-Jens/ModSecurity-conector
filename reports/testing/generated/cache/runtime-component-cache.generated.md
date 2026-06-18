> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T12:14:56Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/prepare-runtime-components.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
> Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
> Input status: `complete`

# Runtime Component Cache

Generated at: `2026-06-18T12:14:56Z`
Cache root: `/var/tmp/ModSecurity-conector-verified/component-cache`

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
- Build ID: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Prefix: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Include dir: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/include`
- Lib dir: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib`

## Apache httpd
- Status: `reused`
- Blocker: `-`
- Connector build ID: `898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67`
- Uses ModSecurity build ID: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Source: `connector-local-build`
- Expected ref/version: `2.4.67`
- Cache path: `/var/tmp/ModSecurity-conector-verified/component-cache/archives/apache`
- Build path: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build`
- apachectl/APACHECTL_BIN: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apachectl-mrts`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `APACHECTL_BIN`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_1`
- CPPFLAGS: `-I/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/include`
- LDFLAGS: `-L/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/lib/pkgconfig`
- crypt.h status: `present`
- crypt.h path: `/usr/include/crypt.h`
- libcrypt status: `present`
- libcrypt paths: `/usr/lib/x86_64-linux-gnu/libcrypt.so, /lib/x86_64-linux-gnu/libcrypt.so, /usr/lib/x86_64-linux-gnu/libcrypt.so.1, /lib/x86_64-linux-gnu/libcrypt.so.1`
- crypt link mode: `compiler:-lcrypt`

## NGINX
- Status: `reused`
- Blocker: `-`
- Connector build ID: `d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12`
- Uses ModSecurity build ID: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Source: `connector-local-build`
- Expected ref/version: `latest`
- Cache path: `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx`
- Build path: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/build`
- MRTS_NATIVE_NGINX_BIN: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules`
- Module file: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

## HAProxy
- Status: `reused`
- Blocker: `-`
- Connector build ID: `599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048`
- Uses ModSecurity build ID: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- HAPROXY_BIN: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-runtime/haproxy/sbin/haproxy`
- SPOA_RUNTIME_BIN: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-spoa-runtime/haproxy-modsecurity-spoa`
- MODSECURITY_BINDING_DIR: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-modsecurity-binding`

## Expat
- Status: `present`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_1`
- Actual head: `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19`
- Prefix: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat`
- expat.h: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/include/expat.h`
- lib dir: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/lib`
- Recursive submodules: `-`

## go-ftw / albedo
| Dependency | Status | Env override | Source | Release tag | Head | Binary | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/go-ftw` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/albedo` | `-` | - | - |

## Git Components
| Name | Status | Ref | Head | Submodules | fsck | Blocker |
|---|---|---|---|---:|---|---|
| modsecurity-v3 | present | `v3/master` | `2fd49292d751fc383b8faf7da6a8d480904774d0` | 8 | SKIPPED_CACHED_PASS | - |
| coreruleset | present | `v4.26.0` | `955649c1221633cc3ea63674904e94fbc5fb6356` | 0 | SKIPPED_CACHED_PASS | - |
| go-ftw | present | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | 0 | SKIPPED_CACHED_PASS | - |
| albedo | present | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | 0 | SKIPPED_CACHED_PASS | - |
| expat | present | `R_2_8_1` | `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19` | 0 | SKIPPED_CACHED_PASS | - |

## Archives
| Name | Status | Checksum | Path | Blocker |
|---|---|---|---|---|
| httpd | present | PASS | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/apache/httpd-2.4.67.tar.bz2` | - |
| apr | present | PASS | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/apache/apr-1.7.6.tar.bz2` | - |
| apr-util | present | PASS | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/apache/apr-util-1.6.3.tar.bz2` | - |
| pcre2 | present | checksum_unavailable | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/apache/pcre2-10.47.tar.bz2` | - |
| haproxy | present | PASS | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/haproxy/haproxy-3.2.19.tar.gz` | - |
| nginx | present | checksum_unavailable | `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx/release-1.31.2.tar.gz` | - |

## Local Dependencies
| Name | Status | Env | Path | Access |
|---|---|---|---|---|
| go-ftw | present | `GO_FTW_BIN` | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/go-ftw` | read-only/executable |
| albedo | present | `ALBEDO_BIN` | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/albedo` | read-only/executable |
| expat | present | `EXPAT_PREFIX` | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat` | local-prefix/read-only |
| libmodsecurity | present | `MODSECURITY_LIB_DIR` | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib/libmodsecurity.so` | shared-local-prefix/read-only |
| apachectl | present | `APACHECTL_BIN` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apachectl-mrts` | local-wrapper/read-only-executable |
| nginx | present | `MRTS_NATIVE_NGINX_BIN` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` | local-build/read-only-executable |
| ngx_http_modsecurity_module.so | present | `MRTS_NATIVE_NGINX_MODULE_DIR` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` | local-build/module-reference |
| haproxy | present | `HAPROXY_BIN` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-runtime/haproxy/sbin/haproxy` | local-build/read-only-executable |
| haproxy-modsecurity-spoa | present | `SPOA_RUNTIME_BIN` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | local-build/read-only-executable |

## Guardrails
- System paths are not used for runtime component writes.
- Runtime writes are constrained to cache/build/runtime roots.
- Native Apache and NGINX use local prepared components when env overrides are absent.
- go-ftw, albedo, and expat are prepared from explicit release-tag sources.
- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/component-cache/manifest.json` | `3904de5ba72723df9e99e34169abd8ba43423752dc66626f0e69c8d5bd6f7d6e` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/component-cache/manifest.json` | present | input file available |

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `reused`
- Blocker: `-`
- Cache path: `/var/tmp/ModSecurity-conector-verified/component-cache/archives/apache`
- Build path: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build`
- apachectl/APACHECTL_BIN: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apachectl-mrts`
- Module file: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build/output/apache/mod_security3.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `APACHECTL_BIN`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_1`
- CPPFLAGS: `-I/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/include`
- LDFLAGS: `-L/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/lib/pkgconfig`
- crypt.h status: `present`
- crypt.h path: `/usr/include/crypt.h`
- libcrypt status: `present`
- libcrypt paths: `/usr/lib/x86_64-linux-gnu/libcrypt.so, /lib/x86_64-linux-gnu/libcrypt.so, /usr/lib/x86_64-linux-gnu/libcrypt.so.1, /lib/x86_64-linux-gnu/libcrypt.so.1`
- crypt link mode: `compiler:-lcrypt`

### NGINX
- Status: `reused`
- Blocker: `-`
- Cache path: `/var/tmp/ModSecurity-conector-verified/component-cache/archives/nginx`
- Build path: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/build`
- MRTS_NATIVE_NGINX_BIN: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules`
- Module file: `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

### Expat
- Status: `present`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_1`
- Actual head: `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19`
- Prefix: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat`
- expat.h: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/include/expat.h`
- lib dir: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/expat/lib`
- Recursive submodules: `-`

### go-ftw / albedo
| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/go-ftw` | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `/var/tmp/ModSecurity-conector-verified/component-cache/bin/albedo` | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `-` | - | - |
<!-- runtime-components:end -->

<!-- runtime-build-cache:start -->
## Runtime Build Cache
- Shared ModSecurity status: `reused`
- Shared ModSecurity source ref/SHA: `v3/master` / `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Shared ModSecurity build ID: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Shared ModSecurity prefix: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Build reuse summary: rebuilt `0`, reused `3`, blocked `0`, saved rebuilds estimate `3`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | reused | `898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - |
| nginx | reused | `d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - |
| haproxy | reused | `599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - |
<!-- runtime-build-cache:end -->

<!-- runtime-diagnostics:start -->
## Native Runtime Diagnostics

- No generated native runtime diagnostics were detected.
<!-- runtime-diagnostics:end -->
