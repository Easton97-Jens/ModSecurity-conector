# Lighttpd sidecar_proxy Beispiel

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

Nur Beispiel. Dies belegt keine Produktionsreife. Der aktuelle Repository-Pfad
ist `sidecar_proxy` / Phase 1. Dieses Repository stellt keine native
Lighttpd-ModSecurity-Integration bereit.

## Benötigte Komponenten

- Lighttpd-Binary, aus dem gepinnten Source-Tarball gebaut durch
  `ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build`.
- Ein erreichbarer ModSecurity-Sidecar/Proxy oder Decision-Backend.
- libmodsecurity, wenn `DECISION_BACKEND=libmodsecurity` verwendet wird.
- ModSecurity-Regeln und optional CRS, wenn ein CRS-Smoke verwendet wird.

## Konfigurationsdateien

- `lighttpd-sidecar-proxy.conf`: illustrative Lighttpd-Frontend-/Proxy-
  Verdrahtung zu einem Application Backend. Der ModSecurity-Sidecar-Pfad ist
  als extern beschrieben; es wird kein natives Modul geladen.

## Start- / Reload-Hinweise

Validieren Sie die Lighttpd-Konfiguration mit dem bereitgestellten Binary,
bevor Sie sie ausführen. Starten oder reloaden Sie Lighttpd nach
Konfigurationsänderungen entsprechend der lokalen Process-Management-Policy.
Starten Sie den Sidecar nach Regel-, Library- oder Backend-Änderungen neu.

## Logs

Verwenden Sie Lighttpd-Access-/Error-Logs plus Sidecar-Decision- und
Audit-Logs. Pfade hier sind illustrativ.

## Externer Einsatz

Dieses Verzeichnis enthält Beispielkonfigurationen für externen Einsatz. Sie
sind nur Startpunkte und keine universellen Produktionsdefaults. Der passende
Compile-Guide erklärt, wie das erforderliche Artefakt
`Lighttpd sidecar_proxy config` gebaut oder vorbereitet wird. Kopieren oder
adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen; Pfade wie
`/etc/...`, `/usr/lib/...`, `127.0.0.1`, Ports, Backend-URLs und Log-Pfade sind
Platzhalter, sofern sie nicht zu Ihrem System passen.

Service-Kontext: Lighttpd plus betreiberseitig bereitgestellter
Sidecar/Decision-Backend. Nach dem Anpassen der Dateien Lighttpd
validieren/reloaden und den Sidecar/das Decision-Backend neu starten.
Lighttpd-Logs plus Sidecar-Audit-/Decision-Logs prüfen.

## Nicht-Claims

- Kein Production-Ready-Nachweis.
- Kein natives Lighttpd-ModSecurity-Modul.
- Keine FastCGI-/SCGI-Integration.
- Keine mod_magnet-/Lua-Integration.
- Kein Full-Matrix-, CRS-Complete- oder Response-Body-Nachweis.

## Verwandter Compile-Guide

Siehe [COMPILE_LIGHTTPD.de.md](../../COMPILE_LIGHTTPD.de.md).
