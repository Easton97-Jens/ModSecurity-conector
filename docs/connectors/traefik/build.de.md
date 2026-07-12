<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# Traefik-Build

**Sprache:** [English](build.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Buildpfad und Hostversion

`make build-traefik` und `make check-config-traefik` bereiten den nativen Middleware-Pfad vor.

Die maßgebliche Hostversion ist die Version der aktuellen vorbereiteten Runtime oder ihres gepinnten Provisionierungsinputs. Eine dokumentierte Version ist keine Aussage über jede Distribution, ABI oder Betriebsumgebung.

## Toolchain und Abhängigkeiten

Benötigt werden der zum Host passende C/C++- bzw. Go-Toolchainpfad, libmodsecurity-Abhängigkeiten und ein beschreibbarer Build-/Cache-Root außerhalb des Checkouts. Compiler, Flags und Hostrevisionen werden als Build-Provenance festgehalten; dieser Leitfaden behauptet keine universelle Compiler- oder Go-Version.

## Cache-v2 und Provenienz

Die Wiederverwendung von Cache-v2 ist identitätsgebunden. Source-URL, Revision oder Digest, Patchset, Architektur, Compiler und Konfiguration bestimmen, ob ein Cache-Eintrag wiederverwendbar ist. Ein Cache-Treffer ist kein Runtime-PASS.

## Build, Config und Runtime

Führen Sie `make build-traefik` und danach `make check-config-traefik` aus. Start- und Runtime-Smokes existieren nur für die jeweils angebotenen Targetfamilien; der ausgewählte Kernlauf ist `make full-lifecycle-traefik`. Erfolgreicher Build oder Config-Check ist kein Rule-Engine-PASS.

## Optionale Profile und Fehlerdiagnose

Kompatibilitäts-, CRS-, erweitertes Matrix-, H2/H3- und Strict-Profile sind getrennt vom ausgewählten Kern. Prüfen Sie bei Fehlern Executable-Pfade, ABI, Modul-/Service-Load, beschreibbare Runtime-Roots sowie gepinnte Source-/Patch-Eingaben, bevor Sie Konfiguration ändern.

## Konfigurationsvariablen und Platzhalter

Die Tabelle enthält nur vorhandene Eingaben oder generierte Pfade. Ein Beispielwert ist kein stiller Default; Details zu Pflicht, Scope, Auswirkung und Sicherheit stehen in der zentralen Referenz.

| Name | Pflicht | Format | Gesetzt durch | Beispielwert |
| --- | --- | --- | --- | --- |
| `TRAEFIK_BIN` | Optional | executable Traefik path | Provisioning or caller | `<component-cache>/traefik/bin/traefik` |
| `TRAEFIK_ENGINE_SERVICE_BUILD_DIR` | Optional | absolute build directory | Build script or caller | `<build-root>/traefik-engine-service` |
| `TRAEFIK_ENGINE_SERVICE_BIN` | Optional | absolute engine-service executable | Build script or caller | `<build-root>/traefik-engine-service/traefik-engine-service` |
| `TRAEFIK_CONNECTOR_CONFIG` | Optional | absolute connector configuration | Start-smoke harness or caller | `config/traefik-forwardauth.conf` |

Siehe die [zentrale Variablenreferenz](../../configuration/variables.de.md).
