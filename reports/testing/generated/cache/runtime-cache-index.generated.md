> Generated file - do not edit manually.
>
> Generated at: `2026-07-13T18:27:24Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/evidence/reports/update-runtime-reports.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `9ff693c3f85b123d549342ccb5e3b9485fd89638`
> Framework SHA: `77b4e89d230a23a75bff4d871d87345d55fcad28`
> Input status: `complete`

# Runtime Cache Index

**Language:** English | [Deutsch](runtime-cache-index.generated.de.md)

- Status: `cache_input_present`
- Component cache root: `<verified-run-root>/cache-v2/shared`
- Build root: `<verified-run-root>/build`
- Component presence: `7/7`
- Important files present: `12/12`
- Policy: Local cache directories and binaries are not committed; this generated index records provenance only.

## Manifests

| Item | Status | SHA256 | Path |
|---|---|---|---|
| component-cache manifest | present | `43d434ce2d26a6e0a2211eb88f19bdd326cebeb3565b48982b4a5a75c0287308` | `<verified-run-root>/cache-v2/shared/manifest.json` |
| runtime build-cache manifest | present | `ef61e45242557bb2c2a4806871baf31e3bf9d86f38844f435503bf70d4686c48` | `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` |
| git components manifest | present | `5d823410ad054b3ce3020642c076850d279cfc3350ddcb4fda3ab1095371193c` | `<verified-run-root>/cache-v2/shared/git-components.json` |
| runtime env | present | `3149ad67b233d38cf5c4b36ab93ba726d7f2c46ec2581cd414a05c067e2cf56c` | `<verified-run-root>/cache-v2/shared/runtime-env.sh` |

## Components

| Component | Status | Build ID | Source / Path |
|---|---|---|---|
| modsecurity | reused | `060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720` |
| apache_httpd | reused | `240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0` | `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/build` |
| nginx | reused | `6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7` | `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/build` |
| haproxy | reused | `553adfcb804bc331ffcfe60106b951a930c0254d63e522ec7594485a7b55d93e` | `<verified-run-root>/cache-v2/shared/builds/connectors/haproxy/553adfcb804bc331ffcfe60106b951a930c0254d63e522ec7594485a7b55d93e` |
| go_ftw | present | `-` | `<verified-run-root>/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` |
| albedo | present | `-` | `<verified-run-root>/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` |
| expat | present | `b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a` | `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix` |

## Important Files

| Item | Status | SHA256 | Path |
|---|---|---|---|
| libmodsecurity | present | `9d2c2493a797b85e463afea695308e1648d00c7d4911c8e35509167455f951f8` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720/lib/libmodsecurity.so` |
| apache_httpd | present | `180809c7355f61facf63616b404b23847df3bf0728ffd35d228b2870b32f07e6` | `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/httpd/bin/httpd` |
| apache_apxs | present | `f287f7ee4c79076bc6e2f28d64ae1ac20684a237562e1173504da8e85259d084` | `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/httpd/bin/apxs` |
| apache_mod_security3 | present | `781518f3d553e5f344a9f123487dd02ef48d7a3be0d7c5e5eef59ebde9686a07` | `<verified-run-root>/cache-v2/shared/builds/connectors/apache/240e4a73d545554d001c7d4c4d5a037375ba616e317cd55684c9d384be3774f0/build/output/apache/mod_security3.so` |
| nginx | present | `e5f81f2db3141b9ea9c1d3891d14cba403d8df31db40ff4de3c0f5eba6f95bc5` | `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/nginx/sbin/nginx` |
| nginx_modsecurity_module | present | `f7f1d0d2910f1533d3a1ea1fbf40e448b2b07d6319a2822d02a5e77d9eea6b24` | `<verified-run-root>/cache-v2/shared/builds/connectors/nginx/6f4d535ef84e518326dab98b64e457b33fef2b08936ff5bd60fac42f2aa0baf7/nginx/modules/ngx_http_modsecurity_module.so` |
| haproxy | present | `dd239e317ee8a3f5ae5faa862d2736251f5b8eeb3271c99951c67e6bcf8f8e66` | `<verified-run-root>/cache-v2/shared/builds/connectors/haproxy/553adfcb804bc331ffcfe60106b951a930c0254d63e522ec7594485a7b55d93e/haproxy-runtime/haproxy/sbin/haproxy` |
| haproxy_spoa | present | `6c015cb027516225b687b39d19c0e7ff8ecafc7b9f0b7d172eb1a9470c9bf409` | `<verified-run-root>/cache-v2/shared/builds/connectors/haproxy/553adfcb804bc331ffcfe60106b951a930c0254d63e522ec7594485a7b55d93e/haproxy-spoa-runtime/haproxy-modsecurity-spoa` |
| go-ftw | present | `332425c41385ee10fa79c543ce8527c099873fd73bcaf73dd2a2cc353f84b952` | `<verified-run-root>/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` |
| albedo | present | `72872f718729f51e924fa8ba3c82b3b5eca9db6be4490fc5cbb731317f2ad1bd` | `<verified-run-root>/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` |
| expat_header | present | `eb43180fbdca40e36d9558060e6e654ef4c451ca656ad679e9e1269eb45456b3` | `<verified-run-root>/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/include/expat.h` |
| shared_build_libmodsecurity | present | `9d2c2493a797b85e463afea695308e1648d00c7d4911c8e35509167455f951f8` | `<verified-run-root>/cache-v2/shared/prefix/modsecurity/060604d44135db16f6aad7d6cc519a2c6e5d1ad5d499d3782ab35cec22753720/lib/libmodsecurity.so` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/cache-v2/shared/manifest.json` | `43d434ce2d26a6e0a2211eb88f19bdd326cebeb3565b48982b4a5a75c0287308` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | `ef61e45242557bb2c2a4806871baf31e3bf9d86f38844f435503bf70d4686c48` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/cache-v2/shared/git-components.json` | `5d823410ad054b3ce3020642c076850d279cfc3350ddcb4fda3ab1095371193c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/cache-v2/shared/runtime-env.sh` | `3149ad67b233d38cf5c4b36ab93ba726d7f2c46ec2581cd414a05c067e2cf56c` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/cache-v2/shared/manifest.json` | present | input file available |
| `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | present | input file available |
| `<verified-run-root>/cache-v2/shared/git-components.json` | present | input file available |
| `<verified-run-root>/cache-v2/shared/runtime-env.sh` | present | input file available |
