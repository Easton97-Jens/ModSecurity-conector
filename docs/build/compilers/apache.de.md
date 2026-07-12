<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build und Lifecycle: Apache HTTP Server

**Sprache:** [English](apache.md) | Deutsch

## Zweck und ausgewählter Hostweg

Diese Anleitung beschreibt die aktuellen Root-Make-Targets für Apache HTTP Server.
Der ausgewählte Full-Lifecycle-Weg ist `full-lifecycle-apache` mit Profil
`native-httpd-module`: natives httpd-Modul, das über APXS gebaut wird. Er ist von Build-, Konfigurations- und
Kompatibilitäts-Smokes getrennt.

| Stufe | aktuelles Target | Bedeutung | keine Aussage über |
| --- | --- | --- | --- |
| Build | `make build-apache` | baut die für den Connector ausgewählte Stufe | Konfigurationsladung oder Traffic |
| Konfiguration | `make check-config-apache` | lädt/prüft die ausgewählte Konfiguration | gesendeten Request |
| Start | `make start-smoke-apache` | startet und beendet den Hostweg ohne Volltraffic | Lifecycle-Coverage |
| minimaler Runtime-Smoke | `make runtime-smoke-apache` | führt begrenzten Runtime-Traffic aus | kanonischer Full Lifecycle |
| Full Lifecycle | `make full-lifecycle-apache` | sammelt ausgewählte No-CRS-Hostevidenz | Produktion, CRS oder Komplettmatrix |

## Hostversion und Quellherkunft

Die Framework-gesteuerte Provenienz für Apache, APR, PCRE2 und libmodsecurity wird bei der Vorbereitung ausgewählt. Effektive Version, URL und Prüfsumme stehen im Cache-v2-Inventar; keine Version aus einer alten Anleitung übernehmen.

Vor einem Build die vorbereiteten Werte sichtbar machen:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevante Variablen: `BUILD_HTTPD_FROM_SOURCE`, `APACHE_BIN`, `APACHECTL_BIN`, `APXS_BIN` sowie die vom Framework weitergereichten Apache-Quell- und Prüfsummenvariablen.
Ihre Formate, Defaults, Scope, Wirkung und Sicherheitsgrenzen stehen in der
[zentralen Variablenreferenz](../../reference/variables.de.md). Ein
Override ist ein expliziter Eingabewechsel und kein Capability-Upgrade.

## Toolchain und Cache-v2

Ein vertrauenswürdiger C-Compiler, Autotools/APXS und passende Apache-Entwicklungsheader sind für einen lokalen Host-Build oder -Check erforderlich. Der C17-Adoptionscheck des Repositorys kann bei fehlenden Headern `77` melden.

Für einen sauberen lokalen Start einen beschreibbaren Stamm außerhalb des
Checkouts auswählen. `VERIFIED_RUN_PARENT` leitet `BUILD_ROOT` und
`CACHE_ROOT=.../cache-v2` ab. Das gemeinsame Cache-Verzeichnis enthält
wiederverwendbare Eingaben, aber keine kanonische Evidenz. Nicht manuell
umsortieren oder zwischen nicht passenden Provenienzen mischen.

```sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-apache VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` ist ein Beispiel für einen absoluten Laufzeitpfad,
kein Repository-Default. Der Target kann bei fehlenden Voraussetzungen mit
Exit-Code `77` als `BLOCKED` enden.

## Build, Konfiguration und Smoke

Die Stufen getrennt ausführen, damit ein Fehler keiner stärkeren Aussage
zugeordnet wird:

```sh
make build-apache
make check-config-apache
make start-smoke-apache
make runtime-smoke-apache
```

Für eine ausgewählte kanonische Evidenzausführung denselben sicheren
Run-Identifier verwenden. Der Befehl `evidence-check` validiert nur bereits
erzeugte Artefakte.

```sh
run_id="apache-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-apache
NO_CRS_RUN_ID="$run_id" make evidence-check-apache
```

`NO_CRS_RUN_ID` muss ein dateisystemsicherer Token sein. Interne
Full-Lifecycle-Profilvariablen nicht setzen, um einen direkten oder
Kompatibilitätslauf umzubenennen.

## Optionale und historische Integrationsnotizen

Für einen diagnostischen Source-Host-Smoke `BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache` verwenden. `make check-apache-c17` prüft die Adoptionsgrenze; optionale neuere C-Profile hängen weiter vom Toolchain-Support ab.

> Historischer Hinweis: Ältere Paketinstallationsbeispiele und allgemeine Smoke-Beschreibungen sind nur Kompatibilitätshinweise. Sie wählen oder ersetzen das Full-Lifecycle-Profil `native-httpd-module` nicht.

Ein eingeschränkter Fall, `FORCE_ALL_CASES=1` oder eine direkte
Connector-Subdirectory-Ausführung ist Diagnoseinput. Nur der dokumentierte
Target mit seinem Artefaktprofil kann kanonische Evidenz produzieren.

## Konfiguration, Beispiele und Fehlersuche

- Aktuelle Connector-Dokumentation:
  [Apache HTTP Server](../../connectors/apache.de.md)
- Konfigurationsdetails:
  [vollständige Connector-Referenz](../../../examples/apache/configuration-reference.de.md)
- Repository-Beispiele:
  [examples/apache](../../../examples/apache/README.de.md)
- Test- und Evidenzgrenzen:
  [Test- und Evidence-Guide](../../testing-and-evidence.de.md)

Bei nicht zusammenpassendem APXS und httpd gegen den ausgewählten Host neu bauen. Schlägt der Konfigurationsschritt fehl, zuerst generierte Konfiguration und sanitisiertes Host-Log prüfen, bevor Regeln oder Modulpfade geändert werden.

Keine ungefilterten Cookies, Autorisierungswerte, Tokens, private Schlüssel
oder Rohlogs in Konfigurationen, Issues oder Evidenz aufnehmen.

## Evidenzgrenze

Dieser Text behauptet keine Produktionsreife, vollständige CRS-Abdeckung,
HTTP/2- oder HTTP/3-Unterstützung, vollständige Matrix oder strikte
Post-Commit-Intervention. Ein PASS gilt nur für den tatsächlich ausgeführten
Target, das dokumentierte Hostprofil und dessen sanitisierten, run-spezifischen
Evidenzsatz.
