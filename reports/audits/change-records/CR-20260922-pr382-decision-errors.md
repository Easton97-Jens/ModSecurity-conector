# Change Record: PR #382 shared decision error boundary

**Language:** English | [Deutsch](CR-20260922-pr382-decision-errors.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-decision-errors` |
| Date (UTC) | `2026-09-22` |
| Base revision | `1301a4e30f04cb82dd0546607bfaab1461671b7b` |
| Pull request | [Draft #382](https://github.com/Easton97-Jens/ModSecurity-conector/pull/382) |

## Motivation and problem statement

The shared host-action mapper returned `log_only` for a missing or unknown
decision. A decision with explicit error status could retain an earlier allow,
log-only or rule kind. The event producer then repeated that stale kind and
claimed an actual host action even though it only had an engine decision.

## Acceptance criteria

Missing/unknown decisions and explicit error status must map to `error`, never
to a successful safe-mode observation. Error events must not carry a stale
rule ID. Legitimate decision kinds, policy body-limit rejection and configured
error HTTP statuses must remain intact. A decision alone must not claim an
observed host action. Existing adapter-specific policy stays with its owner.

## Implementation decision and rationale

Correct the existing Common mapper and producer rather than adding a second
route-specific classifier. Error status precedes kind mapping; the invalid-kind
fallback is an error. The allow/disruptive predicates follow that boundary.
Event construction uses the same error classification and leaves actual action
empty for the adapter that observes the host result. No struct layout changes.

## Changed files

- `common/src/decision_action.c`
- `common/src/decision.c`
- `tests/test_pr382_decision_safety.py`
- `.github/workflows/lint.yml`
- This record and its German companion.

## Commands executed

The added CI command is:

```sh
python -m unittest -v tests.test_pr382_decision_safety
```

The fixture compiles actual Common decision/event dependencies with C17,
`-Wall -Wextra -Werror` and checks 23 cases in seven test methods. At commit
preparation execution is pending; this section does not assert a pass.
No local project command was run because the required RTK wrapper is absent.

## Security impact

A missing or failed control cannot silently become observation-only success.
The change does not disable scanner rules, alter permissions, remove existing
tests or grant unsupported strict/reset capabilities. Metadata remains bounded
by the existing serializer; body data is not added to events.

## Runtime evidence

These are compiled Common-boundary tests, not six live servers or ten route
integrations. Every actual route still requires its own integration evidence.

## Known limitations

This is a contribution to I10/I11, not completion of I09-I12. The remaining
native API, sink, profile and transport requirements remain in the main
[checklist](../../../docs/pr-382-checklist.md).

## Remaining risks

Consumers must treat `actual_action` as observation rather than requested policy.
Callers that previously relied on invalid decisions becoming log-only must now
handle `error`. Valid explicit log-only decisions retain their meaning.

## Checks not run and rationale

Full host/transport/sink fault injection and final-head Sonar/CI have not been
established by this source change. The existing exact-head Sonar-zero gate stays
active. The separate secret-scan finding is not dismissed by this change.

## Final diff and review status

Status at preparation: implementation present, verification pending. Work stays
in the task-owned Draft PR. No merge, master push, deployment, dependency or
Framework/MRTS write is performed. Concurrent branch changes must be preserved.
