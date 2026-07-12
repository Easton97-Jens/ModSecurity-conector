<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Event- und Evidence-Vertrag

**Sprache:** [English](events.md) | Deutsch

## Geltungsbereich

Events tragen begrenzte Metadaten wie Phase, Rule-ID, Message-ID, Aktion, Commit-Status und Lifecycle-Zähler. Sie dürfen keine Request- oder Response-Payloads tragen.

Ein Result und ein Event sind unterschiedliche Evidence-Datensätze; ein Result allein darf kein kausales Host-Event ableiten.

Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Variablen und Pfade

Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz](../../configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees.

## Validierung

Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.
