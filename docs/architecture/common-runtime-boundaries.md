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

Later phases moved productive connector build inputs into the same
adapter-owned source trees: NGINX in Phase 9/10 and Apache in Phase 11. That
does not make those sources Common-owned. Hooks, filters, bucket brigades,
configuration parsing, request/response mapping, intervention finalization,
and `RESPONSE_BODY` behavior remain connector-specific.

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
`$BUILD_ROOT`. At that point the tree was assembled from imported upstream
files plus adapter-owned overlays and contained local manifests. This changed
only the build input location for the monorepo-default NGINX source.

The generated tree does not create Common ownership of NGINX filters, request
mapping, body handling, transaction lifecycle, or intervention behavior. Apache
receives the same generated source evidence, but its module build remains on the
existing sanitized upstream copy in this phase.

## Phase 9 NGINX Adapter-Owned Source Boundary

Phase 9 moves NGINX productive source files into `connectors/nginx/src` and
builds the monorepo-default NGINX module from the generated
`$BUILD_ROOT/nginx-build/connector-src` tree. This is adapter-owned source
ownership, not Common runtime ownership.

Common still does not own:

- NGINX module registration;
- NGINX access, header, body, or log filters;
- phase-4 late intervention behavior;
- response-body blocking semantics;
- libmodsecurity transaction lifetime.

ModSecurity-nginx PR #377 source changes are documented as adapter-owned NGINX
source provenance. They do not make `RESPONSE_BODY` a verified variable and do
not affect Apache.

## Phase 10 NGINX Upstream Removal Boundary

Phase 10 removes the remaining NGINX upstream reference tree only after the
build input has already moved to adapter-owned source. This changes repository
layout and attribution storage, not runtime semantics. NGINX hooks, filters,
phase handlers, body handling, intervention behavior, and transaction ownership
remain connector-specific adapter-owned code, and Common still does not own
those paths.

## Phase 11 Apache Adapter-Owned Source Boundary

Phase 11 moves Apache productive source and Autotools/APXS build inputs into
`connectors/apache/src` and builds the monorepo-default Apache module from
`$BUILD_ROOT/apache-build/connector-src`. This is adapter-owned source
ownership, not Common runtime ownership.

Common still does not own:

- Apache hook registration;
- Apache input/output filters;
- bucket brigade/error response helpers;
- Apache config parsing;
- intervention finalization;
- libmodsecurity transaction lifetime;
- `RESPONSE_BODY` behavior.
