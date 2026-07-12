<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# NGINX-Grenzen

**Sprache:** [English](limitations.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Grenzen

Strict ist eine separate Hostfähigkeit. Die ausgewählte Evidence dokumentiert Safe-Post-Commit-Semantik ohne eine umgeschriebene Response nach dem Commit zu behaupten.

## Nicht durch diesen Leitfaden abgedeckt

Strict-Transport-Enforcement über die ausgewählte Evidence hinaus, vollständige HTTP/2- oder HTTP/3-Verifikation, CRS-Verifikation, vollständige Extended-Matrix-Ausführung, Kompressionsverhalten und Produktionsreife bleiben getrennte Arbeit.

## Kompatibilitätspfade

Kompatibilitätskonfigurationen liegen getrennt unter `examples/` und dürfen nicht als ausgewählter Full-Lifecycle-Beweis zitiert werden.
