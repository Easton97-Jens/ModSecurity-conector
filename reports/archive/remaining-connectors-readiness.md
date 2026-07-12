> Status: Historical
> Superseded by: [../current/six-connector-core-completion.md](../current/six-connector-core-completion.md)
> Date: retained as a historical report during repository organization on 2026-07-12
> Evidence boundary: historical planning, assessment, or snapshot; not current canonical evidence.

# Remaining Connector Readiness: Envoy, Traefik, and lighttpd

**Language:** English | [Deutsch](remaining-connectors-readiness.de.md)

> **Evidence-scope note.** This is a historical local evidence snapshot, not a
> canonical No-CRS result or a current aggregate capability status. The
> `minimal_runtime_smoke` labels below refer only to the recorded 2026-07-10
> runs. The generated [all-connector No-CRS snapshot](../current/all-connectors-no-crs-baseline.md)
> and [canonical capability matrix](../testing/generated/canonical/connector-capabilities.generated.md)
> are authoritative for current status; only canonical `result.json` files can
> promote a No-CRS result.

Evidence snapshot: 2026-07-10

## Outcome

Envoy, Traefik, and lighttpd each have `minimal_runtime_smoke` evidence for one
narrow local request-header path through a real host process, the
repository-owned connector, Common runtime, and libmodsecurity. Each path proves
an allowed HTTP 200 and a rule `1000001` denial with HTTP 403 plus a
metadata-only event.

The evidence is deliberately connector-specific and narrow. It does not combine
into a claim about complete connector coverage. In particular, bodies,
responses, CRS, broad matrices, security, deployment hardening, and long-running
operation remain outside the proven scope.

## Gap Matrix

In this matrix, “passed” means the local 2026-07-10 evidence described below;
“implemented” without “asserted” means code exists but the targeted smoke did
not make a behavioral assertion for that column.

| Connector | Host integration | Common SDK | Config | Request | Request body | Response | Response body | Decision | Events | Build | Start | Minimal runtime |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Envoy | Real HTTP `ext_authz` service used by Envoy | Live config/generic mapper/runtime path | Common config check and Envoy YAML validation passed | Real GET/header path; 200/403 | 4096-byte buffering configured; not exercised | Upstream response unavailable to service | Unsupported | Rule `1000001` request decision -> 403 | Common JSONL metadata; no body payload | C17 service compile/link passed | Service + Envoy alive/stopped; zero requests | `minimal_runtime_smoke` |
| Traefik | Real HTTP `forwardAuth` service used by Traefik | Live config/generic mapper/runtime path | Service config and File Provider path passed | Real GET/header path; 200/403 | Not forwarded or exercised; result records false | Upstream response unavailable; authorization response only | Unsupported | Rule `1000001` request decision -> 403 | Common JSONL metadata; no body payload | C17 service compile/link passed | Service + Traefik alive/stopped; zero requests | `minimal_runtime_smoke` |
| lighttpd | Native `mod_msconnector.so` loaded by lighttpd | Live config/generic mapper/runtime path | Real module load and Common rule config passed | Real `OPTIONS *`/header path; 200/403 | Unsupported; mode must be `none` | Header hook implemented; no response-specific assertion | Unsupported; mode must be `none` | Phase-1 rule `1000001` -> 403 | Common JSONL metadata; no body payload | C17 PIC module compile/link passed | lighttpd alive/stopped; zero requests | `minimal_runtime_smoke` |

## Implemented architectures

### Envoy

The primary path is a repository-owned external HTTP authorization service for
Envoy `ext_authz`. Connector-local C17 code defines the Envoy host profile and
thin Common mapper callbacks. The shared HTTP authorization service and
libmodsecurity transaction runtime remain connector-neutral.

### Traefik

The primary path is a repository-owned external HTTP `forwardAuth` service. It
is neither a Go plugin nor cgo module. Traefik evaluates authorization before
the upstream request, so the connector has no later upstream response view.

### lighttpd

The primary path is a native repository-owned lighttpd plugin. It registers
server configuration, maps request and response headers, begins and finishes a
Common transaction, maps a Phase-1 denial to lighttpd, and cleans up at request
reset. Body modes are rejected unless set to `none`.

