> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T17:47:41Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-matrix-job-completeness.py`
> Make target: `generate-full-matrix-job-completeness`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `f0e5bfc01bff0f25ff02c2b1e910edd00e2fd6a5`
> Framework SHA: `2334d31b942fd79770c7381b02fcaf031cccc4d2`
> Input status: `complete`

# Full-Matrix Job Completeness

Verified run id: `2026-06-16T19-12-00Z-614c8049`

## Summary

| Field | Value |
|---|---|
| Complete jobs | `12/12` |
| Manifest-recorded jobs | `12/12` |
| Overall status | `complete` |
| Evidence scope | `full` |
| Missing jobs | `-` |

## Jobs

| Job | Connector | CRS | MRTS | Status | Duration | Cases | Failures | Log |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `apache:no-crs:no-mrts` | apache | no-crs | no-mrts | `completed_with_mismatches` | 338 | 133 | 13 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` |
| `nginx:no-crs:no-mrts` | nginx | no-crs | no-mrts | `completed_with_mismatches` | 552 | 140 | 27 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` |
| `haproxy:no-crs:no-mrts` | haproxy | no-crs | no-mrts | `completed_with_mismatches` | 271 | 133 | 13 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` |
| `apache:no-crs:with-mrts` | apache | no-crs | with-mrts | `completed_with_mismatches` | 1291 | 516 | 108 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` |
| `nginx:no-crs:with-mrts` | nginx | no-crs | with-mrts | `completed_with_mismatches` | 3208 | 523 | 115 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` |
| `haproxy:no-crs:with-mrts` | haproxy | no-crs | with-mrts | `completed_with_mismatches` | 1049 | 516 | 108 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` |
| `apache:with-crs:no-mrts` | apache | with-crs | no-mrts | `completed_with_mismatches` | 365 | 134 | 13 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` |
| `nginx:with-crs:no-mrts` | nginx | with-crs | no-mrts | `completed_with_mismatches` | 609 | 141 | 27 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` |
| `haproxy:with-crs:no-mrts` | haproxy | with-crs | no-mrts | `completed_with_mismatches` | 309 | 134 | 14 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` |
| `apache:with-crs:with-mrts` | apache | with-crs | with-mrts | `completed_with_mismatches` | 1380 | 517 | 110 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` |
| `nginx:with-crs:with-mrts` | nginx | with-crs | with-mrts | `completed_with_mismatches` | 3439 | 524 | 117 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` |
| `haproxy:with-crs:with-mrts` | haproxy | with-crs | with-mrts | `completed_with_mismatches` | 1182 | 517 | 110 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` |

## Completed Jobs

| Job | Duration | RC | Failures |
| --- | ---: | -: | ---: |
| `apache:no-crs:no-mrts` | 338 | 2 | 13 |
| `nginx:no-crs:no-mrts` | 552 | 2 | 27 |
| `haproxy:no-crs:no-mrts` | 271 | 2 | 13 |
| `apache:no-crs:with-mrts` | 1291 | 2 | 108 |
| `nginx:no-crs:with-mrts` | 3208 | 2 | 115 |
| `haproxy:no-crs:with-mrts` | 1049 | 2 | 108 |
| `apache:with-crs:no-mrts` | 365 | 2 | 13 |
| `nginx:with-crs:no-mrts` | 609 | 2 | 27 |
| `haproxy:with-crs:no-mrts` | 309 | 2 | 14 |
| `apache:with-crs:with-mrts` | 1380 | 2 | 110 |
| `nginx:with-crs:with-mrts` | 3439 | 2 | 117 |
| `haproxy:with-crs:with-mrts` | 1182 | 2 | 110 |

## Missing / Timeout Jobs

Missing/Empty: no missing or timed-out Full-Matrix jobs.

## Slowest Jobs

| Job | Duration | Notes |
| --- | ---: | --- |
| `nginx:with-crs:with-mrts` | 3439 | job.json exists with rc=2 |
| `nginx:no-crs:with-mrts` | 3208 | job.json exists with rc=2 |
| `apache:with-crs:with-mrts` | 1380 | job.json exists with rc=2 |
| `apache:no-crs:with-mrts` | 1291 | job.json exists with rc=2 |
| `haproxy:with-crs:with-mrts` | 1182 | job.json exists with rc=2 |

## NGINX with-crs/with-mrts Runtime Analysis

- Last running case: `mrts_100156_mrts_110_xml_100156_1`
- Last failed case: `v3_transformation_trim_block`
- Run log lines: `7874`
- Running-case lines: `524`
- FAIL lines: `117`
- Observed 500 lines: `0`
- Terminated evidence: `false`
- Partial result rows: `524`

- The previous run was killed while NGINX with-crs/with-mrts was still executing MRTS request-cookie-name cases.
- The partial NGINX job produced result JSONL but no summary JSON and no job.json, so it cannot count as complete evidence.
- Observed failures are dominated by HTTP 500 responses in the NGINX harness for this variant.
- Current connector smoke runners expose TEST_CASE/SMOKE_CASES filters but no stable shard index contract for Full-Matrix merge semantics.

## Sharding Note

Add sharding at the case-list stage in connectors/*/harness/run_*_smoke.sh, after case_cli list-cases and before the force-all loop, then write shard metadata into job.json and merge shards in this report.

## Inputs

| Input | Status | SHA256 |
| --- | --- | --- |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `05187cad277e3352bbc54ba68260c25e3cad2001d726f43e765e00965ca324c4` |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | present | `de718c4d536eb8454dca743a17167482e4eb9ff6d335dac403fd19d647befb3c` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | present | `828d525fe23ba3f9b2c272c87f637459bfd4876edc0980f8ee95f015f75ec9b4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `00f16a615027b01044651ace2785621bfe46fbcb56aefda5b509c777a6060bee` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `1b65a535ebe72e87174dc370b811905ea296753c50eff9fd5371405829d0e9eb` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | `56b6c5431d3a33f554671543e3ece53df1faeec6262c4fd9091371c5cf45a254` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | `0ba72ccf47140e0a0f5f393ae82e6c27949d8e8628b9de2f00d12f32717b98db` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `ef9a0cae4f356eb87acbcd1d594da74f72ceb418d75cb5f10131bddc23ae7f03` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `c938c559d11624657a019a1190003be8c24a27dc5a7a6e2caf7e8d35c63b74d4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `37408eeb1625fe1e220bc6c9ae3b8cde1e960ba8e20c82d0a793148d2a1626ea` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | `1a1edf1ec82089883ffcc19d733bfd82ec32d71d56a3c30e5ed149c30af96274` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `88934b32904dbf58aa322c6c489a411737dc0c90fce9dc2fe433716b8ac3d7a0` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | present | `e993d3c2ccd8a28ad7dd2800a7ccd57eba130011df20ad058abd4088e70ae442` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | present | `26cbf55acb4727bb775a0098ed289339794077175be154ef2492008fdfd86fb7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `c33c6c8b8a6dd3e4ff26a5e4e45056e6b3a0cf5d01566048f5b842e95636af84` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `57ee33b9ec5d21e5391108c0767a23d7411c7f0b95d9b1daf17562ba64f31fb2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | `096f19caed90a5e0005a3f33ad5079857cc13904222d7e173a2cc11e03238c85` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | `eb3b58a8f609e69dabb9dbdb3231fa1285f418527680d33839600e9259709d7b` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `4b39d17d56c7f74c1a859c18f57e861233e46534512bb17275789d15e25bfa73` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `f978aef80fbfcc554f481e6c29201ae8b0b646c7924b24b5b722e74cd2cf7766` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `162f55c82fa86150d34ee852454dcd6d170b4f266fa5fe3d7e87d625a4ec7510` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | `51410e5b10332999808e34d5ba125289471b9a9c8c8602b06399eb51bb8c19cc` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `7f6978c3e76c7e44e6609e554d66086328ee401ada671adef1e1a32ba49e8a4b` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | present | `250286a546bec615a67601f04a49982e2e84b4ba622decd7e78fb8c48035a892` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | present | `089b821666908e40196b50e01d0547b41870a9bdb74c049ccc8d9e1cda5934ef` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `bad577ee975476ad4e188c904bf320015a9a19546174031cd16aa45f4b50603e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `9e910d7cfeb8fb42f8f0914fc3f130ad6d6e3b2325b858ecda8444150d4d8f3d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | `34813ea55e729ab5f6bdd796978a73c971244ff71546af3875ab857746ee5189` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | `f874c834f11c2e3c51616acd85a676849bb0db22bb46c9aee6a8da4c67d1d1fd` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `9afa8bcb0438ac9e436c22b2c9bae5900d99371bb2784e7e6e84b5dce8ad22bd` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `c55cc325773bf155377879ce2df79a153c1c40bdad2241dd0310e53a45a481ec` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `97946cb6194cffc9f992fdcfd5a1f3d6cca5e27c7f96a86c5976c415324286ca` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | `62c93f9e6210b9184438f6c3eae5038240767f1ac74f1c617fa4c4880577a4f1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `18b390115059d795246975499af920dd75b5de84a8d5349a9fd21e6f9e7fc89f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | present | `b539ba3655ba3d305984059fc29f326f8198e8e67f23fa0f77d89de1d0a3c1bb` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | present | `886ea3eed7fdafce0b10bd95d0b9a217492392e068739e061506decf2e13c4a6` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `9a364b71a33156bbd9fa33fdf19be58655d1842a976348a90e34da836809a6fc` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `00a2e4022ad6c75f965fc60d6331078d10aa829720f50ae9afe9920e3e382b2d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | `2fc84a6cd9a4167d2e21a1027e9db66a167a7a239ae8e7a5e9e960710123a13f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | `f4ed58499c55cb4dc826c0b5357487887c5011acfed9b0ca2d97c52440d95cff` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `26784a8ca26bfd9cc9d089218c56c315b5ffe5886db7554e0434d7aa7a4a52f3` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `fb879b5e327bc08626ca315cf8427d784c7532335b57a7f9ada714fcdcb8bcf7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `5a4cb91a12b83ae404a2f4a3d514a68dedf7108aab5dbe0d84225d3410c69fbd` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | `087bb0b8e1f11d74b0aad139591893f99f4348d89c2c9e0e17d63c0cbbf3fef8` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `a6641c40989fd073c5385a8f414545b8752589d1f50897770af8450432581112` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `05187cad277e3352bbc54ba68260c25e3cad2001d726f43e765e00965ca324c4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | `de718c4d536eb8454dca743a17167482e4eb9ff6d335dac403fd19d647befb3c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | `828d525fe23ba3f9b2c272c87f637459bfd4876edc0980f8ee95f015f75ec9b4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | `00f16a615027b01044651ace2785621bfe46fbcb56aefda5b509c777a6060bee` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `1b65a535ebe72e87174dc370b811905ea296753c50eff9fd5371405829d0e9eb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | `56b6c5431d3a33f554671543e3ece53df1faeec6262c4fd9091371c5cf45a254` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | `0ba72ccf47140e0a0f5f393ae82e6c27949d8e8628b9de2f00d12f32717b98db` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `ef9a0cae4f356eb87acbcd1d594da74f72ceb418d75cb5f10131bddc23ae7f03` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `c938c559d11624657a019a1190003be8c24a27dc5a7a6e2caf7e8d35c63b74d4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | `37408eeb1625fe1e220bc6c9ae3b8cde1e960ba8e20c82d0a793148d2a1626ea` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | `1a1edf1ec82089883ffcc19d733bfd82ec32d71d56a3c30e5ed149c30af96274` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | `88934b32904dbf58aa322c6c489a411737dc0c90fce9dc2fe433716b8ac3d7a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | `e993d3c2ccd8a28ad7dd2800a7ccd57eba130011df20ad058abd4088e70ae442` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | `26cbf55acb4727bb775a0098ed289339794077175be154ef2492008fdfd86fb7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | `c33c6c8b8a6dd3e4ff26a5e4e45056e6b3a0cf5d01566048f5b842e95636af84` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `57ee33b9ec5d21e5391108c0767a23d7411c7f0b95d9b1daf17562ba64f31fb2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | `096f19caed90a5e0005a3f33ad5079857cc13904222d7e173a2cc11e03238c85` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | `eb3b58a8f609e69dabb9dbdb3231fa1285f418527680d33839600e9259709d7b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `4b39d17d56c7f74c1a859c18f57e861233e46534512bb17275789d15e25bfa73` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `f978aef80fbfcc554f481e6c29201ae8b0b646c7924b24b5b722e74cd2cf7766` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | `162f55c82fa86150d34ee852454dcd6d170b4f266fa5fe3d7e87d625a4ec7510` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | `51410e5b10332999808e34d5ba125289471b9a9c8c8602b06399eb51bb8c19cc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | `7f6978c3e76c7e44e6609e554d66086328ee401ada671adef1e1a32ba49e8a4b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | `250286a546bec615a67601f04a49982e2e84b4ba622decd7e78fb8c48035a892` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | `089b821666908e40196b50e01d0547b41870a9bdb74c049ccc8d9e1cda5934ef` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | `bad577ee975476ad4e188c904bf320015a9a19546174031cd16aa45f4b50603e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `9e910d7cfeb8fb42f8f0914fc3f130ad6d6e3b2325b858ecda8444150d4d8f3d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | `34813ea55e729ab5f6bdd796978a73c971244ff71546af3875ab857746ee5189` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | `f874c834f11c2e3c51616acd85a676849bb0db22bb46c9aee6a8da4c67d1d1fd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `9afa8bcb0438ac9e436c22b2c9bae5900d99371bb2784e7e6e84b5dce8ad22bd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `c55cc325773bf155377879ce2df79a153c1c40bdad2241dd0310e53a45a481ec` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | `97946cb6194cffc9f992fdcfd5a1f3d6cca5e27c7f96a86c5976c415324286ca` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | `62c93f9e6210b9184438f6c3eae5038240767f1ac74f1c617fa4c4880577a4f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | `18b390115059d795246975499af920dd75b5de84a8d5349a9fd21e6f9e7fc89f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | `b539ba3655ba3d305984059fc29f326f8198e8e67f23fa0f77d89de1d0a3c1bb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | `886ea3eed7fdafce0b10bd95d0b9a217492392e068739e061506decf2e13c4a6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | `9a364b71a33156bbd9fa33fdf19be58655d1842a976348a90e34da836809a6fc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `00a2e4022ad6c75f965fc60d6331078d10aa829720f50ae9afe9920e3e382b2d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `2fc84a6cd9a4167d2e21a1027e9db66a167a7a239ae8e7a5e9e960710123a13f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `f4ed58499c55cb4dc826c0b5357487887c5011acfed9b0ca2d97c52440d95cff` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `26784a8ca26bfd9cc9d089218c56c315b5ffe5886db7554e0434d7aa7a4a52f3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `fb879b5e327bc08626ca315cf8427d784c7532335b57a7f9ada714fcdcb8bcf7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | `5a4cb91a12b83ae404a2f4a3d514a68dedf7108aab5dbe0d84225d3410c69fbd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | `087bb0b8e1f11d74b0aad139591893f99f4348d89c2c9e0e17d63c0cbbf3fef8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | `a6641c40989fd073c5385a8f414545b8752589d1f50897770af8450432581112` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | input file available |
