> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T19:36:08Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/evidence/reports/update-runtime-reports.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
> Framework SHA: `4e9d4ba616235127b6fc0a2ee87107d93d03f40b`
> Input status: `complete`

# Runtime Cache Index

**Language:** English | [Deutsch](runtime-cache-index.generated.de.md)

- Status: `cache_input_present`
- Component cache root: `<verified-run-root>/cache-v2/shared`
- Build root: `<verified-run-root>/build/lighttpd/repository-cleanup-core-20260712T192931Z`
- Component presence: `2/7`
- Important files present: `3/12`
- Policy: Local cache directories and binaries are not committed; this generated index records provenance only.

## Manifests

| Item | Status | SHA256 | Path |
|---|---|---|---|
| component-cache manifest | present | `13123f03dbe90f01402a8c2c439e46455a0fa688448e540a5cdab11722022392` | `<verified-run-root>/cache-v2/shared/manifest.json` |
| runtime build-cache manifest | present | `04ba882c6feda15868fc9b175f3d3c2875fdbdfa480872a332d8317edea1b017` | `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` |
| git components manifest | present | `264e9488d22ea6b598613a178f48a72c89c9e3ec9cd33825c07e5b68a1396262` | `<verified-run-root>/cache-v2/shared/git-components.json` |
| runtime env | present | `30c186efdd2a51a0dde44eb10b2b3b9dfd7a4ee1d3862fe33c2e2bbe2cf71cb1` | `<verified-run-root>/cache-v2/shared/runtime-env.sh` |

## Components

| Component | Status | Build ID | Source / Path |
|---|---|---|---|
| modsecurity | reused | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` |
| apache_httpd | not_selected | `-` | `-` |
| nginx | not_selected | `-` | `-` |
| haproxy | not_selected | `-` | `-` |
| go_ftw | not_selected | `-` | `-` |
| albedo | not_selected | `-` | `-` |
| expat | present | `b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a` | `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix` |

## Important Files

| Item | Status | SHA256 | Path |
|---|---|---|---|
| libmodsecurity | present | `b95a7d601c043ae9dcf94e486bc177903e3864de08742cdd10ffb917e8605f5d` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720/lib/libmodsecurity.so` |
| apache_httpd | missing | `-` | `-` |
| apache_apxs | missing | `-` | `-` |
| apache_mod_security3 | missing | `-` | `-` |
| nginx | missing | `-` | `-` |
| nginx_modsecurity_module | missing | `-` | `-` |
| haproxy | missing | `-` | `-` |
| haproxy_spoa | missing | `-` | `-` |
| go-ftw | missing | `-` | `-` |
| albedo | missing | `-` | `-` |
| expat_header | present | `eb43180fbdca40e36d9558060e6e654ef4c451ca656ad679e9e1269eb45456b3` | `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/include/expat.h` |
| shared_build_libmodsecurity | present | `b95a7d601c043ae9dcf94e486bc177903e3864de08742cdd10ffb917e8605f5d` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720/lib/libmodsecurity.so` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/cache-v2/shared/manifest.json` | `13123f03dbe90f01402a8c2c439e46455a0fa688448e540a5cdab11722022392` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | `04ba882c6feda15868fc9b175f3d3c2875fdbdfa480872a332d8317edea1b017` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/cache-v2/shared/git-components.json` | `264e9488d22ea6b598613a178f48a72c89c9e3ec9cd33825c07e5b68a1396262` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/cache-v2/shared/runtime-env.sh` | `30c186efdd2a51a0dde44eb10b2b3b9dfd7a4ee1d3862fe33c2e2bbe2cf71cb1` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/cache-v2/shared/manifest.json` | present | input file available |
| `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | present | input file available |
| `<verified-run-root>/cache-v2/shared/git-components.json` | present | input file available |
| `<verified-run-root>/cache-v2/shared/runtime-env.sh` | present | input file available |