## Common SDK adoption

All three connectors use real functions rather than dead macro aliases:

- `msconnector_generic_config_init()`
- `msconnector_generic_map_request()`
- `msconnector_generic_map_response()`
- Common configuration parsing/validation and rule loading
- Common transaction-ID, decision/action, intervention, status, resource guard,
  flow/integrity, event, and JSONL paths

Host-specific types, profiles, callback signatures, and host configuration stay
under their connector directories. The aggregate static checks passed:

```sh
make check-remaining-connectors-common-adoption
make check-remaining-connectors-host-integration
make check-remaining-connectors-build-wiring
make check-remaining-connectors-start-wiring
```

## Reproduction commands and evidence

The repository-level wrappers resolve or provision managed local host binaries,
headers, and libmodsecurity paths. Build, config, start, and runtime remain
distinct evidence stages.

| Connector | Build | Config | Request-free start | Real host runtime |
|---|---|---|---|---|
| Envoy | `make build-envoy-connector` | `make check-envoy-config` | `make start-smoke-envoy` | `make runtime-smoke-envoy` |
| Traefik | `make build-traefik-connector` | `make check-traefik-config` | `make start-smoke-traefik` | `make runtime-smoke-traefik` |
| lighttpd | `make build-lighttpd-connector` | `make check-lighttpd-config` | `make start-smoke-lighttpd` | `make runtime-smoke-lighttpd` |

Aggregate entry points are:

```sh
make build-remaining-connectors
make start-smoke-remaining-connectors
make runtime-smoke-remaining-connectors
make readiness-remaining-connectors
```

The observed narrow runtime evidence was:

| Connector | Managed host version | Allowed | Blocked | Rule/event evidence |
|---|---:|---:|---:|---|
| Envoy | 1.38.2 | 200 | 403 | `envoy`, `envoy-block-1`, `1000001` |
| Traefik | 3.7.5 | 200 | 403 | `traefik`, `traefik-forwardauth-block`, `1000001` |
| lighttpd | 1.4.84 | 200 | 403 | `lighttpd`, request-header phase, `1000001` |

Default local evidence roots are below
`<verified-run-root>/build/`. They are reproducible workspace
artifacts, not retained multi-platform CI evidence. Missing pre-run dependencies
may be BLOCKED/77; resolved build, configuration, startup, mapping, status, or
event errors are failures.

## Cross-connector limits and remaining work

- Add bounded request-body delivery and behavioral tests where the host model
  can support it; keep the explicit unsupported boundary where it cannot.
- Add response-header assertions only for host models that actually expose the
  response, and do not infer response support from a linked generic mapper.
- Design response-body capture and late-intervention behavior only after a host
  hook and safe buffering model exist.
- Exercise inline/remote rules and broader Common directive combinations only
  after each host maps them explicitly.
- Add negative configuration, limits, truncation, malformed input, redirect,
  drop/abort, concurrency, resilience, and performance coverage.
- Run connector-appropriate No-CRS and CRS matrices before changing any broader
  evidence claim.
- Retain reproducible CI artifacts across supported platforms and host versions.
- Perform separate security review and operational hardening.

Connector-specific details are in:

- `reports/archive/envoy-connector-readiness.md`
- `reports/archive/traefik-connector-readiness.md`
- `reports/archive/lighttpd-connector-readiness.md`

## Claims supported by the evidence

- Each connector has one real host-integrated request-header path using Common
  runtime and libmodsecurity.
- Each connector's build, configuration check, request-free start smoke, and
  runtime smoke are distinguishable stages.
- Each targeted runtime path has `minimal_runtime_smoke` evidence for HTTP
  200/403 and metadata-only rule evidence.
- lighttpd's legacy bridge self-test is separate from native host runtime
  evidence.

## Claims deliberately not made

- production readiness or production hardening for any connector
- runtime security or security verification for any connector
- CRS verification or CRS completeness
- full-matrix verification
- request-body verification across all three connectors
- upstream-response or response-body verification
- broad platform or host-version compatibility
- verification of all connectors or of every connector capability
