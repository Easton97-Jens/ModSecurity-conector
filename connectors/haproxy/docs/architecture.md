# HAProxy Architecture

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`

This document records HAProxy-specific integration evidence and blockers. Global
status vocabulary, scaffold rules, promotion gates, and runtime-evidence rules
remain in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Repository Evidence Reviewed

- `connectors/haproxy` contains SPOE/SPOA planning material and example files.
- A minimal diagnostic SPOP handshake subset exists for local protocol
  diagnostics and the scoped live `haproxy_phase1_header_block` and
  `haproxy_crs_sqli_anomaly_block` enforcement smokes. No full SPOE/SPOA
  protocol library exists in this repository.
- `common/include/msconnector/` contains connector-neutral data shapes for
  origin, status, request, intervention, and other connector concepts.
- `connectors/apache` and `connectors/nginx` contain productive adapter source,
  origin/source maps, metadata, and harness files, but their server APIs and
  lifecycle code are server-specific and are not reused for HAProxy.
- The parent `Makefile` dispatches HAProxy runtime smoke through the external
  framework; the HAProxy target now verifies the phase-1 header block path and
  the minimal CRS SQLi anomaly path.

## Current HAProxy Integration Decision

Selected minimal path: local SPOA agent starter plus a minimal diagnostic SPOP
handshake subset plus a local ModSecurity binding.

Reason: SPOE/SPOA is the most concrete HAProxy-specific path already referenced
by this connector's planning docs and example snippets, but the repository does
not include enough protocol or harness evidence to claim a compatible SPOA
implementation. The next honest step is therefore a local starter binary that
uses shared request/intervention/status shapes and proves only local
request-decision code through `--self-test`. The diagnostic subset proves local
HELLO/AGENT-HELLO, NOTIFY argument parsing, verified set-var ACK encoding, and
DISCONNECT handling. `make smoke-haproxy` then proves HAProxy can enforce the
live phase-1 header block decision and the CRS SQLi anomaly decision through
SPOA. The ModSecurity binding self-tests still prove only in-process binding
behavior by themselves.

The starter is intentionally limited to:

- compiling repo-authored metadata;
- compiling a local `haproxy-spoa-agent-starter` binary;
- evaluating synthetic requests in process;
- producing a local allow/block self-test result;
- producing a local libmodsecurity phase-1 header block self-test result;
- producing live HAProxy enforcement evidence for `haproxy_phase1_header_block`;
- producing live HAProxy enforcement evidence for
  `haproxy_crs_sqli_anomaly_block` with the prepared local CRS preamble.

The synthetic starter binary does not parse SPOP frames, open a network socket,
start HAProxy, load CRS, or enforce libmodsecurity decisions through HAProxy.

The diagnostic SPOP subset may open local loopback sockets during
`self-test-spoa-runtime` and `make smoke-haproxy`, but it is not a full SPOA
agent implementation and does not verify RESPONSE_BODY behavior. CRS is
verified only for the single `haproxy_crs_sqli_anomaly_block` smoke.

The ModSecurity binding self-test runs a local transaction, but it is not a
HAProxy runtime smoke by itself and may not set `runtime_verified` to true.

## Deferred Integration Options

Possible approaches to evaluate later, without treating any as implemented:

- complete SPOE/SPOA agent with selected SPOP parser/library
- native HAProxy filter/service integration
- external processing/service bridge
- sidecar/proxy integration

## Blockers Before Adapter Ownership

- full SPOA/SPOP implementation beyond the diagnostic handshake subset
- full HAProxy SPOE/SPOA runtime integration beyond the diagnostic subset
- Framework case runtime beyond `haproxy_phase1_header_block` and
  `haproxy_crs_sqli_anomaly_block`
- runtime evidence for broader No-CRS and With-CRS scopes
- RESPONSE_BODY, negative/pass-through, and audit/log evidence

Each approach must be backed by origin/license metadata, build evidence, harness
evidence, and No-CRS/With-CRS runtime results before promotion beyond
partial status is considered.
