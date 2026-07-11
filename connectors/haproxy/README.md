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
HAProxy `unique-id`, keeps bounded transactions for response phases, emits
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
messages. The bounded Phase-4 response-body branch is source-level wiring and
is not canonical evidence for rule observation, strict abort, or full
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
- RESPONSE_BODY blocking: bounded experimental source path only; not promoted.

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
documented as `BLOCKED`. `RESPONSE_BODY` rows stay non-promoted unless a future
canonical host run proves the individual response-body and late-intervention
facets beyond the current bounded experimental path.

## Common SDK adoption boundary

The HAProxy adoption layer embeds/maps `msconnector_config` and uses Common directive specs/adapters, parser primitives, mapper contracts, header helpers, event JSONL helpers, rule-id/log-sanitizing primitives, and global guard structures where implemented. HAProxy-specific SPOE/SPOP protocol handling, cfg glue, process lifecycle, socket/runtime handling, frame parsing, return/action encoding, logging transport, and build glue remain local.

C17 compile evidence is available through `make check-haproxy-c17`; optional C23/future-C checks depend on compiler support. Missing HAProxy/libmodsecurity headers are reported as `BLOCKED` with exit 77. This is not a production, CRS, full-matrix, or runtime-verification claim.

## Canonical Phase-4 boundary

HAProxy uses the repository SPOE/SPOP agent path, including a bounded
experimental response-body branch.  Source wiring alone does not establish
that the agent sees a complete upstream response, that HAProxy can still
change its status, or that a disconnect is a Phase-4 action rather than an
agent failure.  Only `response_body_buffered`, `phase4`, and
`phase4_rule_evaluation` remain `implemented_not_asserted` as source-level
paths. `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` are `not_implemented`.

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
