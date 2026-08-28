# Traefik response observer

**Language:** English | [Deutsch](README.de.md)

This local plugin is the response-only adapter for the canonical transaction
contract. It must run after the C `forwardAuth` service. The service emits one
server-generated `X-Msconnector-Response-Handle`, and Traefik's
`authResponseHeaders` must allow only that header; the plugin consumes exactly
one handle, removes it before invoking the upstream handler, and sends P3/P4
frames to the private Unix socket configured in `socketPath`.

The wire protocol is bounded `MRC1` version 2 with 12-byte headers, a 64 KiB
frame limit, and 32 KiB response chunks. Its one-byte `CANCEL` payload carries
the canonical terminal cause (client cancel, upstream disconnect, connector or
protocol failure, engine timeout/unavailable, or invalid engine response).
There is no version-1 fallback: a mismatched listener fails closed. The plugin
does not carry transaction or host identifiers, does not open P1/P2, and does
not implement a second state machine. Invalid, missing, replayed, or
unavailable handles fail closed before upstream response commitment. A
disruptive result after commitment is reported as log-only and cannot rewrite
the response. The wrapper intentionally exposes neither `Unwrap` nor
`Hijacker`.

Run `../build/build-response-observer.sh test` from this repository to execute
the local unit and vet checks. This is source-level evidence; it does not claim
a Traefik host runtime.
