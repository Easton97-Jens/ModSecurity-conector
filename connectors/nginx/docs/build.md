# NGINX Build

Status: scaffolded

Observed local source uses the NGINX third-party module `config` file. The
source README documents `--add-module` and `--add-dynamic-module`.

The repository provides a PoC helper that builds NGINX from an official GitHub
release archive and uses the observed dynamic-module path:

```sh
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-build \
sh ci/prepare-nginx-build.sh
```

By default the connector source is the controlled monorepo import:

```sh
MODSECURITY_NGINX_SOURCE_DIR=connectors/nginx/upstream
```

Set `MODSECURITY_NGINX_SOURCE_DIR=/path/to/ModSecurity-nginx` to rebuild from an
external read-only checkout. The build helper sanitizes connector source copies
into `BUILD_ROOT` and excludes `.git`, CI files, caches, and build artifacts.

Status `pass` is only a built NGINX binary and dynamic module artifact. Runtime
pass requires `connectors/nginx/harness/run_nginx_smoke.sh` to observe the
expected HTTP behavior.

Observed import-source verification:

```sh
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-import-build \
make smoke-nginx
```

Result: pass. The built NGINX binary and dynamic module paths were under
`/src/ModSecurity-conector-import-build/nginx-runtime/nginx/`.

Open work is tracked in `docs/roadmap/todo-inventory.md`:

- Verify supported NGINX versions.
- Keep dynamic module support as the only active PoC path until static module
  behavior is separately proven.
