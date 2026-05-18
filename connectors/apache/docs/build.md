# Apache Build

Status: adapter-owned source migration complete

Observed local source uses Autotools and `apxs`:

- `configure.ac`
- `Makefile.am`
- `build/apxs-wrapper.in`

The repository provides a controlled adapter-owned build helper:

```sh
REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-build \
sh ci/prepare-apache-build.sh
```

The helper copies libmodsecurity v3 and materializes the Apache connector
source into `BUILD_ROOT`, can build Apache httpd from source under
`BUILD_ROOT`, and uses the observed Autotools/APXS path:

```sh
./autogen.sh
./configure --with-libmodsecurity=<BUILD_ROOT staging prefix>
make
```

Status `pass` is only a built module artifact. Runtime pass requires
`connectors/apache/harness/run_apache_smoke.sh` to observe HTTP `403`.

By default the connector source is the controlled monorepo import:

```sh
MODSECURITY_APACHE_SOURCE_DIR=connectors/apache
```

Set `MODSECURITY_APACHE_SOURCE_DIR=/path/to/ModSecurity-apache` to rebuild from
an external read-only checkout. The build helper sanitizes connector source
copies into `BUILD_ROOT` and excludes `.git`, CI files, caches, and build
artifacts.

For the monorepo default, the productive build input is:

```sh
$BUILD_ROOT/apache-build/connector-src
```

The generated source tree includes `MATERIALIZED_SOURCE.md` and
`materialized-source.json`; required Apache files must be marked
`adapter-owned`, not `upstream-derived`.

Observed import-source verification:

```sh
REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-import-build \
make smoke-apache
```

Result: pass. The built module path was under
`/src/ModSecurity-conector-import-build/apache-build/output/apache/`.

Phase 11 materialized-source verification:

```sh
REFRESH=1 \
BUILD_ROOT=/src/ModSecurity-conector-apache-final-build \
make smoke-apache
```

Result: pass. The former `connectors/apache/upstream/` tree was removed after
this proof.

Phase 12 source-tree cleanup removed `AUTHORS`, `CHANGES`, `LICENSE`, and
`README.md` from `connectors/apache/src/` after the Autoconf source anchor was
changed to `src/mod_security3.c`. The Apache module still builds from the
materialized adapter-owned source tree; attribution remains in
`licenses/apache/`, `connectors/apache/ORIGIN.md`, and
`connectors/apache/SOURCE_MAP.json`.

Phase 13 simplified the repository layout while preserving the materialized
Autotools build layout. Build files now live in `connectors/apache/`, productive
C sources live directly in `connectors/apache/src/`, and retained Autotools
test templates live under `connectors/apache/tests/`.

Open work is tracked in `docs/roadmap/todo-inventory.md`:

- Verify minimum Apache/APR/APR-util/PCRE build requirements.
- Keep CI blocked-safe until those dependencies are explicitly provisioned.
