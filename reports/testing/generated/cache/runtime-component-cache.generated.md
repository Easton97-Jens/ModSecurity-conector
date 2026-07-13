> Generated file - do not edit manually.
>
> Generated at: `2026-07-13T18:27:24Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/provisioning/components/prepare-runtime-components.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `9ff693c3f85b123d549342ccb5e3b9485fd89638`
> Framework SHA: `77b4e89d230a23a75bff4d871d87345d55fcad28`
> Input status: `complete`

# Runtime Component Cache

**Language:** English | [Deutsch](runtime-component-cache.generated.de.md)

- Cache root: `<verified-run-root>/cache-v2/shared`
- Build root: `<verified-run-root>/build`
- Generated at: `2026-07-13T18:27:24Z`
- Local cache binaries and source trees are not committed; this report records provenance.

| Component | Status | Build ID / Ref | Path |
|---|---|---|---|
| modsecurity | reused | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` |
| apache_httpd | reused | `240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0` | `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/build` |
| nginx | reused | `6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7` | `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/build` |
| haproxy | reused | `553adfcb804bc331ffcfe60106b951a930c0254d63e522ec7594485a7b55d93e` | `<verified-run-root>/cache-v2/shared/builds/connectors/haproxy/553adfcb804bc331ffcfe60106b951a930c0254d63e522ec7594485a7b55d93e` |
| go_ftw | present | `v2.4.0` | `<verified-run-root>/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` |
| albedo | present | `v0.3.0` | `<verified-run-root>/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` |
| expat | present | `b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a` | `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/cache-v2/shared/manifest.json` | `43d434ce2d26a6e0a2211eb88f19bdd326cebeb3565b48982b4a5a75c0287308` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/cache-v2/shared/manifest.json` | present | input file available |

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `reused`
- Blocker: `-`
- Cache path: `<verified-run-root>/cache-v2/shared/archives/apache`
- Build path: `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/build`
- apachectl/APACHECTL_BIN: `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/httpd/bin/apachectl-mrts`
- Module file: `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/build/output/apache/mod_security3.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `APACHECTL_BIN`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_2`
- CPPFLAGS: `-I<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/include`
- LDFLAGS: `-L<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/lib/pkgconfig`
- crypt.h status: `present`
- crypt.h path: `/usr/include/crypt.h`
- libcrypt status: `present`
- libcrypt paths: `/usr/lib/x86_64-linux-gnu/libcrypt.so, /lib/x86_64-linux-gnu/libcrypt.so, /usr/lib/x86_64-linux-gnu/libcrypt.so.1, /lib/x86_64-linux-gnu/libcrypt.so.1`
- crypt link mode: `compiler:-lcrypt`

### NGINX
- Status: `reused`
- Blocker: `-`
- Cache path: `<verified-run-root>/cache-v2/shared/archives/nginx`
- Build path: `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/build`
- MRTS_NATIVE_NGINX_BIN: `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/nginx/modules`
- Module file: `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

### Expat
- Status: `present`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_2`
- Actual head: `c61098da494eea1cbd091118118dcee417faacea`
- Prefix: `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix`
- expat.h: `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/include/expat.h`
- lib dir: `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/lib`
- Recursive submodules: `-`

### go-ftw / albedo
| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | present | `<verified-run-root>/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | present | `<verified-run-root>/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `-` | - | - |
<!-- runtime-components:end -->

<!-- runtime-build-cache:start -->
## Runtime Build Cache
- Shared ModSecurity status: `reused`
- Shared ModSecurity source ref/SHA: `v3/master` / `7ea9fefbe0ba409d8733b4d682c8c4c059cd028d`
- Shared ModSecurity build ID: `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720`
- Shared ModSecurity prefix: `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720`
- Build reuse summary: rebuilt `0`, reused `3`, blocked `0`, saved rebuilds estimate `3`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | reused | `240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0` | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | - |
| nginx | reused | `6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7` | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | - |
| haproxy | reused | `553adfcb804bc331ffcfe60106b951a930c0254d63e522ec7594485a7b55d93e` | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | - |
<!-- runtime-build-cache:end -->

<!-- runtime-diagnostics:start -->
## Native Runtime Diagnostics

- No generated native runtime diagnostics were detected.
<!-- runtime-diagnostics:end -->
