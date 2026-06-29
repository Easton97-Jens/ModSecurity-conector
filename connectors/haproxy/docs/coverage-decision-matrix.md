# HAProxy Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Status: partial, production SPOA runtime evidence

The HAProxy matrix is generated from live runtime evidence through HAProxy,
SPOE/SPOP, `haproxy-modsecurity-spoa`, and libmodsecurity. Unsupported or
force-all rows are not promoted into the default smoke summary.

## Current Runtime Counts

| Target | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Default smoke | 55 | 55 | 0 | 0 | 0 | runtime validation snapshot |
| Force-all matrix | 133 | 104 | 23 | 0 | 6 | generated HAProxy detail report |

## Coverage Areas

| Area | Status | Evidence |
| --- | --- | --- |
| Request phases 1/2 | live evidenced | request SPOE group and ModSecurity decisions |
| Phase 3 response headers | implemented, live evidenced | response SPOE group and decision logs |
| Audit/log | live evidenced for current cases | audit-log plumbing and case artifacts |
| CRS SQLi anomaly block | live evidenced | with-CRS runtime summary |
| Phase 4 / RESPONSE_BODY | bounded strict-abort evidence only | `wait-for-body`, response-body limits, and decision logs |
| Full-body RESPONSE_BODY | not promoted | requires separate proof |

## Promotion Rules

- `PASS` means live HAProxy execution produced the expected case result.
- `FAIL` means live HAProxy execution produced a different result.
- `NOT_EXECUTABLE` means outside current HAProxy runtime scope.
- Force-all rows remain in
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- Root summaries remain connector-neutral.
- There is no synthetic matrix writer.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.
