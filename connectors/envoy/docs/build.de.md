# Envoy Connector Build

**Sprache:** [English](build.md) | Deutsch

Status: C17-Kompilierung/Link überprüft; Der gezielte ext_authz-Anforderungspfad lautet
`minimal_runtime_smoke` / `connector-gap`.

## Connector-Dienst

```sh
make -C connectors/envoy build-envoy-connector \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

Stattdessen kann `MODSECURITY_PREFIX` oder `MODSECURITY_LIB_FILE` verwendet werden. Der Bau
akzeptiert vom Framework aufgelöste Werte über dieselben Variablen. Es kompiliert mit
`-std=c17 -Wall -Wextra -Werror`, verknüpft Common SDK/Runtime, das Envoy-Profil und
Thin Mapper und zeichnet einen lokalen R-Pfad zu den explizit ausgewählten auf
libmodsecurity-Verzeichnis.

Ausgabe:

```text
${BUILD_ROOT}/envoy-connector/msconnector_envoy_ext_authz
```

`BUILD_ROOT` muss absolut sein und außerhalb des Checkouts liegen. Das Build-Ziel tut dies
Führen Sie die Binärdatei nicht aus, validieren Sie die Konfiguration nicht, starten Sie keinen Prozess und senden Sie keine Anfrage.

## Separate Tore

```sh
make -C connectors/envoy check-envoy-config RULES_FILE=/absolute/rules.conf
make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy RULES_FILE=/absolute/rules.conf
make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy RULES_FILE=/absolute/rules.conf
```

Die älteren Ziele `build-starter` und `self-test` bleiben isoliert kompatibel
sucht nach der lokalen Bridge-CLI und erstellt oder überprüft den Connector-Dienst nicht.

## Separates Build-Ziel ext_proc Common/libmodsecurity

Der nicht beworbene externe Go-Verarbeitungsdienst wird unabhängig angeheftet. Es ist
Eine normale ausführbare Datei verwendet CGo, um die Connector-lokale Bridge, Common Runtime, zu verknüpfen.
und libmodsecurity, daher sind explizite libmodsecurity-Pfade erforderlich:

```sh
make -C connectors/envoy build-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy test-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-runtime-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc \
  ENVOY_BIN=/absolute/path/to/envoy \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

`go.mod`/`go.sum` pinnt die offiziell generierten Go-API- und gRPC-Abhängigkeiten von Envoy.
`config/envoy-ext-proc-versions.env` pinnt die beabsichtigte Envoy-Version. Der Bau
verwendet `go mod verify`, kompiliert ein privates Common-Archiv und erstellt mit
`-tags libmodsecurity`; Die Konfigurationsmaterialisierer schreiben nur außerhalb von
Kasse. Das Testziel führt nur Quell-Go-Tests aus und wenn die Pfade vorhanden sind
verfügbar, getaggt mit CGo-Lebenszyklustests. Der Laufzeitrauch validiert die
materialisierte YAML und führt echtes Envoy-to-ext_proc/Common/libmodsecurity aus
Regelauswertung mit rohem Common JSONL. Es bleibt nicht beworben: Es wird nicht gefördert
selbst eine kanonische Sammlung, Timeout-/Reset-Semantik, HTTP/2 oder
Produktionsinteroperabilität.
