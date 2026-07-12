# lighttpd-P1--P4-Safe-Absicht

**Sprache:** [English](p1-p4-safe.md) | Deutsch

Die Safe-Referenz ist auf den passenden gepatchten nativen lighttpd-1.4.84-
Host und Identity-HTTP/1.1-Entity-Daten über mod_proxy begrenzt. Sie wählt
gestreamte Body-Modi und phase4_mode safe. Sie aktiviert weder komprimierte
Entities noch behauptet sie HTTP/2-, HTTP/3-, File- oder Zero-Copy-
Response-Prüfung.

Eine späte P4-Entscheidung ist eine Safe-Log-only-Grenze, kein behaupteter
sichtbarer 403 oder Strict-Abbruch. Die minimale Stock-Referenz lässt Bodies
deaktiviert. Es gibt kein Strict-Beispiel.
