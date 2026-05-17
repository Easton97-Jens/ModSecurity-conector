# Common Runtime Boundaries

Status: implemented

Phase 3 adds the first real Common C implementation files, but only for
connector-neutral metadata helpers.

## What Common Contains Now

`common/src/` contains small helpers for:

- `msconnector_status`: C name conversion and runtime-result mapping.
- `msconnector_intervention`: construction and disruptive-state checks.
- `msconnector_origin`: origin construction and empty-origin checks.
- `msconnector_capabilities`: capability flag naming and flag composition.

These helpers depend only on the C standard library and
`common/include/msconnector/*`.

## Harness Relationship

The Apache/NGINX smoke runners do not load these helpers through FFI. Python
uses `tests/runners/msconnector_models.py` as a schema-compatible mirror for the
same status, origin, intervention, and capability names.

That means:

- connector smokes keep their existing Python/Shell execution model;
- Common C helpers are validated independently by `ci/check-common-helpers.sh`;
- summary JSON remains backward-compatible and append-only.

## Explicit Non-Boundaries

Common does not own:

- Apache hook registration or bucket brigades;
- NGINX module registration, phase handlers, or filters;
- request body or response body handling;
- libmodsecurity object ownership or transaction lifetime;
- `RESPONSE_BODY` behavior.

Any future extraction touching those areas requires separate evidence and
passing real-world connector smokes.
