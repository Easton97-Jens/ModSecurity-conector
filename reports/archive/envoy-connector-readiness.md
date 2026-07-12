> Status: Historical
> Superseded by: [../current/six-connector-core-completion.md](../current/six-connector-core-completion.md)
> Date: retained as a historical report during repository organization on 2026-07-12
> Evidence boundary: historical planning, assessment, or snapshot; not current canonical evidence.

# Envoy Connector Readiness

**Language:** English | [Deutsch](envoy-connector-readiness.de.md)

> **Evidence-scope note.** This is a historical local
> `minimal_runtime_smoke` snapshot from 2026-07-10, not a canonical No-CRS
> result. It must not override the current generated
> [Envoy No-CRS snapshot](../evidence/envoy-no-crs-baseline.md) or the
> [canonical capability matrix](../testing/generated/canonical/connector-capabilities.generated.md).
> Only a canonical `result.json` can promote the current No-CRS status; local
> smoke evidence below remains deliberately narrower.

Evidence snapshot: 2026-07-10

## Outcome

The Envoy connector has status `minimal_runtime_smoke`, limited to one local,
targeted HTTP `ext_authz` request-header path. A real Envoy 1.38.2 process sent
an allowed request through the repository-owned authorization service and
received HTTP 200. A second request carrying `X-Modsec-Smoke: block` was denied
with HTTP 403 by libmodsecurity rule `1000001` through the Common decision path.

This evidence does not extend to request-body inspection, upstream responses,
CRS, a broad test matrix, security assessment, or operational deployment.

## Architecture and host integration

The selected host model is a repository-owned external HTTP authorization
service used by Envoy's `ext_authz` filter. It is not a native Envoy filter and
does not depend on the older `envoy_bridge` self-test.

- `connectors/envoy/src/envoy_ext_authz_service_main.c` defines the Envoy host
  profile, URI-header preferences, mapper callbacks, and service entry point.
- `connectors/envoy/src/envoy_modsecurity_mapper.c` contains thin C17 wrappers
  around the Common generic configuration, request, and response mappers.
- `common/runtime/http_authorization_service.c` owns the connector-neutral HTTP
  service lifecycle; `common/runtime/msconnector_runtime.c` owns the
  libmodsecurity transaction, decision, intervention, and event path.
- The runtime uses `x-request-id` for the requested transaction ID and maps the
  disruptive request decision to the authorization response status.
- The selected protocol cannot observe upstream response headers or bodies.
  The linked response mapper is therefore not evidence of an Envoy response
  inspection path.

## Common SDK adoption

The live connector path initializes `msconnector_config` through
`msconnector_generic_config_init()`, maps requests through
`msconnector_generic_map_request()`, and uses Common runtime APIs for rule
loading, transaction IDs, resource guards, decisions, interventions, metadata
events, and JSONL serialization. Envoy types and configuration remain under
`connectors/envoy/`; no Envoy host type is introduced into `common/`.

The repository checks completed successfully:

```sh
make check-envoy-common-adoption
make check-remaining-connectors-host-integration
```

## Configuration

`connectors/envoy/config/envoy-ext-authz.conf` maps the enabled flag, rules file,
transaction-ID header, body modes and limits, block/error statuses, event path,
and header/event resource limits into Common configuration. The launcher writes
a concrete copy outside the checkout and substitutes only managed rules and
event paths.

The template configures a 4096-byte buffered request-body ceiling, but the
current runtime smoke sends GET requests without bodies. That setting is a
configured boundary, not request-body runtime evidence. Response-body mode is
`none`. Inline rules, remote rules, and broader directive combinations were not
exercised by this evidence set.

## Build, config, start, and runtime evidence

| Stage | Reproduction command | Observed evidence | Boundary |
|---|---|---|---|
| Build | `make build-envoy-connector` | C17 compile with `-Wall -Wextra -Werror`; service linked to local libmodsecurity with a local `RUNPATH` | Compile/link only; no process or request |
| Config | `make check-envoy-config` | Concrete Common config accepted and targeted rules loaded | Does not start Envoy |
| Start | `make start-smoke-envoy` | Generated Envoy YAML validated; service and Envoy stayed alive; both stopped; `requests_sent=no` | Process-lifecycle evidence only |
| Runtime | `make runtime-smoke-envoy` | Real Envoy -> `ext_authz` -> Common/libmodsecurity path returned 200 and rule-backed 403; metadata event found; processes stopped | Two targeted request-header cases only |

The observed local evidence is outside the checkout:

- Build artifact:
  `<verified-run-root>/build/envoy-connector/msconnector_envoy_ext_authz`
- Start summary:
  `<verified-run-root>/build/envoy-connector/start-smoke/start-summary.txt`
- Runtime summary:
  `<verified-run-root>/build/envoy-connector/runtime-smoke/runtime-summary.txt`
- Runtime event:
  `<verified-run-root>/build/envoy-connector/runtime-smoke/events.jsonl`

The runtime event identifies connector `envoy`, transaction
`envoy-block-1`, request-header phase, rule `1000001`, and HTTP 403. It contains
metadata rather than request or response body payloads. These local artifacts
are reproducible evidence, but they are not a retained multi-platform CI run.

Missing local prerequisites are reported as BLOCKED with exit 77. Once the
required executables and inputs are resolved, configuration, startup, mapping,
status, or event mismatches are failures rather than skips.

## Known limits and remaining technical gaps

- No request carrying a body has been tested through Envoy and the connector.
- Upstream response headers, response metadata, and response bodies are not
  exposed to this `ext_authz` service.
- No response-phase or late-intervention behavior has been tested.
- Inline/remote rule sources, content-type policies, truncation cases, redirects,
  drop/abort behavior, concurrency, resilience, and performance remain open.
- No CRS execution, full No-CRS/with-CRS matrix, security assessment, or
  deployment hardening was performed.
- The evidence covers one local Envoy version and one targeted rule only.

## Claims supported by the evidence

- A real repository-owned Envoy `ext_authz` host path exists and uses the Common
  SDK and runtime.
- The connector builds and links against local libmodsecurity in the managed
  environment.
- Config validation and a request-free real Envoy start/stop smoke pass locally.
- The targeted request-header host path has `minimal_runtime_smoke` evidence for
  an allowed HTTP 200 and a rule-backed HTTP 403 with a metadata-only event.

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- full-matrix verification
- request-body, response-header, or response-body verification
- broad Envoy-version or platform compatibility
- verification of all connectors
