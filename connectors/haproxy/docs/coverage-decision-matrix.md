# HAProxy Coverage Decision Matrix

**Language:** English | [Deutsch](coverage-decision-matrix.de.md)

Status: partial; historical SPOA runtime records are not canonical Phase-4
promotion evidence

The HAProxy matrix records historical runtime material through HAProxy,
SPOE/SPOP, `haproxy-modsecurity-spoa`, and libmodsecurity. It does not promote
response-body or late-intervention facets. Unsupported or force-all rows are
not promoted into the default smoke summary.

## Current Runtime Counts

| Target | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Default smoke (historical) | 55 | 55 | 0 | 0 | 0 | runtime validation snapshot |
| Force-all matrix (historical) | 133 | 104 | 23 | 0 | 6 | generated HAProxy detail report |

## Coverage Areas

| Area | Status | Evidence |
| --- | --- | --- |
| Request phases 1/2 | historically evidenced | request SPOE group and ModSecurity decisions |
| Phase 3 response headers | implemented, historically evidenced | response SPOE group and decision logs |
| Audit/log | historically evidenced | audit-log plumbing and case artifacts |
| CRS SQLi anomaly block | historically evidenced | with-CRS runtime summary |
| Phase 4 / RESPONSE_BODY | `implemented_not_asserted` | `wait-for-body`, response-body limits, and decision logs are not canonical facet evidence |
| Full-body RESPONSE_BODY | not promoted | requires separate proof |

## Promotion Rules

- `PASS` means live HAProxy execution produced the expected case result.
- `FAIL` means live HAProxy execution produced a different result.
- `NOT_EXECUTABLE` means outside current HAProxy runtime scope.
- Force-all rows remain in
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- Root summaries remain connector-neutral.
- There is no synthetic matrix writer.

Phase 4 / RESPONSE_BODY remains non-promoted. The bounded branch is not proof
of a real host-side strict abort.

## Canonical Phase-4 decision

The bounded SPOA/SPOP response branch is a source-level capability only. It
does not prove response timing or transport behavior. Only response-body
availability, `phase4`, and `phase4_rule_evaluation` remain
`implemented_not_asserted`; the semantic enforcement and late-intervention
facets are `not_implemented`.

| Facet | Declared state | Coverage decision |
| --- | --- | --- |
| `response_body_buffered` and `phase4` | `implemented_not_asserted` | require a joined HAProxy/agent host run |
| `phase4_rule_evaluation` | `implemented_not_asserted` | require observed rule `1100301`, independent of a 403 |
| `phase4_pre_commit_deny` | `not_implemented` | current fields are policy-derived; no host runner captures visible client status and commitment timing |
| `late_intervention`, `late_intervention_log_only`, and `late_intervention_abort` | `not_implemented` | no post-commit HAProxy host point or safe/strict late action exists |
| `late_intervention_status_metadata` | `not_implemented` | no host-observed original/visible status plus timing exists; policy-derived values are insufficient |

If that evidence is unavailable, report `NOT_EXECUTED` rather than a synthetic
403 `PASS`. All evidence is metadata-only.
