<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# HAProxy-Connector

**Sprache:** [English](README.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Ausgewählter Integrationsmodus

`native-htx-filter` — nativer HAProxy-HTX-Filter mit dem Repository-Overlay.

## Aktueller Kern

HTTP/1.1 P1–P4 mit Safe-Post-Commit-Phase-4-Semantik, First-Byte-vor-EOS-Evidence und ohne connector-eigenen vollständigen Response-Buffer.

## Schnelllinks

- [Architektur](architecture.de.md)
- [Build](build.de.md)
- [Konfiguration](configuration.de.md)
- [Lifecycle](lifecycle.de.md)
- [Tests](testing.de.md)
- [Betrieb](operations.de.md)
- [Grenzen](limitations.de.md)
