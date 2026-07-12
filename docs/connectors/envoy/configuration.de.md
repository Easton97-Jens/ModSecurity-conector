<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Envoy-Konfiguration

**Sprache:** [English](configuration.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Konfigurationsmodell

Die ausgewählte Konfiguration streamt Request- und Response-Verarbeitung über einen `ext_proc`-gRPC-Service. `ext_authz` bleibt nur ein Kompatibilitätsbeispiel.

## Minimal, Safe und Strict

Die [annotierten Envoy-Beispiele](../../../examples/envoy/README.de.md) sind die vollständige lokale Quelle. Ersetzen Sie jeden Pfad, Port und Endpoint für den Zielhost. Minimal und Safe gehören zum dokumentierten Kern; Strict wird nur dort beschrieben, wo der Host und aktuelle Evidence es tragen. Kopieren Sie keine Kompatibilitätskonfiguration als ausgewählten Kernpfad.

## Defaults, Body-Scope und Logging

Nur vorhandene Hostdirektiven und Harness-Optionen sind in den Beispielen aufgeführt. Body- und Content-Type-Verhalten bleiben host- und profilgebunden; keine Konfiguration erlaubt einen connector-eigenen vollständigen Response-Buffer. Nutzen Sie payloadfreie Connector-/Evidence-Logs und speichern Sie keine Secrets in Regeln, Pfaden oder Kommandozeilen.

## Validierung

Führen Sie `make check-config-envoy` vor dem Start aus. Der Kernlauf `make full-lifecycle-envoy` benötigt beschreibbare Runtime- und Evidence-Roots; prüfen Sie das Ergebnis immer anhand der Artefakte.

## Konfigurationsvariablen und Platzhalter

Die Tabelle enthält nur vorhandene Eingaben oder generierte Pfade. Ein Beispielwert ist kein stiller Default; Details zu Pflicht, Scope, Auswirkung und Sicherheit stehen in der zentralen Referenz.

| Name | Pflicht | Format | Gesetzt durch | Beispielwert |
| --- | --- | --- | --- | --- |
| `ENVOY_BIN` | Optional | executable Envoy path | Provisioning or caller | `<component-cache>/envoy/bin/envoy` |
| `ENVOY_CONFIG` | Generated | absolute runtime YAML path | Harness | `<build-root>/envoy.yaml` |
| `EXT_PROC_PORT` | Optional | local TCP port number | Harness/caller | `18083` |
| `NO_CRS_RULES_FILE` | Required for canonical rule runs | absolute rules-file path | Make default or caller | `/etc/modsecurity/no-crs-baseline.conf` |

Siehe die [zentrale Variablenreferenz](../../configuration/variables.de.md).
