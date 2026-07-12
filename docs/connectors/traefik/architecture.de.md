<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Traefik-Architektur

**Sprache:** [English](architecture.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Hostintegration

native Traefik-Middleware und lokaler Engine-Service. Common erhält nur neutral gemappte Werte; Host-APIs, Speicherallokation und Callback-Lebensdauer bleiben außerhalb von Common.

## Transaktions-Lifecycle

| Phase | Bedeutung |
| --- | --- |
| P1 | Request-Header vor dem Upstream-Request |
| P2 | Request-Body; Abschluss an Request-EOS |
| P3 | Response-Header |
| P4 | Response-Body; Abschluss an Response-EOS |

## Datenfluss und Engine-Anbindung

Die Adapter geben geliehene Header- und Body-Abschnitte an Common weiter. Common ruft die Engine über seine neutrale Schnittstelle auf; Host-spezifische Typen, Puffer und Callbacks werden nicht in Common übertragen.

## Ownership und Lifetime

Body-Chunks werden nicht connector-eigen vollständig gepuffert. Events und Reports speichern keine Roh-Request- oder Response-Bodies. Adapter-Cleanup folgt dem Ende des Host-Lifecycles und bleibt der gleichen Transaktion zurechenbar.
