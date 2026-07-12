# Haproxy-DetectionOnly-Profil

**Sprache:** [English](README.md) | Deutsch

## Verhalten

`detection-only/haproxy-htx.cfg` lässt den nativen HTX-Filter aktiv und wählt die DetectionOnly-Regeldatei. DetectionOnly lädt und bewertet Engine-Regeln und
zeichnet Treffer auf, führt aber keine disruptiven Engine-Aktionen aus.

## Validierung

Nach dem Anpassen der Hostpfade den im übergeordneten README genannten
Connector-Validierungsbefehl verwenden. Dieses Profil ist
Konfigurationsanleitung und keine Runtime-Evidenz.
