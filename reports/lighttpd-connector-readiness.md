# lighttpd Connector Readiness

**Language:** English | [Deutsch](lighttpd-connector-readiness.de.md)

Evidence snapshot: 2026-07-10

## Outcome

The lighttpd connector has status `minimal_runtime_smoke`, limited to one local,
targeted native-module request-header path. A real lighttpd 1.4.84 process loaded
`mod_msconnector.so`; baseline `OPTIONS *` returned HTTP 200, and the same host
path with `X-Modsec-Smoke: block` returned HTTP 403 from libmodsecurity rule
`1000001` through the Common decision path.

Both request- and response-body modes are deliberately unsupported by the
native module. The evidence does not cover response behavior beyond the
implemented header hook, CRS, a broad test matrix, security assessment, or
operational deployment.

## Architecture and host integration

The primary integration is a repository-owned native lighttpd module, not the
older bridge starter or framework sidecar smoke.

- `connectors/lighttpd/module/mod_msconnector.c` implements plugin
  initialization, server-scope configuration, request lifecycle, and cleanup.
- `handle_uri_clean` maps request metadata and headers, begins the Common
  transaction, processes the request phase, and maps a disruptive decision with
  `http_status_set_err()`.
- `handle_response_start` maps response metadata and headers into the Common
  response API; the targeted smoke does not assert a response-specific rule or
  intervention.
- `handle_request_reset` finishes and destroys the transaction and frees the
  connector-owned mapped arrays.
- `connectors/lighttpd/src/lighttpd_modsecurity_mapper.c` owns host-specific
  mapping and keeps lighttpd types outside `common/`.

## Common SDK adoption

The module initializes configuration through
`msconnector_generic_config_init()`, calls the Common generic request and
response mappers, and uses Common runtime APIs for rule loading, transaction
state and IDs, limits, decisions, interventions, flow/integrity metadata,
events, and JSONL serialization. Header ownership remains connector-local for
the transaction lifetime.

The repository checks completed successfully:

```sh
make check-lighttpd-common-adoption
make check-remaining-connectors-host-integration
```

## Configuration

The lighttpd host config registers `msconnector.enabled` and
`msconnector.config-file`. The referenced Common `key=value` file maps the rules
file, transaction-ID header, body policies and limits, block/error statuses,
event path, and header/event limits.

The native module requires both body modes to be `none`. A negative config check
confirmed that `request_body_mode=buffered` is rejected at module load. The
numeric body-limit fields remain parser/resource settings, not body-processing
capability. Inline rules, remote rules, content-type policy, and broader
directive combinations were not exercised.

## Build, config, start, and runtime evidence

| Stage | Reproduction command | Observed evidence | Boundary |
|---|---|---|---|
| Build | `make build-lighttpd-connector` | C17 PIC compile with `-Wall -Wextra -Werror`; native shared module linked to local libmodsecurity with a local `RUNPATH` | Compile/link only; no implicit self-test |
| Config | `make check-lighttpd-config` | Real lighttpd `-tt` loaded `mod_msconnector.so`, accepted host/Common config, initialized libmodsecurity, and loaded the targeted rule | Does not start request traffic |
| Start | `make start-smoke-lighttpd` | Real foreground process stayed alive, then stopped; output records `requests=0` | Process-lifecycle evidence only |
| Runtime | `make runtime-smoke-lighttpd` | Real lighttpd/module path returned baseline 200 and rule-backed 403; expected event found; process stopped | Two targeted `OPTIONS *` request-header cases only |

The four root targets also completed together:

```sh
make build-lighttpd-connector check-lighttpd-config \
  start-smoke-lighttpd runtime-smoke-lighttpd
```

Observed local artifacts are outside the checkout:

- Native module:
  `/var/tmp/ModSecurity-conector-verified/build/lighttpd-connector/modules/mod_msconnector.so`
- Build inventory:
  `/var/tmp/ModSecurity-conector-verified/build/lighttpd-connector/build-info.txt`
- Generated smoke config and logs:
  `/var/tmp/ModSecurity-conector-verified/build/lighttpd-connector/smoke/`
- Runtime event:
  `/var/tmp/ModSecurity-conector-verified/build/lighttpd-connector/smoke/events.jsonl`

The runtime event identifies connector `lighttpd`, request-header phase, rule
`1000001`, and HTTP 403, and contains no request/response body payload field.
These local artifacts are not a retained multi-platform CI run.

The historical `build-lighttpd-bridge` and `self-test-lighttpd-bridge` targets
are separate. The native build does not run either self-test, and bridge
self-test output is not counted as native host runtime evidence.

## Known limits and remaining technical gaps

- Request-body capture, Phase 2, truncation behavior, and body content-type
  processing are unsupported.
- Response-body capture, Phase 4, and late intervention are unsupported.
- Although the response-header hook is implemented and loaded, the targeted
  smoke does not assert response-header mapping or a response-phase decision.
- Redirect, drop, connection-abort, multi-worker/thread stress, long-running
  resilience, and performance remain open.
- No CRS execution, full No-CRS/with-CRS matrix, security assessment, or
  deployment hardening was performed.
- The evidence covers one local lighttpd version and one targeted rule only.

## Claims supported by the evidence

- A real repository-owned native lighttpd module exists and uses the Common SDK
  and runtime.
- The native module builds, links, and loads in real lighttpd 1.4.84 locally.
- Config validation and a request-free real lighttpd start/stop smoke pass.
- The targeted request-header path has `minimal_runtime_smoke` evidence for
  baseline HTTP 200 and rule-backed HTTP 403 with a metadata-only event.
- Native build, bridge self-test, start smoke, and runtime smoke are separate
  evidence stages.

## Claims deliberately not made

- production readiness or production hardening
- runtime security or security verification
- CRS verification or CRS completeness
- full-matrix verification
- request-body, response-header, or response-body verification
- broad lighttpd-version or platform compatibility
- verification of all connectors
