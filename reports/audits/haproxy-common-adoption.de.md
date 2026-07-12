# HAProxy Common SDK-Adoption

**Sprache:** [English](haproxy-common-adoption.md) | Deutsch

Dieser Bericht dokumentiert die Migrationsgrenze der HAProxy-Adoptionsschicht. Die Evidence ist nur Compile-/Struktur-Evidence: Sie ist kein Claim fuer Produktion, CRS, Full-Matrix oder Runtime-Verifikation.

| Lokale HAProxy-Funktion / lokales Feld | Common-Ersatz | Aktion | Grund |
| --- | --- | --- | --- |
| `haproxy_modsecurity_engine_config.common_config` | `msconnector_config` | ersetzt | Die HAProxy-Engine-Konfiguration bettet die connector-neutrale Konfiguration ein; HAProxy behaelt nur SPOA/libmodsecurity-Pfade und Prozess-Glue lokal. |
| Lokale Config-Defaults/Merge/Validierung | `msconnector_config_init`, `msconnector_config_apply_defaults`, `msconnector_config_merge`, `msconnector_config_validate` | ersetzt | Semantische Defaults, Vererbung und Validierung leben in Common. |
| HAProxy-Optionsnamen fuer ModSecurity-Directives | `MSCONNECTOR_DIRECTIVE_*`, `msconnector_directive_spec`, `msconnector_directive_adapter` | als duenner Adapter behalten | HAProxy-Parsing/Registrierung bleibt Host-Glue; Directive-Semantik und Argument-Policy gehoeren Common. |
| Bool-/Phase4-/Size-/HTTP-Status-Parsing | `msconnector_parse_bool`, `msconnector_parse_phase4_mode`, `msconnector_parse_size`, `msconnector_parse_http_status` | ersetzt | Common besitzt primitives Options-Parsing. |
| Request-Strukturprojektion | `msconnector_request`, `msconnector_request_mapper_contract` | als duenner Adapter behalten | HAProxy/SPOE-Felder werden in Common-Request-Ausgabe gemappt und durch den Common-Mapper-Vertrag validiert. |
| Response-Strukturprojektion | `msconnector_response`, `msconnector_response_mapper_contract` | als duenner Adapter behalten | HAProxy-Response-Metadaten werden in Common-Response-Ausgabe gemappt und durch den Common-Mapper-Vertrag validiert. |
| Host-/Header-Lookup | `msconnector_headers_host`, `msconnector_headers_find*`, `msconnector_headers_parse_content_length` | ersetzt | Header-Semantik gehoert Common; HAProxy behaelt nur Frame-/String-Lifetime-Mapping. |
| Decision-/Intervention-Felder | `msconnector_decision`, `msconnector_late_intervention` | als duenner Adapter behalten | libmodsecurity-Intervention-Capture bleibt HAProxy-Binding-Glue, waehrend Decision-Semantik durch Common-Primitiven dargestellt wird. |
| JSON-Escaping / Event-JSONL | `msconnector_json_escape`, `msconnector_event_write_jsonl_line` | als duenner Adapter behalten | HAProxy-spezifischer Logtransport kann lokal bleiben; JSON-Syntax und Event-Semantik gehoeren Common. |
| Rule-ID-Extraktion | `msconnector_rule_id_extract_from_message` | ersetzt | Rule-ID-Extraktion ist connector-neutral. |
| Log-Sanitizing/Redaction | `msconnector_sanitize_log_message`, `msconnector_redaction` | ersetzt | Sanitizing- und Redaction-Semantik gehoeren Common; Body-Payloads werden nicht geloggt. |
| Limits / DoS / Flow / Integrity | `msconnector_resource_limits`, `msconnector_dos_guard_check_*`, `msconnector_flow_guard`, `msconnector_integrity_event_hash` | als duenner Adapter behalten | Globale Limits und Guards gehoeren Common; HAProxy-Runtime-State entscheidet, wann Phasen beobachtbar sind. |
| Rule-Loading-Statistiken | `msconnector_rule_load_stats`, `msconnector_rule_loader` | als duenner Adapter behalten | libmodsecurity-Loading-Callbacks bleiben HAProxy-Binding-Glue; Statistiken nutzen Common-Strukturen, wo semantisches Zaehlen offengelegt ist. |
| CRS-Setup-Felder | `msconnector_crs_config` | als duenner Adapter behalten | CRS-Setup-Konsistenz gehoert Common; es wird kein CRS-Runtime-verifizierter Claim erhoben. |
| SPOE/SPOP-Frame-Parsing und Socket-Runtime | keiner | behalten, weil HAProxy-spezifisch | Protokoll, Prozesslebenszyklus, Socket-Handling, Return-/Action-Encoding und generierte HAProxy-Cfg-Snippets sind connector-owned. |

## Entfernte Duplikate

Die HAProxy-Adoptionsschicht enthaelt keine eigenstaendigen doppelten Parser, JSON-Escape-, Rule-ID-, Config-Merge-, Config-Validation-, Header-Lookup- oder Status-Normalisierungshelper mehr, wenn ein Common-Primitiv existiert. Verbleibender Code ist Connector-Glue um HAProxy/SPOE/SPOP- und libmodsecurity-APIs.

## C-Standard-Evidence

`ci/checks/connectors/haproxy/check-haproxy-c-standards.sh` fuehrt einen harten C17-Objekt-Compile aus, wenn HAProxy- und libmodsecurity-Header auffindbar sind. C23 und future-C (`c2y`) sind optional und melden skipped, wenn der Compiler sie nicht unterstuetzt. Fehlende HAProxy- oder libmodsecurity-Header werden als `BLOCKED` mit Exit-Code 77 gemeldet.
