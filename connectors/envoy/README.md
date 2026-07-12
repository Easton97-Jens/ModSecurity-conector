# Envoy Connector

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

## Separate, non-promoted `ext_proc` full-lifecycle host path

`ext_proc/` adds a separate Go service selected by the full-lifecycle profile,
based on Envoy's official generated Go protobuf/gRPC API. Its checked-in Envoy
template uses `STREAMED` request and
response body modes, with bounded per-stream counters and incremental callback
delivery; it never selects `BUFFERED` processing. The pinned module and Envoy
release record are in `ext_proc/go.mod`, `ext_proc/go.sum`, and
`config/envoy-ext-proc-versions.env`.

The normal `ext_proc` build is a CGo executable that links a connector-local
ABI to Common Runtime and libmodsecurity. Each real Envoy `Process` stream
opens one Common transaction from Envoy's request headers, forwards bounded
incremental request and response data, and closes it at EOS, cancellation, or
processor failure. Common's run-local raw decision JSONL is the canonical
event source; the payload-free stream-completion JSONL is supplementary only.

`runtime-smoke-envoy-ext-proc` validates the materialized YAML, starts Envoy,
the CGo/Common gRPC service, and an upstream, then exercises P1, P2, P3 deny,
P3 redirect, and P4 safe post-commit log-only behavior. It validates the raw
Common events and the host-confirmed actions after successful gRPC sends. This
is real local host evidence, but it remains non-promoted and does not change
the canonical `ext_authz` capabilities or runtime status. A late P4 decision
in `minimal`/`safe` is recorded as host-confirmed `log_only`; `strict` remains
`strict_abort_not_attempted`. It never claims a late status change,
deterministic reset, client reset, or upstream reset.

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
- `ext_proc/` contains the separately buildable CGo/Common ext_proc stream
  service and its focused unit/CGo lifecycle tests;
  `config/envoy-ext-proc-streaming.yaml.in` is its non-promoted streamed-mode
  template.

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

The independent ext_proc full-lifecycle service has its own commands. Its
normal executable requires explicit libmodsecurity headers and library paths:

```sh
make -C connectors/envoy build-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy test-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-runtime-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc \
  ENVOY_BIN=/absolute/path/to/envoy \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

The source-only Go tests remain useful for protobuf and transport behavior; when
the explicit paths are supplied, the build/test target additionally compiles the
Common archive, links libmodsecurity, and runs the tagged CGo lifecycle tests.
The runtime target writes its effective Common config and raw Common events
under a run-local root. It provides connector-local rule/action evidence but
does not promote a capability or substitute for canonical collection.

## Current evidence boundary

- The service is C17 compile/link verified and the targeted real Envoy request
  path has `minimal_runtime_smoke` evidence. Verification remains
  `connector-gap` outside that narrow scope.
- A service build or request-free start does not prove an Envoy runtime request.
  `runtime-smoke-envoy` exercises the selected `ext_authz` host path, while
  `runtime-smoke-envoy-ext-proc` separately exercises the non-promoted
  Common/libmodsecurity `ext_proc` host path.
- The Framework's older Python `ext_authz` decision service is separate from
  this connector binary and must not be used as evidence for this implementation.
- No production, security, CRS-complete, full-matrix, response-header, or
  response-body verification claim is made.
- The ext_proc service has isolated real-Envoy Common/libmodsecurity host
  evidence for its bounded HTTP/1.1 P1/P2/P3/P4 probes, including raw Common
  rule decisions and host-confirmed deny/redirect/log-only actions. It has no
  timeout, reset, first-byte, HTTP/2, client-byte observation, canonical
  collector, or capability-promotion evidence.

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
