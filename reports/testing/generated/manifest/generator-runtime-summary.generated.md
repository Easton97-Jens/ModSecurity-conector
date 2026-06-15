> Generated file - do not edit manually.
>
> Generated at: `2026-06-15T10:40:38Z`
> Generator: `ci/refresh-connector-reports.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `informational`
> Connector SHA: `b94d4fd3cf130e7c4f28004033d647b2f2de3ad6`
> Framework SHA: `61454d23be52e52d9395e6b091c52d651e16f89b`
> Input status: `partial`

# Generator Runtime Summary

| Report | Generator | Target | Status | Return Code | Duration | Missing Inputs | Missing Outputs |
|---|---|---|---|---:|---:|---|---|
| `connector_coverage_reports` | `framework:ci/generate-case-matrix.py` | `generate-test-matrix` | generated | 0 | 3.989 | - | - |
| `full_runtime_matrix` | `ci/generate-full-runtime-matrix.py` | `generate-full-runtime-matrix` | generated | 0 | 0.599 | - | - |
| `connector_work_queue` | `framework:ci/generate-connector-work-queue.py` | `generate-work-queue` | generated | 0 | 4.364 | - | - |
| `phase_work_queue` | `framework:ci/generate-phase-work-queue.py` | `generate-phase-work-queue` | generated | 0 | 0.809 | - | - |
| `native_mrts_reports` | `framework:ci/generate-mrts-native-report.py` | `mrts-native-full-run` | generated | 0 | 1.137 | BUILD_ROOT:mrts-native/apache2_ubuntu/job.json, BUILD_ROOT:mrts-native/nginx-pr24/job.json | - |
| `nolog_audit_evidence` | `ci/generate-nolog-audit-evidence-analysis.py` | `generate-nolog-audit-evidence-analysis` | generated | 0 | 1.518 | - | - |
| `response_header_hook_analysis` | `ci/generate-response-header-hook-analysis.py` | `generate-response-header-hook-analysis` | generated | 0 | 3.982 | - | - |
| `phase4_hard_abort_capability` | `ci/generate-phase4-hard-abort-capability.py` | `generate-phase4-hard-abort-capability` | generated | 0 | 4.103 | - | - |
| `remaining_failure_analysis` | `ci/generate-remaining-failure-analysis.py` | `generate-remaining-failure-analysis` | generated | 0 | 16.672 | - | - |
| `intervention_blocking_analysis` | `ci/generate-intervention-blocking-analysis.py` | `generate-intervention-blocking-analysis` | generated | 0 | 5.664 | - | - |
| `no_mrts_intervention_nomatch_analysis` | `ci/generate-no-mrts-intervention-nomatch-analysis.py` | `generate-no-mrts-intervention-nomatch-analysis` | generated | 0 | 0.6 | - | - |
| `body_processor_analysis` | `ci/generate-body-processor-analysis.py` | `generate-body-processor-analysis` | generated | 0 | 6.277 | - | - |
| `rule_chain_semantics_analysis` | `ci/generate-rule-chain-semantics-analysis.py` | `generate-rule-chain-semantics-analysis` | generated | 0 | 0.686 | - | - |
| `final_consistency_audit` | `ci/generate-final-consistency-audit.py` | `generate-final-consistency-audit` | generated | 0 | 0.927 | - | - |
| `runtime_cache_reports` | `ci/update-runtime-reports.py` | `prepare-runtime-components` | skipped_missing_input | 0 | 0.004 | reports/testing/generated/cache/runtime-component-cache.generated.json, reports/testing/generated/cache/runtime-build-cache.generated.json | - |

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
