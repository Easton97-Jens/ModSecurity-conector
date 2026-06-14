# Apache Build

Status: adapter-owned source migration complete

The complete repository-supported Apache compile and local verification flow is
documented in the root guide:

- [`COMPILE_APACHE.md`](../../../COMPILE_APACHE.md)

## Current Build Path

The helper materializes connector source into `BUILD_ROOT`, builds
libmodsecurity/httpd dependencies when requested, and uses the observed
Autotools/APXS path:

```bash
git submodule update --init --recursive
REFRESH=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

By default the connector source is the adapter-owned monorepo import:

```bash
MODSECURITY_APACHE_SOURCE_DIR=connectors/apache
```

Set `MODSECURITY_APACHE_SOURCE_DIR=/path/to/ModSecurity-apache` only when
testing an external read-only checkout.

## Current Runtime Evidence

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default Apache smoke | 54 | 54 | 0 | 0 | 0 |
| Apache force-all | 133 | 100 | 27 | 0 | 6 |

Runtime evidence is written under `/src/ModSecurity-conector-build/results/`
and summarized in:

- `reports/testing/generated/apache-runtime-results.generated.md`
- `reports/testing/test-coverage-overview.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
