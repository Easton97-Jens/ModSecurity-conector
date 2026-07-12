<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build und Lifecycle: lighttpd

**Sprache:** [English](lighttpd.md) | Deutsch

## Zweck und ausgewählter Hostweg

Diese Anleitung beschreibt die aktuellen Root-Make-Targets für lighttpd.
Der ausgewählte Full-Lifecycle-Weg ist `full-lifecycle-lighttpd-patched` mit Profil
`patched-native`: gepatchter nativer lighttpd-Host mit passendem Connector-Modul. Er ist von Build-, Konfigurations- und
Kompatibilitäts-Smokes getrennt.

| Stufe | aktuelles Target | Bedeutung | keine Aussage über |
| --- | --- | --- | --- |
| Build | `make build-lighttpd` | baut die für den Connector ausgewählte Stufe | Konfigurationsladung oder Traffic |
| Konfiguration | `make check-config-lighttpd` | lädt/prüft die ausgewählte Konfiguration | gesendeten Request |
| Start | `make start-smoke-lighttpd` | startet und beendet den Hostweg ohne Volltraffic | Lifecycle-Coverage |
| minimaler Runtime-Smoke | `make runtime-smoke-lighttpd` | führt begrenzten Runtime-Traffic aus | kanonischer Full Lifecycle |
| Full Lifecycle | `make full-lifecycle-lighttpd-patched` | sammelt ausgewählte No-CRS-Hostevidenz | Produktion, CRS oder Komplettmatrix |

## Hostversion und Quellherkunft

Die vom Framework/Provider ausgewählten lighttpd-Quelle, der Patch und libmodsecurity-Eingaben sind provenienzgeführt. Cache-v2-Inventar und Records des ausgewählten Hosts nennen die effektive Source-Identität; ein lokales Stock-Binary ist nicht der ausgewählte gepatchte Host.

Vor einem Build die vorbereiteten Werte sichtbar machen:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevante Variablen: `LIGHTTPD_BIN`, `LIGHTTPD_SOURCE_DIR`, `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_INCLUDE_DIR`, `LIGHTTPD_MODULE_DIR`, `LIGHTTPD_PATCHED_ROOT` und die dokumentierten `LIGHTTPD_PATCHED_*`-Laufzeitpfade.
Ihre Formate, Defaults, Scope, Wirkung und Sicherheitsgrenzen stehen in der
[zentralen Variablenreferenz](../../configuration/variables.de.md). Ein
Override ist ein expliziter Eingabewechsel und kein Capability-Upgrade.

## Toolchain und Cache-v2

Ein vertrauenswürdiges C-Toolchain, die ausgewählte lighttpd-Quelle mit Patch, libmodsecurity-Header/-Bibliotheken und ein externer Build-Root sind nötig. Gepatchter Host und Modul müssen als kompatibler Eingabesatz gebaut werden.

Für einen sauberen lokalen Start einen beschreibbaren Stamm außerhalb des
Checkouts auswählen. `VERIFIED_RUN_PARENT` leitet `BUILD_ROOT` und
`CACHE_ROOT=.../cache-v2` ab. Das gemeinsame Cache-Verzeichnis enthält
wiederverwendbare Eingaben, aber keine kanonische Evidenz. Nicht manuell
umsortieren oder zwischen nicht passenden Provenienzen mischen.

```sh
make prepare-lighttpd-runtime-build VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-lighttpd VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` ist ein Beispiel für einen absoluten Laufzeitpfad,
kein Repository-Default. Der Target kann bei fehlenden Voraussetzungen mit
Exit-Code `77` als `BLOCKED` enden.

## Build, Konfiguration und Smoke

Die Stufen getrennt ausführen, damit ein Fehler keiner stärkeren Aussage
zugeordnet wird:

```sh
make build-lighttpd
make check-config-lighttpd
make start-smoke-lighttpd
make runtime-smoke-lighttpd
```

Für eine ausgewählte kanonische Evidenzausführung denselben sicheren
Run-Identifier verwenden. Der Befehl `evidence-check` validiert nur bereits
erzeugte Artefakte.

```sh
run_id="lighttpd-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
```

`NO_CRS_RUN_ID` muss ein dateisystemsicherer Token sein. Interne
Full-Lifecycle-Profilvariablen nicht setzen, um einen direkten oder
Kompatibilitätslauf umzubenennen.

## Optionale und historische Integrationsnotizen

`make -C connectors/lighttpd check-lighttpd-core-patch`, `build-lighttpd-patched-host` und `check-lighttpd-patched-host` sind gezielte Vorbereitungstests. `make smoke-lighttpd` bleibt ein Kompatibilitäts-Smoke, nicht der gepatchte Full-Lifecycle-Run.

> Historischer Hinweis: Stock-Host- und Bridge-/Sidecar-Beschreibungen sind historische oder diagnostische Wege. Die aktuelle kanonische Auswahl ist das Host-Profil `patched-native`; ein erfolgreicher Patch-Apply allein ist kein Laufzeitnachweis.

Ein eingeschränkter Fall, `FORCE_ALL_CASES=1` oder eine direkte
Connector-Subdirectory-Ausführung ist Diagnoseinput. Nur der dokumentierte
Target mit seinem Artefaktprofil kann kanonische Evidenz produzieren.

## Konfiguration, Beispiele und Fehlersuche

- Aktuelle Connector-Dokumentation:
  [lighttpd](../../connectors/lighttpd/README.de.md)
- Konfigurationsdetails:
  [Connector-Konfiguration](../../connectors/lighttpd/configuration.de.md)
- Repository-Beispiele:
  [examples/lighttpd](../../../examples/lighttpd/README.de.md)
- Test- und Evidenzgrenzen:
  [Teststufen](../../testing/README.de.md) ·
  [Evidenzregeln](../../evidence/README.de.md)

Bei Modul-Lade- oder Patch-Fehlern ausgewählte Quelle, Patch und Modul-Build-Roots zusammenhalten und das sanitisierte Host-Log prüfen. Ein Stock-Binary nicht mit einem Modul aus einem anderen Headersatz kombinieren.

Keine ungefilterten Cookies, Autorisierungswerte, Tokens, private Schlüssel
oder Rohlogs in Konfigurationen, Issues oder Evidenz aufnehmen.

## Evidenzgrenze

Dieser Text behauptet keine Produktionsreife, vollständige CRS-Abdeckung,
HTTP/2- oder HTTP/3-Unterstützung, vollständige Matrix oder strikte
Post-Commit-Intervention. Ein PASS gilt nur für den tatsächlich ausgeführten
Target, das dokumentierte Hostprofil und dessen sanitisierten, run-spezifischen
Evidenzsatz.
