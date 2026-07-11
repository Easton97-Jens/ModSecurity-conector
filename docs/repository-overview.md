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
31. [Known limitations](#known-limitations)
32. [Intentionally connector-specific](#intentionally-connector-specific)
33. [AI fact block](#ai-fact-block)
34. [Allowed and forbidden claims](#allowed-and-forbidden-claims)
35. [Glossary](#glossary)
36. [Maintenance checklist](#maintenance-checklist)

## Repository purpose

This repository builds ModSecurity connectors plus a shared Common SDK layer. The architectural goal is to keep connector-neutral semantics in `common/` and host/server API integration in the individual connector directories.

Principle: semantic logic belongs in `common/`; host/server API glue remains in each connector.

Common examples are configuration, directives, directive specifications, parser helpers, request and response models, header helpers, mapper contracts, decision/intervention/status/error models, event JSONL, resource limits, DoS guard, flow guard, integrity metadata, rule-loading contracts, test-result JSON, adapter metadata, capabilities and generic mapper helpers.

Connector-specific examples are Apache `request_rec`, `command_rec`, APR pools and filters; NGINX `ngx_http_request_t`, `ngx_chain_t` and filters; HAProxy SPOE/SPOP, frame parsing and runtime loop; Envoy filter/runtime APIs; Traefik middleware/proxy/runtime APIs; and lighttpd plugin/proxy/runtime APIs.

## Short summary for humans

All six connector areas contain real host-path implementations. Envoy, Traefik
and lighttpd have narrow `minimal_runtime_smoke` evidence for their selected
host models; they are no longer described as starter-only connectors. The
canonical capability manifests are present, but the canonical No-CRS baseline
has not been executed on this branch. Unsupported, not implemented, and not
executed capabilities remain distinct from verified behavior.

## Short summary for AI systems

Use the current repository code, capability manifests, CI scripts, metadata,
and generated reports as source of truth. Do not infer runtime guarantees from
a file name, Makefile target, legacy smoke, or local `result.json`. Distinguish
implementation state from canonical per-run evidence. If evidence is missing,
use the canonical `NOT EXECUTED`, `IMPLEMENTED, NOT ASSERTED`, `UNSUPPORTED`, or
`NOT IMPLEMENTED` state that matches the manifest and result contract.

## Architecture principle

`common/` defines connector-neutral C/C++ contracts and helpers. `connectors/<name>/` adapts server APIs into those contracts. Generated reports live under `reports/`; CI and governance scripts live in `ci/`; reusable tests are expected from `modules/ModSecurity-test-Framework`.

## Repository structure

| Path | Meaning | Evidence status |
|---|---|---|
| `common/include/msconnector/` | Public Common SDK headers. | Contract/static evidence unless a run proves more. |
| `common/src/` | Common SDK helper implementations. | C17/common checks. |
| `connectors/apache/` | Apache adapter source, docs, harness and metadata. | Common adoption; runtime claims require current evidence. |
| `connectors/nginx/` | NGINX adapter source, docs, harness and metadata. | Common adoption; runtime claims require current evidence. |
| `connectors/haproxy/` | HAProxy/SPOA source, docs, harness and metadata. | Common adoption; runtime claims require current evidence. |
| `connectors/envoy/` | Real HTTP `ext_authz` service path. | Targeted `minimal_runtime_smoke`; canonical No-CRS `NOT EXECUTED`. |
| `connectors/traefik/` | Real HTTP `forwardAuth` service path. | Targeted `minimal_runtime_smoke`; canonical No-CRS `NOT EXECUTED`. |
| `connectors/lighttpd/` | Native `mod_msconnector.so` plugin path. | Targeted `minimal_runtime_smoke`; canonical No-CRS `NOT EXECUTED`. |
| `ci/` | Lint, contract, governance, C-standard and report scripts. | Check definitions, not runtime evidence by themselves. |
| `docs/`, `docs/architecture/`, `docs/connectors/` | Repository, architecture and connector documentation. | Documentation; must stay synchronized with source and reports. |
| `reports/` | Generated reports/evidence/matrices. | Trust only current status labels and evidence scope. |

## Common SDK: complete file index

| File | Type | Purpose | Important APIs/structs | Used by | Status / notes |
|---|---|---|---|---|---|
| `common/include/msconnector/adapter.h` | header | adapter integration object and common adapter lifecycle helpers | MSCONNECTOR_ADAPTER_H, msconnector_adapter, msconnector_adapter_metadata, msconnector_capabilities, msconnector_config, msconnector_error, msconnector_transaction_view, msconnector_decision | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/adapter_contract.h` | header | adapter contract validation declarations/implementation | MSCONNECTOR_ADAPTER_CONTRACT_H, msconnector_adapter_contract_result, msconnector_adapter_contract_result_init, msconnector_adapter_contract_validate, msconnector_adapter | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/adapter_metadata.h` | header | adapter metadata and origin/capability completeness checks | MSCONNECTOR_ADAPTER_METADATA_H, msconnector_adapter_metadata, msconnector_origin, msconnector_capabilities, msconnector_adapter_metadata_init, msconnector_adapter_metadata_is_complete | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/artifact_layout.h` | header | standard artifact names for run outputs | MSCONNECTOR_ARTIFACT_LAYOUT_H, msconnector_artifact_layout, msconnector_artifact_layout_init, msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log, msconnector_artifact_name_runtime_stdout_log | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/artifacts.h` | header | default artifact path helpers | MSCONNECTOR_ARTIFACTS_H, msconnector_artifact_paths, msconnector_artifact_paths_init, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/block_statuses.h` | header | allowed/default block and error status helpers | MSCONNECTOR_BLOCK_STATUSES_H, MSCONNECTOR_DEFAULT_BLOCK_STATUS, MSCONNECTOR_DEFAULT_ERROR_STATUS, MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS, msconnector_block_status_support, msconnector_block_status_is_allowed, msconnector_block_status_normalize, msconnector_http_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/blocking.h` | header | blocking policy/action helpers | MSCONNECTOR_BLOCKING_H, msconnector_block_action, MSCONNECTOR_BLOCK_ACTION_DENY, MSCONNECTOR_BLOCK_ACTION_REDIRECT, MSCONNECTOR_BLOCK_ACTION_DROP, MSCONNECTOR_BLOCK_ACTION_LOG_ONLY, MSCONNECTOR_BLOCK_ACTION_ABORT_CONNECTION, msconnector_blocking_policy | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/body_policy.h` | header | body handling policy model | MSCONNECTOR_BODY_POLICY_H, msconnector_body_mode, MSCONNECTOR_BODY_MODE_NONE, MSCONNECTOR_BODY_MODE_BUFFERED, MSCONNECTOR_BODY_MODE_STREAMING, msconnector_body_policy, msconnector_body_policy_init, msconnector_body_mode_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/build_contract.h` | header | build target naming and C-standard contract helpers | MSCONNECTOR_BUILD_CONTRACT_H, msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/capabilities.h` | header | capability flags and capability lookup helpers | MSCONNECTOR_CAPABILITIES_H, msconnector_capability_flags, msconnector_capability_flag, MSCONNECTOR_CAPABILITY_NONE, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED, MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/capabilities.hpp` | header | capability flags and capability lookup helpers | MSCONNECTOR_CAPABILITIES_HPP, msconnector_capability_flags, msconnector_capability_flag, msconnector_capabilities, msconnector_capability_name | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/capability_matrix.h` | header | capability-to-required-test mapping | MSCONNECTOR_CAPABILITY_MATRIX_H, msconnector_capability_required_test, msconnector_capability_flag, msconnector_capability_has_required_test | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/config.h` | header | connector-neutral configuration object, defaults, merge and validation | MSCONNECTOR_CONFIG_H, msconnector_config, msconnector_bool_option, msconnector_phase4_mode, msconnector_config_init, msconnector_config_apply_defaults, msconnector_config_merge, msconnector_config_validate | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/config_parser.h` | header | parsers for booleans, phase4 mode, sizes, HTTP status and content-type tokens | MSCONNECTOR_CONFIG_PARSER_H, msconnector_parse_bool, msconnector_bool_option, msconnector_parse_phase4_mode, msconnector_phase4_mode, msconnector_parse_size, msconnector_parse_http_status, msconnector_validate_content_type_token | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/connector_manifest.h` | header | connector manifest JSON metadata helpers | MSCONNECTOR_CONNECTOR_MANIFEST_H, msconnector_connector_manifest, msconnector_capability_flags, msconnector_connector_manifest_init, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_connector_manifest_write_json | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/crs.h` | header | CRS configuration/mode helpers | MSCONNECTOR_CRS_H, msconnector_crs_mode, MSCONNECTOR_CRS_DISABLED, MSCONNECTOR_CRS_EXTERNAL_PATH, MSCONNECTOR_CRS_BUNDLED_PATH, MSCONNECTOR_CRS_TEST_FIXTURE, msconnector_crs_config, msconnector_crs_config_init | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/decision.h` | header | inspection decision model | MSCONNECTOR_DECISION_H, msconnector_event, msconnector_decision_kind, MSCONNECTOR_DECISION_KIND_ALLOW, MSCONNECTOR_DECISION_KIND_LOG_ONLY, MSCONNECTOR_DECISION_KIND_DENY, MSCONNECTOR_DECISION_KIND_REDIRECT, MSCONNECTOR_DECISION_KIND_DROP | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/decision_action.h` | header | decision-to-action mapping helpers | MSCONNECTOR_DECISION_ACTION_H, msconnector_decision_action, MSCONNECTOR_DECISION_ACTION_ALLOW, MSCONNECTOR_DECISION_ACTION_DENY, MSCONNECTOR_DECISION_ACTION_REDIRECT, MSCONNECTOR_DECISION_ACTION_DROP, MSCONNECTOR_DECISION_ACTION_LOG_ONLY, MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/directive_adapter.h` | header | common directive adapter catalog and validation | MSCONNECTOR_DIRECTIVE_ADAPTER_H, msconnector_directive_scope, MSCONNECTOR_DIRECTIVE_SCOPE_GLOBAL, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_SCOPE_LOCATION, MSCONNECTOR_DIRECTIVE_SCOPE_DIRECTORY, msconnector_directive_argument_policy, MSCONNECTOR_DIRECTIVE_ARG_NONE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/directive_spec.h` | header | global directive specification catalog | MSCONNECTOR_DIRECTIVE_SPEC_H, msconnector_directive_value_type, MSCONNECTOR_DIRECTIVE_VALUE_BOOL, MSCONNECTOR_DIRECTIVE_VALUE_STRING, MSCONNECTOR_DIRECTIVE_VALUE_PATH, MSCONNECTOR_DIRECTIVE_VALUE_ENUM, MSCONNECTOR_DIRECTIVE_VALUE_SIZE, msconnector_directive_spec | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/directives.h` | header | canonical directive name macros | MSCONNECTOR_DIRECTIVES_H, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_RULES_REMOTE, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR, MSCONNECTOR_DIRECTIVE_PHASE4_MODE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/dos_guard.h` | header | request/response DoS guard checks | MSCONNECTOR_DOS_GUARD_H, msconnector_dos_guard_check_request, msconnector_request, msconnector_resource_limits, msconnector_error, msconnector_dos_guard_check_response, msconnector_response, msconnector_dos_guard_check_event_json_size | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/error.h` | header | common error code and message model | MSCONNECTOR_ERROR_H, msconnector_error_code, MSCONNECTOR_ERROR_NONE, MSCONNECTOR_ERROR_INVALID_CONFIG, MSCONNECTOR_ERROR_RULE_PARSE_FAILED, MSCONNECTOR_ERROR_RULE_LOAD_FAILED, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/event.h` | header | event data model | MSCONNECTOR_EVENT_H, msconnector_event_meta, msconnector_event_decision, msconnector_phase, msconnector_status, msconnector_event_http, msconnector_event_request, msconnector_event_integrity | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/event_jsonl.h` | header | JSONL event serialization | MSCONNECTOR_EVENT_JSONL_H, msconnector_event_write_jsonl_line, msconnector_event | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/flow_guard.h` | header | phase/flow guard state machine | MSCONNECTOR_FLOW_GUARD_H, MSCONNECTOR_FLOW_GUARD_OK, MSCONNECTOR_FLOW_GUARD_INVALID, MSCONNECTOR_FLOW_GUARD_PHASE_ORDER, MSCONNECTOR_FLOW_GUARD_IMMUTABLE, MSCONNECTOR_FLOW_GUARD_DUPLICATE_MUTATION, msconnector_flow_guard, msconnector_phase | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/generic_mapper.h` | header | generic request/response mapper for starter connectors | MSCONNECTOR_GENERIC_MAPPER_H, msconnector_generic_request_source, msconnector_endpoint, msconnector_header, msconnector_bytes, msconnector_generic_response_source, msconnector_generic_config_init, msconnector_config | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/headers.h` | header | case-insensitive header lookup helpers | MSCONNECTOR_HEADERS_H, msconnector_header_name_equals, msconnector_header, msconnector_header_name_is, msconnector_headers_find, msconnector_headers_find_first, msconnector_headers_find_last, msconnector_headers_count_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/http_status.h` | header | HTTP status validation/classification helpers | MSCONNECTOR_HTTP_STATUS_H, msconnector_http_status_class, MSCONNECTOR_HTTP_STATUS_CLASS_UNKNOWN, MSCONNECTOR_HTTP_STATUS_CLASS_INFORMATIONAL, MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS, MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION, MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/integrity_event.h` | header | integrity metadata helpers based on non-cryptographic hashes | MSCONNECTOR_INTEGRITY_EVENT_H, msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/intervention.h` | header | intervention/blocking result helpers | MSCONNECTOR_INTERVENTION_H, msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/intervention.hpp` | header | intervention/blocking result helpers | MSCONNECTOR_INTERVENTION_HPP, msconnector_intervention | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/json_escape.h` | header | JSON string escaping helper | MSCONNECTOR_JSON_ESCAPE_H, msconnector_json_escape | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/late_intervention.h` | header | late-intervention policy helpers | MSCONNECTOR_LATE_INTERVENTION_H, msconnector_late_intervention_action, MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY, MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE, MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION, msconnector_late_intervention_policy, msconnector_late_intervention_policy_init, msconnector_late_intervention_action_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/lifecycle_status.h` | header | build/runtime/verification status names | MSCONNECTOR_LIFECYCLE_STATUS_H, msconnector_build_status, MSCONNECTOR_BUILD_STATUS_NOT_STARTED, MSCONNECTOR_BUILD_STATUS_STARTER, MSCONNECTOR_BUILD_STATUS_COMPILES, MSCONNECTOR_BUILD_STATUS_LINKS, MSCONNECTOR_BUILD_STATUS_RUNTIME_READY, msconnector_runtime_status | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/limits.h` | header | compiled-in limit constants | MSCONNECTOR_LIMITS_H, MSCONNECTOR_MAX_HEADER_COUNT, MSCONNECTOR_MAX_HEADER_NAME_LENGTH, MSCONNECTOR_MAX_HEADER_VALUE_LENGTH, MSCONNECTOR_MAX_TOTAL_HEADER_BYTES, MSCONNECTOR_MAX_BODY_BUFFER_SIZE, MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE, MSCONNECTOR_MAX_EVENT_JSON_BYTES | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/log_sanitize.h` | header | log redaction/sanitization helpers | MSCONNECTOR_LOG_SANITIZE_H, msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/logging.h` | header | neutral logging callback model | MSCONNECTOR_LOGGING_H, msconnector_log_level, MSCONNECTOR_LOG_TRACE, MSCONNECTOR_LOG_DEBUG, MSCONNECTOR_LOG_INFO, MSCONNECTOR_LOG_WARN, MSCONNECTOR_LOG_ERROR, msconnector_log_record | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/logging.hpp` | header | neutral logging callback model | MSCONNECTOR_LOGGING_HPP, msconnector_log_level, msconnector_log_record, msconnector_logger, msconnector_log | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/memory.h` | header | checked allocation and allocator callbacks | MSCONNECTOR_MEMORY_H, msconnector_alloc_checked, msconnector_free_checked, msconnector_alloc_callback, msconnector_free_callback, msconnector_allocator, msconnector_allocator_init, msconnector_allocator_within_limit | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/modsecurity_engine.h` | header | connector-neutral ModSecurity engine operation table | MSCONNECTOR_MODSECURITY_ENGINE_H, msconnector_modsecurity_engine_ops, msconnector_error, msconnector_request, msconnector_decision, msconnector_response, msconnector_modsecurity_engine, msconnector_modsecurity_transaction | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/options.h` | header | common option enums and defaults | MSCONNECTOR_OPTIONS_H, MSCONNECTOR_OPTION_ENABLE, MSCONNECTOR_OPTION_RULES_INLINE, MSCONNECTOR_OPTION_RULES_FILE, MSCONNECTOR_OPTION_RULES_REMOTE, MSCONNECTOR_OPTION_TRANSACTION_ID, MSCONNECTOR_OPTION_USE_ERROR_LOG, MSCONNECTOR_OPTION_PHASE4_MODE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/origin.h` | header | source/origin metadata helpers | MSCONNECTOR_ORIGIN_H, msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/origin.hpp` | header | source/origin metadata helpers | MSCONNECTOR_ORIGIN_HPP, msconnector_origin, msconnector_origin_is_empty | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/origin_governance.h` | header | origin governance completeness helpers | MSCONNECTOR_ORIGIN_GOVERNANCE_H, msconnector_origin_governance, msconnector_origin_governance_init, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/path_policy.h` | header | path validation helpers | MSCONNECTOR_PATH_POLICY_H, msconnector_path_is_absolute, msconnector_path_is_empty, msconnector_path_has_parent_reference | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/phase.h` | header | ModSecurity phase enum | MSCONNECTOR_PHASE_H, msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_URI, MSCONNECTOR_PHASE_REQUEST_HEADERS, MSCONNECTOR_PHASE_REQUEST_BODY, MSCONNECTOR_PHASE_RESPONSE_HEADERS, MSCONNECTOR_PHASE_RESPONSE_BODY | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/redaction.h` | header | string redaction helpers | MSCONNECTOR_REDACTION_H, msconnector_redacted_string, msconnector_redact_copy | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/request.h` | header | connector-neutral request model | MSCONNECTOR_REQUEST_H, msconnector_bytes, msconnector_header, msconnector_endpoint, msconnector_request | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/request.hpp` | header | connector-neutral request model | MSCONNECTOR_REQUEST_HPP, msconnector_bytes, msconnector_header, msconnector_endpoint, msconnector_request, msconnector_request_init, msconnector_request_validate | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/request_helpers.h` | header | request initialization/validation helpers | MSCONNECTOR_REQUEST_HELPERS_H, msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_resource_limits, msconnector_request_has_header, msconnector_request_header_value | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/request_mapper_contract.h` | header | request mapper contract validation | MSCONNECTOR_REQUEST_MAPPER_CONTRACT_H, msconnector_mapper_requirement, MSCONNECTOR_MAPPER_REQUIRED, MSCONNECTOR_MAPPER_OPTIONAL, MSCONNECTOR_MAPPER_UNSUPPORTED, msconnector_request_mapper_contract, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract_validate | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/resource_limits.h` | header | runtime resource limits and validators | MSCONNECTOR_RESOURCE_LIMITS_H, msconnector_resource_limits, msconnector_resource_limits_init, msconnector_resource_limits_validate, msconnector_resource_limits_headers_ok, msconnector_header, msconnector_resource_limits_body_ok | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/response.h` | header | connector-neutral response model | MSCONNECTOR_RESPONSE_H, msconnector_response, msconnector_header, msconnector_bytes | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/response.hpp` | header | connector-neutral response model | MSCONNECTOR_RESPONSE_HPP, msconnector_response, msconnector_response_init, msconnector_response_validate | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/response_helpers.h` | header | response initialization/validation helpers | MSCONNECTOR_RESPONSE_HELPERS_H, msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_response_validate_with_limits, msconnector_resource_limits, msconnector_response_has_header, msconnector_response_header_value | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/response_mapper_contract.h` | header | response mapper contract validation | MSCONNECTOR_RESPONSE_MAPPER_CONTRACT_H, msconnector_response_mapper_contract, msconnector_mapper_requirement, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output, msconnector_response | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_error.h` | header | rule-load error helpers | MSCONNECTOR_RULE_ERROR_H, msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_rule_error_set_load_failed, msconnector_rule_error_clear | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_event.h` | header | rule-load event helpers | MSCONNECTOR_RULE_EVENT_H, msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_rule_load_event, msconnector_rule_error_event, msconnector_error | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_id.h` | header | rule ID copy/extraction/validation helpers | MSCONNECTOR_RULE_ID_H, msconnector_rule_id_copy, msconnector_rule_id_extract_from_message, msconnector_rule_id_validate | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_load_stats.h` | header | rule-load statistics model | MSCONNECTOR_RULE_LOAD_STATS_H, msconnector_rule_load_stats, msconnector_rule_load_stats_init, msconnector_rule_load_stats_add, msconnector_rule_load_stats_add_inline, msconnector_rule_load_stats_add_file, msconnector_rule_load_stats_add_remote | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_loader.h` | header | rule loading backend contract | MSCONNECTOR_RULE_LOADER_H, msconnector_rule_loader_backend, msconnector_error, msconnector_rule_loader, msconnector_rule_load_stats, msconnector_rule_loader_init, msconnector_rule_loader_add_inline, msconnector_rule_loader_add_file | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/rule_merge.h` | header | rule collection merge helpers | MSCONNECTOR_RULE_MERGE_H, msconnector_rule_collection, msconnector_rule_collection_init, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/runtime_paths.h` | header | runtime path join helper | MSCONNECTOR_RUNTIME_PATHS_H, msconnector_runtime_path_join | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/runtime_report.h` | header | runtime report JSON helper | MSCONNECTOR_RUNTIME_REPORT_H, msconnector_runtime_report, msconnector_status, msconnector_runtime_report_init, msconnector_runtime_report_write_json | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/status.h` | header | common PASS/FAIL/BLOCKED-like status helpers | MSCONNECTOR_STATUS_H, msconnector_status, MSCONNECTOR_STATUS_OK, MSCONNECTOR_STATUS_ERROR, MSCONNECTOR_STATUS_BLOCKED, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_status_name, msconnector_status_from_result | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/status.hpp` | header | common PASS/FAIL/BLOCKED-like status helpers | MSCONNECTOR_STATUS_HPP, msconnector_status, msconnector_status_name | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/test_result.h` | header | test result model | MSCONNECTOR_TEST_RESULT_H, msconnector_test_result, msconnector_status, msconnector_test_result_init, msconnector_test_result_passed | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/test_result_json.h` | header | test result JSON writer | MSCONNECTOR_TEST_RESULT_JSON_H, msconnector_test_result_write_json, msconnector_test_result | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/transaction.h` | header | transaction view helpers | MSCONNECTOR_TRANSACTION_H, msconnector_transaction_view, msconnector_request, msconnector_response, msconnector_intervention | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/transaction.hpp` | header | transaction view helpers | MSCONNECTOR_TRANSACTION_HPP, msconnector_transaction_view, msconnector_transaction_state, msconnector_decision, msconnector_phase, msconnector_phase_name | Common SDK and adopting connectors | C++ facade |
| `common/include/msconnector/transaction_id.h` | header | transaction ID source/evaluation helpers | MSCONNECTOR_TRANSACTION_ID_H, msconnector_transaction_id_source, MSCONNECTOR_TRANSACTION_ID_SOURCE_NONE, MSCONNECTOR_TRANSACTION_ID_SOURCE_STATIC, MSCONNECTOR_TRANSACTION_ID_SOURCE_EXPR, MSCONNECTOR_TRANSACTION_ID_SOURCE_HOST, MSCONNECTOR_TRANSACTION_ID_SOURCE_HEADER, MSCONNECTOR_TRANSACTION_ID_SOURCE_FALLBACK | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/include/msconnector/transaction_state.h` | header | transaction phase-state helpers | MSCONNECTOR_TRANSACTION_STATE_H, msconnector_transaction_state, msconnector_transaction_state_init, msconnector_transaction_state_mark_phase, msconnector_phase, msconnector_transaction_state_phase_processed, msconnector_phase_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/README.md` | doc | notes for common source layout | macros / declarations | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/adapter.c` | source | adapter integration object and common adapter lifecycle helpers | msconnector_adapter_init, msconnector_adapter, msconnector_adapter_has_metadata, msconnector_adapter_has_capabilities, msconnector_adapter_supports_phase, msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_REQUEST_HEADERS | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/adapter_contract.c` | source | adapter contract validation declarations/implementation | msconnector_adapter_contract_result, msconnector_capabilities, msconnector_capability_flag, msconnector_capability_flags, msconnector_adapter, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/adapter_metadata.c` | source | adapter metadata and origin/capability completeness checks | msconnector_adapter_metadata_init, msconnector_adapter_metadata, MSCONNECTOR_CAPABILITY_NONE, msconnector_adapter_metadata_is_complete | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/artifact_layout.c` | source | standard artifact names for run outputs | msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log, msconnector_artifact_name_runtime_stdout_log, msconnector_artifact_name_runtime_stderr_log, msconnector_artifact_name_server_config, msconnector_artifact_name_connector_config | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/artifacts.c` | source | default artifact path helpers | msconnector_artifact_paths_init, msconnector_artifact_paths, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/block_statuses.c` | source | allowed/default block and error status helpers | msconnector_block_status_is_allowed, msconnector_http_status_is_block_response, msconnector_block_status_normalize, MSCONNECTOR_DEFAULT_BLOCK_STATUS, msconnector_http_status_is_valid, MSCONNECTOR_DEFAULT_ERROR_STATUS, msconnector_http_status_name, msconnector_http_status_info_find | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/blocking.c` | source | blocking policy/action helpers | msconnector_block_action_name, msconnector_block_action, MSCONNECTOR_BLOCK_ACTION_DENY, MSCONNECTOR_BLOCK_ACTION_REDIRECT, MSCONNECTOR_BLOCK_ACTION_DROP, MSCONNECTOR_BLOCK_ACTION_LOG_ONLY, MSCONNECTOR_BLOCK_ACTION_ABORT_CONNECTION, msconnector_block_action_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/body_policy.c` | source | body handling policy model | msconnector_body_policy_init, msconnector_body_policy, MSCONNECTOR_BODY_MODE_NONE, msconnector_body_mode_name, msconnector_body_mode, MSCONNECTOR_BODY_MODE_BUFFERED, MSCONNECTOR_BODY_MODE_STREAMING, msconnector_body_mode_is_supported | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/build_contract.c` | source | build target naming and C-standard contract helpers | msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/capabilities.c` | source | capability flags and capability lookup helpers | msconnector_capability_flag, MSCONNECTOR_CAPABILITY_NONE, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED, MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING, MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS, MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/capability_matrix.c` | source | capability-to-required-test mapping | msconnector_capability_required_test, msconnector_capability_flag, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED, MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING, MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS, MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/config.c` | source | connector-neutral configuration object, defaults, merge and validation | msconnector_bool_option, MSCONNECTOR_BOOL_UNSET, msconnector_phase4_mode, MSCONNECTOR_PHASE4_MODE_UNSET, msconnector_config, MSCONNECTOR_BOOL_ON, msconnector_block_status_is_allowed, msconnector_http_status_is_valid | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/config_parser.c` | source | parsers for booleans, phase4 mode, sizes, HTTP status and content-type tokens | msconnector_parse_bool, msconnector_bool_option, MSCONNECTOR_BOOL_ON, MSCONNECTOR_BOOL_OFF, msconnector_parse_phase4_mode, msconnector_phase4_mode, MSCONNECTOR_PHASE4_MODE_MINIMAL, MSCONNECTOR_PHASE4_MODE_SAFE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/connector_manifest.c` | source | connector manifest JSON metadata helpers | msconnector_json_escape, msconnector_connector_manifest_init, msconnector_connector_manifest, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_adapter_metadata_is_complete, msconnector_connector_manifest_write_json | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/crs.c` | source | CRS configuration/mode helpers | msconnector_crs_config_init, msconnector_crs_config, MSCONNECTOR_CRS_DISABLED, msconnector_crs_mode_name, msconnector_crs_mode, MSCONNECTOR_CRS_EXTERNAL_PATH, MSCONNECTOR_CRS_BUNDLED_PATH, MSCONNECTOR_CRS_TEST_FIXTURE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/decision.c` | source | inspection decision model | msconnector_decision_kind, MSCONNECTOR_DECISION_KIND_ALLOW, MSCONNECTOR_DECISION_KIND_LOG_ONLY, MSCONNECTOR_DECISION_KIND_DENY, MSCONNECTOR_DECISION_KIND_REDIRECT, MSCONNECTOR_DECISION_KIND_DROP, MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT, MSCONNECTOR_DECISION_KIND_ERROR | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/decision_action.c` | source | decision-to-action mapping helpers | msconnector_decision_action_name, msconnector_decision_action, MSCONNECTOR_DECISION_ACTION_ALLOW, MSCONNECTOR_DECISION_ACTION_DENY, MSCONNECTOR_DECISION_ACTION_REDIRECT, MSCONNECTOR_DECISION_ACTION_DROP, MSCONNECTOR_DECISION_ACTION_LOG_ONLY, MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/directive_adapter.c` | source | common directive adapter catalog and validation | msconnector_directive_adapter_entry, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_ARG_RAW, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_RULES_REMOTE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/directive_spec.c` | source | global directive specification catalog | msconnector_directive_spec, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_VALUE_BOOL, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_VALUE_STRING, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_VALUE_PATH, MSCONNECTOR_DIRECTIVE_RULES_REMOTE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/dos_guard.c` | source | request/response DoS guard checks | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_dos_guard_check_request, msconnector_request, msconnector_resource_limits, msconnector_error_init, msconnector_resource_limits_validate | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/error.c` | source | common error code and message model | msconnector_error_init, msconnector_error, MSCONNECTOR_ERROR_NONE, msconnector_error_set, msconnector_error_code, msconnector_error_code_name, MSCONNECTOR_ERROR_INVALID_CONFIG, MSCONNECTOR_ERROR_RULE_PARSE_FAILED | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/event.c` | source | event data model | msconnector_event_json_text_index, msconnector_event_json_status_index, msconnector_event_json_flag_index, msconnector_event_json_parts, msconnector_json_escape, msconnector_event_default_message | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/event_jsonl.c` | source | JSONL event serialization | msconnector_event_write_jsonl_line, msconnector_event, msconnector_event_write_json_ex | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/flow_guard.c` | source | phase/flow guard state machine | msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_LOGGING, msconnector_flow_guard_init, msconnector_flow_guard, msconnector_flow_guard_can_enter_phase, MSCONNECTOR_FLOW_GUARD_INVALID, MSCONNECTOR_FLOW_GUARD_IMMUTABLE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/generic_mapper.c` | source | generic request/response mapper for starter connectors | msconnector_generic_config_init, msconnector_config, msconnector_config_init, msconnector_generic_map_request, msconnector_generic_request_source, msconnector_request_mapper_contract, msconnector_request, msconnector_request_init | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/headers.c` | source | case-insensitive header lookup helpers | msconnector_header_name_is, msconnector_header_name_equals, msconnector_header, msconnector_headers_find_first, msconnector_headers_find, msconnector_headers_find_last, msconnector_headers_count_name, msconnector_headers_find_value | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/http_status.c` | source | HTTP status validation/classification helpers | MSCONNECTOR_HTTP_STATUS_MIN, MSCONNECTOR_HTTP_STATUS_MAX, msconnector_http_status_info, MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS, MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION, MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR, msconnector_http_status_is_valid | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/integrity_event.c` | source | integrity metadata helpers based on non-cryptographic hashes | msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/intervention.c` | source | intervention/blocking result helpers | msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/json_escape.c` | source | JSON string escaping helper | msconnector_json_escape | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/late_intervention.c` | source | late-intervention policy helpers | msconnector_late_intervention_policy_init, msconnector_late_intervention_policy, MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY, MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION, msconnector_late_intervention_action_name, msconnector_late_intervention_action, MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE, msconnector_late_intervention_resolve | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/lifecycle_status.c` | source | build/runtime/verification status names | msconnector_build_status_name, msconnector_build_status, MSCONNECTOR_BUILD_STATUS_NOT_STARTED, MSCONNECTOR_BUILD_STATUS_STARTER, MSCONNECTOR_BUILD_STATUS_COMPILES, MSCONNECTOR_BUILD_STATUS_LINKS, MSCONNECTOR_BUILD_STATUS_RUNTIME_READY, msconnector_runtime_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/limits.c` | source | compiled-in limit constants | msconnector_limit_header_count, MSCONNECTOR_MAX_HEADER_COUNT, msconnector_limit_header_name_length, MSCONNECTOR_MAX_HEADER_NAME_LENGTH, msconnector_limit_header_value_length, MSCONNECTOR_MAX_HEADER_VALUE_LENGTH, msconnector_limit_total_header_bytes, MSCONNECTOR_MAX_TOTAL_HEADER_BYTES | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/log_sanitize.c` | source | log redaction/sanitization helpers | msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/memory.c` | source | checked allocation and allocator callbacks | msconnector_allocator_init, msconnector_allocator, msconnector_alloc_checked, msconnector_free_checked, msconnector_allocator_within_limit | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/modsecurity_engine.c` | source | connector-neutral ModSecurity engine operation table | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_modsecurity_transaction, MSCONNECTOR_ERROR_INTERNAL, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, msconnector_modsecurity_engine_init, msconnector_modsecurity_engine | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/origin.c` | source | source/origin metadata helpers | msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/origin_governance.c` | source | origin governance completeness helpers | msconnector_origin_governance_init, msconnector_origin_governance, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/path_policy.c` | source | path validation helpers | msconnector_path_is_empty, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/redaction.c` | source | string redaction helpers | msconnector_redacted_string, msconnector_redact_copy | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/request_helpers.c` | source | request initialization/validation helpers | msconnector_header, msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_resource_limits, msconnector_resource_limits_headers_ok, msconnector_resource_limits_body_ok | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/request_mapper_contract.c` | source | request mapper contract validation | msconnector_mapper_requirement, MSCONNECTOR_MAPPER_REQUIRED, MSCONNECTOR_MAPPER_UNSUPPORTED, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract, MSCONNECTOR_MAPPER_OPTIONAL, msconnector_request_mapper_contract_validate, msconnector_request_mapper_validate_output | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/resource_limits.c` | source | runtime resource limits and validators | msconnector_resource_limits_init, msconnector_resource_limits, MSCONNECTOR_MAX_HEADER_COUNT, MSCONNECTOR_MAX_HEADER_NAME_LENGTH, MSCONNECTOR_MAX_HEADER_VALUE_LENGTH, MSCONNECTOR_MAX_TOTAL_HEADER_BYTES, MSCONNECTOR_MAX_BODY_BUFFER_SIZE, MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/response_helpers.c` | source | response initialization/validation helpers | msconnector_header, msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_http_status_is_valid, msconnector_response_validate_with_limits, msconnector_resource_limits, msconnector_resource_limits_headers_ok | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/response_mapper_contract.c` | source | response mapper contract validation | msconnector_mapper_requirement, MSCONNECTOR_MAPPER_REQUIRED, MSCONNECTOR_MAPPER_UNSUPPORTED, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract, MSCONNECTOR_MAPPER_OPTIONAL, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_error.c` | source | rule-load error helpers | msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_error_set, MSCONNECTOR_ERROR_RULE_PARSE_FAILED, msconnector_error_default_message, msconnector_rule_error_set_load_failed, MSCONNECTOR_ERROR_RULE_LOAD_FAILED, msconnector_rule_error_clear | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_event.c` | source | rule-load event helpers | msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_event_init, MSCONNECTOR_STATUS_OK, msconnector_rule_load_event, msconnector_rule_error_event, msconnector_error | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_id.c` | source | rule ID copy/extraction/validation helpers | msconnector_rule_id_validate, msconnector_rule_id_copy, msconnector_rule_id_extract_from_message | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_loader.c` | source | rule loading backend contract | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_rule_loader_init, msconnector_rule_loader, msconnector_rule_loader_backend, msconnector_rule_load_stats_init, msconnector_rule_loader_add_inline | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/rule_merge.c` | source | rule collection merge helpers | msconnector_rule_collection_init, msconnector_rule_collection, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/runtime_paths.c` | source | runtime path join helper | msconnector_runtime_path_join, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/runtime_report.c` | source | runtime report JSON helper | msconnector_json_escape, msconnector_runtime_report_init, msconnector_runtime_report, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_runtime_report_write_json, msconnector_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/status.c` | source | common PASS/FAIL/BLOCKED-like status helpers | msconnector_status_name, msconnector_status, MSCONNECTOR_STATUS_OK, MSCONNECTOR_STATUS_ERROR, MSCONNECTOR_STATUS_BLOCKED, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_status_from_result | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/test_result.c` | source | test result model | msconnector_test_result_init, msconnector_test_result, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_test_result_passed, MSCONNECTOR_STATUS_OK | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/test_result_json.c` | source | test result JSON writer | msconnector_json_escape, msconnector_test_result_write_json, msconnector_test_result, msconnector_status_name | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/transaction.c` | source | transaction view helpers | msconnector_decision_kind, msconnector_status, MSCONNECTOR_STATUS_BLOCKED, MSCONNECTOR_DECISION_KIND_DENY, MSCONNECTOR_STATUS_ERROR, MSCONNECTOR_DECISION_KIND_ERROR, MSCONNECTOR_STATUS_UNSUPPORTED, MSCONNECTOR_DECISION_KIND_UNSUPPORTED | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/transaction_id.c` | source | transaction ID source/evaluation helpers | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_transaction_id_result, msconnector_transaction_id_validate, msconnector_transaction_id_copy, msconnector_transaction_id_source, MSCONNECTOR_ERROR_INVALID_CONFIG | Common SDK and adopting connectors | connector-neutral; not runtime evidence |
| `common/src/transaction_state.c` | source | transaction phase-state helpers | msconnector_transaction_state_init, msconnector_transaction_state, msconnector_transaction_state_mark_phase, msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_URI, MSCONNECTOR_PHASE_REQUEST_HEADERS, MSCONNECTOR_PHASE_REQUEST_BODY | Common SDK and adopting connectors | connector-neutral; not runtime evidence |

## Common SDK: modules and responsibilities

- Configuration, directives and parsers define shared vocabulary, defaults, merge behavior and validation. They are connector-neutral because they store semantic values without Apache, NGINX, HAProxy, Envoy, Traefik or lighttpd types. They do not prove host syntax parity.
- Request, response, headers and mapper contracts define neutral HTTP shapes and validation. They do not prove live request or response-body processing.
- Decision, intervention, status, error and event JSONL helpers define shared outcome semantics and serialization. They are not append-only or cryptographic evidence.
- Resource limits, body policy, DoS guard, flow guard and integrity metadata are guardrails. They do not claim runtime secure behavior.
- Rule loading, merge, rule ID and CRS helpers define contracts and metadata. They do not prove CRS execution.
- Adapter metadata, capabilities, origin governance and manifests identify provenance and capability claims. Metadata must remain conservative until evidence changes.

## Config, Directives and Parser Model

`msconnector_config` stores connector-neutral options: enable flag, error-log flag, inline/file/remote rules, static or expression transaction ID, phase-4 mode, content-type file, phase-4 log path, body limit and default statuses.

`msconnector_config_init` initializes values to unset/zero/null. `msconnector_config_apply_defaults` fills only unset values. `msconnector_config_merge` merges parent and child values and then applies defaults; applying defaults too early would break parent/child inheritance. `msconnector_config_validate` validates enum ranges, complete remote-rule key/URL pairs, mutual exclusion of `transaction_id` and `transaction_id_expr`, allowed block statuses and valid error statuses.

Parser helpers use `1 = success` and `0 = failure`: `msconnector_parse_bool`, `msconnector_parse_phase4_mode`, `msconnector_parse_size`, `msconnector_parse_http_status` and `msconnector_validate_content_type_token`. The bool parser accepts `on/off`, `true/false`, `1/0` and `yes/no`. Phase-4 mode accepts `minimal`, `safe` and `strict`. Size parsing accepts positive decimal byte values. HTTP status parsing requires a valid status. Content-type token validation requires one slash, non-empty type and subtype, no control characters and no semicolon. Transaction-ID expression parsing remains connector-specific.

## Allowed config/directive vocabulary

| Config / Directive | Common macro | Type | Allowed values | Default | Parser / validator | Affected connectors | Notes |
|---|---|---|---|---|---|---|---|
| `modsecurity` | `MSCONNECTOR_DIRECTIVE_MODSECURITY` | bool | spec: `on|off`; parser also accepts `true|false|1|0|yes|no` | `off` | `msconnector_parse_bool`, `msconnector_config_validate` | Connector-specific mapping; consult each capability manifest | Enables semantic processing only; no production claim. |
| `modsecurity_rules` | `MSCONNECTOR_DIRECTIVE_RULES` | string/raw | inline rules text | none | directive adapter and connector rule loading | connector-dependent | Rule text does not prove CRS/runtime execution. |
| `modsecurity_rules_file` | `MSCONNECTOR_DIRECTIVE_RULES_FILE` | path | runtime path | none | directive adapter, path policy where used | connector-dependent | Path validity is environment-specific. |
| `modsecurity_rules_remote` | `MSCONNECTOR_DIRECTIVE_RULES_REMOTE` | string pair | `key url` | none | config requires key and URL together | connector-dependent | Incomplete remote pair is invalid. |
| `modsecurity_transaction_id` | `MSCONNECTOR_DIRECTIVE_TRANSACTION_ID` | string | static ID | none | transaction ID helpers; config mutual exclusion | connector-dependent | Mutually exclusive with expression. |
| `modsecurity_transaction_id_expr` | `MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR` | string | connector-parsed expression | none | connector-specific parser; config mutual exclusion | Apache/NGINX may differ; Envoy/Traefik/lighttpd connector-gap | Apache-style expressions must not be treated as NGINX syntax. |
| `modsecurity_use_error_log` | `MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG` | bool | spec: `on|off`; parser also accepts aliases | `on` | `msconnector_parse_bool` | connector-dependent | Common config flag only. |
| `modsecurity_phase4_mode` | `MSCONNECTOR_DIRECTIVE_PHASE4_MODE` | enum | `minimal|safe|strict` | `safe` | `msconnector_parse_phase4_mode` | connector-dependent; starter connectors not verified | Response-body policy model; not response-body verification. |
| `modsecurity_phase4_content_types_file` | `MSCONNECTOR_DIRECTIVE_PHASE4_CONTENT_TYPES_FILE` | path | file with valid content-type tokens | none | content-type token parser and connector file handling | connector-dependent | Strictness is connector/evidence dependent. |
| `modsecurity_phase4_log` | `MSCONNECTOR_DIRECTIVE_PHASE4_LOG` | path | log path | none | directive adapter and path policy where used | connector-dependent | Log path does not prove body handling. |
| `modsecurity_phase4_body_limit` | `MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT` | size | positive decimal bytes | `1048576` | `msconnector_parse_size` | connector-dependent | Truncation metadata requires connector implementation/evidence. |
| `default_block_status` | config field | HTTP status | allowed block statuses | `403` | `msconnector_block_status_is_allowed` | common config consumers | Config field, not a macro in `directives.h`. |
| `default_error_status` | config field | HTTP error status | valid HTTP error status | `500` | HTTP status validation and error-status check | common config consumers | Config field, not a macro in `directives.h`. |
| `unsupported_status` | config field | HTTP error status | valid HTTP error status | `501` | HTTP status validation and error-status check | common config consumers | Config field, not a macro in `directives.h`. |
| CRS setup / CRS mode / fixture mode | CRS/framework metadata | mode/path/string | repository/framework-specific | unknown | `msconnector_crs_config_validate` and framework scripts where used | framework/connector-dependent | Treat as `requires runtime evidence` unless a current report proves the exact run. |

## Request/response mapping

Request mapping owns method, URI, protocol, endpoints, headers, body metadata and transaction identifiers in connector-neutral form. Response mapping owns status, protocol, headers, content-type/body metadata and phase-4 policy state. Mapper contracts define validation and ownership expectations. Host server objects remain outside `common/`.

## Decision, intervention, status and event model

Common decision/action helpers express allow/block/error/unsupported-like outcomes. Intervention helpers normalize blocking results. Status helpers map outcomes to common status names. Event and JSONL helpers serialize per-run evidence. These outputs are not append-only or cryptographically signed unless future code implements and proves that explicitly.

## Resource limits, DoS guard, flow guard and integrity

Resource limits centralize maximum sizes and counts. DoS guard and flow guard check neutral request/response state and phase transitions. Integrity events carry metadata and non-cryptographic hashes. This is governance and safety modeling, not a runtime secure, tamper-proof or cryptographic-integrity claim.

## C Language and Standards

The Common SDK is designed for C17. C17 is the hard required standard when the compiler and required headers exist. C23 is optional. future-C (`c2y`/`gnu2y`) is optional. `c20` and `c26` are not valid C standard modes and should be SKIPPED/INFO if targets exist. Exit 77 means BLOCKED/SKIPPED because the environment, headers, compiler or optional profile is unavailable. Real compile failures must not be hidden as Exit 77.

| Connector group | C17 | C23 | future-C | Header requirements | Exit-77 behavior |
|---|---|---|---|---|---|
| Common | required when compiler exists | optional | optional | Common headers | only environment/unsupported-profile skips |
| Apache | hard when APXS/APR/libmodsecurity headers exist | optional | optional | APXS/APR/libmodsecurity | missing headers may block; compile errors fail |
| NGINX | hard when NGINX/libmodsecurity headers exist | optional | optional | NGINX source/include roots, libmodsecurity | missing roots/headers may block |
| HAProxy | hard when HAProxy/libmodsecurity context exists | optional | optional | HAProxy/SPOE/SPOP context and common includes | missing headers may block |
| Envoy, Traefik, lighttpd | C17 native/service paths | optional | optional | connector and Common headers | targeted runtime path; canonical baseline pending |

## CI, contract and governance checks

| Check / Target | Script | Purpose | Scope | Hard or optional | Exit-77 possible? |
|---|---|---|---|---|---|
| `check-common-helpers` | `ci/check-common-helpers.sh` | Common helper compile/static checks | common | hard when env exists | possible for env blockers |
| `check-common-sdk-contract` | `ci/check-common-sdk-contract.py` | Common SDK API/contract governance | common | hard | usually no |
| `check-common-security-contract` | `ci/check-common-security-contract.py` | security/data contract governance | common | hard | script-specific |
| `check-common-memory-safety` | `ci/check-common-memory-safety.sh` | ownership/memory contract checks | common | hard | script-specific |
| `check-common-flow-integrity` | `ci/check-common-flow-integrity.py` | flow/integrity contract checks | common | hard | script-specific |
| `check-adapter-contracts` | `ci/check-adapter-contracts.py` | adapter metadata/contract checks | connectors | hard | script-specific |
| `check-directive-parity` | `ci/check-directive-parity.py` | common directive parity across connectors | common/connectors | hard | script-specific |
| connector adoption targets | `ci/check-*-common-adoption.py` | adoption/static governance | connectors | hard | script-specific |
| connector C-standard targets | `ci/check-*-c-standards.sh`, `ci/check-*-c-standard-wiring.py` | C17/C23/future-C compile profile checks | connectors | C17 hard, optional profiles optional | yes |
| `check-bilingual-docs` | `ci/check-bilingual-docs.py` | bilingual documentation and link governance | docs/reports | hard for docs | may fail on missing companion docs or missing framework links |

## Makefile Targets: What can be done with `make`?

The Makefile is the operational index for setup, linting, Common SDK checks, connector checks, C-standard profiles, runtime/starter smokes, matrix/report generation, framework integration and bootstrap workflows. A target proves only what its script checks. Compile-only and structure-only targets do not create runtime evidence.

### Target categories

- General targets: setup, dependency fetch, doctor, lint and quick/codex checks.
- Common SDK targets: helper compilation, SDK/security/memory/flow contracts, adapter contracts and directive parity.
- Apache, NGINX and HAProxy targets: common adoption, C-standard wiring and C17/C23/future-C checks, plus smoke/test wrappers.
- Envoy, Traefik, and lighttpd targets: separate build, config-load,
  request-free start, targeted runtime, capability, and evidence checks.
- Framework/test-framework targets: matrix, verified report, MRTS and smoke/test workflows. These may block if `modules/ModSecurity-test-Framework` or runtime components are missing.
- Report/generator targets: generate or check reports and matrices. They do not automatically imply verified runtime behavior.

### Complete Makefile target table

| Makefile target | Purpose | Scope | Requirements | Hard/optional | Exit-77/BLOCKED possible? | Notes |
|---|---|---|---|---|---|---|
| `check-framework` | Runs `check-framework` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-framework-fixture-syntax` | Runs `check-framework-fixture-syntax` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-framework-fixture-syntax.py |
| `prepare-runtime-components` | Runs `prepare-runtime-components` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `prepare-envoy-runtime` | Runs `prepare-envoy-runtime` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | script-dependent | Script/recipe: ci/prepare-envoy-runtime.sh |
| `prepare-traefik-runtime` | Runs `prepare-traefik-runtime` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | script-dependent | Script/recipe: ci/prepare-traefik-runtime.sh |
| `prepare-lighttpd-runtime` | Runs `prepare-lighttpd-runtime` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | script-dependent | Script/recipe: ci/prepare-lighttpd-runtime.sh |
| `prepare-lighttpd-runtime-build` | Runs `prepare-lighttpd-runtime-build` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `prepare-open-connector-runtimes` | Runs `prepare-open-connector-runtimes` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `runtime-components-inventory` | Runs `runtime-components-inventory` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/runtime-components-inventory.sh |
| `runtime-components-sources` | Runs `runtime-components-sources` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/runtime-components-inventory.sh |
| `check-runtime-producer-readiness` | Runs `check-runtime-producer-readiness` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-runtime-producer-readiness.py |
| `check-runtime-path-policy` | Runs `check-runtime-path-policy` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-runtime-path-policy.py |
| `check-bilingual-docs` | Runs `check-bilingual-docs` (Other). | Other | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-bilingual-docs.py |
| `refresh-connector-reports` | Runs `refresh-connector-reports` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/refresh-connector-reports.py |
| `refresh-all-reports` | Runs `refresh-all-reports` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-generated-report-layout` | Runs `check-generated-report-layout` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-generated-report-layout.py |
| `report-governance` | Runs `report-governance` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-generated-report-layout.py |
| `verified-report-evidence-gate` | Runs `verified-report-evidence-gate` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-generated-report-layout | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `generate-system-environment-proof` | Runs `generate-system-environment-proof` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-system-environment-proof.py |
| `generate-verified-runtime-mismatch-analysis` | Runs `generate-verified-runtime-mismatch-analysis` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/generate-verified-runtime-mismatch-analysis.py |
| `generate-remaining-critical-batch-analysis` | Runs `generate-remaining-critical-batch-analysis` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-remaining-critical-batch-analysis.py |
| `generate-native-semantics-comparison` | Runs `generate-native-semantics-comparison` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/run-native-case-comparison.py |
| `prove-generated-reports` | Runs `prove-generated-reports` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `verified-runtime-producers` | Runs `verified-runtime-producers` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `verified-report-producers` | Runs `verified-report-producers` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | verified-runtime-producers | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: dependency target / see Makefile |
| `verified-report-refresh` | Runs `verified-report-refresh` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `verified-report-consumers` | Runs `verified-report-consumers` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `verified-report-checks` | Runs `verified-report-checks` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `verified-report-run` | Runs `verified-report-run` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `verified-report-run-soft` | Runs `verified-report-run-soft` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `verified-report-run-smoke` | Runs `verified-report-run-smoke` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `verified-full-matrix-job` | Runs `verified-full-matrix-job` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `verified-case` | Runs `verified-case` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `verified-native-case` | Runs `verified-native-case` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-native-case-comparison.py |
| `verified-nginx-case` | Runs `verified-nginx-case` (NGINX). | NGINX | check-framework prepare-runtime-components | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `verified-apache-case` | Runs `verified-apache-case` (Apache). | Apache | check-framework prepare-runtime-components | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `verified-haproxy-case` | Runs `verified-haproxy-case` (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `verified-full-matrix-resume` | Runs `verified-full-matrix-resume` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-verified-report-run.py |
| `smoke-common` | Runs `smoke-common` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-connector-smokes.sh |
| `smoke-apache` | Runs `smoke-apache` (Apache). | Apache | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-apache-smoke.sh |
| `smoke-nginx` | Runs `smoke-nginx` (NGINX). | NGINX | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-nginx-smoke.sh |
| `smoke-envoy` | Runs `smoke-envoy` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-envoy-smoke.sh |
| `smoke-envoy-modsecurity` | Runs `smoke-envoy-modsecurity` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-envoy-request-body` | Runs `smoke-envoy-request-body` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-envoy-crs` | Runs `smoke-envoy-crs` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-envoy-crs-secondary` | Runs `smoke-envoy-crs-secondary` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-haproxy` | Runs `smoke-haproxy` (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-haproxy-smoke.sh |
| `smoke-lighttpd` | Runs `smoke-lighttpd` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-lighttpd-smoke.sh |
| `smoke-lighttpd-modsecurity` | Runs `smoke-lighttpd-modsecurity` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-lighttpd-request-body` | Runs `smoke-lighttpd-request-body` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-lighttpd-crs` | Runs `smoke-lighttpd-crs` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-lighttpd-crs-secondary` | Runs `smoke-lighttpd-crs-secondary` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-traefik` | Runs `smoke-traefik` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-traefik-smoke.sh |
| `smoke-traefik-modsecurity` | Runs `smoke-traefik-modsecurity` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-traefik-request-body` | Runs `smoke-traefik-request-body` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-traefik-crs` | Runs `smoke-traefik-crs` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-traefik-crs-secondary` | Runs `smoke-traefik-crs-secondary` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-open-connectors-crs` | Runs `smoke-open-connectors-crs` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-open-connectors-request-body` | Runs `smoke-open-connectors-request-body` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-open-connectors-crs-secondary` | Runs `smoke-open-connectors-crs-secondary` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-new-connectors` | Runs `smoke-new-connectors` (Remaining connectors). | Remaining connectors | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `smoke-all` | Runs `smoke-all` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-connector-smokes.sh |
| `test` | Runs `test` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | test-no-crs test-with-crs | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: dependency target / see Makefile |
| `test-no-crs` | Runs `test-no-crs` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/common.sh, ci/run-connector-smokes.sh |
| `test-with-crs` | Runs `test-with-crs` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/common.sh, ci/fetch-crs.sh, ci/prepare-crs.sh, ci/run-connector-smokes.sh |
| `mrts-generate` | Runs `mrts-generate` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `mrts-load` | Runs `mrts-load` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `mrts-import` | Runs `mrts-import` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `test-no-mrts` | Runs `test-no-mrts` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `test-with-mrts` | Runs `test-with-mrts` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `test-with-mrts-feature-demo` | Runs `test-with-mrts-feature-demo` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `test-mrts-matrix` | Runs `test-mrts-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `mrts-ftw` | Runs `mrts-ftw` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `runtime-matrix` | Runs `runtime-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-runtime-matrix.sh |
| `runtime-matrix-all` | Runs `runtime-matrix-all` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-runtime-matrix.sh |
| `runtime-matrix-all-runtime` | Runs `runtime-matrix-all-runtime` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-runtime-matrix.sh |
| `runtime-matrix-haproxy` | Runs `runtime-matrix-haproxy` (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/composite | script-dependent | Script/recipe: ci/run-haproxy-runtime-matrix.sh |
| `full-mrts-runtime-matrix` | Runs `full-mrts-runtime-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-full-mrts-runtime-matrix.sh |
| `mrts-only-full-run` | Runs `mrts-only-full-run` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | full-mrts-runtime-matrix | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: dependency target / see Makefile |
| `full-runtime-matrix` | Runs `full-runtime-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | full-matrix-parallel | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: dependency target / see Makefile |
| `full-matrix-parallel` | Runs `full-matrix-parallel` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-full-matrix-parallel.sh |
| `full-matrix-parallel-runtime` | Runs `full-matrix-parallel-runtime` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-full-matrix-parallel.sh |
| `full-matrix-single-job-runtime` | Runs `full-matrix-single-job-runtime` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `full-matrix-resume-runtime` | Runs `full-matrix-resume-runtime` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-full-matrix-resume.py |
| `generate-full-runtime-matrix` | Runs `generate-full-runtime-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/generate-full-runtime-matrix.py |
| `generate-full-matrix-job-completeness` | Runs `generate-full-matrix-job-completeness` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/generate-full-matrix-job-completeness.py |
| `generate-nginx-mrts-http500-cluster-analysis` | Runs `generate-nginx-mrts-http500-cluster-analysis` (NGINX). | NGINX | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-nginx-mrts-http500-cluster-analysis.py |
| `generate-work-queue` | Runs `generate-work-queue` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-connector-work-queue.py, ci/generate-phase-work-queue.py, ci/generate-nolog-audit-evidence-analysis.py |
| `generate-phase-work-queue` | Runs `generate-phase-work-queue` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-phase-work-queue.py, ci/generate-nolog-audit-evidence-analysis.py, ci/generate-response-header-hook-analysis.py |
| `generate-nolog-audit-evidence-analysis` | Runs `generate-nolog-audit-evidence-analysis` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-nolog-audit-evidence-analysis.py |
| `generate-response-header-hook-analysis` | Runs `generate-response-header-hook-analysis` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-response-header-hook-analysis.py |
| `generate-phase4-hard-abort-capability` | Runs `generate-phase4-hard-abort-capability` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-phase4-hard-abort-capability.py |
| `generate-intervention-blocking-analysis` | Runs `generate-intervention-blocking-analysis` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-intervention-blocking-analysis.py |
| `generate-no-mrts-intervention-nomatch-analysis` | Runs `generate-no-mrts-intervention-nomatch-analysis` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/generate-no-mrts-intervention-nomatch-analysis.py |
| `generate-body-processor-analysis` | Runs `generate-body-processor-analysis` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-body-processor-analysis.py |
| `generate-rule-chain-semantics-analysis` | Runs `generate-rule-chain-semantics-analysis` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-rule-chain-semantics-analysis.py |
| `generate-final-consistency-audit` | Runs `generate-final-consistency-audit` (Other). | Other | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-final-consistency-audit.py |
| `generate-remaining-failure-analysis` | Runs `generate-remaining-failure-analysis` (Remaining connectors). | Remaining connectors | check-framework | optional/composite | script-dependent | Script/recipe: ci/generate-remaining-failure-analysis.py |
| `mrts-native-full-run` | Runs `mrts-native-full-run` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-mrts-native-full.sh |
| `mrts-native-full-run-runtime` | Runs `mrts-native-full-run-runtime` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-mrts-native-full.sh |
| `mrts-native-apache-full` | Runs `mrts-native-apache-full` (Apache). | Apache | check-framework prepare-runtime-components | optional/composite | script-dependent | Script/recipe: ci/run-mrts-native-full.sh |
| `mrts-native-nginx-pr24-full` | Runs `mrts-native-nginx-pr24-full` (NGINX). | NGINX | check-framework prepare-runtime-components | optional/composite | script-dependent | Script/recipe: ci/run-mrts-native-full.sh |
| `mrts-upstream-infra-check` | Runs `mrts-upstream-infra-check` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `test-haproxy-no-crs` | Runs `test-haproxy-no-crs` (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-haproxy-runtime-matrix.sh |
| `test-haproxy-with-crs` | Runs `test-haproxy-with-crs` (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/run-haproxy-runtime-matrix.sh |
| `probe-response-body` | Runs `probe-response-body` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/probe-response-body-blocking.sh |
| `connector-starter-checks` | Runs `connector-starter-checks` (Other). | Other | check-framework prepare-runtime-components | optional/composite | script-dependent | Script/recipe: ci/run-connector-starter-checks.sh |
| `check-remaining-connectors-common-adoption` | Runs `check-remaining-connectors-common-adoption` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-remaining-connectors-common-adoption.py |
| `check-remaining-connectors-c-standard-wiring` | Runs `check-remaining-connectors-c-standard-wiring` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-remaining-connectors-c-standard-wiring.py |
| `check-remaining-connectors-c-standards` | Runs `check-remaining-connectors-c-standards` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-c17` | Runs `check-remaining-connectors-c17` (Remaining connectors). | Remaining connectors | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-c17-lint` | Runs `check-remaining-connectors-c17-lint` (Remaining connectors). | Remaining connectors | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-c23` | Runs `check-remaining-connectors-c23` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-future-c` | Runs `check-remaining-connectors-future-c` (Remaining connectors). | Remaining connectors | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-remaining-connectors-c-standards.sh |
| `check-block-status-generator` | Runs `check-block-status-generator` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-block-status-generator.py |
| `check-apache-common-adoption` | Runs `check-apache-common-adoption` (Apache). | Apache | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-apache-common-adoption.py |
| `check-apache-c-standard-wiring` | Runs `check-apache-c-standard-wiring` (Apache). | Apache | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-apache-c-standard-wiring.py |
| `check-apache-c-standards` | Runs `check-apache-c-standards` (Apache). | Apache | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-apache-c-standards.sh |
| `check-apache-c17` | Runs `check-apache-c17` (Apache). | Apache | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-apache-c-standards.sh |
| `check-apache-c17-lint` | Runs `check-apache-c17-lint` (Apache). | Apache | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-apache-c-standards.sh |
| `check-apache-c23` | Runs `check-apache-c23` (Apache). | Apache | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-apache-c-standards.sh |
| `check-apache-future-c` | Runs `check-apache-future-c` (Apache). | Apache | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-apache-c-standards.sh |
| `check-apache-c20` | Runs `check-apache-c20` (Apache). | Apache | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-apache-c26` | Runs `check-apache-c26` (Apache). | Apache | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-nginx-common-adoption` | Runs `check-nginx-common-adoption` (NGINX). | NGINX | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-nginx-common-adoption.py |
| `check-nginx-c-standard-wiring` | Runs `check-nginx-c-standard-wiring` (NGINX). | NGINX | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-nginx-c-standard-wiring.py |
| `check-nginx-c-standards` | Runs `check-nginx-c-standards` (NGINX). | NGINX | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-nginx-c-standards.sh |
| `check-nginx-c17` | Runs `check-nginx-c17` (NGINX). | NGINX | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-nginx-c-standards.sh |
| `check-nginx-c17-lint` | Runs `check-nginx-c17-lint` (NGINX). | NGINX | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-nginx-c-standards.sh |
| `check-nginx-c23` | Runs `check-nginx-c23` (NGINX). | NGINX | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-nginx-c-standards.sh |
| `check-nginx-future-c` | Runs `check-nginx-future-c` (NGINX). | NGINX | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-nginx-c-standards.sh |
| `check-nginx-c20` | Runs `check-nginx-c20` (NGINX). | NGINX | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-nginx-c26` | Runs `check-nginx-c26` (NGINX). | NGINX | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-haproxy-common-adoption` | Runs `check-haproxy-common-adoption` (HAProxy). | HAProxy | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-haproxy-common-adoption.py |
| `check-haproxy-c-standard-wiring` | Runs `check-haproxy-c-standard-wiring` (HAProxy). | HAProxy | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-haproxy-c-standard-wiring.py |
| `check-haproxy-c-standards` | Runs `check-haproxy-c-standards` (HAProxy). | HAProxy | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c17` | Runs `check-haproxy-c17` (HAProxy). | HAProxy | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c17-lint` | Runs `check-haproxy-c17-lint` (HAProxy). | HAProxy | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c23` | Runs `check-haproxy-c23` (HAProxy). | HAProxy | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-haproxy-c-standards.sh |
| `check-haproxy-future-c` | Runs `check-haproxy-future-c` (HAProxy). | HAProxy | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c20` | Runs `check-haproxy-c20` (HAProxy). | HAProxy | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-haproxy-c26` | Runs `check-haproxy-c26` (HAProxy). | HAProxy | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-common-helpers` | Runs `check-common-helpers` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-common-helpers.sh |
| `check-common-helpers-c17` | Runs `check-common-helpers-c17` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | hard | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-common-helpers-c23` | Runs `check-common-helpers-c23` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/detect-c-standard.py |
| `check-common-helpers-future-c` | Runs `check-common-helpers-future-c` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/detect-c-standard.py |
| `check-common-helpers-c20` | Runs `check-common-helpers-c20` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-common-helpers-c26` | Runs `check-common-helpers-c26` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |
| `check-common-sdk-contract` | Runs `check-common-sdk-contract` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | hard | script-dependent | Script/recipe: ci/check-common-sdk-contract.py |
| `check-common-security-contract` | Runs `check-common-security-contract` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | hard | script-dependent | Script/recipe: ci/check-common-security-contract.py |
| `check-common-memory-safety` | Runs `check-common-memory-safety` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-common-memory-safety.sh |
| `check-common-flow-integrity` | Runs `check-common-flow-integrity` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | optional/composite | script-dependent | Script/recipe: ci/check-common-flow-integrity.py |
| `check-adapter-contracts` | Runs `check-adapter-contracts` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | hard | script-dependent | Script/recipe: ci/check-adapter-contracts.py |
| `check-directive-parity` | Runs `check-directive-parity` (Common SDK / contracts). | Common SDK / contracts | see Makefile recipe | hard | script-dependent | Script/recipe: ci/check-directive-parity.py |
| `lint` | Runs `lint` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | hard | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `summary` | Runs `summary` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/composite | script-dependent | Script/recipe: ci/summarize-results.py |
| `case-matrix` | Runs `case-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/write-case-matrix.py |
| `install-dev-deps` | Runs `install-dev-deps` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/composite | script-dependent | Script/recipe: ci/bootstrap-python.sh |
| `setup-dev` | Runs `setup-dev` (General setup / lint / bootstrap). | General setup / lint / bootstrap | install-dev-deps | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `fetch-modsecurity-v3` | Runs `fetch-modsecurity-v3` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/composite | script-dependent | Script/recipe: ci/fetch-smoke-sources.sh |
| `fetch-crs` | Runs `fetch-crs` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/composite | script-dependent | Script/recipe: ci/fetch-crs.sh |
| `prepare-crs` | Runs `prepare-crs` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/composite | script-dependent | Script/recipe: ci/prepare-crs.sh, ci/doctor.sh |
| `print-python` | Runs `print-python` (Other). | Other | see Makefile recipe | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `bootstrap-all` | Runs `bootstrap-all` (General setup / lint / bootstrap). | General setup / lint / bootstrap | setup-dev fetch-deps doctor | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `doctor-install-hints` | Runs `doctor-install-hints` (General setup / lint / bootstrap). | General setup / lint / bootstrap | see Makefile recipe | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `doctor-quick` | Runs `doctor-quick` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/composite | script-dependent | Script/recipe: ci/doctor.sh |
| `quick-all` | Runs `quick-all` (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/composite | script-dependent | Script/recipe: ci/quick-all.sh |
| `cloud-quick-check` | Runs `cloud-quick-check` (General setup / lint / bootstrap). | General setup / lint / bootstrap | setup-dev lint generate-test-matrix check-test-matrix quick-check | optional/composite | script-dependent | Script/recipe: Makefile composite / shell recipe |
| `generate-test-matrix` | Runs `generate-test-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: ci/ensure-test-matrix-language-switches.py |
| `check-test-matrix` | Runs `check-test-matrix` (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/composite | yes, for missing environment/headers/framework or optional profile | Script/recipe: Makefile composite / shell recipe |

### C17, C23 and future-C targets

`check-*-c17` targets are required when the relevant compiler and headers are present. `check-*-c23` targets are optional. `check-*-future-c` targets are optional and may use `c2y`/`gnu2y`. `check-*-c20` and `check-*-c26`, where present, are skip/info targets because c20/c26 are not valid C language modes. Exit 77 means a missing environment or unsupported optional profile; it must not hide real compile or contract failures.

## Common Makefile Commands

- `make check-common-helpers`: after common helper changes.
- `make check-common-sdk-contract`: after Common SDK API/header changes.
- `make check-adapter-contracts`: after adapter metadata/contract changes.
- `make check-directive-parity`: after directive/config/parser changes.
- `make check-apache-common-adoption && make check-apache-c17`: after Apache connector changes.
- `make check-nginx-common-adoption && make check-nginx-c17`: after NGINX connector changes.
- `make check-haproxy-common-adoption && make check-haproxy-c17`: after HAProxy connector changes.
- `make check-remaining-connectors-common-adoption && make check-remaining-connectors-c17`: after Envoy/Traefik/lighttpd starter changes; this remains compile/structure evidence only.
- `make lint`, `make quick-check`, `make codex-check`: aggregate validation, subject to framework/environment blockers.

## Exit Codes and BLOCKED/SKIPPED Behavior

- `0`: success.
- `1`, `2` or another non-zero value: real failure or usage error unless a script documents a different meaning.
- `77`: BLOCKED/SKIPPED due to missing environment, missing headers, missing compiler, missing framework input or unsupported optional C profile.

Exit 77 must not hide real compile or contract failures. Lint wrappers may translate environment-limited skips, but they must not hide real failures.

## Environment variables

| Variable | Use | Example | Scope |
|---|---|---|---|
| `CC` | Used by Makefile/CI scripts when set. | `CC=...` | build/check environment |
| `PYTHON` | Used by Makefile/CI scripts when set. | `PYTHON=...` | build/check environment |
| `BUILD_ROOT` | Used by Makefile/CI scripts when set. | `BUILD_ROOT=...` | build/check environment |
| `MSCONNECTOR_C_STD` | Used by Makefile/CI scripts when set. | `MSCONNECTOR_C_STD=...` | build/check environment |
| `MSCONNECTOR_CFLAGS` | Used by Makefile/CI scripts when set. | `MSCONNECTOR_CFLAGS=...` | build/check environment |
| `APXS` | Used by Makefile/CI scripts when set. | `APXS=...` | build/check environment |
| `NGINX_SOURCE_DIR` | Used by Makefile/CI scripts when set. | `NGINX_SOURCE_DIR=...` | build/check environment |
| `NGINX_SRC` | Used by Makefile/CI scripts when set. | `NGINX_SRC=...` | build/check environment |
| `MODSECURITY_NGINX_SOURCE_DIR` | Used by Makefile/CI scripts when set. | `MODSECURITY_NGINX_SOURCE_DIR=...` | build/check environment |
| `NGINX_INCLUDE_DIR` | Used by Makefile/CI scripts when set. | `NGINX_INCLUDE_DIR=...` | build/check environment |
| `MSCONNECTOR_COMMON_SRC` | Used by Makefile/CI scripts when set. | `MSCONNECTOR_COMMON_SRC=...` | build/check environment |
| `MODSECURITY_INC` | Used by Makefile/CI scripts when set. | `MODSECURITY_INC=...` | build/check environment |
| `MODSECURITY_INCLUDE` | Used by Makefile/CI scripts when set. | `MODSECURITY_INCLUDE=...` | build/check environment |
| `MODSECURITY_INCLUDE_DIR` | Used by Makefile/CI scripts when set. | `MODSECURITY_INCLUDE_DIR=...` | build/check environment |
| `V3INCLUDE` | Used by Makefile/CI scripts when set. | `V3INCLUDE=...` | build/check environment |
| `HAPROXY_SOURCE_DIR` | Used by Makefile/CI scripts when set. | `HAPROXY_SOURCE_DIR=...` | build/check environment |
| `HAPROXY_INCLUDE_DIR` | Used by Makefile/CI scripts when set. | `HAPROXY_INCLUDE_DIR=...` | build/check environment |
| `CONNECTOR_C_STD_PROFILE` | Used by Makefile/CI scripts when set. | `CONNECTOR_C_STD_PROFILE=...` | build/check environment |
| `APACHE_C_STD_PROFILE` | Used by Makefile/CI scripts when set. | `APACHE_C_STD_PROFILE=...` | build/check environment |
| `NGINX_C_STD_PROFILE` | Used by Makefile/CI scripts when set. | `NGINX_C_STD_PROFILE=...` | build/check environment |
| `HAPROXY_C_STD_PROFILE` | Used by Makefile/CI scripts when set. | `HAPROXY_C_STD_PROFILE=...` | build/check environment |

## Connector model

Each connector owns server API glue and maps host-specific state into Common SDK contracts. A connector must label missing support as `not supported`, `not applicable`, `connector-gap`, `structure-only`, `partial`, `unknown` or `requires runtime evidence`.

## Apache Connector

### Purpose
The Apache connector keeps host/server API integration in `connectors/apache/` and uses Common SDK contracts where implemented.

### Current status
common-SDK adoption is present; any runtime claim requires current harness/report evidence.

### Common-SDK adoption
The connector may use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, decision/status/event helpers and common source linking. Adoption checks are static, contract or compile evidence, not automatic runtime evidence.

### Config/directive support
Supported Common directives are listed in the directive table. Host-specific syntax remains host-specific. Unsupported syntax must be labelled `not supported`, `not applicable`, `connector-gap`, `partial` or `requires runtime evidence`. NGINX must not silently accept Apache-style transaction expressions as NGINX syntax.

### Request mapping
Request mapping converts host request structures to `msconnector_request` and common header helpers. Missing host details must be treated as `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response, header and body state to `msconnector_response`. Response-body behavior is not verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
The common decision, intervention, status and JSONL event helpers provide shared semantics. Per-run events are evidence only for that run.

### Resource/Body/DoS/Flow limits
Resource limits, body policy, DoS guard and flow guard are connector-neutral guardrails. They do not prove runtime secure behavior or tamper-proof evidence.

### C17/C23/future-C checks
C17 is required when compiler and required headers are present. C23 and future-C are optional. Exit 77 is reserved for missing environment or unsupported optional profiles.

### CI/contract checks
Use connector-specific adoption/C-standard targets and the shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
Trust current capability manifests and canonical results. The targeted host
paths have `minimal_runtime_smoke` evidence; broader capabilities remain
unverified until a current canonical result asserts them.

### Implemented
Connector files, metadata, docs, harness stubs or source files listed below exist in the repository.

### Missing
Anything marked `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` or `requires runtime evidence` still needs evidence or implementation.

### Connector-specific remains
request_rec, command_rec, APR pools, bucket brigades, hooks, filters, APXS/autotools, Apache logging and return codes remain connector-specific and must not move into `common/`.

### Important connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/apache/Makefile.am` | Implements or builds `Makefile` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/ORIGIN.md` | Documents or implements `ORIGIN` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/README.de.md` | Documents or implements `README.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/SOURCE_MAP.json` | Documents or implements `SOURCE MAP` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/TODO.md` | Documents or implements `TODO` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/autogen.sh` | Implements or builds `autogen` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/build/apxs-wrapper.in` | Implements or builds `apxs wrapper` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/build/ax_prog_apache.m4` | Implements or builds `ax prog apache` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/build/find_apxs.m4` | Implements or builds `find apxs` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/build/find_libmodsec.m4` | Implements or builds `find libmodsec` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/configure.ac` | Implements or builds `configure` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/docs/architecture.md` | Documents or implements `architecture` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/docs/build.md` | Documents or implements `build` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/docs/coverage-decision-matrix.de.md` | Documents or implements `coverage decision matrix.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/docs/coverage-decision-matrix.md` | Documents or implements `coverage decision matrix` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/docs/public-sources.md` | Documents or implements `public sources` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/docs/validation.md` | Documents or implements `validation` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/harness/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/harness/run_apache_smoke.sh` | Implements or builds `run apache smoke` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/metadata.c` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/metadata.h` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/apache/src/mod_security3.c` | Implements or builds `mod security3` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/mod_security3.h` | Implements or builds `mod security3` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_apache_mapper.c` | Implements or builds `msc apache mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_apache_mapper.h` | Implements or builds `msc apache mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_config.c` | Implements or builds `msc config` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_config.h` | Implements or builds `msc config` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_filters.c` | Implements or builds `msc filters` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_filters.h` | Implements or builds `msc filters` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_utils.c` | Implements or builds `msc utils` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/apache/src/msc_utils.h` | Implements or builds `msc utils` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |

## NGINX Connector

### Purpose
The NGINX connector keeps host/server API integration in `connectors/nginx/` and uses Common SDK contracts where implemented.

### Current status
common-SDK adoption is present; any runtime claim requires current harness/report evidence.

### Common-SDK adoption
The connector may use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, decision/status/event helpers and common source linking. Adoption checks are static, contract or compile evidence, not automatic runtime evidence.

### Config/directive support
Supported Common directives are listed in the directive table. Host-specific syntax remains host-specific. Unsupported syntax must be labelled `not supported`, `not applicable`, `connector-gap`, `partial` or `requires runtime evidence`. NGINX must not silently accept Apache-style transaction expressions as NGINX syntax.

### Request mapping
Request mapping converts host request structures to `msconnector_request` and common header helpers. Missing host details must be treated as `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response, header and body state to `msconnector_response`. Response-body behavior is not verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
The common decision, intervention, status and JSONL event helpers provide shared semantics. Per-run events are evidence only for that run.

### Resource/Body/DoS/Flow limits
Resource limits, body policy, DoS guard and flow guard are connector-neutral guardrails. They do not prove runtime secure behavior or tamper-proof evidence.

### C17/C23/future-C checks
C17 is required when compiler and required headers are present. C23 and future-C are optional. Exit 77 is reserved for missing environment or unsupported optional profiles.

### CI/contract checks
Use connector-specific adoption/C-standard targets and the shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
Trust current capability manifests and canonical results. The targeted host paths have `minimal_runtime_smoke` evidence; broader capabilities remain unverified until a current canonical result asserts them.

### Implemented
Connector files, metadata, docs, harness stubs or source files listed below exist in the repository.

### Missing
Anything marked `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` or `requires runtime evidence` still needs evidence or implementation.

### Connector-specific remains
ngx_http_request_t, ngx_command_t, ngx_chain_t, ngx_buf_t, headers_in/headers_out, filters, pools, return codes and NGINX module build glue remain connector-specific and must not move into `common/`.

### Important connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/nginx/ORIGIN.md` | Documents or implements `ORIGIN` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/README.de.md` | Documents or implements `README.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/SOURCE_MAP.json` | Documents or implements `SOURCE MAP` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/TODO.md` | Documents or implements `TODO` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/config` | Implements or builds `config` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/docs/architecture.md` | Documents or implements `architecture` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/docs/build.md` | Documents or implements `build` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/docs/coverage-decision-matrix.de.md` | Documents or implements `coverage decision matrix.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/docs/coverage-decision-matrix.md` | Documents or implements `coverage decision matrix` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/docs/public-sources.md` | Documents or implements `public sources` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/docs/validation.md` | Documents or implements `validation` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/harness/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/harness/run_nginx_smoke.sh` | Implements or builds `run nginx smoke` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/metadata.c` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/metadata.h` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/nginx/src/ddebug.h` | Implements or builds `ddebug` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | Implements or builds `ngx http modsecurity access` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | Implements or builds `ngx http modsecurity body filter` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | Implements or builds `ngx http modsecurity common` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | Implements or builds `ngx http modsecurity header filter` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | Implements or builds `ngx http modsecurity log` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.c` | Implements or builds `ngx http modsecurity mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.h` | Implements or builds `ngx http modsecurity mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | Implements or builds `ngx http modsecurity module` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |

## HAProxy Connector

### Purpose
The HAProxy connector keeps host/server API integration in `connectors/haproxy/` and uses Common SDK contracts where implemented.

### Current status
common-SDK adoption is present; any runtime claim requires current harness/report evidence.

### Common-SDK adoption
The connector may use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, decision/status/event helpers and common source linking. Adoption checks are static, contract or compile evidence, not automatic runtime evidence.

### Config/directive support
Supported Common directives are listed in the directive table. Host-specific syntax remains host-specific. Unsupported syntax must be labelled `not supported`, `not applicable`, `connector-gap`, `partial` or `requires runtime evidence`. NGINX must not silently accept Apache-style transaction expressions as NGINX syntax.

### Request mapping
Request mapping converts host request structures to `msconnector_request` and common header helpers. Missing host details must be treated as `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response, header and body state to `msconnector_response`. Response-body behavior is not verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
The common decision, intervention, status and JSONL event helpers provide shared semantics. Per-run events are evidence only for that run.

### Resource/Body/DoS/Flow limits
Resource limits, body policy, DoS guard and flow guard are connector-neutral guardrails. They do not prove runtime secure behavior or tamper-proof evidence.

### C17/C23/future-C checks
C17 is required when compiler and required headers are present. C23 and future-C are optional. Exit 77 is reserved for missing environment or unsupported optional profiles.

### CI/contract checks
Use connector-specific adoption/C-standard targets and the shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
Trust current capability manifests and canonical results. The targeted host paths have `minimal_runtime_smoke` evidence; broader capabilities remain unverified until a current canonical result asserts them.

### Implemented
Connector files, metadata, docs, harness stubs or source files listed below exist in the repository.

### Missing
Anything marked `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` or `requires runtime evidence` still needs evidence or implementation.

### Connector-specific remains
SPOE/SPOP, frame parsing, runtime loop, socket handling, HAProxy cfg snippets, process lifecycle and build glue remain connector-specific and must not move into `common/`.

### Important connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/haproxy/Makefile` | Implements or builds `Makefile` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/ORIGIN.md` | Documents or implements `ORIGIN` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/README.de.md` | Documents or implements `README.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/SOURCE_MAP.json` | Documents or implements `SOURCE MAP` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/TODO.md` | Documents or implements `TODO` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/architecture.md` | Documents or implements `architecture` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/build.md` | Documents or implements `build` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/coverage-decision-matrix.de.md` | Documents or implements `coverage decision matrix.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/coverage-decision-matrix.md` | Documents or implements `coverage decision matrix` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/evidence-findings.de.md` | Documents or implements `evidence findings.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/evidence-findings.md` | Documents or implements `evidence findings` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/evidence-questionnaire.de.md` | Documents or implements `evidence questionnaire.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/evidence-questionnaire.md` | Documents or implements `evidence questionnaire` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/integration-decision.md` | Documents or implements `integration decision` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/public-sources.md` | Documents or implements `public sources` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/spoe-external-evidence.de.md` | Documents or implements `spoe external evidence.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/spoe-external-evidence.md` | Documents or implements `spoe external evidence` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/spoe-minimal-artifacts.md` | Documents or implements `spoe minimal artifacts` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/spoe-poc-plan.md` | Documents or implements `spoe poc plan` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/test-framework-contract.md` | Documents or implements `test framework contract` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/docs/validation.md` | Documents or implements `validation` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/harness/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | Implements or builds `run haproxy smoke` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/metadata.c` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/metadata.h` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/agent/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/agent/design.md` | Documents or implements `design` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/harness/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/harness/design.md` | Documents or implements `design` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/reports/README.de.md` | Documents or implements `README.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/reports/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/poc/spoe/syntax-validation.md` | Documents or implements `syntax validation` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | present; runtime claims require current evidence |
| `connectors/haproxy/src/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_modsecurity_binding.c` | Implements or builds `haproxy modsecurity binding` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_modsecurity_binding.h` | Implements or builds `haproxy modsecurity binding` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c` | Implements or builds `haproxy modsecurity binding self test` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.c` | Implements or builds `haproxy modsecurity mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.h` | Implements or builds `haproxy modsecurity mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | Implements or builds `haproxy spoa agent starter` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | Implements or builds `haproxy spoa agent starter` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_spoa_main.c` | Implements or builds `haproxy spoa main` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | Implements or builds `haproxy spop diagnostic runtime` in the connector area | uses common contracts where included; host API remains connector-specific | yes | present; runtime claims require current evidence |

## Envoy Connector

### Purpose
The Envoy connector keeps host/server API integration in `connectors/envoy/` and uses Common SDK contracts where implemented.

### Current status
minimal_runtime_smoke / connector-gap; targeted real-host runtime path; canonical No-CRS not executed; no production, CRS, full-matrix or RESPONSE_BODY claim.

### Common-SDK adoption
The connector may use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, decision/status/event helpers and common source linking. Adoption checks are static, contract or compile evidence, not automatic runtime evidence.

### Config/directive support
Supported Common directives are listed in the directive table. Host-specific syntax remains host-specific. Unsupported syntax must be labelled `not supported`, `not applicable`, `connector-gap`, `partial` or `requires runtime evidence`. NGINX must not silently accept Apache-style transaction expressions as NGINX syntax.

### Request mapping
Request mapping converts host request structures to `msconnector_request` and common header helpers. Missing host details must be treated as `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response, header and body state to `msconnector_response`. Response-body behavior is not verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
The common decision, intervention, status and JSONL event helpers provide shared semantics. Per-run events are evidence only for that run.

### Resource/Body/DoS/Flow limits
Resource limits, body policy, DoS guard and flow guard are connector-neutral guardrails. They do not prove runtime secure behavior or tamper-proof evidence.

### C17/C23/future-C checks
C17 is required when compiler and required headers are present. C23 and future-C are optional. Exit 77 is reserved for missing environment or unsupported optional profiles.

### CI/contract checks
Use connector-specific adoption/C-standard targets and the shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
Trust current capability manifests and canonical results. The targeted host paths have `minimal_runtime_smoke` evidence; broader capabilities remain unverified until a current canonical result asserts them.

### Implemented
Connector files, metadata, docs, harness stubs or source files listed below exist in the repository.

### Missing
Anything marked `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` or `requires runtime evidence` still needs evidence or implementation.

### Connector-specific remains
Envoy filter/runtime API, native Envoy SDK ownership and deployed proxy integration remain connector-specific and must not move into `common/`.

### Important connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/envoy/Makefile` | Implements or builds `Makefile` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/ORIGIN.md` | Documents or implements `ORIGIN` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/README.de.md` | Documents or implements `README.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/SOURCE_MAP.json` | Documents or implements `SOURCE MAP` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/TODO.md` | Documents or implements `TODO` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/build/build_metadata.sh` | Implements or builds `build metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/architecture.md` | Documents or implements `architecture` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/build.md` | Documents or implements `build` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.de.md` | Documents or implements `coverage decision matrix.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.md` | Documents or implements `coverage decision matrix` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/public-sources.md` | Documents or implements `public sources` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/validation.md` | Documents or implements `validation` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/harness/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/harness/run_envoy_smoke.sh` | Implements or builds `run envoy smoke` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/metadata.c` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/metadata.h` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_bridge.c` | Implements or builds `envoy bridge` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_bridge.h` | Implements or builds `envoy bridge` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_bridge_main.c` | Implements or builds `envoy bridge main` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_modsecurity_mapper.h` | Implements or builds `envoy modsecurity mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |

## Traefik Connector

### Purpose
The Traefik connector keeps host/server API integration in `connectors/traefik/` and uses Common SDK contracts where implemented.

### Current status
minimal_runtime_smoke / connector-gap; targeted real-host runtime path; canonical No-CRS not executed; no production, CRS, full-matrix or RESPONSE_BODY claim.

### Common-SDK adoption
The connector may use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, decision/status/event helpers and common source linking. Adoption checks are static, contract or compile evidence, not automatic runtime evidence.

### Config/directive support
Supported Common directives are listed in the directive table. Host-specific syntax remains host-specific. Unsupported syntax must be labelled `not supported`, `not applicable`, `connector-gap`, `partial` or `requires runtime evidence`. NGINX must not silently accept Apache-style transaction expressions as NGINX syntax.

### Request mapping
Request mapping converts host request structures to `msconnector_request` and common header helpers. Missing host details must be treated as `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response, header and body state to `msconnector_response`. Response-body behavior is not verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
The common decision, intervention, status and JSONL event helpers provide shared semantics. Per-run events are evidence only for that run.

### Resource/Body/DoS/Flow limits
Resource limits, body policy, DoS guard and flow guard are connector-neutral guardrails. They do not prove runtime secure behavior or tamper-proof evidence.

### C17/C23/future-C checks
C17 is required when compiler and required headers are present. C23 and future-C are optional. Exit 77 is reserved for missing environment or unsupported optional profiles.

### CI/contract checks
Use connector-specific adoption/C-standard targets and the shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
Trust current capability manifests and canonical results. The targeted host paths have `minimal_runtime_smoke` evidence; broader capabilities remain unverified until a current canonical result asserts them.

### Implemented
Connector files, metadata, docs, harness stubs or source files listed below exist in the repository.

### Missing
Anything marked `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` or `requires runtime evidence` still needs evidence or implementation.

### Connector-specific remains
Traefik middleware/proxy/runtime API and real traffic path integration remain connector-specific and must not move into `common/`.

### Important connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/traefik/Makefile` | Implements or builds `Makefile` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/ORIGIN.md` | Documents or implements `ORIGIN` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/README.de.md` | Documents or implements `README.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/SOURCE_MAP.json` | Documents or implements `SOURCE MAP` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/TODO.md` | Documents or implements `TODO` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/build/build-starter.sh` | Implements or builds `build starter` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/architecture.md` | Documents or implements `architecture` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/build.md` | Documents or implements `build` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.de.md` | Documents or implements `coverage decision matrix.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.md` | Documents or implements `coverage decision matrix` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/public-sources.md` | Documents or implements `public sources` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/validation.md` | Documents or implements `validation` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/harness/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/harness/run_traefik_smoke.sh` | Implements or builds `run traefik smoke` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/metadata.c` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/metadata.h` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_build_starter.c` | Implements or builds `traefik build starter` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_decision_service.c` | Implements or builds `traefik decision service` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_decision_service.h` | Implements or builds `traefik decision service` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_decision_service_main.c` | Implements or builds `traefik decision service main` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_modsecurity_mapper.h` | Implements or builds `traefik modsecurity mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / connector-gap |

## lighttpd Connector

### Purpose
The lighttpd connector keeps host/server API integration in `connectors/lighttpd/` and uses Common SDK contracts where implemented.

### Current status
minimal_runtime_smoke / partial_runtime_path; targeted real-host runtime path; canonical No-CRS not executed; no production, CRS, full-matrix or RESPONSE_BODY claim.

### Common-SDK adoption
The connector may use `msconnector_config`, directive vocabulary, mapper contracts, request/response models, decision/status/event helpers and common source linking. Adoption checks are static, contract or compile evidence, not automatic runtime evidence.

### Config/directive support
Supported Common directives are listed in the directive table. Host-specific syntax remains host-specific. Unsupported syntax must be labelled `not supported`, `not applicable`, `connector-gap`, `partial` or `requires runtime evidence`. NGINX must not silently accept Apache-style transaction expressions as NGINX syntax.

### Request mapping
Request mapping converts host request structures to `msconnector_request` and common header helpers. Missing host details must be treated as `partial` or `requires runtime evidence`.

### Response mapping
Response mapping converts host response, header and body state to `msconnector_response`. Response-body behavior is not verified unless current runtime evidence proves it.

### Decision/Event/JSONL behavior
The common decision, intervention, status and JSONL event helpers provide shared semantics. Per-run events are evidence only for that run.

### Resource/Body/DoS/Flow limits
Resource limits, body policy, DoS guard and flow guard are connector-neutral guardrails. They do not prove runtime secure behavior or tamper-proof evidence.

### C17/C23/future-C checks
C17 is required when compiler and required headers are present. C23 and future-C are optional. Exit 77 is reserved for missing environment or unsupported optional profiles.

### CI/contract checks
Use connector-specific adoption/C-standard targets and the shared contract targets. Compile and contract checks do not create production, CRS, full-matrix or runtime claims.

### Runtime evidence status
Trust current capability manifests and canonical results. The targeted host paths have `minimal_runtime_smoke` evidence; broader capabilities remain unverified until a current canonical result asserts them.

### Implemented
Connector files, metadata, docs, harness stubs or source files listed below exist in the repository.

### Missing
Anything marked `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` or `requires runtime evidence` still needs evidence or implementation.

### Connector-specific remains
lighttpd plugin/proxy/runtime API and FastCGI/SCGI/native module integration remain connector-specific and must not move into `common/`.

### Important connector files
| File | Purpose | Common relation | Connector-specific? | Status |
|---|---|---|---|---|
| `connectors/lighttpd/Makefile` | Implements or builds `Makefile` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/ORIGIN.md` | Documents or implements `ORIGIN` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/README.de.md` | Documents or implements `README.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/SOURCE_MAP.json` | Documents or implements `SOURCE MAP` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/TODO.md` | Documents or implements `TODO` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/build/bridge_starter.sh` | Implements or builds `bridge starter` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/build/build_starter.sh` | Implements or builds `build starter` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/architecture.md` | Documents or implements `architecture` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/build.md` | Documents or implements `build` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/coverage-decision-matrix.de.md` | Documents or implements `coverage decision matrix.de` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/coverage-decision-matrix.md` | Documents or implements `coverage decision matrix` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/public-sources.md` | Documents or implements `public sources` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/validation.md` | Documents or implements `validation` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/harness/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/harness/run_lighttpd_smoke.sh` | Implements or builds `run lighttpd smoke` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/metadata.c` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/metadata.h` | Implements or builds `metadata` in the connector area | uses common contracts where included; host API remains connector-specific | metadata/docs | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/README.md` | Documents or implements `README` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_bridge.c` | Implements or builds `lighttpd bridge` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_bridge.h` | Implements or builds `lighttpd bridge` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_bridge_main.c` | Implements or builds `lighttpd bridge main` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_build_starter.c` | Implements or builds `lighttpd build starter` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_modsecurity_mapper.h` | Implements or builds `lighttpd modsecurity mapper` in the connector area | uses common contracts where included; host API remains connector-specific | yes | minimal_runtime_smoke / partial_runtime_path |

## Connector status matrix

| Connector | Current status | Common adoption | Runtime evidence | Forbidden inference |
|---|---|---|---|---|
| Apache | connector source present | present | requires current reports/harness output | no production/runtime/CRS/full-matrix claim |
| NGINX | connector source present | present | requires current reports/harness output | no production/runtime/CRS/full-matrix claim |
| HAProxy | SPOA/starter plus mapper/binding source present | present/partial | requires current reports/harness output | no production/runtime/CRS/full-matrix claim |
| Envoy | HTTP `ext_authz` service | adopted | targeted request-header 200/403 path; canonical No-CRS `NOT EXECUTED` | upstream response phases are `UNSUPPORTED`; no broader claim |
| Traefik | HTTP `forwardAuth` service | adopted | targeted request-header 200/403 path; canonical No-CRS `NOT EXECUTED` | native request body `NOT IMPLEMENTED`; upstream response `UNSUPPORTED` |
| lighttpd | native plugin | adopted | targeted Phase-1 200/403 path; canonical No-CRS `NOT EXECUTED` | bodies `NOT IMPLEMENTED`; Phase 3 `IMPLEMENTED, NOT ASSERTED` |

## Test framework relation

The reusable test framework is expected under `modules/ModSecurity-test-Framework`. Framework-dependent targets can be BLOCKED when the submodule, framework docs, fixtures or runtime components are missing. That does not automatically mean a Common SDK or connector compile check failed.

## Runtime evidence and verification policy

Connector metadata describes repository-level connector state. A canonical
`result.json` describes only one run and must match the connector commit,
framework commit, capability manifest, and evidence layout. Legacy starter,
self-test, sidecar, CRS, and targeted-smoke results are not imported into a
canonical No-CRS result.

## Implemented work

Implemented repository facts include the Common SDK, connector-specific host
adapters for all six connectors, canonical capability manifests, separated
evidence stages, C17/C23/future-C check wiring, CI/governance scripts, and
documentation/report areas. Treat implementation as `IMPLEMENTED, NOT
ASSERTED` until current canonical evidence proves the behavior.

## Missing/future work

Missing or future work includes executing the canonical No-CRS baseline,
closing connector-specific capability gaps, any later CRS or extended-matrix
work, production hardening, and only those response-phase features supported by
each selected host model.

## Known limitations

Known limitations are connector-specific host APIs, environment-dependent
headers/toolchains, framework/submodule blockers, partial runtime coverage, and
documentation that must stay synchronized with capability manifests and
canonical results.

## Intentionally connector-specific

Apache request/APR/filter/APXS details, NGINX request/chain/filter/module glue, HAProxy SPOE/SPOP/frame/runtime loop, Envoy APIs, Traefik APIs and lighttpd APIs remain outside `common/`.

## AI fact block

```yaml
repository: Easton97-Jens/ModSecurity-conector
purpose: Shared Common SDK layer for ModSecurity connectors
common_sdk: true
production_ready: false
runtime_verified_all_connectors: false
canonical_no_crs_executed: false
apache_common_adopted: true
nginx_common_adopted: true
haproxy_common_adopted: true
envoy_status: minimal_runtime_smoke / connector-gap
traefik_status: minimal_runtime_smoke / connector-gap
lighttpd_status: minimal_runtime_smoke / partial_runtime_path
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
```

## Allowed and forbidden claims

Allowed claims include connector-neutral Common SDK semantics, C17 required
checks when the environment exists, optional C23/future-C checks, capability
states sourced from `connectors/<name>/capabilities.json`, and per-run evidence
scoped to that run. Without current explicit evidence, do not claim:
production-ready, runtime secure, security verified, CRS verified, full matrix
verified, response body verified across all connectors, production hardened,
tamper-proof, or cryptographic integrity.

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
- Keep German documentation synchronized with English documentation.
- Runtime claims only with evidence.
```
