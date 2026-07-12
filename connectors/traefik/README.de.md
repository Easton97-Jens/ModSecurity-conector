# Traefik-Connector

**Sprache:** [English](README.md) | Deutsch

Status: `forwardAuth`-Kompatibilitäts-Smoke plus nicht-promotierter nativer
Local-Plugin-UDS-Hostprobe.
Der Connector besitzt einen eigenen C17-Entry-Point und bleibt für CRS,
Security, Produktion und Full Matrix bewusst `not_verified` / `connector-gap`.

Daneben existiert unter `native_middleware/` ein repo-eigenes Go-Middleware-
Quellmodul. Es verarbeitet begrenzte Request- und Response-Chunks, puffert
keine ganze Response und erhält `Flush`, `Hijack`, `Push` sowie `ReadFrom`.
Der Full-Lifecycle-Runner staged es über `full-lifecycle-traefik-native` in
Traefiks echten `plugins-local`-Workspace und wählt dort mit `engineMode: uds`
einen persistenten lokalen Common/libmodsecurity-Service. Pro `ServeHTTP`
entsteht genau eine UDS-Verbindung. Der C-`forwardAuth`-Pfad bleibt der
getrennte Request-only-Kompatibilitätspfad.

Der native Hostprobe liefert gezielte reale P1--P4-Safe-Evidenz, promotet aber
keine P1--P4-, Safe-, Strict-, First-Byte-, No-Full-Buffer-, CRS- oder
Produktions-Capability.

## Persistenter nativer UDS-Engine-Service

`src/traefik_engine_service.c` und `src/traefik_engine_protocol.h` ergänzen
einen persistenten lokalen Unix-Domain-Socket-Service mit Common/
libmodsecurity für die Yaegi-kompatible Go-Brücke. Er verwendet begrenzte
Metadaten-/Chunk-Frames und explizite EOS-, Finish- und Destroy-Operationen.
Der Hostprobe liefert den privaten Socket und den run-lokalen Eventpfad und
schreibt ein hostbestätigtes Outcome erst nach erfolgreicher
ResponseWriter-Aktion. Nach Response-Commit akzeptiert P4 nur `LOG_ONLY` mit
dem tatsächlich sichtbaren Status.

```sh
MODSECURITY_INCLUDE_DIR=/lokal/include \
MODSECURITY_LIB_DIR=/lokal/lib \
make -C connectors/traefik test-engine-service
```

Der fokussierte Test startet ausschließlich den lokalen Engine-Service und ist
kein Traefik-Host-Runtime-Test. Lebenszyklus, kanonische Regelauswahl und
Integrationsgrenzen stehen im [Engine-Service-Protokoll](docs/engine-service.de.md).

Der reale Local-Plugin-Hostprobe ist separat ausführbar:

```sh
TRAEFIK_BIN=/absoluter/lokaler/traefik \
TRAEFIK_NATIVE_RUNTIME_ROOT=/absoluter/runtime-root \
MODSECURITY_INCLUDE_DIR=/absolut/include \
MODSECURITY_LIB_DIR=/absolut/lib \
MSCONNECTOR_RULES_FILE=/absolut/no-crs-baseline.conf \
make -C connectors/traefik runtime-smoke-traefik-native
```

Mit der kanonischen Regeldatei verlangt der Probe P1-Allow `200`, P1-Deny
`403` (`1100001`), P2-Deny `403` (`1100101`), P3-Deny vor Commit `403`
(`1100201`) und P4-Safe/Log-only mit sichtbarem `200` (`1100301`). P4-Strict
ist `NOT EXECUTED`. Er schreibt nur Metadaten, keine Payloads; die
hostbestätigten JSONL-Ereignisse verwenden exakt
`integration_mode=native-traefik-middleware` und `transport_result=http_status`
oder `log_only`. Die lokalen Go-Tests/Builds bleiben über
`make -C connectors/traefik test-native-middleware` und
`build-native-middleware` verfügbar, sind aber allein kein Hostnachweis.

- Common Config wird über `traefik_modsecurity_config_init()` initialisiert.
- Request- und Response-Mapper sind dünne Funktionen, keine Makro-Aliase.
- `traefik_forwardauth_service_main.c` registriert das Hostprofil beim neutralen
  HTTP-Authorization-Service; `X-Forwarded-Uri` hat Vorrang.
- Der Build ist compile-/link-only; Config-Check und Start-Smoke sind getrennt.
  Der Start-Smoke startet Service und echtes Traefik mit temporärer
  forwardAuth-File-Provider-Config, sendet aber keine Requests.
- Response-Header/-Body des Upstreams sind für `forwardAuth` nicht verfügbar.
- Es gibt keine Produktions-, CRS-, Full-Matrix- oder Capability-
  Verifikationsbehauptung.

## Kompatibilitäts- und native Phase-4-Grenze

Das Kompatibilitäts-Host-Modell Traefik `forwardAuth` wird vor der
Upstream-Verarbeitung ausgeführt und kann den späteren Upstream-Response-Body
nicht inspizieren. Daher sind für diesen Pfad `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` als `unsupported_by_host_model` und nicht
nur als in einem lokalen Lauf fehlend deklariert.

Der getrennte native UDS-Probe beobachtet die Upstream-Response. Er besitzt
gezielte Evidenz für P3-Deny vor Commit und P4-`log_only` nach Commit mit
ursprünglichem und sichtbarem Status. Er kann keinen späten Abort beweisen;
P4-Strict bleibt `NOT EXECUTED`. Keiner der beiden Pfade ändert ohne getrennte
kanonische Evidenz-/Promotion-Prüfung einen Capability-Status.

Response-Body-Payloads gehören weder in Ereignisse noch in Berichte.
