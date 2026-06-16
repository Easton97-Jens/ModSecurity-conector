> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:58:18Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-matrix-job-completeness.py`
> Make target: `generate-full-matrix-job-completeness`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
> Input status: `complete`

# Full-Matrix Job Completeness

Verified run id: `2026-06-16T16-57-44Z-b53340a8`

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
| `apache:no-crs:no-mrts` | apache | no-crs | no-mrts | `completed_with_mismatches` | 353 | 133 | 19 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` |
| `nginx:no-crs:no-mrts` | nginx | no-crs | no-mrts | `completed_with_mismatches` | 512 | 140 | 31 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` |
| `haproxy:no-crs:no-mrts` | haproxy | no-crs | no-mrts | `completed_with_mismatches` | 0 | 0 | 0 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` |
| `apache:no-crs:with-mrts` | apache | no-crs | with-mrts | `completed_with_mismatches` | 1368 | 516 | 104 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` |
| `nginx:no-crs:with-mrts` | nginx | no-crs | with-mrts | `completed_with_mismatches` | 2538 | 523 | 111 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` |
| `haproxy:no-crs:with-mrts` | haproxy | no-crs | with-mrts | `completed_with_mismatches` | 1 | 0 | 0 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` |
| `apache:with-crs:no-mrts` | apache | with-crs | no-mrts | `completed_with_mismatches` | 376 | 134 | 19 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` |
| `nginx:with-crs:no-mrts` | nginx | with-crs | no-mrts | `completed_with_mismatches` | 573 | 141 | 31 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` |
| `haproxy:with-crs:no-mrts` | haproxy | with-crs | no-mrts | `completed_with_mismatches` | 0 | 0 | 0 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` |
| `apache:with-crs:with-mrts` | apache | with-crs | with-mrts | `completed_with_mismatches` | 1469 | 517 | 106 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` |
| `nginx:with-crs:with-mrts` | nginx | with-crs | with-mrts | `completed_with_mismatches` | 2771 | 524 | 113 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` |
| `haproxy:with-crs:with-mrts` | haproxy | with-crs | with-mrts | `completed_with_mismatches` | 0 | 0 | 0 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` |

## Completed Jobs

| Job | Duration | RC | Failures |
| --- | ---: | -: | ---: |
| `apache:no-crs:no-mrts` | 353 | 2 | 19 |
| `nginx:no-crs:no-mrts` | 512 | 2 | 31 |
| `haproxy:no-crs:no-mrts` | 0 | 2 | 0 |
| `apache:no-crs:with-mrts` | 1368 | 2 | 104 |
| `nginx:no-crs:with-mrts` | 2538 | 2 | 111 |
| `haproxy:no-crs:with-mrts` | 1 | 2 | 0 |
| `apache:with-crs:no-mrts` | 376 | 2 | 19 |
| `nginx:with-crs:no-mrts` | 573 | 2 | 31 |
| `haproxy:with-crs:no-mrts` | 0 | 2 | 0 |
| `apache:with-crs:with-mrts` | 1469 | 2 | 106 |
| `nginx:with-crs:with-mrts` | 2771 | 2 | 113 |
| `haproxy:with-crs:with-mrts` | 0 | 2 | 0 |

## Missing / Timeout Jobs

Missing/Empty: no missing or timed-out Full-Matrix jobs.

## Slowest Jobs

| Job | Duration | Notes |
| --- | ---: | --- |
| `nginx:with-crs:with-mrts` | 2771 | job.json exists with rc=2 |
| `nginx:no-crs:with-mrts` | 2538 | job.json exists with rc=2 |
| `apache:with-crs:with-mrts` | 1469 | job.json exists with rc=2 |
| `apache:no-crs:with-mrts` | 1368 | job.json exists with rc=2 |
| `nginx:with-crs:no-mrts` | 573 | job.json exists with rc=2 |

## NGINX with-crs/with-mrts Runtime Analysis

- Last running case: `mrts_100156_mrts_110_xml_100156_1`
- Last failed case: `v3_transformation_trim_block`
- Run log lines: `7874`
- Running-case lines: `524`
- FAIL lines: `113`
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
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `808eb86b9a8c6b19093fc2daf965ca1fd031be11bfaba263f2988a910586c0bf` |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | present | `f7092c24374de4f6bf26ea230ed84429b8dfc9cded204a709c9619599d6dd73f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | present | `947886627f065d44ee108c14e61884e4711fdb8c0bcfd252de45b5861f8b8ce6` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | present | `c2073e76bc2dc2eda91becfd2e4259c76a003a841315941ef5003999aed21cc0` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `056fd01f02ef7665d48072916e692a369e993e423504ef8c19d5cdb05ae3f933` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `1fb75ed9e641d2c8e060dc6030d8f92aff184cd5815a4fd2754ae02e8b8eb938` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | `a66ddb719af832977e5f9dfcc3843bbbf7ecbc82dc6419972c500f4fde370d3e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | `16d7427ec278130772271c0a6592bea60ea182a7787009e9a7d8122e17f02f18` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `6b786b2af4a2058528b6f25c352773c3c7a540699888de46fbaa9a08ba5007ef` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `25c48f9f671fbb7c6b8622407d11047e10669651f58b42e5d291142b939ecbdc` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `08652610c757311206bf4a3a33b79490dd3814a5891c61751bafc0e3ddac7d97` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | `664bc50b9b2b77c40f60c722d6135d239b94208cc6fb0113f90e611d47efab30` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | present | `a02e23ffded6729e96b66ffb761e334f490d55e206060e07f738af5906d3d2aa` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | present | `28a1255621b19c4bb5721f3177f23f15c6d2a14b90ec5ca3024de44b40c2b8df` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `0b8eb3359e8f27a0941eb834026b92ea31730acb1c61882dc1429d82f7d60ebf` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `1ec58bc047e735e130bcf529adb1d1b91e7d42f4c3a3a52adb69d13f95b157c7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | `6beb1b95910596d2e7c9d0706d5b81cbc62c8ac25c26067dfed0b6434fb38555` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | `0a6ca1c000e76af54bc76d5573d652bbfa9cc9eea50997cd0195b06af8814ef7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `d72de57df3d0b25cd973e11de3f65b5dfce551ce31c7283404dc0b87f4072bc1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `1167a508dcbc92085abf9ae2bcf1ee41c52eb31b1f1bab50ccc09ff4e56f87f5` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `24ddaa455062edc3b5c5a112e72f2a00db41133f445de701d0c15d0af8ecdac2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | `24573e09dde1c400ebb7a8f8335d92d819d845c0b444517156065eef42a10d6f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | present | `2bbb6eb0feffdea276ef0aa7028c4243eea2d84b809813f2d6480f6309b737e0` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | present | `95045dec2f33cfdca48c8d16a96f66c8b858f7a32afaed1a9a908817ee95f2aa` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `44b196bb61b6b29157be63c7b2ef3f54fecc7db62d92ecb279514eaea261baa9` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `9113cabb610af99f90b9bf4a77e700f1f258f4d944fd7d4dcbd8d3398c3230f4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | `d4539d6d4560d364095e633834424ac7feda3177086dea40541b3901ba4d8e8c` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | `3c4d8fa7a16faab1215901f60aab89f72538e98a6737a3c1a1d24f10690bac2c` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `4332e809ba8efbb0fb5b7c87bd9ae94994edb77a4a68041214927ba23be10c87` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `5128a4710e226e227819d25e30de7730cff4b79a4404e47fa37e69cb9dcb0659` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `d424f4de305b39b5b75a023d407b5a2a49dac1d3c6941942370e79a3cfc0d8e6` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | `6e85cdd03dbeaf087492310bf977364ac964e59395583b4c93b09d67916d7c52` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | present | `d985c77acec1d6c5890ead002c56abeecad02f68f7d67bbd40247c5e4216a9b4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | present | `7ff744485107f920ecc3f5e8e9543c86ec286eea274c3e50894b4307bdf4cda4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `ba3e820dd192da52ce9f7f59e894b809d66c536bf90cc2e670648c377f28d65d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `0e30d70613addd7ca98c261e9959c390c61595fd3fd9fd14601e9b1acbbae618` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | `9206a9635a2c539ee6be6364bd72e0f7f5c1cd59f44944053805207de483bacd` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | `cc3624e2c87d64ddbae32d7b431ba38ef7632a43f9d3e18ded5992da510e761e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `ebb0b75de09d92c6e4f6dabb733867c64bbc7054422a7392ceb9bbcc0697f3da` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `40299cbd2d9894d945ba652a65729e2233a20ef72b4ed71cf6f532cbec705df8` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `158169e9f708a0d2a23dfc2f81340778a6db6b0f78e3ff98ddc8ef60212b19b2` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | `667a7e15bdf8a1c0671a7186e1f6b155cae82e78a22d9e618a1196b121240e71` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `808eb86b9a8c6b19093fc2daf965ca1fd031be11bfaba263f2988a910586c0bf` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | `f7092c24374de4f6bf26ea230ed84429b8dfc9cded204a709c9619599d6dd73f` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | `947886627f065d44ee108c14e61884e4711fdb8c0bcfd252de45b5861f8b8ce6` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | `c2073e76bc2dc2eda91becfd2e4259c76a003a841315941ef5003999aed21cc0` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | `056fd01f02ef7665d48072916e692a369e993e423504ef8c19d5cdb05ae3f933` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `1fb75ed9e641d2c8e060dc6030d8f92aff184cd5815a4fd2754ae02e8b8eb938` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | `a66ddb719af832977e5f9dfcc3843bbbf7ecbc82dc6419972c500f4fde370d3e` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | `16d7427ec278130772271c0a6592bea60ea182a7787009e9a7d8122e17f02f18` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `6b786b2af4a2058528b6f25c352773c3c7a540699888de46fbaa9a08ba5007ef` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `25c48f9f671fbb7c6b8622407d11047e10669651f58b42e5d291142b939ecbdc` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | `08652610c757311206bf4a3a33b79490dd3814a5891c61751bafc0e3ddac7d97` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | `664bc50b9b2b77c40f60c722d6135d239b94208cc6fb0113f90e611d47efab30` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | `a02e23ffded6729e96b66ffb761e334f490d55e206060e07f738af5906d3d2aa` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | `28a1255621b19c4bb5721f3177f23f15c6d2a14b90ec5ca3024de44b40c2b8df` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | `0b8eb3359e8f27a0941eb834026b92ea31730acb1c61882dc1429d82f7d60ebf` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `1ec58bc047e735e130bcf529adb1d1b91e7d42f4c3a3a52adb69d13f95b157c7` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | `6beb1b95910596d2e7c9d0706d5b81cbc62c8ac25c26067dfed0b6434fb38555` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | `0a6ca1c000e76af54bc76d5573d652bbfa9cc9eea50997cd0195b06af8814ef7` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `d72de57df3d0b25cd973e11de3f65b5dfce551ce31c7283404dc0b87f4072bc1` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `1167a508dcbc92085abf9ae2bcf1ee41c52eb31b1f1bab50ccc09ff4e56f87f5` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | `24ddaa455062edc3b5c5a112e72f2a00db41133f445de701d0c15d0af8ecdac2` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | `24573e09dde1c400ebb7a8f8335d92d819d845c0b444517156065eef42a10d6f` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | `2bbb6eb0feffdea276ef0aa7028c4243eea2d84b809813f2d6480f6309b737e0` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | `95045dec2f33cfdca48c8d16a96f66c8b858f7a32afaed1a9a908817ee95f2aa` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | `44b196bb61b6b29157be63c7b2ef3f54fecc7db62d92ecb279514eaea261baa9` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `9113cabb610af99f90b9bf4a77e700f1f258f4d944fd7d4dcbd8d3398c3230f4` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | `d4539d6d4560d364095e633834424ac7feda3177086dea40541b3901ba4d8e8c` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | `3c4d8fa7a16faab1215901f60aab89f72538e98a6737a3c1a1d24f10690bac2c` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `4332e809ba8efbb0fb5b7c87bd9ae94994edb77a4a68041214927ba23be10c87` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `5128a4710e226e227819d25e30de7730cff4b79a4404e47fa37e69cb9dcb0659` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | `d424f4de305b39b5b75a023d407b5a2a49dac1d3c6941942370e79a3cfc0d8e6` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | `6e85cdd03dbeaf087492310bf977364ac964e59395583b4c93b09d67916d7c52` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | `d985c77acec1d6c5890ead002c56abeecad02f68f7d67bbd40247c5e4216a9b4` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | `7ff744485107f920ecc3f5e8e9543c86ec286eea274c3e50894b4307bdf4cda4` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | `ba3e820dd192da52ce9f7f59e894b809d66c536bf90cc2e670648c377f28d65d` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `0e30d70613addd7ca98c261e9959c390c61595fd3fd9fd14601e9b1acbbae618` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `9206a9635a2c539ee6be6364bd72e0f7f5c1cd59f44944053805207de483bacd` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `cc3624e2c87d64ddbae32d7b431ba38ef7632a43f9d3e18ded5992da510e761e` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `ebb0b75de09d92c6e4f6dabb733867c64bbc7054422a7392ceb9bbcc0697f3da` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `40299cbd2d9894d945ba652a65729e2233a20ef72b4ed71cf6f532cbec705df8` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | `158169e9f708a0d2a23dfc2f81340778a6db6b0f78e3ff98ddc8ef60212b19b2` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | `667a7e15bdf8a1c0671a7186e1f6b155cae82e78a22d9e618a1196b121240e71` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | `ad6b60f4ebf94f1c9b8b7c5c81a40c33c546cdfe05b4d16a97fa0edb348bd10a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` | `2026-06-16T16-57-44Z-b53340a8` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T16-57-44Z-b53340a8/verified-commands.json` | present | input file available |
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
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | input file available |
