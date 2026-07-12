<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Transaktions-Lifecycle

**Sprache:** [English](transactions.md) | Deutsch

## Geltungsbereich

P1 verarbeitet Request-Header, P2 verarbeitet den Request-Body und endet bei Request-EOS, P3 verarbeitet Response-Header und P4 erhält Response-Body-Chunks und endet bei Response-EOS.

Append und Finish sind getrennte Operationen. Ein Chunk wird während des Forwardings geliehen; EOS führt die einmalig geschützte Finalisierung für diese Body-Richtung aus.

Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Variablen und Pfade

Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz](../../configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees.

## Validierung

Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.
