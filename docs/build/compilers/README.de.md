<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Compiler- und Build-Wege

**Sprache:** [English](README.md) | Deutsch

## Zweck

Dieses Verzeichnis beschreibt die aktuellen Repository-Wege für Build,
Konfigurationsladung, Start-Smoke, minimalen Runtime-Smoke und den ausgewählten
No-CRS-Full-Lifecycle-Run. Es ist keine Anleitung, einen beliebigen
Distributionshost global zu installieren. Ein erfolgreicher Build, Link oder
Config-Check ist kein Produktions-, CRS-, HTTP/2-, HTTP/3- oder
Vollmatrix-Nachweis.

## Ausgewählte Wege

| Detailanleitung | Build | ausgewähltes Full-Lifecycle-Target | Host-Profil |
| --- | --- | --- | --- |
| [Apache HTTP Server](apache.de.md) | `build-apache` | `full-lifecycle-apache` | `native-httpd-module` |
| [NGINX](nginx.de.md) | `build-nginx` | `full-lifecycle-nginx` | `native-nginx-http-module` |
| [HAProxy](haproxy.de.md) | `build-haproxy` | `full-lifecycle-haproxy-htx` | `native-htx-filter` |
| [Envoy](envoy.de.md) | `build-envoy` | `full-lifecycle-envoy-ext-proc` | `ext_proc` |
| [Traefik](traefik.de.md) | `build-traefik` | `full-lifecycle-traefik-native` | `native-middleware` |
| [lighttpd](lighttpd.de.md) | `build-lighttpd` | `full-lifecycle-lighttpd-patched` | `patched-native` |

Die Host-Profilwerte setzt das jeweilige Full-Lifecycle-Target selbst. Die
internen Variablen `NO_CRS_ARTIFACT_PROFILE`,
`FULL_LIFECYCLE_HOST_PROFILE` und `FULL_LIFECYCLE_EXECUTED_TARGET` dürfen nicht
manuell gesetzt werden, um einen Kompatibilitäts-Smoke umzubenennen.

## Gemeinsamer Ablauf

```sh
make check-framework
make prepare-runtime-components
make build-<connector>
make check-config-<connector>
make start-smoke-<connector>
make runtime-smoke-<connector>
```

`<connector>` ist ein Dokumentationsplatzhalter für genau einen Namen aus der
Tabelle. Den Platzhalter nicht wörtlich an `make` übergeben. Für eine
kanonische Evidenz muss ein sicherer Run-Identifier derselben Ausführung
verwendet werden:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-<connector>
NO_CRS_RUN_ID="$run_id" make evidence-check-<connector>
```

Die vollständige Ausführung aller sechs Connectoren ist
`NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors`. Sie erzeugt
run-spezifische Evidenz; sie ersetzt keine Prüfung der resultierenden
Artefakte.

## Cache-v2, Versionen und Provenienz

`VERIFIED_RUN_PARENT` bestimmt einen externen, beschreibbaren
Ausführungsstamm. Daraus leitet der Root-Makefile `BUILD_ROOT` sowie
`CACHE_ROOT=.../cache-v2` und dessen gemeinsames Component-Cache ab. Das Cache
ist wiederverwendbare Eingabe, nicht kanonische Evidenz. Quellen, Versionen,
Prüfsummen und lokale Overrides werden durch die vorbereiteten Komponenten
gebunden; die effektive Identität zeigt:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Die [Variablenreferenz](../../configuration/variables.de.md) definiert Format,
Standard, Scope, Wirkung und Sicherheitsgrenze aller Build-, Cache-,
Provenienz- und Hostvariablen. Nur vertrauenswürdige absolute Pfade außerhalb
des Checkouts für Build, Cache, Log und Evidenz verwenden.

## Dokumentationsgrenze

Die nachstehenden pro-Connector-Anleitungen verweisen auf die aktuelle
[Build-Übersicht](../README.de.md), die
[Teststufen](../../testing/README.de.md), die
[Evidenzregeln](../../evidence/README.de.md), Connector-Anleitungen und
Beispiele. Ältere Integrationsbeschreibungen bleiben gegebenenfalls als
historische oder diagnostische Hinweise markiert; sie sind keine aktiven
Profilselektoren und dürfen keine Capability promoten.

## Weiterführend

Die kompaktere Übersicht für Envoy, Traefik und lighttpd steht in
[Open-Connector-Wege](overview.de.md). Die Detailanleitungen beginnen bei
[Apache](apache.de.md).
