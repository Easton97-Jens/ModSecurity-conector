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

The helper copies both read-only sources into `BUILD_ROOT`, can build Apache
httpd from source under `BUILD_ROOT`, and uses the observed upstream
Autotools/APXS path:

```sh
./autogen.sh
./configure --with-libmodsecurity=<BUILD_ROOT staging prefix>
make
```

Status `pass` is only a built module artifact. Runtime pass requires
`connectors/apache/harness/run_apache_smoke.sh` to observe HTTP `403`.

TODO:

- Verify minimum Apache/APR/APR-util/PCRE build requirements.
- Run source-built httpd mode to avoid system Apache assumptions.
- Keep CI blocked-safe until those dependencies are explicitly provisioned.
