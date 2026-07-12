# Gemeinsame Runtimegrenzen

**Sprache:** [English](common-runtime-boundaries.md) | Deutsch

Status: umgesetzt

Phase 3 fügt die ersten echten Common-C-Implementierungsdateien hinzu, allerdings nur für
Connector-neutrale Metadaten-Helfer.

## Was Common jetzt enthält

`common/src/` enthält kleine Helfer für:

- `msconnector_status`: C-Namenskonvertierung und Runtime-Ergebnis-Zuordnung.
- `msconnector_intervention`: Bau- und Störzustandsprüfungen.
- `msconnector_origin`: Ursprungskonstruktion und Prüfung auf leeren Ursprung.
- `msconnector_capabilities`: Benennung und Zusammensetzung der Fähigkeitsflags.

Diese Helfer hängen nur von der C-Standardbibliothek ab und
`common/include/msconnector/*`.

## Beziehung nutzen

Die Apache/NGINX Smoke Runner laden diese Helfer nicht über FFI. Python
verwendet `modules/ModSecurity-test-Framework/tests/runners/msconnector_models.py` als schemakompatiblen Spiegel für
dieselben Status-, Ursprungs-, Interventions- und Fähigkeitsnamen.

Das bedeutet:

- Connector Smokes behalten ihr bestehendes Python/Shell-Ausführungsmodell;
- Gängige C-Helfer werden unabhängig von `ci/checks/common/check-common-helpers.sh` validiert;
- Zusammenfassung JSON bleibt abwärtskompatibel und nur anfügbar.

## Explizite Nicht-Grenzen

Common besitzt nicht:

- Apache-Hook-Registrierung oder Bucket-Brigaden;
- NGINX-Modulregistrierung, Phasenhandler oder Filter;
- Handhabung des Requests- oder Response Bodyes;
- libmodsecurity-Objektbesitz oder Transaktionslebensdauer;
- `RESPONSE_BODY`-Verhalten.

Für jede künftige Gewinnung, die diese Bereiche betrifft, sind gesonderte Evidence erforderlich
vorbeiziehende reale Verbindungsrauche.

## Phase 5 Grenze zum Ersetzen und Reduzieren

In Phase 5 wurde die nächste mögliche Upstream-Reduzierung überprüft und kein Code erstellt
Ersatz. Die restlichen Hilfsfunktionen sind noch drin
Connector-eigene Runtimebereiche:

– Der Code des Apache-Dienstprogramms enthält das Ausgabeverhalten von bucket/error.
– Die NGINX-String-Konvertierung wird von der Konfigurationsanalyse und Requestsmetadaten verwendet.
– NGINX PCRE-Zuweisungshelfer sind Teil des config/rules-Lebenszyklus.
– NGINX-Antwortheader-Helfer und Protokollrückrufe sind filter/audit-Pfade.

Common darf weiterhin neutrale Metadatenformen definieren, darf es aber nicht absorbieren
Diese Pfade, bis ein Anschlussadapter das Verhalten und den Smoke in der realen Welt besitzt
Die Ergebnisse Evidencen die Kompatibilität.

## Adaptereigene Grenze der Phase 6

Phase 6 fügt die ersten Adapter-eigenen Metadatenskelette hinzu
`connectors/apache/` und `connectors/nginx/`. Diese Dateien gehören nicht zur Common Runtime
Code und sind nicht in die produktiven Apache- oder NGINX-Module eingebunden.

Die Adapter-eigenen Metadaten-Helfer:

- Stabile Connector-source/origin-Felder in einem `msconnector_origin` verfügbar machen
kompatible Form;
- keine Apache- oder NGINX-Server-Header enthalten;
- keine libmodsecurity-Interna enthalten;
- keine Anfrage, Antwort, Text, Filter, Intervention oder Transaktion enthalten
Lebenszyklusverhalten;
- werden nur von `ci/checks/common/check-adapter-helpers.sh` unter `$BUILD_ROOT` validiert.

In späteren Phasen wurden produktive Connector-Build-Eingaben in den Besitz des Adapters verschoben
Connector-Bäume: NGINX in Phase 9/10 und Apache in Phase 11. Phase 13 dann
hält `src/` auf die produktive Quelle beschränkt, mit metadata/provenance an der
Connector-Root. Das macht diese Quellen jedoch nicht zu Gemeinbesitz. Haken, Filter,
Bucket-Brigaden, Konfigurationsanalyse, request/response-Mapping, Intervention
Die Finalisierung und das `RESPONSE_BODY`-Verhalten bleiben konnektorspezifisch.

