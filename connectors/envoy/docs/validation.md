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

## Canonical Phase-4 validation

Envoy HTTP `ext_authz` is invoked before upstream handling.  The chosen host
path cannot observe upstream response headers or body, so
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort`, and `late_intervention_status_metadata` are
`unsupported_by_host_model`.

The canonical Phase-4 cases must consequently be `UNSUPPORTED`, with this
exact host-model boundary as their reason.  The request-side allow/deny smoke
cannot prove a response-body rule, pre-commit response deny, post-commit
log-only result, abort, original upstream status, or visible post-intervention
status.  `UNSUPPORTED` is not `PASS`, and no response-body payload is allowed
in an event or report.

## Separate ext_proc checks

The Go ext_proc groundwork has the following connector-local checks:

```sh
make -C connectors/envoy test-envoy-ext-proc
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc ENVOY_BIN=/absolute/path/to/envoy
```

The unit test covers protobuf service compilation plus bounded streamed callbacks,
EOS cleanup, cancellation cleanup, a pre-response `ImmediateResponse`, and the
fact that a late strict action is recorded as `strict_abort_not_attempted` rather
than as an abort. The template has `STREAMED` body modes and no `BUFFERED` mode.
The runtime smoke invokes real Envoy, selects only `ext_proc`, and records
payload-free request/response body counters. It does not invoke
Common/libmodsecurity, prove a rule action, timeout/reset/client-abort/upstream-
abort/first-byte behavior, or promote an ext_proc capability or runtime result.
