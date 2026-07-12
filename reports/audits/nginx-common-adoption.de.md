# NGINX Common SDK-Adoptionsbericht

**Sprache:** [English](nginx-common-adoption.md) | Deutsch

**Umfang:** Nur Compile-/Struktur-Evidence. Es wird keine Produktion, CRS, Full-Matrix oder Runtime-Verifikation beansprucht.

| Lokale NGINX-Funktion / lokales Feld | Common-Ersatz | Aktion | Grund |
| --- | --- | --- | --- |
| Transitionsflags `enable` / `use_error_log` | `msconnector_config.enable`, `msconnector_config.use_error_log`, `msconnector_parse_bool` | als duenner Adapter behalten | NGINX-Merge und `ngx_conf_set_flag_slot` brauchen native Ablage; Werte werden nach `common_config` synchronisiert. |
| Integer-Konstanten/Parser fuer `phase4_mode` | `msconnector_config.phase4_mode`, `msconnector_parse_phase4_mode` | ersetzt | Phase-4-Modussemantik ist connector-neutral. |
| Helper zur Phase-4-Content-Type-Validierung | `msconnector_validate_content_type_token` | ersetzt | Content-Type-Tokenvalidierung ist gemeinsame Semantik; NGINX behaelt Dateilesen und Allokation. |
| Config-Defaults/Merge/Validierung in `ngx_http_modsecurity_merge_conf` | `msconnector_config_init`, `msconnector_config_merge`, `msconnector_config_validate` | ersetzt | Defaults und Policy gehoeren Common. |
| `ngx_command_t`-Directive-Tabelle | Common-Directive-Makros/Specs/Adapter | als duenner Adapter behalten | Registrierung ist NGINX-API; Namen und Spec-Vertraege gehoeren Common. |
| Request-Header-Iteration ueber `ngx_list_t` und Request-Strings | `msconnector_request`, `msconnector_request_mapper_contract`, Common-Header-Helper | als duenner Adapter behalten | NGINX besitzt `ngx_list_t`; der Mapper wird im Access-Pfad ausgefuehrt, erzeugt ein Common-Request-Modell, NUL-terminiert Request-Stringfelder und validiert es. |
| Response-Header-Iteration ueber `ngx_list_t` plus Spezialheader | `msconnector_response`, `msconnector_response_mapper_contract` | als duenner Adapter behalten | NGINX besitzt Response-State; der Mapper laeuft in Header-/Body-Filterpfaden, erzeugt ein Common-Response-Modell, synthetisiert bei Bedarf Content-Type/Content-Length-Metadaten und validiert es. |
| Host-Fallback aus `r->headers_in.server` | `msconnector_headers_find_first` plus NGINX-spezifischer Fallback | als duenner Adapter behalten | NGINX mappt Host ueber Common-Header-Lookup und faellt danach auf NGINX-Request-Felder zurueck; `msconnector_headers_host` wird hier nicht als von NGINX adoptiert beansprucht. |
| Body-Payload-Mapping | Body-Metadaten des Common-Mapper-Vertrags | NGINX-spezifisch behalten | Der Mapper setzt Body-Groesse auf null, ausser NGINX besitzt sicher einen gepufferten Body; kein Payload-Logging. |
| Rule-Loading ueber libmodsecurity-Callbacks | Common-Rule-Load-Statistiken | als duenner Adapter behalten | libmodsecurity-Loading ist backend-spezifisch; Statistiken nutzen Common-Strukturen. |
| Build-Quellliste | Common-SDK-Objekte, inklusive `transaction_state.c` mit `event.c` | ersetzt | Der NGINX-Modulbuild enthaelt jetzt Common-Objekte fuer adoptierte Aufrufe und vermeidet unaufgeloestes `msconnector_phase_name`. |
| C-Standard-Checks | `ci/checks/connectors/nginx/check-nginx-c-standards.sh` | ersetzt | C17 ist hart, wenn Header vorhanden sind; C23/future-C sind optional und ueberspringen sauber. |
| Phase-4-Intervention-Logtext | metadata-only Redaction Summary plus Common-JSON-Escaping/Rule-ID-Extraktion | ersetzt | Rohmeldungen aus ModSecurity-Interventionen koennen Payload oder matched data enthalten; NGINX schreibt nur Praesenzmarker und Rule-Metadaten. |
| Phase-4-Content-Type-Dateiwildcards | NGINX-Exact-Match-Validierung nach Common-Tokenvalidierung | als duenner Adapter behalten | Der NGINX-Runtime-Scope matched exakt, daher werden Wildcards und fehlerhafte MIME-Eintraege beim Config-Load abgelehnt. |
| NGINX-Callback-Signaturen | explizite `(void)`-Annotationen fuer absichtlich ungenutzte Parameter | NGINX-spezifisch behalten | Die NGINX-Callback-ABI verlangt Parameter, die manche Callbacks nicht nutzen; Annotationen halten `-Wall -Wextra -Werror` sinnvoll, ohne Warnungen zu unterdruecken. |
| Fehler bei Phase-4-Rule-ID-Extraktion | nur positive Resultate aus `msconnector_rule_id_extract_from_message` verwenden | ersetzt | Fehlerhafte oder zu lange IDs werden nicht als Erfolg behandelt und der Extraktionspuffer wird vor Nutzung initialisiert. |
| Phase-4-Body-Limit-Directive | `MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT` und `msconnector_parse_size` | ersetzt | NGINX registriert die Common-bekannte Directive, mappt sie nach `common_config.phase4_body_limit`, zaehlt alle gesehenen Bytes getrennt von inspizierten Bytes und gibt nach dem Limit keine weiteren Bytes an ModSecurity weiter, waehrend Truncation-Metadaten gesetzt werden. |
| Apache-artige Transaction-ID-Expression-Directive | `MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR` | nicht anwendbar | NGINX registriert keine Apache-Expression-Syntax; `modsecurity_transaction_id` bleibt die NGINX-Complex-Value-Directive. |
