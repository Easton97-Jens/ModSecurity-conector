> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T02:40:22Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
> Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `complete`

# Report Refresh Manifest

> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`

## Summary
- Connector SHA: `614c80493b6ebd25a17e1d27979071e5e30584d4`
- Framework SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
- Framework submodule SHA: `24509c107ecf3a22ae9d69875f661690bd6fb95b`
- MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`

## Inputs
- `full_runtime_matrix`: `60a3912caa936f9e6f590ccfa97f62ef56e443d26ecbb66995675468922eddc9`
- `native_mrts`: `7e157457e8784df02207aa2c2d21a3d474d7079b2d182ab72dc981b3b4e4922a`
- `build_cache`: `3a1dbec4eb041664b794b826f247d07be7db658975c0a5cf01e4100fbe789bfc`
- `component_cache`: `a5d2d543de8ce0c9a473daabcaf0c4524c052ef84b9d60604fcc66bb661c4cf9`

## Verified Commands

| Command | Status | Return Code | Duration | Log Hash | Notes |
|---|---|---:|---:|---|---|
| `-` | not_run | - | - | `unknown` | No verified command file was supplied. |

## Submodules
| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `614c80493b6ebd25a17e1d27979071e5e30584d4` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `24509c107ecf3a22ae9d69875f661690bd6fb95b` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Reports
| Category | Owner | Severity | Report | Generator | Target | Status | Return code | Duration | Freshness | Outputs | Input status | Missing inputs | Missing outputs | Generated at |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|
| mixed | connector | informational | connector_coverage_reports | framework:ci/generate-case-matrix.py | generate-test-matrix | generated | 0 | 2.0 | fresh | `reports/testing/test-coverage-overview.md`<br>`reports/testing/generated/runtime/apache-runtime-results.generated.md`<br>`reports/testing/generated/coverage/case-matrix.generated.md`<br>`reports/testing/generated/coverage/connector-gap-summary.generated.md`<br>`reports/testing/generated/coverage/coverage-summary.generated.md`<br>`reports/testing/generated/runtime/haproxy-runtime-results.generated.md`<br>`reports/testing/generated/runtime/nginx-runtime-results.generated.md`<br>`reports/testing/generated/coverage/phase-coverage.generated.md`<br>`reports/testing/generated/runtime/runtime-matrix.generated.md`<br>`reports/testing/generated/coverage/xfail-summary.generated.md` | complete | - | - | - |
| canonical | connector | critical | full_runtime_matrix | ci/generate-full-runtime-matrix.py | generate-full-runtime-matrix | generated | 0 | 0.365 | fresh | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.md` | complete | - | - | 2026-06-17T02:39:19Z |
| manifest | connector | critical | full_matrix_job_completeness | ci/generate-full-matrix-job-completeness.py | generate-full-matrix-job-completeness | generated | 0 | 1.039 | fresh | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json`<br>`reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | complete | - | - | 2026-06-17T02:39:20Z |
| manifest | connector | critical | verified_runtime_mismatch_analysis | ci/generate-verified-runtime-mismatch-analysis.py | generate-verified-runtime-mismatch-analysis | generated | 0 | 2.432 | fresh | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json`<br>`reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | complete | - | - | 2026-06-17T02:39:23Z |
| manifest | connector | critical | nginx_mrts_http500_cluster_analysis | ci/generate-nginx-mrts-http500-cluster-analysis.py | generate-nginx-mrts-http500-cluster-analysis | generated | 0 | 0.42 | fresh | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json`<br>`reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | complete | - | - | 2026-06-17T02:39:23Z |
| work-queues | connector | important | connector_work_queue | framework:ci/generate-connector-work-queue.py | generate-work-queue | generated | 0 | 4.184 | fresh | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.md` | complete | - | - | 2026-06-17T02:39:27Z |
| work-queues | connector | important | phase_work_queue | framework:ci/generate-phase-work-queue.py | generate-phase-work-queue | generated | 0 | 1.153 | fresh | `reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-17T02:39:28Z |
| mixed | connector | informational | native_mrts_reports | framework:ci/generate-mrts-native-report.py | mrts-native-full-run | generated | 0 | 0.495 | fresh | `reports/testing/generated/mrts-native/mrts-native-full.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-full.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | complete | - | - | 2026-06-17T02:39:29Z |
| focused-analysis | connector | informational | nolog_audit_evidence | ci/generate-nolog-audit-evidence-analysis.py | generate-nolog-audit-evidence-analysis | generated | 0 | 1.824 | fresh | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json`<br>`reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-17T02:39:30Z |
| focused-analysis | connector | informational | response_header_hook_analysis | ci/generate-response-header-hook-analysis.py | generate-response-header-hook-analysis | generated | 0 | 3.744 | fresh | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-17T02:39:34Z |
| focused-analysis | connector | informational | phase4_hard_abort_capability | ci/generate-phase4-hard-abort-capability.py | generate-phase4-hard-abort-capability | generated | 0 | 5.703 | fresh | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json`<br>`reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-17T02:39:40Z |
| canonical | connector | important | remaining_failure_analysis | ci/generate-remaining-failure-analysis.py | generate-remaining-failure-analysis | generated | 0 | 21.248 | fresh | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.md`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.md`<br>`reports/testing/generated/canonical/full-run-evidence.generated.json`<br>`reports/testing/generated/canonical/full-run-evidence.generated.md` | complete | - | - | 2026-06-17T02:39:43Z |
| focused-analysis | connector | informational | intervention_blocking_analysis | ci/generate-intervention-blocking-analysis.py | generate-intervention-blocking-analysis | generated | 0 | 6.615 | fresh | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | complete | - | - | 2026-06-17T02:40:07Z |
| focused-analysis | connector | informational | no_mrts_intervention_nomatch_analysis | ci/generate-no-mrts-intervention-nomatch-analysis.py | generate-no-mrts-intervention-nomatch-analysis | generated | 0 | 1.285 | fresh | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | complete | - | - | 2026-06-17T02:40:09Z |
| focused-analysis | connector | informational | body_processor_analysis | ci/generate-body-processor-analysis.py | generate-body-processor-analysis | generated | 0 | 9.233 | fresh | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | complete | - | - | 2026-06-17T02:40:18Z |
| focused-analysis | connector | informational | rule_chain_semantics_analysis | ci/generate-rule-chain-semantics-analysis.py | generate-rule-chain-semantics-analysis | generated | 0 | 1.044 | fresh | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | complete | - | - | 2026-06-17T02:40:19Z |
| canonical | connector | critical | final_consistency_audit | ci/generate-final-consistency-audit.py | generate-final-consistency-audit | generated | 0 | 1.768 | fresh | `reports/testing/generated/canonical/final-consistency-audit.generated.json`<br>`reports/testing/generated/canonical/final-consistency-audit.generated.md` | complete | - | - | 2026-06-17T02:40:20Z |
| mixed | connector | informational | runtime_cache_reports | ci/update-runtime-reports.py | prepare-runtime-components | generated | 0 | 0.201 | fresh | `reports/testing/generated/cache/runtime-component-cache.generated.json`<br>`reports/testing/generated/cache/runtime-component-cache.generated.md`<br>`reports/testing/generated/cache/runtime-build-cache.generated.json`<br>`reports/testing/generated/cache/runtime-build-cache.generated.md` | complete | - | - | 2026-06-17T02:09:29Z |
| manifest | manifest | important | report_dependency_graph | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-dependency-graph.generated.json`<br>`reports/testing/generated/manifest/report-dependency-graph.generated.md` | complete | - | - | 2026-06-17T02:40:22Z |
| manifest | manifest | important | report_data_lineage | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-data-lineage.generated.json`<br>`reports/testing/generated/manifest/report-data-lineage.generated.md` | complete | - | - | 2026-06-17T02:40:22Z |
| manifest | manifest | important | report_path_migration | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-path-migration.generated.json`<br>`reports/testing/generated/manifest/report-path-migration.generated.md` | unknown | - | - | 2026-06-17T02:40:22Z |
| manifest | manifest | informational | generator_runtime_summary | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | unknown | - | - | 2026-06-17T02:40:22Z |
| manifest | manifest | important | report_freshness | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-freshness.generated.json`<br>`reports/testing/generated/manifest/report-freshness.generated.md` | complete | - | - | 2026-06-17T02:40:22Z |
| manifest | manifest | critical | merge_readiness_dashboard | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json`<br>`reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | complete | - | - | 2026-06-17T02:40:22Z |
| manifest | manifest | critical | report_refresh_manifest | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-refresh-manifest.generated.json`<br>`reports/testing/generated/manifest/report-refresh-manifest.generated.md` | unknown | - | - | 2026-06-17T02:40:22Z |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `c9931aa8c2c7205af54c69f8737ea29747c076263a46c8dccf298db9c7d678a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `0f23927f874797d2c824a516929130f2bc23e2f2b28271ca9e888e12fe642970` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `8ad1be1924b8f4c65c131676713b11627aa0f688fd09c0f18701663c7fce8520` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `5a167326a74804cf90537e97cc6e4852ee26846caae37c307aebad550767b561` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `334d224d051eca6bff11ceffd4923332e102e0102ba810d98352e845fdbb60ba` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `14277a0ce581febfb65184cee8cd7111f5c33baddb18a4c457fe1f2e8f350d6c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `caec0a0b5a4f3af821c29ad4cfb2df2f6b83597367590ec9f2033c1a68ea2761` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `8e4db3774f091e7031c19862d57a29ef6291cb2e82469d9626d637869726c1e4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `ee720172a5cbb1c287948963a8f904b7b0079f04ee14811b6574826f6314f6f5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `824ff56ca8d7b80728c8c26467e68e48a65d53cbc432b98e37089851b52bd907` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `676cc8d9b51b9294387e0b73fe8a7ff1f78a4fe5ff268f5996cb1967b906c576` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `09f8685086520789d33c87c98085bd890f4bdf44c5c6977087e442ebc4b86f0b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `c8b4c767c507a9f9d8151f814727e31f344588358aaef07c2def27d43e9057ce` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `ba537476925bacb31e4a64a005723c367eca24fa69604602ed233c6040f01484` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `b6ce3c02e4ed81d078fb8cd9971b03719d558ca1ab79aca20f5d6aada335deee` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `0e0aaf3541012a450270e9742e0536ec6d8167bcd3d8affba1822fc312fa9dee` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `453b7f87822f22de2d4d827ec062fb141f28e7eef0c7ee8935fa8522f3b7b89f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `9d85214d89b16f0fa9c85a2ae5484f535422b141eab65873dc74c132ff7161a2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `7d7a581758867799859f481971e56c0e7da57ca399f5a7e016b2ce839ac83063` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `35bc5588d5432bb09eafc71aebcce4744e3b395b8d5868c917b76aa7c0e1e449` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `b21bba0ae1115efd9761ed2317324b8e142f221801b35359b024704fb2e4c657` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `d8d1e68951551c9e7a3b961f9709176cdcfa5ffbcf750548cf7cd6f0d3593857` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `2243b0038a6ea09a2212f06bdfdd2114d0c4d2eba39fa8221d9035133ddc910b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `1f3bd6d8cd3298763e5a8dce94bedb2f2c06fe2024011965198889bb489c29c9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `9aa3ecd89fbfce7a5c4eba7fdee9b0ba04eda8ec365a1b347aa7c1bba546c900` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `2752447901efdb4e4c1e50c2da4b3097a11e9a482c8bdf81a75fb6b6065a5e3c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `03ea2803bcd564284e704492dee86dcb19afa74b281581aae987bb099ace7a8f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `7ae350e02e06b98311b5b71239baf013d662d43c8b026ac277bfc8db7a6d7485` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `3b861a5183e0369b87af5ade6366668b088b07a5f36ac14dd73a991b2d2d93c6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `a4025e365e22c660656ab067a723ebd01488f95a363b697bba51e3d8d269392e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `c47d344d78abd4861c0ce03b3ecf4f2a9e114e10efbdb6e5329673bd190b3ccd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `d213b112cdcbcdb7a2509c1b80871d5b1e29f8db6e02cb2dcdfb09191598d018` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `b21bba0ae1115efd9761ed2317324b8e142f221801b35359b024704fb2e4c657` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `d8d1e68951551c9e7a3b961f9709176cdcfa5ffbcf750548cf7cd6f0d3593857` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `a15344a1c08d56859ace139142727648a985f759d9c5e5f439361843e62371ca` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `21432689e3588ee295e9fe5b5d674bdf4e2f580056064eeb183432d002725548` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `b21bba0ae1115efd9761ed2317324b8e142f221801b35359b024704fb2e4c657` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `d8d1e68951551c9e7a3b961f9709176cdcfa5ffbcf750548cf7cd6f0d3593857` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `0a712de6297bbe398f7a20ba2fdcbb01edd616a1478df412f56276feced9a0d8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `3ed279746eaadcb5ebea61ada0649dfc74a44630b2a174ca3ae750962fefbecc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `b21bba0ae1115efd9761ed2317324b8e142f221801b35359b024704fb2e4c657` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `d8d1e68951551c9e7a3b961f9709176cdcfa5ffbcf750548cf7cd6f0d3593857` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `893fb7f44572f7c5b06974f727c4bd5b56ac2b68eeaf50bd2eb287292a85c567` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `6912772a751ec416d98fac75243486cd044b522d0d27ac60f2defa965c159e19` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `56d43bad850595932f10e7e412d8d7a2a63b60ec8a170535015b7eb12ad7f15d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `08ab707cbb8708d08f9d603a634ded82ff0cb4d6cb933811883c32bd63b0600a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `6f7c469a2eb7869d6b401cf502cf6195bd3c0efecea4f83192c051a11797dd6a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `0d0501c618a412f0d64557df9e567536e7d20e5a51a10a0437afd2179b1dd016` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `c1bafe3651af877ed965d9b22cdeb6175f4df1d478e28b603ebf0bdc2b68f6e9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `6d43170bcfe9c0fdf777388fad89933cfd3e38f78f91b2728ca9d6326f616f32` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `0134c972c63d349496e01fea4e0c56d8ed8a9177de05b0b6b76474435304f567` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `3621d79891852de9b1ae645c1445ed04c337e85fcfef1af1f38ff45e3dea1bb2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `cda756a42874f999e3bfe3944e8c3862c9b6ecbd19e57886986a25b4074cad5c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `4e17008b2a57a16cb249f0221539bc5d4258aa4159f2747152f05c14451da366` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `217d6fc0d4e3acf725e772745aafa930045013eed839d6009a188b60c39d1ddd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `8da7b21374eb6e5ecb8e6600d95fd22afabc90f59e82ea07a8b192ff97e9f403` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `a59343bebc59e34142df37e8f867b013b9185b07889ff9407d7fbed05fa12f53` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `851a9a2a322c4c932e89158ddec29e3e07f3ee31fae5d9b676b698bce0bb8750` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `8ea0bad90117ba5fcbede1ee8cce97fffff7701297ceb490670faa4ea3c48126` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `963c8a08ffb7483cf1c8bcc72b279827233cbd8d31af85ac36db4f1502fd8742` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `209214455838f98bb34f32ad8fc4c253c89fbf671db412542638a809cb748d87` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `3aaaaaecfb61ff0ae0a47de190d98543466b2657881fa0dd9670454ccce3f284` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.json` | `ab832abc78cdfd4c109b164c17aa56fee1385142c6267221b2c00b40b0b3417f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.md` | `e9c907712ab41aa9bc20f30d857c8a121c7210510b4033a9fcdc64fd1c835aa8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.json` | `dd09b8d68e16ae262d821ee082eb9f445e1604968df9e1759871b75d79f39eb3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.md` | `e2effa7d889ff3e7f0b3f96262879181b7ea245167fa2db6dfa8ca996fdd3428` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.json` | `65b5b1e34d186f51fb85f9eebc539b6d49f3f91fef7c6b70e162f1ca67eae0c4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.md` | `71b37d23536976c84b1f74529a6c635c2f30d5a254ca73c95f11550304e79f87` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | `a6395cb43eeb76c754208e894730ce301bfbc38d2036cc40e9d4f0c1237aac18` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `a641435cfc5eeaa17ca31ae9d560e1c933286f87c8e6f240d3ae3094afb184aa` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.md` | `4b1d6f936f336cda6dc23f2202a611b39fdf686d44c719566208b75fd221263c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `d17547072062dacc80060455fbb24a58e73d0f69588b855167ad9b6b732ea830` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | `79238e83be9cd41505357c14d747f17d15bf7ef4added05d29092ec4c93468cb` | `2026-06-16T19-12-00Z-614c8049` | present |

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
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | present | input file available |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-dependency-graph.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-data-lineage.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-path-migration.generated.md` | present | input file available |
| `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-freshness.generated.md` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | present | input file available |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | present | input file available |
