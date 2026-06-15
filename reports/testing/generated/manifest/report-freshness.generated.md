> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:40:38Z`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `partial`

# Report Freshness

| Report | Status | Generated At | Newest Input | Newest Output | Missing Inputs | Notes |
|---|---|---|---|---|---|---|
| `connector_coverage_reports` | fresh | - | 2026-06-14T20:12:16Z | 2026-06-15T10:39:50Z | - | generated |
| `full_runtime_matrix` | fresh | 2026-06-15T10:39:51Z | 2026-06-13T20:00:51Z | 2026-06-15T10:39:51Z | - | generated |
| `connector_work_queue` | fresh | 2026-06-15T10:39:55Z | 2026-06-15T10:39:51Z | 2026-06-15T10:39:55Z | - | generated |
| `phase_work_queue` | fresh | 2026-06-15T10:39:56Z | 2026-06-15T10:39:55Z | 2026-06-15T10:39:56Z | - | generated |
| `native_mrts_reports` | missing-input | 2026-06-15T10:39:57Z | - | 2026-06-15T10:39:57Z | BUILD_ROOT:mrts-native/apache2_ubuntu/job.json, BUILD_ROOT:mrts-native/nginx-pr24/job.json | generated |
| `nolog_audit_evidence` | fresh | 2026-06-15T10:39:59Z | 2026-06-15T10:39:58Z | 2026-06-15T10:39:59Z | - | generated |
| `response_header_hook_analysis` | fresh | 2026-06-15T10:40:03Z | 2026-06-15T10:40:02Z | 2026-06-15T10:40:03Z | - | generated |
| `phase4_hard_abort_capability` | fresh | 2026-06-15T10:40:07Z | 2026-06-15T10:40:02Z | 2026-06-15T10:40:07Z | - | generated |
| `remaining_failure_analysis` | fresh | 2026-06-15T10:40:09Z | 2026-06-15T10:40:07Z | 2026-06-15T10:40:24Z | - | generated |
| `intervention_blocking_analysis` | fresh | 2026-06-15T10:40:29Z | 2026-06-15T10:40:23Z | 2026-06-15T10:40:29Z | - | generated |
| `no_mrts_intervention_nomatch_analysis` | fresh | 2026-06-15T10:40:30Z | 2026-06-15T10:40:29Z | 2026-06-15T10:40:30Z | - | generated |
| `body_processor_analysis` | fresh | 2026-06-15T10:40:36Z | 2026-06-15T10:40:23Z | 2026-06-15T10:40:36Z | - | generated |
| `rule_chain_semantics_analysis` | fresh | 2026-06-15T10:40:37Z | 2026-06-15T10:40:23Z | 2026-06-15T10:40:37Z | - | generated |
| `final_consistency_audit` | fresh | 2026-06-15T10:40:37Z | 2026-06-15T10:40:38Z | 2026-06-15T10:40:38Z | - | generated |
| `runtime_cache_reports` | skipped | - | - | - | reports/testing/generated/cache/runtime-component-cache.generated.json, reports/testing/generated/cache/runtime-build-cache.generated.json | skipped_missing_input |
| `report_dependency_graph` | missing-input | 2026-06-15T10:40:38Z | 2026-06-15T10:40:38Z | 2026-06-15T10:40:39Z | BUILD_ROOT:mrts-native/apache2_ubuntu/job.json, BUILD_ROOT:mrts-native/nginx-pr24/job.json, reports/testing/generated/cache/runtime-build-cache.generated.json, reports/testing/generated/cache/runtime-component-cache.generated.json | generated |
| `report_data_lineage` | missing-input | 2026-06-15T10:40:38Z | 2026-06-15T10:40:38Z | 2026-06-15T10:40:39Z | BUILD_ROOT:mrts-native/apache2_ubuntu/job.json, BUILD_ROOT:mrts-native/nginx-pr24/job.json, reports/testing/generated/cache/runtime-build-cache.generated.json, reports/testing/generated/cache/runtime-component-cache.generated.json | generated |
| `report_path_migration` | fresh | 2026-06-15T10:40:38Z | - | 2026-06-15T10:40:39Z | - | generated |
| `generator_runtime_summary` | fresh | 2026-06-15T10:40:38Z | - | 2026-06-15T10:40:40Z | - | generated |
| `report_freshness` | missing-input | 2026-06-15T10:40:38Z | 2026-06-15T10:40:40Z | 2026-06-15T10:40:40Z | reports/testing/generated/cache/runtime-component-cache.generated.json, reports/testing/generated/cache/runtime-component-cache.generated.md, reports/testing/generated/cache/runtime-build-cache.generated.json, reports/testing/generated/cache/runtime-build-cache.generated.md | generated |
| `merge_readiness_dashboard` | fresh | 2026-06-15T10:40:38Z | 2026-06-15T10:40:40Z | 2026-06-15T10:40:41Z | - | generated |
| `report_refresh_manifest` | fresh | 2026-06-15T10:40:38Z | - | 2026-06-15T10:39:36Z | - | generated |

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
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | present | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | present | input file available |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.json` | present | input file available |
| `reports/testing/generated/canonical/final-consistency-audit.generated.md` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | present | input file available |
| `reports/testing/generated/canonical/full-run-evidence.generated.md` | present | input file available |
| `reports/testing/generated/cache/runtime-component-cache.generated.json` | missing | input file missing |
| `reports/testing/generated/cache/runtime-component-cache.generated.md` | missing | input file missing |
| `reports/testing/generated/cache/runtime-build-cache.generated.json` | missing | input file missing |
| `reports/testing/generated/cache/runtime-build-cache.generated.md` | missing | input file missing |
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
| `reports/testing/generated/manifest/report-refresh-manifest.generated.json` | present | input file available |
| `reports/testing/generated/manifest/report-refresh-manifest.generated.md` | present | input file available |
