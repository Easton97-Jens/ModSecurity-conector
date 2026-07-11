> Generated file - do not edit manually.
>
> Generated at: `2026-07-11T17:55:31Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/update-runtime-reports.py`
> Make target: `prepare-runtime-components`
> Owner: `cache`
> Severity: `cache`
> Connector SHA: `6bfdc66329fc68531b3f358cab25ef91b3d9a2a9`
> Framework SHA: `9415da97a6cbac472bec3c3e1343b636a51c267b`
> Input status: `complete`

# Runtime Cache Index

**Language:** English | [Deutsch](runtime-cache-index.generated.de.md)

- Status: `cache_input_present`
- Component cache root: `/var/tmp/ModSecurity-conector-verified/cache-v2/shared`
- Build root: `/var/tmp/ModSecurity-conector-verified/build`
- Component presence: `7/7`
- Important files present: `12/12`
- Policy: Local cache directories and binaries are not committed; this generated index records provenance only.

## Manifests

| Item | Status | SHA256 | Path |
|---|---|---|---|
| component-cache manifest | present | `94041f2082aa0f3fe8fc22dc04b56862c2f55edc3c2e12e6b8cb8a97aa5a4774` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/manifest.json` |
| runtime build-cache manifest | present | `2aeaf5f1086a75f267866ce70afeeb9216fcd177c9935c6da06e478fe15d55cb` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/runtime-build-cache.json` |
| git components manifest | present | `2771cf04a8446da6641f3798282e76d99b8485a604e1b6e46cef4aff85944d51` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/git-components.json` |
| runtime env | present | `f74da8cc63ea50a332c97ce9f6bc5dac76df3c312a6fdb03332580c6d20e241a` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/runtime-env.sh` |

## Components

| Component | Status | Build ID | Source / Path |
|---|---|---|---|
| modsecurity | built | `9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/prefix/modsecurity/9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c` |
| apache_httpd | built | `a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/build` |
| nginx | built | `976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/build` |
| haproxy | built | `4938f4d0e0ce1594cebd4e26147b228e82f4276511dc186e5c35a6fdf815a7c9` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/haproxy/4938f4d0e0ce1594cebd4e26147b228e82f4276511dc186e5c35a6fdf815a7c9` |
| go_ftw | built | `-` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` |
| albedo | built | `-` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` |
| expat | built | `b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix` |

## Important Files

| Item | Status | SHA256 | Path |
|---|---|---|---|
| libmodsecurity | present | `78153495602d7920ea039d5d80377e485ff664d59e530002213ee0f2e7a655f5` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/prefix/modsecurity/9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c/lib/libmodsecurity.so` |
| apache_httpd | present | `2d25dc9a9fd95b2ff94b7af1bdd089bc89f28187730644971f015ef521191afc` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/httpd/bin/httpd` |
| apache_apxs | present | `350709490dc6225c4a71ff027d37385b0732defd28317a1de19610a58e8cc6f7` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/httpd/bin/apxs` |
| apache_mod_security3 | present | `c7a6512dac4974c5ee4471275aba6885cc5aa6d621c266b974a0c9b90b62a6fe` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/apache/a101d8d0d6292edf710cca9d29e316235f20f1bc5c7bc196caec649d2d1ef85b/build/output/apache/mod_security3.so` |
| nginx | present | `c7784bfa01e4f1108e00d8865db63054350ee79cbc99560b66c2511ee84c1517` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/nginx/sbin/nginx` |
| nginx_modsecurity_module | present | `24d8fe5311730ae224ee485bf3dbd8dc0f1181d26389caa6e72783b4322259ed` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/nginx/976787199b260ec2c99e82820afb96e581161783a806874984f67c157a918a35/nginx/modules/ngx_http_modsecurity_module.so` |
| haproxy | present | `4302620d3a920b8dd060cb3c7e8ef1a93063efc1c626cb89794232102e0667fe` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/haproxy/4938f4d0e0ce1594cebd4e26147b228e82f4276511dc186e5c35a6fdf815a7c9/haproxy-runtime/haproxy/sbin/haproxy` |
| haproxy_spoa | present | `6276950bf69cc23a9d427e6a38168215aca3c753d4eac03af08c3598bcf9f40f` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/connectors/haproxy/4938f4d0e0ce1594cebd4e26147b228e82f4276511dc186e5c35a6fdf815a7c9/haproxy-spoa-runtime/haproxy-modsecurity-spoa` |
| go-ftw | present | `332425c41385ee10fa79c543ce8527c099873fd73bcaf73dd2a2cc353f84b952` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/go-ftw/74b4c6358105c30563ba2820b7addd03dea61dfb039d4d247d3cbe359c2b3f21/bin/go-ftw` |
| albedo | present | `72872f718729f51e924fa8ba3c82b3b5eca9db6be4490fc5cbb731317f2ad1bd` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/go/albedo/7a41a855770221b2347883bd4de5cc692e364155ad00056173807182bab9e2c1/bin/albedo` |
| expat_header | present | `eb43180fbdca40e36d9558060e6e654ef4c451ca656ad679e9e1269eb45456b3` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/builds/expat/b644c7b974a809dc1562b206e7d29aeeaaa4167d43d42cdd6c9bb10714daf57a/prefix/include/expat.h` |
| shared_build_libmodsecurity | present | `78153495602d7920ea039d5d80377e485ff664d59e530002213ee0f2e7a655f5` | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/prefix/modsecurity/9e93a3edb1d5b3a2355b7cf4c85d6a3e3e1c5c58b637dc5589ceec9aac8d4e5c/lib/libmodsecurity.so` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/manifest.json` | `94041f2082aa0f3fe8fc22dc04b56862c2f55edc3c2e12e6b8cb8a97aa5a4774` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/runtime-build-cache.json` | `2aeaf5f1086a75f267866ce70afeeb9216fcd177c9935c6da06e478fe15d55cb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/git-components.json` | `2771cf04a8446da6641f3798282e76d99b8485a604e1b6e46cef4aff85944d51` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/runtime-env.sh` | `f74da8cc63ea50a332c97ce9f6bc5dac76df3c312a6fdb03332580c6d20e241a` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/runtime-build-cache.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/git-components.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/cache-v2/shared/runtime-env.sh` | present | input file available |
