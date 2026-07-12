# Traefik-Connector

**Sprache:** [English](README.md) | Deutsch

Status: `forwardAuth`-Kompatibilitäts-Smoke plus nicht-promotierter nativer
Local-Plugin-Hostprobe.
Der Connector besitzt einen eigenen C17-Entry-Point und bleibt für Request-Body,
Upstream-Response, CRS, Security, Produktion und Full Matrix bewusst
`not_verified` / `connector-gap`.

Daneben existiert unter `native_middleware/` ein repo-eigenes Go-Middleware-
Quellmodul. Es verarbeitet begrenzte Request- und Response-Chunks über einen
expliziten `PassthroughEngine`, puffert keine ganze Response und erhält
`Flush`, `Hijack`, `Push` sowie `ReadFrom`. Der Full-Lifecycle-Runner staged es
über `full-lifecycle-traefik-native` in Traefiks echten `plugins-local`-
Workspace, lädt es im gepinnten Host und sendet einen body-tragenden Request
durch einen Router mit dieser Middleware.
Das ist ausschließlich eine Host-Auswahlprobe: `PassthroughEngine` ruft weder
Common noch libmodsecurity auf und promotet keine P1–P4-, Safe-, Strict-,
First-Byte- oder No-Full-Buffer-Capability. Der C-`forwardAuth`-Pfad bleibt
der getrennte Kompatibilitätspfad.

Der reale Local-Plugin-Hostprobe ist separat ausführbar:

```sh
TRAEFIK_BIN=/absoluter/lokaler/traefik \
TRAEFIK_NATIVE_RUNTIME_ROOT=/absoluter/runtime-root \
make -C connectors/traefik runtime-smoke-traefik-native
```

Er schreibt nur Status- und Byte-/Chunk-Metadaten, keine Payloads. Die lokalen
Go-Tests/Builds bleiben über `make -C connectors/traefik
test-native-middleware` und `build-native-middleware` verfügbar, sind aber
allein kein Hostnachweis.

- Common Config wird über `traefik_modsecurity_config_init()` initialisiert.
- Request- und Response-Mapper sind dünne Funktionen, keine Makro-Aliase.
- `traefik_forwardauth_service_main.c` registriert das Hostprofil beim neutralen
  HTTP-Authorization-Service; `X-Forwarded-Uri` hat Vorrang.
- Der Build ist compile-/link-only; Config-Check und Start-Smoke sind getrennt.
  Der Start-Smoke startet Service und echtes Traefik mit temporärer
  forwardAuth-File-Provider-Config, sendet aber keine Requests.
- Response-Header/-Body des Upstreams sind für `forwardAuth` nicht verfügbar.
- Es gibt keine Produktions-, CRS-, Full-Matrix-, Runtime- oder RESPONSE_BODY-Verifikationsbehauptung.

## Kanonische Grenze für Phase 4

Das gewählte Host-Modell ist Traefik `forwardAuth`. Es wird vor der
Upstream-Verarbeitung ausgeführt und kann den späteren Upstream-Response-Body
nicht inspizieren. Daher sind `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata` als `unsupported_by_host_model` und nicht
nur als in einem lokalen Lauf fehlend deklariert.

Die gemeinsamen Phase-4-Fälle müssen deshalb mit der eindeutigen
forwardAuth-Architekturbegründung `UNSUPPORTED` ergeben. Ein requestseitiges
200 oder 403 belegt ausschließlich den Autorisierungspfad vor dem Upstream;
es belegt weder Response-Body-Inspektion noch ursprünglichen Upstream-Status,
sichtbaren Status nach dem Commit oder eine späte Aktion. `UNSUPPORTED` zählt
nie als `PASS` und darf nicht allein wegen eines fehlenden Response-Tests in
`NOT_EXECUTED` umgewandelt werden.

Response-Body-Payloads gehören weder in Ereignisse noch in Berichte. Ein
zukünftiger Traefik-Integrationspfad mit Upstream-Response-Sicht wäre ein
anderes Host-Modell und benötigt eigenständige Nachweise.
