# Phase-1-Plan umgestalten

**Sprache:** [English](refactor-phase-1-plan.md) | Deutsch

Status: umgesetzt

Diese Phase beginnt mit einer konservativen gemeinsamen Basis, ohne Apache oder zu ändern
NGINX-Runtime-Connector-Code. Ziel ist es, sichere connectorneutrale Daten bereitzustellen
Formen sichtbar, während das bestehende Smokeverhalten in der realen Welt erhalten bleibt.

## Eingaben überprüft

– Apache-Connector-Quelle, jetzt unter dem Adapter-eigenen `connectors/apache/src/`
nach der Phase-11-Migration.
- NGINX-Upstream-Connector-Quelle unter `connectors/nginx/upstream/src/` am
Zeitpunkt der Phase 1. In Phase 9 wurden diese Dateien später in den Besitz des Adapters migriert
`connectors/nginx/src/` und Phase 10 entfernten den früheren NGINX `upstream/`
Der Referenzbaum nach dauerhafter Zuordnung blieb erhalten.
– Vorhandene gemeinsame C-First-Header unter `common/include/msconnector/`.
- Reale Smokegeschirre für Apache und NGINX.

## Sichere gemeinsame Stiftung

Die folgenden öffentlichen Bereiche sind in Phase 1 sicher, da sie nicht eingeschlossen sind
Server-SDK-Header, besitzen keine libmodsecurity-Objekte und verschieben keine Hooks oder
Filterlogik:

| Bereich | Entscheidung | Grund |
| --- | --- | --- |
| Fähigkeitsbeschreibungen | Behalten Sie das vorhandene `capabilities.h` als kanonisch bei | Bereits connectorneutral und C-kompatibel |
| Interventionsvertretung | Aufgeteilt in `intervention.h` | Sowohl Apache als auch NGINX nutzen libmodsecurity-Eingriffe, die Übersetzung bleibt jedoch konnektorspezifisch |
| Betriebsstatuswerte | Fügen Sie `status.h` hinzu | Wird für neutrales adapter/test-Statusvokabular ohne HTTP-Semantik benötigt |
| Ursprungsmetadaten | Fügen Sie `origin.h` hinzu | Erfasst provenance/version-Zeichenfolgen ohne Annahmen zum Quelleneigentum |
| Request/response-Metadaten | Behalten Sie vorhandene Header bei | Bereits neutral; Es wurden keine Eigentumsregeln geändert |
| Metadaten protokollieren | Vorhandenen Header beibehalten | Der vorhandene Logger-Typ ist nur für Rückrufe und connectorneutral |

## Kandidaten für später umgestalten

| Kandidat | Apache-Evidence | NGINX-Evidence | Entscheidung der Phase 1 |
| --- | --- | --- | --- |
| Regelsatz wird geladen | `msc_rules_add_file`, Remote-Regeln in der Apache-Konfiguration | Regeldateianweisungen in der NGINX-Konfiguration | Nur Dokument |
| Transaktionslebenszyklus | `create_tx_context`, Hook-Phasen, Filter | Requestskontext plus access/header/body/log-Handler | Nur Dokument |
| Umgang mit Interventionen | `process_intervention(Transaction *, request_rec *)` | `ngx_http_modsecurity_process_intervention(Transaction *, ngx_http_request_t *, ngx_int_t)` | Nur Daten darstellen; Verhalten nicht bewegen |
| Audit/logging | Apache error/log-Hooks | NGINX-Protokollrückruf und Protokollphase | Nur Dokument |
| Metadatenzuordnung anfordern | Apache-Requestsdatensätze und -tabellen | NGINX-Anfrage fields/chains | Nur Dokument |
| Zuordnung von Antwortmetadaten | Apache-Ausgabefilter | NGINX header/body-Filter | Nur Dokument |
| Fehlerbehandlung | Serverspezifische HTTP/finalize-Pfade | Serverspezifische return/finalize-Pfade | Nur allgemeines Statusvokabular |

## Nicht-Ziele

- Keine Änderungen bei der Apache-Hook-Registrierung.
- Keine Änderungen bei der Registrierung des NGINX-Moduls.
- Keine Änderungen an der Apache-Bucket-Brigade.
- Keine NGINX body/header-Filteränderungen.
- Keine serverspezifischen Änderungen beim Parsen der Konfiguration.
- Keine Abstraktion des libmodsecurity-Transaktionseigentums.
- Keine Werbung für die Blockierung von Response Bodyn; `RESPONSE_BODY` bleibt der ehemalige expected-failure/mapped-only.

## Akzeptanz für diese Phase

– Neue gemeinsame Header werden als eigenständige C-Header kompiliert.
– Apache- und NGINX-Quellimporte bleiben laufzeitäquivalent zum vorherigen Smoke
Zustand.
– Die vorhandenen Smoke-Ziele passieren weiterhin, bevor künftig Code extrahiert wird
wird versucht.
- Alle externen Referenz-Repositorys bleiben schreibgeschützt.
