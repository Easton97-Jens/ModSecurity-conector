# Adaptereigene Ebene

**Sprache:** [English](adapter-owned-layer.md) | Deutsch

Status: Phase 11 Apache- und NGINX-Quellmigration

Die Adapter-eigene Ebene ist der erste Repo-eigene Connector-Code, der sich daneben befindet
die importierten Upstream-Referenzbäume. Es handelt sich bewusst nicht um die Runtime des Produkts
Code noch nicht.

## Zweck

`connectors/<name>/` ist für Connector-eigenen Code reserviert, der außerhalb entwickelt wurde
importierte Upstream-Referenzbäume. Nach Phase 13 ist `src/` ein striktes Produkt
nur Quelle; Metadaten, Build-Dateien und Herkunftskarten befinden sich daneben im
Connector-Root:

- stabile Connector-Metadaten;
- Herkunfts- und Lizenzbeschreibungen;
- Debug-Kompatibilitäts-Shims;
- Zukünftige Adapter-lokale Helfer mit eindeutigem Smoke-Nachweis.

Für NGINX und Apache enthält dieser Layer nun auch das adaptereigene Modul
Build-Quelle unter Beibehaltung serverspezifischer Quellgrenzen.

Die Schicht ist von `common/` getrennt: Common bleibt connectorneutral, während
Adaptereigene Helfer können Apache oder NGINX als Komponenten benennen. Ersteres
Apache- und NGINX-Upstream-Bäume wurden entfernt. Die Herkunft des Apache bleibt erhalten
`licenses/apache/`, `connectors/apache/ORIGIN.md` und
`connectors/apache/SOURCE_MAP.json`; Die Herkunft von NGINX bleibt erhalten
`licenses/nginx/`, `connectors/nginx/ORIGIN.md` und
`connectors/nginx/SOURCE_MAP.json`.

## Aktuelle Dateien

| Weg | Rolle | Runtimenutzung |
| --- | --- | --- |
| `connectors/apache/metadata.h` | Metadaten-API des Apache-Adapters | Nicht mit Apache-Modul-Builds verknüpft |
| `connectors/apache/metadata.c` | Apache origin/source-Metadaten | Validiert durch `ci/check-adapter-helpers.sh` |
| `connectors/apache/autogen.sh`, `configure.ac`, `Makefile.am`, `build/*` | Adaptereigene Apache Autotools/APXS-Build-Eingaben | Materialisiert in `$BUILD_ROOT/apache-build/connector-src` für Monorepo-Standard-Apache-Builds |
| `connectors/apache/src/*.c`, `src/*.h` | Adaptereigene Apache-Modulquellen | Erstellt durch den generierten Apache-Connector-Quellbaum |
| `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/**/*.in`, `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/t/conf/extra.conf.in` | Apache-Konfigurationsvorlagen, die vom Upstream-Layout übernommen wurden | Aus Gründen der Autotools-Kompatibilität materialisiert |
| `connectors/apache/SOURCE_MAP.json` | Herkunftskarte der Apache-Basis | Wird von Materialized-Source-Manifesten verwendet. nicht kompiliert |
| `connectors/nginx/metadata.h` | Metadaten-API des NGINX-Adapters | Nicht mit NGINX-Modul-Builds verknüpft |
| `connectors/nginx/metadata.c` | NGINX origin/source-Metadaten | Validiert durch `ci/check-adapter-helpers.sh` |
| `connectors/nginx/src/ddebug.h` | NGINX-Debug-Kompatibilitätsheader | Überlagert in materialisierte NGINX-Build-Quellen; Wird bei Bedarf weiterhin als Ausweichquelle für externe Quellen verwendet |
| `connectors/nginx/config` | Build-Metadaten des dynamischen NGINX-Moduls | Materialisiert in `$BUILD_ROOT/nginx-build/connector-src/config` für Monorepo-Standard-NGINX-Builds |
| `connectors/nginx/src/ngx_http_modsecurity_*.c` | Adaptereigene NGINX-Modulquellen | Erstellt durch den generierten NGINX-Connector-Quellbaum |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | Adaptereigene NGINX-Connector-Deklarationen | Erstellt durch den generierten NGINX-Connector-Quellbaum |
| `connectors/nginx/SOURCE_MAP.json` | NGINX base/PR Herkunftskarte | Wird von Materialized-Source-Manifesten verwendet. nicht kompiliert |

## Grenzen

### Sicherer Adapter im Besitz

- Statische Connector-Metadaten;
- source/origin-Deskriptoren;
- Adapter-lokale Debug-Kompatibilität;
- Hilfscode, der nur durch Nicht-Produktvalidierungsprüfungen kompiliert wird.

### Mögliche zukünftige Gemeinsamkeit

- status/origin/intervention-Datenformen nach den Connector-spezifischen Feldern
getrennt von der Serveridentität;
- Fähigkeitsbenennung und zusammenfassende Metadaten;
- Stabile Audit-Schweregrad-Deskriptoren, nachdem das Audit-Verhalten flächendeckend nachgewiesen wurde
Anschlüsse.

