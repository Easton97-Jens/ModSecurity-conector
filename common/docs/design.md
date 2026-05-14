# Common Design

Status: scaffolded

## Boundary

`common/` is connector-neutral. It may define request, response, transaction,
logging, and capability types that can be used by tests and connector adapters,
but it must not include or depend on any server/proxy SDK.

## C-first interface

The shared headers are C-first because the locally analyzed Apache and NGINX
connectors call libmodsecurity through its C API. The C++ headers are thin
aliases over the C structs, not a separate ownership model.

This does not implement a complete connector API. It defines neutral data shapes
that later connector adapters can translate to libmodsecurity v3 calls.

## libmodsecurity v3 alignment

The phase names mirror the public v3 transaction sequence:

- connection metadata
- URI
- request headers
- request body
- response headers
- response body
- logging

The actual calls to libmodsecurity belong in connector adapters or a future
engine-facing layer with explicit ownership rules. They are not hidden in
`common/` until their lifetime, error, and cleanup contracts are documented.

## TODO

- Define ownership rules for header and body buffers.
- Decide whether neutral helpers should return structured errors or integer
  status codes.
- Add compile tests proving these headers remain independent of every connector.
