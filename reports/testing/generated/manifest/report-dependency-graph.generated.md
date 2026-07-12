> Generated file - do not edit manually.
>
> Generated at: `2026-07-12T20:12:32Z`
> Verified run id: `2026-06-16T19-12-00Z-614c8049`
> Data source policy: `verified-inputs-only`
> Generator: `ci/evidence/reports/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `important`
> Connector SHA: `9b718cee0523da3e0822754dc4b05f327b6d969d`
> Framework SHA: `4e9d4ba616235127b6fc0a2ee87107d93d03f40b`
> Input status: `stale`

# Report Dependency Graph

**Language:** English | [Deutsch](report-dependency-graph.generated.de.md)

## Mermaid

```mermaid
flowchart TD
  report_refresh_manifest["report-refresh-manifest.generated"]
  report_dependency_graph["report-dependency-graph.generated"]
  report_data_lineage["report-data-lineage.generated"]
  report_freshness["report-freshness.generated"]
  report_path_migration["report-path-migration.generated"]
  generator_runtime_summary["generator-runtime-summary.generated"]
  verified_run_manifest["verified-run-manifest.generated"]
  merge_readiness_dashboard["merge-readiness-dashboard.generated"]
  connector_roadmap["connector-roadmap.generated"]
  connector_capabilities["connector-capabilities.generated"]
  verified_runtime_mismatch_analysis["verified-runtime-mismatch-analysis.generated"]
  remaining_critical_batch_analysis["remaining-critical-batch-analysis.generated"]
  native_semantics_comparison["native-semantics-comparison.generated"]
  full_matrix_job_completeness["full-matrix-job-completeness.generated"]
  nginx_mrts_http500_cluster_analysis["nginx-mrts-http500-cluster-analysis.generated"]
  system_environment_proof["system-environment-proof.generated"]
  full_runtime_matrix["full-runtime-matrix.generated"]
  full_run_evidence["full-run-evidence.generated"]
  final_consistency_audit["final-consistency-audit.generated"]
  remaining_failure_analysis["remaining-failure-analysis.generated"]
  next_fix_plan["next-fix-plan.generated"]
  connector_work_queue["connector-work-queue.generated"]
  phase_work_queue["phase-work-queue.generated"]
  case_matrix["case-matrix.generated"]
  connector_gap_summary["connector-gap-summary.generated"]
  coverage_summary["coverage-summary.generated"]
  phase_coverage["phase-coverage.generated"]
  xfail_summary["xfail-summary.generated"]
  body_processor_analysis["body-processor-analysis.generated"]
  intervention_blocking_analysis["intervention-blocking-analysis.generated"]
  no_mrts_intervention_nomatch_analysis["no-mrts-intervention-nomatch-analysis.generated"]
  nolog_audit_evidence["nolog-audit-evidence.generated"]
  phase4_hard_abort_capability["phase4-hard-abort-capability.generated"]
  response_header_hook_analysis["response-header-hook-analysis.generated"]
  rule_chain_semantics_analysis["rule-chain-semantics-analysis.generated"]
  apache_runtime_results["apache-runtime-results.generated"]
  nginx_runtime_results["nginx-runtime-results.generated"]
  haproxy_runtime_results["haproxy-runtime-results.generated"]
  runtime_matrix["runtime-matrix.generated"]
  mrts_native_full["mrts-native-full.generated"]
  mrts_native_apache["mrts-native-apache.generated"]
  mrts_native_nginx["mrts-native-nginx.generated"]
  mrts_native_summary["mrts-native-summary.generated"]
  runtime_build_cache["runtime-build-cache.generated"]
  runtime_component_cache["runtime-component-cache.generated"]
  runtime_cache_index["runtime-cache-index.generated"]
  body_processor_analysis --> final_consistency_audit
  connector_work_queue --> body_processor_analysis
  connector_work_queue --> final_consistency_audit
  connector_work_queue --> full_run_evidence
  connector_work_queue --> intervention_blocking_analysis
  connector_work_queue --> next_fix_plan
  connector_work_queue --> nolog_audit_evidence
  connector_work_queue --> phase4_hard_abort_capability
  connector_work_queue --> phase_work_queue
  connector_work_queue --> remaining_failure_analysis
  connector_work_queue --> response_header_hook_analysis
  connector_work_queue --> rule_chain_semantics_analysis
  full_matrix_job_completeness --> nginx_mrts_http500_cluster_analysis
  full_run_evidence --> final_consistency_audit
  full_runtime_matrix --> connector_work_queue
  full_runtime_matrix --> final_consistency_audit
  full_runtime_matrix --> full_run_evidence
  full_runtime_matrix --> intervention_blocking_analysis
  full_runtime_matrix --> next_fix_plan
  full_runtime_matrix --> no_mrts_intervention_nomatch_analysis
  full_runtime_matrix --> nolog_audit_evidence
  full_runtime_matrix --> phase4_hard_abort_capability
  full_runtime_matrix --> phase_work_queue
  full_runtime_matrix --> remaining_failure_analysis
  full_runtime_matrix --> response_header_hook_analysis
  full_runtime_matrix --> rule_chain_semantics_analysis
  intervention_blocking_analysis --> final_consistency_audit
  intervention_blocking_analysis --> no_mrts_intervention_nomatch_analysis
  mrts_native_apache --> phase4_hard_abort_capability
  mrts_native_nginx --> phase4_hard_abort_capability
  mrts_native_summary --> final_consistency_audit
  mrts_native_summary --> full_run_evidence
  mrts_native_summary --> next_fix_plan
  mrts_native_summary --> remaining_failure_analysis
  next_fix_plan --> body_processor_analysis
  next_fix_plan --> final_consistency_audit
  next_fix_plan --> intervention_blocking_analysis
  next_fix_plan --> no_mrts_intervention_nomatch_analysis
  next_fix_plan --> rule_chain_semantics_analysis
  no_mrts_intervention_nomatch_analysis --> final_consistency_audit
  nolog_audit_evidence --> final_consistency_audit
  phase4_hard_abort_capability --> final_consistency_audit
  phase_coverage --> nolog_audit_evidence
  phase_coverage --> phase_work_queue
  phase_coverage --> response_header_hook_analysis
  phase_work_queue --> body_processor_analysis
  phase_work_queue --> final_consistency_audit
  phase_work_queue --> full_run_evidence
  phase_work_queue --> intervention_blocking_analysis
  phase_work_queue --> next_fix_plan
  phase_work_queue --> remaining_failure_analysis
  remaining_failure_analysis --> body_processor_analysis
  remaining_failure_analysis --> final_consistency_audit
  remaining_failure_analysis --> intervention_blocking_analysis
  remaining_failure_analysis --> no_mrts_intervention_nomatch_analysis
  remaining_failure_analysis --> rule_chain_semantics_analysis
  response_header_hook_analysis --> final_consistency_audit
  rule_chain_semantics_analysis --> final_consistency_audit
  verified_runtime_mismatch_analysis --> native_semantics_comparison
  verified_runtime_mismatch_analysis --> nginx_mrts_http500_cluster_analysis
