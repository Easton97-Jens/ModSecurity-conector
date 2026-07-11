> Generated file - do not edit manually.
>
> Generated at: `2026-07-11T17:55:31Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/prepare-runtime-components.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `6bfdc66329fc68531b3f358cab25ef91b3d9a2a9`
> Framework SHA: `9415da97a6cbac472bec3c3e1343b636a51c267b`
> Input status: `complete`

# Runtime Component Cache

**Language:** English | [Deutsch](runtime-component-cache.generated.de.md)

- Cache root: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared`
- Build root: `/var/tmp/ModSecurity-conector-verified/build`
- Generated at: `2026-07-11T17:55:31Z`
- Local cache binaries and source trees are not committed; this report records provenance.

| Component | Status | Build ID / Ref | Path |
|---|---|---|---|
| modsecurity | built | `9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/prefix/modsecurity/9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c` |
| apache_httpd | built | `a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/build` |
| nginx | built | `976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/build` |
| haproxy | built | `4938f4d0e0ce1594cebd4e26147b228e82f4276511dc186e5c35a6fdf815a7c9` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/haproxy/4938f4d0e0ce1594cebd4e26147b228e82f4276511dc186e5c35a6fdf815a7c9` |
| go_ftw | built | `v2.4.0` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` |
| albedo | built | `v0.3.0` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` |
| expat | built | `b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/manifest.json` | `94041f2082aa0f3fe8fc22dc04b56862c2f55edc3c2e12e6b8cb8a97aa5a4774` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/manifest.json` | present | input file available |

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `built`
- Blocker: `-`
- Cache path: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/archives/apache`
- Build path: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/build`
- apachectl/APACHECTL_BIN: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/httpd/bin/apachectl-mrts`
- Module file: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/build/output/apache/mod_security3.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `APACHECTL_BIN`
- Expat source: `https://github.com/libexpat/libexpat`
- Expat release tag: `R_2_8_2`
- CPPFLAGS: `-I/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/include`
- LDFLAGS: `-L/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/lib`
- LIBS: `-lcrypt`
- PKG_CONFIG_PATH: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/lib/pkgconfig`
- crypt.h status: `present`
- crypt.h path: `/usr/include/crypt.h`
- libcrypt status: `present`
- libcrypt paths: `/usr/lib/x86_64-linux-gnu/libcrypt.so.1.1.0, /usr/lib/x86_64-linux-gnu/libcrypt.so.1.1.0, /usr/lib/x86_64-linux-gnu/libcrypt.so.1.1.0, /usr/lib/x86_64-linux-gnu/libcrypt.so.1.1.0`
- crypt link mode: `compiler:-lcrypt`

### NGINX
- Status: `built`
- Blocker: `-`
- Cache path: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/archives/nginx`
- Build path: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/build`
- MRTS_NATIVE_NGINX_BIN: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/nginx/modules`
- Module file: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/nginx/modules/ngx_http_modsecurity_module.so`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `MRTS_NATIVE_NGINX_BIN/MRTS_NATIVE_NGINX_MODULE_DIR`

### Expat
- Status: `built`
- Blocker: `-`
- Source: `https://github.com/libexpat/libexpat`
- Release tag: `R_2_8_2`
- Actual head: `c61098da494eea1cbd091118118dcee417faacea`
- Prefix: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix`
- expat.h: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/include/expat.h`
- lib dir: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/lib`
- Recursive submodules: `-`

### go-ftw / albedo
| Dependency | Status | Binary | Env override | Source | Release tag | Head | Submodules | Release note | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| go-ftw | built | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` | `GO_FTW_BIN` | `https://github.com/coreruleset/go-ftw` | `v2.4.0` | `23db497e3a6133888fcd5e087b8cf456556df041` | `-` | prompt_expected_latest=v2.2.0; current_latest=v2.4.0 | - |
| albedo | built | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` | `ALBEDO_BIN` | `https://github.com/coreruleset/albedo` | `v0.3.0` | `3f7d0238b32d1f98059f5c70e0ffcafad514952c` | `-` | - | - |
<!-- runtime-components:end -->

<!-- runtime-build-cache:start -->
## Runtime Build Cache
- Shared ModSecurity status: `built`
- Shared ModSecurity source ref/SHA: `v3/master` / `7ea9fefbe0ba409d8733b4d682c8c4c059cd028d`
- Shared ModSecurity build ID: `9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c`
- Shared ModSecurity prefix: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/prefix/modsecurity/9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c`
- Build reuse summary: rebuilt `3`, reused `0`, blocked `0`, saved rebuilds estimate `0`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | built | `a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b` | `9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c` | - |
| nginx | built | `976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35` | `9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c` | - |
| haproxy | built | `4938f4d0e0ce1594cebd4e26147b228e82f4276511dc186e5c35a6fdf815a7c9` | `9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c` | - |
<!-- runtime-build-cache:end -->

<!-- runtime-diagnostics:start -->
## Native Runtime Diagnostics

- No generated native runtime diagnostics were detected.
<!-- runtime-diagnostics:end -->
