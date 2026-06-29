# Envoy ext_authz Beispiel

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

Nur Beispiel. Dies belegt keine Produktionsreife. Das Repository bereitet eine
gepinnte Envoy-Runtime-Komponente vor und führt einen `ext_authz`-Smoke-Pfad
aus, wenn die erforderlichen lokalen Runtime-Komponenten vorhanden sind. Envoy
wird von diesem Repository nicht aus Source gebaut.

## Benötigte Komponenten

- Gepinntes Envoy-Binary, bereitgestellt durch `make prepare-envoy-runtime`.
- Ein `ext_authz`-Authorization-Service oder Sidecar-Pfad.
- libmodsecurity, wenn `DECISION_BACKEND=libmodsecurity` verwendet wird.
- ModSecurity-Regeln und optional CRS, wenn ein CRS-Smoke verwendet wird.

## Konfigurationsdateien

- `envoy-ext-authz.yaml`: illustrative Envoy-Listener-, Route- und
  `ext_authz`-Filter-Verdrahtung.

## Start- / Reload-Hinweise

Validieren Sie die Konfiguration mit dem bereitgestellten Envoy-Binary, bevor
Sie sie ausführen. Starten Sie Envoy nach statischen Konfigurationsänderungen je
nach Process Manager des Betreibers neu oder per Hot Restart. Starten Sie den
Authorization-Service nach Regel-, Library- oder Backend-Änderungen neu.

## Logs

Verwenden Sie Envoy-Access-/Runtime-Logs plus Decision- und Audit-Logs des
Authorization-Service. Pfade in diesem Verzeichnis sind illustrativ und sollten
durch deployment-lokale Pfade ersetzt werden.

## Externer Einsatz

Dieses Verzeichnis enthält Beispielkonfigurationen für externen Einsatz. Sie
sind nur Startpunkte und keine universellen Produktionsdefaults. Der passende
Compile-Guide erklärt, wie das erforderliche Artefakt `Envoy ext_authz config`
gebaut oder vorbereitet wird. Kopieren oder adaptieren Sie nur die Dateien, die
zu Ihrem Deployment passen; Pfade wie `/etc/...`, `/usr/lib/...`, `127.0.0.1`,
Ports, Backend-URLs und Log-Pfade sind Platzhalter, sofern sie nicht zu Ihrem
System passen.

Service-Kontext: Envoy plus betreiberseitig bereitgestellter Auth-Service. Nach
dem Anpassen der Dateien Envoy validieren/restarten und den betreiberseitigen
Auth-Service neu starten. Envoy-Logs plus Auth-Service-Decision-/Audit-Logs
prüfen.

## Nicht-Claims

- Kein Production-Ready-Nachweis.
- Kein Full-Matrix-Nachweis.
- Kein CRS-Complete-Nachweis.
- Keine Response-Body-Verifikation.
- Kein Envoy-Source-Build-Rezept.

## Verwandter Compile-Guide

Siehe [COMPILE_ENVOY.de.md](../../COMPILE_ENVOY.de.md).
