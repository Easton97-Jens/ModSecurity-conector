<!-- Generated from scripts/generate_current_documentation.py; do not edit directly. -->

# Erweiterter Katalog

**Sprache:** [English](extended-catalog.md) | Deutsch

## Geltungsbereich

Der erweiterte Katalog ist vom ausgewählten Kern getrennt. `NOT EXECUTED`, `BLOCKED` und `UNSUPPORTED` sind Evidence-Zustände, keine PASS-Werte und keine versteckten Fehler.

Der erweiterte Katalog ist vom ausgewählten Kern getrennt. `NOT EXECUTED`, `BLOCKED` und `UNSUPPORTED` sind Evidence-Zustände, keine PASS-Werte und keine versteckten Fehler.

Dieser Leitfaden beschreibt den aktuellen ausgewählten Sechs-Connector-HTTP/1.1-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Variablen und Pfade

Wiederkehrende Werte wie `BUILD_ROOT`, `CACHE_ROOT`, `EVIDENCE_ROOT`, `FRAMEWORK_ROOT` und `NO_CRS_RUN_ID` stehen in der [zentralen Variablenreferenz](../configuration/variables.de.md). Repository-relative Pfade beginnen am Repository-Root; Lauf-, Cache- und Evidence-Pfade liegen außerhalb des Git-Worktrees.

## Status- und Exit-Werte

`PASS` bedeutet einen erfüllten geprüften Anspruch; `FAIL` einen negativen Prüfbefund; `BLOCKED` eine fehlende Voraussetzung; `NOT EXECUTED` keine Ausführung; `NOT APPLICABLE` keine Anwendbarkeit; `UNSUPPORTED` keine vom Host angebotene Fähigkeit. Prozesscode `0` bedeutet technische Beendigung, `1` allgemeinen Fehler, `2` Validierungs-/Aggregate-Fehler und `77` eine deklarierte fehlende optionale Voraussetzung.

## Validierung

Führe das dokumentierte Make-Target vom Repository-Root aus und bewahre die erzeugte Evidence-Grenze mit dem Ergebnis auf.
