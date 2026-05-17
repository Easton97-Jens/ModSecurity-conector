# Common Design

Status: scaffolded

## Boundary

`common/` is connector-neutral. It may define request, response, transaction,
intervention, status, origin, logging, and capability types that can be used by
tests and connector adapters, but it must not include or depend on any
server/proxy SDK.

## C-first interface

The shared headers are C-first because the locally analyzed Apache and NGINX
connectors call libmodsecurity through its C API. The C++ headers are thin
aliases over the C structs, not a separate ownership model.

This does not implement a complete connector API. It defines neutral data shapes
that later connector adapters can translate to libmodsecurity v3 calls.

## Phase 1 foundation

The first controlled refactor phase adds only small connector-neutral data
shapes:

- `intervention.h` represents the data returned from an intervention check, but
  does not decide how a server sends the response.
- `status.h` defines generic operation outcomes, not HTTP status codes.
- `origin.h` records source/version/license metadata and does not imply code
  ownership or import status.

Existing `request.h`, `response.h`, `transaction.h`, `logging.h`, and
`capabilities.h` remain connector-neutral. `capabilities.h` is the canonical
capability header; no duplicate `capability.h` is introduced.

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
- Decide where neutral status values become part of future adapter APIs.
- Add compile tests proving these headers remain independent of every connector.
