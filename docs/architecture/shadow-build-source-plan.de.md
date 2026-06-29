# Shadow Build-Quellplan

**Sprache:** [English](shadow-build-source-plan.md) | Deutsch

Status: Phase 11-Implementierung im Besitz des Apache- und NGINX-Adapters

Der Connector-Build behandelt `connectors/*/upstream/` nicht mehr als direkt
Build-Eingabe. Die ehemals importierten Oberlaufbäume wurden durch ersetzt
Adaptereigene Quellbäume plus dauerhafte Zuordnung unter `licenses/` und die
Build Harness generiert Einweg-Connector-Quellbäume unter `$BUILD_ROOT`.

## Ziel

Generierte Build-Quellen leben außerhalb des Checkouts:

- `$BUILD_ROOT/apache-build/connector-src/`
- `$BUILD_ROOT/nginx-build/connector-src/`

Jeder generierte Baum ist verfügbar. Es zeichnet Repo-eigene Adapterdateien auf und
generierte Overlays; Explizite externe Quellbuilds bleiben durch ihre dokumentiert
bereinigte Build-Kopien. Dadurch bleibt die Namensnennung sichtbar und ermöglicht eine spätere Zuordnung
Ersetzen-und-Reduzieren-Phasen zur Verkleinerung der Adapter-eigenen Quelle nur dann, wenn Smoke nachweist
die Veränderung.

## Quellpriorität

Für Monorepo-Standard-Connector-Quellen verwendet der materialisierte Baum diese Reihenfolge:

1. Kopieren Sie die Build-Dateien im Besitz des Adapters von `connectors/<name>/` gemäß
Connector `SOURCE_MAP.json`;
2. Generierte Manifeste schreiben.

Explizite externe Connector-Quellen lehnen die Materialisierung weiterhin ab. Wann
`MODSECURITY_APACHE_SOURCE_DIR` oder `MODSECURITY_NGINX_SOURCE_DIR` zeigt nach außen
Bei der Monorepo-Standardeinstellung verwenden die Vorbereitungsskripte weiterhin die externen bereinigten Dateien
Pfad kopieren.

## Namensnennung

Jeder materialisierte Baum enthält:

- `MATERIALIZED_SOURCE.md`
- `materialized-source.json`

In den Manifesten werden die endgültigen Dateien, der Ursprungspfad, die Quellart, die Lizenz und die beobachteten Dateien aufgelistet
commit/version und Grund. Sie werden unter `$BUILD_ROOT` generiert und sind es nicht
engagiert.

## Phase-8-Entscheidung

NGINX wird zuerst umgeschaltet. Der bisherige risikoarme `ddebug.h`-Ersatz ist bereits verfügbar
Es gehört dem Adapter und das NGINX-Modul `config` listet die Build-Eingaben explizit auf.
Der Standard-NGINX-Build verwendet jetzt `$BUILD_ROOT/nginx-build/connector-src`.

Apache wird zu Evidencezwecken erst in Phase 8 materialisiert. Der Apache Autotools-Build
Verwendet in dieser Phase immer noch die vorhandene bereinigte Upstream-Kopie, da die
Der generierte Quellbaum wurde noch nicht als Standard-APXS/Autotools nachgewiesen
Eingang.

## Phase 9 NGINX-Migration

Die produktive NGINX-Quelle gehört jetzt dem Adapter. Der Monorepo-Standard
`MODSECURITY_NGINX_SOURCE_DIR` ist `connectors/nginx` und
`modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh` materialisiert `$BUILD_ROOT/nginx-build/connector-src`
von Adapter-eigenen NGINX `connectors/nginx/config` und Modulquellen in
`connectors/nginx/src` sowie generierte Materialisierungsmanifeste.

Der Materializer ordnet NGINX `connectors/nginx/config` dem Root-`config` zu
die generierte Connector-Quelle. Produktive source/header-Dateien bleiben unter
`src/`; Support-Metadaten im Connector-Stammverzeichnis werden nicht materialisiert. Der
Das generierte JSON-Manifest zeichnet die PR #377-Patch-Herkunft für die Phase-4-Dateien auf
das diese Änderungen erhalten hat.

