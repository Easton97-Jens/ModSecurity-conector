# Gemeinsamer Extraktionsplan

**Sprache:** [English](common-extraction-plan.md) | Deutsch

Status: umgesetzt

Die Apache- und NGINX-Connector-Quellen werden als separater Upstream-Code importiert
Bäume zuerst. Phase 1 schafft nur ein kleines connectorneutrales gemeinsames Fundament;
Das Verhalten von Apache oder NGINX hook/filter wird dadurch nicht verschoben.

## Repository-Rollen

| Bereich | Rolle | Langfristige Ausrichtung |
| --- | --- | --- |
| `connectors/apache/src/` | Adaptereigene Apache-Quelle, abgeleitet von https://github.com/owasp-modsecurity/ModSecurity-apache | Connectorspezifisch bleiben; Nur mit dediziertem Apache-Adapter-Proof reduzieren |
| ehemals `connectors/apache/upstream/` | Apache reference/import-Basis aus https://github.com/owasp-modsecurity/ModSecurity-apache entfernt | In Phase 11 entfernt, nachdem die Quelle auf `connectors/apache/src` migriert und die dauerhafte Zuordnung auf `licenses/apache/` verschoben wurde |
| `connectors/nginx/src/` | Adaptereigene NGINX-Modulquelle, abgeleitet von https://github.com/owasp-modsecurity/ModSecurity-nginx | Connectorspezifisch bleiben; Nur mit dediziertem NGINX-Adapternachweis reduzieren |
| ehemals `connectors/nginx/upstream/` | NGINX reference/import-Basis aus https://github.com/owasp-modsecurity/ModSecurity-nginx entfernt | In Phase 10 entfernt, nachdem die Quelle auf `connectors/nginx/src` migriert und die dauerhafte Zuordnung auf `licenses/nginx/` verschoben wurde |
| `licenses/` | Dauerhafte Lizenz- und Herkunftsnennung | Bewahren Sie den importierten Code oder die aus der Quelle abgeleiteten Evidence auf |
| `common/` | Connector-neutrale C-First-Typen und zukünftige gemeinsame Helfer | Wachsen Sie nur nach evidenzbasierter Extraktion |
| `connectors/<name>/` | Serverspezifischer Build-, Lebenszyklus-, Harness- und Integrationscode | Halten Sie Hooks, Filter und Konfigurationsanalysen konnektorspezifisch |

## Extraktionsregel

Ein Kandidat darf erst dann zu `common/` wechseln, wenn alle folgenden Bedingungen zutreffen:

- das Verhalten ist connectorneutral;
- Die realen Smoketests von Apache und NGINX bestehen nach der Extraktion immer noch;
– Die extrahierte Schnittstelle enthält keine Apache- oder NGINX-Header, -Typen oder
Lebenszyklusannahmen;
- Herkunfts- und Kompatibilitätshinweise wurden aktualisiert.

## Kandidatenbereiche

| Bereich | Begründung des Kandidaten | Aktuelle Entscheidung |
| --- | --- | --- |
| Fähigkeitsbeschreibungen | Connectors kündigen unterstützte Lebenszyklusartefakte an | Das vorhandene `capabilities.h` bleibt kanonisch |
| Vokabular zum Betriebsstatus | Build/test-Adapter benötigen connectorneutrale Ergebnisse | Fügen Sie nur allgemeine Statuswerte hinzu |
| Ursprungsmetadaten | Importierte Connectors benötigen stabile Herkunftsmetadaten | Nur gemeinsame Ursprungsdatenform hinzufügen |
| Interventionsdatenform | Beide Connectoren übersetzen libmodsecurity-Eingriffe in HTTP-Antworten | Nur neutrale Vertretung hinzufügen; Halten Sie die Übersetzung Connector-spezifisch |
| Regelsatz wird geladen | Beide Connectors laden ModSecurity-Regeln und -Dateien | Nur Dokument |
| Transaktionslebenszyklus | Beide erstellen und steuern libmodsecurity-Transaktionen | Nur Dokument |
| Audit/logging | Beide verbinden die libmodsecurity-Protokollierung mit Serverartefakten | Nur Dokument |
| Metadatenzuordnung anfordern | Sowohl Kartenmethode als auch URI, Header, Text und Verbindungsdaten | Behalten Sie die bestehende neutrale Anfrageform bei; Keine Adapterentnahme |
| Zuordnung von Antwortmetadaten | Beide ordnen die Antwort headers/body über Serverfilter zu | Behalten Sie die bestehende neutrale Antwortform bei; Keine Adapterentnahme |
| Konfigurationsmodell | Beide verfügen über eine Connector-Konfiguration im enable/rules-file-Stil | Connectorspezifisch bleiben |
| Fehlerbehandlung | Beide benötigen ein konsistentes blocked/fail-Reporting in Tests | Nur für Testkabel mit allgemeinem Code geeignet |

