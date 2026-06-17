> Generated file - do not edit manually.
>
> Generated at: `2026-06-17T15:48:04Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `critical`
> Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
> Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
> MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`
> Input status: `blocked`

# Report Refresh Manifest

> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`

## Summary
- Connector SHA: `dd6e0455c4838949ce86cff81ce89dccd4e524f8`
- Framework SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
- Framework submodule SHA: `ee23a10d5224401d9e63f28ad374969ac129e5f0`
- MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`

## Inputs
- `full_runtime_matrix`: `42c491a928f6bab6fa3a912ae5fb1f62367c39779449a2e081dc4cbcb959b548`
- `native_mrts`: `7158b953eca776e4b919445d002b2201dc4408d922b6c024c24d0efebf35063b`
- `build_cache`: `3bd9928e7e07e4d5d063ce7406430d19b3bce5a5192ab29bd30665b062b40fe5`
- `component_cache`: `098d556686fecb58087fa9029b4f088516961c3f26dc8f2fd3202a3b1cdb96d4`

## Verified Commands

| Command | Status | Return Code | Duration | Log Hash | Notes |
|---|---|---:|---:|---|---|
| `git submodule update --init --recursive` | PASS | 0 | 0.116 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | executed in verified-report-run |
| `make prepare-runtime-components` | PASS | 0 | 47.168 | `ebe81b14f91deb1172365d8b58dcfc35b851bb0639f9d0146d2e4304d2778a55` | executed in verified-report-run |
| `make check-runtime-producer-readiness` | PASS | 0 | 0.266 | `a3168b1cbb84f6fca2f17b72c0780d1eb8fbd1fdf1c27f9888b3818d10b1f7ed` | executed in verified-report-run |
| `make runtime-matrix-all-runtime` | FAIL | 2 | 34.838 | `7e0668cd479d554d4930d1a73a718d674a4a85dbd7c0882719615853173714b6` | executed in verified-report-run |
| `make full-matrix-parallel-runtime` | BLOCKED_TIMEOUT | -15 | 7200.004 | `5500f1991ef745435b8d012076d0fa4151a3010065888e965e2885355c94daf9` | executed in verified-report-run |
| `make mrts-native-full-run-runtime` | FAILED_OPTIONAL | 2 | 50.088 | `8038538e5e0c3d3b843a4a129dd9836414c633e69acf38b80b952e69004817de` | executed in verified-report-run |
| `make generate-verified-runtime-mismatch-analysis` | PASS | 0 | 1.721 | `adefb6d110ce27068107f5ef954b7b166f0fb5111912b2c443bde54416b74f13` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 3600.006 | `bde32c49cd46fc98bac5075f0eb1983a319e329f1defd34a22fee83e5a408461` | wrapper timed out after completed job artifacts were written |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 1.119 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make check-generated-report-layout` | FAIL | 2 | 1.42 | `76be59f347ff4b075fa9823c84b585776f1581cac197cd3801152ffa710c68ef` | executed in verified-report-run |
| `make lint` | PASS | 0 | 5.737 | `f9e9529216293c430c3c5d4fa4efee6cdfd4bdb5ab9c799ef363f6e5a1999088` | executed in verified-report-run |
| `make quick-check` | PASS | 0 | 6.99 | `0d05c2440f21a9b4f43cfc4524d8870fe0ecc68f9a4ded323f430c96e95ea04a` | executed in verified-report-run |
| `make check-generated-report-layout` | FAIL | 2 | 1.421 | `76be59f347ff4b075fa9823c84b585776f1581cac197cd3801152ffa710c68ef` | executed in verified-report-run |
| `make lint` | PASS | 0 | 5.535 | `f9e9529216293c430c3c5d4fa4efee6cdfd4bdb5ab9c799ef363f6e5a1999088` | executed in verified-report-run |
| `make quick-check` | PASS | 0 | 6.99 | `0d05c2440f21a9b4f43cfc4524d8870fe0ecc68f9a4ded323f430c96e95ea04a` | executed in verified-report-run |
| `make check-generated-report-layout` | FAIL | 2 | 1.319 | `76be59f347ff4b075fa9823c84b585776f1581cac197cd3801152ffa710c68ef` | executed in verified-report-run |
| `make lint` | PASS | 0 | 5.835 | `f9e9529216293c430c3c5d4fa4efee6cdfd4bdb5ab9c799ef363f6e5a1999088` | executed in verified-report-run |
| `make quick-check` | PASS | 0 | 7.089 | `0d05c2440f21a9b4f43cfc4524d8870fe0ecc68f9a4ded323f430c96e95ea04a` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 662.744 | `6e7e638eb701c3da3c3e685c0d8fdc7b9c220372fef9737ddf4cbb417f097e84` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.417 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 1593.675 | `541eb1b41744f8b74b2c6d8c2e57be65279c6058fec570edf842722b9be08aad` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.518 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 687.44 | `75eeb487ad01c574d330af42e12840261db67c101efd4693e2beed478d683ce2` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.517 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=apache CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 1707.546 | `77c4dc3d0da460be567d48ff03b885e5d3ffcb667c8c5f674ccb3213906a2c62` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.618 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 877.15 | `283ea8e4086df99b61a1b41cff364f850cccecdacaa5c4e18eb7f59662619b2a` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.668 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 3523.191 | `78fcb51698576f5bebfd4353a24ffa9d450df93efdca49d7b6acb223df08d05c` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.718 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 934.575 | `d947bc87778ad19138c3570625cdb16a0c240cafb92559d19b25a6b42aa5d4ff` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.768 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=nginx CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 3660.01 | `d54cb5729ada9c4c92b430c7929a0a34a390e002a117d6f84a1bd8201483f9e4` | wrapper timed out after completed job artifacts were written |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.819 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=no-mrts` | FAIL | 2 | 617.9 | `2bff30e3ee54be02c7ba2b1b1cbdbbadcc8c59b4a673ca691f2f4ccef82a33f9` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 0.918 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=no-crs MRTS=with-mrts` | FAIL | 2 | 1412.258 | `8cf7ccdb3863b6dcb08a4f62a3d0eea92bfb46ced76ef343157c2067d02e304c` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 1.019 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=no-mrts` | FAIL | 2 | 650.082 | `11c39d8b433611b8afca3bc828ad3ee0ade1b82ec1c73e0b6c6247f686dd7768` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 1.069 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make full-matrix-single-job-runtime CONNECTOR=haproxy CRS=with-crs MRTS=with-mrts` | FAIL | 2 | 1510.347 | `44b24ec6a1b3879052ae8fc85369c9d480d43639a9716a922e1f8a67fb749349` | job artifacts completed; job.json is source of truth |
| `make generate-full-matrix-job-completeness` | PASS | 0 | 1.12 | `3f6e2647d67f1c6e4c2e6b949a214c33d5e4e8fce62232b7a107be924d5017d6` | executed in verified-report-run |
| `make refresh-all-reports` | FAIL | 2 | 33.131 | `8c29bc597a4e66b80d13d71f65ec2ccea9d77e97858991268357e950f8c9dfde` | executed in verified-report-run |
| `make generate-system-environment-proof` | FAIL | 2 | 55.57 | `816bccc1aee938f3dc336138bbfecb44d564164c4b176bc04c70ef18b0c01d7a` | executed in verified-report-run |

## Submodules
| Name | Path | SHA | Branch | Dirty | Status |
|---|---|---|---|---|---|
| parent | `.` | `dd6e0455c4838949ce86cff81ce89dccd4e524f8` | `master` | dirty | present |
| framework_submodule | `modules/ModSecurity-test-Framework` | `ee23a10d5224401d9e63f28ad374969ac129e5f0` | `master` | dirty | present |
| mrts_submodule | `modules/ModSecurity-test-Framework/tools/MRTS` | `13aa91291adea12d5c607fdd165d010fcfb1da78` | `HEAD` | clean | present |
| framework_sibling_checkout | `/root/git/ModSecurity-test-Framework` | `not_found` | `not_found` | not_found | not_found |

## Reports
| Category | Owner | Severity | Report | Generator | Target | Status | Return code | Duration | Freshness | Outputs | Input status | Missing inputs | Missing outputs | Generated at |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|
| mixed | connector | informational | connector_coverage_reports | framework:ci/generate-case-matrix.py | generate-test-matrix | generated | 0 | 1.905 | fresh | `reports/testing/test-coverage-overview.md`<br>`reports/testing/generated/runtime/apache-runtime-results.generated.md`<br>`reports/testing/generated/coverage/case-matrix.generated.md`<br>`reports/testing/generated/coverage/connector-gap-summary.generated.md`<br>`reports/testing/generated/coverage/coverage-summary.generated.md`<br>`reports/testing/generated/runtime/haproxy-runtime-results.generated.md`<br>`reports/testing/generated/runtime/nginx-runtime-results.generated.md`<br>`reports/testing/generated/coverage/phase-coverage.generated.md`<br>`reports/testing/generated/runtime/runtime-matrix.generated.md`<br>`reports/testing/generated/coverage/xfail-summary.generated.md` | complete | - | - | - |
| canonical | connector | critical | full_runtime_matrix | ci/generate-full-runtime-matrix.py | generate-full-runtime-matrix | generated | 0 | 0.351 | fresh | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.md` | complete | - | - | 2026-06-17T15:47:39Z |
| manifest | connector | critical | full_matrix_job_completeness | ci/generate-full-matrix-job-completeness.py | generate-full-matrix-job-completeness | generated | 0 | 0.966 | fresh | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json`<br>`reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | complete | - | - | 2026-06-17T15:47:40Z |
| manifest | connector | critical | verified_runtime_mismatch_analysis | ci/generate-verified-runtime-mismatch-analysis.py | generate-verified-runtime-mismatch-analysis | generated | 0 | 5.388 | fresh | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json`<br>`reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | complete | - | - | 2026-06-17T15:47:45Z |
| manifest | connector | critical | nginx_mrts_http500_cluster_analysis | ci/generate-nginx-mrts-http500-cluster-analysis.py | generate-nginx-mrts-http500-cluster-analysis | generated | 0 | 0.404 | fresh | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json`<br>`reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | complete | - | - | 2026-06-17T15:47:46Z |
| work-queues | connector | important | connector_work_queue | framework:ci/generate-connector-work-queue.py | generate-work-queue | generated | 0 | 3.909 | fresh | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.md` | complete | - | - | 2026-06-17T15:47:49Z |
| work-queues | connector | important | phase_work_queue | framework:ci/generate-phase-work-queue.py | generate-phase-work-queue | generated | 0 | 1.094 | fresh | `reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-17T15:47:50Z |
| mixed | connector | informational | native_mrts_reports | framework:ci/generate-mrts-native-report.py | mrts-native-full-run | skipped_stale_input | 0 | 0.496 | skipped | `reports/testing/generated/mrts-native/mrts-native-full.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-full.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | complete | - | - | 2026-06-17T15:47:51Z |
| focused-analysis | connector | informational | nolog_audit_evidence | ci/generate-nolog-audit-evidence-analysis.py | generate-nolog-audit-evidence-analysis | generated | 0 | 1.741 | fresh | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json`<br>`reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-17T15:47:53Z |
| focused-analysis | connector | informational | response_header_hook_analysis | ci/generate-response-header-hook-analysis.py | generate-response-header-hook-analysis | generated | 0 | 3.529 | fresh | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | complete | - | - | 2026-06-17T15:47:56Z |
| focused-analysis | connector | informational | phase4_hard_abort_capability | ci/generate-phase4-hard-abort-capability.py | generate-phase4-hard-abort-capability | blocked | 0 | 0.785 | fresh | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json`<br>`reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | blocked | - | - | 2026-06-17T15:47:57Z |
| canonical | connector | important | remaining_failure_analysis | ci/generate-remaining-failure-analysis.py | generate-remaining-failure-analysis | blocked | 0 | 2.177 | fresh | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.md`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.md`<br>`reports/testing/generated/canonical/full-run-evidence.generated.json`<br>`reports/testing/generated/canonical/full-run-evidence.generated.md` | blocked | - | - | 2026-06-17T15:47:58Z |
| focused-analysis | connector | informational | intervention_blocking_analysis | ci/generate-intervention-blocking-analysis.py | generate-intervention-blocking-analysis | blocked | 0 | 1.154 | fresh | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | blocked | - | - | 2026-06-17T15:48:00Z |
| focused-analysis | connector | informational | no_mrts_intervention_nomatch_analysis | ci/generate-no-mrts-intervention-nomatch-analysis.py | generate-no-mrts-intervention-nomatch-analysis | blocked | 0 | 0.234 | fresh | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | blocked | - | - | 2026-06-17T15:48:01Z |
| focused-analysis | connector | informational | body_processor_analysis | ci/generate-body-processor-analysis.py | generate-body-processor-analysis | blocked | 0 | 1.081 | fresh | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | blocked | - | - | 2026-06-17T15:48:01Z |
| focused-analysis | connector | informational | rule_chain_semantics_analysis | ci/generate-rule-chain-semantics-analysis.py | generate-rule-chain-semantics-analysis | blocked | 0 | 0.739 | fresh | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | blocked | - | - | 2026-06-17T15:48:02Z |
| canonical | connector | critical | final_consistency_audit | ci/generate-final-consistency-audit.py | generate-final-consistency-audit | blocked | 0 | 1.284 | fresh | `reports/testing/generated/canonical/final-consistency-audit.generated.json`<br>`reports/testing/generated/canonical/final-consistency-audit.generated.md` | blocked | - | - | 2026-06-17T15:48:03Z |
| mixed | connector | informational | runtime_cache_reports | ci/update-runtime-reports.py | prepare-runtime-components | generated | 0 | 0.198 | fresh | `reports/testing/generated/cache/runtime-component-cache.generated.json`<br>`reports/testing/generated/cache/runtime-component-cache.generated.md`<br>`reports/testing/generated/cache/runtime-build-cache.generated.json`<br>`reports/testing/generated/cache/runtime-build-cache.generated.md` | complete | - | - | 2026-06-17T15:19:04Z |
| manifest | manifest | important | report_dependency_graph | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-dependency-graph.generated.json`<br>`reports/testing/generated/manifest/report-dependency-graph.generated.md` | blocked | - | - | 2026-06-17T15:48:04Z |
| manifest | manifest | important | report_data_lineage | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-data-lineage.generated.json`<br>`reports/testing/generated/manifest/report-data-lineage.generated.md` | blocked | - | - | 2026-06-17T15:48:04Z |
| manifest | manifest | important | report_path_migration | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-path-migration.generated.json`<br>`reports/testing/generated/manifest/report-path-migration.generated.md` | unknown | - | - | 2026-06-17T15:48:04Z |
| manifest | manifest | informational | generator_runtime_summary | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | unknown | - | - | 2026-06-17T15:48:04Z |
| manifest | manifest | important | report_freshness | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-freshness.generated.json`<br>`reports/testing/generated/manifest/report-freshness.generated.md` | blocked | - | - | 2026-06-17T15:48:04Z |
| manifest | manifest | critical | merge_readiness_dashboard | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json`<br>`reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | blocked | - | - | 2026-06-17T15:48:04Z |
| manifest | manifest | critical | report_refresh_manifest | ci/refresh-connector-reports.py | refresh-connector-reports | generated | 0 | 0.0 | fresh | `reports/testing/generated/manifest/report-refresh-manifest.generated.json`<br>`reports/testing/generated/manifest/report-refresh-manifest.generated.md` | unknown | - | - | 2026-06-17T15:48:04Z |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `reports/testing/test-coverage-overview.md` | `c9931aa8c2c7205af54c69f8737ea29747c076263a46c8dccf298db9c7d678a0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | `0e6deb594e359774332e0686f4c68c80efc3b73ec8c1fe12acfd485094911a54` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/case-matrix.generated.md` | `82170b75b5c954556c8c2b4e0f9087c440ac5e051a324690fe3292a7df175a21` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | `5670cf1774cffc12ddb197c092f123c9e835aa0cd069f50d71aba972f8535b98` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/coverage-summary.generated.md` | `364fab3c109351eec73f089603924a3bac54df49eadf01b6f9a9a4019e219d1f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | `12e8a53cf644bc5dd7206c76782823e355de7d2a22c1f313b710d66c17a764e3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | `766de1fb6db9286a4540b4276ec5d538812e8dcebed98cc5fd008a36351df3cd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `cde76d3bbc7355f8c9e8c9dc7b53049c56e19459e4d1fc5818fc85f62c4e63bd` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/runtime/runtime-matrix.generated.md` | `8fe4e12c6a8def0279bbc6c1c5a4b49f1f4f6824f2c4a4320fa48045092b6059` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/coverage/xfail-summary.generated.md` | `6566cf146e53536b131d36971eb75215a7ad1930a5c638f4b2cc41d58c8ae5cc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `b73e9279de250d71c12b771bc4c24bb4b712dac0fed0008c60f6075116916797` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.md` | `4fd61ee3e8f69aeb8c9878032d06b89c40e5f9ecf8a1c94de55a367315c94628` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `bd7f3ba3382d7800e5de9bcf7eb1d28a26b0317b1a5aae2089b5f5812acddc78` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | `6dd15643a1999a514525546dd8f5f36f96f48c72c40bd459ef135f9364369078` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `6bc04b7e3157faa5f7d32e333051db6fe568b604eef038f0706c32d1f2028cac` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | `86b58791c3eab8d6cba377162963dd6afafea6dd4d3b0a761cc3d795d542d05c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json` | `b32116e21ebda7c5d16e99ef78756990823300dbc2624817b2cde688b820c45b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `fda3411959f28230657b72f78a451359d04487a8cf0e55b16626fce23de0dbd7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `c747640b424f6aa6fbbf98f07407ce1dfc47c8ae2295220454554acdd5e70aa8` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.md` | `9687803ca930485c933cfcbc998da659d2780ac015eba725df84f1d040d1c549` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `29210f6193c70c53ff0d6fb934005c9e2f29129f88cb322eabb328198ae25dbf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `fd56f2d8f586423fa7a3c85068ed085bf33def6bbb516a5a4056d53566b952a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | `108230d63647f6abbb6b91ac051a96f4230af75baca4661051f90c62e559c2c8` | `2026-06-16T19-12-00Z-614c8049` | skipped_stale_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | `93cde070cc87f496b4e8e825b3edd7ca20364fbe5af8ff09700523017e1ba2ac` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `90ff4ac6d2ba5a41121be9c56fd637f52b9b7ac5c9854524ea13cd1a94266df9` | `2026-06-16T19-12-00Z-614c8049` | skipped_stale_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | `9a3e2f88b6b54d12ed0427c222cdb0e67f6a789fc348cd22d662f2db8f828b8c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `ebc4b664b9e7a9e5b8d69e1f22a719a1e725426085240726172c08c00fb66c33` | `2026-06-16T19-12-00Z-614c8049` | skipped_stale_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | `4c2012be16620245929ca8a5b06c4212be340b39a53b079651e6b7e4d7941f2c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `eb9242e77b1ed5456b66e3a9ccb94ffff873edf23b955d35254937cb8b77c040` | `2026-06-16T19-12-00Z-614c8049` | skipped_stale_input |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | `52ba885e5e23d8c2fee04d24bf3d974b9b31c1d5cb9dc08e2d392b664f4908f7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `90aeb81722723302cc20ba6994c3868717cb3056ec6a4c0b57b52b6329dbd894` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `b9fe19b5cadff17af3e812bf0a82c4099a79627f91c32e1ef93a69fde914693a` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `29210f6193c70c53ff0d6fb934005c9e2f29129f88cb322eabb328198ae25dbf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `fd56f2d8f586423fa7a3c85068ed085bf33def6bbb516a5a4056d53566b952a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `883fdce904c304d9ea0b2557badb239635568e14ae49b9d5bb54a4b4357816d1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `65e86052c3d5cc15daabf05fc3c47a904e5c425780290e626ddeb787301fdbbb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `29210f6193c70c53ff0d6fb934005c9e2f29129f88cb322eabb328198ae25dbf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `fd56f2d8f586423fa7a3c85068ed085bf33def6bbb516a5a4056d53566b952a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `70b4612471c9b05902042bac06a3fdeb02558aab7b3d3f5fb923dfb34d1ee66c` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `df5db714180215f21bc1943182632d2e3514dfd5793a2de98fad4c6b2986353d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `29210f6193c70c53ff0d6fb934005c9e2f29129f88cb322eabb328198ae25dbf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.md` | `fd56f2d8f586423fa7a3c85068ed085bf33def6bbb516a5a4056d53566b952a1` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `781564315ab245d2dd9d89e2ed9445f71d222553697e36daec83189a8d3d998b` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `15a068c18752c4d90b02ee7887f46ab68a70d9548f7dac1bdf59b3fa16ae2d4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `18f53c9539c3c8d74bd89e6549062846275bbb678857522f3f76ab99af603989` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.md` | `320ded86f5b7a0ee37441184d73ca8f94a6c827e03168da6d2d3c3564bac1356` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `df41566492fb236cb03508161261b1eedb8745fc8aa07feff56de02969cb50fb` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.md` | `46616d22a824a054b18bd0811d17cdfb2d58efc4089639111524df4907f59feb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `68692c6831e04ee96e716010e2d8cfee87fc5351914df21816c508f6346e77e4` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `0dd7637b617d4b1bd51963fd03c8f68c808f18887fd0f8d148c8427bf9e38bec` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `3f52c0b718d8e8b65705890c1540609646f224f4bac4409f7c3d39e4c177a297` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `f03d2225573d318fa763d35a39900d539870de6e6a673fb034aaa55a061fbbc0` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `0e48530472eb758d223f427075d5c03f65f78fc16e3b2e534aee95aa238293b3` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `97cd89f847c4052c7f37555ed270c6c4186a7eba6b0497caef198aec74cf057d` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `9060fe37e06facf05ca49cf4bb37ea42ac07acac63d8b9c721293b426265658b` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `8c366b0c7a0915d4c8e5dd72486550bf0d6f8f9e727e25536ef251904b5b7ad2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.json` | `702781e5bf78f77097a22e2e367dca491d4489a30e161182f9f298823200008b` | `2026-06-16T19-12-00Z-614c8049` | blocked |
| Declared input | `reports/testing/generated/canonical/final-consistency-audit.generated.md` | `f85bc9619d1d057902efe7f213432928432420592ad4598a3eb130737ed65529` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.json` | `3686a53ddbc220907f8a00c168efa62fbd55938611134ba70092fc4f2fe98fb2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-component-cache.generated.md` | `c53e98b81e7203d7baeda4aff237b44f7af303223ff5031cf776481c1c76d8cb` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.json` | `4821cf6619bec7a71578285267d8115e31224583d46a7d0f1d68f2e433cd602f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/cache/runtime-build-cache.generated.md` | `103d3a98548ca83d916e205fd9643eef1e870c56af3506c35fbae9000168435b` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.json` | `a58e2e3576f9a27d2a3583556b764f9c40afffe179669b23a136a31d3a1a7963` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-dependency-graph.generated.md` | `3a9c73c50275b785e0bd7548c0f5c8706aebb237729519db81bed1b836056ecf` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.json` | `a0fe30f1d98af7032217f8c234b7e211f417ac0589c32e15c44c7d1d1e5a2bb9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-data-lineage.generated.md` | `af070bdce520dbf7f162146ea40aad9464b258a716c0e67056b429a32b3586ec` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.json` | `1a183069cb578174931317f3445aa6231ccb62700a427c2c3c0bc65a2529a867` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-path-migration.generated.md` | `314226519b216ba9259c4259fe7bd02506c21e725913d320d56e2ce3b8607294` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | `2d06a35adce6092112d25570e185a26bcc4e1f6061af054c9aca70da53520200` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.json` | `0c036a4c26146a877bf7071392cd519df44326eea28d9fd2ff1dfb6d2a2822f5` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/report-freshness.generated.md` | `af251c45e8a9565aef0fef5f7c4aaea75d0713cbf15b323abd5ffe5897e0c0a3` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json` | `4bcd8974231779d1a792c923d74e43a534a689110fda69bf619eede9a5098508` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | `46d82a703235bf085bd30208bef0fe4b44fd611a1c42f7254becc0999c77e057` | `2026-06-16T19-12-00Z-614c8049` | present |

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
| `reports/testing/generated/mrts-native/mrts-native-full.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-full.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | present | input file available |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | skipped_stale_input | generated report input is not usable: status=skipped_stale_input |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | blocked | generated report input is not usable: status=blocked |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | present | input file available |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | present | input file available |
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
