# Apache Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Status: partial, evidence-scoped

Generated coverage reporting is not automatic runtime promotion. Apache remains
partial because historical force-all evidence still has FAIL and
NOT_EXECUTABLE rows; it does not promote canonical RESPONSE_BODY facets.

## Historical Runtime Counts

| Target | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Default smoke (historical) | 54 | 54 | 0 | 0 | 0 | runtime validation snapshot |
| Force-all matrix (historical) | 133 | 100 | 27 | 0 | 6 | generated Apache detail report |

## Evidence Sources

- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `reports/testing/test-coverage-overview.md`
- `reports/testing/generated/apache-runtime-results.generated.md`
- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/apache-summary.json`

## Promotion Rules

- `PASS` means live Apache execution produced the expected case result.
- `FAIL` means live Apache execution produced a different result.
- `NOT_EXECUTABLE` means outside the current runtime scope.
- Former-XFAIL and force-all rows stay separate from default smoke status.
- Generated reports must be refreshed through `make generate-test-matrix`.

Phase 4 / RESPONSE_BODY remains non-promoted. Strict-mode source wiring is not
evidence of a real host-side late abort.

## Canonical Phase-4 decision

For the canonical No-CRS model, the native Apache response path is present but
not currently asserted by a fresh real-host result. The following source
states intentionally remain `implemented_not_asserted`.

| Facet | Declared state | Coverage decision |
| --- | --- | --- |
| `response_body_buffered` and `phase4` | `implemented_not_asserted` | bounded filter wiring is not runtime proof |
| `phase4_rule_evaluation` | `implemented_not_asserted` | require observed rule `1100301`; do not require 403 |
| `phase4_pre_commit_deny` | `implemented_not_asserted` | require uncommitted headers and matching visible deny status |
| `late_intervention` and `late_intervention_log_only` | `implemented_not_asserted` | require requested `deny`, actual `log_only`, and unchanged visible status |
| `late_intervention_abort` | `implemented_not_asserted` | require actual `abort_connection` and `connection_aborted=true` |
| `late_intervention_status_metadata` | `implemented_not_asserted` | require original host, requested WAF, visible client, requested-action, and actual-action fields |

Absent a current matching run, the relevant case result is `NOT_EXECUTED`; it
is not a 403 `PASS`. Events and reports must remain metadata-only.
