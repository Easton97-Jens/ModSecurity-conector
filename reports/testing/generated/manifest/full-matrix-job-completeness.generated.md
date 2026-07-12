> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:57:57Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-matrix-job-completeness.py`
> Make target: `generate-full-matrix-job-completeness`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

<!-- retained-historical-generated-output -->
> Current refresh status: `skipped_missing_input`. This report retains an earlier evidence-bearing snapshot because no newer verified inputs are available. Reason: required input missing or empty.

# Full-Matrix Job Completeness

**Language:** English | [Deutsch](full-matrix-job-completeness.generated.de.md)

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
| `apache:no-crs:no-mrts` | apache | no-crs | no-mrts | `completed_with_mismatches` | 342 | 133 | 11 | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/run.log` |
| `nginx:no-crs:no-mrts` | nginx | no-crs | no-mrts | `completed_with_mismatches` | 577 | 140 | 25 | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/run.log` |
| `haproxy:no-crs:no-mrts` | haproxy | no-crs | no-mrts | `completed_with_mismatches` | 278 | 133 | 11 | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/run.log` |
| `apache:no-crs:with-mrts` | apache | no-crs | with-mrts | `completed_with_mismatches` | 1314 | 516 | 109 | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/run.log` |
| `nginx:no-crs:with-mrts` | nginx | no-crs | with-mrts | `completed_with_mismatches` | 3358 | 523 | 116 | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/run.log` |
| `haproxy:no-crs:with-mrts` | haproxy | no-crs | with-mrts | `completed_with_mismatches` | 1090 | 516 | 109 | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/run.log` |
| `apache:with-crs:no-mrts` | apache | with-crs | no-mrts | `completed_with_mismatches` | 366 | 134 | 12 | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/run.log` |
| `nginx:with-crs:no-mrts` | nginx | with-crs | no-mrts | `completed_with_mismatches` | 641 | 141 | 26 | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/run.log` |
| `haproxy:with-crs:no-mrts` | haproxy | with-crs | no-mrts | `completed_with_mismatches` | 312 | 134 | 12 | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/run.log` |
| `apache:with-crs:with-mrts` | apache | with-crs | with-mrts | `completed_with_mismatches` | 1423 | 517 | 111 | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/run.log` |
| `nginx:with-crs:with-mrts` | nginx | with-crs | with-mrts | `completed_with_mismatches` | 3594 | 524 | 118 | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/run.log` |
| `haproxy:with-crs:with-mrts` | haproxy | with-crs | with-mrts | `completed_with_mismatches` | 1225 | 517 | 111 | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/run.log` |

## Completed Jobs

| Job | Duration | RC | Failures |
| --- | ---: | -: | ---: |
| `apache:no-crs:no-mrts` | 342 | 2 | 11 |
| `nginx:no-crs:no-mrts` | 577 | 2 | 25 |
| `haproxy:no-crs:no-mrts` | 278 | 2 | 11 |
| `apache:no-crs:with-mrts` | 1314 | 2 | 109 |
| `nginx:no-crs:with-mrts` | 3358 | 2 | 116 |
| `haproxy:no-crs:with-mrts` | 1090 | 2 | 109 |
| `apache:with-crs:no-mrts` | 366 | 2 | 12 |
| `nginx:with-crs:no-mrts` | 641 | 2 | 26 |
| `haproxy:with-crs:no-mrts` | 312 | 2 | 12 |
| `apache:with-crs:with-mrts` | 1423 | 2 | 111 |
| `nginx:with-crs:with-mrts` | 3594 | 2 | 118 |
| `haproxy:with-crs:with-mrts` | 1225 | 2 | 111 |

## Missing / Timeout Jobs

Missing/Empty: no missing or timed-out Full-Matrix jobs.

## Slowest Jobs

| Job | Duration | Notes |
| --- | ---: | --- |
| `nginx:with-crs:with-mrts` | 3594 | job.json exists with rc=2 |
| `nginx:no-crs:with-mrts` | 3358 | job.json exists with rc=2 |
| `apache:with-crs:with-mrts` | 1423 | job.json exists with rc=2 |
| `apache:no-crs:with-mrts` | 1314 | job.json exists with rc=2 |
| `haproxy:with-crs:with-mrts` | 1225 | job.json exists with rc=2 |

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
| `<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `bca8c97edc4f6d5bab304488e596af2a047b9f5f17994cf72ef64ae748430ff8` |
| `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/job.json` | present | `f8bffca462db3c5a1d3c5b81c5a88f5b70c46f35fc99587286ddd5a65549b4df` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/run.log` | present | `0c83f141005f637e31ccb46dd125689201ba17c855572c227ee246e3e6bb1eb1` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `1717c2a630321e9b7bf04cadd161eac0c164673442e843c2bd291994f0a1038c` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `a4a24dae01fe67ef518c454e28b44d6dc4637a93abe9f3dbc2818d88d78dda01` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | `09e92d3abe673f36fbbd9d1ab074bece42f3b6332c9a4af25f49cd517874ab98` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | `f28ee3f648a252c2cc889be82334dca4456369c6c7d02fbd7396ab3bba6f11bb` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `949e28d7142459e86e0cb9ec1fad12b8b7172a5681039421e4075087d6c3de82` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `873569b1fc4f62ceee4634ff017cfd2b72d79f704d9d75dcef7ee6a70c22e9a0` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `6501d8a6129791e465f0b1daf80e607660bb34bff4556a73cf0b703589b88d86` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | `3acb0d0b7bfdc46d706bd0d02f199d7c4bf97b0d9516125bdd681c638ff476af` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `d20599aa223dad587761dd10551cb44fdbc00b83165baa7071c8d159ecc1ea04` |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/job.json` | present | `584d8dde6a59bc69d94b22e04f1da8e402518147c69fdd50bda014acef86176c` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/run.log` | present | `d7c06a31e7d641c4b6fb843eefdef7a4e2051f584282b8627ff6b770d9f62e16` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `0a7ac7b47460d1aece31e5a5cce68ff254229b0d8da71644dd06d92739113aa6` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `f6c70563811a84ec2db3bcdf880d33707e1df6e24a658ecfc0dd1a2a0d026f8d` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | `9907a077c02ecffbc5dcbbe75d0b436b054ad78fbd63eec69e8c3a8770380ecb` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | `7878b4c5671e2b3312d229cc4543d489fddd61a334e59fdbb7bde0f214a28975` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `213018f411175c07f783a4ab48618a52e54b07f2be1d36543a18096b3c6013ef` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `c0e4b73ef686300b798f275107aec12effe78c3a37988e68b273aad2f712fa92` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `8021999a36c6bf0610fd461bd6086cfd319b9ac980d6f2f4c9edee56fb93c428` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | `5c7b541226a793748c7b20d4912051e35e245edab23e89df18421311ca90f0a6` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `af1020b64ee7d12bd6580aafa92e5182aaacaf27dd8599991cfdf6cf161deabe` |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/job.json` | present | `dcfb59e5b34b9c291d2f1fd351c0c9d5607731454c0e7a6b683dc2c58ad0e1ef` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/run.log` | present | `ecba0eb3f85a8dff74503396a2a98ae80ebcf883bc434a1ab5ca6c73b7aaef2f` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `2ad3431b993b3b1bd376f883bf7e4e92a69190a88685056a58dd8072e1ed181e` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `f37761021c8ea8d67946447747872986d6b989a5f0f7d8782fdbc236d06cd40b` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | `3f5477e56a55a0eb4b7c92f5130827663cd70b02eb7c25473358a4a86b299389` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | `5a818a6aaf6a36d9c8cfabc4f84e26061099a93eb61ebcb3abfb237d727fae60` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `fd4de70202d5780055fc4d4ad076133078c876970cf21cf54023d18139dd9fa4` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `395d5e37d1e4eb399ef70b4e40a177099d6f3ab9ed4fde6eabe335c225fa47c5` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `8f3880a92a2c1da5e5da89b7e2852afa352275aabce7d81c04c32452cb4c8af2` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | `076445da559da9eb12ecc8fffbfca94ddc50d8c320e911d07a92156cc032cde6` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `af547bfca06e171781dee73eb432942ce47189d9ab8363fa7c694ed0cd994fda` |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/job.json` | present | `356705da0cb5d8ed3875892b11dd0bad7348567bcdf594ef7728ba1647e1da37` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/run.log` | present | `d252b109e43132a958fb156383f829de466533a20033a557813bbd0187cae06d` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `6f93aac6466c0e301e3bd6dfc3c4bbab4f5955ec884cd28eb28ba6821ab1ba0a` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `cbc919308386ba096dbcd76d0a244074c682d260ce3d0c20f8c93a47adbb1a62` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | `31606405e016d20afb67ce650aaf098b8194133d87869846344929e74c70b8f9` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | `d1425a9d5db6ec05270dd7292078437ab1ffd4981efdaadc8b1bf9da902e621f` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `efc447466ad8121a9316477b087e74a7155148082320a9cd57805aa3327f675e` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `59dd481e19225c369952c566eca3981cb002c7050b699ee45be6dfdbef2d2603` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `be7a1c00e16a92fa3a6d3e9ec4b878df8fa9fdb008e423e301cc704e66734739` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | `444d43f98e73086ef4743f2975eca3dc248c178f237d8e3bc3a008d843405b09` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `1ff741bf7a50983b1d2e403206f2a75ba4cc21e43a45b0dd530f49cd3b344f46` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | `bca8c97edc4f6d5bab304488e596af2a047b9f5f17994cf72ef64ae748430ff8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/job.json` | `f8bffca462db3c5a1d3c5b81c5a88f5b70c46f35fc99587286ddd5a65549b4df` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/run.log` | `0c83f141005f637e31ccb46dd125689201ba17c855572c227ee246e3e6bb1eb1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | `1717c2a630321e9b7bf04cadd161eac0c164673442e843c2bd291994f0a1038c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `a4a24dae01fe67ef518c454e28b44d6dc4637a93abe9f3dbc2818d88d78dda01` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/job.json` | `09e92d3abe673f36fbbd9d1ab074bece42f3b6332c9a4af25f49cd517874ab98` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/run.log` | `f28ee3f648a252c2cc889be82334dca4456369c6c7d02fbd7396ab3bba6f11bb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `949e28d7142459e86e0cb9ec1fad12b8b7172a5681039421e4075087d6c3de82` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `873569b1fc4f62ceee4634ff017cfd2b72d79f704d9d75dcef7ee6a70c22e9a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | `6501d8a6129791e465f0b1daf80e607660bb34bff4556a73cf0b703589b88d86` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | `3acb0d0b7bfdc46d706bd0d02f199d7c4bf97b0d9516125bdd681c638ff476af` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | `d20599aa223dad587761dd10551cb44fdbc00b83165baa7071c8d159ecc1ea04` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/job.json` | `584d8dde6a59bc69d94b22e04f1da8e402518147c69fdd50bda014acef86176c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/run.log` | `d7c06a31e7d641c4b6fb843eefdef7a4e2051f584282b8627ff6b770d9f62e16` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | `0a7ac7b47460d1aece31e5a5cce68ff254229b0d8da71644dd06d92739113aa6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `f6c70563811a84ec2db3bcdf880d33707e1df6e24a658ecfc0dd1a2a0d026f8d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/job.json` | `9907a077c02ecffbc5dcbbe75d0b436b054ad78fbd63eec69e8c3a8770380ecb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/run.log` | `7878b4c5671e2b3312d229cc4543d489fddd61a334e59fdbb7bde0f214a28975` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `213018f411175c07f783a4ab48618a52e54b07f2be1d36543a18096b3c6013ef` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `c0e4b73ef686300b798f275107aec12effe78c3a37988e68b273aad2f712fa92` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | `8021999a36c6bf0610fd461bd6086cfd319b9ac980d6f2f4c9edee56fb93c428` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | `5c7b541226a793748c7b20d4912051e35e245edab23e89df18421311ca90f0a6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | `af1020b64ee7d12bd6580aafa92e5182aaacaf27dd8599991cfdf6cf161deabe` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/job.json` | `dcfb59e5b34b9c291d2f1fd351c0c9d5607731454c0e7a6b683dc2c58ad0e1ef` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/run.log` | `ecba0eb3f85a8dff74503396a2a98ae80ebcf883bc434a1ab5ca6c73b7aaef2f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | `2ad3431b993b3b1bd376f883bf7e4e92a69190a88685056a58dd8072e1ed181e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `f37761021c8ea8d67946447747872986d6b989a5f0f7d8782fdbc236d06cd40b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/job.json` | `3f5477e56a55a0eb4b7c92f5130827663cd70b02eb7c25473358a4a86b299389` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/run.log` | `5a818a6aaf6a36d9c8cfabc4f84e26061099a93eb61ebcb3abfb237d727fae60` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `fd4de70202d5780055fc4d4ad076133078c876970cf21cf54023d18139dd9fa4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `395d5e37d1e4eb399ef70b4e40a177099d6f3ab9ed4fde6eabe335c225fa47c5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | `8f3880a92a2c1da5e5da89b7e2852afa352275aabce7d81c04c32452cb4c8af2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | `076445da559da9eb12ecc8fffbfca94ddc50d8c320e911d07a92156cc032cde6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | `af547bfca06e171781dee73eb432942ce47189d9ab8363fa7c694ed0cd994fda` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/job.json` | `356705da0cb5d8ed3875892b11dd0bad7348567bcdf594ef7728ba1647e1da37` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/run.log` | `d252b109e43132a958fb156383f829de466533a20033a557813bbd0187cae06d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | `6f93aac6466c0e301e3bd6dfc3c4bbab4f5955ec884cd28eb28ba6821ab1ba0a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `cbc919308386ba096dbcd76d0a244074c682d260ce3d0c20f8c93a47adbb1a62` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `31606405e016d20afb67ce650aaf098b8194133d87869846344929e74c70b8f9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `d1425a9d5db6ec05270dd7292078437ab1ffd4981efdaadc8b1bf9da902e621f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `efc447466ad8121a9316477b087e74a7155148082320a9cd57805aa3327f675e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `59dd481e19225c369952c566eca3981cb002c7050b699ee45be6dfdbef2d2603` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | `be7a1c00e16a92fa3a6d3e9ec4b878df8fa9fdb008e423e301cc704e66734739` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | `444d43f98e73086ef4743f2975eca3dc248c178f237d8e3bc3a008d843405b09` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | `1ff741bf7a50983b1d2e403206f2a75ba4cc21e43a45b0dd530f49cd3b344f46` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
| `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | input file available |
| `<verified-run-root>/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | input file available |
