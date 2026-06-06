# HAProxy Architecture

Status: production-spoa-runtime (partial)
Runtime status: live YAML execution through HAProxy, SPOA/SPOP, and
libmodsecurity using the repo-built `haproxy-modsecurity-spoa` production
agent.

This document records HAProxy-specific integration evidence and blockers. Global
status vocabulary, scaffold rules, promotion gates, and runtime-evidence rules
remain in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Repository Evidence Reviewed

- `connectors/haproxy` contains SPOE/SPOA planning material and example files.
- A production SPOP runtime exists for local protocol diagnostics and live
  framework YAML execution. It parses request and response SPOE messages,
  keeps ModSecurity transactions by HAProxy `unique-id`, emits decision JSONL,
  and returns typed ACK variables for HAProxy enforcement.
- `common/include/msconnector/` contains connector-neutral data shapes for
  origin, status, request, intervention, and other connector concepts.
- `connectors/apache` and `connectors/nginx` contain productive adapter source,
  origin/source maps, metadata, and harness files, but their server APIs and
  lifecycle code are server-specific and are not reused for HAProxy.
- The parent `Makefile` dispatches HAProxy runtime smoke through the external
  framework; the HAProxy target now verifies shared request-side YAML cases and
  CRS SQLi anomaly blocking.

## Current HAProxy Integration Decision

Selected path: local SPOA agent starter plus a production SPOP runtime plus a
local ModSecurity binding.

Reason: SPOE/SPOA is the most concrete HAProxy-specific path already referenced
by this connector's planning docs and example snippets. The repository now
builds a production agent that loads ModSecurity rules once, processes request
phases, preserves transactions for response headers and bounded response body
inspection, and writes per-phase decision evidence. `make smoke-haproxy` proves
HAProxy can enforce live YAML decisions through this SPOA/SPOP path. The
ModSecurity binding self-tests still prove only in-process binding behavior by
themselves.

The starter is intentionally limited to:

- compiling repo-authored metadata;
- compiling a local `haproxy-spoa-agent-starter` binary;
- evaluating synthetic requests in process;
- producing a local allow/block self-test result;
- producing local libmodsecurity phase-1 header block and request-body
  self-test results;
- producing live HAProxy enforcement evidence for shared YAML cases;
- producing live HAProxy CRS evidence for `crs_sqli_anomaly_block` with the
  prepared local CRS preamble.

The synthetic starter binary does not parse SPOP frames, open a network socket,
start HAProxy, load CRS, or enforce libmodsecurity decisions through HAProxy.
The production runtime does those jobs and is the only HAProxy runtime path the
YAML harness uses.

Request-body evidence is bounded by HAProxy request buffering, SPOE
`max-frame-size`, HAProxy `tune.bufsize`, and configured body limits. Response
header evidence is live. Phase 4 response body evidence is bounded by
`http-response wait-for-body`, SPOE frame size, `--response-body-limit`, and
timeout; it remains experimental and non-promoted for full `RESPONSE_BODY`.

The ModSecurity binding self-test runs a local transaction, but it is not a
HAProxy runtime smoke by itself and may not set `runtime_verified` to true.

## Deferred Integration Options

Possible approaches to evaluate later, without treating any as implemented:

- complete SPOE/SPOA agent with selected SPOP parser/library
- native HAProxy filter/service integration
- external processing/service bridge
- sidecar/proxy integration

## Blockers Before Adapter Ownership

- broader production hardening of the minimal in-repo SPOP parser
- arbitrary dynamic disruptive status mapping beyond fixed HAProxy rules
- full-body `RESPONSE_BODY` guarantees beyond bounded experimental probes
- multi-worker lifecycle and long-running cache pressure validation

Each approach must be backed by origin/license metadata, build evidence, harness
evidence, and No-CRS/With-CRS runtime results before promotion beyond
partial status is considered.
