# Traefik Template Alignment

Status: decision-service-starter
Runtime status: not-verified

`connectors/traefik` now contains a repo-owned local decision-service starter.
It still follows shared connector gates and does not duplicate the full global
rules locally.

## Scope

- Traefik is scaffold-aligned with a decision-service starter.
- Runtime status: not-verified.
- No local `connectors/traefik/tests` folder is used.
- No Traefik runtime claim is made.
- No Traefik API, plugin SDK, middleware SDK, Go module, HTTP service, or
  runtime harness is implemented.
- Starter source compiles metadata, local decision logic, and shared `common/`
  helpers only.

## Shared References

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `common/include/msconnector/`
- `common/src/`
- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

## Build and Self-Test Evidence

- Metadata command: `connectors/traefik/build/build-starter.sh`
- Decision command: `make -C connectors/traefik build-decision-service`
- Self-test command: `make -C connectors/traefik self-test-decision-service`
- Status: PASS for compile-time metadata starter, decision-service starter, and
  local in-memory decision self-test.
- Artifact paths: `$BUILD_ROOT/traefik-build-starter/traefik_build_starter` and
  `$BUILD_ROOT/traefik-build-starter/traefik_decision_service_starter`.
- Runtime meaning: none; this is not a Traefik adapter runtime build.

## Integration Option Evaluation

| Option | Current decision | Reason |
| --- | --- | --- |
| Plugin | deferred | no Traefik plugin API or Go module in repo |
| Middleware | deferred | no Traefik middleware API or Go dependency in repo |
| `forwardAuth` / external decision service | starter only | local decision model exists; no HTTP server, Traefik config, or runtime harness |
| Sidecar/proxy bridge | deferred | no bridge runtime/config/harness |
| Custom module/build | deferred | no Traefik source/build contract |

## Phase Matrix

| Phase | Status | Notes |
| --- | --- | --- |
| Phase 0 Scaffold | OK | Scaffold files are present |
| Phase 1 Origin/Metadata | starter-present | Repo-owned starter origin, source map, and metadata are present; upstream Traefik origin remains open |
| Phase 2 Build | decision-service-starter | Metadata and decision-service starters passed local compile/self-test |
| Phase 3 Harness | contract only | Harness contract is documented only |
| Phase 4 No-CRS | not-run | No Traefik runtime command was run |
| Phase 5 With-CRS | not-run | No Traefik runtime command was run |
| Phase 6 Coverage Matrix | starter-documented | Connector-specific matrix records open runtime gates |
| Phase 7 RESPONSE_BODY | not-verified | No blocking runtime evidence exists |
| Phase 8 Negative/pass-through | not-verified | No runtime evidence exists |
| Phase 9 Audit/log | not-verified | No runtime evidence exists |
| Phase 10 Promotion | not allowed | Required production origin, build, harness, and runtime gates are open |

## Framework Starter Evidence

`make connector-starter-checks` records Traefik starter results in
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` and
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Those records are connector-starter evidence only and keep
`runtime_verified: false`, `runtime_status: not-verified`, and
`response_body_verified: false`.
