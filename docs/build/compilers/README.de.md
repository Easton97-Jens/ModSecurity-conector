<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Compiler-, Source-Build- und Paketwege

**Sprache:** [English](README.md) | Deutsch

## Zweck

Jeder Detailguide beschreibt einen repository-gesteuerten Testweg, einen
lokalen Source-Build und einen ehrlichen Paketweg. Ein Build, Link,
Config-Check, Start oder Paketinstallationsresultat ist für sich allein keine
Runtime-, CRS-, Sicherheits-, Produktions- oder Vollmatrix-Evidence.

## Gemeinsamer Einstieg

Vor jedem Connector zuerst [libmodsecurity v3 bauen](libmodsecurity.de.md).
Der Einsteigerablauf steht nur dort; die Connector-Guides beginnen danach mit
ihrem jeweiligen Host und Connector.

## Entscheidungsmatrix

| Connector | Testweg | Source-Build | Paketstatus | Ausgewählter Kernpfad |
| --- | --- | --- | --- | --- |
| [Apache HTTP Server](apache.de.md) | `make build-apache` | `make full-lifecycle-apache` | `package-assisted source build` | `native-httpd-module` |
| [NGINX](nginx.de.md) | `make build-nginx` | `make full-lifecycle-nginx` | `package-assisted source build` | `native-nginx-http-module` |
| [HAProxy](haproxy.de.md) | `make build-haproxy` | `make full-lifecycle-haproxy-htx` | `package-assisted source build` | `native-htx-filter` |
| [Envoy](envoy.de.md) | `make build-envoy` | `make full-lifecycle-envoy-ext-proc` | `package-assisted source build` | `ext_proc` |
| [Traefik](traefik.de.md) | `make build-traefik` | `make full-lifecycle-traefik-native` | `package-assisted source build` | `native-middleware` |
| [lighttpd](lighttpd.de.md) | `make build-lighttpd` | `make full-lifecycle-lighttpd-patched` | `selected profile not available package-only` | `patched-native` |

## Entscheidungsbaum

Nur testen?
→ Repository-Testweg verwenden.

Eigene Builds oder Änderungen entwickeln?
→ Lokalen Source-Build mit externem `VERIFIED_RUN_PARENT` verwenden.

Systempakete für Host und Abhängigkeiten verwenden?
→ Paketweg prüfen, Verfügbarkeit vor Installation abfragen und v3/ABI validieren.

Benötigt der Kernpfad Hostpatch, Modul, Middleware oder Service?
→ Paketgestützten Source-Build verwenden, kein Standardpaket als gleichwertig ausgeben.

## Gemeinsame Voraussetzung

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
```

Der externe Stamm liegt außerhalb des Checkouts, enthält Build-, Cache-,
Runtime-, Log- und Evidence-Dateien und sollte keine Secrets im Namen tragen.
Siehe auch [den Connectorüberblick](overview.de.md), die
[Variablenreferenz](../../reference/variables.de.md) und die
[Test-/Evidence-Grenzen](../../testing-and-evidence.de.md).
