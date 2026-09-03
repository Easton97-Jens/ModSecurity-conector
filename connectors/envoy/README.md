# Envoy Connector

**Language:** English | [Deutsch](README.de.md)

Status: `minimal_runtime_smoke` / `connector-gap`

The implemented host model is an external HTTP authorization service for
Envoy's `ext_authz` filter. The connector owns the Envoy profile and thin Common
SDK mapper callbacks; the connector-neutral engine and HTTP service lifecycle
remain in `common/runtime/`.

The direct `ext_authz` protocol is a request-phase integration. It can receive
bounded request headers and a buffered request body and translate a Common
decision into an authorization response. On its own, `ext_authz` does not
expose upstream response headers or response bodies, so the direct protocol is
not a P3/P4-capable host adapter.

The named `envoy-ext-authz` logical connector therefore requires the private
MRC1 response companion described in the [canonical Envoy guide](../../docs/connectors/envoy.md).
It retains the same live Common/native transaction from completed P2 to P3/P4
rather than reconstructing a request snapshot. The response observer is
mandatory: omitting it is a configuration error, and observer or correlation
failure is fail-closed. This is source/component wiring with state
`implemented_not_asserted`; it is not a claim that an arbitrary Envoy
deployment has loaded the required templates.

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
in `minimal`/`safe` is recorded as host-confirmed `log_only`. The service
decoder can represent `late_action_policy: strict`, but a rule-evaluating CGo
service with `phase4_mode=strict` rejects the `envoy-ext-proc` profile at
startup until a deterministic post-commit host action is proven. It never
claims a late status change, deterministic reset, client reset, or upstream
reset.

The exact ext_proc API boundary, opt-in client-cancel observation, and
non-promotion conditions are documented in the
[canonical Envoy guide](../../docs/connectors/envoy.md).

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
connector service, and Envoy, then requires an allowed HTTPS 200 and a
rule-backed `X-Modsec-Smoke: block` HTTPS 403 through an ephemeral private
loopback TLS listener. The local `ext_authz` sidecar remains an internal
loopback HTTP service. Missing binaries are BLOCKED; config, process, mapping,
and status errors fail the smoke. All processes are stopped on success or
failure.

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

## Direct `ext_authz` boundary and logical Phase-4 contract

The direct Envoy HTTP `ext_authz` protocol asks the authorization service
before upstream handling and never exposes the later upstream response to that
service. In the legacy direct capability table,
`response_body_buffered`, `phase4`, `phase4_rule_evaluation`,
`phase4_pre_commit_deny`, `late_intervention`, `late_intervention_log_only`,
`late_intervention_abort`, and `late_intervention_status_metadata` are
therefore `unsupported_by_host_model`, not merely unverified. A request-phase
allow or deny, including a real request-side 200 or 403, is not response-phase
evidence for that direct protocol.

That boundary does not make P3/P4 not-applicable for the complete
`envoy-ext-authz` logical connector. Its required chain hands the live Common
transaction from `ext_authz` after P2 to the private-UDS `ext_proc` response
observer through a server-generated opaque handle. The observer claims the
handle exactly once, strips it before the upstream request, sends P3 before
response commitment, sends bounded P4 chunks plus exactly one EOS, and then
releases or cancels deterministically. Missing, malformed, expired, replayed,
or unavailable correlation is a configuration or protocol failure and fails
closed before response commitment.

Accordingly, a shared P4 case is `UNSUPPORTED` only for an unpaired direct
`ext_authz` protocol. The logical connector must use its required observer for
P3/P4 or fail as misconfigured; it must never silently relabel those phases as
unsupported. No response-body payload is written to events or reports.
