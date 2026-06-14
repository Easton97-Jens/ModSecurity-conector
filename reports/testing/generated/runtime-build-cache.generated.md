# Runtime Build Cache

Generated at: `2026-06-12T17:55:50Z`

## Shared ModSecurity Build
- Status: `reused`
- Blocker: `-`
- Source URL: `https://github.com/owasp-modsecurity/ModSecurity.git`
- Source ref: `v3/master`
- Actual SHA: `2fd49292d751fc383b8faf7da6a8d480904774d0`
- Build ID: `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Prefix: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c`
- Include dir: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c/include`
- Lib dir: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c/lib`
- libmodsecurity: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c/lib/libmodsecurity.so`
- pkg-config path: `/src/ModSecurity-conector-cache/prefix/modsecurity/3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c/lib/pkgconfig`
- Dependency hash: `8ef54119a5e6bdf71d774d1799c72bdb8de3094bd8d11ef67b65126995c3e57a`
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
| apache | reused | `030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - | `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/httpd/bin/httpd` | `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/build/output/apache/mod_security3.so` | `/src/ModSecurity-conector-cache/builds/connectors/apache/030126f9ca4b1e5aacd68c19c603f527dd35ddcd8d5cca84bcd73bf15ab14c72/httpd/conf/httpd.conf` | - |
| nginx | reused | `24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - | `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/sbin/nginx` | `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/modules/ngx_http_modsecurity_module.so` | `/src/ModSecurity-conector-cache/builds/connectors/nginx/24538fdb4ba2c382f8e9266978c966de1d90b7a8761a50cef0ccfe9327ba6d71/nginx/conf/nginx.conf` | - |
| haproxy | reused | `8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939` | `3638197563a475ed5a096b2b87c7d0d6c56e7505bc9a119b4d24a344e900105c` | - | `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-runtime/haproxy/sbin/haproxy` | `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `/src/ModSecurity-conector-cache/builds/connectors/haproxy/8299ef128a35b1f67aa49b6cc75dec561f0c311caf3d7d03353ff3588fbe5939/haproxy-modsecurity-binding/paths.env` | - |

## Build Reuse Summary
- Rebuilt count: `0`
- Reused count: `3`
- Blocked count: `0`
- Saved rebuilds estimate: `3`
- Mismatch status: `ok`
- Mismatch blocker: `-`
