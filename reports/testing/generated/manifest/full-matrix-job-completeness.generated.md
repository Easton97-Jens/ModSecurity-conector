> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:43:21Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-matrix-job-completeness.py`
> Make target: `generate-full-matrix-job-completeness`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
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
| `apache:no-crs:no-mrts` | apache | no-crs | no-mrts | `completed_with_mismatches` | 336 | 133 | 12 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` |
| `nginx:no-crs:no-mrts` | nginx | no-crs | no-mrts | `completed_with_mismatches` | 551 | 140 | 26 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` |
| `haproxy:no-crs:no-mrts` | haproxy | no-crs | no-mrts | `completed_with_mismatches` | 266 | 133 | 12 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` |
| `apache:no-crs:with-mrts` | apache | no-crs | with-mrts | `completed_with_mismatches` | 1296 | 516 | 109 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` |
| `nginx:no-crs:with-mrts` | nginx | no-crs | with-mrts | `completed_with_mismatches` | 3212 | 523 | 116 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` |
| `haproxy:no-crs:with-mrts` | haproxy | no-crs | with-mrts | `completed_with_mismatches` | 1042 | 516 | 109 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` |
| `apache:with-crs:no-mrts` | apache | with-crs | no-mrts | `completed_with_mismatches` | 367 | 134 | 12 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` |
| `nginx:with-crs:no-mrts` | nginx | with-crs | no-mrts | `completed_with_mismatches` | 613 | 141 | 26 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` |
| `haproxy:with-crs:no-mrts` | haproxy | with-crs | no-mrts | `completed_with_mismatches` | 301 | 134 | 12 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` |
| `apache:with-crs:with-mrts` | apache | with-crs | with-mrts | `completed_with_mismatches` | 1388 | 517 | 111 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` |
| `nginx:with-crs:with-mrts` | nginx | with-crs | with-mrts | `completed_with_mismatches` | 3437 | 524 | 118 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` |
| `haproxy:with-crs:with-mrts` | haproxy | with-crs | with-mrts | `completed_with_mismatches` | 1183 | 517 | 111 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` |

## Completed Jobs

| Job | Duration | RC | Failures |
| --- | ---: | -: | ---: |
| `apache:no-crs:no-mrts` | 336 | 2 | 12 |
| `nginx:no-crs:no-mrts` | 551 | 2 | 26 |
| `haproxy:no-crs:no-mrts` | 266 | 2 | 12 |
| `apache:no-crs:with-mrts` | 1296 | 2 | 109 |
| `nginx:no-crs:with-mrts` | 3212 | 2 | 116 |
| `haproxy:no-crs:with-mrts` | 1042 | 2 | 109 |
| `apache:with-crs:no-mrts` | 367 | 2 | 12 |
| `nginx:with-crs:no-mrts` | 613 | 2 | 26 |
| `haproxy:with-crs:no-mrts` | 301 | 2 | 12 |
| `apache:with-crs:with-mrts` | 1388 | 2 | 111 |
| `nginx:with-crs:with-mrts` | 3437 | 2 | 118 |
| `haproxy:with-crs:with-mrts` | 1183 | 2 | 111 |

## Missing / Timeout Jobs

Missing/Empty: no missing or timed-out Full-Matrix jobs.

## Slowest Jobs

| Job | Duration | Notes |
| --- | ---: | --- |
| `nginx:with-crs:with-mrts` | 3437 | job.json exists with rc=2 |
| `nginx:no-crs:with-mrts` | 3212 | job.json exists with rc=2 |
| `apache:with-crs:with-mrts` | 1388 | job.json exists with rc=2 |
| `apache:no-crs:with-mrts` | 1296 | job.json exists with rc=2 |
| `haproxy:with-crs:with-mrts` | 1183 | job.json exists with rc=2 |

## NGINX with-crs/with-mrts Runtime Analysis

- Last running case: `mrts_100156_mrts_110_xml_100156_1`
- Last failed case: `v3_transformation_trim_block`
- Run log lines: `7874`
- Running-case lines: `524`
- FAIL lines: `118`
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
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `fada5d0fadca101488838264f9845932d6c5c1e889a73f7e728d5047efed2011` |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | present | `f15767d79fbcbf0a3ccdbac91d5e60def2afdd860fcb1d26a68966e28ba915af` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | present | `ace154664a76f2f7c60f0056f9e7973c959aa37b55ce4832f5c674bde32a4c16` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `04734a3ae2aaa47b49312b14dcc71ea6bcee783ca2c5508a41bc245761e1abf8` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `1f539b3ddcdd2d312365da7e566732530a9c2ef31f2451cea809bf91e18d2954` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | `4258dc7376d7fd7a0fe5437bc964b8c4ef35dd370ca8008ad00fead0c84f537f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | `8b5e2116ed5d661fbd144c187a94d89aa726b830b38e8d032560edb7a455d4b3` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `72b4115b0147eb477a38d2b0a23d7f735a5602bdf47ad22d9570fe75f8b92216` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `78015092c8cdcabe864955b4b5cd766fb22cbebc04214c2e5ed5d44c6ce477f0` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `072de7cc3d1669021a55169a22ede612da6369d4f2c26407c516424fe528ef76` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | `d9139ccb5020ffa3b8f36c2c6c495ae5ee63b2e39e4d54c3e24c1229c45a9be5` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `4c0a7cd49fcb2998e284a41f5b980d2e18f189af6518c12ae2a229a88c55678b` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | present | `b4f3143c705468bf8de3d37b9981fd937fc8ebdc6bcac335fc68e941745243dd` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | present | `8fd8f799fcad4158b823a0fc5a853bf54bd9f7a60563a1d2cddcd90d52e47faa` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `328ab24e97e6d5891a99cda747bdcc4aeda05f1a6cf22c43af2f4c17609fcaaa` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `e7cecb1e4baa8d7b2760c1cb456c1b849ebe65dbe79a50916be7dc7a60e3c836` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | `a671bef53d954c03975b34e6d7bb8c87787fa2e0a86e2fe9fd05d702523e8890` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | `4c41bd972759e89bb361717c0460e49d4a4ea147296f15225101ad106c56a0f5` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `898101ba678afb4a5e7c1b696ad52842946f96da8c6225481acb017cca1c8e09` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `e8ce34e8dee229fd0478c6c2e982b191b8185f55cdabd9687c528e0ad0286e2f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `2178d65b5262024bb4ac6e7346eeeebef4ccc09e8c0bd2fc38a80aaf5417266d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | `186383ac9e4bb6cd445fb31fde3d71246e50e540cbd658333780da424ad02843` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `7fd2daa0563b88151ee1c449d3a6fd6a320f518a2ebc869ae45a9554607001a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | present | `09b003f3960bcc9b34422f15ed0852ae411af7958b8587f4c8b1db8f63d8dfaf` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | present | `86fe24c7efe9b6c298a90e968e82ee10197897941e15eff5a51d58aaab920c1c` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `c7512b6b6c2d880983c49e45a84bcc9c5cb08af08b0dd1d1b210a998d2144ee8` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `0cc2482790777ee27268cc02c0587aba6eb34e3ea83db6317a238ed3d7a4f744` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | `ff37e9c98de16fbf11d4b6ba7401caa6dda42d52646f405dc39d6e9aebeaec91` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | `4918463264d04a5e52ae5a185ee3e2991cfd90932c377feaad8db0610ce0cdb2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `8d5b8c841aed71dbee678d53125c2e10e8ed132d0cc468d1e9d2f44a527ff9b3` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `1cfc956a5b293dedf768903221890c921e4bbc6cbb53664582672c257f399684` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `cec350319ac91b03605a189b2c5613c47e9a732205daf9618ab8653ee85c28b5` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | `44c5896a0ef1603af467b714076038d6c67be5ff74d2b5737efbc86e76320430` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `bf78cbc8302c3039960cb3c5f66ef9f6c41d1aac9632357b85708e9261ee09f2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | present | `ef6adebbec71fb28c20cc7e0aa774ce69b6134d642e083937c3ad6e05085e711` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | present | `972c3f6afc757e1d2f6f5383124c9639ae91318cfeb91d855dc5c5cfc5f35546` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `298825ae37e70ade53f725e230592159acd37a143d06249de6fba7ef82110c79` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `00bd0ab1789730f937c549bfd11c4df809460e34e29cdf3073690d7433ac166b` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | `79d08ce77343c7ae1e3443bf38fb44e5341b1fa0586ca5ed9cbd69b5de8271bd` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | `79114cad6b8c729beaae429b29d4caa467f5ce686a7cd78d7ba9d1dbd7a7c140` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `ebf9c0111b63f4ccb349e5c4ec1960702ec9e9c5ac53ab70153f60616341aa3d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `8d05493d1747a79de336faf3347245881ef226b7f9587038d945ff048c9b2a5a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `613dcc0f07c1469b82338799bad839a2973b3cc205ec326430052ab4ae0253e2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | `634606d8061ae01aacc6d0e81d3da6d00e865df0db6c36e5528fad49738afb72` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `c9e8a6c20d5e510a574f6f49f1e0c215299b8fec8264c4d3acef23d5bc982699` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `fada5d0fadca101488838264f9845932d6c5c1e889a73f7e728d5047efed2011` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | `f15767d79fbcbf0a3ccdbac91d5e60def2afdd860fcb1d26a68966e28ba915af` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | `ace154664a76f2f7c60f0056f9e7973c959aa37b55ce4832f5c674bde32a4c16` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | `04734a3ae2aaa47b49312b14dcc71ea6bcee783ca2c5508a41bc245761e1abf8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `1f539b3ddcdd2d312365da7e566732530a9c2ef31f2451cea809bf91e18d2954` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | `4258dc7376d7fd7a0fe5437bc964b8c4ef35dd370ca8008ad00fead0c84f537f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | `8b5e2116ed5d661fbd144c187a94d89aa726b830b38e8d032560edb7a455d4b3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `72b4115b0147eb477a38d2b0a23d7f735a5602bdf47ad22d9570fe75f8b92216` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `78015092c8cdcabe864955b4b5cd766fb22cbebc04214c2e5ed5d44c6ce477f0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | `072de7cc3d1669021a55169a22ede612da6369d4f2c26407c516424fe528ef76` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | `d9139ccb5020ffa3b8f36c2c6c495ae5ee63b2e39e4d54c3e24c1229c45a9be5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | `4c0a7cd49fcb2998e284a41f5b980d2e18f189af6518c12ae2a229a88c55678b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | `b4f3143c705468bf8de3d37b9981fd937fc8ebdc6bcac335fc68e941745243dd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | `8fd8f799fcad4158b823a0fc5a853bf54bd9f7a60563a1d2cddcd90d52e47faa` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | `328ab24e97e6d5891a99cda747bdcc4aeda05f1a6cf22c43af2f4c17609fcaaa` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `e7cecb1e4baa8d7b2760c1cb456c1b849ebe65dbe79a50916be7dc7a60e3c836` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | `a671bef53d954c03975b34e6d7bb8c87787fa2e0a86e2fe9fd05d702523e8890` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | `4c41bd972759e89bb361717c0460e49d4a4ea147296f15225101ad106c56a0f5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `898101ba678afb4a5e7c1b696ad52842946f96da8c6225481acb017cca1c8e09` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `e8ce34e8dee229fd0478c6c2e982b191b8185f55cdabd9687c528e0ad0286e2f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | `2178d65b5262024bb4ac6e7346eeeebef4ccc09e8c0bd2fc38a80aaf5417266d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | `186383ac9e4bb6cd445fb31fde3d71246e50e540cbd658333780da424ad02843` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | `7fd2daa0563b88151ee1c449d3a6fd6a320f518a2ebc869ae45a9554607001a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | `09b003f3960bcc9b34422f15ed0852ae411af7958b8587f4c8b1db8f63d8dfaf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | `86fe24c7efe9b6c298a90e968e82ee10197897941e15eff5a51d58aaab920c1c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | `c7512b6b6c2d880983c49e45a84bcc9c5cb08af08b0dd1d1b210a998d2144ee8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `0cc2482790777ee27268cc02c0587aba6eb34e3ea83db6317a238ed3d7a4f744` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | `ff37e9c98de16fbf11d4b6ba7401caa6dda42d52646f405dc39d6e9aebeaec91` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | `4918463264d04a5e52ae5a185ee3e2991cfd90932c377feaad8db0610ce0cdb2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `8d5b8c841aed71dbee678d53125c2e10e8ed132d0cc468d1e9d2f44a527ff9b3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `1cfc956a5b293dedf768903221890c921e4bbc6cbb53664582672c257f399684` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | `cec350319ac91b03605a189b2c5613c47e9a732205daf9618ab8653ee85c28b5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | `44c5896a0ef1603af467b714076038d6c67be5ff74d2b5737efbc86e76320430` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | `bf78cbc8302c3039960cb3c5f66ef9f6c41d1aac9632357b85708e9261ee09f2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | `ef6adebbec71fb28c20cc7e0aa774ce69b6134d642e083937c3ad6e05085e711` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | `972c3f6afc757e1d2f6f5383124c9639ae91318cfeb91d855dc5c5cfc5f35546` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | `298825ae37e70ade53f725e230592159acd37a143d06249de6fba7ef82110c79` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `00bd0ab1789730f937c549bfd11c4df809460e34e29cdf3073690d7433ac166b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `79d08ce77343c7ae1e3443bf38fb44e5341b1fa0586ca5ed9cbd69b5de8271bd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `79114cad6b8c729beaae429b29d4caa467f5ce686a7cd78d7ba9d1dbd7a7c140` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `ebf9c0111b63f4ccb349e5c4ec1960702ec9e9c5ac53ab70153f60616341aa3d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `8d05493d1747a79de336faf3347245881ef226b7f9587038d945ff048c9b2a5a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | `613dcc0f07c1469b82338799bad839a2973b3cc205ec326430052ab4ae0253e2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | `634606d8061ae01aacc6d0e81d3da6d00e865df0db6c36e5528fad49738afb72` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | `c9e8a6c20d5e510a574f6f49f1e0c215299b8fec8264c4d3acef23d5bc982699` | `2026-06-16T19-12-00Z-614c8049` | present |
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
