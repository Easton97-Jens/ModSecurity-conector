<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Runtime-Vertrag

**Sprache:** [English](runtime.md) | Deutsch

## Geltungsbereich

Runtime-Roots sind explizit und außerhalb des Checkouts. Cache-v2 ist nur bei passenden Identity-Eingaben wiederverwendbar; Build-, Log- und Evidence-Roots sind lauflokal.

Verwende `BUILD_ROOT`, `CACHE_ROOT` und `EVIDENCE_ROOT` über Make-Targets; Defaults und Sicherheitsregeln sind zentral dokumentiert.

Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Variablen und Pfade

Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz](../../configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees.

## Validierung

Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.
