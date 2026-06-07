# Shadow Build Source Plan

Status: phase 11 Apache and NGINX adapter-owned implementation

The connector build no longer treats `connectors/*/upstream/` as the direct
build input. The former imported upstream trees have been replaced by
adapter-owned source trees plus durable attribution under `licenses/`, and the
build harness generates disposable connector source trees under `$BUILD_ROOT`.

## Goal

Generated build sources live outside the checkout:

- `$BUILD_ROOT/apache-build/connector-src/`
- `$BUILD_ROOT/nginx-build/connector-src/`

Each generated tree is disposable. It records repo-owned adapter files and
generated overlays; explicit external-source builds remain documented by their
sanitized build copies. This keeps attribution visible while allowing later
replace-and-reduce phases to shrink adapter-owned source only when smokes prove
the change.

## Source Precedence

For monorepo-default connector sources, the materialized tree uses this order:

1. copy adapter-owned build files from `connectors/<name>/` according to the
   connector `SOURCE_MAP.json`;
2. write generated manifests.

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

Apache is materialized for evidence only in Phase 8. The Apache Autotools build
still uses the existing sanitized upstream copy in that phase because the
generated source tree has not yet been proven as the default APXS/Autotools
input.

## Phase 9 NGINX Migration

NGINX productive source is now adapter-owned. The monorepo default
`MODSECURITY_NGINX_SOURCE_DIR` is `connectors/nginx`, and
`modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh` materializes `$BUILD_ROOT/nginx-build/connector-src`
from adapter-owned NGINX `connectors/nginx/config` and module sources in
`connectors/nginx/src`, plus generated materialization manifests.

The materializer maps NGINX `connectors/nginx/config` to root `config` in
the generated connector source. Productive source/header files remain under
`src/`; support metadata at the connector root is not materialized. The
generated JSON manifest records PR #377 patch provenance for the phase-4 files
that received those changes.

The former `connectors/nginx/upstream/` tree is no longer the productive NGINX
module source tree.

## Phase 10 NGINX Upstream Removal

Phase 10 removes the remaining NGINX upstream reference tree entirely. Durable
attribution stays in `licenses/nginx/`, `connectors/nginx/ORIGIN.md`, and
`connectors/nginx/SOURCE_MAP.json`. The NGINX materialized-source manifest
should show only `adapter-owned` and `generated-overlay` entries.

`modules/ModSecurity-test-Framework/ci/run-nginx-smoke.sh` treats an existing monorepo-default NGINX build as
stale when `$BUILD_ROOT/nginx-build/connector-src/materialized-source.json` is
missing, still references `upstream-derived` entries, or does not mark the NGINX
module `config` and C sources as `adapter-owned`. In that case it refreshes only
the generated NGINX build/runtime directories under `$BUILD_ROOT` before running
smokes, so old modules cannot mask or break adapter-owned source validation.

## Phase 11 Apache Migration

Apache productive source is now adapter-owned. The monorepo default
`MODSECURITY_APACHE_SOURCE_DIR` is `connectors/apache`, and
`modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh` materializes
`$BUILD_ROOT/apache-build/connector-src` from adapter-owned Apache source,
Autotools/APXS inputs, required `.in` templates, and generated manifests. The
materializer keeps Apache paths unchanged so `./autogen.sh`, `./configure`, and
`make` run from the generated connector source root.

The former `connectors/apache/upstream/` tree was removed after
`REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-apache-final-build make
smoke-apache` passed. `modules/ModSecurity-test-Framework/ci/run-apache-smoke.sh` treats an existing
monorepo-default Apache build as stale when the materialized-source manifest is
missing, still references `upstream-derived` entries, or does not mark required
Apache build/source/template files as `adapter-owned`.

## Phase 13 Layout Simplification

Phase 13 keeps the generated connector build layouts unchanged while making the
repository layout stricter. NGINX `config` lives at `connectors/nginx/config`
and materializes to root `config`; NGINX `src/` contains only productive module
headers/sources. Apache Autotools/APXS files live at `connectors/apache/`,
productive C files live directly under `connectors/apache/src/`, and retained
Autotools templates live under `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/` while materializing
back to the `t/` and `tests/` paths expected by `configure.ac`.

## Non-Goals

This phase does not change:

- Apache hooks or NGINX filters;
- request, response, body, transaction, intervention, or `RESPONSE_BODY`
  behavior;
- YAML cases or `verified_variables`;
- adapter-owned Apache or NGINX source semantics.

For NGINX, phase 9 changes the build input ownership but not the smoke semantics
or verified variable model. `RESPONSE_BODY` remains former expected-failure/mapped-only.
