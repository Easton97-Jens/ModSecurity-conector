# Traefik Connector Readiness

**Language:** English | [Deutsch](traefik-connector-readiness.de.md)

> **Evidence-scope note.** This is a historical local
> `minimal_runtime_smoke` snapshot from 2026-07-10, not a canonical No-CRS
> result. It must not override the current generated
> [Traefik No-CRS snapshot](traefik-no-crs-baseline.md) or the
> [canonical capability matrix](testing/generated/canonical/connector-capabilities.generated.md).
> Only a canonical `result.json` can promote the current No-CRS status; local
> smoke evidence below remains deliberately narrower.

Evidence snapshot: 2026-07-10

## Outcome

The Traefik connector has status `minimal_runtime_smoke`, limited to one local,
targeted HTTP `forwardAuth` request-header path. A real Traefik 3.7.5 process
sent an allowed request through the repository-owned service and returned HTTP
200 from the upstream. A request carrying `X-Modsec-Smoke: block` was denied
with HTTP 403 by libmodsecurity rule `1000001` through the Common decision path.

This evidence does not cover request bodies, upstream response inspection, CRS,
a broad test matrix, security assessment, or operational deployment.

## Architecture and host integration

The selected host model is an external HTTP `forwardAuth` service. It is not a
Traefik Go plugin, middleware module, or cgo bridge. Traefik invokes the service
before forwarding an allowed request to the configured upstream.

- `connectors/traefik/src/traefik_forwardauth_service_main.c` defines the host
  profile, original-URI header preferences, mapper callbacks, and service entry
  point.
- `connectors/traefik/src/traefik_modsecurity_mapper.c` contains thin C17
  wrappers around the Common generic configuration, request, and response
  mappers.
- `common/runtime/http_authorization_service.c` and
  `common/runtime/msconnector_runtime.c` own the neutral HTTP lifecycle,
  libmodsecurity transaction, decision, intervention, and event handling.
- The runtime smoke forwards only `X-Modsec-Smoke` and `X-Request-Id` as explicit
  authorization request headers.
- `forwardAuth` returns an authorization decision; it does not provide this
  connector with the later upstream response. The linked response mapper is not
  evidence of upstream response inspection.

## Common SDK adoption

The live connector path initializes Common configuration through
`msconnector_generic_config_init()`, maps requests through
`msconnector_generic_map_request()`, and uses Common runtime APIs for rule
loading, transaction IDs, limits, decisions, interventions, metadata events,
and JSONL serialization. Traefik-specific profile and File Provider data remain
under `connectors/traefik/`.

The repository checks completed successfully:

```sh
make check-traefik-common-adoption
make check-remaining-connectors-host-integration
```

## Configuration

`connectors/traefik/config/traefik-forwardauth.conf` maps the enabled flag,
rules file, transaction-ID header, body modes and limits, default block/error
statuses, event path, and header/event resource limits into Common
configuration. `traefik-forwardauth-dynamic.yaml` supplies the real File
Provider `forwardAuth` and upstream wiring for the start smoke.

The Common template uses `request_body_mode=none` because the selected
`forwardAuth` path does not deliver the original request body to the service.
The numeric 4096-byte request-body limit remains a parser/resource setting, not
host capability, and the produced result explicitly records
`request_body_verified` as false. Response-body mode is also `none`. Inline
rules, remote rules, and broader directive combinations were not exercised.

## Build, config, start, and runtime evidence

| Stage | Reproduction command | Observed evidence | Boundary |
|---|---|---|---|
| Build | `make build-traefik-connector` | C17 compile with `-Wall -Wextra -Werror`; service linked to local libmodsecurity with a local `RUNPATH` | Compile/link only; no service self-test or request |
| Config | `make check-traefik-config` | Built service accepted the Common configuration with `--check-config` | Does not start Traefik |
| Start | `make start-smoke-traefik` | Service and real Traefik stayed alive with generated File Provider config, then stopped without a request | Process-lifecycle evidence only |
| Runtime | `make runtime-smoke-traefik` | Real Traefik -> `forwardAuth` -> Common/libmodsecurity path returned 200 and rule-backed 403; expected event found; processes stopped | Two targeted GET/header cases only |

The observed local runtime evidence is outside the checkout:

- Build artifact:
  `/var/tmp/ModSecurity-conector-verified/build/traefik-connector/traefik-forwardauth`
- Runtime result:
  `/var/tmp/ModSecurity-conector-verified/build/traefik-connector/runtime-smoke/result.json`
- Runtime event:
  `/var/tmp/ModSecurity-conector-verified/build/traefik-connector/runtime-smoke/logs/events.jsonl`

The result records allowed status 200, blocked status 403, Common runtime path,
rule `1000001`, and false values for request-body, response-body, upstream
response processing, CRS completeness, and broad-matrix readiness. The event
identifies transaction `traefik-forwardauth-block` and contains no body payload
field. These local artifacts are not a retained multi-platform CI run.

Missing local executables are reported as BLOCKED with exit 77. Once inputs are
resolved, configuration, startup, mapping, HTTP status, and event mismatches are
failures.

## Known limits and remaining technical gaps

- The selected real `forwardAuth` path has no request-body runtime evidence.
- The connector cannot inspect upstream response headers, metadata, or bodies in
  this pre-request integration model.
- No response phase or late intervention is available on the tested path.
- Inline/remote rule sources, content-type policies, truncation cases, redirects,
  drop/abort behavior, concurrency, resilience, and performance remain open.
- No CRS execution, full No-CRS/with-CRS matrix, security assessment, or
  deployment hardening was performed.
- The evidence covers one local Traefik version and one targeted rule only.

## Claims supported by the evidence

- A real repository-owned Traefik `forwardAuth` path exists and uses the Common
  SDK and runtime.
- The connector service builds and links against local libmodsecurity.
- Config validation and a request-free service-plus-Traefik start/stop smoke pass
  locally.
- The targeted request-header host path has `minimal_runtime_smoke` evidence for
  allowed HTTP 200 and rule-backed HTTP 403 with a metadata-only event.

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- full-matrix verification
- request-body, upstream-response, or response-body verification
- broad Traefik-version or platform compatibility
- verification of all connectors
