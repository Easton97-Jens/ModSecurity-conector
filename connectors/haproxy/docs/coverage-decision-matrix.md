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
| Phase 4 / RESPONSE_BODY | `not_implemented` | the former `wait-for-body` sample is disabled; the selected SPOP path has no wired native response-chunk route |
| Full-body RESPONSE_BODY | not promoted | requires separate proof |

## Promotion Rules

- `PASS` means live HAProxy execution produced the expected case result.
- `FAIL` means live HAProxy execution produced a different result.
- `NOT_EXECUTABLE` means outside current HAProxy runtime scope.
- Force-all rows remain in
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- Root summaries remain connector-neutral.
- There is no synthetic matrix writer.

Phase 4 / RESPONSE_BODY remains non-promoted. The former bounded sample is
disabled because it used `wait-for-body`, not a real host-side response stream.

## Canonical Phase-4 decision

The former bounded SPOA/SPOP response branch is disabled because it required
`wait-for-body`. The selected host path has no wired native response-body
callback, so response-body availability, `phase4`, and
`phase4_rule_evaluation` are `not_implemented`; the semantic enforcement and
late-intervention facets are also `not_implemented`. The optional HAProxy
3.2.21 HTX observer source is a separate, bodyless-request-only overlay. It
uses borrowed chunks/EOS but is not configured by this SPOP path and does not
promote these states.

| Facet | Declared state | Coverage decision |
| --- | --- | --- |
| `response_body_buffered` and `phase4` | `not_implemented` | wire a complete native HAProxy response-chunk transaction into the selected path; do not use `wait-for-body` |
| `phase4_rule_evaluation` | `not_implemented` | requires a real selected end-of-stream path and observed rule `1100301` |
| `phase4_pre_commit_deny` | `not_implemented` | current fields are policy-derived; no host runner captures visible client status and commitment timing |
| `late_intervention`, `late_intervention_log_only`, and `late_intervention_abort` | `not_implemented` | no post-commit HAProxy host point or safe/strict late action exists |
| `late_intervention_status_metadata` | `not_implemented` | no host-observed original/visible status plus timing exists; policy-derived values are insufficient |

If that evidence is unavailable, report `NOT_EXECUTED` rather than a synthetic
403 `PASS`. All evidence is metadata-only.
