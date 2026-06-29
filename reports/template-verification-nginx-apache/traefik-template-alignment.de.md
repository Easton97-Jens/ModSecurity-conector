# Traefik-Vorlagenausrichtung

**Sprache:** [English](traefik-template-alignment.md) | Deutsch

Status: Entscheidungsdienststarter
Laufzeitstatus: nicht überprüft

`connectors/traefik` enthält jetzt einen Repo-eigenen lokalen Entscheidungsdienst-Starter.
Es folgt weiterhin gemeinsam genutzten Connector-Gates und dupliziert nicht das gesamte Global
Regeln vor Ort.

## Umfang

- Traefik ist auf einen Entscheidungsdienst-Starter ausgerichtet.
- Laufzeitstatus: nicht überprüft.
- Es wird kein lokaler `connectors/traefik/tests`-Ordner verwendet.
- Es besteht kein Anspruch auf Traefik-Laufzeit.
- Kein Traefik API, Plugin SDK, Middleware SDK, Go-Modul, HTTP Dienst oder real
  Laufzeit-Harness ist implementiert.
- Starter-Quelle stellt Metadaten, lokale Entscheidungslogik und gemeinsame `common/` zusammen
  nur Helfer.

## Gemeinsame Referenzen

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `common/include/msconnector/`
- `common/src/`
- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

## Erstellen Sie Nachweise und testen Sie sie selbst

- Metadatenbefehl: `connectors/traefik/build/build-starter.sh`
- Entscheidungsbefehl: `make -C connectors/traefik build-decision-service`
- Selbsttestbefehl: `make -C connectors/traefik self-test-decision-service`
- Status: PASS für Metadaten-Starter zur Kompilierungszeit, Starter für Entscheidungsdienste und
  Lokaler In-Memory-Entscheidungsselbsttest.
- Artefaktpfade: `$BUILD_ROOT/traefik-build-starter/traefik_build_starter` und
  `$BUILD_ROOT/traefik-build-starter/traefik_decision_service_starter`.
- Laufzeitbedeutung: keine; Dies ist kein Traefik-Adapter-Laufzeit-Build.

## Bewertung der Integrationsoption

| Option | Current decision | Reason |
| --- | --- | --- |
| Plugin | deferred | no Traefik plugin API or Go module in repo |
| Middleware | deferred | no Traefik middleware API or Go dependency in repo |
| `forwardAuth` / external decision service | starter only | local decision model exists; no HTTP server, Traefik config, or runtime harness |
| Sidecar/proxy bridge | deferred | no bridge runtime/config/harness |
| Custom module/build | deferred | no Traefik source/build contract |

## Phasenmatrix

| Phase | Status | Notes |
| --- | --- | --- |
| Phase 0 Scaffold | OK | Scaffold files are present |
| Phase 1 Origin/Metadata | starter-present | Repo-owned starter origin, source map, and metadata are present; upstream Traefik origin remains open |
| Phase 2 Build | decision-service-starter | Metadata and decision-service starters passed local compile/self-test |
| Phase 3 Harness | blocked entrypoint only | Connector-side runtime-smoke script writes BLOCKED evidence only |
| Phase 4 No-CRS | not-run | No Traefik runtime command was run |
| Phase 5 With-CRS | not-run | No Traefik runtime command was run |
| Phase 6 Coverage Matrix | starter-documented | Connector-specific matrix records open runtime gates |
| Phase 7 RESPONSE_BODY | not-verified | No blocking runtime evidence exists |
| Phase 8 Negative/pass-through | not-verified | No runtime evidence exists |
| Phase 9 Audit/log | not-verified | No runtime evidence exists |
| Phase 10 Promotion | not allowed | Required production origin, build, harness, and runtime gates are open |

## Framework-Starter-Nachweis

`make connector-starter-checks` zeichnet die Ergebnisse des Traefik-Starters auf
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` und
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Diese Aufzeichnungen dienen ausschließlich der Nachweissicherung und werden aufbewahrt
`runtime_verified: false`, `runtime_status: not-verified` und
`response_body_verified: false`.

## Runtime-Smoke-Eintrittspunkt

`make smoke-traefik` ruft jetzt den Framework-eigenen Traefik-Runtime-Smoke auf
Runner, der versendet
`connectors/traefik/harness/run_traefik_smoke.sh`. Aktueller Status ist BLOCKED
weil dieser connector-seitige Einstiegspunkt nur Diagnosebeweise schreibt und nein
Es gibt ein echtes Traefik server/config/runtime-Harness. Die Laufzeit bleibt nicht überprüft
und RESPONSE_BODY bleibt nicht verifiziert.
