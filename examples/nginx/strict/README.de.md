# NGINX-Strict-Profilgrenze

**Sprache:** [English](README.md) | Deutsch

## Status

[nginx.conf](nginx.conf) ist eine parserunterstützte Strict-
Konfigurationsform. Sie behauptet keinen sichtbaren späten Statuswechsel;
Post-Commit-Strict-Verhalten muss gegen den installierten NGINX-Host validiert
werden.

## Verwendung

Pfade und Endpunkte anpassen, `nginx -t` ausführen und einen Abbruch als
host-spezifisches Ergebnis statt als garantierte spätere 403 behandeln.
