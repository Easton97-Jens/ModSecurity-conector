# Traefik-P1--P4-Safe-Absicht

**Sprache:** [English](p1-p4-safe.md) | Deutsch

Die native Local-Plugin-Referenz verwendet engineMode uds und einen privaten
lokalen Engine-Socket. Ihre Service-Konfiguration wählt gestreamte Body-Modi
und phase4_mode safe. Ein P4-Ergebnis nach dem Commit soll Safe-Log-only
bleiben; es ist kein behaupteter Response-Wechsel oder Strict-
Verbindungsabbruch.

Die forwardAuth-Dateien sind Request-only-Kompatibilitätsmaterial. Sie dürfen
nicht zur Beschreibung von P3/P4-Abdeckung benutzt werden. Das
[Strict-Verzeichnis](../strict/README.de.md) dokumentiert die optionale Grenze;
es ist kein Host-Abbruch-Anspruch.
