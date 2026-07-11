# NGINX-Connector

**Sprache:** [English](README.md) | Deutsch

Status: Common-SDK-Adoption, Compile-/Structure-Evidence.

Der NGINX-Connector behält NGINX-eigene Integrationspunkte (`ngx_command_t`,
`ngx_http_request_t`, `ngx_chain_t`, `ngx_buf_t`, Filter, Pools, Return-Codes
und Build-Glue). Semantik für Config, Direktiven, Mapper-Verträge, Events und
Limits wird über `common/` angebunden, soweit diese Adoption implementiert ist.

Die C17-Prüfung ist hart, benötigt aber lokale NGINX- und libmodsecurity-Header;
fehlen diese Header, meldet der Check `BLOCKED` mit Exit 77. C23/future-C sind
optionale Compiler-Smokes. Diese Checks sind keine Production-, CRS-,
Full-Matrix- oder Runtime-Verifikation.

NGINX-Common-SDK-Modul-Builds mit kopiertem Connector-Quellbaum müssen `MSCONNECTOR_COMMON_SRC` (oder `CONNECTOR_COMMON_SRC` / `COMMON_SRC_ROOT`) auf den Common-Source-Root des Repositories setzen; `MSCONNECTOR_COMMON_INC` bleibt der Common-Include-Root. Ohne diese Variable wird nur auf `$ngx_addon_dir/../../common/src` zurückgefallen, wenn dieser Pfad existiert.


NGINX registriert `modsecurity_transaction_id` für NGINX-Variablen/Complex-Values, aber nicht die Apache-Ausdrucksdirektive `modsecurity_transaction_id_expr`. `modsecurity_phase4_body_limit` ist ein begrenzender Phase-4-Inspektionswert; überschrittene Bytes werden nicht an ModSecurity übergeben und nur als Metadaten markiert.

## Kanonische Grenze für Phase 4

NGINX verwendet einen begrenzten nativen Response-Body-Filter. Sein Vorhanden-
sein beweist weder eine echte Phase-4-Regelauswertung noch einen zum Zeitpunkt
der Intervention noch änderbaren Antwortstatus. Deshalb stehen
`phase4_pre_commit_deny` auf `not_implemented`: Die native Phase-4-
Entscheidung fällt im Body-Filter nach dem Response-Header-Pfad.
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`late_intervention`, `late_intervention_log_only`, `late_intervention_abort`
und `late_intervention_status_metadata` bleiben `implemented_not_asserted`,
bis ein aktueller kanonischer Lauf über den echten Host das jeweilige Verhalten
belegt.

Ein Regeltreffer wird getrennt von einem sichtbaren 403 gemeldet. Kanonische
Ereignisse bewahren den ursprünglichen Host-Status, angeforderten WAF-Status,
sichtbaren Client-Status, angeforderte und tatsächliche Aktion sowie Header-
und Commit-Zeitpunkt und das Abbruchergebnis. Für eine Sperre vor dem Commit
gibt es in diesem NGINX-Body-Filter-Pfad keinen Anspruch. Nach dem Commit ist
das sichere Ergebnis `log_only` bei unverändertem sichtbaren Status; das
strikte Ergebnis ist `abort_connection` bei bereits sichtbarem Status und
bestätigtem Verbindungsabbruch. Keines davon ist ein umbenannter erfolgreicher
403-Fall.

Die kanonischen Phase-4-Fälle für Regelbeobachtung, Sperre vor dem Commit,
sicheres Protokollieren, strikten Abbruch und Status-/Aktionsmetadaten bleiben
nachweisgebunden. Weder Ereignisse noch Berichte enthalten Response-Body-
Payloads.
