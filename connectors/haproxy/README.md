# HAProxy Connector

**Language:** English | [Deutsch](README.de.md)

Status: partial; historical SPOA runtime records do not promote canonical
Phase-4 capabilities.
Runtime status: the repository contains live YAML execution wiring through
HAProxy, SPOA/SPOP, and a repo-built `haproxy-modsecurity-spoa` agent.
Request-side evidence is separate from response-body and late-intervention
evidence. `RESPONSE_BODY` remains non-promoted.
Template alignment: scaffold-aligned plus local SPOA agent starter/runtime.

This connector contains repository-owned metadata, a local HAProxy SPOA agent
starter, a production SPOP runtime, and a local libmodsecurity binding. The
production agent loads ModSecurity rules once, creates transactions with the
HAProxy `unique-id`, keeps bounded transaction state for its request and
optional response-header phases, emits
decision JSONL, and returns typed SPOE ACK variables for HAProxy enforcement.
`make smoke-haproxy` lists shared framework YAML cases with `case_cli.py`,
materializes each case, starts HAProxy plus the production SPOA agent plus a
backend, sends the case request with curl, asserts the observed status, and
writes the standard HAProxy summary artifacts.

`make runtime-matrix-haproxy` consumes live summary evidence from the split
No-CRS and With-CRS HAProxy runs. PASS/FAIL rows must come from live HAProxy
execution; structurally unmappable rows use `NOT_EXECUTABLE`, and real
environment/build/runtime blockers use `BLOCKED`.

The proven request-side variables are `REQUEST_URI`, `REQUEST_HEADERS`,
`REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`,
`REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES`, and `XML`. URL-encoded,
JSON, XML, multipart, and CRS SQLi anomaly request-body coverage is live
evidence, limited by HAProxy request buffering, SPOE frame size, and configured
request-body limits. Response-header and audit-log paths use SPOE response
messages. A separate optional HTX observer overlay has source-level
response-body wiring for bodyless requests only; it is not the active SPOP
path and is not canonical evidence for rule observation, strict abort, or full
`RESPONSE_BODY` support.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

Shared connector-neutral data shapes used by the starter:

- `common/include/msconnector/origin.h`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`
- `common/src/intervention.c`

## HAProxy-specific State

- Origin/license: documented for repo-authored starter only; upstream HAProxy
  connector source is not selected.
- Metadata: `metadata.c` and `metadata.h` present.
- Build: metadata object and local SPOA agent starter build are present.
- Self-test: local starter self-test exists; it does not start HAProxy.
- SPOP runtime: buildable and self-testable under
  `/src/ModSecurity-conector-build/haproxy-spoa-runtime/` as
  `haproxy-modsecurity-spoa`; the harness and normal deployments use this same
  binary path.
- ModSecurity binding self-test: buildable and self-testable under
  `/src/ModSecurity-conector-build/haproxy-modsecurity-binding/`; verifies
  phase-1 header blocking and request-body append/processing in process.
- Harness: `make smoke-haproxy` verifies live HAProxy to SPOA/SPOP to
  libmodsecurity enforcement for shared framework YAML cases.
- Decision evidence: per-case `decision.jsonl`, HAProxy logs, SPOA logs, audit
  logs, observed status, and normalized `result.json`.
- RESPONSE_BODY blocking: not implemented in the active harness; the former
  `wait-for-body` sample is disabled. The optional native HTX observer is
  nonselected, bodyless-request-only, and does not promote this capability.

## Build Starter

For the complete repository-supported HAProxy compile and local verification
flow, see the root guide: [`COMPILE_HAPROXY.md`](../../COMPILE_HAPROXY.md).
The connector-local notes below describe status and target scope only.

Supported local build targets:

```sh
make -C connectors/haproxy build-metadata
make -C connectors/haproxy build-spoa-starter
make -C connectors/haproxy build-starter
make -C connectors/haproxy self-test-spoa
make -C connectors/haproxy self-test
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-spoa-runtime
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding-crs
```

`build-spoa-starter` compiles a local binary that can describe its limitations
and run a synthetic allow/block decision self-test. It does not compile HAProxy,
does not compile a HAProxy module, does not parse SPOP frames, does not run as a
verified SPOA server, and does not link libmodsecurity.

`build-spoa-runtime` compiles `haproxy-modsecurity-spoa`. Its self-test is
protocol compatibility evidence; `make smoke-haproxy` is the live gate that
starts HAProxy against this production agent and executes framework YAML cases.

`build-modsecurity-binding` first verifies the local libmodsecurity C API
signatures through a compiled probe, then builds a small self-test binary.
`self-test-modsecurity-binding` proves in-process phase-1 header blocking and
request-body processing. `make smoke-haproxy` is required for live HAProxy
runtime evidence.

## Tests

No local `connectors/haproxy/tests` folder is used. Executable runtime tests are
framework-owned.

Framework-owned paths and targets to use for future evidence:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make runtime-matrix-haproxy`
- `make test-haproxy-no-crs`
- `make test-haproxy-with-crs`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

