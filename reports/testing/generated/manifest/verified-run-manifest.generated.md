> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:48:18Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/run-verified-report-run.py`
> Make target: `verified-report-run`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `complete`

# Verified Run Manifest

## Summary
- Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
- Data source policy: `verified-inputs-only`
- Profile: `full`
- Start time UTC: `2026-06-16T04:53:13Z`
- End time UTC: `2026-06-16T05:48:18Z`
- Duration seconds: `3305.0`
- Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
- Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
- MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
- Parent branch: `master`
- Framework branch: `master`
- Dirty status: `dirty` / `dirty`
- Full matrix timeout seconds: `7200`
- Runtime matrix timeout seconds: `1800`
- Full matrix runtime timeout seconds: `7200`
- Report refresh timeout seconds: `1800`
- Native MRTS timeout seconds: `1800`

## Runtime Paths

| Variable | Value |
|---|---|
| `BUILD_ROOT` | `/root/.local/state/ModSecurity-conector-build` |
| `SOURCE_ROOT` | `/root/.local/state/ModSecurity-conector-src` |
| `TMP_ROOT` | `/root/.local/state/ModSecurity-conector-build/tmp` |
| `LOG_ROOT` | `/root/.local/state/ModSecurity-conector-build/logs` |
| `CONNECTOR_COMPONENT_CACHE` | `/root/.local/state/ModSecurity-conector-build/component-cache` |
| `NGINX_HARNESS_PARENT` | `/root/.local/state/ModSecurity-conector-build/tmp/nginx-harness` |
| `MATRIX_ROOT` | `/root/.local/state/ModSecurity-conector-build/full-matrix` |
| `MRTS_BUILD_ROOT` | `/root/.local/state/ModSecurity-conector-build/mrts` |
| `MRTS_NATIVE_ROOT` | `/root/.local/state/ModSecurity-conector-build/mrts-native` |
| `VERIFIED_RUN_ROOT` | `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0` |

## Runtime Producer Readiness

- Status: `PASS`
- Runtime env loaded: `True`
- Runtime env path: `/root/.local/state/ModSecurity-conector-build/component-cache/runtime-env.sh`

| Component | Required | Status | Path | Fix |
|---|---|---|---|---|
| common.sh | True | present | `/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/common.sh` | `ensure FRAMEWORK_ROOT points at modules/ModSecurity-test-Framework` |
| NGINX binary | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/sbin/nginx` | `run make prepare-runtime-components` |
| NGINX ModSecurity module | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules/ngx_http_modsecurity_module.so` | `run make prepare-runtime-components` |
| NGINX libmodsecurity | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/prefix/modsecurity/38503a5b3c496424e81b4d6bba0b34bd329cf40a76e82c3fa3ef07abff5dfc0a/lib/libmodsecurity.so.3.0.15` | `run make prepare-runtime-components` |
| Apache/httpd | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/httpd` | `run make prepare-runtime-components` |
| Apache/APXS | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/httpd/bin/apxs` | `run make prepare-runtime-components` |
| Apache ModSecurity module | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/apache/70269d7c4705bf86cb946dd57aa0f4ba51d9392dd51fa01a5f75577599e50b22/build/output/apache/mod_security3.so` | `run make prepare-runtime-components` |
| HAProxy binary | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-runtime/haproxy/sbin/haproxy` | `run make prepare-runtime-components` |
| HAProxy SPOA runtime | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-spoa-runtime/haproxy-modsecurity-spoa` | `run make prepare-runtime-components` |
| HAProxy binding metadata | True | present | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/haproxy/287be9c0e1cfe3a32892e9df97f415950b4064a49d6d8aee7292476b86773d44/haproxy-modsecurity-binding/paths.env` | `run make prepare-runtime-components` |
| go-ftw | False | present | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/go-ftw` | `optional native MRTS: install or cache go-ftw` |
| albedo | False | present | `/root/.local/state/ModSecurity-conector-build/component-cache/bin/albedo` | `optional native MRTS: install or cache albedo` |

## NGINX Runtime Module Readiness

| Field | Value |
|---|---|
| NGINX_BIN | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/sbin/nginx` |
| NGINX_MODULE_DIR | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules` |
| ModSecurity module path | `/root/.local/state/ModSecurity-conector-build/component-cache/builds/connectors/nginx/b8c4040163e68e315279dcfbd360e01586e650c70c955fb30c1d79bc92841b66/nginx/modules/ngx_http_modsecurity_module.so` |
| Module exists | `true` |
| How to prepare | `make prepare-runtime-components` |

## Runtime Network / Cache Readiness

| Source | Status | Path | Notes |
|---|---|---|---|
| nginx latest release | present | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/nginx/nginx-latest-release.json` | local cache available |
| nginx archive cache | present | `/root/.local/state/ModSecurity-conector-build/component-cache/archives/nginx` | local cache available |
| go-ftw git cache | present | `/root/.local/state/ModSecurity-conector-build/component-cache/git/go-ftw` | local cache available |
| albedo git cache | present | `/root/.local/state/ModSecurity-conector-build/component-cache/git/albedo` | local cache available |

