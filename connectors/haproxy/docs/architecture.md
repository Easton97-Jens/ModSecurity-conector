# HAProxy Architecture

Status: live-yaml-spoa-runtime (partial)
Runtime status: live request-side YAML execution through HAProxy, SPOA/SPOP,
and libmodsecurity.

This document records HAProxy-specific integration evidence and blockers. Global
status vocabulary, scaffold rules, promotion gates, and runtime-evidence rules
remain in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Repository Evidence Reviewed

- `connectors/haproxy` contains SPOE/SPOA planning material and example files.
- A request-side SPOP runtime subset exists for local protocol diagnostics and
  live framework YAML execution. It parses HAProxy `method`, `uri`,
  `req.hdrs_bin`/`req.hdrs`, and `req.body` SPOE arguments. No full production
  SPOE/SPOA protocol library exists in this repository.
- `common/include/msconnector/` contains connector-neutral data shapes for
  origin, status, request, intervention, and other connector concepts.
- `connectors/apache` and `connectors/nginx` contain productive adapter source,
  origin/source maps, metadata, and harness files, but their server APIs and
  lifecycle code are server-specific and are not reused for HAProxy.
- The parent `Makefile` dispatches HAProxy runtime smoke through the external
  framework; the HAProxy target now verifies shared request-side YAML cases and
  CRS SQLi anomaly blocking.

## Current HAProxy Integration Decision

Selected minimal path: local SPOA agent starter plus a request-side SPOP
runtime subset plus a local ModSecurity binding.

Reason: SPOE/SPOA is the most concrete HAProxy-specific path already referenced
by this connector's planning docs and example snippets, but the repository does
not include enough protocol or harness evidence to claim a compatible SPOA
implementation. The next honest step is therefore a local starter binary that
uses shared request/intervention/status shapes and proves only local
request-decision code through `--self-test`. The runtime subset proves local
HELLO/AGENT-HELLO, NOTIFY argument parsing, verified set-var ACK encoding, and
DISCONNECT handling. `make smoke-haproxy` then proves HAProxy can enforce live
request-side YAML decisions through SPOA/SPOP. The ModSecurity binding
self-tests still prove only in-process binding behavior by themselves.

The starter is intentionally limited to:

- compiling repo-authored metadata;
- compiling a local `haproxy-spoa-agent-starter` binary;
- evaluating synthetic requests in process;
- producing a local allow/block self-test result;
- producing local libmodsecurity phase-1 header block and request-body
  self-test results;
- producing live HAProxy enforcement evidence for shared request-side YAML
  cases;
- producing live HAProxy CRS evidence for `crs_sqli_anomaly_block` with the
  prepared local CRS preamble.

The synthetic starter binary does not parse SPOP frames, open a network socket,
start HAProxy, load CRS, or enforce libmodsecurity decisions through HAProxy.

The SPOP runtime subset may open local loopback sockets during
`self-test-spoa-runtime` and `make smoke-haproxy`, but it is not a full
production SPOA agent implementation and does not verify response-phase or
`RESPONSE_BODY` behavior. Request-body evidence is bounded by HAProxy request
buffering, SPOE `max-frame-size 65532`, HAProxy `tune.bufsize 65536`, and one
`req.body` argument.

The ModSecurity binding self-test runs a local transaction, but it is not a
HAProxy runtime smoke by itself and may not set `runtime_verified` to true.

## Deferred Integration Options

Possible approaches to evaluate later, without treating any as implemented:

- complete SPOE/SPOA agent with selected SPOP parser/library
- native HAProxy filter/service integration
- external processing/service bridge
- sidecar/proxy integration

## Blockers Before Adapter Ownership

- full production SPOA/SPOP implementation beyond the request-side runtime
  subset
- full HAProxy SPOE/SPOA runtime integration beyond the current request-side
  subset
- response phase evidence
- audit/log evidence
- redirects and non-403 disruptive status mapping
- `RESPONSE_BODY` evidence

Each approach must be backed by origin/license metadata, build evidence, harness
evidence, and No-CRS/With-CRS runtime results before promotion beyond
partial status is considered.
