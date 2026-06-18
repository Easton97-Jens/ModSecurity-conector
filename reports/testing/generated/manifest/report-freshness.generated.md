> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T21:57:21Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `29083baa42f7cae3aff7c9f340e2fbe437dd410d`
> Framework SHA: `c4d92c02d987a394a970fc3e8f5bfaaff5ed6b67`
> Input status: `blocked`

# Report Freshness

| Report | Status | Generated At | Newest Input | Newest Output | Missing Inputs | Notes |
|---|---|---|---|---|---|---|
| `connector_coverage_reports` | fresh | - | 2026-06-16T19:13:26Z | 2026-06-17T17:04:24Z | - | generated |
| `full_runtime_matrix` | fresh | 2026-06-17T21:56:12Z | 2026-06-17T21:54:47Z | 2026-06-17T21:56:12Z | - | generated |
| `full_matrix_job_completeness` | fresh | 2026-06-17T21:56:13Z | 2026-06-17T21:56:13Z | 2026-06-17T21:56:13Z | - | generated |
| `verified_runtime_mismatch_analysis` | fresh | 2026-06-17T21:56:19Z | 2026-06-17T21:56:13Z | 2026-06-17T21:56:19Z | - | generated |
| `nginx_mrts_http500_cluster_analysis` | fresh | 2026-06-17T21:56:19Z | 2026-06-17T21:56:19Z | 2026-06-17T21:56:19Z | - | generated |
| `connector_work_queue` | fresh | 2026-06-17T21:56:23Z | 2026-06-17T21:56:12Z | 2026-06-17T21:56:23Z | - | generated |
| `phase_work_queue` | fresh | 2026-06-17T21:56:24Z | 2026-06-17T21:56:23Z | 2026-06-17T21:56:24Z | - | generated |
| `native_mrts_reports` | fresh | 2026-06-17T21:56:25Z | 2026-06-16T21:14:22Z | 2026-06-17T21:56:25Z | - | generated |
| `nolog_audit_evidence` | fresh | 2026-06-17T21:56:26Z | 2026-06-17T21:56:26Z | 2026-06-17T21:56:26Z | - | generated |
| `response_header_hook_analysis` | fresh | 2026-06-17T21:56:30Z | 2026-06-17T21:56:30Z | 2026-06-17T21:56:31Z | - | generated |
| `phase4_hard_abort_capability` | fresh | 2026-06-17T21:56:37Z | 2026-06-17T21:56:30Z | 2026-06-17T21:56:37Z | - | generated |
| `remaining_failure_analysis` | fresh | 2026-06-17T21:56:41Z | 2026-06-17T21:56:37Z | 2026-06-17T21:56:56Z | - | generated |
| `intervention_blocking_analysis` | fresh | 2026-06-17T21:57:04Z | 2026-06-17T21:56:56Z | 2026-06-17T21:57:04Z | - | generated |
| `no_mrts_intervention_nomatch_analysis` | fresh | 2026-06-17T21:57:05Z | 2026-06-17T21:57:04Z | 2026-06-17T21:57:05Z | - | generated |
| `body_processor_analysis` | fresh | 2026-06-17T21:57:17Z | 2026-06-17T21:56:56Z | 2026-06-17T21:57:17Z | - | generated |
| `rule_chain_semantics_analysis` | fresh | 2026-06-17T21:57:18Z | 2026-06-17T21:56:56Z | 2026-06-17T21:57:18Z | - | generated |
| `final_consistency_audit` | fresh | 2026-06-17T21:57:19Z | 2026-06-17T21:57:18Z | 2026-06-17T21:57:20Z | - | generated |
| `runtime_cache_reports` | fresh | 2026-06-17T21:57:20Z | 2026-06-17T21:57:20Z | 2026-06-17T21:57:21Z | - | blocked |
| `report_dependency_graph` | fresh | 2026-06-17T21:57:21Z | 2026-06-17T21:57:20Z | 2026-06-17T21:57:21Z | - | generated |
| `report_data_lineage` | fresh | 2026-06-17T21:57:21Z | 2026-06-17T21:57:20Z | 2026-06-17T21:57:23Z | - | generated |
| `report_path_migration` | fresh | 2026-06-17T21:57:21Z | - | 2026-06-17T21:57:24Z | - | generated |
| `generator_runtime_summary` | fresh | 2026-06-17T21:57:21Z | - | 2026-06-17T21:57:25Z | - | generated |
| `report_freshness` | fresh | 2026-06-17T21:57:21Z | 2026-06-17T21:57:25Z | 2026-06-17T21:57:26Z | - | generated |
| `merge_readiness_dashboard` | fresh | 2026-06-17T21:57:21Z | 2026-06-17T21:57:26Z | 2026-06-17T21:57:29Z | - | generated |
| `report_refresh_manifest` | fresh | 2026-06-17T21:57:21Z | - | 2026-06-17T21:56:09Z | - | generated |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `c9931aa8c2c7205af54c69f8737ea29747c076263a46c8dccf298db9c7d678a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `3154830743fe5725e73a64cf314b6cd524e92a19ed0b66bde5167396acafd83a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `1c69add6841262a4421ddf92e78217b1fd2633b366c6b76bbebaba361eb0cef1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `88542a561f0008e648a5d66ef2a0785931e2fd301c0f0a92a3a83f985507145e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `f3abaa425b568839307a5b6bb0a93efbba620f23f0117e5cbd6758e1c568a5bb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `56183b2d1d56dc4902d6290fce5f072d3aa38b4263b9137e480fde577d11d874` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `68b05c96c17a17716eae1400fcfcbde8737b116ad68e9947754d36623e652768` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `b2b936769522f31fea0714ea959bd5fbf624f615ab978b76f176375f3d602db2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `2f27e10348ac56bfb7266e17ab1a91d0565588f77ae0aaf64892b2dbf25d01c8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `3b226e63ddeaea4eab38b982eee9151fa740a258836318c21adc81c5860193b5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `5eb9a018436e2edd12871ccb50aea3f84e08ae00118acfd315399a8f8f7d0512` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `0659b8e11bdfa2e0a7a63cf46722cc8c929f7de4258e365e471adf255c296579` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `33b455ceada395bc04349af5b6914b140a000d93296db983137ee2770d93e027` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `c880f600b890e21cb36db87e0a8fa429493e3042db7e90188221b8d9bf82c060` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `0973c2753c21d2085a5724356db258651404510e5297dce370b88760f78871a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `d0e7888a60f3ffeb197ba50515ccdffca8e8bb074ba1400f40b3475dfb4b9db2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `ce315f609be3496f0baea6dabaeb72659d36af2d517a5c2bb2079cd3f4f09e1f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `b3c85c6a69a7765f4ce926ee89abb2fa444352f6e8b28f199031a985b3401654` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `5af2dd56db978d8414704196dececf85cd691fbbcc654f03c0844c73fb4369a2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `fefb943f14e593e8ad53377e64180d38bd96059372c36dbc8a120e46f4582529` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `2316fe5b7e70ff986d2616f0528e208983f6a5dd4b2671bf443f865c6ffbf26f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `59cff66640760819559d710cda6d350bd97bbaf78e97d86c9fb5aba2c5998a40` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `726f3346965c20d75711a9dcba3c7442b27da57fe80000ff8a928bab18093279` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `fb50ec85c90f10b26ce65db63689d543d153bbcc3fadfcfd1c83e68ff92212e4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `fe88476fc8e20c25bc0dcfc7531fd7de29491acc6de9c7911d645aebb2a93c30` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `1e92fd9298ff8e18ea5bb3dbec6e3eb97252d6ce6e8d00eab2b0cdd8183fd828` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `13efedcf5524f0374b268b8a137905613d2b6d473392671baf0033afc27d213b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `786bfae18dbb72ab5bb70b26ac943af0ee388f7412d6cbc468b408a0999a56a9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `cc4e8d1ab61984bbfa37f314e5be75ceb39c377943382fc219f4c5a43464724a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `99d8f702719fa445234f2fc460f17bb39028e2159d170ac85182ef9b62fe4160` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `87ed3d01f6e9a771170057b3ec9d4914b7365e1021b6317240cb72a401e7f555` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `090fd409f5122e39ac309bbbedeed5b5327748a4654a846e9bc5ecad3ded3165` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `2316fe5b7e70ff986d2616f0528e208983f6a5dd4b2671bf443f865c6ffbf26f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `59cff66640760819559d710cda6d350bd97bbaf78e97d86c9fb5aba2c5998a40` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `81989a156224486e93103ca6f2b22bb0c6991b21f76f72bf0c847a2ae5011b97` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `6e253b13f2efb5a64f8ad9b0b8dc241b804797895618ade0473a6f4bc8d950be` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `2316fe5b7e70ff986d2616f0528e208983f6a5dd4b2671bf443f865c6ffbf26f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `59cff66640760819559d710cda6d350bd97bbaf78e97d86c9fb5aba2c5998a40` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `d39941270b12b850aefb84a407a524f35dbb1853d4ba890c1ceba4c5c21fc322` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `7f32c81caecc23634767fde57f513cb5955b618d6da717d3fc7c80dc03040904` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `2316fe5b7e70ff986d2616f0528e208983f6a5dd4b2671bf443f865c6ffbf26f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `59cff66640760819559d710cda6d350bd97bbaf78e97d86c9fb5aba2c5998a40` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `b237c0433ef2a2d0bf1e4d2bb778d6f7f0501feadebbd3337c99a63d0fe2dd61` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `077614c0c62b0189f845c1bd5974b6c35d7480b6f16226b39ad58f619d3880a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `bf94318ee4981b80cb2d08e43a02a93a0ff4e20ddf22c88e8b79766ac4bb71f7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `248a2e545f702c7a036ef3eecbe0c42c78c6216467a60764eaf555d6e4901670` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `15213b816bf77652e20b9699c24773958abed3cfddca3e4e21c02e73296e8f5e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `8edda8f89635456ce83b4cc9125f7e1e3460ba46a4a94ffca26163a2ad44272a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `7897acaafbcb74c1bdd7052c452a3200be7f34454bf4e67c87ad2e30acf7a5e3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `3a90689b1a18cf22fa3e46b41c3bd8289573e03b6511af254b8af9cfb756f144` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `9cbf88c117020cac2678037f3c566715a10b18c330b44d5ba8a5f1c1ec3c5f31` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `7e75e833b6a4dde5003015245ec134cb5a4ca537c9dea862568e7b5b38b20718` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `538bf1431f1f862bcd57b039bcf7290ac5addc9c41e631707a6fa12550910209` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `29fbd4748fe7eb3ccbd673ad17952db06a9923401dd0862ad9291cf714f633dc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `6d23cc0a735d1a383e9e1f32bfaf3751d0e36db39be96f58b7084422d49a7ebf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `8a3f57c4d0492325416b1025f2c4cbf0dbf16ae7aea407a5416a925b5ee7de08` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `eea11d4e31ff16f2997361464a145d25d7a204249ae38017f4ae4b8be5642949` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `83137ebd31c8a115b7038252ad5c9aa3467fcc7c7984186c3f246af5bbff5729` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `052bb4edb1755851cf582c85dec49a55b90ae6efcf60540a939856343a386469` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `3144f17708c3e5439389a1703a1b433c7001a17996802fde2cf11bd719da6786` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `2c1706a49538aaec952fc352ceca00b8dafa787ad77a418927d9f5cef918ae34` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `916fcf25449577cf80786d2e22cd65764215ef877cdd1cef30f9560566789067` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.json` | `57f13184bbaf008d2b5dc455ea9c47903071b9471d1166edb65937937a1dbdac` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.md` | `ca3e340714fa3b39f6ed1ae679c0bb8c67d035d25b083ad0132cff94e885f7c1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.json` | `e9466aea3d4417e9dbd157f3a7dc4f04fc066bee90aa07d150e240b12fec6609` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.md` | `85fb405853bc3cf99b9f95b418d84fc57cd60720085edd0acb658e9dab7a6ab1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.json` | `9da43b4196c112771f21a29849a3f97b1dc1fc64841488b2cf3a7edb69fb44f4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.md` | `03542155ec6f872c7f007a103002c7e2b643d5b3766b528ce5f9710351b6e780` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | `9ea31b1a01a18d750d360145215d5fb357747182e7e75dd689defa12854380f3` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `reports/testing/test-coverage-overview.md` | present | input file available |
| `reports/testing/generated/runtime/apache-runtime-results.generated.md` | present | input file available |
| `reports/testing/generated/coverage/case-matrix.generated.md` | present | input file available |
| `reports/testing/generated/coverage/connector-gap-summary.generated.md` | present | input file available |
| `reports/testing/generated/coverage/coverage-summary.generated.md` | present | input file available |
| `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | present | input file available |
| `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | present | input file available |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | present | input file available |
| `reports/testing/generated/runtime/runtime-matrix.generated.md` | present | input file available |
| `reports/testing/generated/coverage/xfail-summary.generated.md` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | present | input file available |
| `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | present | input file available |
| `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.md` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.md` | present | input file available |
| `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | present | input file available |
