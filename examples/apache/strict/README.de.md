# Apache-Strict-Profilgrenze

**Sprache:** [English](README.md) | Deutsch

## Status

`modsecurity_phase4_mode strict` wird vom Parser unterstützt, aber dieses
Repository besitzt keinen Apache-Hostnachweis für einen client-sichtbaren
späten Abbruch. Strict ist deshalb optional und enthält hier absichtlich keine
ausführbare Konfiguration.

## Verwendung

Von `../safe/httpd.conf` ausgehen, `modsecurity_phase4_mode strict` setzen,
mit `apachectl -t` validieren und host-spezifische Evidenz erfassen, bevor auf
eine Post-Commit-Aktion vertraut wird.
