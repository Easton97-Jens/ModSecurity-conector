<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Traefik-Betrieb

**Sprache:** [English](operations.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Start und Stop

Verwenden Sie für lokale Harnesses die passenden Make-Targets. Operatorverwaltete Services verwenden ihren eigenen Service-Manager und den Host-Config-Check.

## Logs, Rotation und Health

Nutzen Sie Host-Error-/Access-Logs und payloadfreie Connector-/Evidence-Logs. Rotieren Sie Logs mit der Hostfunktion, nicht durch Umbenennen offener Dateien. Health bedeutet Erreichbarkeit und geladene Konfiguration; es ist kein Security- oder Lifecycle-PASS.

## Timeouts und Ressourcen

Setzen Sie Host-Timeouts, Worker-/Datei-/Speicherlimits und Runtime-Roots nach den Grenzen des Zielhosts. Repository-Timeoutvariablen begrenzen Jobs, ersetzen aber keine Produktionsdimensionierung. Vermeiden Sie Secrets in Pfaden, Prozessen, Events und kanonischer Evidence.

## Diagnose und Updates

Prüfen Sie Endpoint-Erreichbarkeit, Modul-/Service-Load, Lesbarkeit der Rule-Datei, Runtime-Root-Rechte und den ausgewählten Integrationsmodus, bevor Sie ein fehlendes Ergebnis als Rule-Fehler deuten. Host-, Modul-, Patchset- und Source-Revisionen schaffen eine neue Build-/Cache-Identität; führen Sie danach den ausgewählten Evidence-Target erneut aus.
