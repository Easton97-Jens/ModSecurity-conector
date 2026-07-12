# Traefik native transport-hardening boundary

**Language:** English | [Deutsch](transport-hardening.de.md)

This note applies only to the repository-owned native local-plugin path
(`native-traefik-middleware`) on the pinned Traefik `3.7.5` host. It does not
alter the separate `forwardAuth` compatibility path or promote a capability.

## API audit and strict boundary

The plugin's response-commit boundary is the successful delegation of
`WriteHeader` or a body write by `responseWriter`; it then records bounded
commit metadata through its UDS engine session. A late Phase-4 decision is not
an HTTP status rewrite.

| Downstream protocol | Public host surface | Selected behavior | Evidence state |
| --- | --- | --- | --- |
| HTTP/1.1 | `http.Hijacker` can take over a connection, if the actual wrapped writer supports it | The plugin preserves the interface for an upstream handler; it does not invoke `Hijack` for a rule decision | Strict post-commit abort is `NOT EXECUTED` |
| HTTP/2 | Go's `ResponseWriter` intentionally does not implement `http.Hijacker` for HTTP/2 | No request-local `RST_STREAM` path is present in the local-plugin API or selected harness | `NOT EXECUTED` |
| HTTP/3 | No repository-owned UDP/QUIC entry point or middleware stream-control path exists | Not configured | `NOT EXECUTED` |

The Go API documents that hijacking transfers ownership of the whole
connection, that wrappers may not implement it, and that HTTP/2 writers do not
support it. That is a connection-level HTTP/1.1 mechanism, not HTTP/2 stream
evidence. See the [Go `http.Hijacker` contract](https://pkg.go.dev/net/http#Hijacker).

Accordingly, the native UDS protocol currently exposes no rule-driven late
`abort_connection` outcome. A future HTTP/1.1 implementation must first prove
all of the following on the pinned Traefik host: a runtime-supported writer,
headers and one body byte already visible to a real client, an incomplete
declared body after closing only that connection, exactly-once cleanup, and a
healthy independent follow-up request. It must retain only the current bounded
chunk, never a full response. HTTP/2 needs a separate request-local reset hook
and an observed `RST_STREAM`; a Hijack result cannot be reused for it.

## Implemented bounded transport safeguards

`responseWriter` now marks a response incomplete when the wrapped writer
returns an error/short write or when `ReadFrom` returns an error. `finish()`
then skips the response EOS callback. The transaction still closes once, but a
downstream disconnect or upstream read failure cannot be relabelled as a normal
response EOS or a late strict outcome.

The isolated native host probe also uses one actual HTTP/1.1 connection for
the P4 Safe `log_only` request and a subsequent allow request. It requires the
same socket for both requests and writes a payload-free,
non-promoting `transport-observations.diagnostic.json` with:

- `response_committed`, `first_byte_received`, and `eos_received` observed by
  the test client;
- `connection_reused` and the independent follow-up result;
- a diagnostic case label, but no synthetic canonical correlation fields; and
- an explicit `strict.state = NOT_EXECUTED` boundary.

This diagnostic sidecar is not a canonical promotion artifact and is not enough to
promote keep-alive, strict, cancellation, HTTP/2, or HTTP/3 capabilities.

## Execution and non-claims

Run the selected host probe only with a locally provisioned pinned binary and
libmodsecurity inputs:

```sh
make -C connectors/traefik runtime-smoke-traefik-native
```

The source/unit tests cover the no-fabricated-EOS path and prove that a late
decision does not silently hijack a host connection. They are not a client
abort proof. No client-cancel, upstream-reset, timeout, HTTP/2 reset, or
HTTP/3 reset is promoted here.
