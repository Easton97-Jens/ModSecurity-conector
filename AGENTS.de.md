# Repository-Richtlinien

**Sprache:** [English](AGENTS.md) | Deutsch

## Projektstruktur und Modulorganisation

Dies ist ein ModSecurity-Connector-Monorepo. Gemeinsam genutzte connector-neutrale C/C++-Schnittstellen leben in `common/include/msconnector/`, mit Helfern in `common/src/`. Adaptereigener Code befindet sich unter `connectors/`: Aktive Apache-, NGINX- und HAProxy-Quellen verwenden `connectors/<name>/src/`, `harness/`, `docs/` und Metadatendateien. Daneben wohnen zukünftige Verbindungsgerüste. Das wiederverwendbare Testframework ist das Submodul unter `modules/ModSecurity-test-Framework`; Die generierten Beweise und Matrizen finden Sie unter `reports/testing/generated/`. CI-Tools befinden sich in `ci/` und Beispielserverkonfigurationen befinden sich in `examples/`.

## Build-, Test- und Entwicklungsbefehle

- `git submodule update --init --recursive`: Rufen Sie das erforderliche Test-Framework ab.
- `make setup-dev`: Python-Tools aus dem Framework booten und nächste Schritte drucken.
- `make lint`: Ausführen von Shell-/Python-Syntaxprüfungen, Fixture-Validierung, Berichts-Governance, JSON-/Dokumentprüfungen und `git diff --check`.
- `make generate-test-matrix` / `make check-test-matrix`: Generierte Abdeckungs- und Laufzeitmatrixdokumente aktualisieren und überprüfen.
- `make quick-check` oder `make codex-check`: Leichte Validierung, geeignet vor Commits.
- `make smoke-apache`, `make smoke-nginx`, `make smoke-haproxy` oder `make smoke-all`: Runtime Smokes des Connectors ausführen. Verwenden Sie `make test-no-crs` und `make test-with-crs` für breitere CRS-Varianten.

## Codierungsstil und Namenskonventionen

Passen Sie den lokalen Dateistil an. Gemeinsam genutzte C-Helfer verwenden 4-Leerzeichen-Einrückungen, `msconnector_*`-Symbole und connector-neutrale Header. Apache-Code verwendet `msc_*`-Namen; NGINX-Code verwendet `ngx_http_modsecurity_*`; HAProxy-Code verwendet `haproxy_*`-Namen. Halten Sie `common/` frei von Connector-spezifischen Begriffen und Server-APIs. Shell-Skripte sollten POSIX `sh` sein, wo sich vorhandene Skripte befinden, mit `set -eu`; Python sollte `pathlib` und strukturiertes Parsen bevorzugen.

## Testrichtlinien

Tests und Vorrichtungen sind in erster Linie Eigentum von `modules/ModSecurity-test-Framework/tests/`. Fügen Sie die Abdeckung des Connector-Verhaltens dort oder in Connector-Kabelbäumen hinzu, nicht in Ad-hoc-Stammtestverzeichnissen. Wenn Sie generierte Berichte ändern, führen Sie `make generate-test-matrix` und `make check-test-matrix` aus. Notieren Sie für das Laufzeitverhalten den genauen Befehl und die Connector-/CRS-/MRTS-Variante.

## Commit- und Pull-Request-Richtlinien

Aktuelle Commits verwenden kurze, kleingeschriebene, zwingende Zusammenfassungen wie `refresh verified matrix after fixture input fixes`; Es ist kein konventionelles Commit-Präfix erforderlich. Konzentrieren Sie sich auf Commits und fügen Sie generierte Beweise in den Code ein, der dies erfordert. Pull-Anfragen sollten den betroffenen Connector oder Berichtsbereich beschreiben, Validierungsbefehle auflisten, Probleme verknüpfen und neu generierte Dateien unter `reports/testing/generated/` aufrufen.

## Sicherheits- und Konfigurationstipps

Behalten Sie die Laufzeit bei und erstellen Sie Artefakte außerhalb des Checkouts. Das Makefile leitet einen aufruflokal verifizierten Stamm vom CI oder dem temporären übergeordneten Laufzeitobjekt ab. Übertragen Sie keine heruntergeladenen Upstream-Quellbäume, Geheimnisse, lokalen Protokolle oder ungeprüften generierten Artefakte. Behalten Sie angeheftete Upstream-Referenzen und Lizenz-/Ursprungsmetadaten bei, wenn Sie Connector-Importe berühren.

## Dokumentationspflege

Repository-eigene Leser-Dokumentation bleibt als English-/German-Paar mit
genau einer H1 und direkt darunter liegendem Sprachumschalter erhalten. Die
kanonischen Root-Themen sind `docs/architecture.*`,
`docs/configuration.*`, `docs/testing-and-evidence.*`,
`docs/operations-and-security.*` sowie Connector-Index/-Guides unter
`docs/connectors/`; vollständige Hostdirektiven-Syntax bleibt in der
zugehörigen `examples/<connector>/`-Konfigurationsreferenz.

Variablen und ausführbare Platzhalter nahe ihrer ersten Verwendung erklären
und dann auf `docs/reference/variables.*` verlinken. Werte, Pfade, Targets,
IDs, Statusbegriffe und Integrationsmodusnamen bleiben in beiden Sprachen
identisch. Beispiele als Beispiele statt Defaults kennzeichnen,
entwicklerspezifische Pfade und Secrets vermeiden und Build-/Konfigurations-
Checks von Hostverkehr und Evidence unterscheiden.

Generiertes Markdown nicht manuell bearbeiten. Stattdessen Generator oder
Source-Vertrag aktualisieren und danach `make check-bilingual-docs` sowie die
passenden Dokumentationschecks ausführen. Eine Source-, Build-, Konfigurations-
oder Änderung eines generierten Reports ist allein kein Runtime-, CRS-,
Protocol-, Security- oder Production-Claim.
