Sprache: [English](README.md) | Deutsch

# Lighttpd sidecar_proxy Beispiele

## Inhaltsverzeichnis

- [Status](#status)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Konfigurationsdateien](#konfigurationsdateien)
- [Externer Einsatz](#externer-einsatz)
- [Logs](#logs)
- [Nicht-Claims](#nicht-claims)
- [Verwandter Compile-Guide](#verwandter-compile-guide)

## Status

Dieses Verzeichnis enthält Beispiel-Konfigurationen für externen Einsatz. Sie sind Startpunkte, keine universellen Produktionsdefaults. Der passende Compile-Guide erklärt, wie `Lighttpd sidecar_proxy-Konfiguration` gebaut oder vorbereitet wird.

## Benötigte Komponenten

Lighttpd, Sidecar/Decision-Backend, optional libmodsecurity, Regeln/CRS, Logs. Pfade, Ports, Backend-Adressen und Log-Ziele sind Platzhalter und müssen an die Umgebung angepasst werden.

## Konfigurationsdateien

lighttpd-sidecar-proxy.conf. Konfigurationsdateien bleiben sprachneutral; technische Direktiven wie `modsecurity on`, `load_module`, `forwardAuth`, `ext_authz` und `sidecar_proxy` werden nicht übersetzt.

## Externer Einsatz

Kopieren oder adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen. Lighttpd-Konfiguration prüfen/starten; Sidecar/Decision-Backend vom Betreiber starten/restarten. GitHub zeigt weiterhin alle Dateien im Repository-Baum; diese Links halten Sie in der deutschen Dokumentationssprache.

## Logs

Prüfen Sie Lighttpd Logs und Sidecar Audit/Decision Logs. Beispielpfade sind Platzhalter und keine Pflichtpfade.

## Nicht-Claims

- Kein nativer Lighttpd-ModSecurity-Connector.
- Nicht production-ready.
- FastCGI/SCGI/mod_magnet/Lua sind nicht implementiert.

## Verwandter Compile-Guide

Siehe [COMPILE_LIGHTTPD.de.md](../../COMPILE_LIGHTTPD.de.md).