### Connector-spezifisch für immer

- Apache-Hook-Registrierung und Bucket-Brigaden;
- NGINX-Modulregistrierung und Filterkettenintegration;
- Analyse der Serverkonfiguration und Besitz des Serverspeichers;
- Connector-spezifische request/response-Lebenszyklusentscheidungen.

### Nicht sicher für die Extraktion

- Requestskörper-Timing und Pufferung;
- Filterung des Reaktionskörpers und späte Interventionen;
- Besitz der libmodsecurity-Transaktion;
- Verhalten beim Abschluss der Intervention;
- Abwesenheitsverhalten im Audit-Protokoll, bis die umgebungsübergreifenden Evidence stabil sind.

## Validierung

Die Adapter-Metadaten-Helfer werden von `ci/check-adapter-helpers.sh` kompiliert
unter `$BUILD_ROOT/adapter-helper-smoke/`. Das Skript verknüpft die Metadatenquellen
mit dem Common `origin`-Helfer und stellt sicher, dass die stabilen Felder vorhanden sind.
Die erwarteten Werte werden von `modules/ModSecurity-test-Framework/ci/adapter_metadata.py` generiert, das analysiert
die Adapter-eigenen C-Metadaten ohne FFI.

`ci/check-adapter-metadata-drift.sh` vergleicht die analysierten Adaptermetadaten mit
die Connector-`ORIGIN.md`-Dateien, zentrale `licenses/`-Ursprungsdokumente und den Import
Dokumentation. Drift schlägt `make lint` fehl, bevor Metadaten automatisch gemeldet werden können
divergieren.

Es wird keine FFI-Brücke hinzugefügt und die Smokekanäle sind nicht auf diese Helfer angewiesen
Objekte. Für jede zukünftige Produktionsverwendung ist ein separater Schritt zum Ersetzen und Reduzieren erforderlich
mit before/after realer Connector smoked.

## Verwendung der Shadow Build-Quelle

Phase 8 beginnt mit der Verwendung von Adapter-eigenen Dateien in generierten Build-Quellen. Phase 9
Migriert das NGINX-Modul `config` und Quelldateien nach `connectors/nginx/src`.
Für die Monorepo-Standard-NGINX-Quelle wird `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh` materialisiert
`$BUILD_ROOT/nginx-build/connector-src` von der adaptereigenen NGINX-Quelle und
Nur generierte Manifeste. Die generierten Manifeste identifizieren das NGINX-Modul
Quellen als `adapter-owned` und PR #377-Patch-Herkunft aufzeichnen, wo
anwendbar.

Phase 11 migriert die Apache-Quelle und Autotools/APXS-Eingaben in die
Adaptereigener Apache-Baum. Phase 12 entfernt attribution/history/documentation-only
Dateien aus diesem Baum, nachdem der Autoconf-Quellanker dorthin verschoben wurde
`src/mod_security3.c`. Phase 13 flacht das Layout ab, sodass Autotools-Dateien dort gespeichert werden
`connectors/apache/`, produktive C-Dateien leben direkt in
`connectors/apache/src/` und beibehaltene Autotools-Vorlagen leben darunter
`modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`. Für die monorepo-default-Apache-Quelle:
`modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh` materialisiert
`$BUILD_ROOT/apache-build/connector-src` aus der Apache-Quelle im Besitz des Adapters und
Nur generierte Manifeste. Das generierte Manifest identifiziert das Apache-Modul
Quellen, Build-Eingaben und beibehaltene `.in`-Vorlagen als `adapter-owned`; dauerhaft
Die Apache-Zuordnung bleibt in `licenses/apache/`, `connectors/apache/ORIGIN.md`,
und `connectors/apache/SOURCE_MAP.json`.

Phase 13 verschiebt außerdem NGINX-Unterstützungsdateien aus `src/`: `config` lebt jetzt unter
`connectors/nginx/config`, während Metadaten und Herkunft unter leben
`connectors/nginx/metadata.*` und `connectors/nginx/SOURCE_MAP.json`.

## Meldepriorität

Die von Build- und Runtimezusammenfassungen verwendeten Ursprungsmetadaten folgen dieser Reihenfolge:

1. explizite `*_ORIGIN_*`- oder `CONNECTOR_ORIGIN_*`-Umgebungsüberschreibungen;
2. Quellmetadaten des externen Connectors von `git rev-parse` und `git describe`
wenn `MODSECURITY_APACHE_SOURCE_DIR` oder `MODSECURITY_NGINX_SOURCE_DIR` Punkte
außerhalb des Monorepo-Imports;
3. Adaptereigene Metadaten von `connectors/<name>/metadata.c` für
Standardquelle im Besitz des Monorepo-Adapters.

Hierbei handelt es sich lediglich um Berichtsmetadaten. Es verknüpft keine Adaptermetadaten mit Apache oder
NGINX-Module und hat keinen Einfluss auf Anfrage, Antwort, Text, Filter, Transaktion usw.
oder Interventionsverhalten.
