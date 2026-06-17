> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:44:44Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/prepare-runtime-components.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
> Input status: `complete`

# Runtime Build Cache

Generated at: `2026-06-17T02:44:44Z`

## Shared ModSecurity Build
- Status: `reused`
- Blocker: `-`
- Source URL: `https://github.com/owasp-modsecurity/ModSecurity.git`
- Source ref: `v3/master`
- Actual SHA: `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Build ID: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Prefix: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- Include dir: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/include`
- Lib dir: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib`
- libmodsecurity: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib/libmodsecurity.so`
- pkg-config path: `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib/pkgconfig`
- Dependency hash: `6520718cfc3861c8b4bd8046bfb3c50674a89f771041673ed3b132f5cbf8fea4`
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
| apache | reused | `898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/httpd` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build/output/apache/mod_security3.so` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/conf/httpd.conf` | - |
| nginx | reused | `d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/conf/nginx.conf` | - |
| haproxy | reused | `599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048` | `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72` | - | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-runtime/haproxy/sbin/haproxy` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/599b09c9a142d357cf043c4b2046ec7dee4f3585edab18520c52968b06936048/haproxy-modsecurity-binding/paths.env` | - |

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
| Declared input | `/var/tmp/ModSecurity-conector-verified/component-cache/runtime-build-cache.json` | `87188127b17897e96f4e79be597755779142554a5a0a6636d3bbe93b0e33df74` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/component-cache/runtime-build-cache.json` | present | input file available |