## Derzeit keine Kandidaten

- Apache-Hook-Registrierung und Filter.
- NGINX-Phasenhandler und Filterreihenfolge.
- APXS/Autotools-Integration.
- Dynamische Modulintegration NGINX `config`.
- Serverspezifisches Konfigurations-Parsing.
- Lebensdauer oder Besitz der libmodsecurity-Transaktion.
- Jede `RESPONSE_BODY`-Blockierungslogik, bis sie sich für beide als stabil erwiesen hat
Anschlüsse.

## Gemeinsame Basis der Phase 1

Phase 1 darf nur connectorneutrale C-First-Stiftleisten hinzufügen oder aktualisieren
`common/include/msconnector/`:

- Statuswerte für häufige adapter/test-Ergebnisse;
- Interventionsdatendarstellung ohne serverspezifische Antwortbehandlung;
- origin/provenance-Metadaten;
- Dünne C++-Alias-Wrapper, die dem vorhandenen gemeinsamen Header-Muster entsprechen.

Diese Dateien dürfen keine Apache-, NGINX- oder andere server/proxy-Header enthalten. Sie
Außerdem darf das Eigentum an `ModSecurity`, `RulesSet`, `Transaction` oder nicht verborgen bleiben
`ModSecurityIntervention`-Objekte von libmodsecurity.

## Gemeinsame Runtimegrenze der Phase 3

In Phase 3 werden kleine C-Implementierungsdateien unter `common/src/` für den Status hinzugefügt.
Nur Ursprungs-, Interventions- und Fähigkeitsmetadaten. Der Apache und NGINX
Runtimekabelbäume verwenden weiterhin Python/Shell und spiegeln das Schema ohne
FFI.

## Phase 4 Ersetzen-und-Reduzieren-Grenze

Phase 4 ersetzt einen NGINX-Adapter-nahen Debug-Kompatibilitätsheader. Das ist nicht der Fall
a Gemeinsame Extraktion: Der Ersatz lebt unter `connectors/nginx/src/` und ist
nur in generierte Build-Bäume kopiert, die `src/ddebug.h` benötigen.

Kein Apache- oder NGINX-Hook, Filter, Body-Handling, Transaktionseigentum,
Konfigurationsanalyse oder `RESPONSE_BODY`-Verhalten wird zu `common/` verschoben.

Nachdem diese Grenze stabil ist, überprüfen Sie die doppelte Nutzung der libmodsecurity-API und
Entwerfen Sie einen separaten Vorschlag für einen connectorneutralen Adapter. Dieser Vorschlag muss Folgendes enthalten:
before/after Smoke entsteht und darf nicht von der Blockierung des Response Bodys ausgehen
Verhalten, während es das ehemalige expected-failure/mapped-only. bleibt

## Phase 9 NGINX-Quelleigentumsgrenze

Phase 9 migriert NGINX `config` und Modulquelldateien nach
`connectors/nginx/src/` und erstellt den Monorepo-Standard-NGINX-Smoke aus dem
materialisierter, dem Adapter gehörender Quellbaum. Dies ist keine Common-Extraktion.
NGINX-Phasenhandler, Filter, Konfigurationsanalyse, Transaktionseigentum und
Das Verhalten in Phase 4 bleibt NGINX-spezifisch.
