# HAProxy Build

Status: production SPOA runtime build available

The complete repository-supported HAProxy compile and local verification flow
is documented in the root guide:

- [`COMPILE_HAPROXY.md`](../../../COMPILE_HAPROXY.md)

## Current Build Path

```bash
git submodule update --init --recursive
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
make smoke-haproxy
```

The production SPOA binary is staged at:

```text
/src/ModSecurity-conector-build/haproxy-spoa-runtime/haproxy-modsecurity-spoa
```

The HAProxy binary is prepared under:

```text
/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy
```

## Current Runtime Evidence

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default HAProxy smoke | 55 | 55 | 0 | 0 | 0 |
| HAProxy force-all | 133 | 104 | 23 | 0 | 6 |

Evidence is summarized in:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`

Phase 4 / RESPONSE_BODY is `not_implemented` in the selected SPOE/SPOP path.
The former `wait-for-body` strict-abort sample is disabled, legacy, and
noncanonical; it is not current runtime evidence.
