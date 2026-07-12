<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# HAProxy-Konfiguration

**Sprache:** [English](configuration.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Konfigurationsmodell

Der ausgewählte Full-Lifecycle-Pfad ist der native HTX-Filter. Er ist nicht das historische SPOE/SPOP-Kompatibilitätsbeispiel.

## Minimal, Safe und Strict

Die [annotierten HAProxy-Beispiele](../../../examples/haproxy/README.de.md) sind die vollständige lokale Quelle. Ersetzen Sie jeden Pfad, Port und Endpoint für den Zielhost. Minimal und Safe gehören zum dokumentierten Kern; Strict wird nur dort beschrieben, wo der Host und aktuelle Evidence es tragen. Kopieren Sie keine Kompatibilitätskonfiguration als ausgewählten Kernpfad.

## Defaults, Body-Scope und Logging

Nur vorhandene Hostdirektiven und Harness-Optionen sind in den Beispielen aufgeführt. Body- und Content-Type-Verhalten bleiben host- und profilgebunden; keine Konfiguration erlaubt einen connector-eigenen vollständigen Response-Buffer. Nutzen Sie payloadfreie Connector-/Evidence-Logs und speichern Sie keine Secrets in Regeln, Pfaden oder Kommandozeilen.

## Validierung

Führen Sie `make check-config-haproxy` vor dem Start aus. Der Kernlauf `make full-lifecycle-haproxy` benötigt beschreibbare Runtime- und Evidence-Roots; prüfen Sie das Ergebnis immer anhand der Artefakte.

## Konfigurationsvariablen und Platzhalter

Die Tabelle enthält nur vorhandene Eingaben oder generierte Pfade. Ein Beispielwert ist kein stiller Default; Details zu Pflicht, Scope, Auswirkung und Sicherheit stehen in der zentralen Referenz.

| Name | Pflicht | Format | Gesetzt durch | Beispielwert |
| --- | --- | --- | --- | --- |
| `HAPROXY_VERSION` | Optional | selected host version | Framework/provider pin or caller | `the current provider pin` |
| `HAPROXY_SOURCE_URL` | Optional | HTTPS archive URL | Framework/provider pin or caller | `pinned source URL` |
| `HAPROXY_SHA256` | Optional | 64-character SHA-256 | Framework/provider pin or caller | `pinned digest` |
| `HAPROXY_RUNTIME_BUILD_DIR` | Optional | absolute build directory | Provisioning | `<build-root>/haproxy-runtime` |

Siehe die [zentrale Variablenreferenz](../../configuration/variables.de.md).
