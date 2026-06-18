> Generated file - do not edit manually.
>
> Generated at: `2026-06-18T16:15:42Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
> Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `complete`

# Report Refresh Manifest

> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`

## Summary
- Connector SHA: `93172ef0f7d4e3fc4a10e97d63aefe982a593b55`
- Framework SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
- Framework submodule SHA: `131fdad6974cf0f67a874f7c1b1a118c4b25f303`
- MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`

## Inputs
- `full_runtime_matrix`: `27ecf1e6e1d0c348abc551fa3ab116f22febab50b4c51115d386b6b7309d193b`
- `native_mrts`: `ee4e5a808beedc7c488ede3185e2978662aae9f6b0ed69c18e06824c6ba82630`
- `build_cache`: `b34893f207ad2f0098b59f93ca1ce242862e70bb037bb2f906656366da8ca6e6`
- `component_cache`: `ecc858de9057f1e4d948d6d44aec95d46701e275c154cd9b42d4e796477f4b7e`

## Verified Commands

| Command | Status | Return Code | Duration | Log Hash | Notes |
|---|---|---:|---:|---|---|
| `-` | not_run | - | - | `unknown` | No verified command file was supplied. |

## Submodules
| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `93172ef0f7d4e3fc4a10e97d63aefe982a593b55` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `131fdad6974cf0f67a874f7c1b1a118c4b25f303` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Reports
| Category | Owner | Severity | Report | Generator | Target | Status | Return code | Duration | Freshness | Outputs | Input status | Missing inputs | Missing outputs | Generated at |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|
| mixed | connector | informational | connector_coverage_reports | framework:ci/generate-case-matrix.py | generate-test-matrix | generated | 0 | 2.053 | fresh | `reports/testing/test-coverage-overview.md`<br>`reports/testing/generated/runtime/apache-runtime-results.generated.md`<br>`reports/testing/generated/coverage/case-matrix.generated.md`<br>`reports/testing/generated/coverage/connector-gap-summary.generated.md`<br>`reports/testing/generated/coverage/coverage-summary.generated.md`<br>`reports/testing/generated/runtime/haproxy-runtime-results.generated.md`<br>`reports/testing/generated/runtime/nginx-runtime-results.generated.md`<br>`reports/testing/generated/coverage/phase-coverage.generated.md`<br>`reports/testing/generated/runtime/runtime-matrix.generated.md`<br>`reports/testing/generated/coverage/xfail-summary.generated.md` | complete | - | - | - |
| canonical | connector | critical | full_runtime_matrix | ci/generate-full-runtime-matrix.py | generate-full-runtime-matrix | generated | 0 | 0.402 | fresh | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.md` | complete | - | - | 2026-06-18T16:14:35Z |
| manifest | connector | critical | full_matrix_job_completeness | ci/generate-full-matrix-job-completeness.py | generate-full-matrix-job-completeness | generated | 0 | 1.021 | fresh | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json`<br>`reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | complete | - | - | 2026-06-18T16:14:36Z |
| manifest | connector | critical | verified_runtime_mismatch_analysis | ci/generate-verified-runtime-mismatch-analysis.py | generate-verified-runtime-mismatch-analysis | generated | 0 | 5.93 | fresh | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json`<br>`reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | complete | - | - | 2026-06-18T16:14:42Z |
| manifest | connector | critical | nginx_mrts_http500_cluster_analysis | ci/generate-nginx-mrts-http500-cluster-analysis.py | generate-nginx-mrts-http500-cluster-analysis | generated | 0 | 0.458 | fresh | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json`<br>`reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | complete | - | - | 2026-06-18T16:14:42Z |
| work-queues | connector | important | connector_work_queue | framework:ci/generate-connector-work-queue.py | generate-work-queue | generated | 0 | 4.186 | fresh | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.md` | complete | - | - | 2026-06-18T16:14:46Z |
| work-queues | connector | important | phase_work_queue | framework:ci/generate-phase-work-queue.py | generate-phase-work-queue | generated | 0 | 1.101 | fresh | `reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-18T16:14:47Z |
| mixed | connector | informational | native_mrts_reports | framework:ci/generate-mrts-native-report.py | mrts-native-full-run | generated | 0 | 0.459 | fresh | `reports/testing/generated/mrts-native/mrts-native-full.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-full.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | complete | - | - | 2026-06-18T16:14:48Z |
| focused-analysis | connector | informational | nolog_audit_evidence | ci/generate-nolog-audit-evidence-analysis.py | generate-nolog-audit-evidence-analysis | generated | 0 | 1.691 | fresh | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json`<br>`reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-18T16:14:49Z |
| focused-analysis | connector | informational | response_header_hook_analysis | ci/generate-response-header-hook-analysis.py | generate-response-header-hook-analysis | generated | 0 | 3.599 | fresh | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-18T16:14:53Z |
| focused-analysis | connector | informational | phase4_hard_abort_capability | ci/generate-phase4-hard-abort-capability.py | generate-phase4-hard-abort-capability | generated | 0 | 6.199 | fresh | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json`<br>`reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-18T16:14:59Z |
| canonical | connector | important | remaining_failure_analysis | ci/generate-remaining-failure-analysis.py | generate-remaining-failure-analysis | generated | 0 | 21.452 | fresh | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.md`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.md`<br>`reports/testing/generated/canonical/full-run-evidence.generated.json`<br>`reports/testing/generated/canonical/full-run-evidence.generated.md` | complete | - | - | 2026-06-18T16:15:03Z |
| focused-analysis | connector | informational | intervention_blocking_analysis | ci/generate-intervention-blocking-analysis.py | generate-intervention-blocking-analysis | generated | 0 | 6.861 | fresh | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | complete | - | - | 2026-06-18T16:15:27Z |
| focused-analysis | connector | informational | no_mrts_intervention_nomatch_analysis | ci/generate-no-mrts-intervention-nomatch-analysis.py | generate-no-mrts-intervention-nomatch-analysis | generated | 0 | 0.935 | fresh | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | complete | - | - | 2026-06-18T16:15:29Z |
| focused-analysis | connector | informational | body_processor_analysis | ci/generate-body-processor-analysis.py | generate-body-processor-analysis | generated | 0 | 9.768 | fresh | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | complete | - | - | 2026-06-18T16:15:38Z |
| focused-analysis | connector | informational | rule_chain_semantics_analysis | ci/generate-rule-chain-semantics-analysis.py | generate-rule-chain-semantics-analysis | generated | 0 | 1.134 | fresh | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | complete | - | - | 2026-06-18T16:15:39Z |
| canonical | connector | critical | final_consistency_audit | ci/generate-final-consistency-audit.py | generate-final-consistency-audit | generated | 0 | 1.748 | fresh | `reports/testing/generated/canonical/final-consistency-audit.generated.json`<br>`reports/testing/generated/canonical/final-consistency-audit.generated.md` | complete | - | - | 2026-06-18T16:15:41Z |
| mixed | connector | informational | runtime_cache_reports | ci/update-runtime-reports.py | prepare-runtime-components | generated | 0 | 0.22 | fresh | `reports/testing/generated/cache/runtime-component-cache.generated.json`<br>`reports/testing/generated/cache/runtime-component-cache.generated.md`<br>`reports/testing/generated/cache/runtime-build-cache.generated.json`<br>`reports/testing/generated/cache/runtime-build-cache.generated.md` | complete | - | - | 2026-06-18T12:14:56Z |
| manifest | manifest | important | report_dependency_graph | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-dependency-graph.generated.json`<br>`reports/testing/generated/manifest/report-dependency-graph.generated.md` | complete | - | - | 2026-06-18T16:15:42Z |
| manifest | manifest | important | report_data_lineage | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-data-lineage.generated.json`<br>`reports/testing/generated/manifest/report-data-lineage.generated.md` | complete | - | - | 2026-06-18T16:15:42Z |
| manifest | manifest | important | report_path_migration | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-path-migration.generated.json`<br>`reports/testing/generated/manifest/report-path-migration.generated.md` | unknown | - | - | 2026-06-18T16:15:42Z |
| manifest | manifest | informational | generator_runtime_summary | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | unknown | - | - | 2026-06-18T16:15:42Z |
| manifest | manifest | important | report_freshness | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-freshness.generated.json`<br>`reports/testing/generated/manifest/report-freshness.generated.md` | complete | - | - | 2026-06-18T16:15:42Z |
| manifest | manifest | critical | merge_readiness_dashboard | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json`<br>`reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | complete | - | - | 2026-06-18T16:15:42Z |
| manifest | manifest | critical | report_refresh_manifest | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-refresh-manifest.generated.json`<br>`reports/testing/generated/manifest/report-refresh-manifest.generated.md` | unknown | - | - | 2026-06-18T16:15:42Z |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `396c911ae53a8e0e31e8ef2f673414d5573b76131ab09c82a0d4f9a6fe946ee9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `62620524c3483e03c80905aab1c88817dc45f87681a24530b0d08a4bc80ce599` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `9f592189477a5b00bf87842e5d75416e27cfaf5977eb65cabdab75f5ed1f5cb8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `5bec6b45399faa7261a012e9e91119ce5eecf1838809bf492129e7e4ea89f0f8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `1a88a989996df0406696df7b406bab1c69d55577f791ad54676fafc91e5843d8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `bdd80f0d0aa50e9f9d7310f24d0a09513a469302ad5ee10a8e3b70b5b774dad5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `48b20dac717641534aaff2ba8750e83e0d11cc081caeb7119f438e417a570979` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `ec48bccf0bc05f6f9659cedf12e644480f3377e42f8120d2c55df42d4e910970` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `15160e3476f4757a7140c8f1e50d5b67711bb7fad506808f4795a29796bdc804` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `eb11179d047c8f55a30c0c67992d98c6c54a458ea72542ae3af82be9eed40eca` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `94ef7376661e451a7c3a25bd98cb9b769096cd64fe85684fa62e6cef951a017e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `7f689ac9707318870fd94e6261be5e94248c5e4627b56350d9a1084a9d994e9f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `b9194afc316f2d929797e37a5101384b565efdb1809b7409d92866de4dfdd7cc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `30a38e0e1592d2c7d6f12d3d1bffb9b5aa16dc49d654fd5281653ba6112b643a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `509bc6777259ded64851696daa44ebc1785e6850d74245f62002fca00b89d4c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `742446339a214896ec98d880eac00c3387821d8eb618dca34602bd17447a3aef` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `e8efa6fcbc3b164150d760f425c618e77000cd5bc781cbbe755402fc8c7d82f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `b82595f249564212447b65325993329c784a7d06fff7ef472cf51bf609f31619` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `cc04a8bfd49ce1f7daa7859b93446aae935aa69b452e69ba2db8eda757857660` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `6f7c1d2581dfe85095748428f8ca050b138472c9d175b20cfd16597efd8bc427` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0d45c998bc358dc1b4d8de0dd383883b378af08121d3f39aab79e69cea31e4dd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `7eda12ca908450de05872c493ab1ecaf729f8d67fa1100116cbcdfc2261e67f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `ece45a62e50ddd73c0faf430f5eaea8489decaaba71fdb6216f1f73dcf9398c6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `1747c4d2c618327554a4fb377bf541c38a53d06211124fa947b874efc758add6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `c0b560c29eda5ae9f322704efb9298c573317d098e5a37b9763dbe50dd4cc11b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `efa79ea924b27e35240883854e0a90ef899f25a97a9f39f0c3c4e30285d571f7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `2ab53e2dac8d5eb77543c742bbe33b9281731c53c1bf7c709b456c9d6d443f2f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `34c212339f3b0f4352d008a8fd7f216a49427294b6306c27cdbd5abd31f49cab` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `96f772004dfc98334f07d2855b96f8a3e49f578f6fe9090c600d2c983f0bb32d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `17b02d5f6f18a1c78c81335b7a5c63023c02c5bf79c0b89a9729e616cc83c522` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `28679764935257530c5d2958517464b76e35dc8279d9a3655e61efe53d15276a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `f20e8f754821210d4a3ecaec175d60c59d51f39e52d6f87f2124a1f085c8ad6d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0d45c998bc358dc1b4d8de0dd383883b378af08121d3f39aab79e69cea31e4dd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `7eda12ca908450de05872c493ab1ecaf729f8d67fa1100116cbcdfc2261e67f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `2f6988a32b9c8641754bfa5ecf5914a43dcf43235bca04ec103658dc3b3d33b5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `92b9cfb8d0b143b118b10b46157eb66d70b8f570e71be6dfba505b77e73044c9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0d45c998bc358dc1b4d8de0dd383883b378af08121d3f39aab79e69cea31e4dd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `7eda12ca908450de05872c493ab1ecaf729f8d67fa1100116cbcdfc2261e67f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `50e876b98f7149424c83fa3f937c9e312f8d326826687982372e9b0ba2daddf4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `287c4655a685fa7d398c51531e2ca0ae8d6481464b3188f75689bfdf754813d7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `0d45c998bc358dc1b4d8de0dd383883b378af08121d3f39aab79e69cea31e4dd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `7eda12ca908450de05872c493ab1ecaf729f8d67fa1100116cbcdfc2261e67f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `88479f6014f3ca276541b5219356b48ce820401b9146bb365b9839fe9589c1d2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `7fa1d2e36c0260dc37ec96fa2d13625adce4ea19201c2743dfc6f0a472304135` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `05bc958c83d0fba9f7991380580343ddbe984c2e25b5cd856adc79de70f55828` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `af5e46549c43e641de225791160a36a7f59ab756b4308d39c8d60bcddcff7e30` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `4aec42cd1ad41e7d8f3aeff9311774b32f29c12aca6fccc73468054dd890c6a2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `d8d4db47d41cd05f297c618c2a2bca6474a21def7abd5afec76b4cedca3da2c1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `cfb36ec0b68c9177b1e4072ec8e7fe9342f023e4e6727caac86c5224df2d6aa0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `7384202100e10fbb45538c340db59ea5062f261b2ecfac1b37a6490f9aea7cfb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `cb4f403ea5862fc9d0affd53e1cfc32d33a71ac766fc358043f7c2351665fe10` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `0db38310b77f1cd0dbcb841a8a19880f8c65b05899fb8bb86dab2dc9b7e806d8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `dfb78eaa4704dac70b5bbea1951afaded99e66cb2fe976b1324ed4c688b5ca78` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `4c6347dfb57a65734ebff36d89f277313642d94dbbcf3f7dfb55e5537a3aa2b8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `f7c7b87461667d254c5479dc400e4d527e61c39c03c8e50635a0429f087104d7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `b16a3534c899a5900cec67b0664056d94b907a6e5ce47f8f9c2254ecdac46008` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `1f770179e24029f85d2b7b994d225a2f66512e10e22ce854ad80379ecb7381dc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `e00669a4b89f719fc463d75cde85092716723986efb4c51846bdd0d768d5b08d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `79ed3371ef67a807114668c9874b249d937306e31f37b088a0e27e01e46e8939` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `e951bd74f8e5c5e204428f3c009b236f53a3f88e42feb86a474b80ed2f122146` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `37b1b825d74e3e000d417242efcdb36f67ace9c6f08dfcca5caa8392ab4eaf81` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `191424fc89d90d917058b0bf8887acaa98d6185a9050e4bbfa89af2f7c365456` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.json` | `7c9bc6b079b5469b9c9c2bf7eb546bea8d4ed8a2872646773002f01b8b442723` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.md` | `ef6b551d663b4df8f1dd9c34787b7ffc4ec10976d018b690ef62cd59d92ab77a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.json` | `6f49554f9490a25081cbc164df811af4ecab29b61744de068ea3e9e6c33b378f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.md` | `231ee4159689217ea4d741e93cd4f40e025b30f79f8f56a2a1415bc35d669c4a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.json` | `2d8f567e745c7bcfca34798448fe01d537ee7d2f58a0f31e7e54212f9971c7b9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.md` | `b7d3b8831e728d6dcb1e82a2787f6d1f41abd95659048dd1f3a5dba29ef5cb8f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | `4c3d01d238f8591ad23f1440b01556748dd1b3421c7d16d8cacd8d7629dd531a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `d95b56797386aba3174e29391dae144e15462dcd9397c4b066a49c4fa170f000` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.md` | `e1b9e087468762d4f55d5a6108f4bd8dd696c1eec79ba262295ea2389c8a754a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `3e783fdfa68caf8ca8bd1de7dc8cd107e2ac9b27e6d939f661137e574b081113` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | `cfe953d718baf7f8fa086241a4fa45ed82b439454c6efc7687109483c9432698` | `2026-06-16T19-12-00Z-614c8049` | present |

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
