<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Überblick über die sechs Compilerwege

**Sprache:** [English](overview.md) | Deutsch

## Target map

| Connector | Vorbereitung | Build | Config-Test | Ausgewählter Full Lifecycle |
| --- | --- | --- | --- | --- |
| [Apache HTTP Server](apache.de.md) | `prepare-runtime-components` | `build-apache` | `check-config-apache` | `full-lifecycle-apache` |
| [NGINX](nginx.de.md) | `prepare-runtime-components` | `build-nginx` | `check-config-nginx` | `full-lifecycle-nginx` |
| [HAProxy](haproxy.de.md) | `prepare-runtime-components` | `build-haproxy` | `check-config-haproxy` | `full-lifecycle-haproxy-htx` |
| [Envoy](envoy.de.md) | `prepare-envoy-runtime` | `build-envoy` | `check-config-envoy` | `full-lifecycle-envoy-ext-proc` |
| [Traefik](traefik.de.md) | `prepare-traefik-runtime` | `build-traefik` | `check-config-traefik` | `full-lifecycle-traefik-native` |
| [lighttpd](lighttpd.de.md) | `prepare-lighttpd-runtime-build` | `build-lighttpd` | `check-config-lighttpd` | `full-lifecycle-lighttpd-patched` |

Die Detailguides enthalten vollständige Befehle, erwartete Dateien, Exit-Code-Grenzen und Paketprüfungen. Vor einem Lauf `make runtime-components-inventory` und `make runtime-components-sources` ausführen; deren vorbereitete Records sind bei aktualisierten Pins maßgeblich.

## Three paths, three different statements

| Weg | Geeignet für | Systemweite Änderungen | Host aus Source? | Kernpfad möglich? | Evidence möglich? |
| --- | --- | --- | --- | --- | --- |
| Repository-Testweg | Entwicklung und CI | Nein | Repository-gesteuert | Ja | Ja, nach Full Lifecycle und Evidence-Check |
| Lokaler Source-Build | Entwicklung und Integration | Optional | Connectorabhängig dokumentiert | Ja | Ja, nur ausgewählter Run |
| Paketweg | Schneller lokaler Einstieg | Ja | Meist nein | Connectorabhängig | Nur passendes Profil und Run |

## Shared boundary

Die Targets erzeugen reproduzierbare Entwicklungs-, Test- und Buildartefakte. Sie sind keine Bewertung als produktionsreifes Paket oder gehärtete Deployment-Anleitung. Ein Paket, Compile oder einzelner Smoke wird nicht zu Produktions-, CRS-, Sicherheits- oder Vollmatrix-Evidence befördert.
