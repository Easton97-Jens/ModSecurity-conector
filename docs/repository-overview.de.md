# Überblick über das ModSecurity-Connector-Repository

**Sprache:** [English](repository-overview.md) | Deutsch

## Inhaltsverzeichnis

1. [Zweck des Repositorys](#zweck-des-repositorys)
2. [Kurzfassung für Menschen](#kurzfassung-für-menschen)
3. [Kurzfassung für KI-Systeme](#kurzfassung-für-ki-systeme)
4. [Architekturprinzip](#architekturprinzip)
5. [Repository-Struktur](#repository-struktur)
6. [Common SDK: vollständiger Dateiindex](#common-sdk-vollständiger-dateiindex)
7. [Common SDK: Module und Aufgaben](#common-sdk-module-und-aufgaben)
8. [Config-, Direktiven- und Parser-Modell](#config-direktiven-und-parser-modell)
9. [Erlaubte Config-/Directive-Begriffe](#erlaubte-config-directive-begriffe)
10. [Request-/Response-Mapping](#request-response-mapping)
11. [Decision-, Intervention-, Status- und Event-Modell](#decision-intervention-status-und-event-modell)
12. [Ressourcenlimits, DoS-Schutz, Flow-Guard und Integrität](#ressourcenlimits-dos-schutz-flow-guard-und-integrität)
13. [C-Sprache und Standards](#c-sprache-und-standards)
14. [CI-, Contract- und Governance-Checks](#ci-contract-und-governance-checks)
15. [Makefile-Ziele: Was kann man mit `make` tun?](#makefile-ziele-was-kann-man-mit-make-tun)
16. [Häufige Makefile-Aufrufe](#häufige-makefile-aufrufe)
17. [Exit-Codes und BLOCKED/SKIPPED-Verhalten](#exit-codes-und-blockedskipped-verhalten)
18. [Umgebungsvariablen](#umgebungsvariablen)
19. [Connector-Modell](#connector-modell)
20. [Apache-Connector](#apache-connector)
21. [NGINX-Connector](#nginx-connector)
22. [HAProxy-Connector](#haproxy-connector)
23. [Envoy-Connector](#envoy-connector)
24. [Traefik-Connector](#traefik-connector)
25. [lighttpd-Connector](#lighttpd-connector)
26. [Connector-Statusmatrix](#connector-statusmatrix)
27. [Test-Framework-Bezug](#test-framework-bezug)
28. [Runtime-Evidence und Verifikationsrichtlinie](#runtime-evidence-und-verifikationsrichtlinie)
29. [Umgesetzt](#umgesetzt)
30. [Fehlend / Nächste Schritte](#fehlend--nächste-schritte)
31. [Bekannte Grenzen](#bekannte-grenzen)
32. [Bewusst connector-spezifisch](#bewusst-connector-spezifisch)
33. [KI-Faktenblock](#ki-faktenblock)
34. [Erlaubte und verbotene Claims](#erlaubte-und-verbotene-claims)
35. [Glossar](#glossar)
36. [Wartungs-Checkliste](#wartungs-checkliste)

## Zweck des Repositorys

Dieses Repository baut ModSecurity-Connectoren und eine gemeinsame Common-SDK-Schicht. Das Architekturziel ist, connector-neutrale Semantik in `common/` zu halten und Host-/Server-API-Integration in den einzelnen Connector-Verzeichnissen zu belassen.

Grundsatz: Semantische Logik gehört nach `common/`; Host-/Server-API-Glue bleibt im jeweiligen Connector.

Beispiele für Common sind Konfiguration, Direktiven, Direktiven-Spezifikationen, Parser-Helfer, Request- und Response-Modelle, Header-Helfer, Mapper-Verträge, Entscheidungs-/Interventions-/Status-/Fehlermodelle, Event JSONL, Ressourcenlimits, DoS-Schutz, Flow-Guard, Integritätsmetadaten, Rule-Loading-Verträge, Test-Result-JSON, Adapter-Metadaten, Capabilities und generische Mapper-Helfer.

Beispiele für connector-spezifische Teile sind Apache `request_rec`, `command_rec`, APR-Pools und Filter; NGINX `ngx_http_request_t`, `ngx_chain_t` und Filter; HAProxy SPOE/SPOP, Frame-Parsing und Runtime-Loop; Envoy Filter-/Runtime-APIs; Traefik Middleware-/Proxy-/Runtime-APIs; und lighttpd Plugin-/Proxy-/Runtime-APIs.

## Kurzfassung für Menschen

Alle sechs Connector-Bereiche enthalten echte Hostpfad-Implementierungen.
Envoy, Traefik und lighttpd besitzen enge `minimal_runtime_smoke`-Evidence für
ihre gewählten Hostmodelle und werden nicht mehr als bloße Starter beschrieben.
Die kanonischen Capability-Manifeste liegen vor, die kanonische No-CRS-Baseline
wurde auf diesem Branch jedoch noch nicht ausgeführt. Nicht unterstützte, nicht
implementierte und nicht ausgeführte Fähigkeiten bleiben von verifiziertem
Verhalten getrennt.

## Kurzfassung für KI-Systeme

Nutze aktuellen Repository-Code, Capability-Manifeste, CI-Skripte, Metadaten
und generierte Reports als Source of Truth. Leite keine Runtime-Garantien aus
Dateinamen, Makefile-Zielen, Legacy-Smokes oder lokalen `result.json`-Dateien
ab. Unterscheide Implementierungsstatus von kanonischer Evidence pro Lauf.
Wenn Evidence fehlt, verwende passend zu Manifest und Result-Vertrag
`NOT EXECUTED`, `IMPLEMENTED, NOT ASSERTED`, `UNSUPPORTED` oder `NOT
IMPLEMENTED`.

## Architekturprinzip

`common/` definiert connector-neutrale C/C++-Verträge und Helfer. `connectors/<name>/` bildet Server-APIs auf diese Verträge ab. Generierte Reports liegen unter `reports/`; CI- und Governance-Skripte liegen in `ci/`; wiederverwendbare Tests werden unter `modules/ModSecurity-test-Framework` erwartet.

## Repository-Struktur

| Pfad | Bedeutung | Evidenzstatus |
|---|---|---|
| `common/include/msconnector/` | Öffentliche Common-SDK-Header. | Contract-/statische Evidence, sofern kein Lauf zusätzliche Runtime-Evidence belegt. |
| `common/src/` | Implementierungen der Common-SDK-Helfer. | C17-/Common-Checks. |
| `connectors/apache/` | Apache-Adapter-Quellen, Doku, Harness und Metadaten. | Common-Adoption; Runtime-Claims benötigen aktuelle Evidence. |
| `connectors/nginx/` | NGINX-Adapter-Quellen, Doku, Harness und Metadaten. | Common-Adoption; Runtime-Claims benötigen aktuelle Evidence. |
| `connectors/haproxy/` | HAProxy-/SPOA-Quellen, Doku, Harness und Metadaten. | Common-Adoption; Runtime-Claims benötigen aktuelle Evidence. |
| `connectors/envoy/` | Echter HTTP-`ext_authz`-Servicepfad. | Gezielter `minimal_runtime_smoke`; kanonisches No-CRS `NOT EXECUTED`. |
| `connectors/traefik/` | Echter HTTP-`forwardAuth`-Servicepfad. | Gezielter `minimal_runtime_smoke`; kanonisches No-CRS `NOT EXECUTED`. |
| `connectors/lighttpd/` | Nativer `mod_msconnector.so`-Pluginpfad. | Gezielter `minimal_runtime_smoke`; kanonisches No-CRS `NOT EXECUTED`. |
| `ci/` | Lint-, Contract-, Governance-, C-Standard- und Report-Skripte. | Check-Definitionen, für sich allein keine Runtime-Evidence. |
| `docs/`, `docs/architecture/`, `docs/connectors/` | Repository-, Architektur- und Connector-Dokumentation. | Dokumentation; muss mit Quellcode und Reports synchron bleiben. |
| `reports/` | Generierte Reports, Evidence und Matrizen. | Nur aktuellen Statuslabels und Evidenzumfang vertrauen. |

## Common SDK: vollständiger Dateiindex

| Datei | Typ | Zweck | Wichtige APIs/Structs | Genutzt von | Status / Hinweise |
|---|---|---|---|---|---|
| `common/include/msconnector/adapter.h` | Header | Adapter-Integrationsobjekt und gemeinsame Adapter-Lifecycle-Helfer | MSCONNECTOR_ADAPTER_H, msconnector_adapter, msconnector_adapter_metadata, msconnector_capabilities, msconnector_config, msconnector_error, msconnector_transaction_view, msconnector_decision | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/adapter_contract.h` | Header | Validierung des Adapter-Vertrags | MSCONNECTOR_ADAPTER_CONTRACT_H, msconnector_adapter_contract_result, msconnector_adapter_contract_result_init, msconnector_adapter_contract_validate, msconnector_adapter | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/adapter_metadata.h` | Header | Adapter-Metadaten sowie Origin-/Capability-Vollständigkeit | MSCONNECTOR_ADAPTER_METADATA_H, msconnector_adapter_metadata, msconnector_origin, msconnector_capabilities, msconnector_adapter_metadata_init, msconnector_adapter_metadata_is_complete | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/artifact_layout.h` | Header | Standardnamen für Lauf-Artefakte | MSCONNECTOR_ARTIFACT_LAYOUT_H, msconnector_artifact_layout, msconnector_artifact_layout_init, msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log, msconnector_artifact_name_runtime_stdout_log | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/artifacts.h` | Header | Helfer für Standard-Artefaktpfade | MSCONNECTOR_ARTIFACTS_H, msconnector_artifact_paths, msconnector_artifact_paths_init, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/block_statuses.h` | Header | Helfer für erlaubte und standardmäßige Block-/Fehlerstatus | MSCONNECTOR_BLOCK_STATUSES_H, MSCONNECTOR_DEFAULT_BLOCK_STATUS, MSCONNECTOR_DEFAULT_ERROR_STATUS, MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS, msconnector_block_status_support, msconnector_block_status_is_allowed, msconnector_block_status_normalize, msconnector_http_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/blocking.h` | Header | Helfer für Blocking-Policy und Blocking-Aktion | MSCONNECTOR_BLOCKING_H, msconnector_block_action, MSCONNECTOR_BLOCK_ACTION_DENY, MSCONNECTOR_BLOCK_ACTION_REDIRECT, MSCONNECTOR_BLOCK_ACTION_DROP, MSCONNECTOR_BLOCK_ACTION_LOG_ONLY, MSCONNECTOR_BLOCK_ACTION_ABORT_CONNECTION, msconnector_blocking_policy | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/body_policy.h` | Header | Modell für Body-Verarbeitung | MSCONNECTOR_BODY_POLICY_H, msconnector_body_mode, MSCONNECTOR_BODY_MODE_NONE, MSCONNECTOR_BODY_MODE_BUFFERED, MSCONNECTOR_BODY_MODE_STREAMING, msconnector_body_policy, msconnector_body_policy_init, msconnector_body_mode_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/build_contract.h` | Header | Build-Target-Namen und C-Standard-Vertrag | MSCONNECTOR_BUILD_CONTRACT_H, msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/capabilities.h` | Header | Capability-Flags und Capability-Lookups | MSCONNECTOR_CAPABILITIES_H, msconnector_capability_flags, msconnector_capability_flag, MSCONNECTOR_CAPABILITY_NONE, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED, MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/capabilities.hpp` | Header | Capability-Flags und Capability-Lookups | MSCONNECTOR_CAPABILITIES_HPP, msconnector_capability_flags, msconnector_capability_flag, msconnector_capabilities, msconnector_capability_name | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/capability_matrix.h` | Header | Zuordnung von Capabilities zu erforderlichen Tests | MSCONNECTOR_CAPABILITY_MATRIX_H, msconnector_capability_required_test, msconnector_capability_flag, msconnector_capability_has_required_test | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/config.h` | Header | Connector-neutrales Konfigurationsobjekt mit Defaults, Merge und Validierung | MSCONNECTOR_CONFIG_H, msconnector_config, msconnector_bool_option, msconnector_phase4_mode, msconnector_config_init, msconnector_config_apply_defaults, msconnector_config_merge, msconnector_config_validate | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/config_parser.h` | Header | Parser für Boolean-Werte, Phase-4-Modus, Größen, HTTP-Status und Content-Type-Tokens | MSCONNECTOR_CONFIG_PARSER_H, msconnector_parse_bool, msconnector_bool_option, msconnector_parse_phase4_mode, msconnector_phase4_mode, msconnector_parse_size, msconnector_parse_http_status, msconnector_validate_content_type_token | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/connector_manifest.h` | Header | Helfer für Connector-Manifest-JSON | MSCONNECTOR_CONNECTOR_MANIFEST_H, msconnector_connector_manifest, msconnector_capability_flags, msconnector_connector_manifest_init, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_connector_manifest_write_json | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/crs.h` | Header | Helfer für CRS-Konfiguration und CRS-Modus | MSCONNECTOR_CRS_H, msconnector_crs_mode, MSCONNECTOR_CRS_DISABLED, MSCONNECTOR_CRS_EXTERNAL_PATH, MSCONNECTOR_CRS_BUNDLED_PATH, MSCONNECTOR_CRS_TEST_FIXTURE, msconnector_crs_config, msconnector_crs_config_init | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/decision.h` | Header | Entscheidungsmodell für Inspektionsergebnisse | MSCONNECTOR_DECISION_H, msconnector_event, msconnector_decision_kind, MSCONNECTOR_DECISION_KIND_ALLOW, MSCONNECTOR_DECISION_KIND_LOG_ONLY, MSCONNECTOR_DECISION_KIND_DENY, MSCONNECTOR_DECISION_KIND_REDIRECT, MSCONNECTOR_DECISION_KIND_DROP | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/decision_action.h` | Header | Zuordnung von Entscheidungen zu Aktionen | MSCONNECTOR_DECISION_ACTION_H, msconnector_decision_action, MSCONNECTOR_DECISION_ACTION_ALLOW, MSCONNECTOR_DECISION_ACTION_DENY, MSCONNECTOR_DECISION_ACTION_REDIRECT, MSCONNECTOR_DECISION_ACTION_DROP, MSCONNECTOR_DECISION_ACTION_LOG_ONLY, MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/directive_adapter.h` | Header | Common-Katalog für Direktivenadapter und dessen Validierung | MSCONNECTOR_DIRECTIVE_ADAPTER_H, msconnector_directive_scope, MSCONNECTOR_DIRECTIVE_SCOPE_GLOBAL, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_SCOPE_LOCATION, MSCONNECTOR_DIRECTIVE_SCOPE_DIRECTORY, msconnector_directive_argument_policy, MSCONNECTOR_DIRECTIVE_ARG_NONE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/directive_spec.h` | Header | Globaler Katalog der Direktiven-Spezifikationen | MSCONNECTOR_DIRECTIVE_SPEC_H, msconnector_directive_value_type, MSCONNECTOR_DIRECTIVE_VALUE_BOOL, MSCONNECTOR_DIRECTIVE_VALUE_STRING, MSCONNECTOR_DIRECTIVE_VALUE_PATH, MSCONNECTOR_DIRECTIVE_VALUE_ENUM, MSCONNECTOR_DIRECTIVE_VALUE_SIZE, msconnector_directive_spec | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/directives.h` | Header | Kanonische Makros für Direktivenamen | MSCONNECTOR_DIRECTIVES_H, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_RULES_REMOTE, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID, MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR, MSCONNECTOR_DIRECTIVE_PHASE4_MODE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/dos_guard.h` | Header | DoS-Schutzprüfungen für Request und Response | MSCONNECTOR_DOS_GUARD_H, msconnector_dos_guard_check_request, msconnector_request, msconnector_resource_limits, msconnector_error, msconnector_dos_guard_check_response, msconnector_response, msconnector_dos_guard_check_event_json_size | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/error.h` | Header | Gemeinsames Fehlermodell mit Codes und Meldungen | MSCONNECTOR_ERROR_H, msconnector_error_code, MSCONNECTOR_ERROR_NONE, MSCONNECTOR_ERROR_INVALID_CONFIG, MSCONNECTOR_ERROR_RULE_PARSE_FAILED, MSCONNECTOR_ERROR_RULE_LOAD_FAILED, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/event.h` | Header | Ereignismodell | MSCONNECTOR_EVENT_H, msconnector_event_meta, msconnector_event_decision, msconnector_phase, msconnector_status, msconnector_event_http, msconnector_event_request, msconnector_event_integrity | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/event_jsonl.h` | Header | JSONL-Serialisierung von Ereignissen | MSCONNECTOR_EVENT_JSONL_H, msconnector_event_write_jsonl_line, msconnector_event | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/flow_guard.h` | Header | Ablaufwächter für Phasen-/Flow-Zustand | MSCONNECTOR_FLOW_GUARD_H, MSCONNECTOR_FLOW_GUARD_OK, MSCONNECTOR_FLOW_GUARD_INVALID, MSCONNECTOR_FLOW_GUARD_PHASE_ORDER, MSCONNECTOR_FLOW_GUARD_IMMUTABLE, MSCONNECTOR_FLOW_GUARD_DUPLICATE_MUTATION, msconnector_flow_guard, msconnector_phase | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/generic_mapper.h` | Header | Generischer Request-/Response-Mapper für Starter-Connectoren | MSCONNECTOR_GENERIC_MAPPER_H, msconnector_generic_request_source, msconnector_endpoint, msconnector_header, msconnector_bytes, msconnector_generic_response_source, msconnector_generic_config_init, msconnector_config | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/headers.h` | Header | Case-insensitive Header-Lookup-Helfer | MSCONNECTOR_HEADERS_H, msconnector_header_name_equals, msconnector_header, msconnector_header_name_is, msconnector_headers_find, msconnector_headers_find_first, msconnector_headers_find_last, msconnector_headers_count_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/http_status.h` | Header | Validierung und Klassifizierung von HTTP-Statuscodes | MSCONNECTOR_HTTP_STATUS_H, msconnector_http_status_class, MSCONNECTOR_HTTP_STATUS_CLASS_UNKNOWN, MSCONNECTOR_HTTP_STATUS_CLASS_INFORMATIONAL, MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS, MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION, MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/integrity_event.h` | Header | Integritätsmetadaten mit nicht-kryptografischen Hashes | MSCONNECTOR_INTEGRITY_EVENT_H, msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/intervention.h` | Header | Helfer für Interventionen und Blocking-Ergebnisse | MSCONNECTOR_INTERVENTION_H, msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/intervention.hpp` | Header | Helfer für Interventionen und Blocking-Ergebnisse | MSCONNECTOR_INTERVENTION_HPP, msconnector_intervention | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/json_escape.h` | Header | Helfer zum Escapen von JSON-Strings | MSCONNECTOR_JSON_ESCAPE_H, msconnector_json_escape | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/late_intervention.h` | Header | Helfer für Late-Intervention-Policy | MSCONNECTOR_LATE_INTERVENTION_H, msconnector_late_intervention_action, MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY, MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE, MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION, msconnector_late_intervention_policy, msconnector_late_intervention_policy_init, msconnector_late_intervention_action_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/lifecycle_status.h` | Header | Namen für Build-, Runtime- und Verifikationsstatus | MSCONNECTOR_LIFECYCLE_STATUS_H, msconnector_build_status, MSCONNECTOR_BUILD_STATUS_NOT_STARTED, MSCONNECTOR_BUILD_STATUS_STARTER, MSCONNECTOR_BUILD_STATUS_COMPILES, MSCONNECTOR_BUILD_STATUS_LINKS, MSCONNECTOR_BUILD_STATUS_RUNTIME_READY, msconnector_runtime_status | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/limits.h` | Header | Kompilierte Limit-Konstanten | MSCONNECTOR_LIMITS_H, MSCONNECTOR_MAX_HEADER_COUNT, MSCONNECTOR_MAX_HEADER_NAME_LENGTH, MSCONNECTOR_MAX_HEADER_VALUE_LENGTH, MSCONNECTOR_MAX_TOTAL_HEADER_BYTES, MSCONNECTOR_MAX_BODY_BUFFER_SIZE, MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE, MSCONNECTOR_MAX_EVENT_JSON_BYTES | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/log_sanitize.h` | Header | Helfer für Log-Redaktion und Sanitizing | MSCONNECTOR_LOG_SANITIZE_H, msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/logging.h` | Header | Connector-neutrales Logging-Callback-Modell | MSCONNECTOR_LOGGING_H, msconnector_log_level, MSCONNECTOR_LOG_TRACE, MSCONNECTOR_LOG_DEBUG, MSCONNECTOR_LOG_INFO, MSCONNECTOR_LOG_WARN, MSCONNECTOR_LOG_ERROR, msconnector_log_record | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/logging.hpp` | Header | Connector-neutrales Logging-Callback-Modell | MSCONNECTOR_LOGGING_HPP, msconnector_log_level, msconnector_log_record, msconnector_logger, msconnector_log | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/memory.h` | Header | Geprüfte Allokation und Allocator-Callbacks | MSCONNECTOR_MEMORY_H, msconnector_alloc_checked, msconnector_free_checked, msconnector_alloc_callback, msconnector_free_callback, msconnector_allocator, msconnector_allocator_init, msconnector_allocator_within_limit | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/modsecurity_engine.h` | Header | Connector-neutrale Operationstabelle für die ModSecurity-Engine | MSCONNECTOR_MODSECURITY_ENGINE_H, msconnector_modsecurity_engine_ops, msconnector_error, msconnector_request, msconnector_decision, msconnector_response, msconnector_modsecurity_engine, msconnector_modsecurity_transaction | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/options.h` | Header | Gemeinsame Options-Enums und Defaults | MSCONNECTOR_OPTIONS_H, MSCONNECTOR_OPTION_ENABLE, MSCONNECTOR_OPTION_RULES_INLINE, MSCONNECTOR_OPTION_RULES_FILE, MSCONNECTOR_OPTION_RULES_REMOTE, MSCONNECTOR_OPTION_TRANSACTION_ID, MSCONNECTOR_OPTION_USE_ERROR_LOG, MSCONNECTOR_OPTION_PHASE4_MODE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/origin.h` | Header | Helfer für Source-/Origin-Metadaten | MSCONNECTOR_ORIGIN_H, msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/origin.hpp` | Header | Helfer für Source-/Origin-Metadaten | MSCONNECTOR_ORIGIN_HPP, msconnector_origin, msconnector_origin_is_empty | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/origin_governance.h` | Header | Vollständigkeitsprüfungen für Origin-Governance | MSCONNECTOR_ORIGIN_GOVERNANCE_H, msconnector_origin_governance, msconnector_origin_governance_init, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/path_policy.h` | Header | Helfer zur Pfadvalidierung | MSCONNECTOR_PATH_POLICY_H, msconnector_path_is_absolute, msconnector_path_is_empty, msconnector_path_has_parent_reference | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/phase.h` | Header | Enum für ModSecurity-Phasen | MSCONNECTOR_PHASE_H, msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_URI, MSCONNECTOR_PHASE_REQUEST_HEADERS, MSCONNECTOR_PHASE_REQUEST_BODY, MSCONNECTOR_PHASE_RESPONSE_HEADERS, MSCONNECTOR_PHASE_RESPONSE_BODY | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/redaction.h` | Header | Helfer zur String-Redaktion | MSCONNECTOR_REDACTION_H, msconnector_redacted_string, msconnector_redact_copy | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/request.h` | Header | Connector-neutrales Request-Modell | MSCONNECTOR_REQUEST_H, msconnector_bytes, msconnector_header, msconnector_endpoint, msconnector_request | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/request.hpp` | Header | Connector-neutrales Request-Modell | MSCONNECTOR_REQUEST_HPP, msconnector_bytes, msconnector_header, msconnector_endpoint, msconnector_request, msconnector_request_init, msconnector_request_validate | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/request_helpers.h` | Header | Helfer für Request-Initialisierung und -Validierung | MSCONNECTOR_REQUEST_HELPERS_H, msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_resource_limits, msconnector_request_has_header, msconnector_request_header_value | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/request_mapper_contract.h` | Header | Validierung des Request-Mapper-Vertrags | MSCONNECTOR_REQUEST_MAPPER_CONTRACT_H, msconnector_mapper_requirement, MSCONNECTOR_MAPPER_REQUIRED, MSCONNECTOR_MAPPER_OPTIONAL, MSCONNECTOR_MAPPER_UNSUPPORTED, msconnector_request_mapper_contract, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract_validate | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/resource_limits.h` | Header | Ressourcenlimits und Validatoren | MSCONNECTOR_RESOURCE_LIMITS_H, msconnector_resource_limits, msconnector_resource_limits_init, msconnector_resource_limits_validate, msconnector_resource_limits_headers_ok, msconnector_header, msconnector_resource_limits_body_ok | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/response.h` | Header | Connector-neutrales Response-Modell | MSCONNECTOR_RESPONSE_H, msconnector_response, msconnector_header, msconnector_bytes | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/response.hpp` | Header | Connector-neutrales Response-Modell | MSCONNECTOR_RESPONSE_HPP, msconnector_response, msconnector_response_init, msconnector_response_validate | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/response_helpers.h` | Header | Helfer für Response-Initialisierung und -Validierung | MSCONNECTOR_RESPONSE_HELPERS_H, msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_response_validate_with_limits, msconnector_resource_limits, msconnector_response_has_header, msconnector_response_header_value | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/response_mapper_contract.h` | Header | Validierung des Response-Mapper-Vertrags | MSCONNECTOR_RESPONSE_MAPPER_CONTRACT_H, msconnector_response_mapper_contract, msconnector_mapper_requirement, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output, msconnector_response | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/rule_error.h` | Header | Helfer für Fehler beim Laden von Regeln | MSCONNECTOR_RULE_ERROR_H, msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_rule_error_set_load_failed, msconnector_rule_error_clear | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/rule_event.h` | Header | Helfer für Ereignisse beim Laden von Regeln | MSCONNECTOR_RULE_EVENT_H, msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_rule_load_event, msconnector_rule_error_event, msconnector_error | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/rule_id.h` | Header | Kopieren, Extrahieren und Validieren von Rule-IDs | MSCONNECTOR_RULE_ID_H, msconnector_rule_id_copy, msconnector_rule_id_extract_from_message, msconnector_rule_id_validate | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/rule_load_stats.h` | Header | Statistikmodell für geladenen Regeln | MSCONNECTOR_RULE_LOAD_STATS_H, msconnector_rule_load_stats, msconnector_rule_load_stats_init, msconnector_rule_load_stats_add, msconnector_rule_load_stats_add_inline, msconnector_rule_load_stats_add_file, msconnector_rule_load_stats_add_remote | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/rule_loader.h` | Header | Backend-Vertrag für das Laden von Regeln | MSCONNECTOR_RULE_LOADER_H, msconnector_rule_loader_backend, msconnector_error, msconnector_rule_loader, msconnector_rule_load_stats, msconnector_rule_loader_init, msconnector_rule_loader_add_inline, msconnector_rule_loader_add_file | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/rule_merge.h` | Header | Helfer zum Zusammenführen von Rule Collections | MSCONNECTOR_RULE_MERGE_H, msconnector_rule_collection, msconnector_rule_collection_init, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/runtime_paths.h` | Header | Helfer zum Zusammenfügen von Runtime-Pfaden | MSCONNECTOR_RUNTIME_PATHS_H, msconnector_runtime_path_join | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/runtime_report.h` | Header | Helfer für Runtime-Report-JSON | MSCONNECTOR_RUNTIME_REPORT_H, msconnector_runtime_report, msconnector_status, msconnector_runtime_report_init, msconnector_runtime_report_write_json | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/status.h` | Header | Gemeinsame Status-Helfer für PASS/FAIL/BLOCKED-artige Zustände | MSCONNECTOR_STATUS_H, msconnector_status, MSCONNECTOR_STATUS_OK, MSCONNECTOR_STATUS_ERROR, MSCONNECTOR_STATUS_BLOCKED, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_status_name, msconnector_status_from_result | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/status.hpp` | Header | Gemeinsame Status-Helfer für PASS/FAIL/BLOCKED-artige Zustände | MSCONNECTOR_STATUS_HPP, msconnector_status, msconnector_status_name | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/test_result.h` | Header | Test-Result-Modell | MSCONNECTOR_TEST_RESULT_H, msconnector_test_result, msconnector_status, msconnector_test_result_init, msconnector_test_result_passed | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/test_result_json.h` | Header | JSON-Schreiber für Test-Resultate | MSCONNECTOR_TEST_RESULT_JSON_H, msconnector_test_result_write_json, msconnector_test_result | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/transaction.h` | Header | Helfer für Transaction Views | MSCONNECTOR_TRANSACTION_H, msconnector_transaction_view, msconnector_request, msconnector_response, msconnector_intervention | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/transaction.hpp` | Header | Helfer für Transaction Views | MSCONNECTOR_TRANSACTION_HPP, msconnector_transaction_view, msconnector_transaction_state, msconnector_decision, msconnector_phase, msconnector_phase_name | Common SDK und adoptierende Connectoren | C++-Fassade |
| `common/include/msconnector/transaction_id.h` | Header | Helfer für Transaction-ID-Quelle und -Auswertung | MSCONNECTOR_TRANSACTION_ID_H, msconnector_transaction_id_source, MSCONNECTOR_TRANSACTION_ID_SOURCE_NONE, MSCONNECTOR_TRANSACTION_ID_SOURCE_STATIC, MSCONNECTOR_TRANSACTION_ID_SOURCE_EXPR, MSCONNECTOR_TRANSACTION_ID_SOURCE_HOST, MSCONNECTOR_TRANSACTION_ID_SOURCE_HEADER, MSCONNECTOR_TRANSACTION_ID_SOURCE_FALLBACK | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/include/msconnector/transaction_state.h` | Header | Zustand der verarbeiteten Transaction-Phasen | MSCONNECTOR_TRANSACTION_STATE_H, msconnector_transaction_state, msconnector_transaction_state_init, msconnector_transaction_state_mark_phase, msconnector_phase, msconnector_transaction_state_phase_processed, msconnector_phase_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/README.md` | Dokumentation | Hinweise zum Common-Source-Layout | macros / declarations | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/adapter.c` | Source | Adapter-Integrationsobjekt und gemeinsame Adapter-Lifecycle-Helfer | msconnector_adapter_init, msconnector_adapter, msconnector_adapter_has_metadata, msconnector_adapter_has_capabilities, msconnector_adapter_supports_phase, msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_REQUEST_HEADERS | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/adapter_contract.c` | Source | Validierung des Adapter-Vertrags | msconnector_adapter_contract_result, msconnector_capabilities, msconnector_capability_flag, msconnector_capability_flags, msconnector_adapter, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/adapter_metadata.c` | Source | Adapter-Metadaten sowie Origin-/Capability-Vollständigkeit | msconnector_adapter_metadata_init, msconnector_adapter_metadata, MSCONNECTOR_CAPABILITY_NONE, msconnector_adapter_metadata_is_complete | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/artifact_layout.c` | Source | Standardnamen für Lauf-Artefakte | msconnector_artifact_name_result_json, msconnector_artifact_name_decision_jsonl, msconnector_artifact_name_audit_log, msconnector_artifact_name_error_log, msconnector_artifact_name_runtime_stdout_log, msconnector_artifact_name_runtime_stderr_log, msconnector_artifact_name_server_config, msconnector_artifact_name_connector_config | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/artifacts.c` | Source | Helfer für Standard-Artefaktpfade | msconnector_artifact_paths_init, msconnector_artifact_paths, msconnector_artifact_default_result_json, msconnector_artifact_default_decision_jsonl | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/block_statuses.c` | Source | Helfer für erlaubte und standardmäßige Block-/Fehlerstatus | msconnector_block_status_is_allowed, msconnector_http_status_is_block_response, msconnector_block_status_normalize, MSCONNECTOR_DEFAULT_BLOCK_STATUS, msconnector_http_status_is_valid, MSCONNECTOR_DEFAULT_ERROR_STATUS, msconnector_http_status_name, msconnector_http_status_info_find | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/blocking.c` | Source | Helfer für Blocking-Policy und Blocking-Aktion | msconnector_block_action_name, msconnector_block_action, MSCONNECTOR_BLOCK_ACTION_DENY, MSCONNECTOR_BLOCK_ACTION_REDIRECT, MSCONNECTOR_BLOCK_ACTION_DROP, MSCONNECTOR_BLOCK_ACTION_LOG_ONLY, MSCONNECTOR_BLOCK_ACTION_ABORT_CONNECTION, msconnector_block_action_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/body_policy.c` | Source | Modell für Body-Verarbeitung | msconnector_body_policy_init, msconnector_body_policy, MSCONNECTOR_BODY_MODE_NONE, msconnector_body_mode_name, msconnector_body_mode, MSCONNECTOR_BODY_MODE_BUFFERED, MSCONNECTOR_BODY_MODE_STREAMING, msconnector_body_mode_is_supported | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/build_contract.c` | Source | Build-Target-Namen und C-Standard-Vertrag | msconnector_build_contract_target_name, msconnector_build_contract_target_count, msconnector_build_contract_target_is_standard | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/capabilities.c` | Source | Capability-Flags und Capability-Lookups | msconnector_capability_flag, MSCONNECTOR_CAPABILITY_NONE, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED, MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING, MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS, MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/capability_matrix.c` | Source | Zuordnung von Capabilities zu erforderlichen Tests | msconnector_capability_required_test, msconnector_capability_flag, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED, MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING, MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS, MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/config.c` | Source | Connector-neutrales Konfigurationsobjekt mit Defaults, Merge und Validierung | msconnector_bool_option, MSCONNECTOR_BOOL_UNSET, msconnector_phase4_mode, MSCONNECTOR_PHASE4_MODE_UNSET, msconnector_config, MSCONNECTOR_BOOL_ON, msconnector_block_status_is_allowed, msconnector_http_status_is_valid | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/config_parser.c` | Source | Parser für Boolean-Werte, Phase-4-Modus, Größen, HTTP-Status und Content-Type-Tokens | msconnector_parse_bool, msconnector_bool_option, MSCONNECTOR_BOOL_ON, MSCONNECTOR_BOOL_OFF, msconnector_parse_phase4_mode, msconnector_phase4_mode, MSCONNECTOR_PHASE4_MODE_MINIMAL, MSCONNECTOR_PHASE4_MODE_SAFE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/connector_manifest.c` | Source | Helfer für Connector-Manifest-JSON | msconnector_json_escape, msconnector_connector_manifest_init, msconnector_connector_manifest, msconnector_connector_manifest_from_metadata, msconnector_adapter_metadata, msconnector_adapter_metadata_is_complete, msconnector_connector_manifest_write_json | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/crs.c` | Source | Helfer für CRS-Konfiguration und CRS-Modus | msconnector_crs_config_init, msconnector_crs_config, MSCONNECTOR_CRS_DISABLED, msconnector_crs_mode_name, msconnector_crs_mode, MSCONNECTOR_CRS_EXTERNAL_PATH, MSCONNECTOR_CRS_BUNDLED_PATH, MSCONNECTOR_CRS_TEST_FIXTURE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/decision.c` | Source | Entscheidungsmodell für Inspektionsergebnisse | msconnector_decision_kind, MSCONNECTOR_DECISION_KIND_ALLOW, MSCONNECTOR_DECISION_KIND_LOG_ONLY, MSCONNECTOR_DECISION_KIND_DENY, MSCONNECTOR_DECISION_KIND_REDIRECT, MSCONNECTOR_DECISION_KIND_DROP, MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT, MSCONNECTOR_DECISION_KIND_ERROR | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/decision_action.c` | Source | Zuordnung von Entscheidungen zu Aktionen | msconnector_decision_action_name, msconnector_decision_action, MSCONNECTOR_DECISION_ACTION_ALLOW, MSCONNECTOR_DECISION_ACTION_DENY, MSCONNECTOR_DECISION_ACTION_REDIRECT, MSCONNECTOR_DECISION_ACTION_DROP, MSCONNECTOR_DECISION_ACTION_LOG_ONLY, MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/directive_adapter.c` | Source | Common-Katalog für Direktivenadapter und dessen Validierung | msconnector_directive_adapter_entry, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_SCOPE_SERVER, MSCONNECTOR_DIRECTIVE_ARG_ONE, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_ARG_RAW, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_RULES_REMOTE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/directive_spec.c` | Source | Globaler Katalog der Direktiven-Spezifikationen | msconnector_directive_spec, MSCONNECTOR_DIRECTIVE_MODSECURITY, MSCONNECTOR_DIRECTIVE_VALUE_BOOL, MSCONNECTOR_DIRECTIVE_RULES, MSCONNECTOR_DIRECTIVE_VALUE_STRING, MSCONNECTOR_DIRECTIVE_RULES_FILE, MSCONNECTOR_DIRECTIVE_VALUE_PATH, MSCONNECTOR_DIRECTIVE_RULES_REMOTE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/dos_guard.c` | Source | DoS-Schutzprüfungen für Request und Response | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_dos_guard_check_request, msconnector_request, msconnector_resource_limits, msconnector_error_init, msconnector_resource_limits_validate | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/error.c` | Source | Gemeinsames Fehlermodell mit Codes und Meldungen | msconnector_error_init, msconnector_error, MSCONNECTOR_ERROR_NONE, msconnector_error_set, msconnector_error_code, msconnector_error_code_name, MSCONNECTOR_ERROR_INVALID_CONFIG, MSCONNECTOR_ERROR_RULE_PARSE_FAILED | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/event.c` | Source | Ereignismodell | msconnector_event_json_text_index, msconnector_event_json_status_index, msconnector_event_json_flag_index, msconnector_event_json_parts, msconnector_json_escape, msconnector_event_default_message | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/event_jsonl.c` | Source | JSONL-Serialisierung von Ereignissen | msconnector_event_write_jsonl_line, msconnector_event, msconnector_event_write_json_ex | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/flow_guard.c` | Source | Ablaufwächter für Phasen-/Flow-Zustand | msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_LOGGING, msconnector_flow_guard_init, msconnector_flow_guard, msconnector_flow_guard_can_enter_phase, MSCONNECTOR_FLOW_GUARD_INVALID, MSCONNECTOR_FLOW_GUARD_IMMUTABLE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/generic_mapper.c` | Source | Generischer Request-/Response-Mapper für Starter-Connectoren | msconnector_generic_config_init, msconnector_config, msconnector_config_init, msconnector_generic_map_request, msconnector_generic_request_source, msconnector_request_mapper_contract, msconnector_request, msconnector_request_init | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/headers.c` | Source | Case-insensitive Header-Lookup-Helfer | msconnector_header_name_is, msconnector_header_name_equals, msconnector_header, msconnector_headers_find_first, msconnector_headers_find, msconnector_headers_find_last, msconnector_headers_count_name, msconnector_headers_find_value | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/http_status.c` | Source | Validierung und Klassifizierung von HTTP-Statuscodes | MSCONNECTOR_HTTP_STATUS_MIN, MSCONNECTOR_HTTP_STATUS_MAX, msconnector_http_status_info, MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS, MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION, MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR, MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR, msconnector_http_status_is_valid | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/integrity_event.c` | Source | Integritätsmetadaten mit nicht-kryptografischen Hashes | msconnector_non_crypto_hash_bytes, msconnector_non_crypto_hash_string, msconnector_integrity_event_hash, msconnector_event, msconnector_integrity_event_chain_verify | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/intervention.c` | Source | Helfer für Interventionen und Blocking-Ergebnisse | msconnector_intervention, msconnector_intervention_make, msconnector_intervention_none, msconnector_intervention_is_disruptive | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/json_escape.c` | Source | Helfer zum Escapen von JSON-Strings | msconnector_json_escape | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/late_intervention.c` | Source | Helfer für Late-Intervention-Policy | msconnector_late_intervention_policy_init, msconnector_late_intervention_policy, MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY, MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION, msconnector_late_intervention_action_name, msconnector_late_intervention_action, MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE, msconnector_late_intervention_resolve | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/lifecycle_status.c` | Source | Namen für Build-, Runtime- und Verifikationsstatus | msconnector_build_status_name, msconnector_build_status, MSCONNECTOR_BUILD_STATUS_NOT_STARTED, MSCONNECTOR_BUILD_STATUS_STARTER, MSCONNECTOR_BUILD_STATUS_COMPILES, MSCONNECTOR_BUILD_STATUS_LINKS, MSCONNECTOR_BUILD_STATUS_RUNTIME_READY, msconnector_runtime_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/limits.c` | Source | Kompilierte Limit-Konstanten | msconnector_limit_header_count, MSCONNECTOR_MAX_HEADER_COUNT, msconnector_limit_header_name_length, MSCONNECTOR_MAX_HEADER_NAME_LENGTH, msconnector_limit_header_value_length, MSCONNECTOR_MAX_HEADER_VALUE_LENGTH, msconnector_limit_total_header_bytes, MSCONNECTOR_MAX_TOTAL_HEADER_BYTES | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/log_sanitize.c` | Source | Helfer für Log-Redaktion und Sanitizing | msconnector_sanitize_log_message, msconnector_redact_body_snippet | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/memory.c` | Source | Geprüfte Allokation und Allocator-Callbacks | msconnector_allocator_init, msconnector_allocator, msconnector_alloc_checked, msconnector_free_checked, msconnector_allocator_within_limit | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/modsecurity_engine.c` | Source | Connector-neutrale Operationstabelle für die ModSecurity-Engine | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_modsecurity_transaction, MSCONNECTOR_ERROR_INTERNAL, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, msconnector_modsecurity_engine_init, msconnector_modsecurity_engine | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/origin.c` | Source | Helfer für Source-/Origin-Metadaten | msconnector_origin, msconnector_origin_make, msconnector_origin_is_empty | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/origin_governance.c` | Source | Vollständigkeitsprüfungen für Origin-Governance | msconnector_origin_governance_init, msconnector_origin_governance, msconnector_origin_governance_is_complete, msconnector_origin_governance_from_metadata, msconnector_adapter_metadata | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/path_policy.c` | Source | Helfer zur Pfadvalidierung | msconnector_path_is_empty, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/redaction.c` | Source | Helfer zur String-Redaktion | msconnector_redacted_string, msconnector_redact_copy | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/request_helpers.c` | Source | Helfer für Request-Initialisierung und -Validierung | msconnector_header, msconnector_request_init, msconnector_request, msconnector_request_validate, msconnector_request_validate_with_limits, msconnector_resource_limits, msconnector_resource_limits_headers_ok, msconnector_resource_limits_body_ok | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/request_mapper_contract.c` | Source | Validierung des Request-Mapper-Vertrags | msconnector_mapper_requirement, MSCONNECTOR_MAPPER_REQUIRED, MSCONNECTOR_MAPPER_UNSUPPORTED, msconnector_request_mapper_contract_init, msconnector_request_mapper_contract, MSCONNECTOR_MAPPER_OPTIONAL, msconnector_request_mapper_contract_validate, msconnector_request_mapper_validate_output | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/resource_limits.c` | Source | Ressourcenlimits und Validatoren | msconnector_resource_limits_init, msconnector_resource_limits, MSCONNECTOR_MAX_HEADER_COUNT, MSCONNECTOR_MAX_HEADER_NAME_LENGTH, MSCONNECTOR_MAX_HEADER_VALUE_LENGTH, MSCONNECTOR_MAX_TOTAL_HEADER_BYTES, MSCONNECTOR_MAX_BODY_BUFFER_SIZE, MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/response_helpers.c` | Source | Helfer für Response-Initialisierung und -Validierung | msconnector_header, msconnector_response_init, msconnector_response, msconnector_response_validate, msconnector_http_status_is_valid, msconnector_response_validate_with_limits, msconnector_resource_limits, msconnector_resource_limits_headers_ok | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/response_mapper_contract.c` | Source | Validierung des Response-Mapper-Vertrags | msconnector_mapper_requirement, MSCONNECTOR_MAPPER_REQUIRED, MSCONNECTOR_MAPPER_UNSUPPORTED, msconnector_response_mapper_contract_init, msconnector_response_mapper_contract, MSCONNECTOR_MAPPER_OPTIONAL, msconnector_response_mapper_contract_validate, msconnector_response_mapper_validate_output | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/rule_error.c` | Source | Helfer für Fehler beim Laden von Regeln | msconnector_rule_error_set_parse_failed, msconnector_error, msconnector_error_set, MSCONNECTOR_ERROR_RULE_PARSE_FAILED, msconnector_error_default_message, msconnector_rule_error_set_load_failed, MSCONNECTOR_ERROR_RULE_LOAD_FAILED, msconnector_rule_error_clear | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/rule_event.c` | Source | Helfer für Ereignisse beim Laden von Regeln | msconnector_rule_load_event_ex, msconnector_rule_load_stats, msconnector_event, msconnector_event_init, MSCONNECTOR_STATUS_OK, msconnector_rule_load_event, msconnector_rule_error_event, msconnector_error | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/rule_id.c` | Source | Kopieren, Extrahieren und Validieren von Rule-IDs | msconnector_rule_id_validate, msconnector_rule_id_copy, msconnector_rule_id_extract_from_message | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/rule_loader.c` | Source | Backend-Vertrag für das Laden von Regeln | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_rule_loader_init, msconnector_rule_loader, msconnector_rule_loader_backend, msconnector_rule_load_stats_init, msconnector_rule_loader_add_inline | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/rule_merge.c` | Source | Helfer zum Zusammenführen von Rule Collections | msconnector_rule_collection_init, msconnector_rule_collection, msconnector_rule_collection_from_config, msconnector_config, msconnector_rule_collection_merge | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/runtime_paths.c` | Source | Helfer zum Zusammenfügen von Runtime-Pfaden | msconnector_runtime_path_join, msconnector_path_is_absolute, msconnector_path_has_parent_reference | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/runtime_report.c` | Source | Helfer für Runtime-Report-JSON | msconnector_json_escape, msconnector_runtime_report_init, msconnector_runtime_report, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_runtime_report_write_json, msconnector_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/status.c` | Source | Gemeinsame Status-Helfer für PASS/FAIL/BLOCKED-artige Zustände | msconnector_status_name, msconnector_status, MSCONNECTOR_STATUS_OK, MSCONNECTOR_STATUS_ERROR, MSCONNECTOR_STATUS_BLOCKED, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_status_from_result | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/test_result.c` | Source | Test-Result-Modell | msconnector_test_result_init, msconnector_test_result, MSCONNECTOR_STATUS_UNSUPPORTED, msconnector_test_result_passed, MSCONNECTOR_STATUS_OK | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/test_result_json.c` | Source | JSON-Schreiber für Test-Resultate | msconnector_json_escape, msconnector_test_result_write_json, msconnector_test_result, msconnector_status_name | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/transaction.c` | Source | Helfer für Transaction Views | msconnector_decision_kind, msconnector_status, MSCONNECTOR_STATUS_BLOCKED, MSCONNECTOR_DECISION_KIND_DENY, MSCONNECTOR_STATUS_ERROR, MSCONNECTOR_DECISION_KIND_ERROR, MSCONNECTOR_STATUS_UNSUPPORTED, MSCONNECTOR_DECISION_KIND_UNSUPPORTED | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/transaction_id.c` | Source | Helfer für Transaction-ID-Quelle und -Auswertung | msconnector_error, msconnector_error_code, msconnector_error_set, msconnector_transaction_id_result, msconnector_transaction_id_validate, msconnector_transaction_id_copy, msconnector_transaction_id_source, MSCONNECTOR_ERROR_INVALID_CONFIG | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |
| `common/src/transaction_state.c` | Source | Zustand der verarbeiteten Transaction-Phasen | msconnector_transaction_state_init, msconnector_transaction_state, msconnector_transaction_state_mark_phase, msconnector_phase, MSCONNECTOR_PHASE_CONNECTION, MSCONNECTOR_PHASE_URI, MSCONNECTOR_PHASE_REQUEST_HEADERS, MSCONNECTOR_PHASE_REQUEST_BODY | Common SDK und adoptierende Connectoren | connector-neutral; keine Runtime-Evidence |

## Common SDK: Module und Aufgaben

- Konfiguration, Direktiven und Parser definieren das gemeinsame Vokabular, Standardwerte, Merge-Verhalten und Validierung. Sie sind connector-neutral, weil sie semantische Werte ohne Apache-, NGINX-, HAProxy-, Envoy-, Traefik- oder lighttpd-Typen speichern. Sie beweisen keine Host-Syntax-Parität.
- Request, Response, Header und Mapper-Verträge definieren neutrale HTTP-Formen und Validierung. Sie beweisen keine Live-Verarbeitung von Requests oder Response-Bodies.
- Decision-, Intervention-, Status-, Error- und Event-JSONL-Helfer definieren gemeinsame Ergebnissemantik und Serialisierung. Sie sind keine append-only oder kryptografische Evidence.
- Ressourcenlimits, Body Policy, DoS-Schutz, Flow-Guard und Integritätsmetadaten sind Guardrails. Sie behaupten kein runtime-secure Verhalten.
- Rule Loading, Merge, Rule-ID- und CRS-Helfer definieren Verträge und Metadaten. Sie beweisen keine CRS-Ausführung.
- Adapter-Metadaten, Capabilities, Origin-Governance und Manifeste beschreiben Herkunft und Capability-Claims. Metadaten müssen konservativ bleiben, bis Evidence eine Statusänderung rechtfertigt.

## Config-, Direktiven- und Parser-Modell

`msconnector_config` speichert connector-neutrale Optionen: Enable-Flag, Error-Log-Flag, Inline-/File-/Remote-Regeln, statische oder Ausdruck-basierte Transaction-ID, Phase-4-Modus, Content-Type-Datei, Phase-4-Logpfad, Body-Limit und Standardstatuswerte.

`msconnector_config_init` initialisiert Werte auf unset/zero/null. `msconnector_config_apply_defaults` füllt nur nicht gesetzte Werte. `msconnector_config_merge` merged Parent- und Child-Werte und wendet danach Defaults an; zu frühes Anwenden von Defaults würde Parent-/Child-Vererbung verfälschen. `msconnector_config_validate` validiert Enum-Bereiche, vollständige Remote-Rule-Key/URL-Paare, gegenseitigen Ausschluss von `transaction_id` und `transaction_id_expr`, erlaubte Blockstatuswerte und gültige Fehlerstatuswerte.

Parser-Helfer verwenden `1 = success` und `0 = failure`: `msconnector_parse_bool`, `msconnector_parse_phase4_mode`, `msconnector_parse_size`, `msconnector_parse_http_status` und `msconnector_validate_content_type_token`. Der Boolean-Parser akzeptiert `on/off`, `true/false`, `1/0` und `yes/no`. Der Phase-4-Modus akzeptiert `minimal`, `safe` und `strict`. Größen werden als positive dezimale Bytewerte geparst. HTTP-Statuswerte müssen gültig sein. Content-Type-Token benötigen genau einen Slash, nicht-leeren Type und Subtype, keine Control-Characters und kein Semikolon. Transaction-ID-Expression-Parsing bleibt connector-spezifisch.

## Erlaubte Config-/Directive-Begriffe

| Config / Directive | Common Macro | Typ | Erlaubte Werte | Default | Parser / Validator | Betroffene Connectoren | Hinweise |
|---|---|---|---|---|---|---|---|
| `modsecurity` | `MSCONNECTOR_DIRECTIVE_MODSECURITY` | bool | Spezifikation: `on|off`; Parser akzeptiert auch `true|false|1|0|yes|no` | `off` | `msconnector_parse_bool`, `msconnector_config_validate` | Connector-spezifisches Mapping; maßgeblich ist das jeweilige Capability-Manifest | Aktiviert nur semantische Verarbeitung; kein Production-Claim. |
| `modsecurity_rules` | `MSCONNECTOR_DIRECTIVE_RULES` | string/raw | Inline-Regeltext | keiner | Direktivenadapter und connector-spezifisches Rule Loading | connector-abhängig | Regeltext beweist keine CRS-/Runtime-Ausführung. |
| `modsecurity_rules_file` | `MSCONNECTOR_DIRECTIVE_RULES_FILE` | path | Runtime-Pfad | keiner | Direktivenadapter, Path Policy soweit genutzt | connector-abhängig | Pfadgültigkeit ist umgebungsabhängig. |
| `modsecurity_rules_remote` | `MSCONNECTOR_DIRECTIVE_RULES_REMOTE` | string pair | `key url` | keiner | Config verlangt Key und URL gemeinsam | connector-abhängig | Unvollständiges Remote-Paar ist ungültig. |
| `modsecurity_transaction_id` | `MSCONNECTOR_DIRECTIVE_TRANSACTION_ID` | string | statische ID | keiner | Transaction-ID-Helfer; gegenseitiger Ausschluss in Config | connector-abhängig | Gegenseitig exklusiv mit Expression. |
| `modsecurity_transaction_id_expr` | `MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR` | string | connector-geparste Expression | keiner | connector-spezifischer Parser; gegenseitiger Ausschluss in Config | Apache/NGINX können abweichen; Envoy/Traefik/lighttpd connector-gap | Apache-artige Expressions dürfen nicht als NGINX-Syntax behandelt werden. |
| `modsecurity_use_error_log` | `MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG` | bool | Spezifikation: `on|off`; Parser akzeptiert auch Aliase | `on` | `msconnector_parse_bool` | connector-abhängig | Nur Common-Config-Flag. |
| `modsecurity_phase4_mode` | `MSCONNECTOR_DIRECTIVE_PHASE4_MODE` | enum | `minimal|safe|strict` | `safe` | `msconnector_parse_phase4_mode` | connector-abhängig; Starter-Connectoren nicht verifiziert | Response-Body-Policy-Modell; keine Response-Body-Verifikation. |
| `modsecurity_phase4_content_types_file` | `MSCONNECTOR_DIRECTIVE_PHASE4_CONTENT_TYPES_FILE` | path | Datei mit gültigen Content-Type-Tokens | keiner | Content-Type-Token-Parser und connector-spezifisches File-Handling | connector-abhängig | Striktheit hängt von Connector und Evidence ab. |
| `modsecurity_phase4_log` | `MSCONNECTOR_DIRECTIVE_PHASE4_LOG` | path | Logpfad | keiner | Direktivenadapter und Path Policy soweit genutzt | connector-abhängig | Logpfad beweist kein Body Handling. |
| `modsecurity_phase4_body_limit` | `MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT` | size | positive dezimale Bytes | `1048576` | `msconnector_parse_size` | connector-abhängig | Truncation-Metadaten benötigen Connector-Implementierung/Evidence. |
| `default_block_status` | Config-Feld | HTTP-Status | erlaubte Blockstatuswerte | `403` | `msconnector_block_status_is_allowed` | Common-Config-Consumer | Config-Feld, kein Makro in `directives.h`. |
| `default_error_status` | Config-Feld | HTTP-Fehlerstatus | gültiger HTTP-Fehlerstatus | `500` | HTTP-Statusvalidierung und Fehlerstatusprüfung | Common-Config-Consumer | Config-Feld, kein Makro in `directives.h`. |
| `unsupported_status` | Config-Feld | HTTP-Fehlerstatus | gültiger HTTP-Fehlerstatus | `501` | HTTP-Statusvalidierung und Fehlerstatusprüfung | Common-Config-Consumer | Config-Feld, kein Makro in `directives.h`. |
| CRS setup / CRS mode / fixture mode | CRS-/Framework-Metadaten | mode/path/string | repository-/framework-spezifisch | unknown | `msconnector_crs_config_validate` und Framework-Skripte, soweit genutzt | framework-/connector-abhängig | Als `requires runtime evidence` behandeln, sofern kein aktueller Report den konkreten Lauf belegt. |

## Request-/Response-Mapping

Request-Mapping besitzt Methode, URI, Protokoll, Endpunkte, Header, Body-Metadaten und Transaction-IDs in connector-neutraler Form. Response-Mapping besitzt Status, Protokoll, Header, Content-Type-/Body-Metadaten und Phase-4-Policy-Zustand. Mapper-Verträge definieren Validierungs- und Ownership-Erwartungen. Host-Server-Objekte bleiben außerhalb von `common/`.

## Decision-, Intervention-, Status- und Event-Modell

Gemeinsame Decision-/Action-Helfer beschreiben allow-/block-/error-/unsupported-artige Ergebnisse. Intervention-Helfer normalisieren Blocking-Ergebnisse. Status-Helfer bilden Ergebnisse auf gemeinsame Statusnamen ab. Event- und JSONL-Helfer serialisieren per-run Evidence. Diese Ausgaben sind nicht append-only und nicht kryptografisch signiert, sofern zukünftiger Code dies nicht ausdrücklich implementiert und belegt.

## Ressourcenlimits, DoS-Schutz, Flow-Guard und Integrität

Ressourcenlimits zentralisieren Maximalgrößen und Zählwerte. DoS-Schutz und Flow-Guard prüfen connector-neutralen Request-/Response-Zustand und Phasenübergänge. Integrity-Events tragen Metadaten und nicht-kryptografische Hashes. Das ist Governance- und Safety-Modellierung, kein runtime-secure-, tamper-proof- oder cryptographic-integrity-Claim.

## C-Sprache und Standards

Das Common SDK ist auf C17 ausgelegt. C17 ist der harte Pflichtstandard, wenn Compiler und benötigte Header vorhanden sind. C23 ist optional. future-C (`c2y`/`gnu2y`) ist optional. `c20` und `c26` sind keine gültigen C-Standard-Modi und sollen bei vorhandenen Targets als SKIPPED/INFO behandelt werden. Exit 77 bedeutet BLOCKED/SKIPPED, weil Umgebung, Header, Compiler oder optionales Profil fehlen. Echte Compile-Fehler dürfen nicht als Exit 77 versteckt werden.

| Connector-Gruppe | C17 | C23 | future-C | Header-Voraussetzungen | Exit-77-Verhalten |
|---|---|---|---|---|---|
| Common | erforderlich, wenn Compiler vorhanden ist | optional | optional | Common-Header | nur Umgebung/unsupported optional profile darf skippen |
| Apache | hart, wenn APXS/APR/libmodsecurity-Header vorhanden sind | optional | optional | APXS/APR/libmodsecurity | fehlende Header dürfen blockieren; Compile-Fehler müssen fehlschlagen |
| NGINX | hart, wenn NGINX-/libmodsecurity-Header vorhanden sind | optional | optional | NGINX-Source-/Include-Roots, libmodsecurity | fehlende Roots/Header dürfen blockieren |
| HAProxy | hart, wenn HAProxy-/libmodsecurity-Kontext vorhanden ist | optional | optional | HAProxy-/SPOE-/SPOP-Kontext und Common-Includes | fehlende Header dürfen blockieren |
| Envoy, Traefik, lighttpd | C17-Native-/Servicepfade | optional | optional | Connector- und Common-Header | gezielter Runtime-Pfad; kanonische Baseline ausstehend |

## CI-, Contract- und Governance-Checks

| Check / Target | Skript | Zweck | Betrifft | Hart oder optional | Exit 77 möglich? |
|---|---|---|---|---|---|
| `check-common-helpers` | `ci/check-common-helpers.sh` | Common-Helfer Compile-/Static-Checks | common | hart, wenn Umgebung vorhanden ist | möglich bei Umgebungsblockern |
| `check-common-sdk-contract` | `ci/check-common-sdk-contract.py` | Common-SDK-API-/Contract-Governance | common | hart | normalerweise nein |
| `check-common-security-contract` | `ci/check-common-security-contract.py` | Security-/Daten-Contract-Governance | common | hart | skriptabhängig |
| `check-common-memory-safety` | `ci/check-common-memory-safety.sh` | Ownership-/Memory-Contract-Checks | common | hart | skriptabhängig |
| `check-common-flow-integrity` | `ci/check-common-flow-integrity.py` | Flow-/Integritäts-Contract-Checks | common | hart | skriptabhängig |
| `check-adapter-contracts` | `ci/check-adapter-contracts.py` | Adapter-Metadaten-/Contract-Checks | Connectoren | hart | skriptabhängig |
| `check-directive-parity` | `ci/check-directive-parity.py` | Common-Direktivenparität über Connectoren | common/Connectoren | hart | skriptabhängig |
| Connector-Adoption-Ziele | `ci/check-*-common-adoption.py` | Adoption-/Static-Governance | Connectoren | hart | skriptabhängig |
| Connector-C-Standard-Ziele | `ci/check-*-c-standards.sh`, `ci/check-*-c-standard-wiring.py` | C17/C23/future-C Compile-Profile | Connectoren | C17 hart, optionale Profile optional | ja |
| `check-bilingual-docs` | `ci/check-bilingual-docs.py` | Bilinguale Dokumentations- und Link-Governance | docs/reports | hart für Doku | kann bei fehlenden Companion-Dokumenten oder Framework-Links fehlschlagen |

## Makefile-Ziele: Was kann man mit `make` tun?

Das Makefile ist der operative Index für Setup, Linting, Common-SDK-Checks, Connector-Checks, C-Standard-Profile, Runtime-/Starter-Smokes, Matrix-/Report-Generierung, Framework-Integration und Bootstrap-Workflows. Ein Target belegt nur das, was sein Skript tatsächlich prüft. Compile-only- und structure-only-Ziele erzeugen keine Runtime-Evidence.

### Zielkategorien

- Allgemeine Ziele: Setup, Dependency-Fetch, Doctor, Lint und Quick-/Codex-Checks.
- Common-SDK-Ziele: Helfer-Compilation, SDK-/Security-/Memory-/Flow-Verträge, Adapter-Verträge und Direktivenparität.
- Apache-, NGINX- und HAProxy-Ziele: Common-Adoption, C-Standard-Wiring und C17/C23/future-C-Checks sowie Smoke-/Test-Wrapper.
- Envoy-, Traefik- und lighttpd-Ziele: getrennte Build-, Config-Load-,
  request-freie Start-, gezielte Runtime-, Capability- und Evidence-Checks.
- Framework-/Test-Framework-Ziele: Matrix-, Verified-Report-, MRTS- und Smoke-/Test-Workflows. Diese können blockieren, wenn `modules/ModSecurity-test-Framework` oder Runtime-Komponenten fehlen.
- Report-/Generator-Ziele: Reports und Matrizen generieren oder prüfen. Daraus folgt nicht automatisch verifiziertes Runtime-Verhalten.

### Vollständige Makefile-Zieltabelle

| Makefile-Ziel | Zweck | Betrifft | Voraussetzung | Hart/optional | Exit-77/BLOCKED möglich? | Hinweise |
|---|---|---|---|---|---|---|
| `check-framework` | Führt `check-framework` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-framework-fixture-syntax` | Führt `check-framework-fixture-syntax` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-framework-fixture-syntax.py |
| `prepare-runtime-components` | Führt `prepare-runtime-components` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `prepare-envoy-runtime` | Führt `prepare-envoy-runtime` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/prepare-envoy-runtime.sh |
| `prepare-traefik-runtime` | Führt `prepare-traefik-runtime` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/prepare-traefik-runtime.sh |
| `prepare-lighttpd-runtime` | Führt `prepare-lighttpd-runtime` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/prepare-lighttpd-runtime.sh |
| `prepare-lighttpd-runtime-build` | Führt `prepare-lighttpd-runtime-build` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `prepare-open-connector-runtimes` | Führt `prepare-open-connector-runtimes` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `runtime-components-inventory` | Führt `runtime-components-inventory` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/runtime-components-inventory.sh |
| `runtime-components-sources` | Führt `runtime-components-sources` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/runtime-components-inventory.sh |
| `check-runtime-producer-readiness` | Führt `check-runtime-producer-readiness` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-runtime-producer-readiness.py |
| `check-runtime-path-policy` | Führt `check-runtime-path-policy` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-runtime-path-policy.py |
| `check-bilingual-docs` | Führt `check-bilingual-docs` aus (Other). | Other | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-bilingual-docs.py |
| `refresh-connector-reports` | Führt `refresh-connector-reports` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/refresh-connector-reports.py |
| `refresh-all-reports` | Führt `refresh-all-reports` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-generated-report-layout` | Führt `check-generated-report-layout` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-generated-report-layout.py |
| `report-governance` | Führt `report-governance` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-generated-report-layout.py |
| `verified-report-evidence-gate` | Führt `verified-report-evidence-gate` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-generated-report-layout | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `generate-system-environment-proof` | Führt `generate-system-environment-proof` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-system-environment-proof.py |
| `generate-verified-runtime-mismatch-analysis` | Führt `generate-verified-runtime-mismatch-analysis` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/generate-verified-runtime-mismatch-analysis.py |
| `generate-remaining-critical-batch-analysis` | Führt `generate-remaining-critical-batch-analysis` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-remaining-critical-batch-analysis.py |
| `generate-native-semantics-comparison` | Führt `generate-native-semantics-comparison` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/run-native-case-comparison.py |
| `prove-generated-reports` | Führt `prove-generated-reports` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `verified-runtime-producers` | Führt `verified-runtime-producers` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `verified-report-producers` | Führt `verified-report-producers` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | verified-runtime-producers | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: dependency target / see Makefile |
| `verified-report-refresh` | Führt `verified-report-refresh` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `verified-report-consumers` | Führt `verified-report-consumers` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `verified-report-checks` | Führt `verified-report-checks` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `verified-report-run` | Führt `verified-report-run` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `verified-report-run-soft` | Führt `verified-report-run-soft` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `verified-report-run-smoke` | Führt `verified-report-run-smoke` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `verified-full-matrix-job` | Führt `verified-full-matrix-job` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `verified-case` | Führt `verified-case` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `verified-native-case` | Führt `verified-native-case` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-native-case-comparison.py |
| `verified-nginx-case` | Führt `verified-nginx-case` aus (NGINX). | NGINX | check-framework prepare-runtime-components | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `verified-apache-case` | Führt `verified-apache-case` aus (Apache). | Apache | check-framework prepare-runtime-components | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `verified-haproxy-case` | Führt `verified-haproxy-case` aus (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `verified-full-matrix-resume` | Führt `verified-full-matrix-resume` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-verified-report-run.py |
| `smoke-common` | Führt `smoke-common` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-connector-smokes.sh |
| `smoke-apache` | Führt `smoke-apache` aus (Apache). | Apache | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-apache-smoke.sh |
| `smoke-nginx` | Führt `smoke-nginx` aus (NGINX). | NGINX | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-nginx-smoke.sh |
| `smoke-envoy` | Führt `smoke-envoy` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-envoy-smoke.sh |
| `smoke-envoy-modsecurity` | Führt `smoke-envoy-modsecurity` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-envoy-request-body` | Führt `smoke-envoy-request-body` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-envoy-crs` | Führt `smoke-envoy-crs` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-envoy-crs-secondary` | Führt `smoke-envoy-crs-secondary` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-haproxy` | Führt `smoke-haproxy` aus (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-haproxy-smoke.sh |
| `smoke-lighttpd` | Führt `smoke-lighttpd` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-lighttpd-smoke.sh |
| `smoke-lighttpd-modsecurity` | Führt `smoke-lighttpd-modsecurity` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-lighttpd-request-body` | Führt `smoke-lighttpd-request-body` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-lighttpd-crs` | Führt `smoke-lighttpd-crs` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-lighttpd-crs-secondary` | Führt `smoke-lighttpd-crs-secondary` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-traefik` | Führt `smoke-traefik` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-traefik-smoke.sh |
| `smoke-traefik-modsecurity` | Führt `smoke-traefik-modsecurity` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-traefik-request-body` | Führt `smoke-traefik-request-body` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-traefik-crs` | Führt `smoke-traefik-crs` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-traefik-crs-secondary` | Führt `smoke-traefik-crs-secondary` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-open-connectors-crs` | Führt `smoke-open-connectors-crs` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-open-connectors-request-body` | Führt `smoke-open-connectors-request-body` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-open-connectors-crs-secondary` | Führt `smoke-open-connectors-crs-secondary` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-new-connectors` | Führt `smoke-new-connectors` aus (Remaining connectors). | Remaining connectors | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `smoke-all` | Führt `smoke-all` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-connector-smokes.sh |
| `test` | Führt `test` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | test-no-crs test-with-crs | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: dependency target / see Makefile |
| `test-no-crs` | Führt `test-no-crs` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/common.sh, ci/run-connector-smokes.sh |
| `test-with-crs` | Führt `test-with-crs` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/common.sh, ci/fetch-crs.sh, ci/prepare-crs.sh, ci/run-connector-smokes.sh |
| `mrts-generate` | Führt `mrts-generate` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `mrts-load` | Führt `mrts-load` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `mrts-import` | Führt `mrts-import` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `test-no-mrts` | Führt `test-no-mrts` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `test-with-mrts` | Führt `test-with-mrts` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `test-with-mrts-feature-demo` | Führt `test-with-mrts-feature-demo` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `test-mrts-matrix` | Führt `test-mrts-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `mrts-ftw` | Führt `mrts-ftw` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `runtime-matrix` | Führt `runtime-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-runtime-matrix.sh |
| `runtime-matrix-all` | Führt `runtime-matrix-all` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-runtime-matrix.sh |
| `runtime-matrix-all-runtime` | Führt `runtime-matrix-all-runtime` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-runtime-matrix.sh |
| `runtime-matrix-haproxy` | Führt `runtime-matrix-haproxy` aus (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/Composite | skriptabhängig | Skript/Rezept: ci/run-haproxy-runtime-matrix.sh |
| `full-mrts-runtime-matrix` | Führt `full-mrts-runtime-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-full-mrts-runtime-matrix.sh |
| `mrts-only-full-run` | Führt `mrts-only-full-run` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | full-mrts-runtime-matrix | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: dependency target / see Makefile |
| `full-runtime-matrix` | Führt `full-runtime-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | full-matrix-parallel | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: dependency target / see Makefile |
| `full-matrix-parallel` | Führt `full-matrix-parallel` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-full-matrix-parallel.sh |
| `full-matrix-parallel-runtime` | Führt `full-matrix-parallel-runtime` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-full-matrix-parallel.sh |
| `full-matrix-single-job-runtime` | Führt `full-matrix-single-job-runtime` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `full-matrix-resume-runtime` | Führt `full-matrix-resume-runtime` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-full-matrix-resume.py |
| `generate-full-runtime-matrix` | Führt `generate-full-runtime-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/generate-full-runtime-matrix.py |
| `generate-full-matrix-job-completeness` | Führt `generate-full-matrix-job-completeness` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/generate-full-matrix-job-completeness.py |
| `generate-nginx-mrts-http500-cluster-analysis` | Führt `generate-nginx-mrts-http500-cluster-analysis` aus (NGINX). | NGINX | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-nginx-mrts-http500-cluster-analysis.py |
| `generate-work-queue` | Führt `generate-work-queue` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-connector-work-queue.py, ci/generate-phase-work-queue.py, ci/generate-nolog-audit-evidence-analysis.py |
| `generate-phase-work-queue` | Führt `generate-phase-work-queue` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-phase-work-queue.py, ci/generate-nolog-audit-evidence-analysis.py, ci/generate-response-header-hook-analysis.py |
| `generate-nolog-audit-evidence-analysis` | Führt `generate-nolog-audit-evidence-analysis` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-nolog-audit-evidence-analysis.py |
| `generate-response-header-hook-analysis` | Führt `generate-response-header-hook-analysis` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-response-header-hook-analysis.py |
| `generate-phase4-hard-abort-capability` | Führt `generate-phase4-hard-abort-capability` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-phase4-hard-abort-capability.py |
| `generate-intervention-blocking-analysis` | Führt `generate-intervention-blocking-analysis` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-intervention-blocking-analysis.py |
| `generate-no-mrts-intervention-nomatch-analysis` | Führt `generate-no-mrts-intervention-nomatch-analysis` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/generate-no-mrts-intervention-nomatch-analysis.py |
| `generate-body-processor-analysis` | Führt `generate-body-processor-analysis` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-body-processor-analysis.py |
| `generate-rule-chain-semantics-analysis` | Führt `generate-rule-chain-semantics-analysis` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-rule-chain-semantics-analysis.py |
| `generate-final-consistency-audit` | Führt `generate-final-consistency-audit` aus (Other). | Other | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-final-consistency-audit.py |
| `generate-remaining-failure-analysis` | Führt `generate-remaining-failure-analysis` aus (Remaining connectors). | Remaining connectors | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/generate-remaining-failure-analysis.py |
| `mrts-native-full-run` | Führt `mrts-native-full-run` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-mrts-native-full.sh |
| `mrts-native-full-run-runtime` | Führt `mrts-native-full-run-runtime` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-mrts-native-full.sh |
| `mrts-native-apache-full` | Führt `mrts-native-apache-full` aus (Apache). | Apache | check-framework prepare-runtime-components | optional/Composite | skriptabhängig | Skript/Rezept: ci/run-mrts-native-full.sh |
| `mrts-native-nginx-pr24-full` | Führt `mrts-native-nginx-pr24-full` aus (NGINX). | NGINX | check-framework prepare-runtime-components | optional/Composite | skriptabhängig | Skript/Rezept: ci/run-mrts-native-full.sh |
| `mrts-upstream-infra-check` | Führt `mrts-upstream-infra-check` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `test-haproxy-no-crs` | Führt `test-haproxy-no-crs` aus (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-haproxy-runtime-matrix.sh |
| `test-haproxy-with-crs` | Führt `test-haproxy-with-crs` aus (HAProxy). | HAProxy | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/run-haproxy-runtime-matrix.sh |
| `probe-response-body` | Führt `probe-response-body` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework prepare-runtime-components | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/probe-response-body-blocking.sh |
| `connector-starter-checks` | Führt `connector-starter-checks` aus (Other). | Other | check-framework prepare-runtime-components | optional/Composite | skriptabhängig | Skript/Rezept: ci/run-connector-starter-checks.sh |
| `check-remaining-connectors-common-adoption` | Führt `check-remaining-connectors-common-adoption` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-remaining-connectors-common-adoption.py |
| `check-remaining-connectors-c-standard-wiring` | Führt `check-remaining-connectors-c-standard-wiring` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-remaining-connectors-c-standard-wiring.py |
| `check-remaining-connectors-c-standards` | Führt `check-remaining-connectors-c-standards` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-c17` | Führt `check-remaining-connectors-c17` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-c17-lint` | Führt `check-remaining-connectors-c17-lint` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-c23` | Führt `check-remaining-connectors-c23` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-remaining-connectors-c-standards.sh |
| `check-remaining-connectors-future-c` | Führt `check-remaining-connectors-future-c` aus (Remaining connectors). | Remaining connectors | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-remaining-connectors-c-standards.sh |
| `check-block-status-generator` | Führt `check-block-status-generator` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-block-status-generator.py |
| `check-apache-common-adoption` | Führt `check-apache-common-adoption` aus (Apache). | Apache | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-apache-common-adoption.py |
| `check-apache-c-standard-wiring` | Führt `check-apache-c-standard-wiring` aus (Apache). | Apache | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-apache-c-standard-wiring.py |
| `check-apache-c-standards` | Führt `check-apache-c-standards` aus (Apache). | Apache | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-apache-c-standards.sh |
| `check-apache-c17` | Führt `check-apache-c17` aus (Apache). | Apache | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-apache-c-standards.sh |
| `check-apache-c17-lint` | Führt `check-apache-c17-lint` aus (Apache). | Apache | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-apache-c-standards.sh |
| `check-apache-c23` | Führt `check-apache-c23` aus (Apache). | Apache | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-apache-c-standards.sh |
| `check-apache-future-c` | Führt `check-apache-future-c` aus (Apache). | Apache | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-apache-c-standards.sh |
| `check-apache-c20` | Führt `check-apache-c20` aus (Apache). | Apache | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-apache-c26` | Führt `check-apache-c26` aus (Apache). | Apache | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-nginx-common-adoption` | Führt `check-nginx-common-adoption` aus (NGINX). | NGINX | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-nginx-common-adoption.py |
| `check-nginx-c-standard-wiring` | Führt `check-nginx-c-standard-wiring` aus (NGINX). | NGINX | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-nginx-c-standard-wiring.py |
| `check-nginx-c-standards` | Führt `check-nginx-c-standards` aus (NGINX). | NGINX | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-nginx-c-standards.sh |
| `check-nginx-c17` | Führt `check-nginx-c17` aus (NGINX). | NGINX | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-nginx-c-standards.sh |
| `check-nginx-c17-lint` | Führt `check-nginx-c17-lint` aus (NGINX). | NGINX | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-nginx-c-standards.sh |
| `check-nginx-c23` | Führt `check-nginx-c23` aus (NGINX). | NGINX | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-nginx-c-standards.sh |
| `check-nginx-future-c` | Führt `check-nginx-future-c` aus (NGINX). | NGINX | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-nginx-c-standards.sh |
| `check-nginx-c20` | Führt `check-nginx-c20` aus (NGINX). | NGINX | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-nginx-c26` | Führt `check-nginx-c26` aus (NGINX). | NGINX | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-haproxy-common-adoption` | Führt `check-haproxy-common-adoption` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-haproxy-common-adoption.py |
| `check-haproxy-c-standard-wiring` | Führt `check-haproxy-c-standard-wiring` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-haproxy-c-standard-wiring.py |
| `check-haproxy-c-standards` | Führt `check-haproxy-c-standards` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c17` | Führt `check-haproxy-c17` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c17-lint` | Führt `check-haproxy-c17-lint` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c23` | Führt `check-haproxy-c23` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-haproxy-c-standards.sh |
| `check-haproxy-future-c` | Führt `check-haproxy-future-c` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/check-haproxy-c-standards.sh |
| `check-haproxy-c20` | Führt `check-haproxy-c20` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-haproxy-c26` | Führt `check-haproxy-c26` aus (HAProxy). | HAProxy | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-common-helpers` | Führt `check-common-helpers` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-common-helpers.sh |
| `check-common-helpers-c17` | Führt `check-common-helpers-c17` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | hart | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-common-helpers-c23` | Führt `check-common-helpers-c23` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/detect-c-standard.py |
| `check-common-helpers-future-c` | Führt `check-common-helpers-future-c` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/detect-c-standard.py |
| `check-common-helpers-c20` | Führt `check-common-helpers-c20` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-common-helpers-c26` | Führt `check-common-helpers-c26` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |
| `check-common-sdk-contract` | Führt `check-common-sdk-contract` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | hart | skriptabhängig | Skript/Rezept: ci/check-common-sdk-contract.py |
| `check-common-security-contract` | Führt `check-common-security-contract` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | hart | skriptabhängig | Skript/Rezept: ci/check-common-security-contract.py |
| `check-common-memory-safety` | Führt `check-common-memory-safety` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-common-memory-safety.sh |
| `check-common-flow-integrity` | Führt `check-common-flow-integrity` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: ci/check-common-flow-integrity.py |
| `check-adapter-contracts` | Führt `check-adapter-contracts` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | hart | skriptabhängig | Skript/Rezept: ci/check-adapter-contracts.py |
| `check-directive-parity` | Führt `check-directive-parity` aus (Common SDK / contracts). | Common SDK / contracts | siehe Makefile/Rezept | hart | skriptabhängig | Skript/Rezept: ci/check-directive-parity.py |
| `lint` | Führt `lint` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | hart | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `summary` | Führt `summary` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/summarize-results.py |
| `case-matrix` | Führt `case-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/write-case-matrix.py |
| `install-dev-deps` | Führt `install-dev-deps` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/bootstrap-python.sh |
| `setup-dev` | Führt `setup-dev` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | install-dev-deps | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `fetch-modsecurity-v3` | Führt `fetch-modsecurity-v3` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/fetch-smoke-sources.sh |
| `fetch-crs` | Führt `fetch-crs` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/fetch-crs.sh |
| `prepare-crs` | Führt `prepare-crs` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/prepare-crs.sh, ci/doctor.sh |
| `print-python` | Führt `print-python` aus (Other). | Other | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `bootstrap-all` | Führt `bootstrap-all` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | setup-dev fetch-deps doctor | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `doctor-install-hints` | Führt `doctor-install-hints` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | siehe Makefile/Rezept | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `doctor-quick` | Führt `doctor-quick` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/doctor.sh |
| `quick-all` | Führt `quick-all` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | check-framework | optional/Composite | skriptabhängig | Skript/Rezept: ci/quick-all.sh |
| `cloud-quick-check` | Führt `cloud-quick-check` aus (General setup / lint / bootstrap). | General setup / lint / bootstrap | setup-dev lint generate-test-matrix check-test-matrix quick-check | optional/Composite | skriptabhängig | Skript/Rezept: Makefile composite / shell recipe |
| `generate-test-matrix` | Führt `generate-test-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: ci/ensure-test-matrix-language-switches.py |
| `check-test-matrix` | Führt `check-test-matrix` aus (Framework / reports / runtime harnesses). | Framework / reports / runtime harnesses | check-framework | optional/Composite | ja, bei fehlender Umgebung/Headern/Framework oder optionalem Profil | Skript/Rezept: Makefile composite / shell recipe |

### C17-, C23- und future-C-Ziele

`check-*-c17`-Ziele sind erforderlich, wenn der relevante Compiler und die relevanten Header vorhanden sind. `check-*-c23`-Ziele sind optional. `check-*-future-c`-Ziele sind optional und können `c2y`/`gnu2y` verwenden. `check-*-c20` und `check-*-c26`, soweit vorhanden, sind Skip-/Info-Ziele, weil c20/c26 keine gültigen C-Sprachmodi sind. Exit 77 bedeutet fehlende Umgebung oder nicht unterstütztes optionales Profil; echte Compile- oder Contract-Fehler dürfen dadurch nicht versteckt werden.

## Häufige Makefile-Aufrufe

- `make check-common-helpers`: nach Änderungen an Common-Helfern.
- `make check-common-sdk-contract`: nach Änderungen an Common-SDK-APIs oder Headern.
- `make check-adapter-contracts`: nach Änderungen an Adapter-Metadaten oder Adapter-Verträgen.
- `make check-directive-parity`: nach Änderungen an Direktiven, Config oder Parsern.
- `make check-apache-common-adoption && make check-apache-c17`: nach Apache-Connector-Änderungen.
- `make check-nginx-common-adoption && make check-nginx-c17`: nach NGINX-Connector-Änderungen.
- `make check-haproxy-common-adoption && make check-haproxy-c17`: nach HAProxy-Connector-Änderungen.
- `make check-remaining-connectors-common-adoption && make check-remaining-connectors-c17`: nach Envoy-/Traefik-/lighttpd-Starter-Änderungen; das bleibt nur Compile-/Strukturevidence.
- `make lint`, `make quick-check`, `make codex-check`: aggregierte Validierung, abhängig von Framework- und Umgebungsblockern.

## Exit-Codes und BLOCKED/SKIPPED-Verhalten

- `0`: erfolgreich.
- `1`, `2` oder andere Non-Zero-Werte: echter Fehler oder Usage-Fehler, sofern ein Skript nichts anderes dokumentiert.
- `77`: BLOCKED/SKIPPED wegen fehlender Umgebung, fehlender Header, fehlendem Compiler, fehlendem Framework-Input oder nicht unterstütztem optionalem C-Profil.

Exit 77 darf echte Compile- oder Contract-Fehler nicht verstecken. Lint-Wrapper dürfen umgebungsbedingte Skips übersetzen, aber keine echten Fehler verbergen.

## Umgebungsvariablen

| Variable | Verwendung | Beispiel | Betrifft |
|---|---|---|---|
| `CC` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `CC=...` | Build-/Check-Umgebung |
| `PYTHON` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `PYTHON=...` | Build-/Check-Umgebung |
| `BUILD_ROOT` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `BUILD_ROOT=...` | Build-/Check-Umgebung |
| `MSCONNECTOR_C_STD` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `MSCONNECTOR_C_STD=...` | Build-/Check-Umgebung |
| `MSCONNECTOR_CFLAGS` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `MSCONNECTOR_CFLAGS=...` | Build-/Check-Umgebung |
| `APXS` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `APXS=...` | Build-/Check-Umgebung |
| `NGINX_SOURCE_DIR` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `NGINX_SOURCE_DIR=...` | Build-/Check-Umgebung |
| `NGINX_SRC` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `NGINX_SRC=...` | Build-/Check-Umgebung |
| `MODSECURITY_NGINX_SOURCE_DIR` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `MODSECURITY_NGINX_SOURCE_DIR=...` | Build-/Check-Umgebung |
| `NGINX_INCLUDE_DIR` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `NGINX_INCLUDE_DIR=...` | Build-/Check-Umgebung |
| `MSCONNECTOR_COMMON_SRC` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `MSCONNECTOR_COMMON_SRC=...` | Build-/Check-Umgebung |
| `MODSECURITY_INC` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `MODSECURITY_INC=...` | Build-/Check-Umgebung |
| `MODSECURITY_INCLUDE` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `MODSECURITY_INCLUDE=...` | Build-/Check-Umgebung |
| `MODSECURITY_INCLUDE_DIR` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `MODSECURITY_INCLUDE_DIR=...` | Build-/Check-Umgebung |
| `V3INCLUDE` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `V3INCLUDE=...` | Build-/Check-Umgebung |
| `HAPROXY_SOURCE_DIR` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `HAPROXY_SOURCE_DIR=...` | Build-/Check-Umgebung |
| `HAPROXY_INCLUDE_DIR` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `HAPROXY_INCLUDE_DIR=...` | Build-/Check-Umgebung |
| `CONNECTOR_C_STD_PROFILE` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `CONNECTOR_C_STD_PROFILE=...` | Build-/Check-Umgebung |
| `APACHE_C_STD_PROFILE` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `APACHE_C_STD_PROFILE=...` | Build-/Check-Umgebung |
| `NGINX_C_STD_PROFILE` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `NGINX_C_STD_PROFILE=...` | Build-/Check-Umgebung |
| `HAPROXY_C_STD_PROFILE` | Von Makefile/CI-Skripten genutzt, wenn gesetzt. | `HAPROXY_C_STD_PROFILE=...` | Build-/Check-Umgebung |

## Connector-Modell

Jeder Connector besitzt den Server-API-Glue und bildet host-spezifischen Zustand auf Common-SDK-Verträge ab. Ein Connector muss fehlende Unterstützung als `not supported`, `not applicable`, `connector-gap`, `structure-only`, `partial`, `unknown` oder `requires runtime evidence` kennzeichnen.

## Apache-Connector

### Zweck
Der Apache-Connector belässt die Host-/Server-API-Integration in `connectors/apache/` und nutzt Common-SDK-Verträge, soweit dies umgesetzt ist.

### Aktueller Status
Common-SDK-Adoption ist vorhanden; jeder Runtime-Claim benötigt aktuelle Harness-/Report-Evidence.

### Common-SDK-Adoption
Der Connector kann `msconnector_config`, das Direktiven-Vokabular, Mapper-Verträge, Request-/Response-Modelle, Entscheidungs-/Status-/Ereignis-Helfer und Common-Quellen nutzen. Adoption-Checks sind statische, Contract- oder Compile-Evidence und keine automatische Runtime-Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Host-spezifische Syntax bleibt host-spezifisch. Nicht unterstützte Syntax muss als `not supported`, `not applicable`, `connector-gap`, `partial` oder `requires runtime evidence` gekennzeichnet werden. NGINX darf Apache-artige Transaction-Expressions nicht stillschweigend als NGINX-Syntax akzeptieren.

### Request-Mapping
Der Request-Mapper wandelt Host-Request-Strukturen in `msconnector_request` und gemeinsame Header-Helfer um. Fehlende Host-Details müssen als `partial` oder `requires runtime evidence` behandelt werden.

### Response-Mapping
Der Response-Mapper wandelt Host-Response-, Header- und Body-Zustand in `msconnector_response` um. Response-Body-Verhalten ist nur dann verifiziert, wenn aktuelle Runtime-Evidence dies belegt.

### Decision/Event/JSONL-Verhalten
Die gemeinsamen Decision-, Intervention-, Status- und JSONL-Ereignis-Helfer liefern gemeinsame Semantik. Per-run Events sind nur Evidence für genau diesen Lauf.

### Resource-/Body-/DoS-/Flow-Grenzen
Ressourcenlimits, Body Policy, DoS-Schutz und Flow-Guard sind connector-neutrale Guardrails. Sie beweisen kein runtime-secure Verhalten und keine tamper-proof Evidence.

### C17/C23/future-C-Checks
C17 ist erforderlich, wenn Compiler und benötigte Header vorhanden sind. C23 und future-C sind optional. Exit 77 ist für fehlende Umgebung oder nicht unterstützte optionale Profile reserviert.

### CI-/Contract-Checks
Nutze connector-spezifische Adoption-/C-Standard-Ziele und die gemeinsamen Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Maßgeblich sind die aktuellen Capability-Manifeste und kanonischen Ergebnisse. Die gezielten Hostpfade besitzen `minimal_runtime_smoke`-Evidence; breitere Fähigkeiten bleiben bis zu einem aktuellen kanonischen Ergebnis unverifiziert.

### Umgesetzt
Die unten aufgeführten Connector-Dateien, Metadaten, Dokumente, Harness-Stubs oder Quellen existieren im Repository.

### Fehlend
Alles, was als `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` oder `requires runtime evidence` markiert ist, benötigt noch Evidence oder Implementierung.

### Was connector-spezifisch bleibt
`request_rec`, `command_rec`, APR-Pools, Bucket Brigades, Hooks, Filter, APXS/autotools, Apache-Logging und Return-Codes bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Wichtige Connector-Dateien
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/apache/Makefile.am` | Implementiert bzw. baut `Makefile` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/ORIGIN.md` | Dokumentiert oder implementiert `ORIGIN` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/README.de.md` | Dokumentiert oder implementiert `README.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/SOURCE_MAP.json` | Dokumentiert oder implementiert `SOURCE MAP` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/TODO.md` | Dokumentiert oder implementiert `TODO` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/autogen.sh` | Implementiert bzw. baut `autogen` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/build/apxs-wrapper.in` | Implementiert bzw. baut `apxs wrapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/build/ax_prog_apache.m4` | Implementiert bzw. baut `ax prog apache` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/build/find_apxs.m4` | Implementiert bzw. baut `find apxs` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/build/find_libmodsec.m4` | Implementiert bzw. baut `find libmodsec` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/configure.ac` | Implementiert bzw. baut `configure` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/docs/architecture.md` | Dokumentiert oder implementiert `architecture` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/docs/build.md` | Dokumentiert oder implementiert `build` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/docs/coverage-decision-matrix.de.md` | Dokumentiert oder implementiert `coverage decision matrix.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/docs/coverage-decision-matrix.md` | Dokumentiert oder implementiert `coverage decision matrix` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/docs/public-sources.md` | Dokumentiert oder implementiert `public sources` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/docs/validation.md` | Dokumentiert oder implementiert `validation` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/harness/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/harness/run_apache_smoke.sh` | Implementiert bzw. baut `run apache smoke` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/metadata.c` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/metadata.h` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/mod_security3.c` | Implementiert bzw. baut `mod security3` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/mod_security3.h` | Implementiert bzw. baut `mod security3` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_apache_mapper.c` | Implementiert bzw. baut `msc apache mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_apache_mapper.h` | Implementiert bzw. baut `msc apache mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_config.c` | Implementiert bzw. baut `msc config` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_config.h` | Implementiert bzw. baut `msc config` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_filters.c` | Implementiert bzw. baut `msc filters` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_filters.h` | Implementiert bzw. baut `msc filters` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_utils.c` | Implementiert bzw. baut `msc utils` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/apache/src/msc_utils.h` | Implementiert bzw. baut `msc utils` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |

## NGINX-Connector

### Zweck
Der NGINX-Connector belässt die Host-/Server-API-Integration in `connectors/nginx/` und nutzt Common-SDK-Verträge, soweit dies umgesetzt ist.

### Aktueller Status
Common-SDK-Adoption ist vorhanden; jeder Runtime-Claim benötigt aktuelle Harness-/Report-Evidence.

### Common-SDK-Adoption
Der Connector kann `msconnector_config`, das Direktiven-Vokabular, Mapper-Verträge, Request-/Response-Modelle, Entscheidungs-/Status-/Ereignis-Helfer und Common-Quellen nutzen. Adoption-Checks sind statische, Contract- oder Compile-Evidence und keine automatische Runtime-Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Host-spezifische Syntax bleibt host-spezifisch. Nicht unterstützte Syntax muss als `not supported`, `not applicable`, `connector-gap`, `partial` oder `requires runtime evidence` gekennzeichnet werden. NGINX darf Apache-artige Transaction-Expressions nicht stillschweigend als NGINX-Syntax akzeptieren.

### Request-Mapping
Der Request-Mapper wandelt Host-Request-Strukturen in `msconnector_request` und gemeinsame Header-Helfer um. Fehlende Host-Details müssen als `partial` oder `requires runtime evidence` behandelt werden.

### Response-Mapping
Der Response-Mapper wandelt Host-Response-, Header- und Body-Zustand in `msconnector_response` um. Response-Body-Verhalten ist nur dann verifiziert, wenn aktuelle Runtime-Evidence dies belegt.

### Decision/Event/JSONL-Verhalten
Die gemeinsamen Decision-, Intervention-, Status- und JSONL-Ereignis-Helfer liefern gemeinsame Semantik. Per-run Events sind nur Evidence für genau diesen Lauf.

### Resource-/Body-/DoS-/Flow-Grenzen
Ressourcenlimits, Body Policy, DoS-Schutz und Flow-Guard sind connector-neutrale Guardrails. Sie beweisen kein runtime-secure Verhalten und keine tamper-proof Evidence.

### C17/C23/future-C-Checks
C17 ist erforderlich, wenn Compiler und benötigte Header vorhanden sind. C23 und future-C sind optional. Exit 77 ist für fehlende Umgebung oder nicht unterstützte optionale Profile reserviert.

### CI-/Contract-Checks
Nutze connector-spezifische Adoption-/C-Standard-Ziele und die gemeinsamen Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Maßgeblich sind die aktuellen Capability-Manifeste und kanonischen Ergebnisse. Die gezielten Hostpfade besitzen `minimal_runtime_smoke`-Evidence; breitere Fähigkeiten bleiben bis zu einem aktuellen kanonischen Ergebnis unverifiziert.

### Umgesetzt
Die unten aufgeführten Connector-Dateien, Metadaten, Dokumente, Harness-Stubs oder Quellen existieren im Repository.

### Fehlend
Alles, was als `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` oder `requires runtime evidence` markiert ist, benötigt noch Evidence oder Implementierung.

### Was connector-spezifisch bleibt
`ngx_http_request_t`, `ngx_command_t`, `ngx_chain_t`, `ngx_buf_t`, `headers_in`/`headers_out`, Filter, Pools, Return-Codes und NGINX-Modul-Build-Glue bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Wichtige Connector-Dateien
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/nginx/ORIGIN.md` | Dokumentiert oder implementiert `ORIGIN` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/README.de.md` | Dokumentiert oder implementiert `README.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/SOURCE_MAP.json` | Dokumentiert oder implementiert `SOURCE MAP` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/TODO.md` | Dokumentiert oder implementiert `TODO` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/config` | Implementiert bzw. baut `config` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/docs/architecture.md` | Dokumentiert oder implementiert `architecture` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/docs/build.md` | Dokumentiert oder implementiert `build` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/docs/coverage-decision-matrix.de.md` | Dokumentiert oder implementiert `coverage decision matrix.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/docs/coverage-decision-matrix.md` | Dokumentiert oder implementiert `coverage decision matrix` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/docs/public-sources.md` | Dokumentiert oder implementiert `public sources` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/docs/validation.md` | Dokumentiert oder implementiert `validation` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/harness/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/harness/run_nginx_smoke.sh` | Implementiert bzw. baut `run nginx smoke` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/metadata.c` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/metadata.h` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ddebug.h` | Implementiert bzw. baut `ddebug` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_access.c` | Implementiert bzw. baut `ngx http modsecurity access` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_body_filter.c` | Implementiert bzw. baut `ngx http modsecurity body filter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | Implementiert bzw. baut `ngx http modsecurity common` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_header_filter.c` | Implementiert bzw. baut `ngx http modsecurity header filter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_log.c` | Implementiert bzw. baut `ngx http modsecurity log` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.c` | Implementiert bzw. baut `ngx http modsecurity mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_mapper.h` | Implementiert bzw. baut `ngx http modsecurity mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/nginx/src/ngx_http_modsecurity_module.c` | Implementiert bzw. baut `ngx http modsecurity module` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |

## HAProxy-Connector

### Zweck
Der HAProxy-Connector belässt die Host-/Server-API-Integration in `connectors/haproxy/` und nutzt Common-SDK-Verträge, soweit dies umgesetzt ist.

### Aktueller Status
Common-SDK-Adoption ist vorhanden; jeder Runtime-Claim benötigt aktuelle Harness-/Report-Evidence.

### Common-SDK-Adoption
Der Connector kann `msconnector_config`, das Direktiven-Vokabular, Mapper-Verträge, Request-/Response-Modelle, Entscheidungs-/Status-/Ereignis-Helfer und Common-Quellen nutzen. Adoption-Checks sind statische, Contract- oder Compile-Evidence und keine automatische Runtime-Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Host-spezifische Syntax bleibt host-spezifisch. Nicht unterstützte Syntax muss als `not supported`, `not applicable`, `connector-gap`, `partial` oder `requires runtime evidence` gekennzeichnet werden. NGINX darf Apache-artige Transaction-Expressions nicht stillschweigend als NGINX-Syntax akzeptieren.

### Request-Mapping
Der Request-Mapper wandelt Host-Request-Strukturen in `msconnector_request` und gemeinsame Header-Helfer um. Fehlende Host-Details müssen als `partial` oder `requires runtime evidence` behandelt werden.

### Response-Mapping
Der Response-Mapper wandelt Host-Response-, Header- und Body-Zustand in `msconnector_response` um. Response-Body-Verhalten ist nur dann verifiziert, wenn aktuelle Runtime-Evidence dies belegt.

### Decision/Event/JSONL-Verhalten
Die gemeinsamen Decision-, Intervention-, Status- und JSONL-Ereignis-Helfer liefern gemeinsame Semantik. Per-run Events sind nur Evidence für genau diesen Lauf.

### Resource-/Body-/DoS-/Flow-Grenzen
Ressourcenlimits, Body Policy, DoS-Schutz und Flow-Guard sind connector-neutrale Guardrails. Sie beweisen kein runtime-secure Verhalten und keine tamper-proof Evidence.

### C17/C23/future-C-Checks
C17 ist erforderlich, wenn Compiler und benötigte Header vorhanden sind. C23 und future-C sind optional. Exit 77 ist für fehlende Umgebung oder nicht unterstützte optionale Profile reserviert.

### CI-/Contract-Checks
Nutze connector-spezifische Adoption-/C-Standard-Ziele und die gemeinsamen Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Maßgeblich sind die aktuellen Capability-Manifeste und kanonischen Ergebnisse. Die gezielten Hostpfade besitzen `minimal_runtime_smoke`-Evidence; breitere Fähigkeiten bleiben bis zu einem aktuellen kanonischen Ergebnis unverifiziert.

### Umgesetzt
Die unten aufgeführten Connector-Dateien, Metadaten, Dokumente, Harness-Stubs oder Quellen existieren im Repository.

### Fehlend
Alles, was als `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` oder `requires runtime evidence` markiert ist, benötigt noch Evidence oder Implementierung.

### Was connector-spezifisch bleibt
SPOE/SPOP, Frame-Parsing, Runtime-Loop, Socket-Handling, HAProxy-Konfigurationsausschnitte, Prozess-Lifecycle und Build-Glue bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Wichtige Connector-Dateien
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/haproxy/Makefile` | Implementiert bzw. baut `Makefile` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/ORIGIN.md` | Dokumentiert oder implementiert `ORIGIN` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/README.de.md` | Dokumentiert oder implementiert `README.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/SOURCE_MAP.json` | Dokumentiert oder implementiert `SOURCE MAP` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/TODO.md` | Dokumentiert oder implementiert `TODO` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/architecture.md` | Dokumentiert oder implementiert `architecture` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/build.md` | Dokumentiert oder implementiert `build` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/coverage-decision-matrix.de.md` | Dokumentiert oder implementiert `coverage decision matrix.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/coverage-decision-matrix.md` | Dokumentiert oder implementiert `coverage decision matrix` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/evidence-findings.de.md` | Dokumentiert oder implementiert `evidence findings.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/evidence-findings.md` | Dokumentiert oder implementiert `evidence findings` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/evidence-questionnaire.de.md` | Dokumentiert oder implementiert `evidence questionnaire.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/evidence-questionnaire.md` | Dokumentiert oder implementiert `evidence questionnaire` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/integration-decision.md` | Dokumentiert oder implementiert `integration decision` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/public-sources.md` | Dokumentiert oder implementiert `public sources` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/spoe-external-evidence.de.md` | Dokumentiert oder implementiert `spoe external evidence.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/spoe-external-evidence.md` | Dokumentiert oder implementiert `spoe external evidence` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/spoe-minimal-artifacts.md` | Dokumentiert oder implementiert `spoe minimal artifacts` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/spoe-poc-plan.md` | Dokumentiert oder implementiert `spoe poc plan` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/test-framework-contract.md` | Dokumentiert oder implementiert `test framework contract` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/docs/validation.md` | Dokumentiert oder implementiert `validation` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/harness/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | Implementiert bzw. baut `run haproxy smoke` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/metadata.c` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/metadata.h` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/agent/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/agent/design.md` | Dokumentiert oder implementiert `design` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/harness/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/harness/design.md` | Dokumentiert oder implementiert `design` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/reports/README.de.md` | Dokumentiert oder implementiert `README.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/reports/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/poc/spoe/syntax-validation.md` | Dokumentiert oder implementiert `syntax validation` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_modsecurity_binding.c` | Implementiert bzw. baut `haproxy modsecurity binding` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_modsecurity_binding.h` | Implementiert bzw. baut `haproxy modsecurity binding` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c` | Implementiert bzw. baut `haproxy modsecurity binding self test` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.c` | Implementiert bzw. baut `haproxy modsecurity mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_modsecurity_mapper.h` | Implementiert bzw. baut `haproxy modsecurity mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | Implementiert bzw. baut `haproxy spoa agent starter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | Implementiert bzw. baut `haproxy spoa agent starter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_spoa_main.c` | Implementiert bzw. baut `haproxy spoa main` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | Implementiert bzw. baut `haproxy spop diagnostic runtime` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | vorhanden; Runtime-Claims benötigen aktuelle Evidence |

## Envoy-Connector

### Zweck
Der Envoy-Connector belässt die Host-/Server-API-Integration in `connectors/envoy/` und nutzt Common-SDK-Verträge, soweit dies umgesetzt ist.

### Aktueller Status
minimal_runtime_smoke / connector-gap; gezielter echter Host-Laufzeitpfad; kanonisches No-CRS nicht ausgefuehrt; kein Production-, CRS-, Full-Matrix- oder RESPONSE_BODY-Claim.

### Common-SDK-Adoption
Der Connector kann `msconnector_config`, das Direktiven-Vokabular, Mapper-Verträge, Request-/Response-Modelle, Entscheidungs-/Status-/Ereignis-Helfer und Common-Quellen nutzen. Adoption-Checks sind statische, Contract- oder Compile-Evidence und keine automatische Runtime-Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Host-spezifische Syntax bleibt host-spezifisch. Nicht unterstützte Syntax muss als `not supported`, `not applicable`, `connector-gap`, `partial` oder `requires runtime evidence` gekennzeichnet werden. NGINX darf Apache-artige Transaction-Expressions nicht stillschweigend als NGINX-Syntax akzeptieren.

### Request-Mapping
Der Request-Mapper wandelt Host-Request-Strukturen in `msconnector_request` und gemeinsame Header-Helfer um. Fehlende Host-Details müssen als `partial` oder `requires runtime evidence` behandelt werden.

### Response-Mapping
Der Response-Mapper wandelt Host-Response-, Header- und Body-Zustand in `msconnector_response` um. Response-Body-Verhalten ist nur dann verifiziert, wenn aktuelle Runtime-Evidence dies belegt.

### Decision/Event/JSONL-Verhalten
Die gemeinsamen Decision-, Intervention-, Status- und JSONL-Ereignis-Helfer liefern gemeinsame Semantik. Per-run Events sind nur Evidence für genau diesen Lauf.

### Resource-/Body-/DoS-/Flow-Grenzen
Ressourcenlimits, Body Policy, DoS-Schutz und Flow-Guard sind connector-neutrale Guardrails. Sie beweisen kein runtime-secure Verhalten und keine tamper-proof Evidence.

### C17/C23/future-C-Checks
C17 ist erforderlich, wenn Compiler und benötigte Header vorhanden sind. C23 und future-C sind optional. Exit 77 ist für fehlende Umgebung oder nicht unterstützte optionale Profile reserviert.

### CI-/Contract-Checks
Nutze connector-spezifische Adoption-/C-Standard-Ziele und die gemeinsamen Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Maßgeblich sind die aktuellen Capability-Manifeste und kanonischen Ergebnisse. Die gezielten Hostpfade besitzen `minimal_runtime_smoke`-Evidence; breitere Fähigkeiten bleiben bis zu einem aktuellen kanonischen Ergebnis unverifiziert.

### Umgesetzt
Die unten aufgeführten Connector-Dateien, Metadaten, Dokumente, Harness-Stubs oder Quellen existieren im Repository.

### Fehlend
Alles, was als `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` oder `requires runtime evidence` markiert ist, benötigt noch Evidence oder Implementierung.

### Was connector-spezifisch bleibt
Envoy-Filter-/Runtime-API, Besitz nativer Envoy-SDK-Integration und ausgerollte Proxy-Integration bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Wichtige Connector-Dateien
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/envoy/Makefile` | Implementiert bzw. baut `Makefile` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/ORIGIN.md` | Dokumentiert oder implementiert `ORIGIN` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/README.de.md` | Dokumentiert oder implementiert `README.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/SOURCE_MAP.json` | Dokumentiert oder implementiert `SOURCE MAP` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/TODO.md` | Dokumentiert oder implementiert `TODO` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/build/build_metadata.sh` | Implementiert bzw. baut `build metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/architecture.md` | Dokumentiert oder implementiert `architecture` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/build.md` | Dokumentiert oder implementiert `build` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.de.md` | Dokumentiert oder implementiert `coverage decision matrix.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/coverage-decision-matrix.md` | Dokumentiert oder implementiert `coverage decision matrix` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/public-sources.md` | Dokumentiert oder implementiert `public sources` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/docs/validation.md` | Dokumentiert oder implementiert `validation` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/harness/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/harness/run_envoy_smoke.sh` | Implementiert bzw. baut `run envoy smoke` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/metadata.c` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/metadata.h` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_bridge.c` | Implementiert bzw. baut `envoy bridge` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_bridge.h` | Implementiert bzw. baut `envoy bridge` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_bridge_main.c` | Implementiert bzw. baut `envoy bridge main` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/envoy/src/envoy_modsecurity_mapper.h` | Implementiert bzw. baut `envoy modsecurity mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |

## Traefik-Connector

### Zweck
Der Traefik-Connector belässt die Host-/Server-API-Integration in `connectors/traefik/` und nutzt Common-SDK-Verträge, soweit dies umgesetzt ist.

### Aktueller Status
minimal_runtime_smoke / connector-gap; gezielter echter Host-Laufzeitpfad; kanonisches No-CRS nicht ausgefuehrt; kein Production-, CRS-, Full-Matrix- oder RESPONSE_BODY-Claim.

### Common-SDK-Adoption
Der Connector kann `msconnector_config`, das Direktiven-Vokabular, Mapper-Verträge, Request-/Response-Modelle, Entscheidungs-/Status-/Ereignis-Helfer und Common-Quellen nutzen. Adoption-Checks sind statische, Contract- oder Compile-Evidence und keine automatische Runtime-Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Host-spezifische Syntax bleibt host-spezifisch. Nicht unterstützte Syntax muss als `not supported`, `not applicable`, `connector-gap`, `partial` oder `requires runtime evidence` gekennzeichnet werden. NGINX darf Apache-artige Transaction-Expressions nicht stillschweigend als NGINX-Syntax akzeptieren.

### Request-Mapping
Der Request-Mapper wandelt Host-Request-Strukturen in `msconnector_request` und gemeinsame Header-Helfer um. Fehlende Host-Details müssen als `partial` oder `requires runtime evidence` behandelt werden.

### Response-Mapping
Der Response-Mapper wandelt Host-Response-, Header- und Body-Zustand in `msconnector_response` um. Response-Body-Verhalten ist nur dann verifiziert, wenn aktuelle Runtime-Evidence dies belegt.

### Decision/Event/JSONL-Verhalten
Die gemeinsamen Decision-, Intervention-, Status- und JSONL-Ereignis-Helfer liefern gemeinsame Semantik. Per-run Events sind nur Evidence für genau diesen Lauf.

### Resource-/Body-/DoS-/Flow-Grenzen
Ressourcenlimits, Body Policy, DoS-Schutz und Flow-Guard sind connector-neutrale Guardrails. Sie beweisen kein runtime-secure Verhalten und keine tamper-proof Evidence.

### C17/C23/future-C-Checks
C17 ist erforderlich, wenn Compiler und benötigte Header vorhanden sind. C23 und future-C sind optional. Exit 77 ist für fehlende Umgebung oder nicht unterstützte optionale Profile reserviert.

### CI-/Contract-Checks
Nutze connector-spezifische Adoption-/C-Standard-Ziele und die gemeinsamen Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Maßgeblich sind die aktuellen Capability-Manifeste und kanonischen Ergebnisse. Die gezielten Hostpfade besitzen `minimal_runtime_smoke`-Evidence; breitere Fähigkeiten bleiben bis zu einem aktuellen kanonischen Ergebnis unverifiziert.

### Umgesetzt
Die unten aufgeführten Connector-Dateien, Metadaten, Dokumente, Harness-Stubs oder Quellen existieren im Repository.

### Fehlend
Alles, was als `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` oder `requires runtime evidence` markiert ist, benötigt noch Evidence oder Implementierung.

### Was connector-spezifisch bleibt
Traefik-Middleware-/Proxy-/Runtime-API und echte Traffic-Path-Integration bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Wichtige Connector-Dateien
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/traefik/Makefile` | Implementiert bzw. baut `Makefile` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/ORIGIN.md` | Dokumentiert oder implementiert `ORIGIN` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/README.de.md` | Dokumentiert oder implementiert `README.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/SOURCE_MAP.json` | Dokumentiert oder implementiert `SOURCE MAP` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/TODO.md` | Dokumentiert oder implementiert `TODO` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/build/build-starter.sh` | Implementiert bzw. baut `build starter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/architecture.md` | Dokumentiert oder implementiert `architecture` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/build.md` | Dokumentiert oder implementiert `build` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.de.md` | Dokumentiert oder implementiert `coverage decision matrix.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/coverage-decision-matrix.md` | Dokumentiert oder implementiert `coverage decision matrix` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/public-sources.md` | Dokumentiert oder implementiert `public sources` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/docs/validation.md` | Dokumentiert oder implementiert `validation` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/harness/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/harness/run_traefik_smoke.sh` | Implementiert bzw. baut `run traefik smoke` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/metadata.c` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/metadata.h` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_build_starter.c` | Implementiert bzw. baut `traefik build starter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_decision_service.c` | Implementiert bzw. baut `traefik decision service` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_decision_service.h` | Implementiert bzw. baut `traefik decision service` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_decision_service_main.c` | Implementiert bzw. baut `traefik decision service main` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |
| `connectors/traefik/src/traefik_modsecurity_mapper.h` | Implementiert bzw. baut `traefik modsecurity mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / connector-gap |

## lighttpd-Connector

### Zweck
Der lighttpd-Connector belässt die Host-/Server-API-Integration in `connectors/lighttpd/` und nutzt Common-SDK-Verträge, soweit dies umgesetzt ist.

### Aktueller Status
minimal_runtime_smoke / partial_runtime_path; gezielter echter Host-Laufzeitpfad; kanonisches No-CRS nicht ausgeführt; kein Production-, CRS-, Full-Matrix- oder RESPONSE_BODY-Claim.

### Common-SDK-Adoption
Der Connector kann `msconnector_config`, das Direktiven-Vokabular, Mapper-Verträge, Request-/Response-Modelle, Entscheidungs-/Status-/Ereignis-Helfer und Common-Quellen nutzen. Adoption-Checks sind statische, Contract- oder Compile-Evidence und keine automatische Runtime-Evidence.

### Config-/Directive-Unterstützung
Unterstützte Common-Direktiven stehen in der Direktiventabelle. Host-spezifische Syntax bleibt host-spezifisch. Nicht unterstützte Syntax muss als `not supported`, `not applicable`, `connector-gap`, `partial` oder `requires runtime evidence` gekennzeichnet werden. NGINX darf Apache-artige Transaction-Expressions nicht stillschweigend als NGINX-Syntax akzeptieren.

### Request-Mapping
Der Request-Mapper wandelt Host-Request-Strukturen in `msconnector_request` und gemeinsame Header-Helfer um. Fehlende Host-Details müssen als `partial` oder `requires runtime evidence` behandelt werden.

### Response-Mapping
Der Response-Mapper wandelt Host-Response-, Header- und Body-Zustand in `msconnector_response` um. Response-Body-Verhalten ist nur dann verifiziert, wenn aktuelle Runtime-Evidence dies belegt.

### Decision/Event/JSONL-Verhalten
Die gemeinsamen Decision-, Intervention-, Status- und JSONL-Ereignis-Helfer liefern gemeinsame Semantik. Per-run Events sind nur Evidence für genau diesen Lauf.

### Resource-/Body-/DoS-/Flow-Grenzen
Ressourcenlimits, Body Policy, DoS-Schutz und Flow-Guard sind connector-neutrale Guardrails. Sie beweisen kein runtime-secure Verhalten und keine tamper-proof Evidence.

### C17/C23/future-C-Checks
C17 ist erforderlich, wenn Compiler und benötigte Header vorhanden sind. C23 und future-C sind optional. Exit 77 ist für fehlende Umgebung oder nicht unterstützte optionale Profile reserviert.

### CI-/Contract-Checks
Nutze connector-spezifische Adoption-/C-Standard-Ziele und die gemeinsamen Contract-Ziele. Compile- und Contract-Checks erzeugen keine Production-, CRS-, Full-Matrix- oder Runtime-Claims.

### Runtime-Evidence-Status
Maßgeblich sind die aktuellen Capability-Manifeste und kanonischen Ergebnisse. Die gezielten Hostpfade besitzen `minimal_runtime_smoke`-Evidence; breitere Fähigkeiten bleiben bis zu einem aktuellen kanonischen Ergebnis unverifiziert.

### Umgesetzt
Die unten aufgeführten Connector-Dateien, Metadaten, Dokumente, Harness-Stubs oder Quellen existieren im Repository.

### Fehlend
Alles, was als `connector-gap`, `not_verified`, `structure-only`, `partial`, `unknown` oder `requires runtime evidence` markiert ist, benötigt noch Evidence oder Implementierung.

### Was connector-spezifisch bleibt
lighttpd-Plugin-/Proxy-/Runtime-API und FastCGI-/SCGI-/native Modul-Integration bleiben connector-spezifisch und dürfen nicht nach `common/` verschoben werden.

### Wichtige Connector-Dateien
| Datei | Zweck | Common-Bezug | Connector-spezifisch? | Status |
|---|---|---|---|---|
| `connectors/lighttpd/Makefile` | Implementiert bzw. baut `Makefile` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/ORIGIN.md` | Dokumentiert oder implementiert `ORIGIN` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/README.de.md` | Dokumentiert oder implementiert `README.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/SOURCE_MAP.json` | Dokumentiert oder implementiert `SOURCE MAP` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/TODO.md` | Dokumentiert oder implementiert `TODO` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/build/bridge_starter.sh` | Implementiert bzw. baut `bridge starter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/build/build_starter.sh` | Implementiert bzw. baut `build starter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/architecture.md` | Dokumentiert oder implementiert `architecture` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/build.md` | Dokumentiert oder implementiert `build` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/coverage-decision-matrix.de.md` | Dokumentiert oder implementiert `coverage decision matrix.de` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/coverage-decision-matrix.md` | Dokumentiert oder implementiert `coverage decision matrix` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/public-sources.md` | Dokumentiert oder implementiert `public sources` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/docs/validation.md` | Dokumentiert oder implementiert `validation` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/harness/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/harness/run_lighttpd_smoke.sh` | Implementiert bzw. baut `run lighttpd smoke` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/metadata.c` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/metadata.h` | Implementiert bzw. baut `metadata` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | Metadaten/Dokumentation | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/README.md` | Dokumentiert oder implementiert `README` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_bridge.c` | Implementiert bzw. baut `lighttpd bridge` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_bridge.h` | Implementiert bzw. baut `lighttpd bridge` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_bridge_main.c` | Implementiert bzw. baut `lighttpd bridge main` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_build_starter.c` | Implementiert bzw. baut `lighttpd build starter` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |
| `connectors/lighttpd/src/lighttpd_modsecurity_mapper.h` | Implementiert bzw. baut `lighttpd modsecurity mapper` im Connector-Bereich | nutzt Common-Contracts, wenn im Quelltext eingebunden; Host-API bleibt connector-spezifisch | ja | minimal_runtime_smoke / partial_runtime_path |

## Connector-Statusmatrix

| Connector | Aktueller Status | Common-Adoption | Runtime-Evidence | Verbotene Schlussfolgerung |
|---|---|---|---|---|
| Apache | Connector-Quellen vorhanden | vorhanden | benötigt aktuelle Reports/Harness-Ausgabe | kein Production-/Runtime-/CRS-/Full-Matrix-Claim |
| NGINX | Connector-Quellen vorhanden | vorhanden | benötigt aktuelle Reports/Harness-Ausgabe | kein Production-/Runtime-/CRS-/Full-Matrix-Claim |
| HAProxy | SPOA-/Starter- sowie Mapper-/Binding-Quellen vorhanden | vorhanden/partial | benötigt aktuelle Reports/Harness-Ausgabe | kein Production-/Runtime-/CRS-/Full-Matrix-Claim |
| Envoy | HTTP-`ext_authz`-Service | adoptiert | gezielter Request-Header-200/403-Pfad; kanonisches No-CRS `NOT EXECUTED` | Upstream-Response-Phasen sind `UNSUPPORTED`; kein breiterer Claim |
| Traefik | HTTP-`forwardAuth`-Service | adoptiert | gezielter Request-Header-200/403-Pfad; kanonisches No-CRS `NOT EXECUTED` | nativer Request-Body `NOT IMPLEMENTED`; Upstream-Response `UNSUPPORTED` |
| lighttpd | natives Plugin | adoptiert | gezielter Phase-1-200/403-Pfad; kanonisches No-CRS `NOT EXECUTED` | Bodies `NOT IMPLEMENTED`; Phase 3 `IMPLEMENTED, NOT ASSERTED` |

## Test-Framework-Bezug

Das wiederverwendbare Test-Framework wird unter `modules/ModSecurity-test-Framework` erwartet. Framework-abhängige Targets können BLOCKED sein, wenn Submodule, Framework-Dokumente, Fixtures oder Runtime-Komponenten fehlen. Das bedeutet nicht automatisch, dass ein Common-SDK- oder Connector-Compile-Check fehlgeschlagen ist.

## Runtime-Evidence und Verifikationsrichtlinie

Connector-Metadaten beschreiben den repository-weiten Connector-Status. Ein
kanonisches `result.json` beschreibt nur einen Lauf und muss zu Connector-Commit,
Framework-Commit, Capability-Manifest und Evidence-Layout passen. Ältere
Starter-, Self-Test-, Sidecar-, CRS- und gezielte Smoke-Ergebnisse werden nicht
in ein kanonisches No-CRS-Ergebnis übernommen.

## Umgesetzt

Umgesetzte Repository-Fakten umfassen das Common SDK, connector-spezifische
Hostadapter für alle sechs Connectoren, kanonische Capability-Manifeste,
getrennte Evidence-Stufen, C17/C23/future-C-Check-Wiring, CI-/Governance-Skripte
sowie Dokumentations- und Report-Bereiche. Implementierung gilt als
`IMPLEMENTED, NOT ASSERTED`, bis aktuelle kanonische Evidence das Verhalten
belegt.

## Fehlend / Nächste Schritte

Offene oder spätere Arbeiten umfassen die Ausführung der kanonischen
No-CRS-Baseline, connector-spezifische Capability-Lücken, spätere CRS- oder
Extended-Matrix-Arbeit, Production-Härtung und nur jene Response-Phasen, die das
jeweilige Hostmodell unterstützt.

## Bekannte Grenzen

Bekannte Grenzen sind connector-spezifische Host-APIs, umgebungsabhängige
Header/Toolchains, Framework-/Submodule-Blocker, partielle Runtime-Coverage und
Dokumentation, die mit Capability-Manifesten und kanonischen Ergebnissen
synchron bleiben muss.

## Bewusst connector-spezifisch

Apache-Request-/APR-/Filter-/APXS-Details, NGINX-Request-/Chain-/Filter-/Modul-Glue, HAProxy-SPOE-/SPOP-/Frame-/Runtime-Loop, Envoy-APIs, Traefik-APIs und lighttpd-APIs bleiben außerhalb von `common/`.

## KI-Faktenblock

```yaml
repository: Easton97-Jens/ModSecurity-conector
purpose: Gemeinsame Common-SDK-Schicht für ModSecurity-Connectoren
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

## Erlaubte und verbotene Claims

Erlaubte Claims sind connector-neutrale Common-SDK-Semantik, C17-Pflichtchecks
bei vorhandener Umgebung, optionale C23-/future-C-Checks, Capability-Zustände
aus `connectors/<name>/capabilities.json` und per-run Evidence mit Gültigkeit nur
für diesen Lauf. Ohne aktuelle explizite Evidence dürfen nicht behauptet
werden: production-ready, runtime secure, security verified, CRS verified, full
matrix verified, über alle Connectoren verifizierter Response Body, production
hardened, tamper-proof oder cryptographic integrity.

## Glossar

- `common`: connector-neutrales SDK und Semantik.
- `connector-gap`: bekannte Lücke zwischen Starter/Struktur und echter Connector-Runtime-Integration.
- `not_verified`: kein aktueller repository-weiter Runtime-Verifikations-Claim.
- `structure-only`: Dateien/Scaffolding existieren, beweisen aber kein Runtime-Verhalten.
- `compile-only`: nur Compiler-/Static-Check-Evidence.
- `runtime evidence`: aktueller Lauf/Report, der konkretes Runtime-Verhalten belegt.
- `SOURCE_MAP`: Metadaten für Connector-Source-/Origin-/Status-Mapping.

## Wartungs-Checkliste

```text
- Neue Common-Datei -> Common-SDK-Dateiindex aktualisieren.
- Neue Directive -> directives.h, directive_spec, directive_adapter und docs aktualisieren.
- Neuer Parser -> Config-/Directive-Tabelle aktualisieren.
- Neuer Connector -> Statusmatrix aktualisieren.
- Neuer C-Source -> C17-Source-Liste aktualisieren.
- Neuer Header -> Header-Smoke-Checks aktualisieren.
- Neuer Mapper -> Ownership/Cleanup prüfen.
- Statusänderung -> metadata, SOURCE_MAP, Reports und docs synchron halten.
- Deutsche Doku immer mit englischer Doku synchron halten.
- Runtime-Claims nur mit Evidence.
```
