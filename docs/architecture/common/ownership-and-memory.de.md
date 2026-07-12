<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Ownership und Speicher

**Sprache:** [English](ownership-and-memory.md) | Deutsch

## Geltungsbereich

Adapter besitzen Host-Referenzen, Pools, Allokatoren und Callback-Lebensdauer. Common erhält validierte neutrale Werte und gibt nur Speicher frei, den es selbst allokiert hat.

Ein geliehener Body-Chunk darf seinen Host-Callback nicht überleben; kein Evidence-Schreiber darf ihn behalten oder serialisieren.

Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Variablen und Pfade

Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz](../../configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees.

## Validierung

Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.
