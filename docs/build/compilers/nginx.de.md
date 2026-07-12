<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build und Lifecycle: NGINX

**Sprache:** [English](nginx.md) | Deutsch

## Zweck und ausgewählter Hostweg

Diese Anleitung beschreibt die aktuellen Root-Make-Targets für NGINX.
Der ausgewählte Full-Lifecycle-Weg ist `full-lifecycle-nginx` mit Profil
`native-nginx-http-module`: natives NGINX-HTTP-Modul. Er ist von Build-, Konfigurations- und
Kompatibilitäts-Smokes getrennt.

| Stufe | aktuelles Target | Bedeutung | keine Aussage über |
| --- | --- | --- | --- |
| Build | `make build-nginx` | baut die für den Connector ausgewählte Stufe | Konfigurationsladung oder Traffic |
| Konfiguration | `make check-config-nginx` | lädt/prüft die ausgewählte Konfiguration | gesendeten Request |
| Start | `make start-smoke-nginx` | startet und beendet den Hostweg ohne Volltraffic | Lifecycle-Coverage |
| minimaler Runtime-Smoke | `make runtime-smoke-nginx` | führt begrenzten Runtime-Traffic aus | kanonischer Full Lifecycle |
| Full Lifecycle | `make full-lifecycle-nginx` | sammelt ausgewählte No-CRS-Hostevidenz | Produktion, CRS oder Komplettmatrix |

## Hostversion und Quellherkunft

Das Framework löst die NGINX-Quellrichtlinie und die libmodsecurity-Eingaben auf. Das vorbereitete Cache-v2-Inventar mit Provenienz, nicht diese Anleitung, ist die Quelle für effektive Revision und Host-Build-Identität.

Vor einem Build die vorbereiteten Werte sichtbar machen:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevante Variablen: `BUILD_NGINX_FROM_SOURCE`, `NGINX_SOURCE_MODE`, `NGINX_SOURCE_REPO_URL`, `NGINX_SOURCE_GIT_REF`, `NGINX_RELEASE_TAG`, `NGINX_BIN`, `NGINX_PREFIX` und `NGINX_MODULE`.
Ihre Formate, Defaults, Scope, Wirkung und Sicherheitsgrenzen stehen in der
[zentralen Variablenreferenz](../../configuration/variables.de.md). Ein
Override ist ein expliziter Eingabewechsel und kein Capability-Upgrade.

## Toolchain und Cache-v2

Ein vertrauenswürdiger C-Compiler und die ausgewählten NGINX-Build-Eingaben sind erforderlich. Modul-ABI, Prefix, Worker-Berechtigungen und Laufzeitpfade gehören zum ausgewählten Host und müssen außerhalb des Checkouts liegen.

Für einen sauberen lokalen Start einen beschreibbaren Stamm außerhalb des
Checkouts auswählen. `VERIFIED_RUN_PARENT` leitet `BUILD_ROOT` und
`CACHE_ROOT=.../cache-v2` ab. Das gemeinsame Cache-Verzeichnis enthält
wiederverwendbare Eingaben, aber keine kanonische Evidenz. Nicht manuell
umsortieren oder zwischen nicht passenden Provenienzen mischen.

```sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-nginx VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` ist ein Beispiel für einen absoluten Laufzeitpfad,
kein Repository-Default. Der Target kann bei fehlenden Voraussetzungen mit
Exit-Code `77` als `BLOCKED` enden.

## Build, Konfiguration und Smoke

Die Stufen getrennt ausführen, damit ein Fehler keiner stärkeren Aussage
zugeordnet wird:

```sh
make build-nginx
make check-config-nginx
make start-smoke-nginx
make runtime-smoke-nginx
```

Für eine ausgewählte kanonische Evidenzausführung denselben sicheren
Run-Identifier verwenden. Der Befehl `evidence-check` validiert nur bereits
erzeugte Artefakte.

```sh
run_id="nginx-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-nginx
NO_CRS_RUN_ID="$run_id" make evidence-check-nginx
```

`NO_CRS_RUN_ID` muss ein dateisystemsicherer Token sein. Interne
Full-Lifecycle-Profilvariablen nicht setzen, um einen direkten oder
Kompatibilitätslauf umzubenennen.

## Optionale und historische Integrationsnotizen

Für einen diagnostischen Source-Host-Smoke `BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx` verwenden. `make check-nginx-c17` prüft die Adoptionsgrenze; das ist kein Laufzeitnachweis.

> Historischer Hinweis: Ein direkter Dynamic-Module-Build oder ein eingegrenzter Smoke kann ABI- oder Berechtigungsprobleme diagnostizieren, ersetzt aber nicht den ausgewählten Evidenzweg `native-nginx-http-module`.

Ein eingeschränkter Fall, `FORCE_ALL_CASES=1` oder eine direkte
Connector-Subdirectory-Ausführung ist Diagnoseinput. Nur der dokumentierte
Target mit seinem Artefaktprofil kann kanonische Evidenz produzieren.

## Konfiguration, Beispiele und Fehlersuche

- Aktuelle Connector-Dokumentation:
  [NGINX](../../connectors/nginx/README.de.md)
- Konfigurationsdetails:
  [Connector-Konfiguration](../../connectors/nginx/configuration.de.md)
- Repository-Beispiele:
  [examples/nginx](../../../examples/nginx/README.de.md)
- Test- und Evidenzgrenzen:
  [Teststufen](../../testing/README.de.md) ·
  [Evidenzregeln](../../evidence/README.de.md)

Bei Modul-Ladefehlern ausgewähltes Binary, Modul-ABI, Prefix und Worker-Access-Preflight prüfen. Ein Protokollprofil ohne passende Evidenz nicht als HTTP/2- oder HTTP/3-Nachweis bezeichnen.

Keine ungefilterten Cookies, Autorisierungswerte, Tokens, private Schlüssel
oder Rohlogs in Konfigurationen, Issues oder Evidenz aufnehmen.

## Evidenzgrenze

Dieser Text behauptet keine Produktionsreife, vollständige CRS-Abdeckung,
HTTP/2- oder HTTP/3-Unterstützung, vollständige Matrix oder strikte
Post-Commit-Intervention. Ein PASS gilt nur für den tatsächlich ausgeführten
Target, das dokumentierte Hostprofil und dessen sanitisierten, run-spezifischen
Evidenzsatz.
