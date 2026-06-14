# NGINX Build

Status: adapter-owned dynamic module path

The complete repository-supported NGINX compile and local verification flow is
documented in the root guide:

- [`COMPILE_NGINX.md`](../../../COMPILE_NGINX.md)

## Current Build Path

The helper builds NGINX from the supported source mode, stages libmodsecurity
under `BUILD_ROOT`, and builds the connector as a dynamic module:

```bash
git submodule update --init --recursive
REFRESH=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

By default the connector source is the adapter-owned monorepo import:

```bash
MODSECURITY_NGINX_SOURCE_DIR=connectors/nginx
```

Set `MODSECURITY_NGINX_SOURCE_DIR=/path/to/ModSecurity-nginx` only when testing
an external read-only checkout.

## Current Runtime Evidence

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default NGINX smoke | 60 | 60 | 0 | 0 | 0 |
| NGINX force-all | 140 | 95 | 39 | 0 | 6 |

Runtime evidence is written under `/src/ModSecurity-conector-build/results/`
and summarized in:

- `reports/testing/generated/nginx-runtime-results.generated.md`
- `reports/testing/test-coverage-overview.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
