<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build und Lifecycle: Envoy

**Sprache:** [English](envoy.md) | Deutsch

## Zweck und ausgewählter Hostweg

Diese Anleitung beschreibt die aktuellen Root-Make-Targets für Envoy.
Der ausgewählte Full-Lifecycle-Weg ist `full-lifecycle-envoy-ext-proc` mit Profil
`ext_proc`: gestreamter Envoy-External-Processing-Service mit Common/libmodsecurity-Bridge. Er ist von Build-, Konfigurations- und
Kompatibilitäts-Smokes getrennt.

| Stufe | aktuelles Target | Bedeutung | keine Aussage über |
| --- | --- | --- | --- |
| Build | `make build-envoy` | baut die für den Connector ausgewählte Stufe | Konfigurationsladung oder Traffic |
| Konfiguration | `make check-config-envoy` | lädt/prüft die ausgewählte Konfiguration | gesendeten Request |
| Start | `make start-smoke-envoy` | startet und beendet den Hostweg ohne Volltraffic | Lifecycle-Coverage |
| minimaler Runtime-Smoke | `make runtime-smoke-envoy` | führt begrenzten Runtime-Traffic aus | kanonischer Full Lifecycle |
| Full Lifecycle | `make full-lifecycle-envoy-ext-proc` | sammelt ausgewählte No-CRS-Hostevidenz | Produktion, CRS oder Komplettmatrix |

## Hostversion und Quellherkunft

Der Framework-Laufzeitvorbereiter wählt und verifiziert Envoy-Binary und Eingabeprovenienz. Für effektive Host-Version und Prüfsumme das Cache-v2-Inventar und generierte Runtime-Records lesen statt kopierten Release-Text zu verwenden.

Vor einem Build die vorbereiteten Werte sichtbar machen:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevante Variablen: `ENVOY_BIN`, `EXT_PROC_CONFIG`, `EXT_PROC_RUNTIME_CONFIG`, `EXT_PROC_RUNTIME_ROOT`, `RULES_FILE`, `MSCONNECTOR_RULES_FILE` und das Opt-in `ENVOY_TRANSPORT_CANCEL_PROBE`.
Ihre Formate, Defaults, Scope, Wirkung und Sicherheitsgrenzen stehen in der
[zentralen Variablenreferenz](../../reference/variables.de.md). Ein
Override ist ein expliziter Eingabewechsel und kein Capability-Upgrade.

## Toolchain und Cache-v2

Für den ausgewählten ext_proc-Weg werden ein vertrauenswürdiger C-Compiler, Go-Toolchain, libmodsecurity-Build-Eingaben und ein verifiziertes Envoy-Binary benötigt. Direkte Connector-Targets verwenden generierte Dateien unterhalb eines externen Build-Roots.

Für einen sauberen lokalen Start einen beschreibbaren Stamm außerhalb des
Checkouts auswählen. `VERIFIED_RUN_PARENT` leitet `BUILD_ROOT` und
`CACHE_ROOT=.../cache-v2` ab. Das gemeinsame Cache-Verzeichnis enthält
wiederverwendbare Eingaben, aber keine kanonische Evidenz. Nicht manuell
umsortieren oder zwischen nicht passenden Provenienzen mischen.

```sh
make prepare-envoy-runtime VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-envoy VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` ist ein Beispiel für einen absoluten Laufzeitpfad,
kein Repository-Default. Der Target kann bei fehlenden Voraussetzungen mit
Exit-Code `77` als `BLOCKED` enden.

## Build, Konfiguration und Smoke

Die Stufen getrennt ausführen, damit ein Fehler keiner stärkeren Aussage
zugeordnet wird:

```sh
make build-envoy
make check-config-envoy
make start-smoke-envoy
make runtime-smoke-envoy
```

Für eine ausgewählte kanonische Evidenzausführung denselben sicheren
Run-Identifier verwenden. Der Befehl `evidence-check` validiert nur bereits
erzeugte Artefakte.

```sh
run_id="envoy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
```

`NO_CRS_RUN_ID` muss ein dateisystemsicherer Token sein. Interne
Full-Lifecycle-Profilvariablen nicht setzen, um einen direkten oder
Kompatibilitätslauf umzubenennen.

## Optionale und historische Integrationsnotizen

`make -C connectors/envoy build-envoy-ext-proc`, `test-envoy-ext-proc` und `check-envoy-ext-proc-config` sind fokussierte lokale Gates. `transport-cancel-smoke-envoy-ext-proc` ist Opt-in und bleibt nicht-promovierend.

> Historischer Hinweis: Der `ext_authz`-Service und der Kompatibilitätsweg `make smoke-envoy` bleiben nützliche Diagnosen. Sie werden nicht stillschweigend zum ausgewählten Full-Lifecycle-Profil `ext_proc`.

Ein eingeschränkter Fall, `FORCE_ALL_CASES=1` oder eine direkte
Connector-Subdirectory-Ausführung ist Diagnoseinput. Nur der dokumentierte
Target mit seinem Artefaktprofil kann kanonische Evidenz produzieren.

## Konfiguration, Beispiele und Fehlersuche

- Aktuelle Connector-Dokumentation:
  [Envoy](../../connectors/envoy.de.md)
- Konfigurationsdetails:
  [vollständige Connector-Referenz](../../../examples/envoy/configuration-reference.de.md)
- Repository-Beispiele:
  [examples/envoy](../../../examples/envoy/README.de.md)
- Test- und Evidenzgrenzen:
  [Test- und Evidence-Guide](../../testing-and-evidence.de.md)

Bei fehlgeschlagenem Config-/Start-Check aufgelöstes `ENVOY_BIN`, generierte ext_proc-Konfiguration, Loopback-Ports und libmodsecurity-Laufzeitbibliothekspfade prüfen. Ein Cancellation-Probe beweist keinen client-sichtbaren strikten Reset.

Keine ungefilterten Cookies, Autorisierungswerte, Tokens, private Schlüssel
oder Rohlogs in Konfigurationen, Issues oder Evidenz aufnehmen.

## Evidenzgrenze

Dieser Text behauptet keine Produktionsreife, vollständige CRS-Abdeckung,
HTTP/2- oder HTTP/3-Unterstützung, vollständige Matrix oder strikte
Post-Commit-Intervention. Ein PASS gilt nur für den tatsächlich ausgeführten
Target, das dokumentierte Hostprofil und dessen sanitisierten, run-spezifischen
Evidenzsatz.
