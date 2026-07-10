# Envoy Connector Validation

Status: connector service `compile_verified`; targeted Envoy ext_authz request
path `minimal_runtime_smoke` / `connector-gap`.

## Config validation

`config/envoy-ext-authz.conf` is an immutable example template. The launcher
creates a concrete copy under `BUILD_ROOT`, replacing only the rules and event
paths. Both may be supplied as command-line/Make inputs:

```sh
make -C connectors/envoy check-envoy-config \
  RULES_FILE=/absolute/path/rules.conf \
  EVENT_LOG_PATH=/absolute/runtime/path/events.jsonl
```

The built service executes `--check-config --config PATH`. Invalid syntax,
unknown keys, unsafe paths, rule-load errors, invalid statuses or limits fail
the check.

## Request-free start smoke

```sh
make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy \
  RULES_FILE=/absolute/path/rules.conf
```

This gate config-checks the connector, validates generated Envoy YAML, starts
both connector service and Envoy, records both PIDs/liveness states, sends no
request, stops both, and writes a summary outside the checkout.

## Real Envoy runtime smoke

```sh
make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy \
  RULES_FILE=/absolute/path/rules.conf
```

The smoke:

1. creates a temporary Envoy `ext_authz` YAML config;
2. validates it with Envoy;
3. starts a local upstream, connector service, and Envoy;
4. requires an allowed request to return HTTP 200;
5. requires `X-Modsec-Smoke: block` to trigger rule `1000001` and HTTP 403;
6. requires a metadata-only Common event;
7. stops all processes on success, failure, or signal.

Only absent executables/rule inputs are BLOCKED/77. Config rejection, early
process exit, request failure, incorrect status, or missing event evidence is a
real failure.

Observed local implementation evidence is written outside the checkout under
the selected `BUILD_ROOT`. It records `response_body_verified=false` and
`production_ready=false`. Body payloads are not written to the event log.

## Limits

- The implemented model is request-phase HTTP `ext_authz`.
- Request bodies are buffered to at most 4096 bytes; partial messages are not
  allowed by the smoke config.
- Upstream response headers and response bodies are not available to this
  protocol and remain unsupported.
- The targeted 200/403 smoke is not CRS-complete, full-matrix, security, or
  production evidence.
