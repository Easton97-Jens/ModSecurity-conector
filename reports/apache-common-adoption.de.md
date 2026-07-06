# Apache Common SDK-Adoptionsbericht

**Sprache:** [English](apache-common-adoption.md) | Deutsch

Dieser Bericht dokumentiert den Duplicate-Scan vor der Änderung und die daraus entstandene Trennung zwischen Apache und Common. Er ist nur ein Struktur-Adoptionsbericht; er beansprucht keine Produktionsreife, CRS-Bereitschaft, Full-Matrix-Abdeckung oder Runtime-Verifikation.

| Lokale Apache-Funktion / lokales Feld | Common-Ersatz | Aktion | Grund |
|---|---|---|---|
| `msc_conf_t.msc_state` | `msconnector_config.enable` | ersetzt | Enable-, Default- und Merge-Semantik sind connector-neutrale Konfigurationssemantik. |
| `msc_conf_t.use_error_log` | `msconnector_config.use_error_log` | ersetzt | Common besitzt die boolesche Einstellung; Apache nutzt sie nur fuer APLOG-Weiterleitung. |
| `msc_conf_t.transaction_id` | `msconnector_config.transaction_id` | ersetzt | Ablage, Merge und Validierung statischer Transaction-IDs gehoeren zu Common. |
| Semantik des Strings `msc_conf_t.transaction_id_expr` | `msconnector_config.transaction_id_expr` | als duenner Adapter behalten | Apache muss das kompilierte `ap_expr_info_t` behalten; der Roh-Ausdruck wird in die Common-Konfiguration gespiegelt. |
| `msc_conf_t.phase4_mode` | `msconnector_config.phase4_mode` und `msconnector_parse_phase4_mode` | ersetzt | Phase-4-Modusnamen und Defaults sind Common-Semantik. |
| `msc_conf_t.phase4_content_types_file` | `msconnector_config.phase4_content_types_file` | ersetzt | Pfadablage und Merge sind Common; APR-Dateiparsing bleibt Apache-Adaptercode. |
| `msc_conf_t.phase4_log_path` | `msconnector_config.phase4_log_path` | ersetzt | Common besitzt die Einstellung; Apache oeffnet nur die APR-Datei. |
| `msc_conf_t.phase4_body_limit` | `msconnector_config.phase4_body_limit` und `msconnector_parse_size` | ersetzt | Size-Parsing, Defaults und Merge sind Common-Semantik. |
| Manuelles Bool-Parsing in Directive-Handlern | `msconnector_parse_bool` | ersetzt | On/off-Parsing ist Common-Parserverhalten. |
| Manuelles Phase-4-Parsing | `msconnector_parse_phase4_mode` | ersetzt | Vermeidet duplizierte minimal/safe/strict-Logik. |
| Manuelles Size-Parsing | `msconnector_parse_size` | ersetzt | Vermeidet duplizierte positive Dezimal-Size-Logik. |
| Manueller Directory-Config-Merge | `msconnector_config_merge` | ersetzt | Common merged semantische Konfigurationsfelder; Apache merged weiterhin libmodsecurity-Rulesets und APR-eigene Arrays. |
| Apache-`command_rec`-Directive-Tabelle | `msconnector/directives.h` plus `msconnector_directive_adapter_find` | als duenner Adapter behalten | `command_rec` ist Apache-API, waehrend Namen und Spec-Lookup aus Common kommen. |
| Apache-Request-Header-Schleifen | `msc_apache_map_request` mit `msconnector_request_mapper_contract` | als duenner Adapter behalten | Zugriff auf `request_rec` ist Apache-spezifisch; die Ausgabe wird gegen den Common-Mapper-Vertrag validiert. |
| Apache-Response-Header-Schleifen | `msc_apache_map_response` mit `msconnector_response_mapper_contract` | als duenner Adapter behalten | Response-Extraktion ist Apache-spezifisch; Response-Modell und Vertrag sind Common. |
| Response-Content-Type-Lookup aus `request_rec` | `msconnector_headers_*` fuer gemappte Modelle | wegen Apache-Spezifik behalten | Der vorhandene Live-Filter liest Apache-Response-Tabellen noch direkt; der Common-Mapper-Pfad steht zur Vertragsvalidierung bereit. |
| `apache_json_escape` | `msconnector_event_write_jsonl_line` / `msconnector_json_escape` | ersetzt | Event-JSON-Escaping und JSONL-Formatierung sind Common-Semantik. |
| `apache_phase4_rule_id` | `msconnector_rule_id_extract_from_message` | ersetzt | Rule-ID-Extraktion ist Common-Semantik. |
| Phase-4-Event-JSON-Stringformatierung | `msconnector_event` und `msconnector_event_write_jsonl_line` | ersetzt | Common besitzt die metadata-only Event-JSONL-Form; es wird kein Body-Payload geschrieben. |
| APR-Pools, Bucket Brigades, Filter, Hooks, APLOG, Return-Codes | keiner | behalten, weil Apache-spezifisch | Diese Host-Server-Integrationsprimitive duerfen nicht nach Common wandern. |
| libmodsecurity-`RulesSet`-Ladeaufrufe | `msconnector_rule_load_stats` | als duenner Adapter behalten | Native Rule-Loading ist Apache/libmodsecurity-Integration; Statistiken nutzen Common-Strukturen. |

## C-Standard-Smoke-Abdeckung

Die Compile-Kompatibilitaet der Apache/Common-Adoptionsschicht wird durch `ci/check-apache-c-standards.sh` und die Makefile-Targets `check-apache-c17`, `check-apache-c23`, `check-apache-future-c` und `check-apache-c-standards` geprueft.

- C17 ist verpflichtend und nutzt `-std=c17 -Wall -Wextra -Werror`.
- C23 und future-C sind optional und werden uebersprungen, wenn `ci/detect-c-standard.py` meldet, dass der Compiler den angeforderten Modus nicht unterstuetzt.
- Fehlende APXS- oder Apache/APR/libmodsecurity-Header werden als `BLOCKED` mit Exit-Code `77` gemeldet.

Das ist Compile-/Struktur-Evidence nur fuer die Apache/Common-Adoptionsschicht. Es ist keine Evidence fuer Produktion, CRS, Full-Matrix oder Runtime-Verifikation.

## Review-Folgefixes

- Der Apache-APXS-Buildpfad haengt jetzt die Common-SDK-Quellliste der Apache-Adoptionsschicht an, sodass nicht-inline `msconnector_*`-Aufrufe in das Modul gebaut werden.
- Der Directory-Merge priorisiert eine statische Child-`modsecurity_transaction_id` vor einem kompilierten Parent-`modsecurity_transaction_id_expr`.
- `make lint` nutzt `check-apache-c17-lint`, das Apache-C17-`BLOCKED`/Exit-77-Header-Discovery als Lint-Skip behandelt, waehrend `make check-apache-c17` der harte Compile-Check bleibt.
- Phase-4-Intervention-Events setzen einen nicht-OK Common-Status und erfassen Body-Truncation als Metadaten getrennt von JSON-Serialisierungstruncation.
- Der Apache-Response-Mapper enthaelt `err_headers_out`, `headers_out` und einen synthetischen `Content-Type` aus `request_rec.content_type`, nur wenn noch kein Content-Type-Header gemappt wurde.
