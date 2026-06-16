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

# Runtime Build Cache

Generated at: `2026-06-16T04:53:27Z`

## Shared ModSecurity Build
- Status: `reused`
- Blocker: `-`
- Source URL: `https://github.com/owasp-modsecurity/ModSecurity.git`
- Source ref: `v3/master`
- Actual SHA: `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Build ID: `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Prefix: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a`
- Include dir: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/include`
- Lib dir: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/lib`
- libmodsecurity: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/lib/libmodsecurity.so`
- pkg-config path: `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/lib/pkgconfig`
- Dependency hash: `ebb240b087d273581ea1d1fb76edb21afb741abc0797f8a59820735fd3edc3f3`
- Submodules recursive: `True`
- Submodule status: `bc625d5bb0bac6a64bcce8dc9902208612399348 bindings/python (bc625d5)
 211782219663f889f471650150df12b623c5766e others/libinjection (v4.0.0)
 0fe989b6b514192783c469039edd325fd0989806 others/mbedtls (v4.1.0)
 dff9da04438d712f7647fd995bc90fadd0c0e2ce others/mbedtls/framework (mbedtls-4.1.0_tf-psa-crypto-1.1.0)
 29160dd877d29658279fd683b2ae57b320ddcf09 others/mbedtls/tf-psa-crypto (v1.1.0)
 5772b4f4a0105694b1203abb582273f78fa951b7 others/mbedtls/tf-psa-crypto/drivers/pqcp/mldsa-native (remotes/origin/main-53-g5772b4f)
 dff9da04438d712f7647fd995bc90fadd0c0e2ce others/mbedtls/tf-psa-crypto/framework (mbedtls-4.1.0_tf-psa-crypto-1.1.0)
 a3d4405e5a2c90488c387e589c5534974575e35b test/test-cases/secrules-language-tests (a3d4405)`

## Connector Builds
| Connector | Status | Connector build ID | ModSecurity build ID | Invalidation reason | Binary | Module | Config | Blocker |
|---|---|---|---|---|---|---|---|---|
| apache | reused | `70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22` | `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a` | - | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/httpd` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/build/output/apache/mod_security3.so` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/conf/httpd.conf` | - |
| nginx | reused | `b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66` | `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a` | - | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/sbin/nginx` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules/ngx_http_modsecurity_module.so` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/conf/nginx.conf` | - |
| haproxy | reused | `287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44` | `38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a` | - | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-runtime/haproxy/sbin/haproxy` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-modsecurity-binding/paths.env` | - |

## Build Reuse Summary
- Rebuilt count: `0`
- Reused count: `3`
- Blocked count: `0`
- Saved rebuilds estimate: `3`
- Mismatch status: `ok`
- Mismatch blocker: `-`

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/root/.local/state/ModSecurity-conector-build/component-cache/runtime-build-cache.json` | `5947bfeffb10b0431a3aa1b6a608d3ae6edf9cd26144b7688f0136b7341b5d88` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/component-cache/runtime-build-cache.json` | present | input file available |