```

## Reports

| Report | Inputs | Outputs | Dependencies |
|---|---|---|---|
| `report_refresh_manifest` | - | `reports/testing/generated/manifest/report-refresh-manifest.generated.json`<br>`reports/testing/generated/manifest/report-refresh-manifest.generated.md` | - |
| `report_dependency_graph` | - | `reports/testing/generated/manifest/report-dependency-graph.generated.json`<br>`reports/testing/generated/manifest/report-dependency-graph.generated.md` | - |
| `report_data_lineage` | - | `reports/testing/generated/manifest/report-data-lineage.generated.json`<br>`reports/testing/generated/manifest/report-data-lineage.generated.md` | - |
| `report_freshness` | - | `reports/testing/generated/manifest/report-freshness.generated.json`<br>`reports/testing/generated/manifest/report-freshness.generated.md` | - |
| `report_path_migration` | - | `reports/testing/generated/manifest/report-path-migration.generated.json`<br>`reports/testing/generated/manifest/report-path-migration.generated.md` | - |
| `generator_runtime_summary` | - | `reports/testing/generated/manifest/generator-runtime-summary.generated.md` | - |
| `verified_run_manifest` | - | `reports/testing/generated/manifest/verified-run-manifest.generated.json`<br>`reports/testing/generated/manifest/verified-run-manifest.generated.md` | - |
| `merge_readiness_dashboard` | - | `reports/testing/generated/manifest/merge-readiness-dashboard.generated.json`<br>`reports/testing/generated/manifest/merge-readiness-dashboard.generated.md` | - |
| `connector_roadmap` | `connectors`<br>`Makefile`<br>`ci`<br>`config`<br>`docs`<br>`reports/testing/generated` | `reports/testing/generated/manifest/connector-roadmap.generated.json`<br>`reports/testing/generated/manifest/connector-roadmap.generated.md` | - |
| `connector_capabilities` | `connectors/apache/capabilities.json`<br>`connectors/nginx/capabilities.json`<br>`connectors/haproxy/capabilities.json`<br>`connectors/envoy/capabilities.json`<br>`connectors/traefik/capabilities.json`<br>`connectors/lighttpd/capabilities.json` | `reports/testing/generated/canonical/connector-capabilities.generated.json`<br>`reports/testing/generated/canonical/connector-capabilities.generated.md` | - |
| `verified_runtime_mismatch_analysis` | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json`<br>`<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json`<br>`reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.md` | - |
| `remaining_critical_batch_analysis` | - | `reports/testing/generated/manifest/remaining-critical-batch-analysis.generated.json`<br>`reports/testing/generated/manifest/remaining-critical-batch-analysis.generated.md` | - |
| `native_semantics_comparison` | `ci/runtime/lifecycle/run-native-case-comparison.py`<br>`ci/tools/native_modsecurity_oracle.c`<br>`reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `reports/testing/generated/manifest/native-semantics-comparison.generated.json`<br>`reports/testing/generated/manifest/native-semantics-comparison.generated.md` | `verified_runtime_mismatch_analysis` |
| `full_matrix_job_completeness` | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json`<br>`<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json`<br>`reports/testing/generated/manifest/full-matrix-job-completeness.generated.md` | - |
| `nginx_mrts_http500_cluster_analysis` | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json`<br>`<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl`<br>`reports/testing/generated/manifest/full-matrix-job-completeness.generated.json`<br>`reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.json`<br>`reports/testing/generated/manifest/nginx-mrts-http500-cluster-analysis.generated.md` | `full_matrix_job_completeness`, `verified_runtime_mismatch_analysis` |
| `system_environment_proof` | - | `reports/testing/generated/manifest/system-environment-proof.generated.json`<br>`reports/testing/generated/manifest/system-environment-proof.generated.md` | - |
| `full_runtime_matrix` | `<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.md` | - |
| `full_run_evidence` | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `reports/testing/generated/canonical/full-run-evidence.generated.json`<br>`reports/testing/generated/canonical/full-run-evidence.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `mrts_native_summary`, `phase_work_queue` |
| `final_consistency_audit` | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json`<br>`reports/testing/generated/canonical/full-run-evidence.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json`<br>`reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json`<br>`reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json`<br>`reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/body-processor-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `reports/testing/generated/canonical/final-consistency-audit.generated.json`<br>`reports/testing/generated/canonical/final-consistency-audit.generated.md` | `body_processor_analysis`, `connector_work_queue`, `full_run_evidence`, `full_runtime_matrix`, `intervention_blocking_analysis`, `mrts_native_summary`, `next_fix_plan`, `no_mrts_intervention_nomatch_analysis`, `nolog_audit_evidence`, `phase4_hard_abort_capability`, `phase_work_queue`, `remaining_failure_analysis`, `response_header_hook_analysis`, `rule_chain_semantics_analysis` |
| `remaining_failure_analysis` | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `mrts_native_summary`, `phase_work_queue` |
| `next_fix_plan` | `reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `reports/testing/generated/canonical/next-fix-plan.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `mrts_native_summary`, `phase_work_queue` |
| `connector_work_queue` | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/work-queues/connector-work-queue.generated.md` | `full_runtime_matrix` |
| `phase_work_queue` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/coverage/phase-coverage.generated.md`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `phase_coverage` |
| `case_matrix` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/coverage/case-matrix.generated.md` | - |
| `connector_gap_summary` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/coverage/connector-gap-summary.generated.md` | - |
| `coverage_summary` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/coverage/coverage-summary.generated.md` | - |
| `phase_coverage` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/coverage/phase-coverage.generated.md` | - |
| `xfail_summary` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/coverage/xfail-summary.generated.md` | - |
| `body_processor_analysis` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json` | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/body-processor-analysis.generated.md` | `connector_work_queue`, `next_fix_plan`, `phase_work_queue`, `remaining_failure_analysis` |
| `intervention_blocking_analysis` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/work-queues/phase-work-queue.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json` | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `next_fix_plan`, `phase_work_queue`, `remaining_failure_analysis` |
| `no_mrts_intervention_nomatch_analysis` | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json` | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.md` | `full_runtime_matrix`, `intervention_blocking_analysis`, `next_fix_plan`, `remaining_failure_analysis` |
| `nolog_audit_evidence` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/coverage/phase-coverage.generated.md` | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json`<br>`reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `phase_coverage` |
| `phase4_hard_abort_capability` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json`<br>`reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `mrts_native_apache`, `mrts_native_nginx` |
| `response_header_hook_analysis` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.json`<br>`reports/testing/generated/coverage/phase-coverage.generated.md` | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `phase_coverage` |
| `rule_chain_semantics_analysis` | `reports/testing/generated/work-queues/connector-work-queue.generated.json`<br>`reports/testing/generated/canonical/remaining-failure-analysis.generated.json`<br>`reports/testing/generated/canonical/next-fix-plan.generated.json`<br>`reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json`<br>`reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.md` | `connector_work_queue`, `full_runtime_matrix`, `next_fix_plan`, `remaining_failure_analysis` |
| `apache_runtime_results` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/runtime/apache-runtime-results.generated.md` | - |
| `nginx_runtime_results` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/runtime/nginx-runtime-results.generated.md` | - |
| `haproxy_runtime_results` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/runtime/haproxy-runtime-results.generated.md` | - |
| `runtime_matrix` | `config/testing/import-status.json`<br>`reports/testing/runtime-validation-snapshot.json` | `reports/testing/generated/runtime/runtime-matrix.generated.md` | - |
| `mrts_native_full` | `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json`<br>`<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | `reports/testing/generated/mrts-native/mrts-native-full.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-full.generated.md` | - |
| `mrts_native_apache` | `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json`<br>`<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-apache.generated.md` | - |
| `mrts_native_nginx` | `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json`<br>`<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-nginx.generated.md` | - |
| `mrts_native_summary` | `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json`<br>`<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json`<br>`reports/testing/generated/mrts-native/mrts-native-summary.generated.md` | - |
| `runtime_build_cache` | `<verified-run-root>/cache-v2/shared/manifest.json`<br>`<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | `reports/testing/generated/cache/runtime-build-cache.generated.json`<br>`reports/testing/generated/cache/runtime-build-cache.generated.md` | - |
| `runtime_component_cache` | `<verified-run-root>/cache-v2/shared/manifest.json`<br>`<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | `reports/testing/generated/cache/runtime-component-cache.generated.json`<br>`reports/testing/generated/cache/runtime-component-cache.generated.md` | - |
| `runtime_cache_index` | `<verified-run-root>/cache-v2/shared/manifest.json`<br>`<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | `reports/testing/generated/cache/runtime-cache-index.generated.json`<br>`reports/testing/generated/cache/runtime-cache-index.generated.md` | - |

## Root Inputs

- `<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl`
- `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json`
- `<verified-run-root>/build/mrts-native/nginx-pr24/job.json`
- `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json`
- `<verified-run-root>/cache-v2/shared/manifest.json`
- `<verified-run-root>/cache-v2/shared/runtime-build-cache.json`
- `Makefile`
- `ci`
- `ci/runtime/lifecycle/run-native-case-comparison.py`
- `ci/tools/native_modsecurity_oracle.c`
- `config`
- `config/testing/import-status.json`
- `connectors`
- `connectors/apache/capabilities.json`
- `connectors/envoy/capabilities.json`
- `connectors/haproxy/capabilities.json`
- `connectors/lighttpd/capabilities.json`
- `connectors/nginx/capabilities.json`
- `connectors/traefik/capabilities.json`
- `docs`
- `reports/testing/generated`
- `reports/testing/runtime-validation-snapshot.json`

## Final Reports

- `final_consistency_audit`
- `full_run_evidence`
- `merge_readiness_dashboard`

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | `unknown` | `2026-06-16T19-12-00Z-614c8049` | missing |
| Declared input | `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json` | `unknown` | `2026-06-16T19-12-00Z-614c8049` | missing |
| Declared input | `<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | `unknown` | `2026-06-16T19-12-00Z-614c8049` | missing |
| Declared input | `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `unknown` | `2026-06-16T19-12-00Z-614c8049` | missing |
| Declared input | `<verified-run-root>/cache-v2/shared/manifest.json` | `13123f03dbe90f01402a8c2c439e46455a0fa688448e540a5cdab11722022392` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | `04ba882c6feda15868fc9b175f3d3c2875fdbdfa480872a332d8317edea1b017` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `Makefile` | `e81bc90df73a382f0e4a199f81e39b97335667b73060407a8a145a0803702a01` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `ci` | `ddf1490014048ffaaf92e1aad9ad3b474486f5cb49ab4b5caa067fa2c44517d7` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `ci/runtime/lifecycle/run-native-case-comparison.py` | `fb502563cb45d7862033e58aec5e1c37f7084f55af3e85741ce8341c55a91c9c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `ci/tools/native_modsecurity_oracle.c` | `57bcb4e66611f597b623599680807795296193e156d4bd91c694422f9eb0f9db` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `config` | `c72a2c9c7ccf6252032ef6d044e1170edd65cf4b02202d25addc21949eb3bd83` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `config/testing/import-status.json` | `5eea82df1ded18c34bbc8cf6fc5992572edaa6723a33b6dd4a0b49ee00ab5a4f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors` | `794c7060fe47b86b9f899dc4e39562f0c879bfa68b65e00efb9dd70840584e19` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/apache/capabilities.json` | `95ba425551d9261bbbf4693c989f55468da78f7a2a6efa6eca8dc0ad69833a59` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/envoy/capabilities.json` | `b38f59423c0908064eeb9b253eafa83f3606e4d755ef78e0837ed39100e61216` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/haproxy/capabilities.json` | `b8e3ca621904e925580604d5b7af1c97cf0a4c01a4c7a42cc7c58fae4c9d599c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/lighttpd/capabilities.json` | `4aac60435527d7a17ddc11deb14ae49f5a48e15c8a357c0ea45627fa4dc82995` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/nginx/capabilities.json` | `70fa6bb202c0ac3ea8292fa654a98586852b238e1885e43e7d5235e7daa0a982` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `connectors/traefik/capabilities.json` | `04dbf29b4ed7085f1db172619b0957e6dc740964b9741c736b70e158fe904adc` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `docs` | `791125d2131a185596df3d066193483cb2b49e002bb0c2e0bbda3db68cc3766c` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated` | `ada391ed04c9b86c45926679ee9f8f1fd5a544adb6ca5d6d1c248c2c1657c634` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/canonical/full-run-evidence.generated.json` | `486d395cbc4da9e489dcc2f81e0fda69c34e66971e03133f02f797570f9a2400` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | `3f41446a7fb73a361c12e31507673774698ec41d108f2c8e75c8c57b8d2ef007` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/next-fix-plan.generated.json` | `45c592a17f99671474b5f510d59c5c5f162861bcc74e37f4a7c72e6e4bc6a736` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | `c581790d4581ac9cf843e973f127b274784caf286d1661d72b5144f078049165` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/coverage/phase-coverage.generated.md` | `7da89e3821de5ee8fdc4c129dcd766a10eed8eece8c1cd928b58b531fcf30872` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | `4ca4fc4f48a5420c3dc9892faa3d53b1b28b322dc49fcc3adc6e341681465be4` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | `256bdac6851d1bea706d7ae21377412ce79edb977969ec5774e0b27a6ae56a8e` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | `a163cfa2dd4408fb802138a063f4651c6c930b4799b6089976083e19a45b5082` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | `4cc4b220df8adb4ebdb3e8666a41be8c1e37660ba0baf0a37e489087415dca4c` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | `6e00d5cd2e1239d414915f89feca72d744dcaf27d5c224513dc78ed3db310682` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | `7d73f40c3ec211958b2eb5979a0c45f13303b53da032a90f96f00d8d77da5092` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | `97fca3207c05713f8e25bc092e5bf9e9ab65c7f36e5ba1da28cece9ff7637636` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `a54dc3f43ffc6d2eb4493ad56c58e6eff959cb2ce1380f5eb3d4b4e02003f5c2` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `340546dbab42432eef255f99fda65c0d4301db589d6ac5c9f2a201a94326420e` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | `a628c7910973dfe3ea2379d1de447632bb7a68bc93945814d7e5922711b01933` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | `dcb7aea74fa53c58425123bf580dbe52ae9898bbc0af29bd38ee98925848c833` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | `8b8298f135b70c6487dcfbae620801fc09fabe03e73c91fe8657a27505216bce` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/connector-work-queue.generated.json` | `89f3d29f508ef24e279589f6a3fa791c2f62d5a13ca89f58b10adb4ba4cd3484` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/generated/work-queues/phase-work-queue.generated.json` | `de46f52db4aa93f393cf9e7a97ef734435d9e9d7f9af4c99ceed8294867d9a1b` | `2026-06-16T19-12-00Z-614c8049` | stale |
| Declared input | `reports/testing/runtime-validation-snapshot.json` | `d3017f038a44a5f5596e36e3482f92cd93ce6f2173bb958da98cddc05884cd8f` | `2026-06-16T19-12-00Z-614c8049` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/build/full-matrix/full-runtime-matrix-runs.jsonl` | missing | input file missing |
| `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json` | missing | input file missing |
| `<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | missing | input file missing |
| `<verified-run-root>/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | missing | input file missing |
| `<verified-run-root>/cache-v2/shared/manifest.json` | present | input file available |
| `<verified-run-root>/cache-v2/shared/runtime-build-cache.json` | present | input file available |
| `Makefile` | present | input file available |
| `ci` | present | input directory available |
| `ci/runtime/lifecycle/run-native-case-comparison.py` | present | input file available |
| `ci/tools/native_modsecurity_oracle.c` | present | input file available |
| `config` | present | input directory available |
| `config/testing/import-status.json` | present | input file available |
| `connectors` | present | input directory available |
| `connectors/apache/capabilities.json` | present | input file available |
| `connectors/envoy/capabilities.json` | present | input file available |
| `connectors/haproxy/capabilities.json` | present | input file available |
| `connectors/lighttpd/capabilities.json` | present | input file available |
| `connectors/nginx/capabilities.json` | present | input file available |
| `connectors/traefik/capabilities.json` | present | input file available |
| `docs` | present | input directory available |
| `reports/testing/generated` | present | input directory available |
| `reports/testing/generated/canonical/full-run-evidence.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/full-runtime-matrix.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/next-fix-plan.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/canonical/remaining-failure-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/coverage/phase-coverage.generated.md` | stale | generated report input is stale: framework_sha differs |
| `reports/testing/generated/focused-analysis/body-processor-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/intervention-blocking-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/no-mrts-intervention-nomatch-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/nolog-audit-evidence.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/phase4-hard-abort-capability.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/response-header-hook-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/focused-analysis/rule-chain-semantics-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-apache.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-nginx.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/mrts-native/mrts-native-summary.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/connector-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/generated/work-queues/phase-work-queue.generated.json` | stale | generated report input is stale: connector_sha differs; framework_sha differs |
| `reports/testing/runtime-validation-snapshot.json` | present | input file available |
