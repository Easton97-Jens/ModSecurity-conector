<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build und Lifecycle: HAProxy

**Sprache:** [English](haproxy.md) | Deutsch

## Zweck und ausgewählter Hostweg

Diese Anleitung beschreibt die aktuellen Root-Make-Targets für HAProxy.
Der ausgewählte Full-Lifecycle-Weg ist `full-lifecycle-haproxy-htx` mit Profil
`native-htx-filter`: nativer HTX-Filter, der für den vollständigen Lifecycle ausgewählt ist. Er ist von Build-, Konfigurations- und
Kompatibilitäts-Smokes getrennt.

| Stufe | aktuelles Target | Bedeutung | keine Aussage über |
| --- | --- | --- | --- |
| Build | `make build-haproxy` | baut die für den Connector ausgewählte Stufe | Konfigurationsladung oder Traffic |
| Konfiguration | `make check-config-haproxy` | lädt/prüft die ausgewählte Konfiguration | gesendeten Request |
| Start | `make start-smoke-haproxy` | startet und beendet den Hostweg ohne Volltraffic | Lifecycle-Coverage |
| minimaler Runtime-Smoke | `make runtime-smoke-haproxy` | führt begrenzten Runtime-Traffic aus | kanonischer Full Lifecycle |
| Full Lifecycle | `make full-lifecycle-haproxy-htx` | sammelt ausgewählte No-CRS-Hostevidenz | Produktion, CRS oder Komplettmatrix |

## Hostversion und Quellherkunft

Der Framework-/Provider-Pin wählt HAProxy-Quelle, Prüfsumme und Laufzeiteingaben. Cache-v2-Provenienz und Host-Metadaten des ausgewählten Runs liefern die effektive Host-Identität; diese nicht aus einem Kompatibilitäts-Agent-Build ableiten.

Vor einem Build die vorbereiteten Werte sichtbar machen:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevante Variablen: `HAPROXY_VERSION`, `HAPROXY_SOURCE_URL`, `HAPROXY_SHA256`, `HAPROXY_SOURCE_DIR`, `HAPROXY_BIN` und die erweiterten `HAPROXY_HTX_*`-Pfade.
Ihre Formate, Defaults, Scope, Wirkung und Sicherheitsgrenzen stehen in der
[zentralen Variablenreferenz](../../configuration/variables.de.md). Ein
Override ist ein expliziter Eingabewechsel und kein Capability-Upgrade.

## Toolchain und Cache-v2

Ein vertrauenswürdiges C/C++-Toolchain, libmodsecurity-Header/-Bibliotheken und die ausgewählte HAProxy-Quelle werden benötigt. Der Root-Build erzeugt SPOA/libmodsecurity-Kompatibilitätsartefakte; der ausgewählte Full-Lifecycle-Weg baut und beobachtet den HTX-Host-Overlay getrennt.

Für einen sauberen lokalen Start einen beschreibbaren Stamm außerhalb des
Checkouts auswählen. `VERIFIED_RUN_PARENT` leitet `BUILD_ROOT` und
`CACHE_ROOT=.../cache-v2` ab. Das gemeinsame Cache-Verzeichnis enthält
wiederverwendbare Eingaben, aber keine kanonische Evidenz. Nicht manuell
umsortieren oder zwischen nicht passenden Provenienzen mischen.

```sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-haproxy VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` ist ein Beispiel für einen absoluten Laufzeitpfad,
kein Repository-Default. Der Target kann bei fehlenden Voraussetzungen mit
Exit-Code `77` als `BLOCKED` enden.

## Build, Konfiguration und Smoke

Die Stufen getrennt ausführen, damit ein Fehler keiner stärkeren Aussage
zugeordnet wird:

```sh
make build-haproxy
make check-config-haproxy
make start-smoke-haproxy
make runtime-smoke-haproxy
```

Für eine ausgewählte kanonische Evidenzausführung denselben sicheren
Run-Identifier verwenden. Der Befehl `evidence-check` validiert nur bereits
erzeugte Artefakte.

```sh
run_id="haproxy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-haproxy-htx
NO_CRS_RUN_ID="$run_id" make evidence-check-haproxy
```

`NO_CRS_RUN_ID` muss ein dateisystemsicherer Token sein. Interne
Full-Lifecycle-Profilvariablen nicht setzen, um einen direkten oder
Kompatibilitätslauf umzubenennen.

## Optionale und historische Integrationsnotizen

`make -C connectors/haproxy build-spoa-runtime` und seine Selbsttests sind hilfreiche lokale Diagnosen. `make check-haproxy-htx-overlay` prüft die Overlay-Struktur; `make check-haproxy-c17` die C-Adoptionsgrenze.

> Historischer Hinweis: Der SPOE/SPOP-Kompatibilitäts-Agent und ein eigenständiger HTX-Smoke sind historische oder diagnostische Integrationswege. Sie dürfen nicht als kanonischer `native-htx-filter`-Run umetikettiert werden.

Ein eingeschränkter Fall, `FORCE_ALL_CASES=1` oder eine direkte
Connector-Subdirectory-Ausführung ist Diagnoseinput. Nur der dokumentierte
Target mit seinem Artefaktprofil kann kanonische Evidenz produzieren.

## Konfiguration, Beispiele und Fehlersuche

- Aktuelle Connector-Dokumentation:
  [HAProxy](../../connectors/haproxy/README.de.md)
- Konfigurationsdetails:
  [Connector-Konfiguration](../../connectors/haproxy/configuration.de.md)
- Repository-Beispiele:
  [examples/haproxy](../../../examples/haproxy/README.de.md)
- Test- und Evidenzgrenzen:
  [Teststufen](../../testing/README.de.md) ·
  [Evidenzregeln](../../evidence/README.de.md)

Ist ein Binding-Build blockiert, die vorbereiteten libmodsecurity-Include-/Library-Pfade prüfen. Schlägt der HTX-Weg fehl, Overlay-Provenienz und sanitisierte Host-Records bewahren, statt ein SPOA-Ergebnis zu ersetzen.

Keine ungefilterten Cookies, Autorisierungswerte, Tokens, private Schlüssel
oder Rohlogs in Konfigurationen, Issues oder Evidenz aufnehmen.

## Evidenzgrenze

Dieser Text behauptet keine Produktionsreife, vollständige CRS-Abdeckung,
HTTP/2- oder HTTP/3-Unterstützung, vollständige Matrix oder strikte
Post-Commit-Intervention. Ein PASS gilt nur für den tatsächlich ausgeführten
Target, das dokumentierte Hostprofil und dessen sanitisierten, run-spezifischen
Evidenzsatz.
