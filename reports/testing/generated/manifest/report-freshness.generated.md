> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T11:26:39Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `1ed85089212c791958b5f09abf7b17d73bdfde91`
> Framework SHA: `9e2c82b829036d28f54459814773b92c801b6e24`
> Input status: `blocked`

# Report Freshness

| Report | Status | Generated At | Newest Input | Newest Output | Missing Inputs | Notes |
|---|---|---|---|---|---|---|
| `connector_coverage_reports` | fresh | - | 2026-06-16T19:13:26Z | 2026-06-18T07:15:58Z | - | generated |
| `full_runtime_matrix` | fresh | 2026-06-18T11:25:34Z | 2026-06-18T11:24:17Z | 2026-06-18T11:25:34Z | - | generated |
| `full_matrix_job_completeness` | fresh | 2026-06-18T11:25:35Z | 2026-06-18T11:25:34Z | 2026-06-18T11:25:35Z | - | generated |
| `verified_runtime_mismatch_analysis` | fresh | 2026-06-18T11:25:41Z | 2026-06-18T11:25:34Z | 2026-06-18T11:25:41Z | - | generated |
| `nginx_mrts_http500_cluster_analysis` | fresh | 2026-06-18T11:25:41Z | 2026-06-18T11:25:41Z | 2026-06-18T11:25:41Z | - | generated |
| `connector_work_queue` | fresh | 2026-06-18T11:25:45Z | 2026-06-18T11:25:34Z | 2026-06-18T11:25:46Z | - | generated |
| `phase_work_queue` | fresh | 2026-06-18T11:25:46Z | 2026-06-18T11:25:45Z | 2026-06-18T11:25:47Z | - | generated |
| `native_mrts_reports` | fresh | 2026-06-18T11:25:47Z | 2026-06-16T21:14:22Z | 2026-06-18T11:25:47Z | - | generated |
| `nolog_audit_evidence` | fresh | 2026-06-18T11:25:49Z | 2026-06-18T11:25:48Z | 2026-06-18T11:25:49Z | - | generated |
| `response_header_hook_analysis` | fresh | 2026-06-18T11:25:52Z | 2026-06-18T11:25:51Z | 2026-06-18T11:25:52Z | - | generated |
| `phase4_hard_abort_capability` | fresh | 2026-06-18T11:25:58Z | 2026-06-18T11:25:51Z | 2026-06-18T11:25:59Z | - | generated |
| `remaining_failure_analysis` | fresh | 2026-06-18T11:26:02Z | 2026-06-18T11:25:59Z | 2026-06-18T11:26:17Z | - | generated |
| `intervention_blocking_analysis` | fresh | 2026-06-18T11:26:24Z | 2026-06-18T11:26:17Z | 2026-06-18T11:26:24Z | - | generated |
| `no_mrts_intervention_nomatch_analysis` | fresh | 2026-06-18T11:26:25Z | 2026-06-18T11:26:24Z | 2026-06-18T11:26:25Z | - | generated |
| `body_processor_analysis` | fresh | 2026-06-18T11:26:35Z | 2026-06-18T11:26:17Z | 2026-06-18T11:26:35Z | - | generated |
| `rule_chain_semantics_analysis` | fresh | 2026-06-18T11:26:36Z | 2026-06-18T11:26:17Z | 2026-06-18T11:26:36Z | - | generated |
| `final_consistency_audit` | fresh | 2026-06-18T11:26:37Z | 2026-06-18T11:26:36Z | 2026-06-18T11:26:38Z | - | generated |
| `runtime_cache_reports` | fresh | 2026-06-18T11:26:38Z | 2026-06-18T11:26:39Z | 2026-06-18T11:26:39Z | - | blocked |
| `report_dependency_graph` | fresh | 2026-06-18T11:26:39Z | 2026-06-18T11:26:39Z | 2026-06-18T11:26:39Z | - | generated |
| `report_data_lineage` | fresh | 2026-06-18T11:26:39Z | 2026-06-18T11:26:39Z | 2026-06-18T11:26:41Z | - | generated |
| `report_path_migration` | fresh | 2026-06-18T11:26:39Z | - | 2026-06-18T11:26:42Z | - | generated |
| `generator_runtime_summary` | fresh | 2026-06-18T11:26:39Z | - | 2026-06-18T11:26:43Z | - | generated |
| `report_freshness` | fresh | 2026-06-18T11:26:39Z | 2026-06-18T11:26:43Z | 2026-06-18T11:26:44Z | - | generated |
| `merge_readiness_dashboard` | fresh | 2026-06-18T11:26:39Z | 2026-06-18T11:26:44Z | 2026-06-18T11:26:47Z | - | generated |
| `report_refresh_manifest` | fresh | 2026-06-18T11:26:39Z | - | 2026-06-18T11:25:31Z | - | generated |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `396c911ae53a8e0e31e8ef2f673414d5573b76131ab09c82a0d4f9a6fe946ee9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `d2475065444eeb359f53dc528dee9340a306a0e00019c3d007b9cbe57d11ce26` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `45a9b56a87d118189e57affa88c69eb1346c2d1fe059e608b8c66b204ae31d4a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `04be6411c6abe89ec3d2900f2f3e7ff1458cf55c9e1fefb71c18e02750b30f24` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `c39602b8aa8e818b0f9c3f59e1f5ff8abe50ed2b27d6c10623f3bf6bb1d1b0fe` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `33eb51fcfb7be67368ea4088dea9e110c596a4d027a201a4ab16a17480424315` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `568b64889d3b2a7c9651ba478cfb172d873e1cec9391abf9202b1b13704a2db0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `5aadf47046d89054c5d56ff2b8e3cd86640018bedff5776543e96f2f819b38ae` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `3845f1fa86231d82a03fdd3f600ef1eeb39c6e141befa1e8b18457c5f91d4cb1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `632354603d0ef13692d63a91eeac04d37f0d1afed46455fab52330b75e7df07d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `151fed6d47dda6380e0ece49684d4a9c333f464846e3810c5466cbdab5f72950` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `fa5a84d23b5316676319c77f3fba795211369f0fd7d59cc39b380a366a053f7d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `97aec7e6787265828fb40f4b15ed00b6b51ed24c133f1508b0b938385c22bd70` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `219b30168a146c0670d73ac961aca6521d5e5f3345e0bdb656988e4afd4aefe4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `f0b86c64ce32e2bd1ff2a56c6242f01f8d01f8fa4af0fd2801772622c3b62d4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `aea0b37785491fbe2f028b51a3d1ee4b3afeb0bcfa2ffd379feee2514c0e46a5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `2205124a5d719e2992df099b7d1f3fcb75a6452c538df426f75fdba1613497db` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `39be9bc59bd21dabfa50aca9150f78aa45ff88d096587aeef216efbd9aab43ba` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `d7c81f175d60a485129de14484840a7c8ccbe556a26bdddb3a51a6d16817a783` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `d7a4414ad464f0afcbbb41f8daad21128ddb17d0292380c68ffba5977572f9f5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `5b6fb8e3d407cbbd4c7ce9a4769bc036fca39432524e9bfa68a39fbb1bdc4569` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `212986e154c5420f0b63c03094f2e9ad912237951db4961fbfe421a009632296` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `31d0f6dfc4aa566f87a6da28f70d8efb2eac7b67d24614505a76b6bd6b05207c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `45be9aa1d949dcc20856efc2b15dba80a832968e050e04f928e21eabdd800ee5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `bb767fc3587a58a7c5333cfa1b1671e09b5013fb22c5a2f4f0c5d7d12622866f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `3dad209f0b0f1c67cefd3f36f859d3dd7aff135a40d04f0ca89c0d8fa3dba530` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `59804b01d795b35bc8a5c05ecec68a28ab20e93c91588dd57a559306df54ea99` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `25664092d0fe56ab688dbf84826938e8335ee2a7634600791f597a6c5dad70f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `af64a4f7d3a53aa9971f6a9a862d6438d11557d89184fe1114dc24e1ed078cc9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `68f50bdf98786c0455749c00d59699efb481dc3acd1a63c33bec493d2dfbd238` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `10e6a97a5a89f6bb8b0961ff6faed3a24da3c35fce806324bb0ba53739fe8c72` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `99e92b196a6437a9bd9cbc4f08a8ba046d1492c6f3d9645b123bbb04e8a52c79` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `5b6fb8e3d407cbbd4c7ce9a4769bc036fca39432524e9bfa68a39fbb1bdc4569` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `212986e154c5420f0b63c03094f2e9ad912237951db4961fbfe421a009632296` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `fffa02026f90fa941e88d7c22ecd2fbf7368bcecca506962eab3c16ca9cc0eaf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `1e0eb1ce5915c5194bc0c5e230a033b58758cf067c62ff0eec06eefc1831dbfc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `5b6fb8e3d407cbbd4c7ce9a4769bc036fca39432524e9bfa68a39fbb1bdc4569` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `212986e154c5420f0b63c03094f2e9ad912237951db4961fbfe421a009632296` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `7cbd509b1b8604c7ea79e04b617fc8abf4a2671664b863c95fd8b3488717ec05` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `00113a030ff9f3d5c557400b5501f022097af68082a313b4ecce1dda9c44d04b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `5b6fb8e3d407cbbd4c7ce9a4769bc036fca39432524e9bfa68a39fbb1bdc4569` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `212986e154c5420f0b63c03094f2e9ad912237951db4961fbfe421a009632296` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `08e4aec8662e658fc14a44732bbedcdbb1ea401fb075cff0dd22cb3d94d0a0a4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `205f234451dedb129789046c9736aa8a078cb1b980b32b714f88fb853f4b1807` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `8cbf4ad7816be93d057616a8e2dba7146906c56f5e93e4202318b78607b91781` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `c15a140d92e2069fed3463ef1ccdb49b3ef88be1463f41e61e9ea950cd82b41d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `8199f2813c853163a3eddd848421bb327eacf6d75cc1a9e032d1943f5a2112fb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `de311bd909182695cb5eca9355ca35bfb074a68b8a5baafad1953286c365b804` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `00b32aea8d39ea25925f1cf6d91b4833a6c65ee324037c08c52722cb03c273ac` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `938dd2f5865769473f99ddefae127e8cd5d7cf7fe59158d91b2cf50d1bcb1828` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `5b3456d466c5a51e8627240cdda89e321c2aeecd45502b64a2dfec0b5a8a0a75` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `dd5055de9f72f42aaf6c04dbbc8112cf1b3e384a7c2582300bd4f010620c7998` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `8606398f7824743aca1e22f5cb4f6c73cb19c8d434dd7750c7fbc9713d5dd2b3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `dfd9626b6959d00476503d8c77bc5a6e1857ec054dc2ccc8e6ba4737fc478eff` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `3701ef0da41abd31645c82eb2214c5a7269b4485eaee6f261dfe6e338d94ff0d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `4d3ac2d0494a1e8dc580150a88091753d0553ae370c0b0054e5a3afb08ed3309` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `98790eeffd8d0ed96137ec3247f6c13ad3e70470df24bbb873030c5ba6d6eb41` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `5a2ca03b1b70b3667d0540f13432a9de11ef57ade0418406e4cb42dd832a3860` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `62975c957320615abd7c64046652d0016536661f14c6ae37d3716ee4a2b0bac3` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `4e78d26a1dacb3c220c81320eaf531330ab47b95d1f36595ba3ff6bad60d9451` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `85b71692f45ed1cab2940f590a39f18aafc9972405b0f7123b16eb3b1038d7a9` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `f1d0df68847a501270c5f40694cdd9b52d53e101c4cd7c57bc3479e88bfe2d59` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.json` | `1cc5af3025d3631253a599b49626a54fe939f00f81de494b93cadd2f31b27ed4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.md` | `707f58ec4ed022ba9ed38bfb8aa21d34eacf39f35b068086ad3e05762c74b9b4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.json` | `caa7860c727c3afa62cce2650765e704eb30e540b4415cf71abf849b240ec640` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.md` | `caab7da3dff089717221c1573bd4b66e8fe05dcef50a4b8f3d16e7286dbd96c4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.json` | `68f84c0662395f5f9f58c276bb18350c51dd6ceff3a3547205589f463ef82766` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.md` | `c2f7a5c3e4ef17c43cce99288cbb3c73c963753e49e0e113872f2c6466db8413` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | `7c5350734780b26cc9ea3eaa014eb9ceeaf9405ce91ed5aed64a4d00f11a7b95` | `2026-06-16T19-12-00Z-614c8049` | present |

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