## Verified Commands

| Phase | Command | Required | Status | Return Code | Classification | Signal | Duration | Log Hash | Affected Reports |
|---|---|---|---|---:|---|---|---:|---|---|
| full-matrix-resume | `make full-matrix-resume-runtime` | True | FAIL | 2 | command_failed | - | 3299.249 | `aa4e36bd191587ade34676afae8fbd549eb2b62b315a39be24d8f3b81f1c6c9e` | full_matrix_job_completeness, verified_runtime_mismatch_analysis |
| full-matrix-resume | `make generate-full-matrix-job-completeness` | False | PASS | 0 | success | - | 1.019 | `3cfdd9654bd9aea02a14560a77993e6c5dd609181939a80f167cbcd8096e567f` | full_matrix_job_completeness |
| full-matrix-resume | `make generate-verified-runtime-mismatch-analysis` | False | PASS | 0 | success | - | 4.279 | `2f5b365ee8c42635ad8196bd844e78a931b45c98239fd8cc3585f9006f569ff8` | verified_runtime_mismatch_analysis |

## Input Files

| Input | Status | Hash | Verified Run ID | Notes |
|---|---|---|---|---|
| `BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl` | present | `6ccf6b32b3d3ff2a223b8845665cb30e7b6780af1b1dcd51ad18494c62199e22` | `unknown` | input file available |
| `BUILD_ROOT:mrts-native/apache2_ubuntu/job.json` | present | `8b350ba5c18a3b09fe0e4bea9b2ac83cab48e9c0d4e88a384577784a7c26e99e` | `unknown` | input file available |
| `BUILD_ROOT:mrts-native/nginx-pr24/job.json` | present | `8f66d8d8c5bff22af0b1ea1385c3a52fb41121c530efbc9be4f8404f688f84eb` | `unknown` | input file available |
| `BUILD_ROOT:verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | `671974a44c2e4b18fb2aa9dfc319b90ad3371e5b7a2fe7fc5b36f807eea6bf4f` | `unknown` | input file available |
| `config/testing/import-status.json` | present | `5eea82df1ded18c34bbc8cf6fc5992572edaa6723a33b6dd4a0b49ee00ab5a4f` | `unknown` | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | `2fa73fb20acc3d8ebf3c5f13b25df04745e965bc6b12857d01ed60376a24ff37` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | `c346d6359ca121be6ee58811893fc95ee6f3244edef4f560940330dfe60850d3` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | present | `475a142d0460dad007d08bc16d9a678da63b89d81ae8f8e9e6156ba1e0b24970` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | `8aa64d43d1c69d0624e8fa96a2e10d6d74be92d6aa34e524e64cb576c17881ba` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | `b0b57583e5ffecfe97459edb9b92ba6b12f6b6ebee3343c74a9955e671874990` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | present | `cba744caca5f7a040034c64b63264b6de09dd9224b7e1f7d24351f64f9a01b90` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | blocked | `7df81e3248e22e0b9c9704bc04029fc1f7826b2875b5565bc67046b6a91890ac` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | `d7379502a744d95a3faf857f525abc0086c67c7ac5a75d8dbd29d325aba050fe` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | blocked | `ad7cce72954b847dd02f0f4d3e6b5cbe1c14a4ac0ccdbe3bd88752319a6b9845` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked_timeout |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | present | `bb872b715b954d4023c3476af2e9c9d3c89024dfa3a2f92b90d552557e220739` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | blocked | `d2517cb962f76c53c5bff5a9609018063c3c5d9e4e8a579612eebda909cd54e3` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.md` | present | `e162c7b7a08b31b6647b6aa5c00e58197a17ae505b89b5974d6def679c7654eb` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | blocked | `b13f5619431dd862914e307ddeb9109e02192ee4303b366f56f87139431efa41` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | present | `1cf981c433ed8a08d1a46745cc0dd7c149653ddd677b2f4dad7ad46bcc234ca4` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/coverage/case-matrix.generated.md` | present | `71dc15ffc54fc14a7383d9d699479d22b561d2642843ee500027df548e6cd096` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/coverage/connector-gap-summary.generated.md` | present | `741505150c075ff27a898425053f22901d1fb5585f513458aae8c29c06632038` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/coverage/coverage-summary.generated.md` | present | `6861d17dfebcbd5886d824f232646f1267395d9c3bb77fa9cd2ed35a16a6981a` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | `83a569d4edecbaf1a158f61de872194b5d297df37326508523983cc38bcf7a43` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/coverage/xfail-summary.generated.md` | present | `fb1ac4559f83c471ccd87929109dd6c76445c6f084bcc689bbe9e79906336c6e` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | blocked | `e765e41dc39a959c66302242391ac0c5380c92e6b1927da339833cf1094acd94` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | present | `bc177355e8fcfb225984390b383b4bfd7a78d009170446d0cd0f10e82fa0a4b1` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | blocked | `7f92194820446848229e8c8d988b5ab7a7344879a7cf3fe367069c9ff762ea4e` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | present | `d3f5d826b4602e49da56961f1111805f4441c6a21fff90e41103b4aff9110539` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | blocked | `7b1c4b67076a9181c64680d0a9c336ab71e229cc83aaaa0c58f95a26e6c7028b` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | present | `34e57cf6fa3a65f175969aaedb3b1caa9245e8bded1ffe440de844b4ace1cc17` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | blocked | `15fd40a83021c9895528a93f0a64dc6bf417b0f624085680dcf6b9ef422ea960` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | present | `2b93f96c0e23c93ae2487737b2aece9db6a5c3f7b3530c94e2803c4e2c21331f` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | blocked | `c91229efaa024396925a75d3905cc6d6e5a637bcca2d956062021a7df0118251` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | present | `4da847720d9223fcfcc21f9ed6fd83330c48274302889c3012e02987839311d4` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | blocked | `6ed71cdca4dfba5f159a4ccd83aee7fd6e49200a7ac15aebfb174894a4918d90` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | present | `491f25432f42988e14f79192c1efe9ab76b1e0e373687a0edbcae5461d584bfd` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | blocked | `ddbf7b3071b1042cf01096b68169d4d76b8cafd55b3526f5aa8c455cdd979612` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | present | `2496d201a9aa0c472076516200f58f8822eac47680901a3bd4d381db87da00e2` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | present | `830e1523156a2b45e77a3ad6e7e52c3f46b558a9ca1a5646e4bfd0a75c64d792` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.json` | present | `fa3996b147a0ce207b2e6d767ca7deeb63830785836d5d1ae3932d2a80f9865d` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.md` | present | `1383404244be5db60996f91ee73294a30840493969aba6d5359cfd8dcf227c8c` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.json` | present | `7cbdf7066f27e0653cef42a7dc9de5d068c60f6163ba26ba5b5549cb446dc49d` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.md` | present | `57815ab4786ff3fbfc9e1a6f4d617fc4320c9697b549dda6e0dd8e22641969c5` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | `746c706f12e49373f08d379ffd0cdeec50c6ea384c078dbb4ffe3eff54ea3ad8` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.json` | present | `5a55b747d6cc59f5a94a704f3d0c14a091c7f401f4ea2a73fee6d2be2c495a2c` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.md` | present | `af78e8fde6d11579b3c5d2ea3462b2909b40b5751533d73313e2b6d06297da4b` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | `8fa41f5e3b1ad3b286286d860e38390801850bbc19e0555ebd2fe1e61b33d83d` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | present | `2766c8ed28f4672cca1369db33a45d387ab9947f2c0753b7c83a73e3ca9ea832` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | skipped_stale_input | `9ccb5431764aac542ae1fcc02de342d814491d3930590ffad49889e2aa6b59f1` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | present | `a8633e8e841b90d730d9ebcb02730acc4fc7850c079dd93a26e45cfe25665250` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | skipped_stale_input | `ef1782f5883aa61a97b31c773626890019504c3d39d259dd650fe10b43e64caf` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | present | `0f8c15d99cafe463c5c2b3ae2d0b231b826a7a39d5be3f7b812be80840bb0346` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | skipped_stale_input | `7603d2d25d50d28601bf426cce70657faea786102d32340e705041dd0301ad94` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | present | `55aaab4c5b4c06862fa88267c0088b3afbc5a96f0688222e141dc4385f270fc8` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | skipped_stale_input | `ec837bd41cd5d356213d325785e78ed7c08da8afbd62dc49609021c5d156fe6b` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | present | `44a0af41e18afc437e3eef2cc5337dd0b8505ef6fb9aafd602cd3d2aa464e647` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/runtime/apache-runtime-results.generated.md` | present | `d02d9f600385604b9139d8a7e50832ac0eafe4d50f605d1e593b4121c98e3fdc` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | present | `41c2fc870163d1165ffec1a77d846c009d53f9a80c378424a53b72bab5106db3` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | present | `f21dfc2d1be602668d7e9c400c19c16c4e5434459c7fd690d8350b7c9119b966` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/runtime/runtime-matrix.generated.md` | present | `0b6853474ac767101b15af4ceb1dbae06ba1ff6441ea50a28725ab69cb3b4d96` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | blocked | `683e6b8d49fd9dc2321e2547fff545e7773d304c0aec2e0f59fce00571f97e51` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/connector-work-queue.generated.md` | present | `e044b85c8fd4ca9f14d8c593bf8095f4e1af58e12461fdff41ae09e2d1ead3b4` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | blocked | `5c41e4ab4a98cabef427230a0a9438cc9dad25c395c50ff3fc05e8f79e745cf8` | `2026-06-15T21-01-39Z-9391a8d0` | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | `96aff1253a1edd79c962ddd1587fa49ab66e7254f39546d99c41ca74c3759e37` | `2026-06-15T21-01-39Z-9391a8d0` | input file available |
| `reports/testing/runtime-validation-snapshot.json` | present | `dfeb2c386052d649210cd1b1acaa5dab644396c933eec71daa33e2bbd5f3b5ed` | `unknown` | input file available |
| `reports/testing/test-coverage-overview.md` | present | `5c8096063ef4627fe301c55db152507274507583728ddfe1d838c120bdeaa911` | `unknown` | input file available |

## Output Files

| Output | Status | Hash | Bytes |
|---|---|---|---:|
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | `443a82e324f1acc1b0ab2faaa3304e7244e40bfd18e5666297bb3fed586c0d16` | 16621 |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | `6710a7aec9c0b8bf82a48f90200bf7ebf352e2313536d9fc6b60558b24643ec0` | 5603 |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | present | `cb6706def1a85d59cfb8562b1d15c697a2118f936f7319a9401b229206798c11` | 80699 |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | `45cdb3aff692c89b12052deb83ad3bae10c58433f3bf43bca8ca630a105971d3` | 16362 |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | `b0b57583e5ffecfe97459edb9b92ba6b12f6b6ebee3343c74a9955e671874990` | 10227 |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | present | `cba744caca5f7a040034c64b63264b6de09dd9224b7e1f7d24351f64f9a01b90` | 6477 |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | `5ea741c3579719fe85f0f08f7344a0665db75a1cce1dc521564d805e9b5e2b68` | 5890 |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | `4d48b4011817c0b2fffeea356d4a720ab712709c0d26589300bcaff6b537e67a` | 3671 |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | `ad7cce72954b847dd02f0f4d3e6b5cbe1c14a4ac0ccdbe3bd88752319a6b9845` | 2630 |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | present | `bb872b715b954d4023c3476af2e9c9d3c89024dfa3a2f92b90d552557e220739` | 1981 |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | `d2517cb962f76c53c5bff5a9609018063c3c5d9e4e8a579612eebda909cd54e3` | 4181 |
| `reports/testing/generated/canonical/next-fix-plan.generated.md` | present | `e162c7b7a08b31b6647b6aa5c00e58197a17ae505b89b5974d6def679c7654eb` | 2670 |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | `b13f5619431dd862914e307ddeb9109e02192ee4303b366f56f87139431efa41` | 4220 |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | present | `1cf981c433ed8a08d1a46745cc0dd7c149653ddd677b2f4dad7ad46bcc234ca4` | 2681 |
| `reports/testing/generated/coverage/case-matrix.generated.md` | present | `71dc15ffc54fc14a7383d9d699479d22b561d2642843ee500027df548e6cd096` | 30958 |
| `reports/testing/generated/coverage/connector-gap-summary.generated.md` | present | `741505150c075ff27a898425053f22901d1fb5585f513458aae8c29c06632038` | 11054 |
| `reports/testing/generated/coverage/coverage-summary.generated.md` | present | `6861d17dfebcbd5886d824f232646f1267395d9c3bb77fa9cd2ed35a16a6981a` | 2999 |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | `83a569d4edecbaf1a158f61de872194b5d297df37326508523983cc38bcf7a43` | 1749 |
| `reports/testing/generated/coverage/xfail-summary.generated.md` | present | `fb1ac4559f83c471ccd87929109dd6c76445c6f084bcc689bbe9e79906336c6e` | 24839 |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | present | `e765e41dc39a959c66302242391ac0c5380c92e6b1927da339833cf1094acd94` | 4273 |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | present | `bc177355e8fcfb225984390b383b4bfd7a78d009170446d0cd0f10e82fa0a4b1` | 2723 |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | present | `7f92194820446848229e8c8d988b5ab7a7344879a7cf3fe367069c9ff762ea4e` | 4920 |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | present | `d3f5d826b4602e49da56961f1111805f4441c6a21fff90e41103b4aff9110539` | 3104 |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | present | `7b1c4b67076a9181c64680d0a9c336ab71e229cc83aaaa0c58f95a26e6c7028b` | 4409 |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | present | `34e57cf6fa3a65f175969aaedb3b1caa9245e8bded1ffe440de844b4ace1cc17` | 2790 |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | present | `15fd40a83021c9895528a93f0a64dc6bf417b0f624085680dcf6b9ef422ea960` | 3679 |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | present | `2b93f96c0e23c93ae2487737b2aece9db6a5c3f7b3530c94e2803c4e2c21331f` | 2339 |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | present | `c91229efaa024396925a75d3905cc6d6e5a637bcca2d956062021a7df0118251` | 4273 |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | present | `4da847720d9223fcfcc21f9ed6fd83330c48274302889c3012e02987839311d4` | 2718 |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | present | `6ed71cdca4dfba5f159a4ccd83aee7fd6e49200a7ac15aebfb174894a4918d90` | 3706 |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | present | `491f25432f42988e14f79192c1efe9ab76b1e0e373687a0edbcae5461d584bfd` | 2342 |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | present | `ddbf7b3071b1042cf01096b68169d4d76b8cafd55b3526f5aa8c455cdd979612` | 4330 |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | present | `2496d201a9aa0c472076516200f58f8822eac47680901a3bd4d381db87da00e2` | 2746 |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | `28baba532291a1a3e193b63e494117140a1435961bac4e5bf1e31f306e6a8050` | 106630 |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | present | `4829a63ccb89df5d233673831d9568b66b70101ef89cce8c50ede3409a19c44d` | 40556 |
| `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | present | `830e1523156a2b45e77a3ad6e7e52c3f46b558a9ca1a5646e4bfd0a75c64d792` | 22637 |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | `3b3387c0b99c427fe38858123d3d5743b979b484e74c83c7425fb71176321da6` | 7917 |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | present | `0f005f9fffbd526263286d11d0b68c9c158507182d6aa5d69d977f001c2901d9` | 4915 |
| `reports/testing/generated/manifest/report-data-lineage.generated.json` | present | `fa3996b147a0ce207b2e6d767ca7deeb63830785836d5d1ae3932d2a80f9865d` | 58623 |
| `reports/testing/generated/manifest/report-data-lineage.generated.md` | present | `1383404244be5db60996f91ee73294a30840493969aba6d5359cfd8dcf227c8c` | 26645 |
| `reports/testing/generated/manifest/report-dependency-graph.generated.json` | present | `7cbdf7066f27e0653cef42a7dc9de5d068c60f6163ba26ba5b5549cb446dc49d` | 65200 |
| `reports/testing/generated/manifest/report-dependency-graph.generated.md` | present | `57815ab4786ff3fbfc9e1a6f4d617fc4320c9697b549dda6e0dd8e22641969c5` | 30243 |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | `746c706f12e49373f08d379ffd0cdeec50c6ea384c078dbb4ffe3eff54ea3ad8` | 217094 |
| `reports/testing/generated/manifest/report-freshness.generated.md` | present | `831f55fb47076b2d5b78138dddabfe19fc19764f9fae5ff08981ed58c7829f10` | 25249 |
| `reports/testing/generated/manifest/report-path-migration.generated.json` | present | `5a55b747d6cc59f5a94a704f3d0c14a091c7f401f4ea2a73fee6d2be2c495a2c` | 18010 |
| `reports/testing/generated/manifest/report-path-migration.generated.md` | present | `af78e8fde6d11579b3c5d2ea3462b2909b40b5751533d73313e2b6d06297da4b` | 12447 |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | `496ed44753e03da8f4f121d0580c7bca5b3abc6338bcb5e7f9589339aee5fe53` | 238232 |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.md` | present | `208e4fa46f14cb8772f3d4063546906305384a3659453f74cfa3cda2cd4960c7` | 38197 |
| `reports/testing/generated/manifest/system-environment-proof.generated.json` | present | `267e83fbbafa1c25200c0686560dac73737c139954dd1cee5491955a0a3b65ca` | 70339 |
| `reports/testing/generated/manifest/system-environment-proof.generated.md` | present | `30d5ca4ff1811964c9e8a2ff7ae21a4dcca9385eec13ee13259a05c465d1a43b` | 15966 |
| `reports/testing/generated/manifest/verified-run-manifest.generated.json` | present | `3dfb45d9ee605ceb6c3e09d1ce9e52f96854a75b383ccf951011d933102677fa` | 257959 |
| `reports/testing/generated/manifest/verified-run-manifest.generated.md` | present | `c146e469754b0a0c5757cd2af9bb945a3428a6162500024e144279c88de5accd` | 41126 |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | `33b428edf7c204327a38506f46b745ab77c37335ee42909d9ec16dde1d02375a` | 2189630 |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | present | `7793a1ae08c5f74e14e1debd59c16c1cd213616ef65e19ab3ba95be70290a652` | 54273 |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | `9ccb5431764aac542ae1fcc02de342d814491d3930590ffad49889e2aa6b59f1` | 2747 |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | present | `a8633e8e841b90d730d9ebcb02730acc4fc7850c079dd93a26e45cfe25665250` | 2088 |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | present | `ef1782f5883aa61a97b31c773626890019504c3d39d259dd650fe10b43e64caf` | 2741 |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | present | `0f8c15d99cafe463c5c2b3ae2d0b231b826a7a39d5be3f7b812be80840bb0346` | 2090 |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | `7603d2d25d50d28601bf426cce70657faea786102d32340e705041dd0301ad94` | 2744 |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | present | `55aaab4c5b4c06862fa88267c0088b3afbc5a96f0688222e141dc4385f270fc8` | 2087 |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | present | `ec837bd41cd5d356213d325785e78ed7c08da8afbd62dc49609021c5d156fe6b` | 2750 |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | present | `44a0af41e18afc437e3eef2cc5337dd0b8505ef6fb9aafd602cd3d2aa464e647` | 2065 |
| `reports/testing/generated/runtime/apache-runtime-results.generated.md` | present | `d02d9f600385604b9139d8a7e50832ac0eafe4d50f605d1e593b4121c98e3fdc` | 65918 |
| `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | present | `41c2fc870163d1165ffec1a77d846c009d53f9a80c378424a53b72bab5106db3` | 67951 |
| `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | present | `f21dfc2d1be602668d7e9c400c19c16c4e5434459c7fd690d8350b7c9119b966` | 73981 |
| `reports/testing/generated/runtime/runtime-matrix.generated.md` | present | `0b6853474ac767101b15af4ceb1dbae06ba1ff6441ea50a28725ab69cb3b4d96` | 114084 |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | `683e6b8d49fd9dc2321e2547fff545e7773d304c0aec2e0f59fce00571f97e51` | 2669 |
| `reports/testing/generated/work-queues/connector-work-queue.generated.md` | present | `e044b85c8fd4ca9f14d8c593bf8095f4e1af58e12461fdff41ae09e2d1ead3b4` | 1820 |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | `5c41e4ab4a98cabef427230a0a9438cc9dad25c395c50ff3fc05e8f79e745cf8` | 4053 |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | `96aff1253a1edd79c962ddd1587fa49ab66e7254f39546d99c41ca74c3759e37` | 2709 |

## Missing / Skipped / Blocked / Failed

| Item | Status | Reason | Affected Reports |
|---|---|---|---|
| `native_mrts_reports` | skipped_stale_input | required generated input is stale | reports/testing/generated/mrts-native/mrts-native-full.generated.json, reports/testing/generated/mrts-native/mrts-native-full.generated.md, reports/testing/generated/mrts-native/mrts-native-apache.generated.json, reports/testing/generated/mrts-native/mrts-native-apache.generated.md, reports/testing/generated/mrts-native/mrts-native-nginx.generated.json, reports/testing/generated/mrts-native/mrts-native-nginx.generated.md, reports/testing/generated/mrts-native/mrts-native-summary.generated.json, reports/testing/generated/mrts-native/mrts-native-summary.generated.md |
| `full_runtime_matrix` | blocked_timeout | full-matrix-parallel timed out before producing complete verified evidence | reports/testing/generated/canonical/full-runtime-matrix.generated.json, reports/testing/generated/canonical/full-runtime-matrix.generated.md |
| `connector_work_queue` | blocked | required generated input is blocked | reports/testing/generated/work-queues/connector-work-queue.generated.json, reports/testing/generated/work-queues/connector-work-queue.generated.md |
| `phase_work_queue` | blocked | required generated input is blocked | reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `nolog_audit_evidence` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json, reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `response_header_hook_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json, reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `phase4_hard_abort_capability` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json, reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md, reports/testing/generated/work-queues/phase-work-queue.generated.json, reports/testing/generated/work-queues/phase-work-queue.generated.md |
| `remaining_failure_analysis` | blocked | required generated input is blocked | reports/testing/generated/canonical/remaining-failure-analysis.generated.json, reports/testing/generated/canonical/remaining-failure-analysis.generated.md, reports/testing/generated/canonical/next-fix-plan.generated.json, reports/testing/generated/canonical/next-fix-plan.generated.md, reports/testing/generated/canonical/full-run-evidence.generated.json, reports/testing/generated/canonical/full-run-evidence.generated.md |
| `intervention_blocking_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json, reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md |
| `no_mrts_intervention_nomatch_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json, reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md |
| `body_processor_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/body-processor-analysis.generated.json, reports/testing/generated/focused-analysis/body-processor-analysis.generated.md |
| `rule_chain_semantics_analysis` | blocked | required generated input is blocked | reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json, reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md |
| `final_consistency_audit` | blocked | required generated input is blocked | reports/testing/generated/canonical/final-consistency-audit.generated.json, reports/testing/generated/canonical/final-consistency-audit.generated.md |

## Tool Versions

| Tool | Status | Version / Output |
|---|---|---|
| git | present | `git version 2.53.0` |
| python3 | present | `Python 3.14.4` |
| python | present | `Python 3.14.4` |
| make | present | `GNU Make 4.4.1` |
| bash | present | `GNU bash, version 5.3.9(1)-release (x86_64-pc-linux-gnu)` |
| sh | present | `POSIX shell available (/usr/bin/dash)` |
| gcc | present | `gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0` |
| clang | present | `Ubuntu clang version 21.1.8 (6ubuntu1)` |
| go | present | `go version go1.26.0 linux/amd64` |
| go-ftw | missing | `command not found` |
| albedo | missing | `command not found` |
| actionlint | missing | `command not found` |
| jq | present | `jq-1.8.1` |
| curl | present | `curl 8.18.0 (x86_64-pc-linux-gnu) libcurl/8.18.0 OpenSSL/3.5.5 zlib/1.3.1 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.2 libssh2/1.11.1 nghttp2/1.68.0 librtmp/2.3 mit-krb5/1.22.1 OpenLDAP/2.6.10` |
| docker | missing | `command not found` |
| apachectl | missing | `no candidate found: apachectl` |
| apache/httpd | missing | `no candidate found: apache2 httpd apachectl` |
| nginx | missing | `no candidate found: nginx` |
| haproxy | configured_missing | `file not found` |
| apxs | missing | `no candidate found: apxs apxs2` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | `a351abf7f756d9bf30cb805bdc57e3e5830a456735d9a6307c3bf154ce75bab9` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | `496ed44753e03da8f4f121d0580c7bca5b3abc6338bcb5e7f9589339aee5fe53` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/system-environment-proof.generated.json` | `267e83fbbafa1c25200c0686560dac73737c139954dd1cee5491955a0a3b65ca` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `3b3387c0b99c427fe38858123d3d5743b979b484e74c83c7425fb71176321da6` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | input file available |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/system-environment-proof.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
