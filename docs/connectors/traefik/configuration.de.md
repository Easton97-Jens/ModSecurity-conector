<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Traefik-Konfiguration

**Sprache:** [English](configuration.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Konfigurationsmodell

Der ausgewählte Pfad verwendet EntryPoint, Router, native Middleware und lokalen Engine-Service. `forwardAuth` bleibt ein Kompatibilitätsbeispiel.

## Minimal, Safe und Strict

Die [annotierten Traefik-Beispiele](../../../examples/traefik/README.de.md) sind die vollständige lokale Quelle. Ersetzen Sie jeden Pfad, Port und Endpoint für den Zielhost. Minimal und Safe gehören zum dokumentierten Kern; Strict wird nur dort beschrieben, wo der Host und aktuelle Evidence es tragen. Kopieren Sie keine Kompatibilitätskonfiguration als ausgewählten Kernpfad.

## Defaults, Body-Scope und Logging

Nur vorhandene Hostdirektiven und Harness-Optionen sind in den Beispielen aufgeführt. Body- und Content-Type-Verhalten bleiben host- und profilgebunden; keine Konfiguration erlaubt einen connector-eigenen vollständigen Response-Buffer. Nutzen Sie payloadfreie Connector-/Evidence-Logs und speichern Sie keine Secrets in Regeln, Pfaden oder Kommandozeilen.

## Validierung

Führen Sie `make check-config-traefik` vor dem Start aus. Der Kernlauf `make full-lifecycle-traefik` benötigt beschreibbare Runtime- und Evidence-Roots; prüfen Sie das Ergebnis immer anhand der Artefakte.

## Konfigurationsvariablen und Platzhalter

Die Tabelle enthält nur vorhandene Eingaben oder generierte Pfade. Ein Beispielwert ist kein stiller Default; Details zu Pflicht, Scope, Auswirkung und Sicherheit stehen in der zentralen Referenz.

| Name | Pflicht | Format | Gesetzt durch | Beispielwert |
| --- | --- | --- | --- | --- |
| `TRAEFIK_BIN` | Optional | executable Traefik path | Provisioning or caller | `<component-cache>/traefik/bin/traefik` |
| `TRAEFIK_ENGINE_SERVICE_BUILD_DIR` | Optional | absolute build directory | Build script or caller | `<build-root>/traefik-engine-service` |
| `TRAEFIK_ENGINE_SERVICE_BIN` | Optional | absolute engine-service executable | Build script or caller | `<build-root>/traefik-engine-service/traefik-engine-service` |
| `TRAEFIK_CONNECTOR_CONFIG` | Optional | absolute connector configuration | Start-smoke harness or caller | `config/traefik-forwardauth.conf` |

Siehe die [zentrale Variablenreferenz](../../configuration/variables.de.md).
