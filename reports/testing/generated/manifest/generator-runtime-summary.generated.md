> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T06:44:38Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `informational`
> Connector SHA: `02d952fa8a986ef519c671973809d7634998e961`
> Framework SHA: `62c5dce8733d77138999bf6054fd4b1ec1712d40`
> Input status: `complete`

# Generator Runtime Summary

| Report | Generator | Target | Status | Return Code | Duration | Missing Inputs | Missing Outputs |
|---|---|---|---|---:|---:|---|---|
| `connector_coverage_reports` | `framework:ci/generate-case-matrix.py` | `generate-test-matrix` | generated | 0 | 2.169 | - | - |
| `full_runtime_matrix` | `ci/generate-full-runtime-matrix.py` | `generate-full-runtime-matrix` | generated | 0 | 0.397 | - | - |
| `full_matrix_job_completeness` | `ci/generate-full-matrix-job-completeness.py` | `generate-full-matrix-job-completeness` | generated | 0 | 0.907 | - | - |
| `verified_runtime_mismatch_analysis` | `ci/generate-verified-runtime-mismatch-analysis.py` | `generate-verified-runtime-mismatch-analysis` | generated | 0 | 5.912 | - | - |
| `nginx_mrts_http500_cluster_analysis` | `ci/generate-nginx-mrts-http500-cluster-analysis.py` | `generate-nginx-mrts-http500-cluster-analysis` | generated | 0 | 0.501 | - | - |
| `connector_work_queue` | `framework:ci/generate-connector-work-queue.py` | `generate-work-queue` | generated | 0 | 4.235 | - | - |
| `phase_work_queue` | `framework:ci/generate-phase-work-queue.py` | `generate-phase-work-queue` | generated | 0 | 1.111 | - | - |
| `native_mrts_reports` | `framework:ci/generate-mrts-native-report.py` | `mrts-native-full-run` | generated | 0 | 0.482 | - | - |
| `native_semantics_comparison` | `ci/run-native-case-comparison.py` | `generate-native-semantics-comparison` | generated | 0 | 0.566 | - | - |
| `nolog_audit_evidence` | `ci/generate-nolog-audit-evidence-analysis.py` | `generate-nolog-audit-evidence-analysis` | generated | 0 | 1.899 | - | - |
| `response_header_hook_analysis` | `ci/generate-response-header-hook-analysis.py` | `generate-response-header-hook-analysis` | generated | 0 | 4.273 | - | - |
| `phase4_hard_abort_capability` | `ci/generate-phase4-hard-abort-capability.py` | `generate-phase4-hard-abort-capability` | generated | 0 | 6.228 | - | - |
| `remaining_failure_analysis` | `ci/generate-remaining-failure-analysis.py` | `generate-remaining-failure-analysis` | generated | 0 | 21.968 | - | - |
| `intervention_blocking_analysis` | `ci/generate-intervention-blocking-analysis.py` | `generate-intervention-blocking-analysis` | generated | 0 | 12.102 | - | - |
| `no_mrts_intervention_nomatch_analysis` | `ci/generate-no-mrts-intervention-nomatch-analysis.py` | `generate-no-mrts-intervention-nomatch-analysis` | generated | 0 | 1.069 | - | - |
| `body_processor_analysis` | `ci/generate-body-processor-analysis.py` | `generate-body-processor-analysis` | generated | 0 | 11.536 | - | - |
| `rule_chain_semantics_analysis` | `ci/generate-rule-chain-semantics-analysis.py` | `generate-rule-chain-semantics-analysis` | generated | 0 | 1.044 | - | - |
| `final_consistency_audit` | `ci/generate-final-consistency-audit.py` | `generate-final-consistency-audit` | generated | 0 | 1.767 | - | - |
| `runtime_cache_reports` | `ci/update-runtime-reports.py` | `prepare-runtime-components` | generated | 0 | 1.59 | - | - |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `44d8b6f5ca1f42d689651e37e166210f29de48ad3524310bb6161580443e85dc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `413809ec6a616e06aa2c093ecf3c902623b019e668bbb8717ca17a4e95cf5718` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `065df397b3da017a321716e51fd2f282d7cd6cc4d5f0bdb7319541e55934353c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `6b779a30f70c113b94b54602bb3b79b5397ec4399125cb36dd4229d7a1334878` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `1a122f2c4e09e7498d6f09aac90c6d4e8a1bdf7ee9cfe80c31b0ce76f871404d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `07f0ef6ab83df4f5ee20c1ed5f99998e65f60071f9504437ada4e34e6d5bd680` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `af82e294807d56476b17548d3f12f8958120124006fd6cb9c68919f74c36a3b0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `1ece47889904965f7cff2af0be36c362cb45f09a41b69eb5979d052665ac935a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `75e960a3ba5abd3ccd8289b5daded9b6d401467fc237f2392e6571153d816e9c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `8dda11973a9a23654bb889cf506f5f0ceae724cac4db2ca63288c8eae03f43a2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `fdaa878e3a9e246ae057fe7b46c2208f20c4aa87cc7fbf1e679467bfcfe69d25` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `55652e2ff4a0018ba14b8a35ddba83e76413269adf4e8cba7295cbdefd69eb35` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `3f11d1fce15cdfa561cc96ef730cbd1b5604528e8f8a7fa8b2e7209629377e3b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `a0a64bba5bc50ad6d22550f8b0fe7b5908177766804876c086f3c23f8056584a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `6934388824f6a335f3ffb3e8282b0c0ec98d28b3e466b9bce7266e9db3b5fcd4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `1b94a278dc3d14e65463e9293d600578d7239225fed9c5a5b3516aa35fbc2d3b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `8a3dda4419efa2b084634d6d6f1f492fe8c88bd6c18510f5199e5cd9e6d82483` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `d2519f6a6252051ad8f42a786f66a3fcbf4d2cd1147b0c23bf6504c87368aee8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `e270fa2d3f5496b6f5013accb531e9f467fb00871beb7a6c42ac32b45e757676` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `22e10369b2612ee1b3b600d90206a90fe9f6bbdc88e96cdc1e41dd11b50ec6e2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `d0ee4bf5ca82cf279209d179703f7b15f244056edd31451b42c708b9e3083c13` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `918d660a1b580a5ae66d337ee310dfc7970d69eee9bb671ecc65195abeb28625` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `9453c36fa4b13cc8c83bf1685870217f9cab3d1aaf4c248092492c8f32e6605c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `f5fb8888bc9f284192cb876ffcb8fc5b6d2943ae45271ce4165d6494602b394b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `6f80c01c4e5af53144685e17d1cb95a4416862f6a2a04b2b79cb5d87b08bdc48` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `a085a8239c6600ce573a92a9e981d7c9ef26e6d3a7c61e4941d7a58ac82cc781` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `6da3160351259ac1f864890e3666c2f2f7acd4c8eebd06e1a3df5d0b85f67550` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `537e4088af2aff8afd422a8d67cfa0c4d6e3ab5722e225eed01e5f62ddac9b7a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `8c51a5df1cf88c5ec3f9476ef02fa02740e5bf5bf598214a5adc76ad80cb90ea` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `e91198abecabf6390883fd3a5e17f6917b1818d891149c3af3e5464e5b0d4541` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/native-semantics-comparison.generated.json` | `c6cf3c4621f53a0a239eaaa60a2db0fc549e09c3bae455d1345d11dabb947f46` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/native-semantics-comparison.generated.md` | `742d4efabdc1317a615e4d02c8e3c3aeb4a45278a6c930b14412684363a5030f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `5ad62e74b8ef51eeb42d850915db370c3a022fb2a9360746653e31e002fa1050` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `c4897c8b412f027db73c2ef7caf1dfa6b67633cc265719e2ddaf5cc3d1326f5e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `d0ee4bf5ca82cf279209d179703f7b15f244056edd31451b42c708b9e3083c13` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `918d660a1b580a5ae66d337ee310dfc7970d69eee9bb671ecc65195abeb28625` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `dc5776468070e81d00ed9f7ffcab971cc7acbaec79be0773aeb6155f2ea4bd0f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `fc62b99839b47b490d9e869fa9f947b5e728884fd4e9b2bcae2ddddc7799fe90` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `d0ee4bf5ca82cf279209d179703f7b15f244056edd31451b42c708b9e3083c13` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `918d660a1b580a5ae66d337ee310dfc7970d69eee9bb671ecc65195abeb28625` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `c581b8a0265c7d0ee7f7f7f6258facb4699b4729c992080a94e4e3c015e235d4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `39226463371c67751b80b7236a99ca7d1f4c9fda09dfbc55005826cba6374695` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `d0ee4bf5ca82cf279209d179703f7b15f244056edd31451b42c708b9e3083c13` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `918d660a1b580a5ae66d337ee310dfc7970d69eee9bb671ecc65195abeb28625` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `40bf2a3a4325fe9e0dba795d48c4153b1b633d936212a809adce08387261ed80` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `3c4d90d3161f66b740144ad7560c1638742fe3978d24eed16694129d1b0222a6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f264523d6bb83b4a3382d4871099d221aac496d36dc8697548b4bba10fd2e52a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `f3aeca61fca5cbf925f06cd42d132af426adff0aba0d5fc06952bed384780981` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `e90c02f636c5b356c7db009eb39b4997c83b6db20d64fc90f796fec9ff3083e8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `3f85eed8af807434fe97b85ff4a51cf65ba8324b2ca03ccbe34f3ed53a310439` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `ba3c88e495c93ac7a05a48a1726a7ec7f73ecda79f22ce7fdff2af83a87b7d35` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `3982b9726c67200c5f318ba0e0d38cecf861e42dc92b2b886fdd61649448b595` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `100fe560747e0b0fbe0d5072e347fa85377e2be8e4088bcd8c0d739090f91bcf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `1617c559d746ff239a81ee74fd19b29161d81b5d931fe63b01a135f89a305310` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `60148b03389c8e40f20dac5d459f14f8761a4f373646c03c67d7bb3223629c27` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `f58382dd4ed5b6e7bbdc4a52186294be4599c2ce2220672ddcb455380ba1dd58` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `28a7cb799c7fcdd659c63bf564a4267989079df75b3bd40005416b1e2a940638` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `a704cd11c8bd8d38314abc6d102bd2f1282a36f0f05538f3be0a3e7404147107` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `90c84d11f426f45af700e33fe389db832ba4f8e5da315459af31e5903c0ff77a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `d0d4b6d21a136157a66198425f8ed7f0049cf350ab99d7415acca1bef0c44b0c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `27f02abcb1b59bb628bf1356c540b4da0c29b8b04daeae5fe17d566831579b21` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `4937b30f1089adecd505620230834ce6813e77319d3a3b26473647cc1e6939b6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `828bef8d3b3e7007337b6960c235f38f2499f19502bd145aba6bba8c5f7dcc89` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `f1c8e3f25691ba921dfc7b993dc491d8344190ca09ba4aa094e7d0201de1b9ee` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-cache-index.generated.json` | `a716c7a131f108c02f1177d6732a1e04d709d2f290b4f991f8480143101538a4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-cache-index.generated.md` | `48aada9345fbd7f3ce2db66e3fe44e8a7abb5d36e9c7778d06bcd45d39c70f90` | `2026-06-16T19-12-00Z-614c8049` | present |

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
| `reports/testing/generated/manifest/native-semantics-comparison.generated.json` | present | input file available |
| `reports/testing/generated/manifest/native-semantics-comparison.generated.md` | present | input file available |
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
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-cache-index.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-cache-index.generated.md` | present | input file available |
