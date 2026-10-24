# ADR-003: Shared P1--P4 lifecycle semantics

**Language:** English | [Deutsch](ADR-003-shared-p1-p4-lifecycle-semantics.de.md)

## ID

ADR-003

## Status

accepted

## Date

2026-08-25

## Context

The ten named connector solutions expose different host callbacks and protocol
boundaries. The product nevertheless needs one source-derived meaning for P1,
P2, P3, and P4, one decision taxonomy, bounded retained state, and deterministic
lifecycle cleanup. This decision is limited to Parent source, local tests, and
documentation. CI, branch governance, Rulesets, and Required Checks are out of
scope.

Implementation evidence defines P1 as request headers after Connection/URI
prerequisites and before request commitment; P2 as bounded request-body
ingestion with exactly one request EOS decision; P3 as response headers before
response commitment while the original status remains mutable; and P4 as
bounded response-body ingestion with exactly one response EOS decision.
Connection, URI, and Logging remain host lifecycle prerequisites or epilogues,
not additional business phases.

No versioned Change Record is associated at this point: the repository archive
policy requires an explicit record decision, and no delivery is eligible while
the ten-solution acceptance criteria remain incomplete.

## Decision

Use `msconnector_transaction_contract` as the one canonical, fixed-size Common
transaction record and finite-state machine for every named connector solution.
It owns validated transaction and host identities, P1--P4 ordering, bounded
request/response metadata and body counters, decision/rule-ID/action/mode/error
correlation, time fields, response commitment, and cleanup state. Retained
contract/event state contains metadata only, never request or response payload
bytes.

Each host adapter selects one explicit connector profile. A profile either maps
a phase directly through a host callback or marks P3/P4 as
`COMPANION_REQUIRED`. A request-only protocol may satisfy the latter only with
a mandatory private response companion that hands off and claims a
server-generated opaque capability exactly once. The response component is part
of the logical connector solution, not an optional capability fallback.

The shared MRC1 response-companion transport remains the authority for bounded
framing, private UDS identity, timeout, cleanup, and response-operation order.
The HAProxy SPOE/SPOP bridge uses the Common protocol/parser core plus an
owner-preserving SPOP backend; it does not copy MRC1 framing or expose a native
transaction pointer to the HTX process. The selected Stock lighttpd solution
is the traffic-owning `stock-lighttpd-sidecar`: a private literal-loopback
HTTP/1.1 sidecar owns one bounded exchange and executes P1--P4 directly. The
native `stock-lighttpd` module route remains an explicit noncanonical P1/P3
compatibility translation and is never an implicit fallback. The patched
lighttpd route remains a distinct connector solution.

## Alternatives

1. Keep independent host-specific phase meaning and decision policy. Rejected:
   it permits divergent business semantics and inconsistent cleanup.
2. Declare P3/P4 `not_applicable` for request-only protocols. Rejected: it
   removes required response protection instead of solving the protocol boundary.
3. Add a traffic-owning generic sidecar for Stock lighttpd. Selected for the
   canonical Stock solution: the sidecar is a deliberately bounded private
   loopback HTTP/1.1 traffic owner, while the native Stock module remains an
   explicit P1/P3 compatibility translation rather than a fallback.
4. Duplicate MRC1 in a HAProxy-local UDS server. Rejected: framing, limits,
   peer authentication, capability handling, timeout, and cleanup would drift
   from Common.

## Consequences

Direct adapters must begin and complete each phase exactly once, record bounded
metadata/body counters, map decisions through the Common taxonomy, and finish
or cancel before cleanup. Companion adapters must retain no unbounded
cross-transaction state, must use opaque single-claim correlation with a
bounded capacity and TTL, and must fail closed for missing, expired, replayed,
or malformed correlation.

Host actions remain host-specific translations. A pre-commit Block or Redirect
may become a mutable HTTP response; a post-commit Strict decision may become a
documented connection abort when the host cannot safely rewrite bytes. This is
a translation difference, not a change to the canonical decision meaning.

The decision deliberately leaves current evidence gaps visible. It does not
promote source wiring to a native Stock-module host-runtime pass: P2/P4 are
provided by the separately selected traffic-owning sidecar, not by the
unchanged Stock module. It also does not treat an unintegrated HAProxy
companion as a complete P1--P4 route. The sidecar binds only to literal
loopback, owns cleanup in one worker, and therefore needs no cross-process
correlation or TTL registry; its event JSONL remains metadata-only.

## Security impact

The contract enforces header, body, event, frame, capacity, and TTL limits;
rejects invalid, duplicate, skipped, late, terminal, and cleaned phase
transitions; and makes cancel, timeout, engine/protocol failure, and incomplete
cleanup explicit terminal outcomes. MRC1 requires an owner-only parent
directory, a private socket, supported peer credentials, bounded frames, and
an opaque capability that is not a client-controlled transaction identity.

Event JSONL is metadata-only. There is no body payload, native transaction
pointer, host identity, or unbounded request key on the response-observer wire
boundary. No silent version or capability fallback is permitted.

## Test and evidence impact

The mandatory local contract suite covers valid/invalid order, duplicate and
missing phases, limits, all canonical decision types in Safe/Strict modes,
timeouts, cancel, cleanup, capacity recovery, parallel transactions, and two
sequential transactions on one MRC1 connection. Adapter source/component tests
cover their narrow host translations. Isolated Envoy `ext_authz` and Traefik
`forwardAuth` runtime receipts exercise their response companions.

This ADR makes no full ten-solution production-runtime-pass claim. In
particular, native Apache/NGINX/lighttpd host receipts remain separately
evidenced; the canonical Stock P2/P4 evidence is for the sidecar component,
while the unchanged native Stock module remains P1/P3-only. The HAProxy
combined MRC1-v2 evidence is local and qualified, not a blanket
production-readiness claim.

## Affected documentation

- `common/docs/transaction-phase-contract.md`
- `common/docs/transaction-phase-contract.de.md`
- `common/docs/design.md`
- `common/docs/design.de.md`
- `docs/architecture.md`
- `docs/architecture.de.md`
- `connectors/*/capabilities.json`
