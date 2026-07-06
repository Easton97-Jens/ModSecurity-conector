# Überblick über das ModSecurity-Connector-Repository

**Sprache:** [English](repository-overview.md) | Deutsch

## Inhaltsverzeichnis

1. [Zweck des Repositorys](#repository-purpose)
2. [Kurzfassung für Menschen](#short-summary-for-humans)
3. [Kurzfassung für KI-Systeme](#short-summary-for-ai-systems)
4. [Architekturprinzip](#architecture-principle)
5. [Repository-Struktur](#repository-structure)
6. [Common SDK: vollständiger Dateiindex](#common-sdk-complete-file-index)
7. [Common SDK: Module und Aufgaben](#common-sdk-modules-and-responsibilities)
8. [Config-, Direktiven- und Parser-Modell](#config-directives-and-parser-model)
9. [Erlaubte Config-/Directive-Begriffe](#allowed-configdirective-vocabulary)
10. [Request-/Response-Mapping](#requestresponse-mapping)
11. [Decision-, Intervention-, Status- und Event-Modell](#decision-intervention-status-and-event-model)
12. [Resource Limits, DoS Guard, Flow Guard und Integrity](#reSource-limits-dos-guard-flow-guard-and-integrity)
13. [C-Sprache und Standards](#c-language-and-standards)
14. [CI-, Contract- und Governance-Checks](#ci-contract-and-governance-checks)
15. [Makefile-Ziele: Was kann man mit `make` tun?](#makefile-targets-what-can-be-done-with-make)
16. [Häufige Makefile-Aufrufe](#common-makefile-commands)
17. [Exit-Codes und BLOCKED/SKIPPED-Verhalten](#exit-codes-and-blockedskipped-behavior)
18. [Umgebungsvariablen](#environment-variables)
19. [Connector-Modell](#connector-model)
20. [Apache-Connector](#apache-connector)
21. [NGINX-Connector](#nginx-connector)
22. [HAProxy-Connector](#haproxy-connector)
23. [Envoy-Connector](#envoy-connector)
24. [Traefik-Connector](#traefik-connector)
25. [lighttpd-Connector](#lighttpd-connector)
26. [Connector-Statusmatrix](#connector-status-matrix)
27. [Test-Framework-Bezug](#test-framework-relation)
28. [Runtime Evidence und Verification Policy](#runtime-evidence-and-verification-policy)
29. [Was bereits umgesetzt ist](#implemented-work)
30. [Was noch fehlt](#missingfuture-work)
31. [Bekannte Grenzen](#known-limits)
32. [Was bewusst connector-spezifisch bleibt](#intentionally-connector-specific)
33. [KI-Faktenblock](#ai-fact-block)
34. [Erlaubte und verbotene Claims](#allowed-and-forbidden-claims)
35. [Glossar](#glossary)
36. [Wartungs-Checkliste](#maintenance-checklist)

## Zweck des Repositorys

Diese deutsche Datei ist inhaltlich gleichwertig zur englischen Übersicht. Code-, API-, Datei- und Statusnamen bleiben absichtlich unverändert, damit spätere KI-Systeme sie direkt mit dem Repository abgleichen können. Die Aussagen sind konservativ: Compile-, Struktur- und Governance-Checks werden nicht als Runtime-, CRS-, Full-Matrix-, RESPONSE_BODY- oder Production-Nachweise beschrieben.


Dieses Repository baut ModSecurity-Connectoren und eine gemeinsame Common-SDK-Schicht auf. Ziel ist, connector-neutrale Semantik in `common/` zu halten und Host-/Server-API-Integration in den jeweiligen Connectoren zu belassen.

Grundsatz: Alles, was Semantik ist, gehört nach `common/`; alles, was Host-/Server-API ist, bleibt im Connector.

Beispiele für Common: Config, Direktiven, Direktiven-Spezifikationen, Parser-Helfer, Request- und Response-Modelle, Header-Helfer, Mapper-Contracts, Decision-/Intervention-/Status-/Error-Modelle, Event JSONL, Resource Limits, DoS Guard, Flow Guard, Integrity-Metadaten, Rule-Loading-Contracts, Test-Result-JSON, Adapter-Metadaten, Capabilities und Generic-Mapper-Helfer.

Beispiele für Connector-spezifische Teile: Apache `request_rec`, `command_rec` und APR; NGINX `ngx_http_request_t`, `ngx_chain_t` und Filter; HAProxy SPOE/SPOP, Frame-Parsing und Runtime-Loop; Envoy Filter-/Runtime-APIs; Traefik Middleware-/Proxy-/Runtime-APIs; und lighttpd Plugin-/Proxy-/Runtime-APIs.

## Kurzfassung für Menschen

Das Repository ist ein Connector-Monorepo. Apache, NGINX und HAProxy besitzen aktiven Connector-Code und Common-Adoption-Checks. Envoy, Traefik und lighttpd besitzen Starter-/Structure-only-/Compile-only-Vorbereitung und müssen bis zu echter Runtime Evidence als `not_verified / connector-gap` behandelt werden. Compile-, Lint- und Contract-Checks sind wertvoll, sind aber keine Production-, CRS-, Full-Matrix-, Response-Body- oder Runtime-Verifikations-Claims.

## Kurzfassung für KI-Systeme

Nutze Repository-Code, CI-Skripte und aktuelle Reports als Source of Truth. Leite keine Runtime-Garantien aus Dateinamen, Makefile-Zielen oder lokalen Smoke-Ergebnissen ab. Unterscheide Connector-Metadaten von per-run `result.json`. Verwende `unknown`, `partial`, `structure-only`, `not_verified`, `connector-gap` oder `requires runtime evidence`, wenn Nachweise fehlen.

## Architekturprinzip

`common/` definiert connector-neutrale C/C++-Contracts und Helfer. `connectors/<name>/` bildet Server-APIs auf diese Contracts ab. Generierte Reports liegen unter `reports/testing/generated/`; CI- und Governance-Skripte liegen in `ci/`; wiederverwendbare Tests werden unter `modules/ModSecurity-test-Framework` erwartet.

## Repository-Struktur

| Pfad | Bedeutung | Evidenzstatus |
|---|---|---|
| `common/include/msconnector/` | Öffentliche Common-SDK-Header. | Nur Contract-/statische Evidenz, außer in einem Lauf getestet. |
| `common/src/` | Common-SDK-Helferimplementierungen. | C17-/Common-Checks. |
| `connectors/apache/` | Apache-Adapter-Quellen, docs, Harness und Metadaten. | Common-Adoption; Runtime-Claims benötigen aktuelle Evidenz. |
| `connectors/nginx/` | NGINX-Adapter-Quellen, docs, Harness und Metadaten. | Common-Adoption; Runtime-Claims benötigen aktuelle Evidenz. |
| `connectors/haproxy/` | HAProxy-/SPOA-Starter und Mapping-Quellen, docs, Harness und Metadaten. | Common-Adoption; Runtime-Claims benötigen aktuelle Evidenz. |
| `connectors/envoy/` | Envoy-Bridge-Starter. | `not_verified / connector-gap`. |
| `connectors/traefik/` | Traefik-Decision-Service-Starter. | `not_verified / connector-gap`. |
| `connectors/lighttpd/` | lighttpd-Bridge-/Build-Starter. | `not_verified / connector-gap`. |
| `ci/` | Lint, contract, governance, C-standard and report scripts. | Check-Definitionen, für sich allein keine Runtime Evidence. |
| `docs/` | Repository-weite und Architektur-Dokumentation. | Dokumentation; muss synchron bleiben. |
| `reports/` | Generierte Reports/Evidenz/Matrizen. | Nur aktuelle generierte Evidenz und Statuslabels vertrauen. |

## Common SDK: vollständiger Dateiindex

| Datei | Typ | Zweck | Wichtige APIs/Structs | Genutzt von | Status / Hinweise |
|---|---|---|---|---|---|
| `common/include/msconnector/adapter.h` | Header | adapter helper/model for the connector-neutral SDK | msconnector_adapter, msconnector_adapter_metadata, msconnector_capabilities, msconnector_config, msconnector_error, msconnector_transaction_view | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/adapter_contract.h` | Header | adapter contract declarations | msconnector_adapter_contract_result, msconnector_adapter_contract_result_init, msconnector_adapter_contract_validate, msconnector_adapter | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/adapter_metadata.h` | Header | adapter metadata shape | msconnector_adapter_metadata, msconnector_origin, msconnector_capabilities, msconnector_adapter_metadata_init, msconnector_adapter_metadata_is_complete | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/artifact_layout.h` | Header | artifact layout helper/model for the connector-neutral SDK | msconnector_artifact_layout, msconnector_artifact_layout_init, msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/artifacts.h` | Header | artifacts helper/model for the connector-neutral SDK | msconnector_artifact_paths, msconnector_artifact_paths_init, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/block_statuses.h` | Header | block statuses helper/model for the connector-neutral SDK | msconnector_block_status_support, msconnector_block_status_is_allowed, msconnector_block_status_normalize, msconnector_http_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/blocking.h` | Header | blocking helper/model for the connector-neutral SDK | msconnector_block_action, msconnector_blocking_policy, msconnector_block_action_name, msconnector_block_action_is_disruptive, msconnector_blocking_policy_make | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/body_policy.h` | Header | body policy helper/model for the connector-neutral SDK | msconnector_body_mode, msconnector_body_policy, msconnector_body_policy_init, msconnector_body_mode_name, msconnector_body_mode_is_supported | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/build_contract.h` | Header | build contract helper/model for the connector-neutral SDK | msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/capabilities.h` | Header | capability declarations | msconnector_capability_flags, msconnector_capability_flag, msconnector_capabilities, msconnector_capabilities_has, msconnector_capability_name, msconnector_capability_from_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/capabilities.hpp` | Header | capability declarations | msconnector_capability_flags, msconnector_capability_flag, msconnector_capabilities, msconnector_capability_name | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/capability_matrix.h` | Header | capability matrix helper/model for the connector-neutral SDK | msconnector_capability_required_test, msconnector_capability_flag, msconnector_capability_has_required_test | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/config.h` | Header | connector-neutral configuration object, defaults, merge and validation | msconnector_config, msconnector_bool_option, msconnector_phase4_mode, msconnector_config_init, msconnector_config_apply_defaults, msconnector_config_merge | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/config_parser.h` | Header | shared parsers for booleans, phase4 mode, sizes, HTTP statuses and content-type tokens | msconnector_parse_bool, msconnector_bool_option, msconnector_parse_phase4_mode, msconnector_phase4_mode, msconnector_parse_size, msconnector_parse_http_status | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/connector_manifest.h` | Header | connector manifest helper/model for the connector-neutral SDK | msconnector_connector_manifest, msconnector_capability_flags, msconnector_connector_manifest_init, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_connector_manifest_write_json | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/crs.h` | Header | crs helper/model for the connector-neutral SDK | msconnector_crs_mode, msconnector_crs_config, msconnector_crs_config_init, msconnector_crs_config_validate, msconnector_crs_mode_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/decision.h` | Header | inspection decision model | msconnector_event, msconnector_decision_kind, msconnector_decision, msconnector_status, msconnector_phase, msconnector_intervention | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/decision_action.h` | Header | decision action helper/model for the connector-neutral SDK | msconnector_decision_action, msconnector_decision_action_name, msconnector_decision_action_from_decision, msconnector_decision, msconnector_decision_action_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/directive_adapter.h` | Header | helpers that apply directive values to msconnector_config | msconnector_directive_scope, msconnector_directive_argument_policy, msconnector_directive_adapter_entry, msconnector_directive_spec, msconnector_directive_adapter_count, msconnector_directive_adapter_at | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/directive_spec.h` | Header | global directive catalog with value types, defaults and allowed values | msconnector_directive_value_type, msconnector_directive_spec, msconnector_directive_specs, msconnector_directive_spec_count, msconnector_directive_spec_find | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/directives.h` | Header | canonical directive name macros | file-local helpers / metadata | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/dos_guard.h` | Header | DoS guard counters and checks | msconnector_dos_guard_check_request, msconnector_request, msconnector_reSource_limits, msconnector_error, msconnector_dos_guard_check_response, msconnector_response | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/error.h` | Header | error helper/model for the connector-neutral SDK | msconnector_error_code, msconnector_error, msconnector_error_init, msconnector_error_set, msconnector_error_code_name, msconnector_error_default_message | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/event.h` | Header | event model | msconnector_event_meta, msconnector_event_decision, msconnector_phase, msconnector_status, msconnector_event_http, msconnector_event_request | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/event_jsonl.h` | Header | JSONL serialization for events | msconnector_event_write_jsonl_line, msconnector_event | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/flow_guard.h` | Header | request/response flow guard | msconnector_flow_guard, msconnector_phase, msconnector_flow_guard_init, msconnector_flow_guard_can_enter_phase, msconnector_flow_guard_mark_validated, msconnector_flow_guard_mark_immutable | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/generic_mapper.h` | Header | generic request/response mapper helpers for starter connectors | msconnector_generic_request_Source, msconnector_endpoint, msconnector_Header, msconnector_bytes, msconnector_generic_response_Source, msconnector_generic_config_init | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/Headers.h` | Header | connector-neutral Header list helpers | msconnector_Header_name_equals, msconnector_Header, msconnector_Header_name_is, msconnector_Headers_find, msconnector_Headers_find_first, msconnector_Headers_find_last | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/http_status.h` | Header | http status helper/model for the connector-neutral SDK | msconnector_http_status_class, msconnector_http_status_info, msconnector_http_status_info_find, msconnector_http_status_reason_phrase, msconnector_http_status_default_message, msconnector_http_status_classify | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/integrity_event.h` | Header | integrity metadata events without cryptographic claims | msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/intervention.h` | Header | intervention/blocking model | msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/intervention.hpp` | Header | intervention/blocking model | msconnector_intervention | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/json_escape.h` | Header | json escape helper/model for the connector-neutral SDK | msconnector_json_escape | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/late_intervention.h` | Header | late intervention helper/model for the connector-neutral SDK | msconnector_late_intervention_action, msconnector_late_intervention_policy, msconnector_late_intervention_policy_init, msconnector_late_intervention_action_name, msconnector_late_intervention_resolve | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/lifecycle_status.h` | Header | lifecycle status helper/model for the connector-neutral SDK | msconnector_build_status, msconnector_runtime_status, msconnector_verification_status, msconnector_build_status_name, msconnector_runtime_status_name, msconnector_verification_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/limits.h` | Header | limits helper/model for the connector-neutral SDK | msconnector_limit_Header_count, msconnector_limit_Header_name_length, msconnector_limit_Header_value_length, msconnector_limit_total_Header_bytes, msconnector_limit_body_buffer_size, msconnector_limit_response_body_buffer_size | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/log_sanitize.h` | Header | log sanitize helper/model for the connector-neutral SDK | msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/logging.h` | Header | logging helper/model for the connector-neutral SDK | msconnector_log_level, msconnector_log_record, msconnector_log_callback, msconnector_logger, msconnector_log | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/logging.hpp` | Header | logging helper/model for the connector-neutral SDK | msconnector_log_level, msconnector_log_record, msconnector_logger, msconnector_log | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/memory.h` | Header | memory helper/model for the connector-neutral SDK | msconnector_alloc_checked, msconnector_free_checked, msconnector_alloc_callback, msconnector_free_callback, msconnector_allocator, msconnector_allocator_init | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/modsecurity_engine.h` | Header | modsecurity engine helper/model for the connector-neutral SDK | msconnector_modsecurity_engine_ops, msconnector_error, msconnector_request, msconnector_decision, msconnector_response, msconnector_modsecurity_engine | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/options.h` | Header | options helper/model for the connector-neutral SDK | msconnector_bool_option, msconnector_phase4_mode | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/origin.h` | Header | origin/license metadata | msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/origin.hpp` | Header | origin/license metadata | msconnector_origin, msconnector_origin_is_empty | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/origin_governance.h` | Header | origin governance helper/model for the connector-neutral SDK | msconnector_origin_governance, msconnector_origin_governance_init, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/path_policy.h` | Header | path policy helper/model for the connector-neutral SDK | msconnector_path_is_absolute, msconnector_path_is_empty, msconnector_path_has_parent_reference | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/phase.h` | Header | phase helper/model for the connector-neutral SDK | msconnector_phase | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/redaction.h` | Header | redaction helper/model for the connector-neutral SDK | msconnector_redacted_string, msconnector_redact_copy | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/request.h` | Header | connector-neutral request model | msconnector_bytes, msconnector_Header, msconnector_endpoint, msconnector_request | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/request.hpp` | Header | connector-neutral request model | msconnector_bytes, msconnector_Header, msconnector_endpoint, msconnector_request, msconnector_request_init, msconnector_request_validate | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/request_helpers.h` | Header | request helpers helper/model for the connector-neutral SDK | msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_reSource_limits, msconnector_request_has_Header | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/request_mapper_contract.h` | Header | request mapper contract validation | msconnector_mapper_requirement, msconnector_request_mapper_contract, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract_validate, msconnector_request_mapper_validate_output, msconnector_request | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/reSource_limits.h` | Header | reSource limit model | msconnector_reSource_limits, msconnector_reSource_limits_init, msconnector_reSource_limits_validate, msconnector_reSource_limits_Headers_ok, msconnector_Header, msconnector_reSource_limits_body_ok | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/response.h` | Header | connector-neutral response model | msconnector_response, msconnector_Header, msconnector_bytes | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/response.hpp` | Header | connector-neutral response model | msconnector_response, msconnector_response_init, msconnector_response_validate | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/response_helpers.h` | Header | response helpers helper/model for the connector-neutral SDK | msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_response_validate_with_limits, msconnector_reSource_limits, msconnector_response_has_Header | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/response_mapper_contract.h` | Header | response mapper contract validation | msconnector_response_mapper_contract, msconnector_mapper_requirement, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output, msconnector_response | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/rule_error.h` | Header | rule error helper/model for the connector-neutral SDK | msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_rule_error_set_load_failed, msconnector_rule_error_clear | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/rule_event.h` | Header | rule event helper/model for the connector-neutral SDK | msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_rule_load_event, msconnector_rule_error_event, msconnector_error | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/rule_id.h` | Header | rule id helper/model for the connector-neutral SDK | msconnector_rule_id_copy, msconnector_rule_id_extract_from_message, msconnector_rule_id_validate | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/rule_load_stats.h` | Header | rule load stats helper/model for the connector-neutral SDK | msconnector_rule_load_stats, msconnector_rule_load_stats_init, msconnector_rule_load_stats_add, msconnector_rule_load_stats_add_inline, msconnector_rule_load_stats_add_file, msconnector_rule_load_stats_add_remote | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/rule_loader.h` | Header | rule loading contracts | msconnector_rule_loader_backend, msconnector_error, msconnector_rule_loader, msconnector_rule_load_stats, msconnector_rule_loader_init, msconnector_rule_loader_add_inline | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/rule_merge.h` | Header | rule merge helper/model for the connector-neutral SDK | msconnector_rule_collection, msconnector_rule_collection_init, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/runtime_paths.h` | Header | runtime paths helper/model for the connector-neutral SDK | msconnector_runtime_path_join | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/runtime_report.h` | Header | runtime report helper/model for the connector-neutral SDK | msconnector_runtime_report, msconnector_status, msconnector_runtime_report_init, msconnector_runtime_report_write_json | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/status.h` | Header | status classification helpers | msconnector_status, msconnector_status_name, msconnector_status_from_result | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/status.hpp` | Header | status classification helpers | msconnector_status, msconnector_status_name | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/test_result.h` | Header | test result helper/model for the connector-neutral SDK | msconnector_test_result, msconnector_status, msconnector_test_result_init, msconnector_test_result_passed | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/test_result_json.h` | Header | test result JSON writer | msconnector_test_result_write_json, msconnector_test_result | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/transaction.h` | Header | transaction helper/model for the connector-neutral SDK | msconnector_transaction_view, msconnector_request, msconnector_response, msconnector_intervention | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/transaction.hpp` | Header | transaction helper/model for the connector-neutral SDK | msconnector_transaction_view, msconnector_transaction_state, msconnector_decision, msconnector_phase, msconnector_phase_name | Common SDK und adoptierende Connectoren | C++ facade |
| `common/include/msconnector/transaction_id.h` | Header | transaction id helper/model for the connector-neutral SDK | msconnector_transaction_id_Source, msconnector_transaction_id_expr_eval, msconnector_request, msconnector_transaction_id_context, msconnector_config, msconnector_transaction_id_result | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/include/msconnector/transaction_state.h` | Header | transaction state helper/model for the connector-neutral SDK | msconnector_transaction_state, msconnector_transaction_state_init, msconnector_transaction_state_mark_phase, msconnector_phase, msconnector_transaction_state_phase_processed, msconnector_phase_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/README.md` | Dokumentation | README helper/model for the connector-neutral SDK | file-local helpers / metadata | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/adapter.c` | Source | adapter helper/model for the connector-neutral SDK | msconnector_adapter_init, msconnector_adapter, msconnector_adapter_has_metadata, msconnector_adapter_has_capabilities, msconnector_adapter_supports_phase, msconnector_phase | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/adapter_contract.c` | Source | adapter contract declarations | msconnector_adapter_contract_result, msconnector_capabilities, msconnector_capability_flag, msconnector_capability_flags, msconnector_adapter, msconnector_adapter_contract_result_init | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/adapter_metadata.c` | Source | adapter metadata shape | msconnector_adapter_metadata_init, msconnector_adapter_metadata, msconnector_adapter_metadata_is_complete | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/artifact_layout.c` | Source | artifact layout helper/model for the connector-neutral SDK | msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log, msconnector_artifact_name_runtime_stdout_log, msconnector_artifact_name_runtime_stderr_log | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/artifacts.c` | Source | artifacts helper/model for the connector-neutral SDK | msconnector_artifact_paths_init, msconnector_artifact_paths, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/block_statuses.c` | Source | block statuses helper/model for the connector-neutral SDK | msconnector_block_status_is_allowed, msconnector_http_status_is_block_response, msconnector_block_status_normalize, msconnector_http_status_is_valid, msconnector_http_status_name, msconnector_http_status_info_find | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/blocking.c` | Source | blocking helper/model for the connector-neutral SDK | msconnector_block_action_name, msconnector_block_action, msconnector_block_action_is_disruptive, msconnector_blocking_policy, msconnector_blocking_policy_make, msconnector_block_status_normalize | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/body_policy.c` | Source | body policy helper/model for the connector-neutral SDK | msconnector_body_policy_init, msconnector_body_policy, msconnector_body_mode_name, msconnector_body_mode, msconnector_body_mode_is_supported | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/build_contract.c` | Source | build contract helper/model for the connector-neutral SDK | msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/capabilities.c` | Source | capability declarations | msconnector_capability_flag, msconnector_capability_name, msconnector_capability_from_name, msconnector_capability_flags, msconnector_capabilities_add | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/capability_matrix.c` | Source | capability matrix helper/model for the connector-neutral SDK | msconnector_capability_required_test, msconnector_capability_flag, msconnector_capability_has_required_test | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/config.c` | Source | connector-neutral configuration object, defaults, merge and validation | msconnector_bool_option, msconnector_phase4_mode, msconnector_config, msconnector_block_status_is_allowed, msconnector_http_status_is_valid, msconnector_http_status_is_error | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/config_parser.c` | Source | shared parsers for booleans, phase4 mode, sizes, HTTP statuses and content-type tokens | msconnector_parse_bool, msconnector_bool_option, msconnector_parse_phase4_mode, msconnector_phase4_mode, msconnector_parse_size, msconnector_parse_http_status | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/connector_manifest.c` | Source | connector manifest helper/model for the connector-neutral SDK | msconnector_json_escape, msconnector_connector_manifest_init, msconnector_connector_manifest, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_adapter_metadata_is_complete | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/crs.c` | Source | crs helper/model for the connector-neutral SDK | msconnector_crs_config_init, msconnector_crs_config, msconnector_crs_mode_name, msconnector_crs_mode, msconnector_crs_config_validate | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/decision.c` | Source | inspection decision model | msconnector_decision_kind, msconnector_decision_init, msconnector_decision, msconnector_intervention_none, msconnector_decision_kind_name, msconnector_decision_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/decision_action.c` | Source | decision action helper/model for the connector-neutral SDK | msconnector_decision_action_name, msconnector_decision_action, msconnector_decision_action_from_decision, msconnector_decision, msconnector_decision_action_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/directive_adapter.c` | Source | helpers that apply directive values to msconnector_config | msconnector_directive_adapter_entry, msconnector_directive_adapter_count, msconnector_directive_adapter_at, msconnector_directive_spec_find, msconnector_directive_adapter_find, msconnector_directive_adapter_validate_entry | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/directive_spec.c` | Source | global directive catalog with value types, defaults and allowed values | msconnector_directive_spec, msconnector_directive_specs, msconnector_directive_spec_count, msconnector_directive_spec_find | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/dos_guard.c` | Source | DoS guard counters and checks | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_dos_guard_check_request, msconnector_request, msconnector_reSource_limits | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/error.c` | Source | error helper/model for the connector-neutral SDK | msconnector_error_init, msconnector_error, msconnector_error_set, msconnector_error_code, msconnector_error_code_name, msconnector_error_default_message | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/event.c` | Source | event model | msconnector_event_json_text_index, msconnector_event_json_status_index, msconnector_event_json_flag_index, msconnector_event_json_parts | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/event_jsonl.c` | Source | JSONL serialization for events | msconnector_event_write_jsonl_line, msconnector_event, msconnector_event_write_json_ex | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/flow_guard.c` | Source | request/response flow guard | msconnector_phase, msconnector_flow_guard_init, msconnector_flow_guard, msconnector_flow_guard_can_enter_phase, msconnector_flow_guard_mark_validated, msconnector_flow_guard_mark_immutable | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/generic_mapper.c` | Source | generic request/response mapper helpers for starter connectors | msconnector_generic_config_init, msconnector_config, msconnector_config_init, msconnector_generic_map_request, msconnector_generic_request_Source, msconnector_request_mapper_contract | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/Headers.c` | Source | connector-neutral Header list helpers | msconnector_Header_name_is, msconnector_Header_name_equals, msconnector_Header, msconnector_Headers_find_first, msconnector_Headers_find, msconnector_Headers_find_last | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/http_status.c` | Source | http status helper/model for the connector-neutral SDK | msconnector_http_status_info, msconnector_http_status_is_valid, msconnector_http_status_class, msconnector_http_status_classify, msconnector_http_status_info_find, msconnector_http_status_reason_phrase | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/integrity_event.c` | Source | integrity metadata events without cryptographic claims | msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/intervention.c` | Source | intervention/blocking model | msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/json_escape.c` | Source | json escape helper/model for the connector-neutral SDK | msconnector_json_escape | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/late_intervention.c` | Source | late intervention helper/model for the connector-neutral SDK | msconnector_late_intervention_policy_init, msconnector_late_intervention_policy, msconnector_late_intervention_action_name, msconnector_late_intervention_action, msconnector_late_intervention_resolve | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/lifecycle_status.c` | Source | lifecycle status helper/model for the connector-neutral SDK | msconnector_build_status_name, msconnector_build_status, msconnector_runtime_status_name, msconnector_runtime_status, msconnector_verification_status_name, msconnector_verification_status | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/limits.c` | Source | limits helper/model for the connector-neutral SDK | msconnector_limit_Header_count, msconnector_limit_Header_name_length, msconnector_limit_Header_value_length, msconnector_limit_total_Header_bytes, msconnector_limit_body_buffer_size, msconnector_limit_response_body_buffer_size | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/log_sanitize.c` | Source | log sanitize helper/model for the connector-neutral SDK | msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/memory.c` | Source | memory helper/model for the connector-neutral SDK | msconnector_allocator_init, msconnector_allocator, msconnector_alloc_checked, msconnector_free_checked, msconnector_allocator_within_limit | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/modsecurity_engine.c` | Source | modsecurity engine helper/model for the connector-neutral SDK | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_modsecurity_transaction, msconnector_modsecurity_engine_init, msconnector_modsecurity_engine | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/origin.c` | Source | origin/license metadata | msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/origin_governance.c` | Source | origin governance helper/model for the connector-neutral SDK | msconnector_origin_governance_init, msconnector_origin_governance, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/path_policy.c` | Source | path policy helper/model for the connector-neutral SDK | msconnector_path_is_empty, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/redaction.c` | Source | redaction helper/model for the connector-neutral SDK | msconnector_redacted_string, msconnector_redact_copy | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/request_helpers.c` | Source | request helpers helper/model for the connector-neutral SDK | msconnector_Header, msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_reSource_limits | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/request_mapper_contract.c` | Source | request mapper contract validation | msconnector_mapper_requirement, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract, msconnector_request_mapper_contract_validate, msconnector_request_mapper_validate_output, msconnector_request | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/reSource_limits.c` | Source | reSource limit model | msconnector_reSource_limits_init, msconnector_reSource_limits, msconnector_reSource_limits_validate, msconnector_reSource_limits_Headers_ok, msconnector_Header, msconnector_reSource_limits_body_ok | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/response_helpers.c` | Source | response helpers helper/model for the connector-neutral SDK | msconnector_Header, msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_http_status_is_valid, msconnector_response_validate_with_limits | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/response_mapper_contract.c` | Source | response mapper contract validation | msconnector_mapper_requirement, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output, msconnector_response | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/rule_error.c` | Source | rule error helper/model for the connector-neutral SDK | msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_error_set, msconnector_error_default_message, msconnector_rule_error_set_load_failed, msconnector_rule_error_clear | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/rule_event.c` | Source | rule event helper/model for the connector-neutral SDK | msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_event_init, msconnector_rule_load_event, msconnector_rule_error_event | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/rule_id.c` | Source | rule id helper/model for the connector-neutral SDK | msconnector_rule_id_validate, msconnector_rule_id_copy, msconnector_rule_id_extract_from_message | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/rule_loader.c` | Source | rule loading contracts | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_rule_loader_init, msconnector_rule_loader, msconnector_rule_loader_backend | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/rule_merge.c` | Source | rule merge helper/model for the connector-neutral SDK | msconnector_rule_collection_init, msconnector_rule_collection, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/runtime_paths.c` | Source | runtime paths helper/model for the connector-neutral SDK | msconnector_runtime_path_join, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/runtime_report.c` | Source | runtime report helper/model for the connector-neutral SDK | msconnector_json_escape, msconnector_runtime_report_init, msconnector_runtime_report, msconnector_runtime_report_write_json, msconnector_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/status.c` | Source | status classification helpers | msconnector_status_name, msconnector_status, msconnector_status_from_result | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/test_result.c` | Source | test result helper/model for the connector-neutral SDK | msconnector_test_result_init, msconnector_test_result, msconnector_test_result_passed | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/test_result_json.c` | Source | test result JSON writer | msconnector_json_escape, msconnector_test_result_write_json, msconnector_test_result, msconnector_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/transaction.c` | Source | transaction helper/model for the connector-neutral SDK | msconnector_decision_kind, msconnector_status, msconnector_decision, msconnector_intervention_none, msconnector_decision_make, msconnector_intervention | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/transaction_id.c` | Source | transaction id helper/model for the connector-neutral SDK | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_transaction_id_result, msconnector_transaction_id_validate, msconnector_transaction_id_copy | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |
| `common/src/transaction_state.c` | Source | transaction state helper/model for the connector-neutral SDK | msconnector_transaction_state_init, msconnector_transaction_state, msconnector_transaction_state_mark_phase, msconnector_phase, msconnector_transaction_state_phase_processed, msconnector_phase_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime Evidence |

## Common SDK: Module und Aufgaben

- Configuration/directives/parser: owns neutral vocabulary, defaults, merge and validation. It is neutral because it stores values without Apache/NGINX/HAProxy/Envoy/Traefik/lighttpd types. It does not claim host syntax parity unless a connector implements it.
- Request/response/Header/mapper contracts: define neutral HTTP shapes and validation. They do not prove body processing in a live server.
- Decision/intervention/status/error/event JSONL: define shared semantics and serialization. They are not tamper-proof or cryptographic evidence.
- Resource limits/body policy/DoS guard/flow guard/integrity metadata: define guardrails and metadata. They do not claim runtime secure behavior.
- Rule loading, merge and CRS helpers: define contracts and metadata. They do not prove CRS execution or full matrix coverage.
- Adapter metadata/capabilities/origin/manifests: identify Source, status and capabilities. Metadata status must not be overridden by a successful per-run starter smoke.

## Config-, Direktiven- und Parser-Modell

`msconnector_config` stores neutral options: enable, error-log use, inline/file/remote rules, static or expression transaction ID, phase-4 response-body mode, content-type file, log path, body limit and default statuses.

`msconnector_config_init` sets fields to unset/zero/null. `msconnector_config_apply_defaults` fills unset values only. `msconnector_config_merge` merges parent and child values and then applies defaults; defaults must not be applied too early because doing so would incorrectly override parent/child inheritance. `msconnector_config_validate` checks enum ranges, complete remote-rule pairs, mutual exclusion of `transaction_id` and `transaction_id_expr`, and allowed status values.

Parser helpers use `1 = success` and `0 = failure`: `msconnector_parse_bool`, `msconnector_parse_phase4_mode`, `msconnector_parse_size`, `msconnector_parse_http_status` and `msconnector_validate_content_type_token`. Boolean parsing accepts on/off-style values; phase4 mode accepts `minimal`, `safe`, `strict`; size parsing accepts positive decimal byte sizes; HTTP status parsing requires a valid HTTP status; content-type token validation requires one slash, non-empty type/subtype and rejects control characters and semicolons. Transaction-ID validation is represented by `transaction_id` helpers and connector-specific expression parsing remains connector-specific.

## Erlaubte Config-/Directive-Begriffe

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

## Request-/Response-Mapping

Request mapping owns neutral method, URI, protocol, Headers, body metadata and transaction identifiers. Response mapping owns status, Headers, content-type/body metadata and phase-4 policy data. Mapper contracts validate ownership, required fields and cleanup expectations. Host server objects bleiben außerhalb von `common/`.

## Decision-, Intervention-, Status- und Event-Modell

Common decision/action helpers express allow/block/error/unsupported-like outcomes. Intervention helpers normalize block handling; status helpers map to HTTP statuses; event and JSONL helpers serialize structured evidence for a run. These outputs are per-run artifacts and not append-only or cryptographically signed unless such evidence is explicitly implemented later.

## Resource Limits, DoS Guard, Flow Guard und Integrity

Resource limits centralize maximum sizes/counts. DoS guard and flow guard detect policy violations in neutral state. Integrity events carry metadata. This is governance and safety modeling, not a claim that runtime traffic is secure, tamper-proof or cryptographically protected.

## C-Sprache und Standards

The Common SDK is designed for C17. C17 is the required profile when the compiler and required host/libmodsecurity Headers are present. C23 is optional. future-C (`c2y`/`gnu2y`) is optional. `c20` and `c26` are not C standard modes and should be reported as SKIPPED/INFO if targets exist. Exit 77 means BLOCKED/SKIPPED due to missing environment, missing Headers, missing compiler or unsupported optional profile. Real compile failures must not be hidden as 77.

| Connector | C17 | C23 | future-C | Header requirements | Exit-77 behavior |
|---|---|---|---|---|---|
| Common | required when compiler exists | optional | optional | common Headers | only missing/unsupported environment should skip |
| Apache | hard when APXS/APR/libmodsecurity Headers exist | optional | optional | APXS, APR, libmodsecurity | missing Headers may block; compile errors must fail |
| NGINX | hard when NGINX/libmodsecurity Headers exist | optional | optional | NGINX Source/include roots, libmodsecurity | missing Source/Header roots may block |
| HAProxy | hard when HAProxy/libmodsecurity context exists | optional | optional | HAProxy/SPOE/SPOP and common includes | missing Headers may block |
| Envoy | compile/structure-level only | optional | optional | starter/common Headers; no native Envoy SDK claim | not_verified connector-gap remains |
| Traefik | compile/structure-level only | optional | optional | starter/common Headers | not_verified connector-gap remains |
| lighttpd | compile/structure-level only | optional | optional | starter/common Headers | not_verified connector-gap remains |

## CI-, Contract- und Governance-Checks

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
| `check-bilingual-docs` | `ci/check_bilingual_docs.py` | Englisch/deutsche Dokumentations-Paarung | docs/connectors | hart für docs | no/usage-specific |
| `lint`, `quick-check`, `codex-check` | Makefile composites | aggregate lint/check workflows | repo | hard aggregate | framework blockers possible |
| framework/report targets | framework scripts | runtime matrix/report governance | reports/framework | optional or composite | yes when submodule/env missing |

## Makefile-Ziele: Was kann man mit `make` tun?

Das Makefile ist der operative Index für Setup, Linting, Common-SDK-Checks, Connector-Checks, C-Standard-Profile, Runtime-/Starter-Smoke-Läufe, Matrix-/Report-Generierung, Framework-Integration sowie Cleanup-/Bootstrap-Workflows. Wichtige Regel: Ein Makefile-Ziel kann nur das belegen, was sein Skript tatsächlich prüft. Compile-only- und Structure-only-Ziele erzeugen keine Runtime Evidence.

### Zielkategorien

1. General targets: `lint`, `quick-check`, `codex-check`, `setup-dev`, `install-dev-deps`, `Dokumentationtor`, `Dokumentationtor-quick`, `cloud-quick-check`, `quick-all`, `clean`-like/bootstrap targets where present.
2. Common SDK targets: `check-common-helpers`, C17/C23/future-C variants, SDK/security/memory/flow contracts, adapter contracts and directive parity.
3. Apache targets: common adoption, C-standard wiring, C17/C23/future-C and smoke/test targets. `check-apache-c17` is hard when APXS/APR/libmodsecurity Headers exist; `check-apache-c17-lint` may translate environment skips in lint context.
4. NGINX targets: common adoption, C-standard wiring, C17/C23/future-C and smoke/test targets. NGINX Source/include variables may be required.
5. HAProxy targets: common adoption, C-standard wiring, C17/C23/future-C and HAProxy smoke/test targets. HAProxy/SPOE/SPOP remains connector-specific.
6. Remaining connector targets: Envoy, Traefik and lighttpd adoption/C-standard/starter smoke targets. These remain `not_verified / connector-gap` and compile/structure-level only.
7. Framework/test-framework targets: `check-framework`, runtime matrix, verified report and MRTS targets; these can block if `modules/ModSecurity-test-Framework/...` is missing.
8. Report/generator targets: generate/check matrix and report artifacts. Reports require valid inputs and do not automatically imply verified claims.

### Vollständige Makefile-Zieltabelle

| Makefile-Ziel | Zweck | Betrifft | Voraussetzung | Hart/optional | Exit-77/BLOCKED möglich? | Hinweise |
|---|---|---|---|---|---|---|
| `check-framework` | Führt den Workflow `check-framework` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-framework-fixture-syntax` | Führt den Workflow `check-framework-fixture-syntax` aus. | framework/reports | check-framework | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework |
| `prepare-runtime-components` | Führt den Workflow `prepare-runtime-components` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-envoy-runtime` | Führt den Workflow `prepare-envoy-runtime` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-traefik-runtime` | Führt den Workflow `prepare-traefik-runtime` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-lighttpd-runtime` | Führt den Workflow `prepare-lighttpd-runtime` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-lighttpd-runtime-build` | Führt den Workflow `prepare-lighttpd-runtime-build` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-open-connector-runtimes` | Führt den Workflow `prepare-open-connector-runtimes` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `runtime-components-inventory` | Führt den Workflow `runtime-components-inventory` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `runtime-components-sources` | Führt den Workflow `runtime-components-sources` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-runtime-producer-readiness` | Führt den Workflow `check-runtime-producer-readiness` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-runtime-path-policy` | Führt den Workflow `check-runtime-path-policy` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-bilingual-docs` | Führt den Workflow `check-bilingual-docs` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `refresh-connector-reports` | Führt den Workflow `refresh-connector-reports` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `refresh-all-reports` | Führt den Workflow `refresh-all-reports` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `check-generated-report-layout` | Führt den Workflow `check-generated-report-layout` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `report-governance` | Führt den Workflow `report-governance` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-evidence-gate` | Führt den Workflow `verified-report-evidence-gate` aus. | framework/reports | check-generated-report-layout | optional/composite | usually no; script-specific | depends on check-generated-report-layout |
| `generate-system-environment-proof` | Führt den Workflow `generate-system-environment-proof` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-verified-runtime-mismatch-analysis` | Führt den Workflow `generate-verified-runtime-mismatch-analysis` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-remaining-critical-batch-analysis` | Führt den Workflow `generate-remaining-critical-batch-analysis` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-native-semantics-comparison` | Führt den Workflow `generate-native-semantics-comparison` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prove-generated-reports` | Führt den Workflow `prove-generated-reports` aus. | framework/reports | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `verified-runtime-producers` | Führt den Workflow `verified-runtime-producers` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-producers` | Führt den Workflow `verified-report-producers` aus. | framework/reports | verified-runtime-producers | optional/composite | usually no; script-specific | depends on verified-runtime-producers |
| `verified-report-refresh` | Führt den Workflow `verified-report-refresh` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-consumers` | Führt den Workflow `verified-report-consumers` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-checks` | Führt den Workflow `verified-report-checks` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-run` | Führt den Workflow `verified-report-run` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-run-soft` | Führt den Workflow `verified-report-run-soft` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-report-run-smoke` | Führt den Workflow `verified-report-run-smoke` aus. | framework/reports | check-framework | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework |
| `verified-full-matrix-job` | Führt den Workflow `verified-full-matrix-job` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-case` | Führt den Workflow `verified-case` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `verified-native-case` | Führt den Workflow `verified-native-case` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-nginx-case` | Führt den Workflow `verified-nginx-case` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-apache-case` | Führt den Workflow `verified-apache-case` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-haproxy-case` | Führt den Workflow `verified-haproxy-case` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `verified-full-matrix-resume` | Führt den Workflow `verified-full-matrix-resume` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `smoke-common` | Führt den Workflow `smoke-common` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-apache` | Führt den Workflow `smoke-apache` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-nginx` | Führt den Workflow `smoke-nginx` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-envoy` | Führt den Workflow `smoke-envoy` aus. | framework/reports | check-framework | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework |
| `smoke-envoy-modsecurity` | Führt den Workflow `smoke-envoy-modsecurity` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-envoy-request-body` | Führt den Workflow `smoke-envoy-request-body` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-envoy-crs` | Führt den Workflow `smoke-envoy-crs` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-envoy-crs-secondary` | Führt den Workflow `smoke-envoy-crs-secondary` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-haproxy` | Führt den Workflow `smoke-haproxy` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-lighttpd` | Führt den Workflow `smoke-lighttpd` aus. | framework/reports | check-framework | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework |
| `smoke-lighttpd-modsecurity` | Führt den Workflow `smoke-lighttpd-modsecurity` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-lighttpd-request-body` | Führt den Workflow `smoke-lighttpd-request-body` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-lighttpd-crs` | Führt den Workflow `smoke-lighttpd-crs` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-lighttpd-crs-secondary` | Führt den Workflow `smoke-lighttpd-crs-secondary` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik` | Führt den Workflow `smoke-traefik` aus. | framework/reports | check-framework | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework |
| `smoke-traefik-modsecurity` | Führt den Workflow `smoke-traefik-modsecurity` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik-request-body` | Führt den Workflow `smoke-traefik-request-body` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik-crs` | Führt den Workflow `smoke-traefik-crs` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-traefik-crs-secondary` | Führt den Workflow `smoke-traefik-crs-secondary` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-open-connectors-crs` | Führt den Workflow `smoke-open-connectors-crs` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-open-connectors-request-body` | Führt den Workflow `smoke-open-connectors-request-body` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-open-connectors-crs-secondary` | Führt den Workflow `smoke-open-connectors-crs-secondary` aus. | framework/reports | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `smoke-new-connectors` | Führt den Workflow `smoke-new-connectors` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `smoke-all` | Führt den Workflow `smoke-all` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test` | Führt den Workflow `test` aus. | framework/reports | test-no-crs test-with-crs | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on test-no-crs test-with-crs |
| `test-no-crs` | Führt den Workflow `test-no-crs` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-with-crs` | Führt den Workflow `test-with-crs` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `mrts-generate` | Führt den Workflow `mrts-generate` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `mrts-load` | Führt den Workflow `mrts-load` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `mrts-import` | Führt den Workflow `mrts-import` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `test-no-mrts` | Führt den Workflow `test-no-mrts` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-with-mrts` | Führt den Workflow `test-with-mrts` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-with-mrts-feature-demo` | Führt den Workflow `test-with-mrts-feature-demo` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-mrts-matrix` | Führt den Workflow `test-mrts-matrix` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `mrts-ftw` | Führt den Workflow `mrts-ftw` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix` | Führt den Workflow `runtime-matrix` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix-all` | Führt den Workflow `runtime-matrix-all` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix-all-runtime` | Führt den Workflow `runtime-matrix-all-runtime` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `runtime-matrix-haproxy` | Führt den Workflow `runtime-matrix-haproxy` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-mrts-runtime-matrix` | Führt den Workflow `full-mrts-runtime-matrix` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-only-full-run` | Führt den Workflow `mrts-only-full-run` aus. | framework/reports | full-mrts-runtime-matrix | optional/composite | usually no; script-specific | depends on full-mrts-runtime-matrix |
| `full-runtime-matrix` | Führt den Workflow `full-runtime-matrix` aus. | framework/reports | full-matrix-parallel | optional/composite | usually no; script-specific | depends on full-matrix-parallel |
| `full-matrix-parallel` | Führt den Workflow `full-matrix-parallel` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-matrix-parallel-runtime` | Führt den Workflow `full-matrix-parallel-runtime` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-matrix-single-job-runtime` | Führt den Workflow `full-matrix-single-job-runtime` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `full-matrix-resume-runtime` | Führt den Workflow `full-matrix-resume-runtime` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `generate-full-runtime-matrix` | Führt den Workflow `generate-full-runtime-matrix` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-full-matrix-job-completeness` | Führt den Workflow `generate-full-matrix-job-completeness` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-nginx-mrts-http500-cluster-analysis` | Führt den Workflow `generate-nginx-mrts-http500-cluster-analysis` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-work-queue` | Führt den Workflow `generate-work-queue` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-phase-work-queue` | Führt den Workflow `generate-phase-work-queue` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-nolog-audit-evidence-analysis` | Führt den Workflow `generate-nolog-audit-evidence-analysis` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-response-header-hook-analysis` | Führt den Workflow `generate-response-header-hook-analysis` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-phase4-hard-abort-capability` | Führt den Workflow `generate-phase4-hard-abort-capability` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-intervention-blocking-analysis` | Führt den Workflow `generate-intervention-blocking-analysis` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-no-mrts-intervention-nomatch-analysis` | Führt den Workflow `generate-no-mrts-intervention-nomatch-analysis` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-body-processor-analysis` | Führt den Workflow `generate-body-processor-analysis` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-rule-chain-semantics-analysis` | Führt den Workflow `generate-rule-chain-semantics-analysis` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-final-consistency-audit` | Führt den Workflow `generate-final-consistency-audit` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `generate-remaining-failure-analysis` | Führt den Workflow `generate-remaining-failure-analysis` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `mrts-native-full-run` | Führt den Workflow `mrts-native-full-run` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-native-full-run-runtime` | Führt den Workflow `mrts-native-full-run-runtime` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-native-apache-full` | Führt den Workflow `mrts-native-apache-full` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-native-nginx-pr24-full` | Führt den Workflow `mrts-native-nginx-pr24-full` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `mrts-upstream-infra-check` | Führt den Workflow `mrts-upstream-infra-check` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `test-haproxy-no-crs` | Führt den Workflow `test-haproxy-no-crs` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `test-haproxy-with-crs` | Führt den Workflow `test-haproxy-with-crs` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework prepare-runtime-components |
| `probe-response-body` | Führt den Workflow `probe-response-body` aus. | framework/reports | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `connector-starter-checks` | Führt den Workflow `connector-starter-checks` aus. | repo | check-framework prepare-runtime-components | optional/composite | usually no; script-specific | depends on check-framework prepare-runtime-components |
| `check-remaining-connectors-common-adoption` | Führt den Workflow `check-remaining-connectors-common-adoption` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c-standard-wiring` | Führt den Workflow `check-remaining-connectors-c-standard-wiring` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c-standards` | Führt den Workflow `check-remaining-connectors-c-standards` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c17` | Führt den Workflow `check-remaining-connectors-c17` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c17-lint` | Führt den Workflow `check-remaining-connectors-c17-lint` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-remaining-connectors-c23` | Führt den Workflow `check-remaining-connectors-c23` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-remaining-connectors-future-c` | Führt den Workflow `check-remaining-connectors-future-c` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-block-status-generator` | Führt den Workflow `check-block-status-generator` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-common-adoption` | Führt den Workflow `check-apache-common-adoption` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-c-standard-wiring` | Führt den Workflow `check-apache-c-standard-wiring` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-c-standards` | Führt den Workflow `check-apache-c-standards` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-apache-c17` | Führt den Workflow `check-apache-c17` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-apache-c17-lint` | Führt den Workflow `check-apache-c17-lint` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-apache-c23` | Führt den Workflow `check-apache-c23` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-apache-future-c` | Führt den Workflow `check-apache-future-c` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-apache-c20` | Führt den Workflow `check-apache-c20` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-apache-c26` | Führt den Workflow `check-apache-c26` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-nginx-common-adoption` | Führt den Workflow `check-nginx-common-adoption` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-nginx-c-standard-wiring` | Führt den Workflow `check-nginx-c-standard-wiring` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-nginx-c-standards` | Führt den Workflow `check-nginx-c-standards` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-nginx-c17` | Führt den Workflow `check-nginx-c17` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-nginx-c17-lint` | Führt den Workflow `check-nginx-c17-lint` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-nginx-c23` | Führt den Workflow `check-nginx-c23` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-nginx-future-c` | Führt den Workflow `check-nginx-future-c` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-nginx-c20` | Führt den Workflow `check-nginx-c20` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-nginx-c26` | Führt den Workflow `check-nginx-c26` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-common-adoption` | Führt den Workflow `check-haproxy-common-adoption` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-haproxy-c-standard-wiring` | Führt den Workflow `check-haproxy-c-standard-wiring` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-haproxy-c-standards` | Führt den Workflow `check-haproxy-c-standards` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-haproxy-c17` | Führt den Workflow `check-haproxy-c17` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-haproxy-c17-lint` | Führt den Workflow `check-haproxy-c17-lint` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-haproxy-c23` | Führt den Workflow `check-haproxy-c23` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-future-c` | Führt den Workflow `check-haproxy-future-c` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-c20` | Führt den Workflow `check-haproxy-c20` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-haproxy-c26` | Führt den Workflow `check-haproxy-c26` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers` | Führt den Workflow `check-common-helpers` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-common-helpers-c17` | Führt den Workflow `check-common-helpers-c17` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-common-helpers-c23` | Führt den Workflow `check-common-helpers-c23` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers-future-c` | Führt den Workflow `check-common-helpers-future-c` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers-c20` | Führt den Workflow `check-common-helpers-c20` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-common-helpers-c26` | Führt den Workflow `check-common-helpers-c26` aus. | common/connectors | see Makefile/script | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | direct script/action |
| `check-common-sdk-contract` | Führt den Workflow `check-common-sdk-contract` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-common-security-contract` | Führt den Workflow `check-common-security-contract` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-common-memory-safety` | Führt den Workflow `check-common-memory-safety` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-common-flow-integrity` | Führt den Workflow `check-common-flow-integrity` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `check-adapter-contracts` | Führt den Workflow `check-adapter-contracts` aus. | common/connectors | see Makefile/script | hard | usually no; script-specific | direct script/action |
| `check-directive-parity` | Führt den Workflow `check-directive-parity` aus. | common/connectors | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `lint` | Führt den Workflow `lint` aus. | repo | check-framework | hard | usually no; script-specific | depends on check-framework |
| `summary` | Führt den Workflow `summary` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `case-matrix` | Führt den Workflow `case-matrix` aus. | framework/reports | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `install-dev-deps` | Führt den Workflow `install-dev-deps` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `setup-dev` | Führt den Workflow `setup-dev` aus. | repo | install-dev-deps | optional/composite | usually no; script-specific | depends on install-dev-deps |
| `fetch-modsecurity-v3` | Führt den Workflow `fetch-modsecurity-v3` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `fetch-crs` | Führt den Workflow `fetch-crs` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `prepare-crs` | Führt den Workflow `prepare-crs` aus. | repo | check-framework | optional/composite | usually no; script-specific | depends on check-framework |
| `print-python` | Führt den Workflow `print-python` aus. | repo | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `bootstrap-all` | Führt den Workflow `bootstrap-all` aus. | repo | setup-dev fetch-deps Dokumentationtor | optional/composite | usually no; script-specific | depends on setup-dev fetch-deps Dokumentationtor |
| `Dokumentationtor-install-hints` | Führt den Workflow `Dokumentationtor-install-hints` aus. | repo | see Makefile/script | optional/composite | usually no; script-specific | direct script/action |
| `Dokumentationtor-quick` | Führt den Workflow `Dokumentationtor-quick` aus. | repo | check-framework | hard | usually no; script-specific | depends on check-framework |
| `quick-all` | Führt den Workflow `quick-all` aus. | repo | check-framework | hard | usually no; script-specific | depends on check-framework |
| `cloud-quick-check` | Führt den Workflow `cloud-quick-check` aus. | repo | setup-dev lint generate-test-matrix check-test-matrix quick-check | hard | usually no; script-specific | depends on setup-dev lint generate-test-matrix check-test-matrix quick-check |
| `generate-test-matrix` | Führt den Workflow `generate-test-matrix` aus. | framework/reports | check-framework | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework |
| `check-test-matrix` | Führt den Workflow `check-test-matrix` aus. | framework/reports | check-framework | optional/composite | yes for framework/env/Header blockers; optional profiles may skip | depends on check-framework |

### C17-, C23- und future-C-Ziele

C17 targets (`check-*-c17`) are the required standard checks when the relevant compiler and Headers are present. C23 targets (`check-*-c23`) are optional. future-C targets (`check-*-future-c`) are optional and may use `c2y`/`gnu2y` where supported. `check-*-c20` and `check-*-c26`, where present, are skip/info targets because c20/c26 are not valid C language modes. Exit 77 must mean an environment or unsupported-profile skip, never a hidden compile or contract error.

## Häufige Makefile-Aufrufe

- `make check-common-helpers`: use after common helper changes.
- `make check-common-sdk-contract`: use after adding/changing Common SDK Headers or APIs.
- `make check-adapter-contracts`: use after metadata or connector contract changes.
- `make check-directive-parity`: use after directive/config/parser changes.
- `make check-apache-common-adoption && make check-apache-c17`: use after Apache connector changes.
- `make check-nginx-common-adoption && make check-nginx-c17`: use after NGINX connector changes.
- `make check-haproxy-common-adoption && make check-haproxy-c17`: use after HAProxy connector changes.
- `make check-remaining-connectors-common-adoption && make check-remaining-connectors-c17`: use after Envoy/Traefik/lighttpd starter changes; still no runtime claim.
- `make lint`: aggregate repository lint/governance check.
- `make quick-check` or `make codex-check`: lightweight pre-commit validation.

## Exit-Codes und BLOCKED/SKIPPED-Verhalten

- `0`: success.
- `1`, `2` or other non-zero values: real failure or usage error unless the script Dokumentationuments otherwise.
- `77`: BLOCKED/SKIPPED because the environment, Headers, compiler, submodule or optional C profile is unavailable.

Exit 77 darf echte Compile- oder Contract-Fehler nicht verstecken. Lint-Wrapper dürfen 77 für umgebungsbedingt begrenzte Checks übersetzen, aber nicht für echte Fehler.

## Umgebungsvariablen

| Variable | Verwendung | Beispiel | Betrifft |
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


## Connector-Modell

Each connector owns server API glue and may call common config, request/response mapping, directive adapter, decision/intervention/status/event and reSource-limit helpers. A connector must state unsupported features as `not supported`, `connector-gap`, `structure-only`, `partial`, `unknown` or `requires runtime evidence`.

## Apache-Connector

### Zweck des Connectors
Der Apache-Connector belässt Host-/Server-API-Arbeit in `connectors/apache/` und adoptiert Common-Config, Mapping, Decision-, Status-, Event- und Metadaten-Contracts, soweit umgesetzt.

### Aktueller Status
common SDK adoption present; runtime claims require current harness/report evidence.

### Common-SDK-Adoption
Der Connector soll, soweit passend, `msconnector_config`, Direktiven-Vokabular, Mapper-Contracts, Request-/Response-Modelle, Status-/Decision-/Event-Helfer und Common-Source-Linking verwenden. Adoption-Checks sind Compile-/Static-/Contract-Evidenz, keine automatische Runtime Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Nicht unterstützte oder host-spezifische Syntax muss als `not supported`, `not applicable`, `connector-gap` oder `structure-only` markiert werden; Apache-artige Expressions dürfen nicht stillschweigend als NGINX-Syntax akzeptiert werden.

### Request-Mapping
Request-Mapping wandelt Host-Request-Objekte in `msconnector_request` und Header-Helfer um. Fehlende Host-Details sind `partial` oder `requires runtime evidence`.

### Response-Mapping
Response-Mapping wandelt Host-Response-/Header-/Body-Zustand in `msconnector_response` um. RESPONSE_BODY-Verhalten darf nur mit aktueller Runtime Evidence als verifiziert bezeichnet werden.

### Decision/Event/JSONL-Verhalten
Decision-, Intervention-, Status- und JSONL-Event-Helfer sind Common-Semantik. Per-run Event-Ausgabe ist nur Evidenz für diesen Lauf.

### Resource-/Body-/DoS-/Flow boundaries
Resource Limits, Body Policy, DoS Guard und Flow Guard sind connector-neutrale Kontrollen. Sie sind Guardrails und Governance-Modelle, keine runtime-secure- oder tamper-proof-Claims.

### C-Sprachstandard / Checks
C17 ist das erforderliche Compile-Profil, wenn Compiler und Header vorhanden sind. C23 und future-C sind optional. Exit 77 bedeutet BLOCKED/SKIPPED wegen fehlender Umgebung oder nicht unterstütztem optionalem Profil, nicht versteckter Compile-Fehler.

### CI-/Contract-Checks
Nutze connector-spezifische Common-Adoption- und C-Standard-Ziele plus gemeinsame Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
For Apache-Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Was umgesetzt ist
Common-facing structure, metadata, docs/harness stubs or Connector-Quellen are present as listed below.

### Was fehlt
Fehlende Arbeit ist alles, was als `connector-gap`, `not_verified`, `structure-only`, `unknown` oder `requires runtime evidence` markiert ist, besonders echte Runtime-Integration für Starter-Connectoren.

### Was connector-spezifisch bleibt
request_rec, command_rec, APR pools, bucket brigades, hooks, filters, APXS/autotools, Apache logging and return codes bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Dateien des Connectors
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/apache/Makefile.am` | Makefile helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/README.de.md` | README.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/TODO.md` | TODO helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/autogen.sh` | autogen helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/build/apxs-wrapper.in` | apxs-wrapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/build/ax_prog_apache.m4` | ax prog apache helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/build/find_apxs.m4` | find apxs helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/build/find_libmodsec.m4` | find libmodsec helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/configure.ac` | configure helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/docs/build.md` | build helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/docs/validation.md` | validation helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/harness/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/harness/run_apache_smoke.sh` | run apache smoke helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/metadata.c` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/metadata.h` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/mod_security3.c` | mod security3 helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/mod_security3.h` | mod security3 helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_apache_mapper.c` | msc apache mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_apache_mapper.h` | msc apache mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_config.c` | msc config helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_config.h` | msc config helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_filters.c` | msc filters helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_filters.h` | msc filters helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_utils.c` | msc utils helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/apache/src/msc_utils.h` | msc utils helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |

## NGINX-Connector

### Zweck des Connectors
Der NGINX-Connector belässt Host-/Server-API-Arbeit in `connectors/nginx/` und adoptiert Common-Config, Mapping, Decision-, Status-, Event- und Metadaten-Contracts, soweit umgesetzt.

### Aktueller Status
common SDK adoption present; runtime claims require current harness/report evidence.

### Common-SDK-Adoption
Der Connector soll, soweit passend, `msconnector_config`, Direktiven-Vokabular, Mapper-Contracts, Request-/Response-Modelle, Status-/Decision-/Event-Helfer und Common-Source-Linking verwenden. Adoption-Checks sind Compile-/Static-/Contract-Evidenz, keine automatische Runtime Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Nicht unterstützte oder host-spezifische Syntax muss als `not supported`, `not applicable`, `connector-gap` oder `structure-only` markiert werden; Apache-artige Expressions dürfen nicht stillschweigend als NGINX-Syntax akzeptiert werden.

### Request-Mapping
Request-Mapping wandelt Host-Request-Objekte in `msconnector_request` und Header-Helfer um. Fehlende Host-Details sind `partial` oder `requires runtime evidence`.

### Response-Mapping
Response-Mapping wandelt Host-Response-/Header-/Body-Zustand in `msconnector_response` um. RESPONSE_BODY-Verhalten darf nur mit aktueller Runtime Evidence als verifiziert bezeichnet werden.

### Decision/Event/JSONL-Verhalten
Decision-, Intervention-, Status- und JSONL-Event-Helfer sind Common-Semantik. Per-run Event-Ausgabe ist nur Evidenz für diesen Lauf.

### Resource-/Body-/DoS-/Flow boundaries
Resource Limits, Body Policy, DoS Guard und Flow Guard sind connector-neutrale Kontrollen. Sie sind Guardrails und Governance-Modelle, keine runtime-secure- oder tamper-proof-Claims.

### C-Sprachstandard / Checks
C17 ist das erforderliche Compile-Profil, wenn Compiler und Header vorhanden sind. C23 und future-C sind optional. Exit 77 bedeutet BLOCKED/SKIPPED wegen fehlender Umgebung oder nicht unterstütztem optionalem Profil, nicht versteckter Compile-Fehler.

### CI-/Contract-Checks
Nutze connector-spezifische Common-Adoption- und C-Standard-Ziele plus gemeinsame Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
For NGINX-Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Was umgesetzt ist
Common-facing structure, metadata, docs/harness stubs or Connector-Quellen are present as listed below.

### Was fehlt
Fehlende Arbeit ist alles, was als `connector-gap`, `not_verified`, `structure-only`, `unknown` oder `requires runtime evidence` markiert ist, besonders echte Runtime-Integration für Starter-Connectoren.

### Was connector-spezifisch bleibt
ngx_http_request_t, ngx_command_t, ngx_chain_t, ngx_buf_t, Headers_in/Headers_out, filters, pools, return codes and NGINX module build glue bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Dateien des Connectors
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/nginx/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/README.de.md` | README.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/TODO.md` | TODO helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/config` | connector-neutral configuration object, defaults, merge and validation | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/docs/build.md` | build helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/docs/validation.md` | validation helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/harness/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/harness/run_nginx_smoke.sh` | run nginx smoke helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/metadata.c` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/metadata.h` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ddebug.h` | ddebug helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | ngx http modsecurity access helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | ngx http modsecurity body filter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | ngx http modsecurity common helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_Header_filter.c` | ngx http modsecurity Header filter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | ngx http modsecurity log helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.c` | ngx http modsecurity mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.h` | ngx http modsecurity mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | ngx http modsecurity module helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |

## HAProxy-Connector

### Zweck des Connectors
Der HAProxy-Connector belässt Host-/Server-API-Arbeit in `connectors/haproxy/` und adoptiert Common-Config, Mapping, Decision-, Status-, Event- und Metadaten-Contracts, soweit umgesetzt.

### Aktueller Status
common SDK adoption present; runtime claims require current harness/report evidence.

### Common-SDK-Adoption
Der Connector soll, soweit passend, `msconnector_config`, Direktiven-Vokabular, Mapper-Contracts, Request-/Response-Modelle, Status-/Decision-/Event-Helfer und Common-Source-Linking verwenden. Adoption-Checks sind Compile-/Static-/Contract-Evidenz, keine automatische Runtime Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Nicht unterstützte oder host-spezifische Syntax muss als `not supported`, `not applicable`, `connector-gap` oder `structure-only` markiert werden; Apache-artige Expressions dürfen nicht stillschweigend als NGINX-Syntax akzeptiert werden.

### Request-Mapping
Request-Mapping wandelt Host-Request-Objekte in `msconnector_request` und Header-Helfer um. Fehlende Host-Details sind `partial` oder `requires runtime evidence`.

### Response-Mapping
Response-Mapping wandelt Host-Response-/Header-/Body-Zustand in `msconnector_response` um. RESPONSE_BODY-Verhalten darf nur mit aktueller Runtime Evidence als verifiziert bezeichnet werden.

### Decision/Event/JSONL-Verhalten
Decision-, Intervention-, Status- und JSONL-Event-Helfer sind Common-Semantik. Per-run Event-Ausgabe ist nur Evidenz für diesen Lauf.

### Resource-/Body-/DoS-/Flow boundaries
Resource Limits, Body Policy, DoS Guard und Flow Guard sind connector-neutrale Kontrollen. Sie sind Guardrails und Governance-Modelle, keine runtime-secure- oder tamper-proof-Claims.

### C-Sprachstandard / Checks
C17 ist das erforderliche Compile-Profil, wenn Compiler und Header vorhanden sind. C23 und future-C sind optional. Exit 77 bedeutet BLOCKED/SKIPPED wegen fehlender Umgebung oder nicht unterstütztem optionalem Profil, nicht versteckter Compile-Fehler.

### CI-/Contract-Checks
Nutze connector-spezifische Common-Adoption- und C-Standard-Ziele plus gemeinsame Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
For HAProxy-Connector, trust current metadata and generated reports only. Envoy, Traefik and lighttpd explicitly remain `not_verified / connector-gap` until real runtime evidence exists.

### Was umgesetzt ist
Common-facing structure, metadata, docs/harness stubs or Connector-Quellen are present as listed below.

### Was fehlt
Fehlende Arbeit ist alles, was als `connector-gap`, `not_verified`, `structure-only`, `unknown` oder `requires runtime evidence` markiert ist, besonders echte Runtime-Integration für Starter-Connectoren.

### Was connector-spezifisch bleibt
SPOE/SPOP, frame parsing, runtime loop, socket handling, HAProxy cfg snippets, process lifecycle and build glue bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Dateien des Connectors
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/haproxy/Makefile` | Makefile helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/README.de.md` | README.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/TODO.md` | TODO helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/build.md` | build helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/evidence-findings.de.md` | evidence-findings.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/evidence-findings.md` | evidence-findings helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/evidence-questionnaire.de.md` | evidence-questionnaire.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/evidence-questionnaire.md` | evidence-questionnaire helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/integration-decision.md` | integration-decision helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/spoe-external-evidence.de.md` | spoe-external-evidence.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/spoe-external-evidence.md` | spoe-external-evidence helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/spoe-minimal-artifacts.md` | spoe-minimal-artifacts helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/spoe-poc-plan.md` | spoe-poc-plan helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/test-framework-contract.md` | test-framework-contract helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/docs/validation.md` | validation helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/harness/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | run haproxy smoke helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/metadata.c` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/metadata.h` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/agent/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/agent/design.md` | design helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/harness/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/harness/design.md` | design helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/reports/README.de.md` | README.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/reports/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/poc/spoe/syntax-validation.md` | syntax-validation helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_modsecurity_binding.c` | haproxy modsecurity binding helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_modsecurity_binding.h` | haproxy modsecurity binding helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c` | haproxy modsecurity binding self test helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.c` | haproxy modsecurity mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.h` | haproxy modsecurity mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | haproxy spoa agent starter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | haproxy spoa agent starter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_spoa_main.c` | haproxy spoa main helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | haproxy spop diagnostic runtime helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | implemented or dokumentiert; benötigt Evidenz für Runtime-Claims |

## Envoy-Connector

### Zweck des Connectors
Der Envoy-Connector belässt Host-/Server-API-Arbeit in `connectors/envoy/` und adoptiert Common-Config, Mapping, Decision-, Status-, Event- und Metadaten-Contracts, soweit umgesetzt.

### Aktueller Status
not_verified / connector-gap; Starter / structure-only / compile-only; kein Production-, CRS-, Full-Matrix- oder RESPONSE_BODY-Claim.

### Common-SDK-Adoption
Der Connector soll, soweit passend, `msconnector_config`, Direktiven-Vokabular, Mapper-Contracts, Request-/Response-Modelle, Status-/Decision-/Event-Helfer und Common-Source-Linking verwenden. Adoption-Checks sind Compile-/Static-/Contract-Evidenz, keine automatische Runtime Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Nicht unterstützte oder host-spezifische Syntax muss als `not supported`, `not applicable`, `connector-gap` oder `structure-only` markiert werden; Apache-artige Expressions dürfen nicht stillschweigend als NGINX-Syntax akzeptiert werden.

### Request-Mapping
Request-Mapping wandelt Host-Request-Objekte in `msconnector_request` und Header-Helfer um. Fehlende Host-Details sind `partial` oder `requires runtime evidence`.

### Response-Mapping
Response-Mapping wandelt Host-Response-/Header-/Body-Zustand in `msconnector_response` um. RESPONSE_BODY-Verhalten darf nur mit aktueller Runtime Evidence als verifiziert bezeichnet werden.

### Decision/Event/JSONL-Verhalten
Decision-, Intervention-, Status- und JSONL-Event-Helfer sind Common-Semantik. Per-run Event-Ausgabe ist nur Evidenz für diesen Lauf.

### Resource-/Body-/DoS-/Flow boundaries
Resource Limits, Body Policy, DoS Guard und Flow Guard sind connector-neutrale Kontrollen. Sie sind Guardrails und Governance-Modelle, keine runtime-secure- oder tamper-proof-Claims.

### C-Sprachstandard / Checks
C17 ist das erforderliche Compile-Profil, wenn Compiler und Header vorhanden sind. C23 und future-C sind optional. Exit 77 bedeutet BLOCKED/SKIPPED wegen fehlender Umgebung oder nicht unterstütztem optionalem Profil, nicht versteckter Compile-Fehler.

### CI-/Contract-Checks
Nutze connector-spezifische Common-Adoption- und C-Standard-Ziele plus gemeinsame Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Für den Envoy-Connector gelten nur aktuelle Metadaten und generierte Reports. Envoy, Traefik und lighttpd bleiben ausdrücklich `not_verified / connector-gap`, bis echte Runtime Evidence existiert.

### Was umgesetzt ist
Common-facing structure, metadata, docs/harness stubs or Connector-Quellen are present as listed below.

### Was fehlt
Fehlende Arbeit ist alles, was als `connector-gap`, `not_verified`, `structure-only`, `unknown` oder `requires runtime evidence` markiert ist, besonders echte Runtime-Integration für Starter-Connectoren.

### Was connector-spezifisch bleibt
Envoy filter/runtime API, native Envoy SDK ownership and deployed proxy integration bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Dateien des Connectors
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/envoy/Makefile` | Makefile helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/envoy/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/README.de.md` | README.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/TODO.md` | TODO helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/build/build_metadata.sh` | build metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/build.md` | build helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/docs/validation.md` | validation helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/harness/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/envoy/harness/run_envoy_smoke.sh` | run envoy smoke helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/envoy/metadata.c` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/metadata.h` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/envoy/src/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_bridge.c` | envoy bridge helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_bridge.h` | envoy bridge helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_bridge_main.c` | envoy bridge main helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/envoy/src/envoy_modsecurity_mapper.h` | envoy modsecurity mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |

## Traefik-Connector

### Zweck des Connectors
Der Traefik-Connector belässt Host-/Server-API-Arbeit in `connectors/traefik/` und adoptiert Common-Config, Mapping, Decision-, Status-, Event- und Metadaten-Contracts, soweit umgesetzt.

### Aktueller Status
not_verified / connector-gap; Starter / structure-only / compile-only; kein Production-, CRS-, Full-Matrix- oder RESPONSE_BODY-Claim.

### Common-SDK-Adoption
Der Connector soll, soweit passend, `msconnector_config`, Direktiven-Vokabular, Mapper-Contracts, Request-/Response-Modelle, Status-/Decision-/Event-Helfer und Common-Source-Linking verwenden. Adoption-Checks sind Compile-/Static-/Contract-Evidenz, keine automatische Runtime Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Nicht unterstützte oder host-spezifische Syntax muss als `not supported`, `not applicable`, `connector-gap` oder `structure-only` markiert werden; Apache-artige Expressions dürfen nicht stillschweigend als NGINX-Syntax akzeptiert werden.

### Request-Mapping
Request-Mapping wandelt Host-Request-Objekte in `msconnector_request` und Header-Helfer um. Fehlende Host-Details sind `partial` oder `requires runtime evidence`.

### Response-Mapping
Response-Mapping wandelt Host-Response-/Header-/Body-Zustand in `msconnector_response` um. RESPONSE_BODY-Verhalten darf nur mit aktueller Runtime Evidence als verifiziert bezeichnet werden.

### Decision/Event/JSONL-Verhalten
Decision-, Intervention-, Status- und JSONL-Event-Helfer sind Common-Semantik. Per-run Event-Ausgabe ist nur Evidenz für diesen Lauf.

### Resource-/Body-/DoS-/Flow boundaries
Resource Limits, Body Policy, DoS Guard und Flow Guard sind connector-neutrale Kontrollen. Sie sind Guardrails und Governance-Modelle, keine runtime-secure- oder tamper-proof-Claims.

### C-Sprachstandard / Checks
C17 ist das erforderliche Compile-Profil, wenn Compiler und Header vorhanden sind. C23 und future-C sind optional. Exit 77 bedeutet BLOCKED/SKIPPED wegen fehlender Umgebung oder nicht unterstütztem optionalem Profil, nicht versteckter Compile-Fehler.

### CI-/Contract-Checks
Nutze connector-spezifische Common-Adoption- und C-Standard-Ziele plus gemeinsame Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Für den Traefik-Connector gelten nur aktuelle Metadaten und generierte Reports. Envoy, Traefik und lighttpd bleiben ausdrücklich `not_verified / connector-gap`, bis echte Runtime Evidence existiert.

### Was umgesetzt ist
Common-facing structure, metadata, docs/harness stubs or Connector-Quellen are present as listed below.

### Was fehlt
Fehlende Arbeit ist alles, was als `connector-gap`, `not_verified`, `structure-only`, `unknown` oder `requires runtime evidence` markiert ist, besonders echte Runtime-Integration für Starter-Connectoren.

### Was connector-spezifisch bleibt
Traefik middleware/proxy/runtime API and real traffic path integration bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Dateien des Connectors
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/traefik/Makefile` | Makefile helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/README.de.md` | README.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/TODO.md` | TODO helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/build/build-starter.sh` | build-starter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/build.md` | build helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/docs/validation.md` | validation helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/harness/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/harness/run_traefik_smoke.sh` | run traefik smoke helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/metadata.c` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/metadata.h` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/traefik/src/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_build_starter.c` | traefik build starter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_decision_service.c` | traefik decision service helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_decision_service.h` | traefik decision service helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_decision_service_main.c` | traefik decision service main helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/traefik/src/traefik_modsecurity_mapper.h` | traefik modsecurity mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |

## lighttpd-Connector

### Zweck des Connectors
Der lighttpd-Connector belässt Host-/Server-API-Arbeit in `connectors/lighttpd/` und adoptiert Common-Config, Mapping, Decision-, Status-, Event- und Metadaten-Contracts, soweit umgesetzt.

### Aktueller Status
not_verified / connector-gap; Starter / structure-only / compile-only; kein Production-, CRS-, Full-Matrix- oder RESPONSE_BODY-Claim.

### Common-SDK-Adoption
Der Connector soll, soweit passend, `msconnector_config`, Direktiven-Vokabular, Mapper-Contracts, Request-/Response-Modelle, Status-/Decision-/Event-Helfer und Common-Source-Linking verwenden. Adoption-Checks sind Compile-/Static-/Contract-Evidenz, keine automatische Runtime Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Nicht unterstützte oder host-spezifische Syntax muss als `not supported`, `not applicable`, `connector-gap` oder `structure-only` markiert werden; Apache-artige Expressions dürfen nicht stillschweigend als NGINX-Syntax akzeptiert werden.

### Request-Mapping
Request-Mapping wandelt Host-Request-Objekte in `msconnector_request` und Header-Helfer um. Fehlende Host-Details sind `partial` oder `requires runtime evidence`.

### Response-Mapping
Response-Mapping wandelt Host-Response-/Header-/Body-Zustand in `msconnector_response` um. RESPONSE_BODY-Verhalten darf nur mit aktueller Runtime Evidence als verifiziert bezeichnet werden.

### Decision/Event/JSONL-Verhalten
Decision-, Intervention-, Status- und JSONL-Event-Helfer sind Common-Semantik. Per-run Event-Ausgabe ist nur Evidenz für diesen Lauf.

### Resource-/Body-/DoS-/Flow boundaries
Resource Limits, Body Policy, DoS Guard und Flow Guard sind connector-neutrale Kontrollen. Sie sind Guardrails und Governance-Modelle, keine runtime-secure- oder tamper-proof-Claims.

### C-Sprachstandard / Checks
C17 ist das erforderliche Compile-Profil, wenn Compiler und Header vorhanden sind. C23 und future-C sind optional. Exit 77 bedeutet BLOCKED/SKIPPED wegen fehlender Umgebung oder nicht unterstütztem optionalem Profil, nicht versteckter Compile-Fehler.

### CI-/Contract-Checks
Nutze connector-spezifische Common-Adoption- und C-Standard-Ziele plus gemeinsame Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Für den lighttpd-Connector gelten nur aktuelle Metadaten und generierte Reports. Envoy, Traefik und lighttpd bleiben ausdrücklich `not_verified / connector-gap`, bis echte Runtime Evidence existiert.

### Was umgesetzt ist
Common-facing structure, metadata, docs/harness stubs or Connector-Quellen are present as listed below.

### Was fehlt
Fehlende Arbeit ist alles, was als `connector-gap`, `not_verified`, `structure-only`, `unknown` oder `requires runtime evidence` markiert ist, besonders echte Runtime-Integration für Starter-Connectoren.

### Was connector-spezifisch bleibt
lighttpd plugin/proxy/runtime API and FastCGI/SCGI/native module integration bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Dateien des Connectors
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/lighttpd/Makefile` | Makefile helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/ORIGIN.md` | ORIGIN helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/README.de.md` | README.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/SOURCE_MAP.json` | SOURCE MAP helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/TODO.md` | TODO helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/build/bridge_starter.sh` | bridge starter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/build/build_starter.sh` | build starter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/architecture.md` | architecture helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/build.md` | build helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/coverage-decision-matrix.de.md` | coverage-decision-matrix.de helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/coverage-decision-matrix.md` | coverage-decision-matrix helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/public-sources.md` | public-sources helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/docs/validation.md` | validation helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/harness/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/harness/run_lighttpd_smoke.sh` | run lighttpd smoke helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/metadata.c` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/metadata.h` | metadata helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | metadata/docs | not_verified / connector-gap |
| `connectors/lighttpd/src/README.md` | README helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_bridge.c` | lighttpd bridge helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_bridge.h` | lighttpd bridge helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_bridge_main.c` | lighttpd bridge main helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_build_starter.c` | lighttpd build starter helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |
| `connectors/lighttpd/src/lighttpd_modsecurity_mapper.h` | lighttpd modsecurity mapper helper/model for the connector-neutral SDK | nutzt Common-Contracts, soweit eingebunden; siehe Source | yes | not_verified / connector-gap |

## Connector-Statusmatrix

| Connector | Current status | Common adoption | Runtime evidence | Forbidden inference |
|---|---|---|---|---|
| Apache | implementierte Connector-Quellen | present | benötigt aktuelle Reports/Harness-Ausgabe | no production/runtime/CRS/full-matrix claim |
| NGINX | implementierte Connector-Quellen | present | benötigt aktuelle Reports/Harness-Ausgabe | no production/runtime/CRS/full-matrix claim |
| HAProxy | SPOA/starter plus mapper/binding Source | present/partial | benötigt aktuelle Reports/Harness-Ausgabe | no production/runtime/CRS/full-matrix claim |
| Envoy | starter/structure-only/compile-only | prepared | missing | no production, CRS, full-matrix or RESPONSE_BODY claim |
| Traefik | starter/structure-only/compile-only | prepared | missing; per-run result only if run | no production, CRS, full-matrix or RESPONSE_BODY claim |
| lighttpd | starter/structure-only/compile-only | prepared | missing | no production, CRS, full-matrix or RESPONSE_BODY claim |

## Test-Framework-Bezug

Das wiederverwendbare Test-Framework wird unter `modules/ModSecurity-test-Framework` erwartet. Framework-abhängige Ziele können BLOCKED sein, wenn das Submodule oder seine Inputs fehlen. Das bedeutet nicht automatisch, dass Common-/Connector-Compile-Checks fehlgeschlagen sind.

## Runtime Evidence und Verification Policy

Connector-Metadatenfelder wie `runtime_status`, `verification_status`, `not_verified` and `connector-gap` beschreiben den Repository-weiten Connector-Status. Per-run `result.json` fields such as `status: PASS/BLOCKED/FAIL`, `runtime_verified: true/false` and `runtime_status: verified/blocked/...` beschreiben nur diesen Lauf. Ein Starter-Smoke kann per-run PASS oder sogar `runtime_verified: true` für diesen Lauf erzeugen, aber das ändert Connector-Metadaten nicht automatisch von `not_verified / connector-gap`.

## Was bereits umgesetzt ist

Umgesetzte Repository-Fakten umfassen the Common SDK, config/directive/parser model, request/response mapper contracts, common security/data-flow guard helpers, Apache/NGINX/HAProxy common-adoption structures, Envoy/Traefik/lighttpd starter preparation, C17/C23/future-C check wiring, CI/governance scripts and generated docs/reports areas. Behandle dies jeweils als Static-/Compile-/Governance-Evidenz, sofern keine aktuelle spezifische Runtime Evidence vorliegt.

## Was noch fehlt

Fehlende oder zukünftige Arbeit umfasst real runtime evidence for Envoy, Traefik and lighttpd; CRS matrix evidence; RESPONSE_BODY runtime evidence; full-matrix verification; production hardening; HMAC/signed event chains if desired; append-only evidence storage if desired; and additional runtime harnesses.

## Bekannte Grenzen

Bekannte Grenzen sind connector-specific host APIs, umgebungsabhängige Header/Toolchains, Framework-/Submodule-Blocker, Starter-only-Connectoren, partial/unknown runtime coverage and Dokumentation that must be kept synchronized with metadata and reports.

## Was bewusst connector-spezifisch bleibt

Apache request/APR/filter/APXS details, NGINX request/chain/filter/module glue, HAProxy SPOE/SPOP/frame/runtime loop, Envoy APIs, Traefik APIs and lighttpd APIs bleiben außerhalb von `common/`.

## KI-Faktenblock

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

## Erlaubte und verbotene Claims

Erlaubte Claims: connector-neutral common semantics, C17 required check when environment exists, optional C23/future-C, compile-only/static/governance checks, starter/structure-only status and per-run evidence scoped to that run. Ohne aktuelle Evidenz verboten: production-ready, runtime secure, security verified, CRS verified, full matrix verified, response body verified, runtime verified, production hardened, tamper-proof and cryptographic integrity.

## Glossar

- `common`: connector-neutrales SDK und Semantik.
- `connector-gap`: bekannte Lücke zwischen Starter/Struktur und echter Connector-Runtime-Integration.
- `not_verified`: kein aktueller Repository-weiter Runtime-Verifikations-Claim.
- `structure-only`: Dateien/Scaffolding existieren, beweisen aber kein Runtime-Verhalten.
- `compile-only`: nur Compiler-/Static-Check-Evidenz.
- `runtime evidence`: aktueller Lauf/Report, der konkretes Runtime-Verhalten belegt.
- `SOURCE_MAP`: Connector-Source-/Origin-/Status-Mapping-Metadaten.

## Wartungs-Checkliste

```text
- Neue Common-Datei -> Common-SDK-Dateiindex aktualisieren.
- New directive -> update directives.h, directive_spec, directive_adapter and docs.
- Neuer Parser -> Config-/Directive-Tabelle aktualisieren.
- Neuer Connector -> Statusmatrix aktualisieren.
- Neuer C-Source -> C17-Source-Liste aktualisieren.
- Neuer Header -> Header-Smoke-Checks aktualisieren.
- Neuer Mapper -> Ownership/Cleanup prüfen.
- Status change -> keep metadata, SOURCE_MAP, reports and docs synchronized.
- Keep German docs synchronized with English docs.
- Runtime-Claims nur mit Evidence.
```
