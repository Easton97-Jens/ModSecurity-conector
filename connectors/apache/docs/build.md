# Apache Build

Status: scaffolded

Observed local source uses Autotools and `apxs`:

- `configure.ac`
- `Makefile.am`
- `build/apxs-wrapper.in`

The repository now provides a PoC helper, not a full connector build system:

```sh
REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-build \
sh ci/prepare-apache-build.sh
```

The helper copies libmodsecurity v3 and the Apache connector source into
`BUILD_ROOT`, can build Apache httpd from source under `BUILD_ROOT`, and uses
the observed upstream Autotools/APXS path:

```sh
./autogen.sh
./configure --with-libmodsecurity=<BUILD_ROOT staging prefix>
make
```

Status `pass` is only a built module artifact. Runtime pass requires
`connectors/apache/harness/run_apache_smoke.sh` to observe HTTP `403`.

By default the connector source is the controlled monorepo import:

```sh
MODSECURITY_APACHE_SOURCE_DIR=connectors/apache/upstream
```

Set `MODSECURITY_APACHE_SOURCE_DIR=/path/to/ModSecurity-apache` to rebuild from
an external read-only checkout. The build helper sanitizes connector source
copies into `BUILD_ROOT` and excludes `.git`, CI files, caches, and build
artifacts.

Observed import-source verification:

```sh
REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-import-build \
make smoke-apache
```

Result: pass. The built module path was under
`/src/ModSecurity-conector-import-build/apache-build/output/apache/`.

TODO:

- Verify minimum Apache/APR/APR-util/PCRE build requirements.
- Keep CI blocked-safe until those dependencies are explicitly provisioned.
