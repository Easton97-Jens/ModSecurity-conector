# Ursprung des Traefik-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: forwardAuth compatibility smoke plus targeted native UDS host probe
Runtime status: targeted local P1--P4-safe evidence; broader verification remains open

In dieses Repository wurde keine Upstream-Quellbasis eines Traefik-Connectors
importiert. Das Repository besitzt ein kleines Go-Modul der Standardbibliothek
unter `native_middleware/`; es ist weder importierter Traefik-Quellcode noch
ein Traefik-SDK oder eine cgo-Bridge. Die Standard-Kompatibilitätsgrenze bleibt
das externe HTTP-`forwardAuth`-Protokoll von Traefik; der Full-Lifecycle-
Host-Probe wählt separat das native lokale Plugin und seine repository-eigene
persistente UDS-Common-/libmodsecurity-Bridge aus, ohne
Capability-Deklarationen zu verändern.

## Aktuelles Quelleninventar

| Pfad | Ursprung | Upstream-Version | Lizenzstatus | Hinweise |
| --- | --- | --- | --- | --- |
| `connectors/traefik/metadata.c` | repository-eigene Starter-Metadaten | not selected | repository root license not documented | Compile-Time-Metadaten für den lokalen Starter |
| `connectors/traefik/metadata.h` | repository-eigene Starter-Metadaten | not selected | repository root license not documented | Compile-Time-Metadatendeklarationen |
| `connectors/traefik/src/traefik_build_starter.c` | repository-eigener Build-Starter-Quellcode | not selected | repository root license not documented | Enthält weder Traefik- noch libmodsecurity-APIs |
| `connectors/traefik/src/traefik_decision_service.h` | repository-eigener Decision-Service-Starter | not selected | repository root license not documented | Deklarationen des lokalen Decision-Modells |
| `connectors/traefik/src/traefik_decision_service.c` | repository-eigener Decision-Service-Starter | not selected | repository root license not documented | Nur lokale Request-Decision-Logik |
| `connectors/traefik/src/traefik_decision_service_main.c` | repository-eigener Decision-Service-Starter | not selected | repository root license not documented | Nur CLI-/Self-Test-Einstiegspunkt |
| `connectors/traefik/build/build-starter.sh` | repository-eigener Build-Helper | not selected | repository root license not documented | Kompiliert Metadaten- und Decision-Service-Starter |
| `connectors/traefik/Makefile` | repository-eigener Build-Helper | not selected | repository root license not documented | Connector-lokale Build-/Self-Test-Targets |
| `connectors/traefik/src/traefik_modsecurity_mapper.c` | repository-eigener Adapter-Quellcode | not selected | repository root license not documented | Schlanke Common-Mapper-Callsites |
| `connectors/traefik/src/traefik_forwardauth_service_main.c` | repository-eigener Adapter-Quellcode | not selected | repository root license not documented | Host-Profil für den Common-HTTP-Autorisierungsservice |
| `connectors/traefik/build/build-connector.sh` | repository-eigener Build-Helper | not selected | repository root license not documented | Nur C17-Compile-/Link-Service-Build |
| `connectors/traefik/scripts/check-config.sh` | repository-eigener Validierungs-Helper | not selected | repository root license not documented | Einstiegspunkt für Konfigurationsprüfung |
| `connectors/traefik/scripts/start-smoke.sh` | repository-eigener Validierungs-Helper | not selected | repository root license not documented | Nur Process-Start-/Stop-Smoke |
| `connectors/traefik/scripts/runtime-smoke.sh` | repository-eigener Validierungs-Helper | not selected | repository root license not documented | Runtime-Smoke-Einstiegspunkt |
| `connectors/traefik/scripts/runtime_smoke.py` | repository-eigener Validierungs-Helper | not selected | repository root license not documented | Traefik-/forwardAuth-/Upstream-Orchestrierung und Evidenz |
| `connectors/traefik/config/traefik-forwardauth.conf` | repository-eigene Beispielkonfiguration | not selected | repository root license not documented | Request-Phase-Konfiguration; Response-Verarbeitung deaktiviert |
| `connectors/traefik/config/traefik-forwardauth-dynamic.yaml` | repository-eigene Beispielkonfiguration | not selected | repository root license not documented | Traefik-File-Provider-Vorlage für den Start-Smoke |
| `connectors/traefik/src/traefik_engine_protocol.h` | repository-eigenes UDS-Protokoll | selected by non-promoted full-lifecycle host probe | repository root license not documented | Begrenzter P1--P4-Lifecycle- und Host-Outcome-Vertrag |
| `connectors/traefik/src/traefik_engine_service.c` | repository-eigener Common-/libmodsecurity-Service | selected by non-promoted full-lifecycle host probe | repository root license not documented | Persistenter privater UDS-Engine-Service |
| `connectors/traefik/native_middleware/middleware.go` | repository-eigener Go-Middleware-Quellcode | selected by non-promoted full-lifecycle host probe | repository root license not documented | Begrenzter Streaming-Wrapper mit Passthrough als Default und UDS-Auswahl |
| `connectors/traefik/native_middleware/engine_uds.go` | repository-eigener Go-UDS-Client | selected by non-promoted full-lifecycle host probe | repository root license not documented | Eine Session pro Host-Request zum persistenten Engine-Service |
| `connectors/traefik/native_middleware/middleware_test.go` | repository-eigene Go-Unit-Tests | selected by non-promoted full-lifecycle host probe | repository root license not documented | Fokussierte Source-Level-Behavior-Tests |
| `connectors/traefik/native_middleware/engine_uds_test.go` | repository-eigene Go-UDS-Tests | selected by non-promoted full-lifecycle host probe | repository root license not documented | Lifecycle- und Host-Outcome-Ordering-Tests |
| `connectors/traefik/native_middleware/go.mod` | repository-eigene Go-Modulmetadaten | selected only by non-promoted full-lifecycle host probe | repository root license not documented | Keine externen Abhängigkeiten |
| `connectors/traefik/native_middleware/.traefik.yml` | repository-eigenes Plugin-Manifest | selected only by non-promoted full-lifecycle host probe | repository root license not documented | Traefik-Plugin-Metadaten/Testdaten; gepinnter Host-Load-Probe vorhanden |
| `connectors/traefik/build/build-native-middleware.sh` | repository-eigener Build-Helper | selected only by non-promoted full-lifecycle host probe | repository root license not documented | Go-Source-Build-/Test-Befehl, Report nur außerhalb des Checkouts |
| `connectors/traefik/config/traefik-native-middleware-dynamic.yaml` | repository-eigene Beispielkonfiguration | selected only by non-promoted full-lifecycle host probe | repository root license not documented | Referenzform des lokalen Plugin-File-Providers |
| `connectors/traefik/config/traefik-native-middleware-static.yaml` | repository-eigene Beispielkonfiguration | selected only by non-promoted full-lifecycle host probe | repository root license not documented | Referenzform der lokalen Plugin-Registrierung |
| `connectors/traefik/scripts/runtime_native_smoke.py` | repository-eigenes Host-Harness | selected by non-promoted full-lifecycle host probe | repository root license not documented | Isolierter Host, UDS-Engine, kanonische Regeln und Orchestrierung ausschließlich von Outcome-Metadaten |

## Nicht importiert

- Traefik-Quellcode: not selected.
- Traefik-Plugin- oder Middleware-SDK: not selected.
- Traefik-Go-Modul: nicht importiert; das repository-eigene
  Standardbibliotheksmodul ist ein lokales Plugin-Source-Package, kein
  Upstream-SDK-Quellcode.
- Traefik-Plugin-/cgo-Integrations-Quellcode: nicht vorhanden und not selected.

## Runtime-Claim

Diese Datei erhebt keinen Capability-Claim. Sie dokumentiert nur
repository-eigene Source- und Build-Grenzen; der gezielte Host-Probe belegt
weder CRS-Vollständigkeit noch vollständige Response-Phase-Abdeckung oder
Produktionsreife.
