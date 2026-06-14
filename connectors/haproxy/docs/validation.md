# HAProxy Validation

Status: production SPOA runtime, evidence-scoped

`make smoke-haproxy` verifies framework YAML cases by materializing each case,
starting HAProxy, starting `haproxy-modsecurity-spoa`, starting a backend,
sending the case request through HAProxy, and asserting the observed status.

`make runtime-matrix-haproxy` records rows from live summary evidence. PASS and
FAIL are used only for live HAProxy execution. Generated artifacts may differ by
environment and case inventory, but no HAProxy PASS/FAIL may be fabricated from
synthetic matrix rows.

## Commands

```bash
git submodule update --init --recursive
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make smoke-haproxy
make runtime-matrix-haproxy
FORCE_ALL_CASES=1 make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

## Current Evidence

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default HAProxy smoke | 55 | 55 | 0 | 0 | 0 |
| HAProxy force-all | 133 | 104 | 23 | 0 | 6 |

Evidence is recorded in:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`
- `reports/testing/runtime-validation-snapshot.json`

## Not Claimed

- Force-all FAIL rows are not hidden by default smoke.
- Full-body RESPONSE_BODY support is not promoted.
- A build self-test alone is not runtime verification.
- There is no synthetic matrix writer.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
