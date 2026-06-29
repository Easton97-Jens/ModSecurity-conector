# NGINX Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Status: partial, evidence-scoped

Generated coverage reporting is not automatic runtime promotion. NGINX remains
partial because force-all evidence still has FAIL and NOT_EXECUTABLE rows and
full RESPONSE_BODY support is not promoted.

## Current Runtime Counts

| Target | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Default smoke | 60 | 60 | 0 | 0 | 0 | runtime validation snapshot |
| Force-all matrix | 140 | 95 | 39 | 0 | 6 | generated NGINX detail report |

## Evidence Sources

- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `reports/testing/test-coverage-overview.md`
- `reports/testing/generated/nginx-runtime-results.generated.md`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/nginx-summary.json`

## Promotion Rules

- `PASS` means live NGINX execution produced the expected case result.
- `FAIL` means live NGINX execution produced a different result.
- `NOT_EXECUTABLE` means outside the current runtime scope.
- Former-XFAIL and force-all rows stay separate from default smoke status.
- Generated reports must be refreshed through `make generate-test-matrix`.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
