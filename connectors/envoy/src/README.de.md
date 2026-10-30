# Envoy-Quellcode

**Sprache:** [English](README.md) | Deutsch

Der C-Dienst `ext_authz` und der separate Go-Dienst `ext_proc` sind verschiedene
Connector-Profile. Quellcode und Kompilierung beweisen keinen Lauf im Host.

- `envoy_ext_authz_service_main.c` wählt das Connector-eigene Hostprofil und den
  gemeinsamen HTTP-Autorisierungsdienst in `common/runtime/` aus.
- `envoy_modsecurity_mapper.h` / `.c` adaptieren Request-, Response- und
  Konfigurationsmetadaten an die Mapper-Verträge von Common.
- `envoy_bridge.h` / `.c` behalten das historische lokale Entscheidungsmodell.
- `envoy_bridge_main.c` bietet den Starter-Metadatenbefehl `--describe` an.

Der Bridge-Starter ruft weder Envoy noch libmodsecurity auf. Seine
Regressionsassertions gehören nun zum gepinnten Framework unter
`connector_native_tests/connectors/envoy/src/envoy_bridge.inc`. Aus dem
Connector-Wurzelverzeichnis werden sie mit
`make -C connectors/envoy self-test ON_DEMAND_TESTS=1` gestartet.
Das Starterprogramm akzeptiert `--self-test` nicht mehr. Dies erweitert weder die
Standardauswahl noch belegt es Enforcement im Host.

Produktive Launcher bleiben unter `../scripts/` im Connector:
`serve_envoy_connector.sh` und `serve_envoy_ext_proc.sh`. Konfigurations- und
Serve-Befehle verlangen ein explizites produktives `RULES_FILE` oder
`MSCONNECTOR_RULES_FILE`; `serve-envoy-ext-proc` akzeptiert auch
`EXT_PROC_RULES_FILE`. Die Produktkonfiguration verwendet keine implizite
Framework-Fixture. Benannte Smoke-Targets wählen ihre Framework-Regeln explizit;
ihre Harnesses liegen im Framework unter `connector_suite/adapters/envoy/`.
Testausgaben müssen außerhalb der Quellverzeichnisse liegen.
