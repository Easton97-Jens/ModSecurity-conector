> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T16:22:44Z`
> Verified run id: `2026-06-15T21-01-39Z-9391a8d0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `informational`
> Connector SHA: `efac6d66d0e165af8d6e1b5404083d5f50601327`
> Framework SHA: `04e31a60676eebba86be2a4c1510ff596e37ba2f`
> Input status: `blocked`

# Generator Runtime Summary

| Report | Generator | Target | Status | Return Code | Duration | Missing Inputs | Missing Outputs |
|---|---|---|---|---:|---:|---|---|
| `connector_coverage_reports` | `framework:ci/generate-case-matrix.py` | `generate-test-matrix` | generated | 0 | 2.079 | - | - |
| `full_runtime_matrix` | `ci/generate-full-runtime-matrix.py` | `generate-full-runtime-matrix` | skipped_missing_input | 0 | 0.121 | BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | - |
| `full_matrix_job_completeness` | `ci/generate-full-matrix-job-completeness.py` | `generate-full-matrix-job-completeness` | skipped_missing_input | 0 | 0.122 | BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | - |
| `verified_runtime_mismatch_analysis` | `ci/generate-verified-runtime-mismatch-analysis.py` | `generate-verified-runtime-mismatch-analysis` | skipped_missing_input | 0 | 0.116 | BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | - |
| `nginx_mrts_http500_cluster_analysis` | `ci/generate-nginx-mrts-http500-cluster-analysis.py` | `generate-nginx-mrts-http500-cluster-analysis` | blocked | 0 | 0.174 | BUILD_ROOT:full-matrix/full-runtime-matrix-runs.jsonl | - |
| `connector_work_queue` | `framework:ci/generate-connector-work-queue.py` | `generate-work-queue` | blocked | 0 | 0.139 | - | - |
| `phase_work_queue` | `framework:ci/generate-phase-work-queue.py` | `generate-phase-work-queue` | blocked | 0 | 0.194 | - | - |
| `native_mrts_reports` | `framework:ci/generate-mrts-native-report.py` | `mrts-native-full-run` | skipped_missing_input | 0 | 0.436 | BUILD_ROOT:mrts-native/apache2_ubuntu/job.json, BUILD_ROOT:mrts-native/nginx-pr24/job.json | - |
| `nolog_audit_evidence` | `ci/generate-nolog-audit-evidence-analysis.py` | `generate-nolog-audit-evidence-analysis` | blocked | 0 | 0.199 | - | - |
| `response_header_hook_analysis` | `ci/generate-response-header-hook-analysis.py` | `generate-response-header-hook-analysis` | blocked | 0 | 0.2 | - | - |
| `phase4_hard_abort_capability` | `ci/generate-phase4-hard-abort-capability.py` | `generate-phase4-hard-abort-capability` | blocked | 0 | 0.346 | - | - |
| `remaining_failure_analysis` | `ci/generate-remaining-failure-analysis.py` | `generate-remaining-failure-analysis` | blocked | 0 | 0.584 | - | - |
| `intervention_blocking_analysis` | `ci/generate-intervention-blocking-analysis.py` | `generate-intervention-blocking-analysis` | blocked | 0 | 0.252 | - | - |
| `no_mrts_intervention_nomatch_analysis` | `ci/generate-no-mrts-intervention-nomatch-analysis.py` | `generate-no-mrts-intervention-nomatch-analysis` | blocked | 0 | 0.223 | - | - |
| `body_processor_analysis` | `ci/generate-body-processor-analysis.py` | `generate-body-processor-analysis` | blocked | 0 | 0.223 | - | - |
| `rule_chain_semantics_analysis` | `ci/generate-rule-chain-semantics-analysis.py` | `generate-rule-chain-semantics-analysis` | blocked | 0 | 0.222 | - | - |
| `final_consistency_audit` | `ci/generate-final-consistency-audit.py` | `generate-final-consistency-audit` | blocked | 0 | 0.508 | - | - |
| `runtime_cache_reports` | `ci/update-runtime-reports.py` | `prepare-runtime-components` | blocked | 0 | 0.301 | - | - |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `5c8096063ef4627fe301c55db152507274507583728ddfe1d838c120bdeaa911` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `98e18743ea72bc3612c38579e9773e476b4f1f87a5ef4abb40a2b77d043a1354` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `f690ddc52b561e1ada7033721f31f30b5872bef42df24d4eb7b8293cbfef32f1` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `b2c3e9696f107a251d2c872fec9ea43eb50c480e5bfd44af58bd0225308eff7c` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `d5c65e112c925f145e731e4c6d4db55eed3f2c2f2562c464b5140f459aaa7a93` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `414f90aa0d3f48d1c3a1128eb3871f5e78fd32dc3788e48fb2e01b58ccc2d3aa` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `71e5b1be73172d7cded78857db29c85449f59428ad16c1cbd20d81c1a814ac2d` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `75d0fb7a0bcfb37d68d44de8bc6fb57e0b624e00e460eb5fbc080a79d2653ae1` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `5c8196c192325c5c2e3dbe695659ae459ac87ec920b35c57dc33c06d9b6be24f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `5d092ca5c350995fd6f0961a44d7b484a666fad75efd8b080c635c4ec7c04277` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `74dff241151f409d4a958eff005fd65b7e0dc5e03a886ad44bcfc2084e52585f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `91b59897b970d43b45a76fc5417b02d700071dc794fd416a925cd24170c96c91` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `a630cb38023a9bfbf47b87e513fc640a176497b5f16a3e5c94b49aa78a54079f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `b938b94e2b9dab8a36b89a4114c5dea70ded6c6bb870c41a23e2ae48c2df146d` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `052ecc3d98a7bb1608fdfc517a762d02386ddb4a648c000fdcc54a38fc291d80` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `d06a7a4f11f2ba8c655f0762514995238d429221d3881a8ce9ef8d201e7f7a2e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `36feb9c7543606b80ed2d17e428a9f4d5d19f5ce8c056a60d6cdd7d364431abe` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `ad2e565f9258aefd89313bda085d9c8d9c940c2ec55efe46adc8a2668d55df1f` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `3f570cdeada65c05b87f63069c1ed107b78dc1bd2159566a8dfa718b8d8bbfe7` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `c137b0121f16b4038e070461f51eaa7cdf488a61283ca292593731294b34abb6` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `cc2e3e94ad36ce80f8675c014493a35a11238ec6e4b008cafedf021486ce8010` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `bad7b355c9466f573b8e9a343a1a0d229e4ea2257c315ac0ca22b1e47e2a344e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `1b9a3341dd987c09a9f65b2f324a3a4375b7795ca37fd7aa1bf296fc8ba6a4e5` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `a48855057e42c898afd19c25a6392b09f6ac032af709564c9ae798235b7dbcdf` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `3f29f03f5e41e041a7f4a072fcf20441401b7633f1afc6f62cd9f6ed9c45785f` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `666d7238f00a9b85e5cf7821052045f01fc6b33b57850495ed9fee9da10188c9` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `17994ec83ca33c03a84eabd97f494c7a706cef28658c68de50699fc6c160b8b4` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `fb6e8cdc3b1d55c8e1a7b31973d2cbab6055a81faa0d8a5867119efc3955da42` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `fa93fe73005003fce1a16fc8d3fb9c1f3288c15b21b8b9d47b9d5d83f354b776` | `2026-06-15T21-01-39Z-9391a8d0` | skipped_missing_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `d976abef9c4452b17cedc3c50a9f6d0a60255211c7912212e924b288f44b4d55` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `af894d4043bf85d6b941b2c9a5b76b8060bbbb484ed37908547139b5f3fed198` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `379ea58307a0be763c5ae4b0b1d40b8a07b9e506019580d4043c9d716b9934d5` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `cc2e3e94ad36ce80f8675c014493a35a11238ec6e4b008cafedf021486ce8010` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `bad7b355c9466f573b8e9a343a1a0d229e4ea2257c315ac0ca22b1e47e2a344e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `c12403d7b77b18bfe9928c9277475659867790c26f2419cd6c18361a9dc89f7e` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `6e72813c13364ab01bf24d14c2e2add7e61ee41456a14bccf43e1ca2ad4fe4da` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `cc2e3e94ad36ce80f8675c014493a35a11238ec6e4b008cafedf021486ce8010` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `bad7b355c9466f573b8e9a343a1a0d229e4ea2257c315ac0ca22b1e47e2a344e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `c04d82c7d4ee21f85bee1ab24642054bf72d53e2053bad7a9df62a148ecc4bad` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `96b05c599c47721e0914f3fd6fe3689b73ca4a64ed0480404256b65502a72131` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `cc2e3e94ad36ce80f8675c014493a35a11238ec6e4b008cafedf021486ce8010` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `bad7b355c9466f573b8e9a343a1a0d229e4ea2257c315ac0ca22b1e47e2a344e` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `b2226fe0c3e25f3ae3650ce97c77f43f7c2dee694fad2403544b1279942286b3` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `99a84f5c023b9f6c49e1d65fb4d08e604be969f55a4a9dadc8a16d1000793561` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `c27eb0b4dfb6334be9af6aa87597368c2107b924b11689250583fba45df4b7f2` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `f00b69081fe304d467e7c86d0909dade01de83d23864d834d11fc0448558fb39` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `99c88712991be652654f3fb3818eec7bc1a0635b1c43fcd0c548a40a00a16133` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `2def7e673bcb4f9730579be7663f59d2574a8536b92cee5e847dc34be89c525a` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `fbbc2c097a08c4b99471215a7fde4ad77b5536577aa6783479f264540a31fc14` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `a791b2609c6942323a88a4f7c443c3eaa8c19029f0073b32a9f4e2a0b1189e29` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `15b3149cfa94cab5a1f62cb6f424104eaf740569ba26844b370e7604d9c46aeb` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `927a1f483592200c85ca5b2ffb9298080bfcf09dbf763d1de1b0ecc11252037b` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `41b01c37817133fd26edbb881422128c0c58a3c957a22f3bfd5a63756d58b766` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `038489f4f56ad85e445016d6ad170a2ac5fa7d15dd81abd4eacebe7307986c9c` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `a5c6dbf0e44c0f3a069ea9d8277619a6f8045e7ccf0802dade28b710ec91404b` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `72fa302903468b38debbd85f7e9feac68f380a48acbd99fbe748027c1320338b` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `21f2c11040b4c146bdde0a6edec38176b65393d39e564398a6cc64773ec0855b` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `eff9f2ebc5bc406da681de63a097da8265af0b33a9e44fd209b405c8bf63ede6` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `66036d9685b85b9c3b33dc0ea98bfb11949af2ab20a405fc78cf01186a420738` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `d85c7234e071eed5fe8e597729d51e0bb51053dd588f7d2c2cdfbd7a0b0f1384` | `2026-06-15T21-01-39Z-9391a8d0` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `1a1153884a8b455e7776c4e34a791a3720aefde40c81cfaaf328eb556d4b7d70` | `2026-06-15T21-01-39Z-9391a8d0` | blocked |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `12cacf639fda9027229321108365f4ee29b1d3f504b392e36ac7b55f97e354ae` | `2026-06-15T21-01-39Z-9391a8d0` | present |

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
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | present | input file available |
| `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/connector-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | skipped_missing_input | generated report input is not usable: status=skipped_missing_input |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | present | input file available |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/next-fix-plan.generated.md` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | input file available |
