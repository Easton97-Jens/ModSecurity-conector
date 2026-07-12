# HAProxy-P1--P4-Safe-Absicht

**Sprache:** [English](p1-p4-safe.md) | Deutsch

Die native HTX-Safe-Referenz wählt phase4-mode safe. Sie ist für den
gepatchten nativen Filterpfad gedacht, nicht für den SPOE/SPOP-
Kompatibilitätsservice. Eine P4-Entscheidung nach dem Beginn einer Response
wird als Safe-Log-only aufgezeichnet; die Konfiguration verspricht keinen
Statuswechsel und keinen Strict-Abbruch.

Die Minimal-Referenz zeigt den parser-unterstützten minimal-Modus. Es gibt kein
Strict-Beispiel, weil eine eingecheckte Filteroption keinen
clientbeobachteten Abbruch nach dem Commit beweist.
