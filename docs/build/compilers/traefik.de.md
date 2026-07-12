<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build und Lifecycle: Traefik

**Sprache:** [English](traefik.md) | Deutsch

## Zweck und ausgewählter Hostweg

Diese Anleitung beschreibt die aktuellen Root-Make-Targets für Traefik.
Der ausgewählte Full-Lifecycle-Weg ist `full-lifecycle-traefik-native` mit Profil
`native-middleware`: native Traefik-Middleware mit privatem persistentem UDS-Engine-Service. Er ist von Build-, Konfigurations- und
Kompatibilitäts-Smokes getrennt.

| Stufe | aktuelles Target | Bedeutung | keine Aussage über |
| --- | --- | --- | --- |
| Build | `make build-traefik` | baut die für den Connector ausgewählte Stufe | Konfigurationsladung oder Traffic |
| Konfiguration | `make check-config-traefik` | lädt/prüft die ausgewählte Konfiguration | gesendeten Request |
| Start | `make start-smoke-traefik` | startet und beendet den Hostweg ohne Volltraffic | Lifecycle-Coverage |
| minimaler Runtime-Smoke | `make runtime-smoke-traefik` | führt begrenzten Runtime-Traffic aus | kanonischer Full Lifecycle |
| Full Lifecycle | `make full-lifecycle-traefik-native` | sammelt ausgewählte No-CRS-Hostevidenz | Produktion, CRS oder Komplettmatrix |

## Hostversion und Quellherkunft

Der Framework-Laufzeitvorbereiter liefert die ausgewählte Traefik-Eingabe und dokumentiert ihre Provenienz. Cache-v2-Inventar und Records des ausgewählten Runs sind die Versionsquelle; ein lokal installiertes Binary ist ein explizites Override, kein versteckter Default.

Vor einem Build die vorbereiteten Werte sichtbar machen:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevante Variablen: `TRAEFIK_BIN`, `TRAEFIK_NATIVE_RUNTIME_ROOT`, `TRAEFIK_CONNECTOR_CONFIG`, `TRAEFIK_ENGINE_SERVICE_BIN`, `MSCONNECTOR_RULES_FILE` und normale Compiler-/Linker-Variablen.
Ihre Formate, Defaults, Scope, Wirkung und Sicherheitsgrenzen stehen in der
[zentralen Variablenreferenz](../../configuration/variables.de.md). Ein
Override ist ein expliziter Eingabewechsel und kein Capability-Upgrade.

## Toolchain und Cache-v2

Für den ausgewählten nativen Middleware-Weg werden ein vertrauenswürdiges Traefik-Binary, Go-Toolchain, C-Compiler und libmodsecurity-Build-Eingaben benötigt. UDS-Service und generierte Provider-Konfiguration sind invocationslokale Runtime-Dateien.

Für einen sauberen lokalen Start einen beschreibbaren Stamm außerhalb des
Checkouts auswählen. `VERIFIED_RUN_PARENT` leitet `BUILD_ROOT` und
`CACHE_ROOT=.../cache-v2` ab. Das gemeinsame Cache-Verzeichnis enthält
wiederverwendbare Eingaben, aber keine kanonische Evidenz. Nicht manuell
umsortieren oder zwischen nicht passenden Provenienzen mischen.

```sh
make prepare-traefik-runtime VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-traefik VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` ist ein Beispiel für einen absoluten Laufzeitpfad,
kein Repository-Default. Der Target kann bei fehlenden Voraussetzungen mit
Exit-Code `77` als `BLOCKED` enden.

## Build, Konfiguration und Smoke

Die Stufen getrennt ausführen, damit ein Fehler keiner stärkeren Aussage
zugeordnet wird:

```sh
make build-traefik
make check-config-traefik
make start-smoke-traefik
make runtime-smoke-traefik
```

Für eine ausgewählte kanonische Evidenzausführung denselben sicheren
Run-Identifier verwenden. Der Befehl `evidence-check` validiert nur bereits
erzeugte Artefakte.

```sh
run_id="traefik-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
```

`NO_CRS_RUN_ID` muss ein dateisystemsicherer Token sein. Interne
Full-Lifecycle-Profilvariablen nicht setzen, um einen direkten oder
Kompatibilitätslauf umzubenennen.

## Optionale und historische Integrationsnotizen

`make -C connectors/traefik build-native-middleware`, `test-native-middleware`, `build-engine-service` und `test-engine-service` sind fokussierte lokale Checks. Sie erzeugen für sich allein keine kanonische Evidenz.

> Historischer Hinweis: Der ForwardAuth-Kompatibilitätsservice und `make smoke-traefik` sind getrennte Diagnosewege. Sie ersetzen das ausgewählte Profil `native-middleware` nicht und beweisen keine strikte Post-Commit-Aktion.

Ein eingeschränkter Fall, `FORCE_ALL_CASES=1` oder eine direkte
Connector-Subdirectory-Ausführung ist Diagnoseinput. Nur der dokumentierte
Target mit seinem Artefaktprofil kann kanonische Evidenz produzieren.

## Konfiguration, Beispiele und Fehlersuche

- Aktuelle Connector-Dokumentation:
  [Traefik](../../connectors/traefik/README.de.md)
- Konfigurationsdetails:
  [Connector-Konfiguration](../../connectors/traefik/configuration.de.md)
- Repository-Beispiele:
  [examples/traefik](../../../examples/traefik/README.de.md)
- Test- und Evidenzgrenzen:
  [Teststufen](../../testing/README.de.md) ·
  [Evidenzregeln](../../evidence/README.de.md)

Ausgewähltes `TRAEFIK_BIN`, UDS-Berechtigungen, generierte File-Provider-Konfiguration und Loopback-Listener prüfen. Einen Native-Middleware-Fehler nicht durch Veröffentlichung von ForwardAuth-Kompatibilitätsausgabe als kanonische Evidenz umgehen.

Keine ungefilterten Cookies, Autorisierungswerte, Tokens, private Schlüssel
oder Rohlogs in Konfigurationen, Issues oder Evidenz aufnehmen.

## Evidenzgrenze

Dieser Text behauptet keine Produktionsreife, vollständige CRS-Abdeckung,
HTTP/2- oder HTTP/3-Unterstützung, vollständige Matrix oder strikte
Post-Commit-Intervention. Ein PASS gilt nur für den tatsächlich ausgeführten
Target, das dokumentierte Hostprofil und dessen sanitisierten, run-spezifischen
Evidenzsatz.
