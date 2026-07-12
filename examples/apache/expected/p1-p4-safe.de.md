# Apache-P1--P4-Safe-Absicht

**Sprache:** [English](p1-p4-safe.md) | Deutsch

Die Safe-Referenz konfiguriert die Verarbeitung des nativen httpd-Moduls für
P1 bis P4 und begrenzt den Response-Body-Input auf 1048576 Bytes. Eine
P4-Entscheidung nach dem Response-Commit soll als Safe-Log-only behandelt
werden; ohne passende Host-Evidence darf sie nicht als sichtbarer HTTP-403
dokumentiert werden.

Diese Datei beschreibt Konfigurationsabsicht, kein Laufergebnis. Der native
Pfad verspricht weder Regelbewertung pro Chunk noch einen vollständigen
Connector-Response-Buffer oder einen Strict-Abbruch nach dem Commit. Dafür
gibt es hier kein Strict-Beispiel.
