Sprache: [English](README.md) | Deutsch

# Envoy ext_authz Beispiele

## Inhaltsverzeichnis

- [Status](#status)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Konfigurationsdateien](#konfigurationsdateien)
- [Externer Einsatz](#externer-einsatz)
- [Logs](#logs)
- [Nicht-Claims](#nicht-claims)
- [Verwandter Compile-Guide](#verwandter-compile-guide)

## Status

Dieses Verzeichnis enthält Beispiel-Konfigurationen für externen Einsatz. Sie sind Startpunkte, keine universellen Produktionsdefaults. Der passende Compile-Guide erklärt, wie `Envoy ext_authz-Konfiguration` gebaut oder vorbereitet wird.

## Benötigte Komponenten

Envoy-Binary, ext_authz Auth-Service/Sidecar, optional libmodsecurity, Regeln/CRS, Logs. Pfade, Ports, Backend-Adressen und Log-Ziele sind Platzhalter und müssen an die Umgebung angepasst werden.

## Konfigurationsdateien

envoy-ext-authz.yaml. Konfigurationsdateien bleiben sprachneutral; technische Direktiven wie `modsecurity on`, `load_module`, `forwardAuth`, `ext_authz` und `sidecar_proxy` werden nicht übersetzt.

## Externer Einsatz

Kopieren oder adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen. Envoy-Konfiguration validieren/starten; Auth-Service vom Betreiber starten/restarten. GitHub zeigt weiterhin alle Dateien im Repository-Baum; diese Links halten Sie in der deutschen Dokumentationssprache.

## Logs

Prüfen Sie Envoy Logs und Auth-Service Decision/Audit Logs. Beispielpfade sind Platzhalter und keine Pflichtpfade.

## Nicht-Claims

- Envoy wird hier nicht aus Source kompiliert.
- Nicht production-ready.
- Kein vollständiger Produktions-Auth-Service enthalten.

## Verwandter Compile-Guide

Siehe [COMPILE_ENVOY.de.md](../../COMPILE_ENVOY.de.md).
