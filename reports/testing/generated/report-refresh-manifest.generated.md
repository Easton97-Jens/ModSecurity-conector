# Report Refresh Manifest

Generated file - do not edit manually.

- Generated at: `2026-06-14T19:39:52Z`
- Connector SHA: `1792360f4abf0bd19b145eb57a66ad77a620c0bf`
- Framework SHA: `b928e944a0f5928fb0ac1a7466292f92f1c88cfe`
- Framework submodule SHA: `b928e944a0f5928fb0ac1a7466292f92f1c88cfe`
- MRTS SHA: `13aa91291adea12d5c607fdd165d010fcfb1da78`

## Inputs
- `full_runtime_matrix`: `c2594bb3599a4219364300ba5121da0220f658815ad6c416cc3731c1a0c3fa84`
- `native_mrts`: `e76859e6673c48a4aea523f8c02561a61132518381b0701baca344adf5fe6513`
- `build_cache`: `047eb3758de4dcced26b3ddf0504f9d2580b171d8f3c9116a6afd1a42dbfb7e6`
- `component_cache`: `b08761c80e144f379d77396a40b6b0fdd23f58c6565754b51fad923eb196d3b2`

## Reports
| Report | Owner | Generator | Target | Status | Requires runtime | Requires native MRTS | Requires full matrix | Missing input |
|---|---|---|---|---|---|---|---|---|
| connector_coverage_reports | connector | framework:ci/generate-case-matrix.py | generate-test-matrix | generated | true | false | false | - |
| full_runtime_matrix | connector | ci/generate-full-runtime-matrix.py | generate-full-runtime-matrix | generated | true | false | true | - |
| connector_work_queue | connector | framework:ci/generate-connector-work-queue.py | generate-work-queue | generated | true | false | true | - |
| phase_work_queue | connector | framework:ci/generate-phase-work-queue.py | generate-phase-work-queue | generated | true | false | true | - |
| native_mrts_reports | connector | framework:ci/generate-mrts-native-report.py | mrts-native-full-run | skipped_missing_input | false | true | false | BUILD_ROOT:mrts-native/apache2_ubuntu/job.json, BUILD_ROOT:mrts-native/nginx-pr24/job.json |
| nolog_audit_evidence | connector | ci/generate-nolog-audit-evidence-analysis.py | generate-nolog-audit-evidence-analysis | generated | true | false | true | - |
| response_header_hook_analysis | connector | ci/generate-response-header-hook-analysis.py | generate-response-header-hook-analysis | generated | true | false | true | - |
| phase4_hard_abort_capability | connector | ci/generate-phase4-hard-abort-capability.py | generate-phase4-hard-abort-capability | generated | true | false | true | - |
| remaining_failure_analysis | connector | ci/generate-remaining-failure-analysis.py | generate-remaining-failure-analysis | generated | true | false | true | - |
| intervention_blocking_analysis | connector | ci/generate-intervention-blocking-analysis.py | generate-intervention-blocking-analysis | generated | true | false | true | - |
| no_mrts_intervention_nomatch_analysis | connector | ci/generate-no-mrts-intervention-nomatch-analysis.py | generate-no-mrts-intervention-nomatch-analysis | generated | true | false | true | - |
| body_processor_analysis | connector | ci/generate-body-processor-analysis.py | generate-body-processor-analysis | generated | true | false | true | - |
| rule_chain_semantics_analysis | connector | ci/generate-rule-chain-semantics-analysis.py | generate-rule-chain-semantics-analysis | generated | true | false | true | - |
| final_consistency_audit | connector | ci/generate-final-consistency-audit.py | generate-final-consistency-audit | generated | true | false | true | - |
| runtime_cache_reports | connector | ci/update-runtime-reports.py | prepare-runtime-components | generated | true | false | false | - |
