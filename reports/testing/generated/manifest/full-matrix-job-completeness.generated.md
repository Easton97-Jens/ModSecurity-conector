> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T05:56:28Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-full-matrix-job-completeness.py`
> Make target: `generate-full-matrix-job-completeness`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `9391a8d0d5bf170f8af994c361f0b9fa50015834`
> Framework SHA: `708183dce7dcd0ad190a5cb5211b1ba3de6a2385`
> Input status: `complete`

# Full-Matrix Job Completeness

Verified run id: `2026-06-15T21-01-39Z-9391a8d0`

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
| `apache:no-crs:no-mrts` | apache | no-crs | no-mrts | `completed_with_mismatches` | 344 | 133 | 19 | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/run.log` |
| `nginx:no-crs:no-mrts` | nginx | no-crs | no-mrts | `completed_with_mismatches` | 524 | 140 | 60 | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/run.log` |
| `haproxy:no-crs:no-mrts` | haproxy | no-crs | no-mrts | `completed_with_mismatches` | 329 | 133 | 19 | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/run.log` |
| `apache:no-crs:with-mrts` | apache | no-crs | with-mrts | `completed_with_mismatches` | 1372 | 516 | 104 | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/run.log` |
| `nginx:no-crs:with-mrts` | nginx | no-crs | with-mrts | `completed_with_mismatches` | 3141 | 523 | 517 | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/run.log` |
| `haproxy:no-crs:with-mrts` | haproxy | no-crs | with-mrts | `completed_with_mismatches` | 1209 | 516 | 104 | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/run.log` |
| `apache:with-crs:no-mrts` | apache | with-crs | no-mrts | `completed_with_mismatches` | 398 | 134 | 19 | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/run.log` |
| `nginx:with-crs:no-mrts` | nginx | with-crs | no-mrts | `completed_with_mismatches` | 597 | 141 | 59 | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/run.log` |
| `haproxy:with-crs:no-mrts` | haproxy | with-crs | no-mrts | `completed_with_mismatches` | 383 | 134 | 19 | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/run.log` |
| `apache:with-crs:with-mrts` | apache | with-crs | with-mrts | `completed_with_mismatches` | 1521 | 517 | 106 | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/run.log` |
| `nginx:with-crs:with-mrts` | nginx | with-crs | with-mrts | `completed_with_mismatches` | 3273 | 524 | 518 | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/run.log` |
| `haproxy:with-crs:with-mrts` | haproxy | with-crs | with-mrts | `completed_with_mismatches` | 1347 | 517 | 106 | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/run.log` |

## Completed Jobs

| Job | Duration | RC | Failures |
| --- | ---: | -: | ---: |
| `apache:no-crs:no-mrts` | 344 | 2 | 19 |
| `nginx:no-crs:no-mrts` | 524 | 2 | 60 |
| `haproxy:no-crs:no-mrts` | 329 | 2 | 19 |
| `apache:no-crs:with-mrts` | 1372 | 2 | 104 |
| `nginx:no-crs:with-mrts` | 3141 | 2 | 517 |
| `haproxy:no-crs:with-mrts` | 1209 | 2 | 104 |
| `apache:with-crs:no-mrts` | 398 | 2 | 19 |
| `nginx:with-crs:no-mrts` | 597 | 2 | 59 |
| `haproxy:with-crs:no-mrts` | 383 | 2 | 19 |
| `apache:with-crs:with-mrts` | 1521 | 2 | 106 |
| `nginx:with-crs:with-mrts` | 3273 | 2 | 518 |
| `haproxy:with-crs:with-mrts` | 1347 | 2 | 106 |

## Missing / Timeout Jobs

Missing/Empty: no missing or timed-out Full-Matrix jobs.

## Slowest Jobs

| Job | Duration | Notes |
| --- | ---: | --- |
| `nginx:with-crs:with-mrts` | 3273 | job.json exists with rc=2 |
| `nginx:no-crs:with-mrts` | 3141 | job.json exists with rc=2 |
| `apache:with-crs:with-mrts` | 1521 | job.json exists with rc=2 |
| `apache:no-crs:with-mrts` | 1372 | job.json exists with rc=2 |
| `haproxy:with-crs:with-mrts` | 1347 | job.json exists with rc=2 |

## NGINX with-crs/with-mrts Runtime Analysis

- Last running case: `mrts_100156_mrts_110_xml_100156_1`
- Last failed case: `mrts_100156_mrts_110_xml_100156_1`
- Run log lines: `7874`
- Running-case lines: `524`
- FAIL lines: `518`
- Observed 500 lines: `510`
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
| `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | present | `f9634d21e3486bd05843bab0d423dd871d48edcfe6a2ec7a46cd5c694f3b54bb` |
| `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | `a351abf7f756d9bf30cb805bdc57e3e5830a456735d9a6307c3bf154ce75bab9` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/job.json` | present | `c8402f160a295c0771a536254b82be01d30ee5ac6e889d3788831b61dcf71078` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/run.log` | present | `83ec8b550d1f12f188f44a49a827cafdf7bc86ff23b32944d398c85a23557f46` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `51ed44be35af5488aece950470f42c121296a25708f26d4abaf459fb621a084d` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `97dca6f7609b294e1891743c5100ef4fef1eb9116a450554ad970985efb461ae` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | `01bbff9b29b7ea6b99675661e94fda6bee0d82e80e60f84bfb779f99997d0e0f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | `ee53cc7eea42857ddd6a9da3d30d0036724486a4f615a735d34edb3643cc282f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `47b2bb86a5ba0352664796a58827a2310763b006085215914fc239bff9084757` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `7a4c06511e35054fea0fb8147522514bf339ababa8694650be89ca329776f70f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | `dfdc25be9e88791784904eee41e3f14c0963c4d3937ee02fd1d9f2b7d33cb001` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | `71bfb17d8f32c026125e489c83b7a10ce06bb37d87a2690121b534f9cd5cbdd6` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `0f3a0b511cc163d3528cd2a8a3e227445edf51b73131d7448aa6246a61c931cc` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/job.json` | present | `3d78b7443596377e0edb3ee3ea18b1f35250a25205b0d2f74d2ca517bf3202f8` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/run.log` | present | `c9efff78d7d31b417f73c6a84d377c79b81cf1709b6667bcf8e8707295d460d7` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `19d476da10b282fe0b3dda4e5b33f7d6af022291c556dd0c5cdd2fa2f45b12aa` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `129e1fa808b689d323925fd08b73fcb962a1c6b761b8f221a7458f38f5cc37c4` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | `d9dc4ab30c858f67255701c0ee2b7ee77d6ec1835b675cea43d796be29480083` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | `c64e6a925b4cad9c6f773f5a15909682639b38fd90e0a2ed256b5657fd88011d` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `0a23ef8755e377c3a1f02072a5ae0778000ba36a65fb0f1a4e03ec0b494ab0bb` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `4045bb83c5db845fb321392ad53d7da034f0de3304fdc4cf3667a62e8766ad31` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | `33c1e28170576345db47af9fea8431d2838a7fe6105d9578d6e25593f8290b2a` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | `072941ca72b7ba749efcce790a0ffcaa1ce1855eddd2757fbebac5ecaaff7593` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `8999743cd573a3fbb48273cacf45e6c9ea3da3abac769f47395c3d46aa49b424` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/job.json` | present | `4eeec4587355925ba8d7922e43436c5e7d60d17632c89848eda1e438cdc0954a` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/run.log` | present | `4eb32ec96d317e6dac363d05261c13623bc29f0c0c2d476297b67d48d4618280` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | `8b80105e55523c2dba26ee787c046e0dbac2318685ca4afe38ef01e5362d8e44` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | `2d08836ddc6e417ff77d35aee044c6afa65818f097a90dfffa3387b5748fce54` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | `539e70cbe89c2d1c0ee010d3fa935294552f0d9ea8778e303ef1c8b9a6fa4610` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | `1e6bf082f772f4c82acac2bed1d37b92cdb1981fe28101f421f3ae1aa9b0d29b` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | `af2f0b5878d7d5bb584f84b2c8d664008ef2f6f5f9ec767e5af2beb78748d202` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `e1a4c477ab3f864e164bbe7a7f8c710e109553a2aad07f5b42a8fa843505417b` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | `54b49ce81980fe2ee2679d87e94af43eb1a35bfd68f461465f57cba81216e3b7` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | `e9846c2f18e6195cef0dcdc76bd049a393330e0e006a7f86aae6ec14b77b4bcb` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | `38edd35d5d84110a318587bf1a5571d3eba41414c1b3693c8fb97ae744fde8b1` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/job.json` | present | `1864576f38033a6e8ac8294a2532ffc0d82b2d6738988556928a11e8ad9ce03d` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/run.log` | present | `8b9ffd9bada7755e039d2947efbf5e1b5ebadfd54323312f1ff5ed09b2763955` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | `6ae8ee4339ffc6fe9aac0528e750685def7ee88df50e464f8b931b841b624be9` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | `95548c4aadd957405d9315bade3bbed93873696ecbedf8256d61243c09899148` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | `cc976ebe3ad755c099812bbe31393f92476e717cfbf83a54da91df67a647e2f7` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | `01a74cbafdd3ffdc001a0037435a2a9f8328e4e79f4a12f9d4762e80c398b171` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | `4f0e9c8f457e28365c361cf25b5c2bfdb481625c22ffd4739c5e7434314f567e` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | `6c1859588a5d1cff7ee5a6fd1c347f4629381bd6c6221e0c7978f0f072ef989e` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | `8efbce6ae1454ca86ce4d7f5fde168a47b78743b9a8fad525e84c972f5cf7e47` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | `665e4200a092978c7c7007e3d06e043c5f7162ad789899943891150fc07767e5` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | `1e8998bdf289217d45a7df434310de0f91c3b6ef6d6785bb45ec3052e95e396f` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | `bdbf4a2f04351e22236196cf66906f37c8cb652a24f9d039ac0a9c52c8f40fb9` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | `1bebe0cc629cf0f3d171f7147da0d3f1cdf5f75669ff7752327aa91f5e4ed4c3` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | `06ea33eb554077cd9db79e044fa0a7e60391c9f3e855a33e83870c53bb6e7cf0` |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | `f9634d21e3486bd05843bab0d423dd871d48edcfe6a2ec7a46cd5c694f3b54bb` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | `a351abf7f756d9bf30cb805bdc57e3e5830a456735d9a6307c3bf154ce75bab9` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/job.json` | `c8402f160a295c0771a536254b82be01d30ee5ac6e889d3788831b61dcf71078` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/run.log` | `83ec8b550d1f12f188f44a49a827cafdf7bc86ff23b32944d398c85a23557f46` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | `51ed44be35af5488aece950470f42c121296a25708f26d4abaf459fb621a084d` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `97dca6f7609b294e1891743c5100ef4fef1eb9116a450554ad970985efb461ae` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/job.json` | `01bbff9b29b7ea6b99675661e94fda6bee0d82e80e60f84bfb779f99997d0e0f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/run.log` | `ee53cc7eea42857ddd6a9da3d30d0036724486a4f615a735d34edb3643cc282f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `47b2bb86a5ba0352664796a58827a2310763b006085215914fc239bff9084757` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `7a4c06511e35054fea0fb8147522514bf339ababa8694650be89ca329776f70f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/job.json` | `dfdc25be9e88791784904eee41e3f14c0963c4d3937ee02fd1d9f2b7d33cb001` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/run.log` | `71bfb17d8f32c026125e489c83b7a10ce06bb37d87a2690121b534f9cd5cbdd6` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | `0f3a0b511cc163d3528cd2a8a3e227445edf51b73131d7448aa6246a61c931cc` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/job.json` | `3d78b7443596377e0edb3ee3ea18b1f35250a25205b0d2f74d2ca517bf3202f8` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/run.log` | `c9efff78d7d31b417f73c6a84d377c79b81cf1709b6667bcf8e8707295d460d7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | `19d476da10b282fe0b3dda4e5b33f7d6af022291c556dd0c5cdd2fa2f45b12aa` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `129e1fa808b689d323925fd08b73fcb962a1c6b761b8f221a7458f38f5cc37c4` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/job.json` | `d9dc4ab30c858f67255701c0ee2b7ee77d6ec1835b675cea43d796be29480083` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/run.log` | `c64e6a925b4cad9c6f773f5a15909682639b38fd90e0a2ed256b5657fd88011d` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `0a23ef8755e377c3a1f02072a5ae0778000ba36a65fb0f1a4e03ec0b494ab0bb` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `4045bb83c5db845fb321392ad53d7da034f0de3304fdc4cf3667a62e8766ad31` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/job.json` | `33c1e28170576345db47af9fea8431d2838a7fe6105d9578d6e25593f8290b2a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/run.log` | `072941ca72b7ba749efcce790a0ffcaa1ce1855eddd2757fbebac5ecaaff7593` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | `8999743cd573a3fbb48273cacf45e6c9ea3da3abac769f47395c3d46aa49b424` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/job.json` | `4eeec4587355925ba8d7922e43436c5e7d60d17632c89848eda1e438cdc0954a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/run.log` | `4eb32ec96d317e6dac363d05261c13623bc29f0c0c2d476297b67d48d4618280` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | `8b80105e55523c2dba26ee787c046e0dbac2318685ca4afe38ef01e5362d8e44` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | `2d08836ddc6e417ff77d35aee044c6afa65818f097a90dfffa3387b5748fce54` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/job.json` | `539e70cbe89c2d1c0ee010d3fa935294552f0d9ea8778e303ef1c8b9a6fa4610` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/run.log` | `1e6bf082f772f4c82acac2bed1d37b92cdb1981fe28101f421f3ae1aa9b0d29b` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | `af2f0b5878d7d5bb584f84b2c8d664008ef2f6f5f9ec767e5af2beb78748d202` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | `e1a4c477ab3f864e164bbe7a7f8c710e109553a2aad07f5b42a8fa843505417b` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/job.json` | `54b49ce81980fe2ee2679d87e94af43eb1a35bfd68f461465f57cba81216e3b7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/run.log` | `e9846c2f18e6195cef0dcdc76bd049a393330e0e006a7f86aae6ec14b77b4bcb` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | `38edd35d5d84110a318587bf1a5571d3eba41414c1b3693c8fb97ae744fde8b1` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/job.json` | `1864576f38033a6e8ac8294a2532ffc0d82b2d6738988556928a11e8ad9ce03d` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/run.log` | `8b9ffd9bada7755e039d2947efbf5e1b5ebadfd54323312f1ff5ed09b2763955` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | `6ae8ee4339ffc6fe9aac0528e750685def7ee88df50e464f8b931b841b624be9` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | `95548c4aadd957405d9315bade3bbed93873696ecbedf8256d61243c09899148` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | `bd1821bb4bfa96e7c6fd369839f803b6031063f7468fa776bc0e3d7a865de15f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | `cc976ebe3ad755c099812bbe31393f92476e717cfbf83a54da91df67a647e2f7` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/job.json` | `01a74cbafdd3ffdc001a0037435a2a9f8328e4e79f4a12f9d4762e80c398b171` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/run.log` | `4f0e9c8f457e28365c361cf25b5c2bfdb481625c22ffd4739c5e7434314f567e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `6c1859588a5d1cff7ee5a6fd1c347f4629381bd6c6221e0c7978f0f072ef989e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `8efbce6ae1454ca86ce4d7f5fde168a47b78743b9a8fad525e84c972f5cf7e47` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | `ea212075df625b0068175103bfbeacb9b3bbd8d4c22d5a3fc3a1bbe052c422d2` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | `665e4200a092978c7c7007e3d06e043c5f7162ad789899943891150fc07767e5` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/job.json` | `1e8998bdf289217d45a7df434310de0f91c3b6ef6d6785bb45ec3052e95e396f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/run.log` | `bdbf4a2f04351e22236196cf66906f37c8cb652a24f9d039ac0a9c52c8f40fb9` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | `1bebe0cc629cf0f3d171f7147da0d3f1cdf5f75669ff7752327aa91f5e4ed4c3` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | `86e39438d492ecbca9220c940de80847c1d6556b60325c70f22e185bb306954e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | `06ea33eb554077cd9db79e044fa0a7e60391c9f3e855a33e83870c53bb6e7cf0` | `2026-06-15T21-01-39Z-9391a8d0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `/root/.local/state/ModSecurity-conector-build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/verified-runs/2026-06-15T21-01-39Z-9391a8d0/verified-commands.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/apache/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/nginx/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/no-mrts/haproxy/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/apache/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/nginx/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/no-crs/with-mrts/haproxy/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/apache/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/nginx/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/no-mrts/haproxy/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/apache/preambles/apache-with-crs-with-mrts.load` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/nginx/preambles/nginx-with-crs-with-mrts.load` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/job.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/run.log` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/build-manifest.json` | present | input file available |
| `/root/.local/state/ModSecurity-conector-build/full-matrix/with-crs/with-mrts/haproxy/preambles/haproxy-with-crs-with-mrts.load` | present | input file available |