Unsupported or currently unmaterializable rows are documented as
`NOT_EXECUTABLE`. Harness, dependency, build, and runtime failures are
documented as `BLOCKED`. `RESPONSE_BODY` rows stay unselected/not implemented
until a future native host response-chunk path proves the individual
response-body and late-intervention facets without `wait-for-body`.

## Common SDK adoption boundary

The HAProxy adoption layer embeds/maps `msconnector_config` and uses Common directive specs/adapters, parser primitives, mapper contracts, header helpers, event JSONL helpers, rule-id/log-sanitizing primitives, and global guard structures where implemented. HAProxy-specific SPOE/SPOP protocol handling, cfg glue, process lifecycle, socket/runtime handling, frame parsing, return/action encoding, logging transport, and build glue remain local.

C17 compile evidence is available through `make check-haproxy-c17`; optional C23/future-C checks depend on compiler support. Missing HAProxy/libmodsecurity headers are reported as `BLOCKED` with exit 77. This is not a production, CRS, full-matrix, or runtime-verification claim.

## Canonical Phase-4 boundary

HAProxy uses the repository SPOE/SPOP agent path for request and optional
response-header handling.  Its old bounded response-body sample depended on
`http-response wait-for-body`; it is deliberately disabled because a sample
wait is not a genuine response-chunk API and would violate the low-latency
contract.  `response_body_buffered`, `phase4`, and
`phase4_rule_evaluation` are therefore `not_implemented` in the selected
SPOE/SPOP path until that path uses a native HTX/filter adapter with borrowed
response chunks and an explicit end of stream. `phase4_pre_commit_deny`,
`late_intervention`, `late_intervention_log_only`,
`late_intervention_abort`, and `late_intervention_status_metadata` are also
`not_implemented`.

The agent currently serializes policy-derived pre-commit fields, but the host
runner does not observe a client-visible Phase-4 deny, actual commitment timing,
or a post-commit response point.  It therefore implements neither safe
`log_only` nor strict `abort_connection`, and cannot claim semantic
original/requested/visible-status metadata.  An agent timeout, agent failure,
or generic HAProxy disconnect is not evidence of a late-intervention abort.

The shared Phase-4 case set remains evidence-gated. Rule observation is
separate from a client-visible 403; the semantic pre-commit, late-action, and
status-metadata cases remain `NOT_EXECUTED` until their missing host behavior
is implemented. Response-body payloads must never be written to events or
reports.

## Optional native HTX observer overlay

`htx-overlay/` contains a source-linked HAProxy **3.2.21** observer filter for
the native HTX `http_payload` and `http_end` callbacks. It is built into a
disposable upstream worktree, not into the selected SPOE/SPOP runtime:

```sh
make -C connectors/haproxy check-htx-overlay
HAPROXY_HTX_SOURCE_DIR=/path/to/haproxy-3.2.21 \
HAPROXY_HTX_BUILD_DIR=/var/tmp/haproxy-htx-overlay \
MODSECURITY_INCLUDE_DIR=/path/to/include \
MODSECURITY_LIB_DIR=/path/to/lib \
make -C connectors/haproxy build-htx-overlay
```

The overlay forwards only the current borrowed `HTX_BLK_DATA` slices to the
binding and finishes Phase 4 once at response EOS. It neither uses
`wait-for-body`/`res.body` nor keeps a connector-owned response buffer.
It is intentionally observer-only after response commitment: a late rule is
logged without a fabricated deny, redirect, or abort. The current binding also
limits this experimental path to bodyless requests, because its request-body
phase is still atomic.

This optional overlay is not configured by the checked-in SPOP harness and is
not canonical No-CRS evidence. Therefore it does **not** promote the selected
SPOE/SPOP Phase-4, late-intervention, no-buffer, or first-byte capabilities.
