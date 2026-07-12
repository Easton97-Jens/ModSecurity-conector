# lighttpd-Strict-Profilgrenze

**Sprache:** [English](README.md) | Deutsch

## Status

Common Runtime akzeptiert `phase4_mode=strict`, aber das native lighttpd-Modul
implementiert keinen strikten Transportabbruch. Strict ist optional und es
wird kein ausführbares striktes Hostprofil geliefert.

## Verwendung

Das passende Host-/Modulpaar und die Common-Runtime-Konfiguration validieren,
bevor ein strikter Wert getestet wird; ihn nicht als implementierten
Client-Abbruch beschreiben.
