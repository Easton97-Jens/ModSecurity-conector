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

## Phase 5 Replace-And-Reduce Boundary

Phase 5 reviewed the next possible upstream reduction and made no code
replacement. The remaining helper-looking functions are still inside
connector-owned runtime areas:

- Apache utility code includes output bucket/error behavior.
- NGINX string conversion is used by config parsing and request metadata.
- NGINX PCRE allocation helpers are part of config/rules lifecycle.
- NGINX response-header helpers and log callback are filter/audit paths.

Common may continue to define neutral metadata shapes, but it must not absorb
these paths until a connector adapter owns the behavior and real-world smoke
results prove compatibility.

## Phase 6 Adapter-Owned Boundary

Phase 6 adds the first adapter-owned source skeletons under
`connectors/apache/src/` and `connectors/nginx/src/`. These files are not Common
runtime code and are not linked into the productive Apache or NGINX modules.

The adapter-owned metadata helpers:

- expose stable connector source/origin fields in an `msconnector_origin`
  compatible shape;
- contain no Apache or NGINX server headers;
- contain no libmodsecurity internals;
- contain no request, response, body, filter, intervention, or transaction
  lifecycle behavior;
- are validated only by `ci/check-adapter-helpers.sh` under `$BUILD_ROOT`.

This creates a place for future adapter-owned replacements without changing the
current real-world connector path. Any production use still requires a separate
replace-and-reduce phase and passing before/after smokes.

## Phase 7 Reporting Integration

Phase 7 allows adapter-owned metadata to feed build and runtime summaries. The
smoke scripts read the metadata through `ci/adapter_metadata.py`, a local parser
with no FFI or C runtime dependency. The reporting order is explicit env
override, external source git metadata, then adapter-owned monorepo metadata.

The summary JSON gains `origin.source_url` append-only. Existing result status,
case discovery, `verified_variables`, YAML semantics, and `RESPONSE_BODY`
classification remain unchanged.

## Phase 8 Shadow Build Boundary

Phase 8 lets NGINX build from a generated connector source tree under
`$BUILD_ROOT`. The tree is assembled from imported upstream files plus
adapter-owned overlays and contains local manifests. This changes only the build
input location for the monorepo-default NGINX source.

The generated tree does not create Common ownership of NGINX filters, request
mapping, body handling, transaction lifecycle, or intervention behavior. Apache
receives the same generated source evidence, but its module build remains on the
existing sanitized upstream copy in this phase.
