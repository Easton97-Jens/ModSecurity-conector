# Adapter-Owned Layer

Status: phase 9 NGINX source migration

The adapter-owned layer is the first repo-owned connector code that sits beside
the imported upstream reference trees. It is intentionally not product runtime
code yet.

## Purpose

`connectors/<name>/src/` is reserved for connector-owned code developed outside
imported upstream reference trees:

- stable connector metadata;
- origin and license descriptors;
- debug compatibility shims;
- future adapter-local helpers with explicit smoke evidence.

For NGINX, this layer now also contains the adapter-owned module build source.
For Apache, it remains metadata-only.

The layer is separate from `common/`: Common remains connector-neutral, while
adapter-owned helpers may name Apache or NGINX as components. For Apache, the
layer is also separate from the retained `connectors/apache/upstream/` import.
For NGINX, the former upstream tree has been removed and `connectors/nginx/src/`
is now the build source; provenance remains in `licenses/nginx/`,
`connectors/nginx/ORIGIN.md`, and `connectors/nginx/src/SOURCE_MAP.json`.

## Current Files

| Path | Role | Runtime use |
| --- | --- | --- |
| `connectors/apache/src/metadata.h` | Apache adapter metadata API | Not linked into Apache module builds |
| `connectors/apache/src/metadata.c` | Apache origin/source metadata | Validated by `ci/check-adapter-helpers.sh` |
| `connectors/nginx/src/metadata.h` | NGINX adapter metadata API | Not linked into NGINX module builds |
| `connectors/nginx/src/metadata.c` | NGINX origin/source metadata | Validated by `ci/check-adapter-helpers.sh` |
| `connectors/nginx/src/ddebug.h` | NGINX debug compatibility header | Overlaid into NGINX materialized build sources; still used as external-source fallback when needed |
| `connectors/nginx/src/config` | NGINX dynamic module build metadata | Materialized to `$BUILD_ROOT/nginx-build/connector-src/config` for monorepo-default NGINX builds |
| `connectors/nginx/src/ngx_http_modsecurity_*.c` | Adapter-owned NGINX module sources | Built through the generated NGINX connector source tree |
| `connectors/nginx/src/ngx_http_modsecurity_common.h` | Adapter-owned NGINX connector declarations | Built through the generated NGINX connector source tree |
| `connectors/nginx/src/SOURCE_MAP.json` | NGINX base/PR provenance map | Used by materialized-source manifests; not compiled |

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
Its expected values are generated from `ci/adapter_metadata.py`, which parses
the adapter-owned C metadata without FFI.

`ci/check-adapter-metadata-drift.sh` compares the parsed adapter metadata with
the connector `ORIGIN.md` files, central `licenses/` origin docs, and import
documentation. Drift fails `make lint` before report metadata can silently
diverge.

No FFI bridge is added, and the smoke runners do not depend on these helper
objects. Any future production use requires a separate replace-and-reduce step
with before/after real-world connector smokes.

## Shadow Build Source Use

Phase 8 starts using adapter-owned files in generated build sources. Phase 9
migrates the NGINX module `config` and source files into `connectors/nginx/src`.
For the monorepo-default NGINX source, `ci/prepare-nginx-build.sh` materializes
`$BUILD_ROOT/nginx-build/connector-src` from adapter-owned NGINX source and
generated manifests only. The generated manifests identify the NGINX module
sources as `adapter-owned` and record PR #377 patch provenance where
applicable.

Apache is materialized for evidence only in phase 8. Its productive module build
continues to use the sanitized upstream copy until the Autotools/APXS path is
validated against the generated source tree.

## Reporting Precedence

Origin metadata used by build and runtime summaries follows this order:

1. explicit `*_ORIGIN_*` or `CONNECTOR_ORIGIN_*` environment overrides;
2. external connector source metadata from `git rev-parse` and `git describe`
   when `MODSECURITY_APACHE_SOURCE_DIR` or `MODSECURITY_NGINX_SOURCE_DIR` points
   outside the monorepo import;
3. adapter-owned metadata from `connectors/<name>/src/metadata.c` for the
   default monorepo adapter-owned source.

This is report metadata only. It does not link adapter metadata into Apache or
NGINX modules and does not affect request, response, body, filter, transaction,
or intervention behavior.
