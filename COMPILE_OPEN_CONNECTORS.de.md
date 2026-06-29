# Compile / Prepare Open Connectors


**Sprache:** [English](COMPILE_OPEN_CONNECTORS.md) | Deutsch

## Inhaltsverzeichnis

- [Zweck](#zweck)
- [Status und Grenzen](#status-und-grenzen)
- [Überblick: Drei Pfade](#überblick-drei-pfade)
- [Pfad 1: Repository-Smoke / Validierung](#pfad-1-repository-smoke--validierung)
- [CI-Workflow und Artefakte](#ci-workflow-und-artefakte)
- [Pfad 2: Externer Einsatz mit Distribution-Paketen](#pfad-2-externer-einsatz-mit-distribution-paketen)
- [Pfad 3: Externer Einsatz aus Source](#pfad-3-externer-einsatz-aus-source)
- [Connector-spezifische Guides](#connector-spezifische-guides)
- [Nicht erlaubte Claims](#nicht-erlaubte-claims)

## Zweck

Dies ist ein gemeinsamer Index für die offenen Connector-Runtime-Pfade: Envoy,
Traefik und Lighttpd. Verwenden Sie die connector-spezifischen Guides für
Betreiberschritte; diese Datei fasst nur gemeinsame Repository-Vorbereitung und
Evidence-Regeln zusammen.

## Status und Grenzen

Envoy und Traefik werden von diesem Repository zur Runtime bereitgestellt, aber
nicht aus Source gebaut. Lighttpd kann lokal aus einem gepinnten Source-Tarball
gebaut werden, die aktuelle Integration ist jedoch `sidecar_proxy` / Phase 1
und kein natives Modul. PASS in dieser Datei bedeutet, dass ein
Repository-Target-/Evidence-Pfad existiert, wenn Abhängigkeiten vorhanden sind;
es bedeutet keine Produktionsreife.

## Überblick: Drei Pfade

| Pfad | Zweck | Haupteinsatz |
| --- | --- | --- |
| Pfad 1: Repository-Smoke | Repository-Evidence validieren | Entwickler / Reviewer |
| Pfad 2: Externer Einsatz mit Paketen | Betreiberseitige Runtime-Pakete/-Binaries nutzen | Betreiber mit Systempaketen |
| Pfad 3: Externer Einsatz aus Source | libmodsecurity und anwendbare Sidecar-/Runtime-Teile bauen | Betreiber mit genauer Versionskontrolle |

## Pfad 1: Repository-Smoke / Validierung

Diese Befehle validieren Repository-Evidence. Sie sind nicht die externe
Installationsprozedur.

```sh
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
TMPDIR=/tmp ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
TMPDIR=/tmp make smoke-envoy
TMPDIR=/tmp make smoke-traefik
TMPDIR=/tmp make smoke-lighttpd
```

Gezielte libmodsecurity- und CRS-Smokes sind nur Repository-Evidence:

```sh
TMPDIR=/tmp make smoke-envoy-modsecurity
TMPDIR=/tmp make smoke-traefik-modsecurity
TMPDIR=/tmp make smoke-lighttpd-modsecurity
TMPDIR=/tmp make smoke-open-connectors-crs
TMPDIR=/tmp make smoke-open-connectors-crs-secondary
```

## CI-Workflow und Artefakte

Der manuelle GitHub-Actions-Workflow
`.github/workflows/open-connectors-smoke.yml` führt denselben
Repository-Evidence-Pfad unter `TMPDIR=/tmp` aus:

- Envoy- und Traefik-Runtime-Komponenten mit `ALLOW_RUNTIME_DOWNLOADS=1`
  vorbereiten;
- Lighttpd mit `ALLOW_RUNTIME_DOWNLOADS=1` und `ALLOW_RUNTIME_BUILDS=1`
  vorbereiten und bauen;
- einfache, gezielte libmodsecurity-, Minimal-CRS- und sekundäre CRS-Smokes
  ausführen;
- `make lint`, `make quick-check` und `git diff --check` ausführen;
- `ci-artifacts/open-connectors/` als `open-connectors-smoke-evidence`
  hochladen.

Das hochgeladene Artefakt enthält den kopierten
`/tmp/ModSecurity-conector-verified/`-Baum, Runtime-Inventory-Ausgabe,
Result-JSON, Decision-Logs, Audit-Logs und Request-Transcripts, die während des
Laufs erzeugt wurden.

## Pfad 2: Externer Einsatz mit Distribution-Paketen

Verwenden Sie betreiberseitig bereitgestellte Envoy-, Traefik- oder
Lighttpd-Pakete/-Binaries, wo sie kompatibel sind. Paketnamen, Servicenamen,
Runtime-Verzeichnisse und Log-Orte unterscheiden sich je Distribution. Das
Repository installiert diese Komponenten nicht global. Folgen Sie dem
connector-spezifischen Guide für ext_authz-, forwardAuth- oder
sidecar_proxy-Verdrahtung und Beispielkonfigurationen.

## Pfad 3: Externer Einsatz aus Source

Behandeln Sie bei Envoy und Traefik den Source-Build des Proxys selbst nicht als
repository-unterstützt. Source-basierter externer Einsatz bezieht sich auf
libmodsecurity und jedes betreiberseitig bereitgestellte Decision-Backend. Bei
Lighttpd kann der Repository-Helper die gepinnte Lighttpd-Runtime lokal bauen;
das bleibt jedoch ein sidecar_proxy-Pfad und kein nativer Connector.

## Connector-spezifische Guides

- [Envoy](COMPILE_ENVOY.de.md)
- [Traefik](COMPILE_TRAEFIK.de.md)
- [Lighttpd](COMPILE_LIGHTTPD.de.md)

## Nicht erlaubte Claims

Open-Connector-Evidence darf Folgendes nicht behaupten:

- `production_ready = true`
- `full_matrix_ready = true`
- `crs_complete = true`
- `response_body_verified = true`

Lighttpd-Phase-1-Evidence darf außerdem kein natives Lighttpd-Modul behaupten.
