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

Phase 4 / RESPONSE_BODY remains non-promoted. The source now forwards each
current output brigade before EOS and finalizes at EOS, but safe/strict
transport behavior still requires current real-host evidence.

## Common-Adoption C Standard Checks

The Apache/Common-adoption compile layer is checked independently from an Apache
runtime start:

- `make check-apache-c17` is the mandatory C17 smoke.
- `make check-apache-c23` is optional and skips when the compiler lacks c23/c2x.
- `make check-apache-future-c` is optional and skips when the compiler lacks
  c2y/gnu2y.
- `make check-apache-c-standards` runs the mandatory and optional profiles.

The check discovers APXS through `APXS`, `apxs`, or `apxs2`, adds APR flags from
`apr-1-config`/`apr-2-config` when available, and compiles only objects. It does
not link libmodsecurity or start httpd. Missing APXS or Apache/APR/
libmodsecurity headers are reported as `BLOCKED` with exit code `77`. This is
compile/structure evidence only and does not claim production readiness, CRS
coverage, full-matrix coverage, or runtime verification.

## APXS Common SDK object inclusion

The APXS wrapper appends the Common SDK C sources required by the Apache
adoption layer to the module compile command. This keeps the build path
Apache-owned while ensuring calls such as Common config merge/validation,
mapper-contract validation, event JSONL writing, rule-id extraction, resource
limits, and HTTP-status helpers are compiled into the Apache module. The wrapper
continues to add `common/include` and does not add Apache types to Common.
