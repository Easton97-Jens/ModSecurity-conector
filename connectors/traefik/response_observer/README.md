# Traefik response observer

**Language:** English | [Deutsch](README.de.md)

By default this local plugin is the response-only adapter for the canonical transaction
contract. It must run after the C `forwardAuth` service. The service emits one
server-generated `X-Msconnector-Response-Handle`, and Traefik's
`authResponseHeaders` must allow only that header; the plugin consumes exactly
one handle, removes it before invoking the upstream handler, and sends P3/P4
frames to the private Unix socket configured in `socketPath`.

The optional trusted provenance mode instead runs **outermost**, before the
built-in ForwardAuth middleware. Set `provenanceSocketPath`, `runID`, and
`transportCaseID` together, and set `MSCONNECTOR_TRAEFIK_PROVENANCE_SOCKET` to
the same sibling socket in the C Traefik ForwardAuth service. The service owns
a separate Traefik-only `MTP1` v1 listener; the canonical MRC1 wire protocol
and ordinary/default call paths are unchanged. Both
processes must share the expected effective Unix UID/GID. The socket must not
already exist and its canonical parent must be service-owned mode 0700.

Use this exact chain order: outer observer → built-in ForwardAuth → inner
observer with `confirmProvenance: true` → backend. The inner instance must not
set `provenanceSocketPath`, `runID`, or `transportCaseID`. ForwardAuth's explicit
`authRequestHeaders` allow-list must include
`X-Msconnector-Trusted-Reservation`. The inner observer confirms the private
reply before invoking the backend and removes that header and
`X-Msconnector-Response-Handle`, including trailer declarations.
The observer removes client reservation headers/trailers and client handles,
reserves privately before invoking the next handler, and injects only a random
one-time capability into the immediate authorization hop. Its own final strip
is additional cleanup; it cannot replace the inner confirmation instance.

MTP1 accepts three bounded, nonempty ASCII identifiers (128 bytes each) and a
zero reuse byte. At most 128 reservations live for 5 seconds each. Closure,
expiry, malformed or duplicate frames, a missing/duplicate/forged token, and
an already consumed token fail closed. The C service atomically claims and
copies the private metadata before native P1, then removes the capability
from native request headers. A private completion query binds the actual
authorization reply status or response-companion handle to that same lease.
The package-private request context binds inner confirmation to its outer
reservation; missing or duplicate confirmation fails closed. Cached private
attestation keeps backend waiting time outside the five-second reservation
window. MRC1 initially expires after at most five seconds. Before releasing
an Allow handle, the peer-authenticated inner MTP1 query confirms it exactly
once under the Common registry lock, extending only that unused, still-valid
handle to its original configured handoff deadline (30 seconds for Traefik).
This grants only the remaining handoff lifetime, not a fresh 30 seconds.
Backend waiting consumes this remaining absolute lifetime and fails closed
when the configured handoff deadline expires.
Expired, claimed, replayed, foreign or shutdown entries and confirmation
callback failures fail closed before backend entry. Deny/empty handles do not
extend any entry. Ordinary MRC1 clients retain the five-second preclaim limit.
Normal MRC1 `CLAIM` occurs at the first response header. Panic,
cancellation or return before any header instead claims the cached handle
only for immediate typed `CANCEL`, using a detached bounded cleanup context.
A cleanup failure is retained and emits a fixed payload-free physical log
signal; the confirmed handle's bounded expiry remains its fallback.
The outer observer forwards a terminal authorization response only when its
status matches the private attestation; an Allow opens the attested MRC1
handle. No client HTTP field can supply identifiers or the attestation.

`connection_id` is an instance-local HMAC of trusted Go local/remote socket
tuples. It is opaque correlation: tuple recycling is possible and the plugin
has no ConnState close hook. Therefore `connection_reused` remains false;
physical same-live-socket evidence is still required for a keepalive claim.
Neither Forwarded headers nor the authorization service's loopback socket
determine downstream connection identity. Common deep-copies identifiers
before P1, uses actual body-finish state for `eos_seen`, and emits its final
integrity-chained cleanup record only after native Free and contract cleanup.
That event proves runtime cleanup, not client delivery or native EOS from TCP
EOF. The existing `maxResponseBodySize=32768` remains solely authorization
response capacity and must remain configured.

The wire protocol is bounded `MRC1` version 2 with 12-byte headers and 32 KiB
response chunks. All non-P3 frames remain limited to 64 KiB. A P3
`RESPONSE_HEADERS` frame may use a payload of up to 66,630 bytes across MRC1 peers;
this HTTP/1.1 observer emits at most 66,574 payload bytes, while the logical header
name/value aggregate remains capped at 64 KiB. Its one-byte `CANCEL` payload
carries the canonical terminal cause (client cancel, upstream disconnect,
connector or protocol failure, engine timeout/unavailable, or invalid engine
response).
There is no version-1 fallback: a mismatched listener fails closed. The plugin
in default mode does not carry transaction or host identifiers, does not open P1/P2, and does
not implement a second state machine. Invalid, missing, replayed, or
unavailable handles fail closed before upstream response commitment. A
disruptive result after commitment is reported as log-only and cannot rewrite
the response. The wrapper intentionally exposes neither `Unwrap` nor
`Hijacker`.

Before its first `CLAIM` frame, the observer authenticates the connected
response-companion server with Linux `SO_PEERCRED`. By default it expects the
observer's effective UID and GID. Deployments using a different companion
identity must set both `expectedPeerUID` and `expectedPeerGID` in the plugin
configuration; either value may explicitly be `0`. Missing credentials, an
identity mismatch, or a non-Linux platform fails closed before the upstream
handler runs. The companion's private socket directory and its full ancestor
chain must also resist cross-UID replacement. Matching Unix IDs form one trust
domain: `SO_PEERCRED` does not attest binary integrity, security labels, or
user-namespace mapping.

Run `../build/build-response-observer.sh test` from this repository to execute
the local unit and vet checks. This is source-level evidence; it does not claim
a Traefik host runtime.
