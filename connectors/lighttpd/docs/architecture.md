# lighttpd Architecture

Status: native module, `minimal_runtime_smoke` for a Phase-1 header rule

## Runtime flow

```text
lighttpd handle_uri_clean
  -> lighttpd request mapper
  -> Common request contract and resource limits
  -> Common/libmodsecurity transaction begin
  -> allow or http_status_set_err(...)

lighttpd handle_response_start
  -> lighttpd response mapper
  -> Common response contract and resource limits
  -> Common/libmodsecurity response processing

lighttpd handle_request_reset
  -> transaction finish and destroy
  -> mapped header storage release
```

`module/mod_msconnector.c` is the only plugin-lifecycle layer.
`src/lighttpd_modsecurity_mapper.c` is the only host-mapping layer. The Common
runtime and all Common SDK types remain free of lighttpd headers and callback
types.

## Plugin lifecycle

The module exports `mod_msconnector_plugin_init` for the lighttpd loader and
registers:

- `init` to allocate plugin state;
- `set_defaults` to register host directives, validate the Common runtime
  config, load rules, and construct the shared runtime;
- `handle_uri_clean` for request metadata and request headers;
- `handle_response_start` for response metadata and response headers;
- `handle_request_reset` for transaction finalization and cleanup;
- `cleanup` to destroy the Common runtime.

The directives are server-scoped. A single runtime is created from
`msconnector.config-file`; each request receives its own transaction and mapper
storage in `r->plugin_ctx`.

## Mapping and ownership

The request mapper exposes method, original target, HTTP version, hostname,
client address/port, server name/port, and every lighttpd string header as a
length-delimited Common header. The response mapper exposes status, HTTP
version, and response headers.

Header count and total-byte limits are checked before runtime entry. The Common
DoS/resource guard applies the configured per-name, per-value, body, and other
limits. Header values remain slices and are never treated as unvalidated C
strings.

The Common runtime borrows the mapped request and response. Therefore the
handler context owns the mapped header arrays until `handle_request_reset`.
All mapper-error and transaction-begin error paths release their owned state.

## Decisions and events

A disruptive request-header decision is converted to an error response using
lighttpd's `http_status_set_err()`. The verified rule requests status 403.
Runtime or mapper errors use the Common error-to-HTTP mapping. Redirect, drop,
connection-abort, and late-intervention semantics have not been separately
verified by this narrow smoke.

The Common runtime owns rule loading, transaction IDs, flow guards,
libmodsecurity calls, decisions, event construction, integrity metadata, and
JSONL serialization. The stock connector mode passes no request or response
body payload to that event path.

## Body boundary

The stock mode overrides both mapper contracts to
`MSCONNECTOR_MAPPER_UNSUPPORTED` and maps a zero-length body. The native smoke
config sets `request_body_mode=none` and `response_body_mode=none`.

The separate full-lifecycle-selected lighttpd 1.4.84 patch appends a versioned
ABI for borrowed HTTP/1.x request-body ranges and identity entity-response
ranges. The response callback is invoked in `http_chunk_append_mem()` and
`http_chunk_append_buffer()` before this core applies HTTP/1 transfer framing;
it is not a socket-queue callback. The selected filter order is
application/backend → selected identity entity range → msconnector callback →
HTTP/1 transfer framing → socket. The callback receives only a synchronous
borrowed pointer and length, advances a monotonic entity offset, and signals
EOS once. It retains no connector-owned body queue.

The patched binding can incrementally pass request and response ranges to
Common Runtime when the corresponding mode is `streaming`. Buffered request
mode remains rejected. The selected response scope is identity only: gzip/br,
HTTP/2, and unexamined file/zero-copy output routes are not asserted as body
inspection paths. Short writes and `EAGAIN` occur after the one-time append
callback, so the structural contract cannot duplicate entity ingestion on a
socket retry; that behavior still lacks a real-host fault-injection run.

The patched host has a narrow real Phase-1 200/403 smoke, but this is not P4
runtime evidence. It does not yet prove a client-observed Phase-4 rule, safe
outcome, strict abort, truncation, first byte, or no-full-buffer result.
Safe/minimal source behavior records `log_only`; strict intentionally remains
`NOT EXECUTED` because no client-validated lighttpd abort primitive is present.

## Alternative paths

The legacy bridge starter and framework `sidecar_proxy` smoke remain separate
artifacts. The primary connector path is now the native module. FastCGI, SCGI,
and mod_magnet/Lua are not implemented by this module.

## Current claim boundary

The verified 200/403 smoke supports `minimal_runtime_smoke` and
`partial_runtime_path` only. It does not support production-ready, security
verified, CRS verified, response-body verified, or full-matrix claims.