Der ehemalige `connectors/nginx/upstream/`-Baum ist nicht mehr der produktive NGINX
Modulquellbaum.

## Phase 10 NGINX Upstream-Entfernung

Phase 10 entfernt den verbleibenden NGINX-Upstream-Referenzbaum vollständig. Dauerhaft
Die Zuordnung bleibt in `licenses/nginx/`, `connectors/nginx/ORIGIN.md` und
`connectors/nginx/SOURCE_MAP.json`. Das NGINX-Materialized-Source-Manifest
sollte nur die Einträge `adapter-owned` und `generated-overlay` anzeigen.

`modules/ModSecurity-test-Framework/ci/run-nginx-smoke.sh` behandelt einen vorhandenen Monorepo-Standard-NGINX-Build als
veraltet, wenn `$BUILD_ROOT/nginx-build/connector-src/materialized-source.json` ist
fehlt, verweist immer noch auf `upstream-derived`-Einträge oder markiert den NGINX nicht
Modul `config` und C-Quellen als `adapter-owned`. In diesem Fall wird nur aktualisiert
die generierten NGINX build/runtime-Verzeichnisse unter `$BUILD_ROOT` vor der Ausführung
smoked, sodass alte Module die Quellenvalidierung im Besitz des Adapters nicht maskieren oder unterbrechen können.

## Phase 11 Apache-Migration

Die produktive Apache-Quelle gehört jetzt dem Adapter. Der Monorepo-Standard
`MODSECURITY_APACHE_SOURCE_DIR` ist `connectors/apache` und
`modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh` materialisiert
`$BUILD_ROOT/apache-build/connector-src` aus der Apache-Quelle im Besitz des Adapters,
Autotools/APXS-Eingaben, erforderliche `.in`-Vorlagen und generierte Manifeste. Der
Materializer behält die Apache-Pfade unverändert bei, also `./autogen.sh`, `./configure` und
`make` wird aus dem generierten Connector-Source-Root ausgeführt.

Der frühere `connectors/apache/upstream/`-Baum wurde entfernt, nachdem
`REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-apache-final-build make
smoke-apache` bestanden hatte. `modules/ModSecurity-test-Framework/ci/run-apache-smoke.sh` behandelt ein vorhandenes
monorepo-default Apache-Build als veraltet, wenn das Materialized-Source-Manifest vorhanden ist
fehlt, verweist weiterhin auf `upstream-derived`-Einträge oder markiert nicht erforderlich
Apache build/source/template-Dateien als `adapter-owned`.

## Phase 13 Layout-Vereinfachung

In Phase 13 bleiben die generierten Connector-Build-Layouts während der Erstellung unverändert
Repository-Layout strenger. NGINX `config` wohnt bei `connectors/nginx/config`
und materialisiert sich als Root `config`; NGINX `src/` enthält nur produktive Module
headers/sources. Apache Autotools/APXS-Dateien live unter `connectors/apache/`,
Produktive C-Dateien werden direkt unter `connectors/apache/src/` gespeichert und beibehalten
Autotools-Vorlagen leben während der Materialisierung unter `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`
zurück zu den von `configure.ac` erwarteten Pfaden `t/` und `tests/`.

## Nicht-Ziele

Diese Phase ändert sich nicht:

- Apache-Hooks oder NGINX-Filter;
- Anfrage, Antwort, Text, Transaktion, Intervention oder `RESPONSE_BODY`
Verhalten;
- YAML-Fälle oder `verified_variables`;
- Adaptereigene Apache- oder NGINX-Quellsemantik.

Für NGINX ändert Phase 9 den Build-Input-Eigentum, nicht jedoch die Smoke-Semantik
oder verifiziertes Variablenmodell. `RESPONSE_BODY` bleibt der ehemalige expected-failure/mapped-only.
