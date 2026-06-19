> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T16:40:14Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `58b2135bb8adf12a4cad8afb448d1156e801cc00`
> Framework SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `complete`

# Report Refresh Manifest

> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`

## Summary
- Connector SHA: `58b2135bb8adf12a4cad8afb448d1156e801cc00`
- Framework SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
- Framework submodule SHA: `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4`
- MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`

## Inputs
- `full_runtime_matrix`: `a81b9fe95a788ab2a4e1d5ae42f9dab8c90911933cb4c91e189d84dec5581120`
- `native_mrts`: `a57d1fdf9b17afe446a1cb31f8cf5ce5d58b7b8e9a5af75fec3118d978c68fd7`
- `build_cache`: `0cd0a39720c8f5e4f5332443279f545a36424173e92e56f3ed476e52e6972e92`
- `component_cache`: `65f7595978901165d27f350d930d25dcd9589246241599a845be514a2d6ea70a`

## Verified Commands

| Command | Status | Return Code | Duration | Log Hash | Notes |
|---|---|---:|---:|---|---|
| `-` | not_run | - | - | `unknown` | No verified command file was supplied. |

## Submodules
| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `58b2135bb8adf12a4cad8afb448d1156e801cc00` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `6cb57e476a40f8644d4cb84b8a0f9a7016a71ff4` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Reports
| Category | Owner | Severity | Report | Generator | Target | Status | Return code | Duration | Freshness | Outputs | Input status | Missing inputs | Missing outputs | Generated at |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|
| mixed | connector | informational | connector_coverage_reports | framework:ci/generate-case-matrix.py | generate-test-matrix | generated | 0 | 2.21 | fresh | `reports/testing/test-coverage-overview.md`<br>`reports/testing/generated/runtime/apache-runtime-results.generated.md`<br>`reports/testing/generated/coverage/case-matrix.generated.md`<br>`reports/testing/generated/coverage/connector-gap-summary.generated.md`<br>`reports/testing/generated/coverage/coverage-summary.generated.md`<br>`reports/testing/generated/runtime/haproxy-runtime-results.generated.md`<br>`reports/testing/generated/runtime/nginx-runtime-results.generated.md`<br>`reports/testing/generated/coverage/phase-coverage.generated.md`<br>`reports/testing/generated/runtime/runtime-matrix.generated.md`<br>`reports/testing/generated/coverage/xfail-summary.generated.md` | complete | - | - | - |
| canonical | connector | critical | full_runtime_matrix | ci/generate-full-runtime-matrix.py | generate-full-runtime-matrix | generated | 0 | 0.413 | fresh | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.md` | complete | - | - | 2026-06-19T16:38:58Z |
| manifest | connector | critical | full_matrix_job_completeness | ci/generate-full-matrix-job-completeness.py | generate-full-matrix-job-completeness | generated | 0 | 0.953 | fresh | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json`<br>`reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | complete | - | - | 2026-06-19T16:38:59Z |
| manifest | connector | critical | verified_runtime_mismatch_analysis | ci/generate-verified-runtime-mismatch-analysis.py | generate-verified-runtime-mismatch-analysis | generated | 0 | 6.535 | fresh | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json`<br>`reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | complete | - | - | 2026-06-19T16:39:06Z |
| manifest | connector | critical | nginx_mrts_http500_cluster_analysis | ci/generate-nginx-mrts-http500-cluster-analysis.py | generate-nginx-mrts-http500-cluster-analysis | generated | 0 | 0.529 | fresh | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json`<br>`reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | complete | - | - | 2026-06-19T16:39:06Z |
| work-queues | connector | important | connector_work_queue | framework:ci/generate-connector-work-queue.py | generate-work-queue | generated | 0 | 4.652 | fresh | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.md` | complete | - | - | 2026-06-19T16:39:11Z |
| work-queues | connector | important | phase_work_queue | framework:ci/generate-phase-work-queue.py | generate-phase-work-queue | generated | 0 | 1.176 | fresh | `reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-19T16:39:12Z |
| mixed | connector | informational | native_mrts_reports | framework:ci/generate-mrts-native-report.py | mrts-native-full-run | generated | 0 | 0.522 | fresh | `reports/testing/generated/mrts-native/mrts-native-full.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-full.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | complete | - | - | 2026-06-19T16:39:12Z |
| manifest | connector | important | native_semantics_comparison | ci/run-native-case-comparison.py | generate-native-semantics-comparison | generated | 0 | 0.581 | fresh | `reports/testing/generated/manifest/native-semantics-comparison.generated.json`<br>`reports/testing/generated/manifest/native-semantics-comparison.generated.md` | complete | - | - | 2026-06-19T16:39:13Z |
| focused-analysis | connector | informational | nolog_audit_evidence | ci/generate-nolog-audit-evidence-analysis.py | generate-nolog-audit-evidence-analysis | generated | 0 | 1.973 | fresh | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json`<br>`reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-19T16:39:15Z |
| focused-analysis | connector | informational | response_header_hook_analysis | ci/generate-response-header-hook-analysis.py | generate-response-header-hook-analysis | generated | 0 | 4.233 | fresh | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-19T16:39:19Z |
| focused-analysis | connector | informational | phase4_hard_abort_capability | ci/generate-phase4-hard-abort-capability.py | generate-phase4-hard-abort-capability | generated | 0 | 6.403 | fresh | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json`<br>`reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-19T16:39:25Z |
| canonical | connector | important | remaining_failure_analysis | ci/generate-remaining-failure-analysis.py | generate-remaining-failure-analysis | generated | 0 | 18.17 | fresh | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.md`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.md`<br>`reports/testing/generated/canonical/full-run-evidence.generated.json`<br>`reports/testing/generated/canonical/full-run-evidence.generated.md` | complete | - | - | 2026-06-19T16:39:29Z |
| focused-analysis | connector | informational | intervention_blocking_analysis | ci/generate-intervention-blocking-analysis.py | generate-intervention-blocking-analysis | generated | 0 | 11.77 | fresh | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | complete | - | - | 2026-06-19T16:39:55Z |
| focused-analysis | connector | informational | no_mrts_intervention_nomatch_analysis | ci/generate-no-mrts-intervention-nomatch-analysis.py | generate-no-mrts-intervention-nomatch-analysis | generated | 0 | 1.127 | fresh | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | complete | - | - | 2026-06-19T16:39:57Z |
| focused-analysis | connector | informational | body_processor_analysis | ci/generate-body-processor-analysis.py | generate-body-processor-analysis | generated | 0 | 11.782 | fresh | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | complete | - | - | 2026-06-19T16:40:08Z |
| focused-analysis | connector | informational | rule_chain_semantics_analysis | ci/generate-rule-chain-semantics-analysis.py | generate-rule-chain-semantics-analysis | generated | 0 | 1.132 | fresh | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | complete | - | - | 2026-06-19T16:40:09Z |
| canonical | connector | critical | final_consistency_audit | ci/generate-final-consistency-audit.py | generate-final-consistency-audit | generated | 0 | 1.804 | fresh | `reports/testing/generated/canonical/final-consistency-audit.generated.json`<br>`reports/testing/generated/canonical/final-consistency-audit.generated.md` | complete | - | - | 2026-06-19T16:40:11Z |
| mixed | cache | informational | runtime_cache_reports | ci/update-runtime-reports.py | prepare-runtime-components | generated | 0 | 1.583 | fresh | `reports/testing/generated/cache/runtime-component-cache.generated.json`<br>`reports/testing/generated/cache/runtime-component-cache.generated.md`<br>`reports/testing/generated/cache/runtime-build-cache.generated.json`<br>`reports/testing/generated/cache/runtime-build-cache.generated.md`<br>`reports/testing/generated/cache/runtime-cache-index.generated.json`<br>`reports/testing/generated/cache/runtime-cache-index.generated.md` | complete | - | - | 2026-06-19T16:22:55Z |
| manifest | manifest | important | report_dependency_graph | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-dependency-graph.generated.json`<br>`reports/testing/generated/manifest/report-dependency-graph.generated.md` | complete | - | - | 2026-06-19T16:40:14Z |
| manifest | manifest | important | report_data_lineage | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-data-lineage.generated.json`<br>`reports/testing/generated/manifest/report-data-lineage.generated.md` | complete | - | - | 2026-06-19T16:40:14Z |
| manifest | manifest | important | report_path_migration | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-path-migration.generated.json`<br>`reports/testing/generated/manifest/report-path-migration.generated.md` | unknown | - | - | 2026-06-19T16:40:14Z |
| manifest | manifest | informational | generator_runtime_summary | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | unknown | - | - | 2026-06-19T16:40:14Z |
| manifest | manifest | important | report_freshness | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-freshness.generated.json`<br>`reports/testing/generated/manifest/report-freshness.generated.md` | complete | - | - | 2026-06-19T16:40:14Z |
| manifest | manifest | critical | merge_readiness_dashboard | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json`<br>`reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | complete | - | - | 2026-06-19T16:40:14Z |
| manifest | manifest | critical | report_refresh_manifest | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-refresh-manifest.generated.json`<br>`reports/testing/generated/manifest/report-refresh-manifest.generated.md` | self_generated_no_direct_input | - | - | 2026-06-19T16:40:14Z |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `69070f2de357eb2ba8e183aab3538eba889f94adb7bc85aee84b34854cf4fadb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `715e0d979ba376f7338703b0563ae464a9a0b34c099ef4ad63b259960ae00b35` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `ccd5865d69eef8d5e493cc2713df76b696088f050372968acd63a95985956464` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `b3a4a32863f801eafd062a29b1c9de18312780e99f61eb51afb512d4d7d32b21` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `f75e68fb57c3248a250b79d27cc41c36ef8c6637111b230123f284a4d4367e9f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `169718c69d08433353f310157810e679e70a13dbe4d1e7c1388da65925928e4b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `3962623db8eaf7ea3d6183d53c522313c8ce4aee024bc1b8ec89973f64158ac8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `33d505be8e410e1f508c7633e2e716ae5e5100ade9d7a2ae99b85ff60a16d496` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `38d4b269d9f91e6521a5b38a275a9f1e9074ed4a5a3d477c8a09fa01d3968513` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `8d771d19da310aea4fe2a3a9a782d32f99005fc16c3656e3467deb7e0f58c8c7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `8e2d2ac2aff46856cd32e419ff73f333ce37a5321b15fad5f8b93bff85c1f16e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `38a584a4c75ab9dbf258f504fe1957c88cb298c73f77797d5f482029d0e6f7bb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `401ad4822628cf5abd03471a376848f5bb77f4fab934c603cbcda42c89f60050` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `1ae7bac76c1e3f07a6e982b2fa90390b69ee8b90f423b43281db191d81fb9593` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `682daa5f4a31c9630b61a6bb5cc29090283acfdbfe6c37a3da83ce0008e437e1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `a43fe621396d7e32d57300b2a5eee9f53bd6dcd4e5ea8d08af60048428d36707` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `5b156bcea29fc9536e3e887f448c62f024da49cce37433cab71df91df40a5168` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `1be28b91da38f2e701be376ba17d7afb58ea1772173148177971d80cf366ee3b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `e9871fd60f06407d734b70f836656ba81f931d31fb6bfeee010f365ac87fa926` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `1d30ff7700b60d97ab4b1f986727ef11e3ece343b1f33eaf55cbcc057cdf7a1a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `6230717b3d574fafec127dec16059901f1137ca001ff092886a4d2170cf6387b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `5758625509bfce6b46a1805212fcc2143f816ca848881e0bb31fbf87f05c0e71` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `a3bac6e2ceb7f389365aa0df64724024903457befad95fdca81695ea84b611e5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `907bda6eec9ec3821529192ef26989b8e7ddc3de16fc33313e244433ddfdfa9b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `6c266638bedb64d6eef5e4019166250a91bbe6fdd891c6305983989d78a3ffbd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `19cb8eef01b31d6f5da49b7b55fbe49bcda341995ac0d5ec7b4eb9831f2b9076` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `3a383219cecd9ef88202f413c5b3c01a814f1f5b5995d652f2beafaacb02287a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `7c203a4bc6fe9206549b414ad387e39dbceaa7851e96190cc11728550c2c5635` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `ece2b1e07ae4dcc4d0f90ac21ff86f0bd2817c5906835365b313d0570f3e064e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `165749973d2359f4297ccd69a8918aca47a7828fe6c6a89f3cc60a27ccff5c09` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/native-semantics-comparison.generated.json` | `fa4da197c607a541b3e578b07b1e5683f24708e2498ddbd29c9313231756b6f3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/native-semantics-comparison.generated.md` | `0c818458f725913ea7e4059f5d1f615c31556420b80c2cde1b96c158ccc9076f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `0b233448cf42ef0a79103b42718f1d8b64a4e83ed2009375c6e101fa7a6f3999` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `3225211b3fc0060a5c3ed567ae9aa98a2abf4cb9a6e3b87878146db1e28aa0b5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `6230717b3d574fafec127dec16059901f1137ca001ff092886a4d2170cf6387b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `5758625509bfce6b46a1805212fcc2143f816ca848881e0bb31fbf87f05c0e71` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `018472ace1d129017f55e7386d7d9c0ca6bab97d21ebfba439179777b1bf4c79` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `42208d0409f0903399f4b8fbdb9280dc055dc1af54955d31d6381e77c9d1a0dc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `6230717b3d574fafec127dec16059901f1137ca001ff092886a4d2170cf6387b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `5758625509bfce6b46a1805212fcc2143f816ca848881e0bb31fbf87f05c0e71` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `99a1313443b6902af4e0e673eba79071d1e34c662e92dbd700154839450efdba` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `5a7cd54751090ee3c4af48e0c7a8d9d29f7af6f27640c1849b416dd4558b0f4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `6230717b3d574fafec127dec16059901f1137ca001ff092886a4d2170cf6387b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `5758625509bfce6b46a1805212fcc2143f816ca848881e0bb31fbf87f05c0e71` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `8d20679b744b065ef1b19c70135e47a1ae078af23bd4d394349d78a624a640a4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `57ca8dbfd65d140cd185f0d771505bde73e5f2a39f94004eb938b3587709fd13` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `cde00865dd00752f1a857c92f0f9db74adaa032921c7619bec174a9371034d23` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `7ceacc290598e6880b7c516d7fb31e74fd50e434fc875e188dadf08235add1e4` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `2db466da1006f40605c3fbf9be46e8f370d486be124f3e288e573a1cff96a29f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `2fde07841164d9f7c2aed996b59603d9c5e041251e5a46e291868018d18effcc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `42b3aecb4efda7c19caac8f6613a800e81cb3b7f829cd67ac5d6464879f9f5f9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `3b298f1335a141bda45547f25d63cd83a678ba0caae42b7d29eb9df8b62bfb8c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `fef57f4802a7a606f527614bb6807ab434ac19cbb35349fd9f6899bed365b708` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `a8378865cedf5d170d2f58c42a03adca082f7e742f60c3f73c5a226c18f9ff3a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `c094ad744691ddc16d86f247720264df53ba1710fccd03b443555c0e2353977f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `988ff53b3d3ebb87bbf26c7989da61cc52a32852fbf24da8a59ab11b962cabfc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `b04c000ebc809e6bf482e54266f71339a02ffb04e289d4e91ca22cf8611ea319` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `3854c846b7d6710dcb3446a49ad38749d2f299c234dd12c921970248bec825d1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `d31ab608dc993cfc14d4e8f35efb90bf8b05b7525aece85acac725e5232bca68` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `c537ec9f53d36eca7531a712048365e00333153b9d7a08b45806a9fff66a2f79` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `33f60405c8ce38bac8689eb5cc6046089f99569c0b8980629fa7f193267faa0d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `62a83cac776768366bd294f66df9615770bcaa009f899eb015c524119d393ae6` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `8a9d0c44783aedde91f730a53c08c5a802a29998bbe244f4f82fb03fe193ee09` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `ea9e73e7a2f339116476bd7d7562e8191cde8f727bfc1eadb38f92d57b275791` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-cache-index.generated.json` | `ce348fd0e5df25e710d72d0191af92bd5a787be5bddf635f92d4b6a83f7c8faa` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-cache-index.generated.md` | `305a0ab2e626250e43ff34b1a2dbef744c97e15e0e43a775baab95a3149114bb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.json` | `62677cb7cc7486ca8bf81856449cf75b8fd955064fab78984f64ccc8010e437a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.md` | `e4738d74ff76172dc9a4f5d38ec19535bf99a820649d2e2ddf14f4d4a29e4b84` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.json` | `c5a62d7d345f7bfa53c88240401786aaba217c1704f72c0c910b5af16ee06ae2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.md` | `96b2521c6dd98dc959ab73be3df50770b0c8536dae76de5f32012212bc7530f1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.json` | `e3a504d256c92edcc8570b80b478ebca271cd1be1d23a82808258d5c4e52d425` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.md` | `6fedd119df54575fe6320dc2a376131afcca26aecab5ff3138b8ea2e3220a2fa` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | `25d0e082cbe663e0e32cace1fc067c66d1a58ebdccf43482160b50bb338e9c40` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `e422a08561f2a79a4298b4c89b237d4fefe174c373758ed8df5978f516326468` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.md` | `64bf09e2dd6e7d2f555984b0e63f1fd406f79b0124c6da93b2a2222618a95009` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `6a6d411311f909bc8dfa5b5f194ecffa5c41ac228894b68ca2d1b967469345f8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | `d89274a6073d43a221585a772310506e4d613110b2424abdf945b7230a89505f` | `2026-06-16T19-12-00Z-614c8049` | present |

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
