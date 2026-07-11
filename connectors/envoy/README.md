# Envoy Connector

**Language:** English | [Deutsch](README.de.md)

**Language:** English | [Deutsch](README.de.md)

Status: `minimal_runtime_smoke` / `connector-gap`

The implemented host model is an external HTTP authorization service for
Envoy's `ext_authz` filter. The connector owns the Envoy profile and thin Common
SDK mapper callbacks; the connector-neutral engine and HTTP service lifecycle
remain in `common/runtime/`.

This is a request-phase integration. It can receive bounded request headers and
a buffered request body and translate a Common decision into an authorization
response. `ext_authz` does not expose upstream response headers or response
bodies to this service, so response inspection remains unsupported and no
response-body claim is made.

## Source layout

- `src/envoy_ext_authz_service_main.c` defines the Envoy host profile, original
  URI header preferences, and the service entry point.
- `src/envoy_modsecurity_mapper.c` contains thin C17 calls to the Common generic
  request and response mappers.
- `config/envoy-ext-authz.conf` is the checked-in configuration template.
- `config/prepare_envoy_config.sh` creates a concrete runtime copy outside the
  checkout and substitutes rule/event paths.
- `build/build_connector.sh` performs a compile/link-only C17 build.
- `harness/start_envoy_connector.sh` validates Envoy config, starts and observes
  both Envoy and the service, and stops both without sending a request.

The older `envoy_bridge` CLI remains a local decision self-test. It is not used
by the `ext_authz` service and is not runtime evidence.

## Build, config, and start separation

Provide local libmodsecurity paths directly or through the Framework-managed
environment:

```sh
make -C connectors/envoy build-envoy-connector \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

The build target only compiles and links. It does not run the service or a
self-test.

Validate a concrete configuration, optionally overriding the rule file from the
command line:

```sh
make -C connectors/envoy check-envoy-config \
  RULES_FILE=/absolute/path/to/rules.conf
```

Run the request-free Envoy-plus-service start smoke:

```sh
make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absolute/path/to/envoy \
  RULES_FILE=/absolute/path/to/rules.conf
```

Run the real Envoy host-path smoke with a prepared Envoy binary:

```sh
make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absolute/path/to/envoy \
  RULES_FILE=/absolute/path/to/rules.conf
```

This target validates a generated temporary Envoy config, starts the upstream,
connector service, and Envoy, then requires an allowed HTTP 200 and a
rule-backed `X-Modsec-Smoke: block` HTTP 403. Missing binaries are BLOCKED;
config, process, mapping, and status errors fail the smoke. All processes are
stopped on success or failure.

For an operator-controlled foreground service:

```sh
make -C connectors/envoy serve-envoy-connector \
  RULES_FILE=/absolute/path/to/rules.conf \
  LISTEN_ADDRESS=127.0.0.1 LISTEN_PORT=18082
```

The template config enables request processing, uses `x-request-id` as the host
transaction ID header, caps request bodies at 4096 bytes, disables response-body
processing, uses 403/500 block/error defaults, applies explicit header/event
limits, and writes metadata-only JSONL outside the checkout.

## Current evidence boundary

- The service is C17 compile/link verified and the targeted real Envoy request
  path has `minimal_runtime_smoke` evidence. Verification remains
  `connector-gap` outside that narrow scope.
- A service build or request-free start does not prove an Envoy runtime request;
  only `runtime-smoke-envoy` exercises that host path.
- The Framework's older Python `ext_authz` decision service is separate from
  this connector binary and must not be used as evidence for this implementation.
- No production, security, CRS-complete, full-matrix, response-header, or
  response-body verification claim is made.

## Canonical Phase-4 boundary

The selected host model is Envoy HTTP `ext_authz`.  It asks the authorization
service before upstream handling and never exposes the later upstream response
to that service.  `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` are therefore
`unsupported_by_host_model`, not merely unverified.

Every shared Phase-4 case for this integration must be `UNSUPPORTED`, with the
reason that the selected ext_authz integration executes before the upstream
response and does not expose upstream response-body data.  A request-phase
allow or deny, including a real request-side 200 or 403, is not response-phase
evidence.  The service cannot supply original upstream status, visible client
status after a late intervention, or a post-commit action because no such host
event reaches it.

`UNSUPPORTED` describes this chosen architecture; it never counts as `PASS`.
No response-body payload is written to events or reports.
