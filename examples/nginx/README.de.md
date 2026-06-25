Sprache: [English](README.md) | Deutsch

# NGINX ModSecurity Beispiele

## Inhaltsverzeichnis

- [Status](#status)
- [Benötigte Komponenten](#benötigte-komponenten)
- [Konfigurationsdateien](#konfigurationsdateien)
- [Externer Einsatz](#externer-einsatz)
- [Logs](#logs)
- [Nicht-Claims](#nicht-claims)
- [Verwandter Compile-Guide](#verwandter-compile-guide)

## Status

Dieses Verzeichnis enthält Beispiel-Konfigurationen für externen Einsatz. Sie sind Startpunkte, keine universellen Produktionsdefaults. Der passende Compile-Guide erklärt, wie `ngx_http_modsecurity_module.so` gebaut oder vorbereitet wird.

## Benötigte Komponenten

NGINX mit passender ABI, libmodsecurity v3, Regeln/CRS optional, Logs. Pfade, Ports, Backend-Adressen und Log-Ziele sind Platzhalter und müssen an die Umgebung angepasst werden.

## Konfigurationsdateien

nginx-modsecurity-request-only.conf, modsecurity-request-only.conf, optional Phase-4-Beispiele. Konfigurationsdateien bleiben sprachneutral; technische Direktiven wie `modsecurity on`, `load_module`, `forwardAuth`, `ext_authz` und `sidecar_proxy` werden nicht übersetzt.

## Externer Einsatz

Kopieren oder adaptieren Sie nur die Dateien, die zu Ihrem Deployment passen. NGINX mit `nginx -t` prüfen und neu laden; Modulwechsel kann Neustart erfordern. GitHub zeigt weiterhin alle Dateien im Repository-Baum; diese Links halten Sie in der deutschen Dokumentationssprache.

## Logs

Prüfen Sie NGINX Access/Error Logs und ModSecurity Audit Log. Beispielpfade sind Platzhalter und keine Pflichtpfade.

## Nicht-Claims

- Nicht als universelle Produktionsdefaults.
- NGINX-Modul muss zur ABI passen.
- RESPONSE_BODY / Phase 4 bleibt nicht promoted.

## Verwandter Compile-Guide

Siehe [COMPILE_NGINX.de.md](../../COMPILE_NGINX.de.md).
