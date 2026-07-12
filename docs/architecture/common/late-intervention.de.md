<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Späte Intervention

**Sprache:** [English](late-intervention.md) | Deutsch

## Geltungsbereich

Vor dem Commit kann ein Host eine unterstützte Deny-Aktion anwenden. Nach dem Commit zeichnet der Safe-Modus ein `log_only`-Ergebnis auf; es darf nicht als umgeschriebener Client-Status dargestellt werden.

Strict-Verhalten ist eine getrennte Host-Capability und wird nicht für jeden Connector behauptet.

Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Variablen und Pfade

Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz](../../configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees.

## Validierung

Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.
