Sprache: [English](README.md) | Deutsch

# HAProxy ModSecurity Beispiele

## Inhaltsverzeichnis

- [Status](#status)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Konfigurationsdateien](#konfigurationsdateien)
- [Externer Einsatz](#externer-einsatz)
- [Logs](#logs)
- [Nicht-Claims](#nicht-claims)
- [Verwandter Compile-Guide](#verwandter-compile-guide)

## Status

Dieses Verzeichnis enthält Beispiel-Konfigurationen für externen Einsatz. Sie sind Startpunkte, keine universellen Produktionsdefaults. Der passende Compile-Guide erklärt, wie `haproxy-modsecurity-spoa` gebaut oder vorbereitet wird.

## Benötigte Komponenten

HAProxy, SPOE/SPOP, SPOA-Prozess, libmodsecurity v3, Regeln/CRS optional, Logs. Pfade, Ports, Backend-Adressen und Log-Ziele sind Platzhalter und müssen an die Umgebung angepasst werden.

## Konfigurationsdateien

haproxy-request-only.cfg, spoe-modsecurity.conf, modsecurity-agent.conf. Konfigurationsdateien bleiben sprachneutral; technische Direktiven wie `modsecurity on`, `load_module`, `forwardAuth`, `ext_authz` und `sidecar_proxy` werden nicht übersetzt.

## Externer Einsatz

Kopieren oder adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen. HAProxy mit `haproxy -c` prüfen und neu laden; SPOA-Prozess vom Betreiber neu starten. GitHub zeigt weiterhin alle Dateien im Repository-Baum; diese Links halten Sie in der deutschen Dokumentationssprache.

## Logs

Prüfen Sie HAProxy Logs, decision.jsonl, audit.log und Agent Logs. Beispielpfade sind Platzhalter und keine Pflichtpfade.

## Nicht-Claims

- Keine repository-eigene systemd-Unit.
- RESPONSE_BODY / Phase 4 bleibt nicht promoted.
- Force-all-FAIL-Zeilen sind kein Produktionssupport.

## Verwandter Compile-Guide

Siehe [COMPILE_HAPROXY.de.md](../../COMPILE_HAPROXY.de.md).
