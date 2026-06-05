# Traefik Connector

Status: decision-service-starter
Runtime status: not-verified
Template alignment: scaffold-aligned with local decision-service starter

This connector now contains a repo-owned local decision-service starter in
addition to the compile-time metadata starter. It still does not contain a
runtime-verified Traefik adapter implementation.

The starter compiles only repository-owned C code and shared common helpers:

- `connectors/traefik/metadata.c`
- `connectors/traefik/metadata.h`
- `connectors/traefik/src/traefik_build_starter.c`
- `connectors/traefik/src/traefik_decision_service.*`
- shared helpers from `common/src/` and `common/include/msconnector/`

It does not include a Traefik API, Traefik plugin SDK, Go module,
libmodsecurity runtime integration, Traefik traffic handling, CRS execution,
RESPONSE_BODY handling, or a Traefik runtime harness.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Traefik-specific State

- Origin/license: documented for repo-owned starter; upstream Traefik source not selected
- Metadata: repo-owned compile-time metadata present
- Build: metadata and decision-service starter commands present
- Self-test: local decision-service starter self-test present
- Harness: contract only
- No-CRS runtime: not run
- With-CRS runtime: not run
- RESPONSE_BODY blocking: not verified

## Build and Self-Test

Run the metadata build starter with:

```sh
connectors/traefik/build/build-starter.sh
```

Run the local decision-service starter self-test with:

```sh
make -C connectors/traefik self-test-decision-service
```

A successful self-test proves only local allow/block decision logic for in-memory
request structs. It is not a Traefik runtime, `forwardAuth`, CRS, or
libmodsecurity validation.

## Tests

No local `connectors/traefik/tests` folder is used. Executable tests are
framework-owned.

Framework-owned paths and targets to use after a real Traefik build and harness
are implemented:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

No No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through, audit/log, or Traefik
runtime result is claimed for Traefik by this starter.