Dies schafft einen Platz für zukünftige Ersetzungen im Besitz des Adapters, ohne dass dieser geändert werden muss
aktueller realer Verbindungspfad. Für jede Produktionsverwendung ist weiterhin eine separate Verwendung erforderlich
Ersetzen-und-Reduzieren-Phase und vorbeiziehender before/after-Smoke.

## Phase 7 Reporting-Integration

In Phase 7 können Adapter-eigene Metadaten als Feed für Build- und Runtimezusammenfassungen verwendet werden. Der
Smoke-Skripte lesen die Metadaten über `modules/ModSecurity-test-Framework/ci/lib/adapter_metadata.py`, einen lokalen Parser
ohne FFI- oder C-Runtimeabhängigkeit. Die Meldereihenfolge ist explizit festgelegt
Override, Git-Metadaten der externen Quelle, dann Adapter-eigene Monorepo-Metadaten.

Der Zusammenfassungs-JSON erhält `origin.source_url` nur durch Anhängen. Vorhandener Ergebnisstatus,
Fallerkennung, `verified_variables`, YAML-Semantik und `RESPONSE_BODY`
Die Klassifizierung bleibt unverändert.

## Phase 8 Shadow Build-Grenze

In Phase 8 kann NGINX aus einem unten generierten Connector-Quellbaum erstellen
`$BUILD_ROOT`. Zu diesem Zeitpunkt wurde der Baum aus importierten Quellen zusammengebaut
Dateien sowie Adapter-eigene Overlays und enthaltene lokale Manifeste. Das hat sich geändert
Nur der Build-Eingabespeicherort für die monorepo-default-NGINX-Quelle.

Der generierte Baum erstellt keinen gemeinsamen Besitz von NGINX-Filtern, Anfrage
Mapping, Körperhandhabung, Transaktionslebenszyklus oder Interventionsverhalten. Apache
erhält den gleichen generierten Quellnachweis, sein Modulaufbau bleibt jedoch auf dem
vorhandene bereinigte Upstream-Kopie in dieser Phase.

## Phase 9 NGINX-Adaptereigene Quellgrenze

Phase 9 verschiebt produktive NGINX-Quelldateien nach `connectors/nginx/src` und
Erstellt das Monorepo-Standard-NGINX-Modul aus dem Generierten
`$BUILD_ROOT/nginx-build/connector-src`-Baum. Dies ist eine Quelle im Besitz des Adapters
Eigentum, nicht Common Runtime Ownership.

Common besitzt immer noch nicht:

- Registrierung des NGINX-Moduls;
- NGINX-Zugriffs-, Header-, Text- oder Protokollfilter;
- Spätinterventionsverhalten der Phase 4;
- Response Body-Blockierungssemantik;
- Lebensdauer der libmodsecurity-Transaktion.

Quelländerungen von ModSecurity-nginx PR #377 werden als adaptereigenes NGINX dokumentiert
Herkunft der Quelle. Sie machen `RESPONSE_BODY` nicht zu einer verifizierten Variablen, und das tun sie auch
hat keinen Einfluss auf Apache.

## Phase 10 NGINX Upstream-Entfernungsgrenze

Phase 10 entfernt den verbleibenden NGINX-Upstream-Referenzbaum erst nach dem
Die Build-Eingabe wurde bereits in die Quelle im Besitz des Adapters verschoben. Dadurch ändert sich das Repository
Layout- und Attributspeicherung, keine Runtimesemantik. NGINX-Hooks, Filter,
Phasenhandler, Körperhandhabung, Interventionsverhalten und Transaktionseigentum
Es bleibt Connector-spezifischer Adapter-eigener Code, und Common besitzt immer noch keinen Code
diese Wege.

## Phase 11 Apache-Adaptereigene Quellgrenze

Phase 11 verschiebt die Apache-Produktivquelle und Autotools/APXS-Build-Eingaben in
`connectors/apache/src` und erstellt daraus das monorepo-default-Apache-Modul
`$BUILD_ROOT/apache-build/connector-src`. Dies ist eine Quelle im Besitz des Adapters
Eigentum, nicht Common Runtime Ownership.

Common besitzt immer noch nicht:

- Apache-Hook-Registrierung;
- Apache input/output-Filter;
- Bucket brigade/error-Reaktionshelfer;
- Analyse der Apache-Konfiguration;
- Abschluss der Intervention;
- Lebensdauer der libmodsecurity-Transaktion;
- `RESPONSE_BODY`-Verhalten.
