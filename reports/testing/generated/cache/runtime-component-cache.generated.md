> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T04:53:27Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/prepare-runtime-components.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `complete`

# Runtime Component Cache

Generated at: `2026-06-16T04:53:27Z`
Cache root: `/root/.local/state/ModSecurity-conector-build/component-cache`

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
- Build ID: `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Prefix: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Include dir: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/include`
- Lib dir: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/lib`

## Apache httpd
- Status: `reused`
- Blocker: `-`
- Connector build ID: `70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22`
- Uses ModSecurity build ID: `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Source: `connector-local-build`
- Expected ref/version: `2.4.67`
- Cache path: `/root/.local/state/ModSecurity-conector-build/component-cache/archives/apache`
- Build path: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/build`
- apachectl/APACHECTL_BIN: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/apachectl-mrts`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `APACHECTL_BIN`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_1`
- CPPFLAGS: `-I/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/include`
- LDFLAGS: `-L/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/lib/pkgconfig`
- crypt.h status: `present`
- crypt.h path: `/usr/include/crypt.h`
- libcrypt status: `present`
- libcrypt paths: `/usr/lib/x86_64-linux-gnu/libcrypt.so, /lib/x86_64-linux-gnu/libcrypt.so, /usr/lib/x86_64-linux-gnu/libcrypt.so.1, /lib/x86_64-linux-gnu/libcrypt.so.1`
- crypt link mode: `compiler:-lcrypt`

## NGINX
- Status: `reused`
- Blocker: `-`
- Connector build ID: `b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66`
- Uses ModSecurity build ID: `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Source: `connector-local-build`
- Expected ref/version: `latest`
- Cache path: `/root/.local/state/ModSecurity-conector-build/component-cache/archives/nginx`
- Build path: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/build`
- MRTS_NATIVE_NGINX_BIN: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules`
- Module file: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

## HAProxy
- Status: `reused`
- Blocker: `-`
- Connector build ID: `287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44`
- Uses ModSecurity build ID: `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- HAPROXY_BIN: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-runtime/haproxy/sbin/haproxy`
- SPOA_RUNTIME_BIN: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-spoa-runtime/haproxy-modsecurity-spoa`
- MODSECURITY_BINDING_DIR: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-modsecurity-binding`

## Expat
- Status: `present`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_1`
- Actual head: `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19`
- Prefix: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat`
- expat.h: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/include/expat.h`
- lib dir: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/lib`
- Recursive submodules: `-`

## go-ftw / albedo
| Dependency | Status | Env override | Source | Release tag | Head | Binary | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/go-ftw` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/albedo` | `-` | - | - |

## Git Components
| Name | Status | Ref | Head | Submodules | fsck | Blocker |
|---|---|---|---|---:|---|---|
| modsecurity-v3 | present | `v3/master` | `2fd49292d751fc383b8faf7da6a8d480904774d0` | 8 | SKIPPED_CACHED_PASS | - |
| coreruleset | present | `v4.26.0` | `955649c1221633cc3ea63674904e94fbc5fb6356` | 0 | SKIPPED_CACHED_PASS | - |
| go-ftw | present | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | 0 | PASS | - |
| albedo | present | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | 0 | SKIPPED_CACHED_PASS | - |
| expat | present | `R_2_8_1` | `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19` | 0 | SKIPPED_CACHED_PASS | - |

## Archives
| Name | Status | Checksum | Path | Blocker |
|---|---|---|---|---|
| httpd | present | PASS | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/apache/httpd-2.4.67.tar.bz2` | - |
| apr | present | PASS | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/apache/apr-1.7.6.tar.bz2` | - |
| apr-util | present | PASS | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/apache/apr-util-1.6.3.tar.bz2` | - |
| pcre2 | present | checksum_unavailable | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/apache/pcre2-10.47.tar.bz2` | - |
| haproxy | present | PASS | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/haproxy/haproxy-3.2.19.tar.gz` | - |
| nginx | present | checksum_unavailable | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/nginx/release-1.31.1.tar.gz` | - |

