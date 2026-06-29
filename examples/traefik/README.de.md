# Traefik forwardAuth Beispiel

**Sprache:** [English](README.md) | Deutsch

## Inhaltsverzeichnis

- [Status](#status)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Konfigurationsdateien](#konfigurationsdateien)
- [Start- / Reload-Hinweise](#start---reload-hinweise)
- [Logs](#logs)
- [Externer Einsatz](#externer-einsatz)
- [Nicht-Claims](#nicht-claims)
- [Verwandter Compile-Guide](#verwandter-compile-guide)

## Status

Nur Beispiel. Dies belegt keine Produktionsreife. Das Repository bereitet ein
gepinntes Traefik-Release-Archiv/-Binary vor und führt einen `forwardAuth`-
Smoke-Pfad aus, wenn die erforderlichen lokalen Runtime-Komponenten vorhanden
sind. Traefik wird von diesem Repository nicht aus Source gebaut.

## Benötigte Komponenten

- Gepinntes Traefik-Binary, bereitgestellt durch `make prepare-traefik-runtime`.
- Ein erreichbarer forwardAuth-Decision-Service.
- libmodsecurity, wenn `DECISION_BACKEND=libmodsecurity` verwendet wird.
- ModSecurity-Regeln und optional CRS, wenn ein CRS-Smoke verwendet wird.

## Konfigurationsdateien

- `traefik-static.yaml`: illustrativer statischer Entry Point und File Provider.
- `traefik-dynamic.yaml`: illustrativer Router/Service/Middleware mit
  `forwardAuth`.

## Start- / Reload-Hinweise

Statische Konfigurationsänderungen erfordern einen Neustart von Traefik.
Dynamische File-Provider-Konfiguration kann von Traefik neu geladen werden,
wenn Watching aktiviert ist. Starten Sie den Authorization-Service nach Regel-,
Library- oder Backend-Änderungen neu.

## Logs

Verwenden Sie Traefik-Logs/Access-Logs plus Decision- und Audit-Logs des
Authorization-Service. Pfade hier sind illustrativ.

## Externer Einsatz

Dieses Verzeichnis enthält Beispielkonfigurationen für externen Einsatz. Sie
sind nur Startpunkte und keine universellen Produktionsdefaults. Der passende
Compile-Guide erklärt, wie das erforderliche Artefakt
`Traefik forwardAuth config` gebaut oder vorbereitet wird. Kopieren oder
adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen; Pfade wie
`/etc/...`, `/usr/lib/...`, `127.0.0.1`, Ports, Backend-URLs und Log-Pfade sind
Platzhalter, sofern sie nicht zu Ihrem System passen.

Service-Kontext: Traefik plus betreiberseitig bereitgestellter Decision-Service.
Nach dem Anpassen der Dateien Traefik für statische Konfiguration neu starten
und den betreiberseitigen Decision-Service neu starten. Traefik-Logs plus
Decision-Service-Audit-/Decision-Logs prüfen.

## Nicht-Claims

- Kein Production-Ready-Nachweis.
- Kein Full-Matrix-Nachweis.
- Kein CRS-Complete-Nachweis.
- Keine Response-Body-Verifikation.
- Kein Traefik-Source-Build-Rezept.
- Keine Go-Plugin-Implementierung.

## Verwandter Compile-Guide

Siehe [COMPILE_TRAEFIK.de.md](../../COMPILE_TRAEFIK.de.md).
