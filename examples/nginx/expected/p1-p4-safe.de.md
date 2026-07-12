# NGINX-P1--P4-Safe-Absicht

**Sprache:** [English](p1-p4-safe.md) | Deutsch

Die Safe-Konfiguration aktiviert das native Modul, beschränkt die
Response-Prüfung auf die genannten Content-Types und verwendet Safe für eine
späte P4-Entscheidung. Ein später Treffer verspricht keinen vom Client
gesehenen Ersatz-403. Die Referenz lässt gzip deaktiviert, damit die
untersuchte Byte-Repräsentation nicht vorausgesetzt wird.

Die Strict-Konfiguration ist nur eine vorhandene Konfigurationsform. Sie
beweist weder einen clientbeobachteten Abbruch noch einen Statuswechsel oder
vollständiges Response-Buffering.
