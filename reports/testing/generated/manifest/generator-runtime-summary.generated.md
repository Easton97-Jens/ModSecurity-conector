> Generated file - do not edit manually.
>
> Generated at: `2026-06-16T18:58:49Z`
> Verified run id: `2026-06-16T16-57-44Z-b53340a8`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `informational`
> Connector SHA: `b53340a84f9acd5fbc3aff3de136c92ac122c3fa`
> Framework SHA: `2b2e402708fca5ff40664926ff01c2c5e520a48a`
> Input status: `blocked`

# Generator Runtime Summary

| Report | Generator | Target | Status | Return Code | Duration | Missing Inputs | Missing Outputs |
|---|---|---|---|---:|---:|---|---|
| `connector_coverage_reports` | `framework:ci/generate-case-matrix.py` | `generate-test-matrix` | generated | 0 | 1.997 | - | - |
| `full_runtime_matrix` | `ci/generate-full-runtime-matrix.py` | `generate-full-runtime-matrix` | generated | 0 | 0.33 | - | - |
| `full_matrix_job_completeness` | `ci/generate-full-matrix-job-completeness.py` | `generate-full-matrix-job-completeness` | generated | 0 | 0.691 | - | - |
| `verified_runtime_mismatch_analysis` | `ci/generate-verified-runtime-mismatch-analysis.py` | `generate-verified-runtime-mismatch-analysis` | generated | 0 | 1.736 | - | - |
| `nginx_mrts_http500_cluster_analysis` | `ci/generate-nginx-mrts-http500-cluster-analysis.py` | `generate-nginx-mrts-http500-cluster-analysis` | generated | 0 | 0.35 | - | - |
| `connector_work_queue` | `framework:ci/generate-connector-work-queue.py` | `generate-work-queue` | generated | 0 | 3.83 | - | - |
| `phase_work_queue` | `framework:ci/generate-phase-work-queue.py` | `generate-phase-work-queue` | generated | 0 | 0.877 | - | - |
| `native_mrts_reports` | `framework:ci/generate-mrts-native-report.py` | `mrts-native-full-run` | generated | 0 | 0.487 | - | - |
| `nolog_audit_evidence` | `ci/generate-nolog-audit-evidence-analysis.py` | `generate-nolog-audit-evidence-analysis` | generated | 0 | 1.36 | - | - |
| `response_header_hook_analysis` | `ci/generate-response-header-hook-analysis.py` | `generate-response-header-hook-analysis` | generated | 0 | 2.282 | - | - |
| `phase4_hard_abort_capability` | `ci/generate-phase4-hard-abort-capability.py` | `generate-phase4-hard-abort-capability` | generated | 0 | 3.454 | - | - |
| `remaining_failure_analysis` | `ci/generate-remaining-failure-analysis.py` | `generate-remaining-failure-analysis` | generated | 0 | 11.734 | - | - |
| `intervention_blocking_analysis` | `ci/generate-intervention-blocking-analysis.py` | `generate-intervention-blocking-analysis` | skipped_stale_input | 0 | 0.941 | - | - |
| `no_mrts_intervention_nomatch_analysis` | `ci/generate-no-mrts-intervention-nomatch-analysis.py` | `generate-no-mrts-intervention-nomatch-analysis` | blocked | 0 | 0.257 | - | - |
| `body_processor_analysis` | `ci/generate-body-processor-analysis.py` | `generate-body-processor-analysis` | skipped_stale_input | 0 | 0.898 | - | - |
| `rule_chain_semantics_analysis` | `ci/generate-rule-chain-semantics-analysis.py` | `generate-rule-chain-semantics-analysis` | skipped_stale_input | 0 | 0.647 | - | - |
| `final_consistency_audit` | `ci/generate-final-consistency-audit.py` | `generate-final-consistency-audit` | blocked | 0 | 1.257 | - | - |
| `runtime_cache_reports` | `ci/update-runtime-reports.py` | `prepare-runtime-components` | generated | 0 | 0.218 | - | - |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `bd16d5153ccc31ebaffbc51fa6ac1090ebea8056250674fc0b1d35eabb5fcd6c` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `c1f12bcc85c917be8b90b7b216887c2d9555da289d3cb3b2c375126db06119c5` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `fd95d7d06a493220652899f6b26670bdf5430e57274bfd341939a7aa41d23eb3` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `2f9f70b1ed4bc6db3603c914d5843afae696b447df27a5c15d20c51ccce4bbdb` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `4fd07d51770ad9b65e1b7fd923f35e3a4a9befd3df03c47eb0639d2f2889ea74` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `05692ba1e23af7e123e1bebcf864af3f12847c7810c9c4c834480d0b8334c6ec` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `521746eedbfcada92ab17f4851e2d74d5079e4de3759751ef6c6ce45bc2728f2` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `27f5f0cdd2b94697fd5bea41e8e39bbc5f3463d3a53931eb8abf5002b910075d` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `0af0602e7438c0350400f3e38fbc2505858a81983c9bc022ddaf6f6d403c37cb` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `a93ca07ce1d8ba33b13703dff39bc0c228e092d8d0d0e94bf15adb29d9c3ed7e` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `f2c570c502a53acd154797e1b2b9bc6d6b2b49f76de90402a9a13b3d47d5077d` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `9962f5c723c5514d01acd68996a36975c077684069d883738f6143ca3b0641b9` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `b3ac7d2737b2859e60b8a624cd1e5500fffda8052a874d3c47dafdd35d47d07a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `0dc7e590d3a8fb06083fc10e09fa7819dd27ab03e2c2ab2e708222c0fb4745c9` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `5a46b78e9b0b07805bfa70305a7f2fb7f907511087e8952d7ee18b91f6e9f5bb` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `5ba3e0d19bcb8231dd04327d4dd7ee515b60008a128ac17c7f562bebd5a2004c` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `2350fd5058f2b74bbfdf43204d4dba5f7afbf741e7b55fce3c52e3fc2dec8424` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `cd1abe07313142907fa75d6a42d5c8040c0af2bcff1a35a3e57a9881d038fd71` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `ec37c9971529b06b80763ce9c360dd9164c46f80f63e8d69526854253daf7e7c` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `55ca656b2626c5efb59d44775f50c375db48c6b3c8bc46fd7498052664625ff6` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `36f90db93c8a3a554305350d2a745835c1a9d8773742ef5359192beb364299ea` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `c50972930e23e8b469ca09cb94eb12ecb67fabe11bcd176c5669c1c8c7270b32` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `5627c6b99f6285289d7685b2857e0b33bba2c97e2517531776f34bc5f6a7832a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `20d4868784094571e3c9d7862146346029b2b95ba6c60e0283a67a5e8b9fac14` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `cf4fc89931e535da77cd91f57eda28d65fdeb44a3af07c568303a87db7c8867a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `ea7446449e31098726416e15443d5d568489b91ca647383e3c7bd4f1a62d21bd` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `d1d6c1592ae4287cf93001eb543aa75d99dc4ef267489498737f470fe5f9fa6a` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `3ad6ecde3c132c51ae504943d3b5d695f50a6efc3e4920e94fd9878d452e43ea` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `56f68e0495da29c03f847d077d74a6f79b2608c9624f3217a2f725e28d953644` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `1c7f98f30dbd8e0e136ca9b471d49adada6559ec89620e31ad4f77ddf689db29` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `88c93af067aff9d0039f0fdb70588e0b760ba950e249375081b65ef346d318b2` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `531396bacd4da44b833e3346edc9ffbd97abdd949f9bc04c058592bcaab94d22` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `36f90db93c8a3a554305350d2a745835c1a9d8773742ef5359192beb364299ea` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `c50972930e23e8b469ca09cb94eb12ecb67fabe11bcd176c5669c1c8c7270b32` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `29a64da4865de4f551ffd230b36ce8c8ff8261e43c1d88ecfac1ca8249b9bd43` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `e7495a525a27aecfdf775d18fb0ea94481a01734faa219f48045b48e96779499` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `36f90db93c8a3a554305350d2a745835c1a9d8773742ef5359192beb364299ea` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `c50972930e23e8b469ca09cb94eb12ecb67fabe11bcd176c5669c1c8c7270b32` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `5bc32041708470287a9581441360673a6d1ecbfffa00cdc32eb25fed93aa3cb9` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `57382b0ca57cd6884e67afb132a336deacee9dd9d4357a4d1b7f70e4e1429799` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `36f90db93c8a3a554305350d2a745835c1a9d8773742ef5359192beb364299ea` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `c50972930e23e8b469ca09cb94eb12ecb67fabe11bcd176c5669c1c8c7270b32` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `7bbf04c71c0bf6a56e892371205db4618f97e091458c0073ac41952a956eb205` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `8a37211e958c222022f4b917a1f9d3070b08f7d79a346ddba7bf2b80406d06b7` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `f6134d5f7cc94e181c222e627cd7b4f3bb0a95a9ef85e0b63fb5b55b85268560` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `86220ee5fac8980e53d20d60554f2c46e538365cda9908838f69dcf7a81139bf` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `dd74444ee2dda65ac29c6c32ad15aa9592fbb95ad095f607e1b02e03b309e6d4` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `3ea2d1500daa3dd446ad0809b009266b3b1843973c6b38d6ebd5c34827e2fcf2` | `2026-06-16T16-57-44Z-b53340a8` | stale |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `a20c5dd83c2a4ab1b072d6f61a472e55a675a8be48212b1bf108621e052f6e69` | `2026-06-16T16-57-44Z-b53340a8` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `bf1b1e48e8eac9b186f45bf5e0e00488ffe8ea369e78d9bb914ef445c0efc31d` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `b3e54024c30f3b3a31a5800714e6b65658ec01f5610a39560b5d925e5fccf07b` | `2026-06-16T16-57-44Z-b53340a8` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `a4024dbc28077ed1f1a539ca361542e6fe0ae20c03df797dc94f95ac0c61c851` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `bca39fdc9484e13668b49c73a89db6f0e90ac73d976d8c125d5e49a80591d447` | `2026-06-16T16-57-44Z-b53340a8` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `bc160a392c004aca0b9eca2e9d5d9d55e46c7c50ba1bf79fe6287094b105a00f` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `34c111cc26bc25e09ed6d820ef127bdd830bd55a76e896ebf7fc6f8cd39cd06e` | `2026-06-16T16-57-44Z-b53340a8` | skipped_stale_input |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `d8e9ba2ff3e90ce0b530ed79bd72e40ef4883e7c0012cbd95c618e1b725322ea` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `8086864d8051f96776b54d45482eaf4b02e220dedc3ca191547c119ecfc4419b` | `2026-06-16T16-57-44Z-b53340a8` | blocked |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `720a3e47a70a25917e92101cc14c9d0668859134ae54285e5d0795021680ee3b` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `bd47303437524a77a8b31743668e6b50041f176dec683c2efe25737f6d0d8ef7` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `556aa3ee961759324a4ba78f12c40ad004ffcce38b3338e5d15c27d24868ef55` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `58c14894ad3f824f4aaf66730bfa8af0beefaae7674039e3e813c67542cadf54` | `2026-06-16T16-57-44Z-b53340a8` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `8e24e9c936f04c47084173b2a0db9e9605522aa78008cfb8de1e39fc6a5c502d` | `2026-06-16T16-57-44Z-b53340a8` | present |

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
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | input file available |
