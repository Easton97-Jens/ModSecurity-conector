# ModSecurity Connector Repository Overview

**Language:** English | [Deutsch](repository-overview.de.md)

## Table of contents

1. [Repository purpose](#repository-purpose)
2. [Short summary for humans](#short-summary-for-humans)
3. [Short summary for AI systems](#short-summary-for-ai-systems)
4. [Architecture principle](#architecture-principle)
5. [Repository structure](#repository-structure)
6. [Common SDK: complete file index](#common-sdk-complete-file-index)
7. [Common SDK: modules and responsibilities](#common-sdk-modules-and-responsibilities)
8. [Config, Directives and Parser Model](#config-directives-and-parser-model)
9. [Allowed config/directive vocabulary](#allowed-configdirective-vocabulary)
10. [Request/response mapping](#requestresponse-mapping)
11. [Decision, intervention, status and event model](#decision-intervention-status-and-event-model)
12. [Resource limits, DoS guard, flow guard and integrity](#resource-limits-dos-guard-flow-guard-and-integrity)
13. [C Language and Standards](#c-language-and-standards)
14. [CI, contract and governance checks](#ci-contract-and-governance-checks)
15. [Makefile Targets: What can be done with `make`?](#makefile-targets-what-can-be-done-with-make)
16. [Common Makefile Commands](#common-makefile-commands)
17. [Exit Codes and BLOCKED/SKIPPED Behavior](#exit-codes-and-blockedskipped-behavior)
18. [Environment variables](#environment-variables)
19. [Connector model](#connector-model)
20. [Apache Connector](#apache-connector)
21. [NGINX Connector](#nginx-connector)
22. [HAProxy Connector](#haproxy-connector)
23. [Envoy Connector](#envoy-connector)
24. [Traefik Connector](#traefik-connector)
25. [lighttpd Connector](#lighttpd-connector)
26. [Connector status matrix](#connector-status-matrix)
27. [Test framework relation](#test-framework-relation)
28. [Runtime evidence and verification policy](#runtime-evidence-and-verification-policy)
29. [Implemented work](#implemented-work)
30. [Missing/future work](#missingfuture-work)
31. [Known limits](#known-limits)
32. [Intentionally connector-specific](#intentionally-connector-specific)
33. [AI fact block](#ai-fact-block)
34. [Allowed and forbidden claims](#allowed-and-forbidden-claims)
35. [Glossary](#glossary)
36. [Maintenance checklist](#maintenance-checklist)

## Repository purpose

This repository builds ModSecurity connectors and a shared Common SDK layer. The goal is to keep connector-neutral semantics in `common/` and host/server API integration in each connector.

Principle: everything that is semantic belongs in `common/`; everything that is host/server API remains in the connector.

Common examples: config, directives, directive specs, parser helpers, request and response models, header helpers, mapper contracts, decision/intervention/status/error models, event JSONL, resource limits, DoS guard, flow guard, integrity metadata, rule-loading contracts, test-result JSON, adapter metadata, capabilities and generic mapper helpers.

Connector-specific examples: Apache `request_rec`, `command_rec` and APR; NGINX `ngx_http_request_t`, `ngx_chain_t` and filters; HAProxy SPOE/SPOP, frame parsing and runtime loop; Envoy filter/runtime APIs; Traefik middleware/proxy/runtime APIs; and lighttpd plugin/proxy/runtime APIs.

## Short summary for humans

The repository is a connector monorepo. Apache, NGINX and HAProxy have active connector code and common-adoption checks. Envoy, Traefik and lighttpd have starter/structure-only/compile-only preparation and must be treated as `not_verified / connector-gap` until real runtime evidence exists. Compile, lint and contract checks are valuable but are not production, CRS, full-matrix, response-body or runtime verification claims.

## Short summary for AI systems

Use repository code, CI scripts and current reports as source of truth. Do not infer runtime guarantees from a file name, Makefile target or local smoke result. Distinguish connector metadata from per-run result JSON. Use `unknown`, `partial`, `structure-only`, `not_verified`, `connector-gap` or `requires runtime evidence` when evidence is missing.

## Architecture principle

`common/` defines connector-neutral C/C++ contracts and helpers. `connectors/<name>/` adapts server APIs into those contracts. Generated reports live under `reports/testing/generated/`; CI and governance scripts live in `ci/`; reusable tests are expected from `modules/ModSecurity-test-Framework`.

## Repository structure

| Path | Meaning | Evidence status |
|---|---|---|
| `common/include/msconnector/` | Public Common SDK headers. | Contract/static evidence only unless tested in a run. |
| `common/src/` | Common SDK helper implementations. | C17/common checks. |
| `connectors/apache/` | Apache adapter source, docs, harness and metadata. | Common adoption; runtime claims require current evidence. |
| `connectors/nginx/` | NGINX adapter source, docs, harness and metadata. | Common adoption; runtime claims require current evidence. |
| `connectors/haproxy/` | HAProxy/SPOA starter and mapping source, docs, harness and metadata. | Common adoption; runtime claims require current evidence. |
| `connectors/envoy/` | Envoy bridge starter. | `not_verified / connector-gap`. |
| `connectors/traefik/` | Traefik decision-service starter. | `not_verified / connector-gap`. |
| `connectors/lighttpd/` | lighttpd bridge/build starter. | `not_verified / connector-gap`. |
| `ci/` | Lint, contract, governance, C-standard and report scripts. | Check definitions, not runtime evidence by themselves. |
| `docs/` | Repository-level and architecture docs. | Documentation; must stay synchronized. |
| `reports/` | Generated reports/evidence/matrices. | Trust only current generated evidence and status labels. |

## Common SDK: complete file index

| File | Type | Purpose | Important APIs/structs | Used by | Status / notes |
|---|---|---|---|---|---|
| `common/include/msconnector/adapter.h` | header | adapter helper/model for the connector-neutral SDK | msconnector_adapter, msconnector_adapter_metadata, msconnector_capabilities, msconnector_config, msconnector_error, msconnector_transaction_view | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/adapter_contract.h` | header | adapter contract declarations | msconnector_adapter_contract_result, msconnector_adapter_contract_result_init, msconnector_adapter_contract_validate, msconnector_adapter | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/adapter_metadata.h` | header | adapter metadata shape | msconnector_adapter_metadata, msconnector_origin, msconnector_capabilities, msconnector_adapter_metadata_init, msconnector_adapter_metadata_is_complete | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/artifact_layout.h` | header | artifact layout helper/model for the connector-neutral SDK | msconnector_artifact_layout, msconnector_artifact_layout_init, msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/artifacts.h` | header | artifacts helper/model for the connector-neutral SDK | msconnector_artifact_paths, msconnector_artifact_paths_init, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/block_statuses.h` | header | block statuses helper/model for the connector-neutral SDK | msconnector_block_status_support, msconnector_block_status_is_allowed, msconnector_block_status_normalize, msconnector_http_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/blocking.h` | header | blocking helper/model for the connector-neutral SDK | msconnector_block_action, msconnector_blocking_policy, msconnector_block_action_name, msconnector_block_action_is_disruptive, msconnector_blocking_policy_make | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/body_policy.h` | header | body policy helper/model for the connector-neutral SDK | msconnector_body_mode, msconnector_body_policy, msconnector_body_policy_init, msconnector_body_mode_name, msconnector_body_mode_is_supported | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/build_contract.h` | header | build contract helper/model for the connector-neutral SDK | msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/capabilities.h` | header | capability declarations | msconnector_capability_flags, msconnector_capability_flag, msconnector_capabilities, msconnector_capabilities_has, msconnector_capability_name, msconnector_capability_from_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/capabilities.hpp` | header | capability declarations | msconnector_capability_flags, msconnector_capability_flag, msconnector_capabilities, msconnector_capability_name | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/capability_matrix.h` | header | capability matrix helper/model for the connector-neutral SDK | msconnector_capability_required_test, msconnector_capability_flag, msconnector_capability_has_required_test | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/config.h` | header | connector-neutral configuration object, defaults, merge and validation | msconnector_config, msconnector_bool_option, msconnector_phase4_mode, msconnector_config_init, msconnector_config_apply_defaults, msconnector_config_merge | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/config_parser.h` | header | shared parsers for booleans, phase4 mode, sizes, HTTP statuses and content-type tokens | msconnector_parse_bool, msconnector_bool_option, msconnector_parse_phase4_mode, msconnector_phase4_mode, msconnector_parse_size, msconnector_parse_http_status | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/connector_manifest.h` | header | connector manifest helper/model for the connector-neutral SDK | msconnector_connector_manifest, msconnector_capability_flags, msconnector_connector_manifest_init, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_connector_manifest_write_json | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/crs.h` | header | crs helper/model for the connector-neutral SDK | msconnector_crs_mode, msconnector_crs_config, msconnector_crs_config_init, msconnector_crs_config_validate, msconnector_crs_mode_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/decision.h` | header | inspection decision model | msconnector_event, msconnector_decision_kind, msconnector_decision, msconnector_status, msconnector_phase, msconnector_intervention | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/decision_action.h` | header | decision action helper/model for the connector-neutral SDK | msconnector_decision_action, msconnector_decision_action_name, msconnector_decision_action_from_decision, msconnector_decision, msconnector_decision_action_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/directive_adapter.h` | header | helpers that apply directive values to msconnector_config | msconnector_directive_scope, msconnector_directive_argument_policy, msconnector_directive_adapter_entry, msconnector_directive_spec, msconnector_directive_adapter_count, msconnector_directive_adapter_at | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/directive_spec.h` | header | global directive catalog with value types, defaults and allowed values | msconnector_directive_value_type, msconnector_directive_spec, msconnector_directive_specs, msconnector_directive_spec_count, msconnector_directive_spec_find | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/directives.h` | header | canonical directive name macros | file-local helpers / metadata | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/dos_guard.h` | header | DoS guard counters and checks | msconnector_dos_guard_check_request, msconnector_request, msconnector_resource_limits, msconnector_error, msconnector_dos_guard_check_response, msconnector_response | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/error.h` | header | error helper/model for the connector-neutral SDK | msconnector_error_code, msconnector_error, msconnector_error_init, msconnector_error_set, msconnector_error_code_name, msconnector_error_default_message | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/event.h` | header | event model | msconnector_event_meta, msconnector_event_decision, msconnector_phase, msconnector_status, msconnector_event_http, msconnector_event_request | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/event_jsonl.h` | header | JSONL serialization for events | msconnector_event_write_jsonl_line, msconnector_event | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/flow_guard.h` | header | request/response flow guard | msconnector_flow_guard, msconnector_phase, msconnector_flow_guard_init, msconnector_flow_guard_can_enter_phase, msconnector_flow_guard_mark_validated, msconnector_flow_guard_mark_immutable | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/generic_mapper.h` | header | generic request/response mapper helpers for starter connectors | msconnector_generic_request_source, msconnector_endpoint, msconnector_header, msconnector_bytes, msconnector_generic_response_source, msconnector_generic_config_init | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/headers.h` | header | connector-neutral header list helpers | msconnector_header_name_equals, msconnector_header, msconnector_header_name_is, msconnector_headers_find, msconnector_headers_find_first, msconnector_headers_find_last | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/http_status.h` | header | http status helper/model for the connector-neutral SDK | msconnector_http_status_class, msconnector_http_status_info, msconnector_http_status_info_find, msconnector_http_status_reason_phrase, msconnector_http_status_default_message, msconnector_http_status_classify | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/integrity_event.h` | header | integrity metadata events without cryptographic claims | msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/intervention.h` | header | intervention/blocking model | msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/intervention.hpp` | header | intervention/blocking model | msconnector_intervention | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/json_escape.h` | header | json escape helper/model for the connector-neutral SDK | msconnector_json_escape | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/late_intervention.h` | header | late intervention helper/model for the connector-neutral SDK | msconnector_late_intervention_action, msconnector_late_intervention_policy, msconnector_late_intervention_policy_init, msconnector_late_intervention_action_name, msconnector_late_intervention_resolve | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/lifecycle_status.h` | header | lifecycle status helper/model for the connector-neutral SDK | msconnector_build_status, msconnector_runtime_status, msconnector_verification_status, msconnector_build_status_name, msconnector_runtime_status_name, msconnector_verification_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/limits.h` | header | limits helper/model for the connector-neutral SDK | msconnector_limit_header_count, msconnector_limit_header_name_length, msconnector_limit_header_value_length, msconnector_limit_total_header_bytes, msconnector_limit_body_buffer_size, msconnector_limit_response_body_buffer_size | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/log_sanitize.h` | header | log sanitize helper/model for the connector-neutral SDK | msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/logging.h` | header | logging helper/model for the connector-neutral SDK | msconnector_log_level, msconnector_log_record, msconnector_log_callback, msconnector_logger, msconnector_log | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/logging.hpp` | header | logging helper/model for the connector-neutral SDK | msconnector_log_level, msconnector_log_record, msconnector_logger, msconnector_log | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/memory.h` | header | memory helper/model for the connector-neutral SDK | msconnector_alloc_checked, msconnector_free_checked, msconnector_alloc_callback, msconnector_free_callback, msconnector_allocator, msconnector_allocator_init | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/modsecurity_engine.h` | header | modsecurity engine helper/model for the connector-neutral SDK | msconnector_modsecurity_engine_ops, msconnector_error, msconnector_request, msconnector_decision, msconnector_response, msconnector_modsecurity_engine | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/options.h` | header | options helper/model for the connector-neutral SDK | msconnector_bool_option, msconnector_phase4_mode | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/origin.h` | header | origin/license metadata | msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/origin.hpp` | header | origin/license metadata | msconnector_origin, msconnector_origin_is_empty | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/origin_governance.h` | header | origin governance helper/model for the connector-neutral SDK | msconnector_origin_governance, msconnector_origin_governance_init, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/path_policy.h` | header | path policy helper/model for the connector-neutral SDK | msconnector_path_is_absolute, msconnector_path_is_empty, msconnector_path_has_parent_reference | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/phase.h` | header | phase helper/model for the connector-neutral SDK | msconnector_phase | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/redaction.h` | header | redaction helper/model for the connector-neutral SDK | msconnector_redacted_string, msconnector_redact_copy | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/request.h` | header | connector-neutral request model | msconnector_bytes, msconnector_header, msconnector_endpoint, msconnector_request | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/request.hpp` | header | connector-neutral request model | msconnector_bytes, msconnector_header, msconnector_endpoint, msconnector_request, msconnector_request_init, msconnector_request_validate | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/request_helpers.h` | header | request helpers helper/model for the connector-neutral SDK | msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_resource_limits, msconnector_request_has_header | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/request_mapper_contract.h` | header | request mapper contract validation | msconnector_mapper_requirement, msconnector_request_mapper_contract, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract_validate, msconnector_request_mapper_validate_output, msconnector_request | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/resource_limits.h` | header | resource limit model | msconnector_resource_limits, msconnector_resource_limits_init, msconnector_resource_limits_validate, msconnector_resource_limits_headers_ok, msconnector_header, msconnector_resource_limits_body_ok | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/response.h` | header | connector-neutral response model | msconnector_response, msconnector_header, msconnector_bytes | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/response.hpp` | header | connector-neutral response model | msconnector_response, msconnector_response_init, msconnector_response_validate | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/response_helpers.h` | header | response helpers helper/model for the connector-neutral SDK | msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_response_validate_with_limits, msconnector_resource_limits, msconnector_response_has_header | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/response_mapper_contract.h` | header | response mapper contract validation | msconnector_response_mapper_contract, msconnector_mapper_requirement, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output, msconnector_response | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_error.h` | header | rule error helper/model for the connector-neutral SDK | msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_rule_error_set_load_failed, msconnector_rule_error_clear | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_event.h` | header | rule event helper/model for the connector-neutral SDK | msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_rule_load_event, msconnector_rule_error_event, msconnector_error | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_id.h` | header | rule id helper/model for the connector-neutral SDK | msconnector_rule_id_copy, msconnector_rule_id_extract_from_message, msconnector_rule_id_validate | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_load_stats.h` | header | rule load stats helper/model for the connector-neutral SDK | msconnector_rule_load_stats, msconnector_rule_load_stats_init, msconnector_rule_load_stats_add, msconnector_rule_load_stats_add_inline, msconnector_rule_load_stats_add_file, msconnector_rule_load_stats_add_remote | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_loader.h` | header | rule loading contracts | msconnector_rule_loader_backend, msconnector_error, msconnector_rule_loader, msconnector_rule_load_stats, msconnector_rule_loader_init, msconnector_rule_loader_add_inline | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_merge.h` | header | rule merge helper/model for the connector-neutral SDK | msconnector_rule_collection, msconnector_rule_collection_init, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/runtime_paths.h` | header | runtime paths helper/model for the connector-neutral SDK | msconnector_runtime_path_join | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/runtime_report.h` | header | runtime report helper/model for the connector-neutral SDK | msconnector_runtime_report, msconnector_status, msconnector_runtime_report_init, msconnector_runtime_report_write_json | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/status.h` | header | status classification helpers | msconnector_status, msconnector_status_name, msconnector_status_from_result | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/status.hpp` | header | status classification helpers | msconnector_status, msconnector_status_name | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/test_result.h` | header | test result helper/model for the connector-neutral SDK | msconnector_test_result, msconnector_status, msconnector_test_result_init, msconnector_test_result_passed | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/test_result_json.h` | header | test result JSON writer | msconnector_test_result_write_json, msconnector_test_result | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/transaction.h` | header | transaction helper/model for the connector-neutral SDK | msconnector_transaction_view, msconnector_request, msconnector_response, msconnector_intervention | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/transaction.hpp` | header | transaction helper/model for the connector-neutral SDK | msconnector_transaction_view, msconnector_transaction_state, msconnector_decision, msconnector_phase, msconnector_phase_name | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/transaction_id.h` | header | transaction id helper/model for the connector-neutral SDK | msconnector_transaction_id_source, msconnector_transaction_id_expr_eval, msconnector_request, msconnector_transaction_id_context, msconnector_config, msconnector_transaction_id_result | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/transaction_state.h` | header | transaction state helper/model for the connector-neutral SDK | msconnector_transaction_state, msconnector_transaction_state_init, msconnector_transaction_state_mark_phase, msconnector_phase, msconnector_transaction_state_phase_processed, msconnector_phase_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/README.md` | doc | README helper/model for the connector-neutral SDK | file-local helpers / metadata | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/adapter.c` | source | adapter helper/model for the connector-neutral SDK | msconnector_adapter_init, msconnector_adapter, msconnector_adapter_has_metadata, msconnector_adapter_has_capabilities, msconnector_adapter_supports_phase, msconnector_phase | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/adapter_contract.c` | source | adapter contract declarations | msconnector_adapter_contract_result, msconnector_capabilities, msconnector_capability_flag, msconnector_capability_flags, msconnector_adapter, msconnector_adapter_contract_result_init | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/adapter_metadata.c` | source | adapter metadata shape | msconnector_adapter_metadata_init, msconnector_adapter_metadata, msconnector_adapter_metadata_is_complete | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/artifact_layout.c` | source | artifact layout helper/model for the connector-neutral SDK | msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log, msconnector_artifact_name_runtime_stdout_log, msconnector_artifact_name_runtime_stderr_log | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/artifacts.c` | source | artifacts helper/model for the connector-neutral SDK | msconnector_artifact_paths_init, msconnector_artifact_paths, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/block_statuses.c` | source | block statuses helper/model for the connector-neutral SDK | msconnector_block_status_is_allowed, msconnector_http_status_is_block_response, msconnector_block_status_normalize, msconnector_http_status_is_valid, msconnector_http_status_name, msconnector_http_status_info_find | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/blocking.c` | source | blocking helper/model for the connector-neutral SDK | msconnector_block_action_name, msconnector_block_action, msconnector_block_action_is_disruptive, msconnector_blocking_policy, msconnector_blocking_policy_make, msconnector_block_status_normalize | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/body_policy.c` | source | body policy helper/model for the connector-neutral SDK | msconnector_body_policy_init, msconnector_body_policy, msconnector_body_mode_name, msconnector_body_mode, msconnector_body_mode_is_supported | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/build_contract.c` | source | build contract helper/model for the connector-neutral SDK | msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/capabilities.c` | source | capability declarations | msconnector_capability_flag, msconnector_capability_name, msconnector_capability_from_name, msconnector_capability_flags, msconnector_capabilities_add | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/capability_matrix.c` | source | capability matrix helper/model for the connector-neutral SDK | msconnector_capability_required_test, msconnector_capability_flag, msconnector_capability_has_required_test | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/config.c` | source | connector-neutral configuration object, defaults, merge and validation | msconnector_bool_option, msconnector_phase4_mode, msconnector_config, msconnector_block_status_is_allowed, msconnector_http_status_is_valid, msconnector_http_status_is_error | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/config_parser.c` | source | shared parsers for booleans, phase4 mode, sizes, HTTP statuses and content-type tokens | msconnector_parse_bool, msconnector_bool_option, msconnector_parse_phase4_mode, msconnector_phase4_mode, msconnector_parse_size, msconnector_parse_http_status | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/connector_manifest.c` | source | connector manifest helper/model for the connector-neutral SDK | msconnector_json_escape, msconnector_connector_manifest_init, msconnector_connector_manifest, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_adapter_metadata_is_complete | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/crs.c` | source | crs helper/model for the connector-neutral SDK | msconnector_crs_config_init, msconnector_crs_config, msconnector_crs_mode_name, msconnector_crs_mode, msconnector_crs_config_validate | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/decision.c` | source | inspection decision model | msconnector_decision_kind, msconnector_decision_init, msconnector_decision, msconnector_intervention_none, msconnector_decision_kind_name, msconnector_decision_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/decision_action.c` | source | decision action helper/model for the connector-neutral SDK | msconnector_decision_action_name, msconnector_decision_action, msconnector_decision_action_from_decision, msconnector_decision, msconnector_decision_action_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/directive_adapter.c` | source | helpers that apply directive values to msconnector_config | msconnector_directive_adapter_entry, msconnector_directive_adapter_count, msconnector_directive_adapter_at, msconnector_directive_spec_find, msconnector_directive_adapter_find, msconnector_directive_adapter_validate_entry | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/directive_spec.c` | source | global directive catalog with value types, defaults and allowed values | msconnector_directive_spec, msconnector_directive_specs, msconnector_directive_spec_count, msconnector_directive_spec_find | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/dos_guard.c` | source | DoS guard counters and checks | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_dos_guard_check_request, msconnector_request, msconnector_resource_limits | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/error.c` | source | error helper/model for the connector-neutral SDK | msconnector_error_init, msconnector_error, msconnector_error_set, msconnector_error_code, msconnector_error_code_name, msconnector_error_default_message | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/event.c` | source | event model | msconnector_event_json_text_index, msconnector_event_json_status_index, msconnector_event_json_flag_index, msconnector_event_json_parts | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/event_jsonl.c` | source | JSONL serialization for events | msconnector_event_write_jsonl_line, msconnector_event, msconnector_event_write_json_ex | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/flow_guard.c` | source | request/response flow guard | msconnector_phase, msconnector_flow_guard_init, msconnector_flow_guard, msconnector_flow_guard_can_enter_phase, msconnector_flow_guard_mark_validated, msconnector_flow_guard_mark_immutable | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/generic_mapper.c` | source | generic request/response mapper helpers for starter connectors | msconnector_generic_config_init, msconnector_config, msconnector_config_init, msconnector_generic_map_request, msconnector_generic_request_source, msconnector_request_mapper_contract | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/headers.c` | source | connector-neutral header list helpers | msconnector_header_name_is, msconnector_header_name_equals, msconnector_header, msconnector_headers_find_first, msconnector_headers_find, msconnector_headers_find_last | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/http_status.c` | source | http status helper/model for the connector-neutral SDK | msconnector_http_status_info, msconnector_http_status_is_valid, msconnector_http_status_class, msconnector_http_status_classify, msconnector_http_status_info_find, msconnector_http_status_reason_phrase | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/integrity_event.c` | source | integrity metadata events without cryptographic claims | msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/intervention.c` | source | intervention/blocking model | msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/json_escape.c` | source | json escape helper/model for the connector-neutral SDK | msconnector_json_escape | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/late_intervention.c` | source | late intervention helper/model for the connector-neutral SDK | msconnector_late_intervention_policy_init, msconnector_late_intervention_policy, msconnector_late_intervention_action_name, msconnector_late_intervention_action, msconnector_late_intervention_resolve | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/lifecycle_status.c` | source | lifecycle status helper/model for the connector-neutral SDK | msconnector_build_status_name, msconnector_build_status, msconnector_runtime_status_name, msconnector_runtime_status, msconnector_verification_status_name, msconnector_verification_status | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/limits.c` | source | limits helper/model for the connector-neutral SDK | msconnector_limit_header_count, msconnector_limit_header_name_length, msconnector_limit_header_value_length, msconnector_limit_total_header_bytes, msconnector_limit_body_buffer_size, msconnector_limit_response_body_buffer_size | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/log_sanitize.c` | source | log sanitize helper/model for the connector-neutral SDK | msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/memory.c` | source | memory helper/model for the connector-neutral SDK | msconnector_allocator_init, msconnector_allocator, msconnector_alloc_checked, msconnector_free_checked, msconnector_allocator_within_limit | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/modsecurity_engine.c` | source | modsecurity engine helper/model for the connector-neutral SDK | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_modsecurity_transaction, msconnector_modsecurity_engine_init, msconnector_modsecurity_engine | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/origin.c` | source | origin/license metadata | msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/origin_governance.c` | source | origin governance helper/model for the connector-neutral SDK | msconnector_origin_governance_init, msconnector_origin_governance, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/path_policy.c` | source | path policy helper/model for the connector-neutral SDK | msconnector_path_is_empty, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/redaction.c` | source | redaction helper/model for the connector-neutral SDK | msconnector_redacted_string, msconnector_redact_copy | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/request_helpers.c` | source | request helpers helper/model for the connector-neutral SDK | msconnector_header, msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_resource_limits | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/request_mapper_contract.c` | source | request mapper contract validation | msconnector_mapper_requirement, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract, msconnector_request_mapper_contract_validate, msconnector_request_mapper_validate_output, msconnector_request | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/resource_limits.c` | source | resource limit model | msconnector_resource_limits_init, msconnector_resource_limits, msconnector_resource_limits_validate, msconnector_resource_limits_headers_ok, msconnector_header, msconnector_resource_limits_body_ok | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/response_helpers.c` | source | response helpers helper/model for the connector-neutral SDK | msconnector_header, msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_http_status_is_valid, msconnector_response_validate_with_limits | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/response_mapper_contract.c` | source | response mapper contract validation | msconnector_mapper_requirement, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output, msconnector_response | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_error.c` | source | rule error helper/model for the connector-neutral SDK | msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_error_set, msconnector_error_default_message, msconnector_rule_error_set_load_failed, msconnector_rule_error_clear | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_event.c` | source | rule event helper/model for the connector-neutral SDK | msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_event_init, msconnector_rule_load_event, msconnector_rule_error_event | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_id.c` | source | rule id helper/model for the connector-neutral SDK | msconnector_rule_id_validate, msconnector_rule_id_copy, msconnector_rule_id_extract_from_message | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_loader.c` | source | rule loading contracts | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_rule_loader_init, msconnector_rule_loader, msconnector_rule_loader_backend | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_merge.c` | source | rule merge helper/model for the connector-neutral SDK | msconnector_rule_collection_init, msconnector_rule_collection, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/runtime_paths.c` | source | runtime paths helper/model for the connector-neutral SDK | msconnector_runtime_path_join, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/runtime_report.c` | source | runtime report helper/model for the connector-neutral SDK | msconnector_json_escape, msconnector_runtime_report_init, msconnector_runtime_report, msconnector_runtime_report_write_json, msconnector_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/status.c` | source | status classification helpers | msconnector_status_name, msconnector_status, msconnector_status_from_result | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/test_result.c` | source | test result helper/model for the connector-neutral SDK | msconnector_test_result_init, msconnector_test_result, msconnector_test_result_passed | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/test_result_json.c` | source | test result JSON writer | msconnector_json_escape, msconnector_test_result_write_json, msconnector_test_result, msconnector_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/transaction.c` | source | transaction helper/model for the connector-neutral SDK | msconnector_decision_kind, msconnector_status, msconnector_decision, msconnector_intervention_none, msconnector_decision_make, msconnector_intervention | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/transaction_id.c` | source | transaction id helper/model for the connector-neutral SDK | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_transaction_id_result, msconnector_transaction_id_validate, msconnector_transaction_id_copy | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/transaction_state.c` | source | transaction state helper/model for the connector-neutral SDK | msconnector_transaction_state_init, msconnector_transaction_state, msconnector_transaction_state_mark_phase, msconnector_phase, msconnector_transaction_state_phase_processed, msconnector_phase_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |

## Common SDK: modules and responsibilities

- Configuration/directives/parser: owns neutral vocabulary, defaults, merge and validation. It is neutral because it stores values without Apache/NGINX/HAProxy/Envoy/Traefik/lighttpd types. It does not claim host syntax parity unless a connector implements it.
- Request/response/header/mapper contracts: define neutral HTTP shapes and validation. They do not prove body processing in a live server.
- Decision/intervention/status/error/event JSONL: define shared semantics and serialization. They are not tamper-proof or cryptographic evidence.
- Resource limits/body policy/DoS guard/flow guard/integrity metadata: define guardrails and metadata. They do not claim runtime secure behavior.
- Rule loading, merge and CRS helpers: define contracts and metadata. They do not prove CRS execution or full matrix coverage.
- Adapter metadata/capabilities/origin/manifests: identify source, status and capabilities. Metadata status must not be overridden by a successful per-run starter smoke.

## Config, Directives and Parser Model

`msconnector_config` stores neutral options: enable, error-log use, inline/file/remote rules, static or expression transaction ID, phase-4 response-body mode, content-type file, log path, body limit and default statuses.

`msconnector_config_init` sets fields to unset/zero/null. `msconnector_config_apply_defaults` fills unset values only. `msconnector_config_merge` merges parent and child values and then applies defaults; defaults must not be applied too early because doing so would incorrectly override parent/child inheritance. `msconnector_config_validate` checks enum ranges, complete remote-rule pairs, mutual exclusion of `transaction_id` and `transaction_id_expr`, and allowed status values.

Parser helpers use `1 = success` and `0 = failure`: `msconnector_parse_bool`, `msconnector_parse_phase4_mode`, `msconnector_parse_size`, `msconnector_parse_http_status` and `msconnector_validate_content_type_token`. Boolean parsing accepts on/off-style values; phase4 mode accepts `minimal`, `safe`, `strict`; size parsing accepts positive decimal byte sizes; HTTP status parsing requires a valid HTTP status; content-type token validation requires one slash, non-empty type/subtype and rejects control characters and semicolons. Transaction-ID validation is represented by `transaction_id` helpers and connector-specific expression parsing remains connector-specific.

## Allowed config/directive vocabulary

| Config / Directive | Common macro | Type | Allowed values | Default | Parser / validator | Supported connectors | Notes |
|---|---|---|---|---|---|---|---|
| `modsecurity` | `MSCONNECTOR_DIRECTIVE_MODSECURITY` | bool | `on|off` in spec; bool parser also accepts `true|false|1|0|yes|no` | `off` | `msconnector_parse_bool`, config validation | Apache/NGINX/HAProxy where adopted; Envoy/Traefik/lighttpd structure-only | Enables connector processing; no production claim. |
| `modsecurity_rules` | `MSCONNECTOR_DIRECTIVE_RULES` | string | inline rules text | none | directive adapter / config validation | connector-dependent | Rule text presence does not prove CRS/runtime execution. |
| `modsecurity_rules_file` | `MSCONNECTOR_DIRECTIVE_RULES_FILE` | path | connector/runtime path | none | directive adapter / path policy where used | connector-dependent | Path validity is environment-specific. |
| `modsecurity_rules_remote` | `MSCONNECTOR_DIRECTIVE_RULES_REMOTE` | string pair | `key url` | none | config requires key and URL together | connector-dependent | Incomplete pair is invalid. |
| `modsecurity_transaction_id` | `MSCONNECTOR_DIRECTIVE_TRANSACTION_ID` | string | static ID | none | transaction-id helpers / config mutual exclusion | connector-dependent | Mutually exclusive with expression. |
| `modsecurity_transaction_id_expr` | `MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR` | string | connector-parsed expression | none | connector-specific expression parser plus config mutual exclusion | Apache/NGINX behavior may differ; Envoy/Traefik/lighttpd connector-gap | Do not treat Apache expression syntax as NGINX syntax. |
| `modsecurity_use_error_log` | `MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG` | bool | `on|off` in spec; bool parser also accepts aliases | `on` | `msconnector_parse_bool` | connector-dependent | Controls common config flag only. |
| `modsecurity_phase4_mode` | `MSCONNECTOR_DIRECTIVE_PHASE4_MODE` | enum | `minimal|safe|strict` | `safe` | `msconnector_parse_phase4_mode` | connector-dependent; starter connectors not_verified | Response-body mode model; no RESPONSE_BODY verification by itself. |
| `modsecurity_phase4_content_types_file` | `MSCONNECTOR_DIRECTIVE_PHASE4_CONTENT_TYPES_FILE` | path | file of valid content-type tokens | none | content-type token parser; connector-specific strictness possible | connector-dependent | Exact matching/strictness depends on connector implementation and evidence. |
| `modsecurity_phase4_log` | `MSCONNECTOR_DIRECTIVE_PHASE4_LOG` | path | log path | none | directive adapter / path policy where used | connector-dependent | Log path does not imply verified body handling. |
| `modsecurity_phase4_body_limit` | `MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT` | size | positive decimal bytes | `1048576` | `msconnector_parse_size` | connector-dependent | Body truncation metadata requires connector implementation/evidence. |
| `default_block_status` | config field | HTTP status | allowed block statuses | `403` | `msconnector_block_status_is_allowed` | common config consumers | Field, not listed in `directives.h`. |
| `default_error_status` | config field | HTTP error status | valid HTTP error status | `500` | `msconnector_http_status_is_valid` and error check | common config consumers | Field, not listed in `directives.h`. |
| `unsupported_status` | config field | HTTP error status | valid HTTP error status | `501` | HTTP status validation | common config consumers | Field, not listed in `directives.h`. |
| CRS setup/path/fixture modes | reports/framework metadata | string/path/mode | current framework-specific values | unknown | framework scripts | framework-dependent | Document as `requires runtime evidence` unless current report proves it. |

## Request/response mapping

Request mapping owns neutral method, URI, protocol, headers, body metadata and transaction identifiers. Response mapping owns status, headers, content-type/body metadata and phase-4 policy data. Mapper contracts validate ownership, required fields and cleanup expectations. Host server objects remain outside `common/`.

## Decision, intervention, status and event model

Common decision/action helpers express allow/block/error/unsupported-like outcomes. Intervention helpers normalize block handling; status helpers map to HTTP statuses; event and JSONL helpers serialize structured evidence for a run. These outputs are per-run artifacts and not append-only or cryptographically signed unless such evidence is explicitly implemented later.

## Resource limits, DoS guard, flow guard and integrity

Resource limits centralize maximum sizes/counts. DoS guard and flow guard detect policy violations in neutral state. Integrity events carry metadata. This is governance and safety modeling, not a claim that runtime traffic is secure, tamper-proof or cryptographically protected.

## C Language and Standards

The Common SDK is designed for C17. C17 is the required profile when the compiler and required host/libmodsecurity headers are present. C23 is optional. future-C (`c2y`/`gnu2y`) is optional. `c20` and `c26` are not C standard modes and should be reported as SKIPPED/INFO if targets exist. Exit 77 means BLOCKED/SKIPPED due to missing environment, missing headers, missing compiler or unsupported optional profile. Real compile failures must not be hidden as 77.

| Connector | C17 | C23 | future-C | Header requirements | Exit-77 behavior |
|---|---|---|---|---|---|
| Common | required when compiler exists | optional | optional | common headers | only missing/unsupported environment should skip |
| Apache | hard when APXS/APR/libmodsecurity headers exist | optional | optional | APXS, APR, libmodsecurity | missing headers may block; compile errors must fail |
| NGINX | hard when NGINX/libmodsecurity headers exist | optional | optional | NGINX source/include roots, libmodsecurity | missing source/header roots may block |
| HAProxy | hard when HAProxy/libmodsecurity context exists | optional | optional | HAProxy/SPOE/SPOP and common includes | missing headers may block |
| Envoy | compile/structure-level only | optional | optional | starter/common headers; no native Envoy SDK claim | not_verified connector-gap remains |
| Traefik | compile/structure-level only | optional | optional | starter/common headers | not_verified connector-gap remains |
| lighttpd | compile/structure-level only | optional | optional | starter/common headers | not_verified connector-gap remains |

## CI, contract and governance checks

| Check / Target | Script | Purpose | Scope | Hard or optional | Exit-77 possible? |
|---|---|---|---|---|---|
| `check-common-helpers` | `ci/check_common_helpers.py` | Common helper compile/static checks | common | hard when env exists | possible for env blockers |
| `check-common-sdk-contract` | `ci/check_common_sdk_contract.py` | Common SDK API/contract governance | common | hard | usually no |
| `check-common-security-contract` | `ci/check_common_security_contract.py` | Security/data contract governance | common | hard | script-specific |
| `check-common-memory-safety` | `ci/check_common_memory_safety.py` | Memory ownership/safety contract checks | common | hard | script-specific |
| `check-common-flow-integrity` | `ci/check_common_flow_integrity.py` | Flow/integrity contract checks | common | hard | script-specific |
| `check-adapter-contracts` | `ci/check_adapter_contracts.py` | Adapter metadata/contract checks | connectors | hard | script-specific |
| `check-directive-parity` | `ci/check_directive_parity.py` | Common directive parity across connectors | common/connectors | hard | script-specific |
| connector common-adoption checks | `ci/check_*_common_adoption.py` | adoption/static governance | connector | hard | script-specific |
| connector C17/C23/future-C checks | `ci/check_*_c_standard*.py` | compile standard profiles | connector | C17 hard, others optional | yes for missing env/optional profile |
| `check-bilingual-docs` | `ci/check_bilingual_docs.py` | English/German doc pairing | docs/connectors | hard for docs | no/usage-specific |
| `lint`, `quick-check`, `codex-check` | Makefile composites | aggregate lint/check workflows | repo | hard aggregate | framework blockers possible |
| framework/report targets | framework scripts | runtime matrix/report governance | reports/framework | optional or composite | yes when submodule/env missing |

## Makefile Targets: What can be done with `make`?

The Makefile is the operational index for setup, linting, common SDK checks, connector checks, C-standard profiles, runtime/starter smoke runs, matrix/report generation, framework integration and cleanup/bootstrap workflows. Important rule: a Makefile target can prove only what its script actually checks. Compile-only and structure-only targets do not create runtime evidence.

### Target categories

1. General targets: `lint`, `quick-check`, `codex-check`, `setup-dev`, `install-dev-deps`, `doctor`, `doctor-quick`, `cloud-quick-check`, `quick-all`, `clean`-like/bootstrap targets where present.
2. Common SDK targets: `check-common-helpers`, C17/C23/future-C variants, SDK/security/memory/flow contracts, adapter contracts and directive parity.
3. Apache targets: common adoption, C-standard wiring, C17/C23/future-C and smoke/test targets. `check-apache-c17` is hard when APXS/APR/libmodsecurity headers exist; `check-apache-c17-lint` may translate environment skips in lint context.
4. NGINX targets: common adoption, C-standard wiring, C17/C23/future-C and smoke/test targets. NGINX source/include variables may be required.
5. HAProxy targets: common adoption, C-standard wiring, C17/C23/future-C and HAProxy smoke/test targets. HAProxy/SPOE/SPOP remains connector-specific.
6. Remaining connector targets: Envoy, Traefik and lighttpd adoption/C-standard/starter smoke targets. These remain `not_verified / connector-gap` and compile/structure-level only.
7. Framework/test-framework targets: `check-framework`, runtime matrix, verified report and MRTS targets; these can block if `modules/ModSecurity-test-Framework/...` is missing.
8. Report/generator targets: generate/check matrix and report artifacts. Reports require valid inputs and do not automatically imply verified claims.

### Complete Makefile target table

| Makefile target | Purpose | Scope | Requirements | Hard/optional | Exit-77/BLOCKED possible? | Notes |
|---|---|---|---|---|---|---|
| `check-framework` | Run the `check-framework` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-framework-fixture-syntax` | Run the `check-framework-fixture-syntax` workflow. | framework/reports | check-framework | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework |
| `prepare-runtime-components` | Run the `prepare-runtime-components` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-envoy-runtime` | Run the `prepare-envoy-runtime` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-traefik-runtime` | Run the `prepare-traefik-runtime` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-lighttpd-runtime` | Run the `prepare-lighttpd-runtime` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-lighttpd-runtime-build` | Run the `prepare-lighttpd-runtime-build` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-open-connector-runtimes` | Run the `prepare-open-connector-runtimes` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `runtime-components-inventory` | Run the `runtime-components-inventory` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `runtime-components-sources` | Run the `runtime-components-sources` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-runtime-producer-readiness` | Run the `check-runtime-producer-readiness` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-runtime-path-policy` | Run the `check-runtime-path-policy` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-bilingual-docs` | Run the `check-bilingual-docs` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `refresh-connector-reports` | Run the `refresh-connector-reports` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `refresh-all-reports` | Run the `refresh-all-reports` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-generated-report-layout` | Run the `check-generated-report-layout` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `report-governance` | Run the `report-governance` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-evidence-gate` | Run the `verified-report-evidence-gate` workflow. | framework/reports | check-generated-report-layout | optional/composite | usually no; script-specific | depends on check-generated-report-layout |
| `generate-system-environment-proof` | Run the `generate-system-environment-proof` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-verified-runtime-mismatch-analysis` | Run the `generate-verified-runtime-mismatch-analysis` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-remaining-critical-batch-analysis` | Run the `generate-remaining-critical-batch-analysis` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-native-semantics-comparison` | Run the `generate-native-semantics-comparison` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prove-generated-reports` | Run the `prove-generated-reports` workflow. | framework/reports | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `verified-runtime-producers` | Run the `verified-runtime-producers` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-producers` | Run the `verified-report-producers` workflow. | framework/reports | verified-runtime-producers | optional/composite | usually no; script-specific | depends on verified-runtime-producers |
| `verified-report-refresh` | Run the `verified-report-refresh` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-consumers` | Run the `verified-report-consumers` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-checks` | Run the `verified-report-checks` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-run` | Run the `verified-report-run` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-run-soft` | Run the `verified-report-run-soft` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-run-smoke` | Run the `verified-report-run-smoke` workflow. | framework/reports | check-framework | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework |
| `verified-full-matrix-job` | Run the `verified-full-matrix-job` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-case` | Run the `verified-case` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-native-case` | Run the `verified-native-case` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-nginx-case` | Run the `verified-nginx-case` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-apache-case` | Run the `verified-apache-case` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-haproxy-case` | Run the `verified-haproxy-case` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-full-matrix-resume` | Run the `verified-full-matrix-resume` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `smoke-common` | Run the `smoke-common` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-apache` | Run the `smoke-apache` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-nginx` | Run the `smoke-nginx` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-envoy` | Run the `smoke-envoy` workflow. | framework/reports | check-framework | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework |
| `smoke-envoy-modsecurity` | Run the `smoke-envoy-modsecurity` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-envoy-request-body` | Run the `smoke-envoy-request-body` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-envoy-crs` | Run the `smoke-envoy-crs` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-envoy-crs-secondary` | Run the `smoke-envoy-crs-secondary` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-haproxy` | Run the `smoke-haproxy` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-lighttpd` | Run the `smoke-lighttpd` workflow. | framework/reports | check-framework | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework |
| `smoke-lighttpd-modsecurity` | Run the `smoke-lighttpd-modsecurity` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-lighttpd-request-body` | Run the `smoke-lighttpd-request-body` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-lighttpd-crs` | Run the `smoke-lighttpd-crs` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-lighttpd-crs-secondary` | Run the `smoke-lighttpd-crs-secondary` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik` | Run the `smoke-traefik` workflow. | framework/reports | check-framework | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework |
| `smoke-traefik-modsecurity` | Run the `smoke-traefik-modsecurity` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik-request-body` | Run the `smoke-traefik-request-body` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik-crs` | Run the `smoke-traefik-crs` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik-crs-secondary` | Run the `smoke-traefik-crs-secondary` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-open-connectors-crs` | Run the `smoke-open-connectors-crs` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-open-connectors-request-body` | Run the `smoke-open-connectors-request-body` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-open-connectors-crs-secondary` | Run the `smoke-open-connectors-crs-secondary` workflow. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `smoke-new-connectors` | Run the `smoke-new-connectors` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-all` | Run the `smoke-all` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test` | Run the `test` workflow. | framework/reports | test-no-crs test-with-crs | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on test-no-crs test-with-crs |
| `test-no-crs` | Run the `test-no-crs` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-with-crs` | Run the `test-with-crs` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `mrts-generate` | Run the `mrts-generate` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `mrts-load` | Run the `mrts-load` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `mrts-import` | Run the `mrts-import` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `test-no-mrts` | Run the `test-no-mrts` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-with-mrts` | Run the `test-with-mrts` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-with-mrts-feature-demo` | Run the `test-with-mrts-feature-demo` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-mrts-matrix` | Run the `test-mrts-matrix` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `mrts-ftw` | Run the `mrts-ftw` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix` | Run the `runtime-matrix` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix-all` | Run the `runtime-matrix-all` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix-all-runtime` | Run the `runtime-matrix-all-runtime` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix-haproxy` | Run the `runtime-matrix-haproxy` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-mrts-runtime-matrix` | Run the `full-mrts-runtime-matrix` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-only-full-run` | Run the `mrts-only-full-run` workflow. | framework/reports | full-mrts-runtime-matrix | optional/composite | usually no; script-specific | depends on full-mrts-runtime-matrix |
| `full-runtime-matrix` | Run the `full-runtime-matrix` workflow. | framework/reports | full-matrix-parallel | optional/composite | usually no; script-specific | depends on full-matrix-parallel |
| `full-matrix-parallel` | Run the `full-matrix-parallel` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-matrix-parallel-runtime` | Run the `full-matrix-parallel-runtime` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-matrix-single-job-runtime` | Run the `full-matrix-single-job-runtime` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-matrix-resume-runtime` | Run the `full-matrix-resume-runtime` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `generate-full-runtime-matrix` | Run the `generate-full-runtime-matrix` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-full-matrix-job-completeness` | Run the `generate-full-matrix-job-completeness` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-nginx-mrts-http500-cluster-analysis` | Run the `generate-nginx-mrts-http500-cluster-analysis` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-work-queue` | Run the `generate-work-queue` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-phase-work-queue` | Run the `generate-phase-work-queue` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-nolog-audit-evidence-analysis` | Run the `generate-nolog-audit-evidence-analysis` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-response-header-hook-analysis` | Run the `generate-response-header-hook-analysis` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-phase4-hard-abort-capability` | Run the `generate-phase4-hard-abort-capability` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-intervention-blocking-analysis` | Run the `generate-intervention-blocking-analysis` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-no-mrts-intervention-nomatch-analysis` | Run the `generate-no-mrts-intervention-nomatch-analysis` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-body-processor-analysis` | Run the `generate-body-processor-analysis` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-rule-chain-semantics-analysis` | Run the `generate-rule-chain-semantics-analysis` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-final-consistency-audit` | Run the `generate-final-consistency-audit` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-remaining-failure-analysis` | Run the `generate-remaining-failure-analysis` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `mrts-native-full-run` | Run the `mrts-native-full-run` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-native-full-run-runtime` | Run the `mrts-native-full-run-runtime` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-native-apache-full` | Run the `mrts-native-apache-full` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-native-nginx-pr24-full` | Run the `mrts-native-nginx-pr24-full` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-upstream-infra-check` | Run the `mrts-upstream-infra-check` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `test-haproxy-no-crs` | Run the `test-haproxy-no-crs` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-haproxy-with-crs` | Run the `test-haproxy-with-crs` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `probe-response-body` | Run the `probe-response-body` workflow. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `connector-starter-checks` | Run the `connector-starter-checks` workflow. | repo | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `check-remaining-connectors-common-adoption` | Run the `check-remaining-connectors-common-adoption` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c-standard-wiring` | Run the `check-remaining-connectors-c-standard-wiring` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c-standards` | Run the `check-remaining-connectors-c-standards` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c17` | Run the `check-remaining-connectors-c17` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c17-lint` | Run the `check-remaining-connectors-c17-lint` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c23` | Run the `check-remaining-connectors-c23` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-remaining-connectors-future-c` | Run the `check-remaining-connectors-future-c` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-block-status-generator` | Run the `check-block-status-generator` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-common-adoption` | Run the `check-apache-common-adoption` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-c-standard-wiring` | Run the `check-apache-c-standard-wiring` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-c-standards` | Run the `check-apache-c-standards` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-c17` | Run the `check-apache-c17` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-apache-c17-lint` | Run the `check-apache-c17-lint` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-apache-c23` | Run the `check-apache-c23` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-apache-future-c` | Run the `check-apache-future-c` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-apache-c20` | Run the `check-apache-c20` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-apache-c26` | Run the `check-apache-c26` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-nginx-common-adoption` | Run the `check-nginx-common-adoption` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-nginx-c-standard-wiring` | Run the `check-nginx-c-standard-wiring` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-nginx-c-standards` | Run the `check-nginx-c-standards` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-nginx-c17` | Run the `check-nginx-c17` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-nginx-c17-lint` | Run the `check-nginx-c17-lint` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-nginx-c23` | Run the `check-nginx-c23` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-nginx-future-c` | Run the `check-nginx-future-c` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-nginx-c20` | Run the `check-nginx-c20` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-nginx-c26` | Run the `check-nginx-c26` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-common-adoption` | Run the `check-haproxy-common-adoption` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-haproxy-c-standard-wiring` | Run the `check-haproxy-c-standard-wiring` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-haproxy-c-standards` | Run the `check-haproxy-c-standards` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-haproxy-c17` | Run the `check-haproxy-c17` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-haproxy-c17-lint` | Run the `check-haproxy-c17-lint` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-haproxy-c23` | Run the `check-haproxy-c23` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-future-c` | Run the `check-haproxy-future-c` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-c20` | Run the `check-haproxy-c20` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-c26` | Run the `check-haproxy-c26` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers` | Run the `check-common-helpers` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-common-helpers-c17` | Run the `check-common-helpers-c17` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-common-helpers-c23` | Run the `check-common-helpers-c23` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers-future-c` | Run the `check-common-helpers-future-c` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers-c20` | Run the `check-common-helpers-c20` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers-c26` | Run the `check-common-helpers-c26` workflow. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/header blockers; optional profiles may skip | direct script/action |
| `check-common-sdk-contract` | Run the `check-common-sdk-contract` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-common-security-contract` | Run the `check-common-security-contract` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-common-memory-safety` | Run the `check-common-memory-safety` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-common-flow-integrity` | Run the `check-common-flow-integrity` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-adapter-contracts` | Run the `check-adapter-contracts` workflow. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-directive-parity` | Run the `check-directive-parity` workflow. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `lint` | Run the `lint` workflow. | repo | check-framework | hard | usually no; script-specific | depends on check-framework |
| `summary` | Run the `summary` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `case-matrix` | Run the `case-matrix` workflow. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `install-dev-deps` | Run the `install-dev-deps` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `setup-dev` | Run the `setup-dev` workflow. | repo | install-dev-deps | optional/composite | usually no; script-specific | depends on install-dev-deps |
| `fetch-modsecurity-v3` | Run the `fetch-modsecurity-v3` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `fetch-crs` | Run the `fetch-crs` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-crs` | Run the `prepare-crs` workflow. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `print-python` | Run the `print-python` workflow. | repo | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `bootstrap-all` | Run the `bootstrap-all` workflow. | repo | setup-dev fetch-deps doctor | optional/composite | usually no; script-specific | depends on setup-dev fetch-deps doctor |
| `doctor-install-hints` | Run the `doctor-install-hints` workflow. | repo | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `doctor-quick` | Run the `doctor-quick` workflow. | repo | check-framework | hard | usually no; script-specific | depends on check-framework |
| `quick-all` | Run the `quick-all` workflow. | repo | check-framework | hard | usually no; script-specific | depends on check-framework |
| `cloud-quick-check` | Run the `cloud-quick-check` workflow. | repo | setup-dev lint generate-test-matrix check-test-matrix quick-check | hard | usually no; script-specific | depends on setup-dev lint generate-test-matrix check-test-matrix quick-check |
| `generate-test-matrix` | Run the `generate-test-matrix` workflow. | framework/reports | check-framework | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework |
| `check-test-matrix` | Run the `check-test-matrix` workflow. | framework/reports | check-framework | optional/composite | yes for framework/env/header blockers; optional profiles may skip | depends on check-framework |

### C17, C23 and future-C targets

C17 targets (`check-*-c17`) are the required standard checks when the relevant compiler and headers are present. C23 targets (`check-*-c23`) are optional. future-C targets (`check-*-future-c`) are optional and may use `c2y`/`gnu2y` where supported. `check-*-c20` and `check-*-c26`, where present, are skip/info targets because c20/c26 are not valid C language modes. Exit 77 must mean an environment or unsupported-profile skip, never a hidden compile or contract error.

## Common Makefile Commands

- `make check-common-helpers`: use after common helper changes.
- `make check-common-sdk-contract`: use after adding/changing Common SDK headers or APIs.
- `make check-adapter-contracts`: use after metadata or connector contract changes.
- `make check-directive-parity`: use after directive/config/parser changes.
- `make check-apache-common-adoption && make check-apache-c17`: use after Apache connector changes.
- `make check-nginx-common-adoption && make check-nginx-c17`: use after NGINX connector changes.
- `make check-haproxy-common-adoption && make check-haproxy-c17`: use after HAProxy connector changes.
- `make check-remaining-connectors-common-adoption && make check-remaining-connectors-c17`: use after Envoy/Traefik/lighttpd starter changes; still no runtime claim.
- `make lint`: aggregate repository lint/governance check.
- `make quick-check` or `make codex-check`: lightweight pre-commit validation.

## Exit Codes and BLOCKED/SKIPPED Behavior

- `0`: success.
- `1`, `2` or other non-zero values: real failure or usage error unless the script documents otherwise.
- `77`: BLOCKED/SKIPPED because the environment, headers, compiler, submodule or optional C profile is unavailable.

Exit 77 must not hide real compile or contract failures. Lint wrappers may translate 77 for environment-limited checks, but not for real failures.

## Environment variables

| Variable | Use | Example | Scope |
|---|---|---|---|
| `APACHE_C_STD_PROFILE` | Used by Makefile/CI scripts when present. | `APACHE_C_STD_PROFILE=...` | build/check environment |
| `APXS` | Used by Makefile/CI scripts when present. | `APXS=...` | build/check environment |
| `BUILD_ROOT` | Used by Makefile/CI scripts when present. | `BUILD_ROOT=...` | build/check environment |
| `CONNECTOR_C_STD_PROFILE` | Used by Makefile/CI scripts when present. | `CONNECTOR_C_STD_PROFILE=...` | build/check environment |
| `HAPROXY_C_STD_PROFILE` | Used by Makefile/CI scripts when present. | `HAPROXY_C_STD_PROFILE=...` | build/check environment |
| `HAPROXY_SOURCE_DIR` | Used by Makefile/CI scripts when present. | `HAPROXY_SOURCE_DIR=...` | build/check environment |
| `MODSECURITY_INC` | Used by Makefile/CI scripts when present. | `MODSECURITY_INC=...` | build/check environment |
| `MODSECURITY_INCLUDE_DIR` | Used by Makefile/CI scripts when present. | `MODSECURITY_INCLUDE_DIR=...` | build/check environment |
| `MODSECURITY_NGINX_SOURCE_DIR` | Used by Makefile/CI scripts when present. | `MODSECURITY_NGINX_SOURCE_DIR=...` | build/check environment |
| `MSCONNECTOR_CFLAGS` | Used by Makefile/CI scripts when present. | `MSCONNECTOR_CFLAGS=...` | build/check environment |
| `MSCONNECTOR_COMMON_SRC` | Used by Makefile/CI scripts when present. | `MSCONNECTOR_COMMON_SRC=...` | build/check environment |
| `MSCONNECTOR_C_STD` | Used by Makefile/CI scripts when present. | `MSCONNECTOR_C_STD=...` | build/check environment |
| `NGINX_C_STD_PROFILE` | Used by Makefile/CI scripts when present. | `NGINX_C_STD_PROFILE=...` | build/check environment |
| `NGINX_SOURCE_DIR` | Used by Makefile/CI scripts when present. | `NGINX_SOURCE_DIR=...` | build/check environment |
| `NGINX_SRC` | Used by Makefile/CI scripts when present. | `NGINX_SRC=...` | build/check environment |
| `PYTHON` | Used by Makefile/CI scripts when present. | `PYTHON=...` | build/check environment |


## Connector model

Each connector owns server API glue and may call common config, request/response mapping, directive adapter, decision/intervention/status/event and resource-limit helpers. A connector must state unsupported features as `not supported`, `connector-gap`, `structure-only`, `partial`, `unknown` or `requires runtime evidence`.

## Apache Connector

### Purpose
The Apache Connector keeps host-server API work in `connectors/apache/` while adopting common configuration, mapping, decision, status, event and metadata contracts where implemented.

### Current status
common SDK adoption present; runtime claims require current harness/report evidence.

### Common-SDK adoption
The connector is expected to use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, status/decision/event helpers and common source linking as applicable. Adoption checks are compile/static/contract evidence, not automatic runtime evidence.

### Config-/directive support
Supported common directives are listed in the directive table. Unsupported or host-specific syntax must be marked `not supported`, `not applicable`, `connector-gap` or `structure-only`; Apache-style expressions must not be silently accepted as NGINX syntax.

### Request mapping
Request mapping converts host request objects to `msconnector_request` and header helpers. Missing host details are `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response/header/body state to `msconnector_response`. RESPONSE_BODY behavior must not be called verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
Decision, intervention, status and JSONL event helpers are common semantics. Per-run event output is evidence for that run only.

### Resource-/Body-/DoS-/Flow boundaries
Resource limits, body policy, DoS guard and flow guard are connector-neutral controls. They are guardrails and governance models, not runtime secure or tamper-proof claims.

### C language / checks
C17 is the required compile profile when compiler and headers exist. C23 and future-C are optional. Exit 77 means BLOCKED/SKIPPED for missing environment or unsupported optional profile, not hidden compile failure.

### CI-/contract checks
Use connector-specific common-adoption and C-standard targets plus shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
For Apache Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Implemented
Common-facing structure, metadata, docs/harness stubs or connector sources are present as listed below.

### Missing
Current missing work is any item marked `connector-gap`, `not_verified`, `structure-only`, `unknown`, or `requires runtime evidence`, especially real runtime integration for starter connectors.

### Connector-specific remains
request_rec, command_rec, APR pools, bucket brigades, hooks, filters, APXS/autotools, Apache logging and return codes remain connector-specific and must not move into `common/`.

### Connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/apache/Makefile.am` | Makefile helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/README.de.md` | README.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/TODO.md` | TODO helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/autogen.sh` | autogen helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/build/apxs-wrapper.in` | apxs-wrapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/build/ax_prog_apache.m4` | ax prog apache helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/build/find_apxs.m4` | find apxs helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/build/find_libmodsec.m4` | find libmodsec helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/configure.ac` | configure helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/docs/build.md` | build helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/docs/validation.md` | validation helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/harness/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/harness/run_apache_smoke.sh` | run apache smoke helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/metadata.c` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/metadata.h` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/mod_security3.c` | mod security3 helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/mod_security3.h` | mod security3 helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_apache_mapper.c` | msc apache mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_apache_mapper.h` | msc apache mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_config.c` | msc config helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_config.h` | msc config helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_filters.c` | msc filters helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_filters.h` | msc filters helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_utils.c` | msc utils helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/apache/src/msc_utils.h` | msc utils helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |

## NGINX Connector

### Purpose
The NGINX Connector keeps host-server API work in `connectors/nginx/` while adopting common configuration, mapping, decision, status, event and metadata contracts where implemented.

### Current status
common SDK adoption present; runtime claims require current harness/report evidence.

### Common-SDK adoption
The connector is expected to use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, status/decision/event helpers and common source linking as applicable. Adoption checks are compile/static/contract evidence, not automatic runtime evidence.

### Config-/directive support
Supported common directives are listed in the directive table. Unsupported or host-specific syntax must be marked `not supported`, `not applicable`, `connector-gap` or `structure-only`; Apache-style expressions must not be silently accepted as NGINX syntax.

### Request mapping
Request mapping converts host request objects to `msconnector_request` and header helpers. Missing host details are `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response/header/body state to `msconnector_response`. RESPONSE_BODY behavior must not be called verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
Decision, intervention, status and JSONL event helpers are common semantics. Per-run event output is evidence for that run only.

### Resource-/Body-/DoS-/Flow boundaries
Resource limits, body policy, DoS guard and flow guard are connector-neutral controls. They are guardrails and governance models, not runtime secure or tamper-proof claims.

### C language / checks
C17 is the required compile profile when compiler and headers exist. C23 and future-C are optional. Exit 77 means BLOCKED/SKIPPED for missing environment or unsupported optional profile, not hidden compile failure.

### CI-/contract checks
Use connector-specific common-adoption and C-standard targets plus shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
For NGINX Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Implemented
Common-facing structure, metadata, docs/harness stubs or connector sources are present as listed below.

### Missing
Current missing work is any item marked `connector-gap`, `not_verified`, `structure-only`, `unknown`, or `requires runtime evidence`, especially real runtime integration for starter connectors.

### Connector-specific remains
ngx_http_request_t, ngx_command_t, ngx_chain_t, ngx_buf_t, headers_in/headers_out, filters, pools, return codes and NGINX module build glue remain connector-specific and must not move into `common/`.

### Connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/nginx/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/README.de.md` | README.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/TODO.md` | TODO helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/config` | connector-neutral configuration object, defaults, merge and validation | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/docs/build.md` | build helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/docs/validation.md` | validation helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/harness/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/harness/run_nginx_smoke.sh` | run nginx smoke helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/metadata.c` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/metadata.h` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ddebug.h` | ddebug helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | ngx http modsecurity access helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | ngx http modsecurity body filter helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | ngx http modsecurity common helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | ngx http modsecurity header filter helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | ngx http modsecurity log helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.c` | ngx http modsecurity mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.h` | ngx http modsecurity mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | ngx http modsecurity module helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |

## HAProxy Connector

### Purpose
The HAProxy Connector keeps host-server API work in `connectors/haproxy/` while adopting common configuration, mapping, decision, status, event and metadata contracts where implemented.

### Current status
common SDK adoption present; runtime claims require current harness/report evidence.

### Common-SDK adoption
The connector is expected to use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, status/decision/event helpers and common source linking as applicable. Adoption checks are compile/static/contract evidence, not automatic runtime evidence.

### Config-/directive support
Supported common directives are listed in the directive table. Unsupported or host-specific syntax must be marked `not supported`, `not applicable`, `connector-gap` or `structure-only`; Apache-style expressions must not be silently accepted as NGINX syntax.

### Request mapping
Request mapping converts host request objects to `msconnector_request` and header helpers. Missing host details are `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response/header/body state to `msconnector_response`. RESPONSE_BODY behavior must not be called verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
Decision, intervention, status and JSONL event helpers are common semantics. Per-run event output is evidence for that run only.

### Resource-/Body-/DoS-/Flow boundaries
Resource limits, body policy, DoS guard and flow guard are connector-neutral controls. They are guardrails and governance models, not runtime secure or tamper-proof claims.

### C language / checks
C17 is the required compile profile when compiler and headers exist. C23 and future-C are optional. Exit 77 means BLOCKED/SKIPPED for missing environment or unsupported optional profile, not hidden compile failure.

### CI-/contract checks
Use connector-specific common-adoption and C-standard targets plus shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
For HAProxy Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Implemented
Common-facing structure, metadata, docs/harness stubs or connector sources are present as listed below.

### Missing
Current missing work is any item marked `connector-gap`, `not_verified`, `structure-only`, `unknown`, or `requires runtime evidence`, especially real runtime integration for starter connectors.

### Connector-specific remains
SPOE/SPOP, frame parsing, runtime loop, socket handling, HAProxy cfg snippets, process lifecycle and build glue remain connector-specific and must not move into `common/`.

### Connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/haproxy/Makefile` | Makefile helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/README.de.md` | README.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/TODO.md` | TODO helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/build.md` | build helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/evidence-findings.de.md` | evidence-findings.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/evidence-findings.md` | evidence-findings helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/evidence-questionnaire.de.md` | evidence-questionnaire.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/evidence-questionnaire.md` | evidence-questionnaire helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/integration-decision.md` | integration-decision helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/spoe-external-evidence.de.md` | spoe-external-evidence.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/spoe-external-evidence.md` | spoe-external-evidence helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/spoe-minimal-artifacts.md` | spoe-minimal-artifacts helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/spoe-poc-plan.md` | spoe-poc-plan helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/test-framework-contract.md` | test-framework-contract helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/docs/validation.md` | validation helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/harness/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | run haproxy smoke helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/metadata.c` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/metadata.h` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/agent/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/agent/design.md` | design helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/harness/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/harness/design.md` | design helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/reports/README.de.md` | README.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/reports/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/poc/spoe/syntax-validation.md` | syntax-validation helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_modsecurity_binding.c` | haproxy modsecurity binding helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_modsecurity_binding.h` | haproxy modsecurity binding helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c` | haproxy modsecurity binding self test helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.c` | haproxy modsecurity mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.h` | haproxy modsecurity mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | haproxy spoa agent starter helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | haproxy spoa agent starter helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_spoa_main.c` | haproxy spoa main helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | haproxy spop diagnostic runtime helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | implemented or documented; requires evidence for runtime claims |

## Envoy Connector

### Purpose
The Envoy Connector keeps host-server API work in `connectors/envoy/` while adopting common configuration, mapping, decision, status, event and metadata contracts where implemented.

### Current status
not_verified / connector-gap; starter / structure-only / compile-only; no production, CRS, full-matrix or RESPONSE_BODY claim.

### Common-SDK adoption
The connector is expected to use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, status/decision/event helpers and common source linking as applicable. Adoption checks are compile/static/contract evidence, not automatic runtime evidence.

### Config-/directive support
Supported common directives are listed in the directive table. Unsupported or host-specific syntax must be marked `not supported`, `not applicable`, `connector-gap` or `structure-only`; Apache-style expressions must not be silently accepted as NGINX syntax.

### Request mapping
Request mapping converts host request objects to `msconnector_request` and header helpers. Missing host details are `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response/header/body state to `msconnector_response`. RESPONSE_BODY behavior must not be called verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
Decision, intervention, status and JSONL event helpers are common semantics. Per-run event output is evidence for that run only.

### Resource-/Body-/DoS-/Flow boundaries
Resource limits, body policy, DoS guard and flow guard are connector-neutral controls. They are guardrails and governance models, not runtime secure or tamper-proof claims.

### C language / checks
C17 is the required compile profile when compiler and headers exist. C23 and future-C are optional. Exit 77 means BLOCKED/SKIPPED for missing environment or unsupported optional profile, not hidden compile failure.

### CI-/contract checks
Use connector-specific common-adoption and C-standard targets plus shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
For Envoy Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Implemented
Common-facing structure, metadata, docs/harness stubs or connector sources are present as listed below.

### Missing
Current missing work is any item marked `connector-gap`, `not_verified`, `structure-only`, `unknown`, or `requires runtime evidence`, especially real runtime integration for starter connectors.

### Connector-specific remains
Envoy filter/runtime API, native Envoy SDK ownership and deployed proxy integration remain connector-specific and must not move into `common/`.

### Connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/envoy/Makefile` | Makefile helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/envoy/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/README.de.md` | README.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/TODO.md` | TODO helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/build/build_metadata.sh` | build metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/build.md` | build helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/validation.md` | validation helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/harness/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/envoy/harness/run_envoy_smoke.sh` | run envoy smoke helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/envoy/metadata.c` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/metadata.h` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/src/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_bridge.c` | envoy bridge helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_bridge.h` | envoy bridge helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_bridge_main.c` | envoy bridge main helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_modsecurity_mapper.h` | envoy modsecurity mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |

## Traefik Connector

### Purpose
The Traefik Connector keeps host-server API work in `connectors/traefik/` while adopting common configuration, mapping, decision, status, event and metadata contracts where implemented.

### Current status
not_verified / connector-gap; starter / structure-only / compile-only; no production, CRS, full-matrix or RESPONSE_BODY claim.

### Common-SDK adoption
The connector is expected to use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, status/decision/event helpers and common source linking as applicable. Adoption checks are compile/static/contract evidence, not automatic runtime evidence.

### Config-/directive support
Supported common directives are listed in the directive table. Unsupported or host-specific syntax must be marked `not supported`, `not applicable`, `connector-gap` or `structure-only`; Apache-style expressions must not be silently accepted as NGINX syntax.

### Request mapping
Request mapping converts host request objects to `msconnector_request` and header helpers. Missing host details are `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response/header/body state to `msconnector_response`. RESPONSE_BODY behavior must not be called verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
Decision, intervention, status and JSONL event helpers are common semantics. Per-run event output is evidence for that run only.

### Resource-/Body-/DoS-/Flow boundaries
Resource limits, body policy, DoS guard and flow guard are connector-neutral controls. They are guardrails and governance models, not runtime secure or tamper-proof claims.

### C language / checks
C17 is the required compile profile when compiler and headers exist. C23 and future-C are optional. Exit 77 means BLOCKED/SKIPPED for missing environment or unsupported optional profile, not hidden compile failure.

### CI-/contract checks
Use connector-specific common-adoption and C-standard targets plus shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
For Traefik Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Implemented
Common-facing structure, metadata, docs/harness stubs or connector sources are present as listed below.

### Missing
Current missing work is any item marked `connector-gap`, `not_verified`, `structure-only`, `unknown`, or `requires runtime evidence`, especially real runtime integration for starter connectors.

### Connector-specific remains
Traefik middleware/proxy/runtime API and real traffic path integration remain connector-specific and must not move into `common/`.

### Connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/traefik/Makefile` | Makefile helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/README.de.md` | README.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/TODO.md` | TODO helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/build/build-starter.sh` | build-starter helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/build.md` | build helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/validation.md` | validation helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/harness/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/harness/run_traefik_smoke.sh` | run traefik smoke helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/metadata.c` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/metadata.h` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/src/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_build_starter.c` | traefik build starter helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_decision_service.c` | traefik decision service helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_decision_service.h` | traefik decision service helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_decision_service_main.c` | traefik decision service main helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_modsecurity_mapper.h` | traefik modsecurity mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |

## lighttpd Connector

### Purpose
The lighttpd Connector keeps host-server API work in `connectors/lighttpd/` while adopting common configuration, mapping, decision, status, event and metadata contracts where implemented.

### Current status
not_verified / connector-gap; starter / structure-only / compile-only; no production, CRS, full-matrix or RESPONSE_BODY claim.

### Common-SDK adoption
The connector is expected to use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, status/decision/event helpers and common source linking as applicable. Adoption checks are compile/static/contract evidence, not automatic runtime evidence.

### Config-/directive support
Supported common directives are listed in the directive table. Unsupported or host-specific syntax must be marked `not supported`, `not applicable`, `connector-gap` or `structure-only`; Apache-style expressions must not be silently accepted as NGINX syntax.

### Request mapping
Request mapping converts host request objects to `msconnector_request` and header helpers. Missing host details are `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response/header/body state to `msconnector_response`. RESPONSE_BODY behavior must not be called verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
Decision, intervention, status and JSONL event helpers are common semantics. Per-run event output is evidence for that run only.

### Resource-/Body-/DoS-/Flow boundaries
Resource limits, body policy, DoS guard and flow guard are connector-neutral controls. They are guardrails and governance models, not runtime secure or tamper-proof claims.

### C language / checks
C17 is the required compile profile when compiler and headers exist. C23 and future-C are optional. Exit 77 means BLOCKED/SKIPPED for missing environment or unsupported optional profile, not hidden compile failure.

### CI-/contract checks
Use connector-specific common-adoption and C-standard targets plus shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
For lighttpd Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Implemented
Common-facing structure, metadata, docs/harness stubs or connector sources are present as listed below.

### Missing
Current missing work is any item marked `connector-gap`, `not_verified`, `structure-only`, `unknown`, or `requires runtime evidence`, especially real runtime integration for starter connectors.

### Connector-specific remains
lighttpd plugin/proxy/runtime API and FastCGI/SCGI/native module integration remain connector-specific and must not move into `common/`.

### Connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/lighttpd/Makefile` | Makefile helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/README.de.md` | README.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/TODO.md` | TODO helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/build/bridge_starter.sh` | bridge starter helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/build/build_starter.sh` | build starter helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/build.md` | build helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/validation.md` | validation helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/harness/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/harness/run_lighttpd_smoke.sh` | run lighttpd smoke helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/metadata.c` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/metadata.h` | metadata helper/model for the connector-neutral SDK | uses common contracts where included; see source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/src/README.md` | README helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_bridge.c` | lighttpd bridge helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_bridge.h` | lighttpd bridge helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_bridge_main.c` | lighttpd bridge main helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_build_starter.c` | lighttpd build starter helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_modsecurity_mapper.h` | lighttpd modsecurity mapper helper/model for the connector-neutral SDK | uses common contracts where included; see source | yes | not_verified / connector-gap |

## Connector status matrix

| Connector | Current status | Common adoption | Runtime evidence | Forbidden inference |
|---|---|---|---|---|
| Apache | implemented connector source | present | requires current reports/harness output | no production/runtime/CRS/full-matrix claim |
| NGINX | implemented connector source | present | requires current reports/harness output | no production/runtime/CRS/full-matrix claim |
| HAProxy | SPOA/starter plus mapper/binding source | present/partial | requires current reports/harness output | no production/runtime/CRS/full-matrix claim |
| Envoy | starter/structure-only/compile-only | prepared | missing | no production, CRS, full-matrix or RESPONSE_BODY claim |
| Traefik | starter/structure-only/compile-only | prepared | missing; per-run result only if run | no production, CRS, full-matrix or RESPONSE_BODY claim |
| lighttpd | starter/structure-only/compile-only | prepared | missing | no production, CRS, full-matrix or RESPONSE_BODY claim |

## Test framework relation

The reusable test framework is expected under `modules/ModSecurity-test-Framework`. Framework-dependent targets can be BLOCKED when the submodule or its inputs are missing. That does not automatically mean common/connector compile checks failed.

## Runtime evidence and verification policy

Connector metadata fields such as `runtime_status`, `verification_status`, `not_verified` and `connector-gap` describe repository-level connector state. Per-run `result.json` fields such as `status: PASS/BLOCKED/FAIL`, `runtime_verified: true/false` and `runtime_status: verified/blocked/...` describe only that run. A starter smoke may produce a per-run PASS or even `runtime_verified: true` for the run, but that does not automatically change connector metadata from `not_verified / connector-gap`.

## Implemented work

Implemented repository facts include the Common SDK, config/directive/parser model, request/response mapper contracts, common security/data-flow guard helpers, Apache/NGINX/HAProxy common-adoption structures, Envoy/Traefik/lighttpd starter preparation, C17/C23/future-C check wiring, CI/governance scripts and generated docs/reports areas. Treat each as static/compile/governance evidence unless runtime evidence is current and specific.

## Missing/future work

Missing or future work includes real runtime evidence for Envoy, Traefik and lighttpd; CRS matrix evidence; RESPONSE_BODY runtime evidence; full-matrix verification; production hardening; HMAC/signed event chains if desired; append-only evidence storage if desired; and additional runtime harnesses.

## Known limits

Known limits are connector-specific host APIs, environment-dependent headers/toolchains, framework/submodule blockers, starter-only connectors, partial/unknown runtime coverage and documentation that must be kept synchronized with metadata and reports.

## Intentionally connector-specific

Apache request/APR/filter/APXS details, NGINX request/chain/filter/module glue, HAProxy SPOE/SPOP/frame/runtime loop, Envoy APIs, Traefik APIs and lighttpd APIs remain outside `common/`.

## AI fact block

```yaml
repository: Easton97-Jens/ModSecurity-conector
purpose: Shared Common SDK layer for ModSecurity connectors
common_sdk: true
production_ready: false
runtime_verified_all_connectors: false
apache_common_adopted: true
nginx_common_adopted: true
haproxy_common_adopted: true
envoy_status: not_verified / connector-gap
traefik_status: not_verified / connector-gap
lighttpd_status: not_verified / connector-gap
c_standard_required: C17
c_standard_optional:
  - C23
  - future-C / c2y / gnu2y
forbidden_claims:
  - production-ready
  - runtime secure
  - security verified
  - CRS verified
  - full matrix verified
  - response body verified
  - runtime verified
  - production hardened
  - tamper-proof
  - cryptographic integrity
```

## Allowed and forbidden claims

Allowed claims: connector-neutral common semantics, C17 required check when environment exists, optional C23/future-C, compile-only/static/governance checks, starter/structure-only status and per-run evidence scoped to that run. Forbidden without current evidence: production-ready, runtime secure, security verified, CRS verified, full matrix verified, response body verified, runtime verified, production hardened, tamper-proof and cryptographic integrity.

## Glossary

- `common`: connector-neutral SDK and semantics.
- `connector-gap`: known gap between starter/structure and real connector runtime integration.
- `not_verified`: no current repository-level runtime verification claim.
- `structure-only`: files/scaffolding exist but do not prove runtime behavior.
- `compile-only`: compiler/static check evidence only.
- `runtime evidence`: current run/report proving specific runtime behavior.
- `SOURCE_MAP`: connector source/origin/status mapping metadata.

## Maintenance checklist

```text
- New Common file -> update the Common SDK file index.
- New directive -> update directives.h, directive_spec, directive_adapter and docs.
- New parser -> update the config/directive table.
- New connector -> update the status matrix.
- New C source -> update the C17 source list.
- New header -> update header smoke checks.
- New mapper -> verify ownership/cleanup.
- Status change -> keep metadata, SOURCE_MAP, reports and docs synchronized.
- Keep German docs synchronized with English docs.
- Runtime claims only with evidence.
```
