> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:39:20Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-matrix-job-completeness.py`
> Make target: `generate-full-matrix-job-completeness`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
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
| `apache:no-crs:no-mrts` | apache | no-crs | no-mrts | `completed_with_mismatches` | 354 | 133 | 19 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` |
| `nginx:no-crs:no-mrts` | nginx | no-crs | no-mrts | `completed_with_mismatches` | 584 | 140 | 31 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` |
| `haproxy:no-crs:no-mrts` | haproxy | no-crs | no-mrts | `completed_with_mismatches` | 330 | 133 | 19 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` |
| `apache:no-crs:with-mrts` | apache | no-crs | with-mrts | `completed_with_mismatches` | 1378 | 516 | 104 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` |
| `nginx:no-crs:with-mrts` | nginx | no-crs | with-mrts | `completed_with_mismatches` | 3391 | 523 | 111 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` |
| `haproxy:no-crs:with-mrts` | haproxy | no-crs | with-mrts | `completed_with_mismatches` | 1202 | 516 | 104 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` |
| `apache:with-crs:no-mrts` | apache | with-crs | no-mrts | `completed_with_mismatches` | 379 | 134 | 19 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` |
| `nginx:with-crs:no-mrts` | nginx | with-crs | no-mrts | `completed_with_mismatches` | 645 | 141 | 31 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` |
| `haproxy:with-crs:no-mrts` | haproxy | with-crs | no-mrts | `completed_with_mismatches` | 365 | 134 | 19 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` |
| `apache:with-crs:with-mrts` | apache | with-crs | with-mrts | `completed_with_mismatches` | 1502 | 517 | 106 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` |
| `nginx:with-crs:with-mrts` | nginx | with-crs | with-mrts | `completed_with_mismatches` | 3593 | 524 | 113 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` |
| `haproxy:with-crs:with-mrts` | haproxy | with-crs | with-mrts | `completed_with_mismatches` | 1360 | 517 | 106 | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` |

## Completed Jobs

| Job | Duration | RC | Failures |
| --- | ---: | -: | ---: |
| `apache:no-crs:no-mrts` | 354 | 2 | 19 |
| `nginx:no-crs:no-mrts` | 584 | 2 | 31 |
| `haproxy:no-crs:no-mrts` | 330 | 2 | 19 |
| `apache:no-crs:with-mrts` | 1378 | 2 | 104 |
| `nginx:no-crs:with-mrts` | 3391 | 2 | 111 |
| `haproxy:no-crs:with-mrts` | 1202 | 2 | 104 |
| `apache:with-crs:no-mrts` | 379 | 2 | 19 |
| `nginx:with-crs:no-mrts` | 645 | 2 | 31 |
| `haproxy:with-crs:no-mrts` | 365 | 2 | 19 |
| `apache:with-crs:with-mrts` | 1502 | 2 | 106 |
| `nginx:with-crs:with-mrts` | 3593 | 2 | 113 |
| `haproxy:with-crs:with-mrts` | 1360 | 2 | 106 |

## Missing / Timeout Jobs

Missing/Empty: no missing or timed-out Full-Matrix jobs.

## Slowest Jobs

| Job | Duration | Notes |
| --- | ---: | --- |
| `nginx:with-crs:with-mrts` | 3593 | job.json exists with rc=2 |
| `nginx:no-crs:with-mrts` | 3391 | job.json exists with rc=2 |
| `apache:with-crs:with-mrts` | 1502 | job.json exists with rc=2 |
| `apache:no-crs:with-mrts` | 1378 | job.json exists with rc=2 |
| `haproxy:with-crs:with-mrts` | 1360 | job.json exists with rc=2 |

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
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `d2e21234df8b14aa214920453961538724f99e195f37d247c91785db79b7db23` |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | `cbdb375cdfd0974fcdb515076272ae2edc7a4f78fcf56e02e35c944f5d2c56c7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | present | `82de69f45d424f1c0a25fb648b3085a6b0e207b89c5975a5ac47c18d4e23e664` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | present | `d8c1315d8ecd38f11a8b2b056f5a62a638bc3c090561d398e5890760f7d7f4a7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `056fd01f02ef7665d48072916e692a369e993e423504ef8c19d5cdb05ae3f933` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `1fb75ed9e641d2c8e060dc6030d8f92aff184cd5815a4fd2754ae02e8b8eb938` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | `711f3b39d78086288a7a74e89954269ac547787d0f8dd4bd4bb7c7392b502fc3` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | `c144955dcd349b13056a023e1371453f972876a6e8c9d6057160df94730e30ed` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `6b786b2af4a2058528b6f25c352773c3c7a540699888de46fbaa9a08ba5007ef` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `25c48f9f671fbb7c6b8622407d11047e10669651f58b42e5d291142b939ecbdc` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `f64861e689b719c5de9fd18dcc34b9b3c7140099d28594a3a838510f084d85a3` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | `37b1f7eb3cab3ef8643b978e2c6af20cc716f3e2b465056ba38b0dcdcc668216` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `dd59a95c72855986b3d85bdc4f7130ede9155f9e8f9ec4511ed2c5e5ffd9cab1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | present | `5f09acc89f8e1b86b7ec2bc4698bc693f1fd59e8f2ebe96ca4378fdf0202e7c6` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | present | `ffbbc166041ff12040dc939adc0bbd599bf9e83c1b3fa19680a00e687d8b2776` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `0b8eb3359e8f27a0941eb834026b92ea31730acb1c61882dc1429d82f7d60ebf` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `1ec58bc047e735e130bcf529adb1d1b91e7d42f4c3a3a52adb69d13f95b157c7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | `7bf56fd6afe9101efdd044eff0817c78634473b66cc590168be1c9aae704d611` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | `72910ecc14ff5216c778061bd1796d5ed49058df4e39165712c09b3052e28fda` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `d72de57df3d0b25cd973e11de3f65b5dfce551ce31c7283404dc0b87f4072bc1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `1167a508dcbc92085abf9ae2bcf1ee41c52eb31b1f1bab50ccc09ff4e56f87f5` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `394b0c1ad9b16b6ba688242aad993d156362985dfba3be285405183d161a3d7e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | `f429a61fbc57dc98bea6d90625783405c9f89f4b89053bc47c5092736325e74e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `8b95c8d25b729f1fc3aae852021cac3b216a3e2a6d6272ac17e562511dfafabc` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | present | `0b56032e03ae207701e0ac924176678a3b314eba2e44bf681946e172d33bcb3d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | present | `96f3a691b1d2cf7a84263072ddc12e59696e19c0144c78389b4821787dce3d1e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `44b196bb61b6b29157be63c7b2ef3f54fecc7db62d92ecb279514eaea261baa9` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `9113cabb610af99f90b9bf4a77e700f1f258f4d944fd7d4dcbd8d3398c3230f4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | `c539ae5740caf5b7614d5b44420d46e7ed2de19211279310cdec9330b1eb9932` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | `de0574fd40c55931a6bac6a2133c46fa58b9f544bc29ec45ecc1dd17a037b8e9` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `4332e809ba8efbb0fb5b7c87bd9ae94994edb77a4a68041214927ba23be10c87` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `5128a4710e226e227819d25e30de7730cff4b79a4404e47fa37e69cb9dcb0659` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `c00d745856dc57fd37a63c244dcbbe6559c744ab5aabd4bf0e1ebff27785387e` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | `a027cdf893b30a46c2eaa63330f983d396792b5d2e8f17acec0e605ad41f7b67` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `1eaa0e3dddd9efa5e703af28d4f74a54089cfeab0c6f5ca50c092b99af1ac3ea` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | present | `0fc73808442c9ed876d4a8f4c454744ac3ab01ed56066faf55b3be41c4434a9c` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | present | `b0702b76041ea331a66f0f8879873a2ea2b4749cf081095ed286ec425df74950` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `ba3e820dd192da52ce9f7f59e894b809d66c536bf90cc2e670648c377f28d65d` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `0e30d70613addd7ca98c261e9959c390c61595fd3fd9fd14601e9b1acbbae618` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | `c16d5312eb346234dbef3b01c12d23bc5eea015648f88c1fbe3102149140a78a` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | `a7f3a84a51d9219e3302a63320a66a36c1bf7197706fde0771982aa9102fd284` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `ebb0b75de09d92c6e4f6dabb733867c64bbc7054422a7392ceb9bbcc0697f3da` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `40299cbd2d9894d945ba652a65729e2233a20ef72b4ed71cf6f532cbec705df8` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `08ad11d613d11d5c7e76d123988b6d7ed8894660b6bcf073a81415c2886c85d0` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | `2449e9b00dba1d5eca988dd5917ada064e578ab1aebf806d48325b37d46f9b95` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `c337a70247dff017797ab857ed1bb932a48652ed15eee9e106c6fcf5b41fb4a4` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | `5770573af35d8c7ffe9be9c6940b23a84bc1d9dc1abe5df97d939ea150ef02a7` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `d2e21234df8b14aa214920453961538724f99e195f37d247c91785db79b7db23` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `cbdb375cdfd0974fcdb515076272ae2edc7a4f78fcf56e02e35c944f5d2c56c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/job.json` | `82de69f45d424f1c0a25fb648b3085a6b0e207b89c5975a5ac47c18d4e23e664` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log` | `d8c1315d8ecd38f11a8b2b056f5a62a638bc3c090561d398e5890760f7d7f4a7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | `056fd01f02ef7665d48072916e692a369e993e423504ef8c19d5cdb05ae3f933` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `1fb75ed9e641d2c8e060dc6030d8f92aff184cd5815a4fd2754ae02e8b8eb938` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/job.json` | `711f3b39d78086288a7a74e89954269ac547787d0f8dd4bd4bb7c7392b502fc3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log` | `c144955dcd349b13056a023e1371453f972876a6e8c9d6057160df94730e30ed` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `6b786b2af4a2058528b6f25c352773c3c7a540699888de46fbaa9a08ba5007ef` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `25c48f9f671fbb7c6b8622407d11047e10669651f58b42e5d291142b939ecbdc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/job.json` | `f64861e689b719c5de9fd18dcc34b9b3c7140099d28594a3a838510f084d85a3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log` | `37b1f7eb3cab3ef8643b978e2c6af20cc716f3e2b465056ba38b0dcdcc668216` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | `dd59a95c72855986b3d85bdc4f7130ede9155f9e8f9ec4511ed2c5e5ffd9cab1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/job.json` | `5f09acc89f8e1b86b7ec2bc4698bc693f1fd59e8f2ebe96ca4378fdf0202e7c6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log` | `ffbbc166041ff12040dc939adc0bbd599bf9e83c1b3fa19680a00e687d8b2776` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | `0b8eb3359e8f27a0941eb834026b92ea31730acb1c61882dc1429d82f7d60ebf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `1ec58bc047e735e130bcf529adb1d1b91e7d42f4c3a3a52adb69d13f95b157c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/job.json` | `7bf56fd6afe9101efdd044eff0817c78634473b66cc590168be1c9aae704d611` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log` | `72910ecc14ff5216c778061bd1796d5ed49058df4e39165712c09b3052e28fda` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `d72de57df3d0b25cd973e11de3f65b5dfce551ce31c7283404dc0b87f4072bc1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `1167a508dcbc92085abf9ae2bcf1ee41c52eb31b1f1bab50ccc09ff4e56f87f5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/job.json` | `394b0c1ad9b16b6ba688242aad993d156362985dfba3be285405183d161a3d7e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log` | `f429a61fbc57dc98bea6d90625783405c9f89f4b89053bc47c5092736325e74e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | `8b95c8d25b729f1fc3aae852021cac3b216a3e2a6d6272ac17e562511dfafabc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/job.json` | `0b56032e03ae207701e0ac924176678a3b314eba2e44bf681946e172d33bcb3d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log` | `96f3a691b1d2cf7a84263072ddc12e59696e19c0144c78389b4821787dce3d1e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | `44b196bb61b6b29157be63c7b2ef3f54fecc7db62d92ecb279514eaea261baa9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `9113cabb610af99f90b9bf4a77e700f1f258f4d944fd7d4dcbd8d3398c3230f4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/job.json` | `c539ae5740caf5b7614d5b44420d46e7ed2de19211279310cdec9330b1eb9932` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log` | `de0574fd40c55931a6bac6a2133c46fa58b9f544bc29ec45ecc1dd17a037b8e9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `4332e809ba8efbb0fb5b7c87bd9ae94994edb77a4a68041214927ba23be10c87` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `5128a4710e226e227819d25e30de7730cff4b79a4404e47fa37e69cb9dcb0659` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/job.json` | `c00d745856dc57fd37a63c244dcbbe6559c744ab5aabd4bf0e1ebff27785387e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log` | `a027cdf893b30a46c2eaa63330f983d396792b5d2e8f17acec0e605ad41f7b67` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | `1eaa0e3dddd9efa5e703af28d4f74a54089cfeab0c6f5ca50c092b99af1ac3ea` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | `22b44ab88da91f92983ebdd9114ac3c29e4ad4874252c5005ad8242b41b526e7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/job.json` | `0fc73808442c9ed876d4a8f4c454744ac3ab01ed56066faf55b3be41c4434a9c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log` | `b0702b76041ea331a66f0f8879873a2ea2b4749cf081095ed286ec425df74950` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | `ba3e820dd192da52ce9f7f59e894b809d66c536bf90cc2e670648c377f28d65d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `0e30d70613addd7ca98c261e9959c390c61595fd3fd9fd14601e9b1acbbae618` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | `18dbf05a0a629641287b1b8efe8f78bc621a7db69337bc1c7f533eef7f7640a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | `1076096770e3992d3be0479bb91c7c57de449a1c9cfeea4d95253a77f105234f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `c16d5312eb346234dbef3b01c12d23bc5eea015648f88c1fbe3102149140a78a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `a7f3a84a51d9219e3302a63320a66a36c1bf7197706fde0771982aa9102fd284` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `ebb0b75de09d92c6e4f6dabb733867c64bbc7054422a7392ceb9bbcc0697f3da` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `40299cbd2d9894d945ba652a65729e2233a20ef72b4ed71cf6f532cbec705df8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | `3f8f804d2954273fad22b5a6ababe4c51a91a3b93e9dd304fc099863e61d4a90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | `79c6dbe2ce8b15f21e9e0af9604f1f0553df025fa65d1c8e690c6dc867494726` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/job.json` | `08ad11d613d11d5c7e76d123988b6d7ed8894660b6bcf073a81415c2886c85d0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log` | `2449e9b00dba1d5eca988dd5917ada064e578ab1aebf806d48325b37d46f9b95` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | `c337a70247dff017797ab857ed1bb932a48652ed15eee9e106c6fcf5b41fb4a4` | `2026-06-16T19-12-00Z-614c8049` | present |
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
