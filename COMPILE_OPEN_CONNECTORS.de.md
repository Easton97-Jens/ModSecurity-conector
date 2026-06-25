Sprache: [English](COMPILE_OPEN_CONNECTORS.md) | Deutsch

# Compile / Prepare Open Connectors

## Inhaltsverzeichnis

- [Zweck](#zweck)
- [Status und Grenzen](#status-und-grenzen)
- [Überblick: Drei Pfade](#überblick-drei-pfade)
- [Pfad 1: Repository-Smoke / Validierung](#pfad-1-repository-smoke--validierung)
- [Pfad 2: Externer Einsatz mit Paketen](#pfad-2-externer-einsatz-mit-paketen)
- [Pfad 3: Externer Einsatz aus Source](#pfad-3-externer-einsatz-aus-source)
- [Connector-spezifische Guides](#connector-spezifische-guides)
- [Nicht erlaubte Claims](#nicht-erlaubte-claims)

## Zweck

Dies ist ein gemeinsamer Index für die offenen Runtime-Pfade Envoy, Traefik und Lighttpd. Nutzen Sie die connector-spezifischen Guides für Betreiber-Schritte; diese Datei fasst nur gemeinsame Repository-Vorbereitung und Evidence-Regeln zusammen.

## Status und Grenzen

Envoy und Traefik werden von diesem Repository als Runtime-Komponenten gestaged, nicht aus Source gebaut. Lighttpd kann lokal aus einem gepinnten Source-Tarball gebaut werden, aber die aktuelle Integration bleibt `sidecar_proxy` / Phase 1 und kein natives Modul. PASS in dieser Datei bedeutet, dass ein Repository-Target/Evidence-Pfad existiert, wenn Abhängigkeiten vorhanden sind; das ist keine Produktionsreife.

## Überblick: Drei Pfade

| Pfad | Zweck | Haupteinsatz |
| --- | --- | --- |
| Pfad 1: Repository-Smoke | Repository-Evidence validieren | Entwickler / Reviewer |
| Pfad 2: Externer Einsatz mit Paketen | Vom Betreiber bereitgestellte Runtime-Pakete/Binaries nutzen | Betreiber mit Systempaketen |
| Pfad 3: Externer Einsatz aus Source | libmodsecurity und anwendbare Sidecar-/Runtime-Teile bauen | Betreiber mit genauer Versionskontrolle |

## Pfad 1: Repository-Smoke / Validierung

Diese Befehle validieren Repository-Evidence. Sie sind nicht die externe Installationsprozedur.

```sh
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
TMPDIR=/tmp make smoke-envoy
TMPDIR=/tmp make smoke-traefik
TMPDIR=/tmp make smoke-lighttpd
```

Targeted libmodsecurity- und CRS-Smokes sind nur Repository-Evidence:

```sh
TMPDIR=/tmp make smoke-envoy-modsecurity
TMPDIR=/tmp make smoke-traefik-modsecurity
TMPDIR=/tmp make smoke-lighttpd-modsecurity
TMPDIR=/tmp make smoke-open-connectors-crs
TMPDIR=/tmp make smoke-open-connectors-crs-secondary
```

## Pfad 2: Externer Einsatz mit Paketen

Nutzen Sie vom Betreiber bereitgestellte Envoy-, Traefik- oder Lighttpd-Pakete/Binaries, sofern kompatibel. Paketnamen, Service-Namen, Runtime-Verzeichnisse und Log-Orte variieren je Distribution. Das Repository installiert diese Komponenten nicht global. Folgen Sie dem jeweiligen Guide für ext_authz-, forwardAuth- oder sidecar_proxy-Wiring und Beispiel-Konfigurationen.

## Pfad 3: Externer Einsatz aus Source

Für Envoy und Traefik ist das Bauen des Proxys selbst aus Source kein repository-unterstützter Pfad. Source-basierter externer Einsatz betrifft libmodsecurity und vom Betreiber bereitzustellende Decision-Backends. Für Lighttpd kann der Repository-Helper die gepinnte Lighttpd-Runtime lokal bauen, aber das bleibt ein sidecar_proxy-Pfad und kein nativer Connector.

## Connector-spezifische Guides

- [Envoy](COMPILE_ENVOY.de.md)
- [Traefik](COMPILE_TRAEFIK.de.md)
- [Lighttpd](COMPILE_LIGHTTPD.de.md)

## Nicht erlaubte Claims

Open-Connector-Evidence darf Folgendes nicht claimen:

- `production_ready = true`
- `full_matrix_ready = true`
- `crs_complete = true`
- `response_body_verified = true`

Lighttpd-Phase-1-Evidence darf außerdem kein natives Lighttpd-Modul claimen.
