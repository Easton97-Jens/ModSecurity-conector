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

The project records the full C vs C++ decision in
`docs/architecture/c-vs-cpp-decision.md`. In short: product connector cores stay C-first,
C++ remains limited to thin wrappers, build/test utilities, and optional helper
programs, and C++ objects must not cross Apache, NGINX, or future server ABI
boundaries.

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

`transaction.h` also owns the small `msconnector_decision` shape used by open
connector adapters to return neutral status, intervention, rule ID, and reason
data without creating connector-local Result types.

## Runtime-smoke evidence helpers

Connector-neutral smoke result helpers live under `common/scripts/`, not the
public C headers. They centralize Result/Evidence JSON writing for open
connector harnesses while keeping the runtime ABI focused on request, response,
intervention, status, logging, capabilities, origin, transaction, and decision
data.

These helpers may write common smoke artifacts such as `result.json`,
`summary.json`, `summary.txt`, and `results.jsonl`. They must not include
server-specific terms or depend on Envoy, Traefik, lighttpd, Apache, HAProxy, or
Nginx SDKs.

Runtime dependency discovery belongs to the test-framework shell helpers that
source `modules/ModSecurity-test-Framework/ci/common.sh`. Connector smokes must
use common.sh-managed paths or explicit environment variables such as
`ENVOY_BIN`, `TRAEFIK_BIN`, and `LIGHTTPD_BIN`. They must not install runtime
components globally or silently fall back to system `PATH`.

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

## Open Work

Tracked in `docs/roadmap/todo-inventory.md`:

- common ownership rules for header and body buffers;
- future adapter API use of neutral status values;
- compile tests proving Common headers remain independent of every connector.
