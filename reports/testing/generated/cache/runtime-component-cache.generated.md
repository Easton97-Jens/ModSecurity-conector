> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T19:36:08Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/provisioning/components/prepare-runtime-components.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
> Framework SHA: `4e9d4ba616235127b6fc0a2ee87107d93d03f40b`
> Input status: `complete`

# Runtime Component Cache

**Language:** English | [Deutsch](runtime-component-cache.generated.de.md)

- Cache root: `<verified-run-root>/cache-v2/shared`
- Build root: `<verified-run-root>/build/lighttpd/repository-cleanup-core-20260712T192931Z`
- Generated at: `2026-07-12T19:36:08Z`
- Local cache binaries and source trees are not committed; this report records provenance.

| Component | Status | Build ID / Ref | Path |
|---|---|---|---|
| modsecurity | reused | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` |
| apache_httpd | not_selected | `-` | `-` |
| nginx | not_selected | `-` | `-` |
| haproxy | not_selected | `-` | `-` |
| go_ftw | not_selected | `-` | `-` |
| albedo | not_selected | `-` | `-` |
| expat | present | `b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a` | `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/cache-v2/shared/manifest.json` | `13123f03dbe90f01402a8c2c439e46455a0fa688448e540a5cdab11722022392` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/cache-v2/shared/manifest.json` | present | input file available |

<!-- runtime-components:start -->
## Runtime Components

### Apache httpd
- Status: `not_selected`
- Blocker: `-`
- Cache path: `-`
- Build path: `-`
- apachectl/APACHECTL_BIN: `-`
- Module file: `-`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `-`
- Expat source: `-`
- Expat release tag: `-`
- CPPFLAGS: `-`
- LDFLAGS: `-`
- LIBS: `-`
- PKG_CONFIG_PATH: `-`
- crypt.h status: `-`
- crypt.h path: `-`
- libcrypt status: `-`
- libcrypt paths: `-`
- crypt link mode: `-`

### NGINX
- Status: `not_selected`
- Blocker: `-`
- Cache path: `-`
- Build path: `-`
- MRTS_NATIVE_NGINX_BIN: `-`
- MRTS_NATIVE_NGINX_MODULE_DIR: `-`
- Module file: `-`
- Missing file: `-`
- Build component: `-`
- Env variable to set: `-`

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
| go-ftw | not_selected | `-` | `-` | `-` | `-` | `-` | `-` | - | - |
| albedo | not_selected | `-` | `-` | `-` | `-` | `-` | `-` | - | - |
<!-- runtime-components:end -->

<!-- runtime-build-cache:start -->
## Runtime Build Cache
- Shared ModSecurity status: `reused`
- Shared ModSecurity source ref/SHA: `v3/master` / `7ea9fefbe0ba409d8733b4d682c8c4c059cd028d`
- Shared ModSecurity build ID: `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720`
- Shared ModSecurity prefix: `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720`
- Build reuse summary: rebuilt `0`, reused `0`, blocked `0`, saved rebuilds estimate `0`

| Connector | Status | Connector build ID | Uses ModSecurity build ID | Blocker |
|---|---|---|---|---|
| apache | not_selected | `-` | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | - |
| nginx | not_selected | `-` | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | - |
| haproxy | not_selected | `-` | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | - |
<!-- runtime-build-cache:end -->

<!-- runtime-diagnostics:start -->
## Native Runtime Diagnostics

- No generated native runtime diagnostics were detected.
<!-- runtime-diagnostics:end -->
