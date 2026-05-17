# Shadow Build Source Plan

Status: phase 9 NGINX adapter-owned implementation

The connector build should gradually stop treating `connectors/*/upstream/` as
the direct build input. The imported upstream trees remain provenance and
reference material, but the build harness can now generate a connector source
tree under `$BUILD_ROOT`.

## Goal

Generated build sources live outside the checkout:

- `$BUILD_ROOT/apache-build/connector-src/`
- `$BUILD_ROOT/nginx-build/connector-src/`

Each generated tree is disposable. It records which files are still
upstream-derived and which files are repo-owned adapter files. This keeps
attribution visible while allowing later replace-and-reduce phases to shrink the
imported upstream surface.

## Source Precedence

For monorepo-default connector sources, the materialized tree uses this order:

1. copy remaining imported/reference files from `connectors/<name>/upstream/`;
2. overlay adapter-owned files from `connectors/<name>/src/`;
3. write generated manifests.

Explicit external connector sources still opt out of materialization. When
`MODSECURITY_APACHE_SOURCE_DIR` or `MODSECURITY_NGINX_SOURCE_DIR` points outside
the monorepo default, the prepare scripts keep using the external sanitized
copy path.

## Attribution

Every materialized tree contains:

- `MATERIALIZED_SOURCE.md`
- `materialized-source.json`

The manifests list the final files, origin path, source kind, license, observed
commit/version, and reason. They are generated under `$BUILD_ROOT` and are not
committed.

## Phase 8 Decision

NGINX is switched first. Its previous low-risk `ddebug.h` replacement is already
adapter-owned, and the NGINX module `config` explicitly lists the build inputs.
The default NGINX build now uses `$BUILD_ROOT/nginx-build/connector-src`.

Apache is materialized for evidence only. The Apache Autotools build still uses
the existing sanitized upstream copy in this phase because the generated source
tree has not yet been proven as the default APXS/Autotools input.

## Phase 9 NGINX Migration

NGINX productive source is now adapter-owned. The monorepo default
`MODSECURITY_NGINX_SOURCE_DIR` is `connectors/nginx/src`, and
`ci/prepare-nginx-build.sh` materializes `$BUILD_ROOT/nginx-build/connector-src`
from:

- retained upstream attribution/reference files in `connectors/nginx/upstream/`;
- adapter-owned NGINX `config` and module sources in `connectors/nginx/src/`;
- generated materialization manifests.

The materializer maps NGINX `connectors/nginx/src/config` to root `config` in
the generated connector source. All other adapter files are placed under
`src/`. The generated JSON manifest records PR #377 patch provenance for the
phase-4 files that received those changes.

`connectors/nginx/upstream/` is reduced to `LICENSE`, `AUTHORS`, `CHANGES`, and
`README.md`; it is no longer the productive NGINX module source tree.

## Non-Goals

This phase does not change:

- Apache hooks or NGINX filters;
- request, response, body, transaction, intervention, or `RESPONSE_BODY`
  behavior;
- YAML cases or `verified_variables`;
- Apache imported upstream files in the checkout.

For NGINX, phase 9 changes the build input ownership but not the smoke semantics
or verified variable model. `RESPONSE_BODY` remains xfail/mapped-only.
