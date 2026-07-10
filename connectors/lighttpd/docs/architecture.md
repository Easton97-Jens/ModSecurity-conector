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
JSONL serialization. The connector passes no request or response body payload
to that event path.

## Body boundary

lighttpd request and response bodies are not implemented in this module.
Regardless of the runtime's general capabilities, the module overrides both
mapper contracts to `MSCONNECTOR_MAPPER_UNSUPPORTED` and maps a zero-length
body. The native smoke config sets `request_body_mode=none` and
`response_body_mode=none`.

This boundary prevents compile/start/header evidence from being mislabeled as
body evidence. Body buffering, truncation metadata, Phase 2, Phase 4, and late
intervention remain future work.

## Alternative paths

The legacy bridge starter and framework `sidecar_proxy` smoke remain separate
artifacts. The primary connector path is now the native module. FastCGI, SCGI,
and mod_magnet/Lua are not implemented by this module.

## Current claim boundary

The verified 200/403 smoke supports `minimal_runtime_smoke` and
`partial_runtime_path` only. It does not support production-ready, security
verified, CRS verified, response-body verified, or full-matrix claims.