## Local Dependencies
| Name | Status | Env | Path | Access |
|---|---|---|---|---|
| go-ftw | present | `GO_FTW_BIN` | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/go-ftw` | read-only/executable |
| albedo | present | `ALBEDO_BIN` | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/albedo` | read-only/executable |
| expat | present | `EXPAT_PREFIX` | `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat` | local-prefix/read-only |
| libmodsecurity | present | `MODSECURITY_LIB_DIR` | `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/lib/libmodsecurity.so` | shared-local-prefix/read-only |
| apachectl | present | `APACHECTL_BIN` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/apachectl-mrts` | local-wrapper/read-only-executable |
| nginx | present | `MRTS_NATIVE_NGINX_BIN` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/sbin/nginx` | local-build/read-only-executable |
| ngx_http_modsecurity_module.so | present | `MRTS_NATIVE_NGINX_MODULE_DIR` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules/ngx_http_modsecurity_module.so` | local-build/module-reference |
| haproxy | present | `HAPROXY_BIN` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-runtime/haproxy/sbin/haproxy` | local-build/read-only-executable |
| haproxy-modsecurity-spoa | present | `SPOA_RUNTIME_BIN` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | local-build/read-only-executable |

## Guardrails
- System paths are not used for runtime component writes.
- Runtime writes are constrained to cache/build/runtime roots.
- Native Apache and NGINX use local prepared components when env overrides are absent.
- go-ftw, albedo, and expat are prepared from explicit release-tag sources.
- `RUNTIME_COMPONENT_STRICT_VERIFY=1` forces full git fsck.

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/root/.local/state/ModSecurity-conector-build/component-cache/manifest.json` | `b137c5fb283d3fc07d2c8c35d5708735019ddc984bc66a58ea05e81cef18fd52` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/component-cache/manifest.json` | present | input file available |

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `reused`
- Blocker: `-`
- Cache path: `/root/.local/state/ModSecurity-conector-build/component-cache/archives/apache`
- Build path: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/build`
- apachectl/APACHECTL_BIN: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/apachectl-mrts`
- Module file: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/build/output/apache/mod_security3.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `APACHECTL_BIN`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_1`
- CPPFLAGS: `-I/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/include`
- LDFLAGS: `-L/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/lib/pkgconfig`
- crypt.h status: `present`
- crypt.h path: `/usr/include/crypt.h`
- libcrypt status: `present`
- libcrypt paths: `/usr/lib/x86_64-linux-gnu/libcrypt.so, /lib/x86_64-linux-gnu/libcrypt.so, /usr/lib/x86_64-linux-gnu/libcrypt.so.1, /lib/x86_64-linux-gnu/libcrypt.so.1`
- crypt link mode: `compiler:-lcrypt`

### NGINX
- Status: `reused`
- Blocker: `-`
- Cache path: `/root/.local/state/ModSecurity-conector-build/component-cache/archives/nginx`
- Build path: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/build`
- MRTS_NATIVE_NGINX_BIN: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules`
- Module file: `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

### Expat
- Status: `present`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_1`
- Actual head: `c7ffbf3879f6aef7a7b020ef84ddb4ee00222b19`
- Prefix: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat`
- expat.h: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/include/expat.h`
- lib dir: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/expat/lib`
- Recursive submodules: `-`

### go-ftw / albedo
| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/go-ftw` | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/albedo` | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `-` | - | - |
<!-- runtime-components:end -->

<!-- runtime-build-cache:start -->
## Runtime Build Cache
- Shared ModSecurity status: `reused`
- Shared ModSecurity source ref/SHA: `v3/master` / `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Shared ModSecurity build ID: `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Shared ModSecurity prefix: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Build reuse summary: rebuilt `0`, reused `3`, blocked `0`, saved rebuilds estimate `3`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | reused | `70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22` | `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a` | - |
| nginx | reused | `b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66` | `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a` | - |
| haproxy | reused | `287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44` | `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a` | - |
<!-- runtime-build-cache:end -->

<!-- runtime-diagnostics:start -->
## Native Runtime Diagnostics

- No generated native runtime diagnostics were detected.
<!-- runtime-diagnostics:end -->
