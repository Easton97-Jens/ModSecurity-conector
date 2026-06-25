Sprache: [English](README.md) | Deutsch

# Traefik forwardAuth Beispiele

## Inhaltsverzeichnis

- [Status](#status)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Konfigurationsdateien](#konfigurationsdateien)
- [Externer Einsatz](#externer-einsatz)
- [Logs](#logs)
- [Nicht-Claims](#nicht-claims)
- [Verwandter Compile-Guide](#verwandter-compile-guide)

## Status

Dieses Verzeichnis enthält Beispiel-Konfigurationen für externen Einsatz. Sie sind Startpunkte, keine universellen Produktionsdefaults. Der passende Compile-Guide erklärt, wie `Traefik forwardAuth-Konfiguration` gebaut oder vorbereitet wird.

## Benötigte Komponenten

Traefik-Binary, Decision-Service, optional libmodsecurity, Regeln/CRS, Logs. Pfade, Ports, Backend-Adressen und Log-Ziele sind Platzhalter und müssen an die Umgebung angepasst werden.

## Konfigurationsdateien

traefik-static.yaml, traefik-dynamic.yaml. Konfigurationsdateien bleiben sprachneutral; technische Direktiven wie `modsecurity on`, `load_module`, `forwardAuth`, `ext_authz` und `sidecar_proxy` werden nicht übersetzt.

## Externer Einsatz

Kopieren oder adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen. Traefik neu starten oder dynamische Konfiguration neu laden; Decision-Service vom Betreiber starten/restarten. GitHub zeigt weiterhin alle Dateien im Repository-Baum; diese Links halten Sie in der deutschen Dokumentationssprache.

## Logs

Prüfen Sie Traefik Logs und Decision-Service Audit/Decision Logs. Beispielpfade sind Platzhalter und keine Pflichtpfade.

## Nicht-Claims

- Traefik wird hier nicht aus Source kompiliert.
- Nicht production-ready.
- Keine Go-Plugin-Implementierung.

## Verwandter Compile-Guide

Siehe [COMPILE_TRAEFIK.de.md](../../COMPILE_TRAEFIK.de.md).
