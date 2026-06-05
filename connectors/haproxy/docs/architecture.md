# HAProxy Architecture

Status: spoa-agent-starter
Runtime status: not-verified

This document records HAProxy-specific integration evidence and blockers. Global
status vocabulary, scaffold rules, promotion gates, and runtime-evidence rules
remain in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Repository Evidence Reviewed

- `connectors/haproxy` contains SPOE/SPOA planning material and example files.
- No SPOP frame parser, SPOE/SPOA protocol library, or verified HAProxy runtime
  harness exists in this repository.
- `common/include/msconnector/` contains connector-neutral data shapes for
  origin, status, request, intervention, and other connector concepts.
- `connectors/apache` and `connectors/nginx` contain productive adapter source,
  origin/source maps, metadata, and harness files, but their server APIs and
  lifecycle code are server-specific and are not reused for HAProxy.
- The parent `Makefile` dispatches Apache and NGINX runtime smokes through the
  external framework; no HAProxy runtime smoke dispatch exists in the parent
  `Makefile` or framework at this commit.

## Current HAProxy Integration Decision

Selected minimal path: local SPOA agent starter.

Reason: SPOE/SPOA is the most concrete HAProxy-specific path already referenced
by this connector's planning docs and example snippets, but the repository does
not include enough protocol or harness evidence to claim a compatible SPOA
implementation. The next honest step is therefore a local starter binary that
uses shared request/intervention/status shapes and proves only local
request-decision code through `--self-test`.

The starter is intentionally limited to:

- compiling repo-authored metadata;
- compiling a local `haproxy-spoa-agent-starter` binary;
- evaluating synthetic requests in process;
- producing a local allow/block self-test result.

The starter does not parse SPOP frames, open a network socket, start HAProxy,
load CRS, or call libmodsecurity.

## Deferred Integration Options

Possible approaches to evaluate later, without treating any as implemented:

- complete SPOE/SPOA agent with selected SPOP parser/library
- native HAProxy filter/service integration
- external processing/service bridge
- sidecar/proxy integration

## Blockers Before Adapter Ownership

- selected SPOP frame parser or SPOE/SPOA protocol library
- verified HAProxy SPOE/SPOA configuration against a running HAProxy
- selected libmodsecurity binding strategy for HAProxy
- HAProxy harness capable of starting HAProxy and the starter/agent component
- runtime evidence for No-CRS and With-CRS scopes

Each approach must be backed by origin/license metadata, build evidence, harness
evidence, and No-CRS/With-CRS runtime results before promotion beyond
spoa-agent-starter or partial status is considered.
