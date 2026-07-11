# NGINX Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Status: partial, evidence-scoped

Generated coverage reporting is not automatic runtime promotion. NGINX remains
partial because historical force-all evidence still has FAIL and
NOT_EXECUTABLE rows; it does not promote canonical RESPONSE_BODY facets.

## Historical Runtime Counts

| Target | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Default smoke (historical) | 60 | 60 | 0 | 0 | 0 | runtime validation snapshot |
| Force-all matrix (historical) | 140 | 95 | 39 | 0 | 6 | generated NGINX detail report |

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

Phase 4 / RESPONSE_BODY remains non-promoted. Strict-mode source wiring is not
evidence of a real host-side late abort.

## Canonical Phase-4 decision

The native bounded NGINX response-body filter is source evidence, not current
canonical behavior evidence. Each executable Phase-4 and late-intervention
facet below is deliberately `implemented_not_asserted`; the pre-commit branch
is excluded by the current body-filter timing model.

| Facet | Declared state | Coverage decision |
| --- | --- | --- |
| `response_body_buffered` and `phase4` | `implemented_not_asserted` | body-filter wiring alone does not establish execution |
| `phase4_rule_evaluation` | `implemented_not_asserted` | require observed rule `1100301`; visible 403 is independent |
| `phase4_pre_commit_deny` | `not_implemented` | the native Phase-4 body filter runs after the response-header path; do not infer a visible Phase-4 deny |
| `late_intervention` and `late_intervention_log_only` | `implemented_not_asserted` | require requested `deny`, actual `log_only`, late flag, and unchanged visible status |
| `late_intervention_abort` | `implemented_not_asserted` | require actual `abort_connection` and `connection_aborted=true` |
| `late_intervention_status_metadata` | `implemented_not_asserted` | require original host, requested WAF, visible client, requested-action, and actual-action fields |

Without a current matching host run the outcome is `NOT_EXECUTED`, not a 403
`PASS`; metadata-only event handling remains mandatory.
