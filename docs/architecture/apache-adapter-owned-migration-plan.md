# Apache Adapter-Owned Migration Plan

Status: implemented in Phase 11

Apache now follows the same materialized adapter-owned source model as NGINX.
The migration preserves the upstream Autotools/APXS layout inside
`connectors/apache/src/` and builds from a disposable generated source tree
under `$BUILD_ROOT/apache-build/connector-src`.

## Current State

| Area | Current location | Phase 11 decision |
| --- | --- | --- |
| Apache module sources | `connectors/apache/src/src/*.c`, `*.h` | Adapter-owned path ownership; no semantic edits |
| Autotools entrypoints | `connectors/apache/src/autogen.sh`, `configure.ac`, `Makefile.am` | Adapter-owned build inputs, preserving upstream layout |
| Build macros/templates | `connectors/apache/src/build/*.m4`, `.in` templates | Adapter-owned build inputs retained because `configure.ac` references them |
| License/context files | `licenses/apache/`; `connectors/apache/src/LICENSE`, `AUTHORS`, `CHANGES` | Durable attribution plus build-root source anchor |
| Per-file provenance | `connectors/apache/src/SOURCE_MAP.json` | Machine-readable source map for materialized manifests |
| Former upstream tree | `connectors/apache/upstream/` | Removed after materialized build and smoke proof |

## Proven Build Path

Monorepo-default Apache builds use:

```sh
MODSECURITY_APACHE_SOURCE_DIR=connectors/apache/src
APACHE_CONNECTOR_BUILD_DIR=$BUILD_ROOT/apache-build/connector-src
```

`ci/prepare-apache-build.sh` materializes the source tree, then runs the
standard Autotools/APXS sequence from the generated directory:

```sh
./autogen.sh
./configure --with-libmodsecurity=<BUILD_ROOT staging prefix> --with-apxs=<apxs>
make
```

Evidence command:

```sh
REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-apache-final-build make smoke-apache
```

That proof built `mod_security3.so` through APXS and passed the current Apache
real-world smoke suite before the former upstream tree was removed.

## Boundaries

The migration does not change:

- Apache hook registration;
- input/output filters;
- bucket brigades or `send_error_bucket()`;
- request/response metadata mapping;
- libmodsecurity transaction ownership;
- intervention runtime semantics;
- YAML case behavior;
- `RESPONSE_BODY` xfail/mapped-only status.

## Remaining Risk

Apache is still more fragile than NGINX because Autotools, APXS discovery,
generated templates, and Apache filter/bucket behavior are tightly coupled.
Future reductions inside `connectors/apache/src/` require a dedicated
before/after proof:

```sh
REFRESH=1 BUILD_ROOT=/src/ModSecurity-conector-apache-reduce-build make smoke-apache
BUILD_ROOT=/src/ModSecurity-conector-apache-reduce-build make smoke-all
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-all
```

No source file should be removed merely because it looks unused; the
materialized manifest and smoke evidence must prove the reduction.
