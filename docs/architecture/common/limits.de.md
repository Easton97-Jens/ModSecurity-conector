<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Limits und Buffering

**Sprache:** [English](limits.md) | Deutsch

## Geltungsbereich

Der ausgewählte Kern erlaubt keinen connector-eigenen vollständigen Response-Buffer. Hosts können eigene begrenzte Einrichtungen verwenden, aber Evidence beschreibt die beobachtete Grenze statt sie anzunehmen.

Konfiguriere nur vorhandene Host-Controls und zeichne ihre effektive Konfiguration als Hashes oder sichere Metadaten auf.

Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Variablen und Pfade

Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz](../../configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees.

## Validierung

Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.
