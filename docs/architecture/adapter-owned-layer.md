# Adapter-Owned Layer

Status: phase 6 skeleton

The adapter-owned layer is the first repo-owned connector code that sits beside
the imported upstream reference trees. It is intentionally not product runtime
code yet.

## Purpose

`connectors/<name>/src/` is reserved for small connector-owned helpers that are
safe to develop outside `connectors/<name>/upstream/`:

- stable connector metadata;
- origin and license descriptors;
- debug compatibility shims;
- future adapter-local helpers with explicit smoke evidence.

The layer is separate from `common/`: Common remains connector-neutral, while
adapter-owned helpers may name Apache or NGINX as components. The layer is also
separate from `upstream/`: imported sources remain the functional reference
implementation until a later replace-and-reduce phase proves equivalence.

## Current Files

| Path | Role | Runtime use |
| --- | --- | --- |
| `connectors/apache/src/metadata.h` | Apache adapter metadata API | Not linked into Apache module builds |
| `connectors/apache/src/metadata.c` | Apache origin/source metadata | Validated by `ci/check-adapter-helpers.sh` |
| `connectors/nginx/src/metadata.h` | NGINX adapter metadata API | Not linked into NGINX module builds |
| `connectors/nginx/src/metadata.c` | NGINX origin/source metadata | Validated by `ci/check-adapter-helpers.sh` |
| `connectors/nginx/src/ddebug.h` | NGINX debug compatibility header | Copied into generated build trees only when the selected source lacks `src/ddebug.h` |

## Boundaries

### Safe Adapter-Owned

- static connector metadata;
- source/origin descriptors;
- adapter-local debug compatibility;
- helper code compiled only by non-product validation checks.

### Possible Future Common

- status/origin/intervention data shapes after the connector-specific fields are
  separated from server identity;
- capability naming and summary metadata;
- stable audit severity descriptors after audit behavior is proven across
  connectors.

### Connector-Specific Forever

- Apache hook registration and bucket brigades;
- NGINX module registration and filter chain integration;
- server configuration parsing and server memory ownership;
- connector-specific request/response lifecycle decisions.

### Unsafe For Extraction

- request body timing and buffering;
- response body filtering and late interventions;
- libmodsecurity transaction ownership;
- intervention finalization behavior;
- audit-log absence behavior until cross-environment evidence is stable.

## Validation

The adapter metadata helpers are compiled by `ci/check-adapter-helpers.sh`
under `$BUILD_ROOT/adapter-helper-smoke/`. The script links the metadata sources
with the Common `origin` helper and asserts that the stable fields are present.

No FFI bridge is added, and the smoke runners do not depend on these helper
objects. Any future production use requires a separate replace-and-reduce step
with before/after real-world connector smokes.
