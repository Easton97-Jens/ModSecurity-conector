<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# NGINX-Lifecycle

**Sprache:** [English](lifecycle.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Phasen und EOS

| Phase | Bedeutung |
| --- | --- |
| P1 | Request-Header |
| P2 | Request-Body; Abschluss an Request-EOS |
| P3 | Response-Header |
| P4 | Response-Body; Abschluss an Response-EOS |

## Pre-Commit und Post-Commit

Vor dem Response-Commit darf ein Host eine unterstützte Pre-Commit-Aktion anwenden. Nach dem Commit protokolliert Safe `log_only`; Safe behauptet keinen umgeschriebenen sichtbaren Status. Strict ist eine separate Hostfähigkeit. Die ausgewählte Evidence dokumentiert Safe-Post-Commit-Semantik ohne eine umgeschriebene Response nach dem Commit zu behaupten.

## First Byte, Buffering und Cleanup

Die ausgewählte Evidence verlangt, wo anwendbar, eine First-Byte-vor-EOS-Beobachtung und verbietet einen connector-eigenen Full-Response-Buffer. Lifecycle-Counter, Events und Cleanup müssen derselben Transaktion zurechenbar sein.
