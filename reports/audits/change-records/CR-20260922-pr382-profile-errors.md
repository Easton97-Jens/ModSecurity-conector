# Change Record: mode-independent technical failures

**Language:** English | [Deutsch](CR-20260922-pr382-profile-errors.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-profile-errors` |
| Date (UTC) | `2026-09-22` |
| Base revision | `97d3ea10d526f8ab306bc1cc24fa63f573f36bc9` |

## Motivation and problem statement

The Common transaction policy explicitly translated technical failures to
`log_only`/`fail_open` in safe mode and after response commitment. This disagreed
with the requested native error semantics. Stale engine decision kinds could
also hide an explicit error status at the Common contract boundary.

## Acceptance criteria

Engine timeout/unavailability/invalid response, connector errors and protocol
errors must be terminal in either contract mode. Before commitment select deny
and fail-closed; after commitment select error and stop-I/O, not a replacement
HTTP response or an invented reset. Preserve cause, existing response status,
first-error ownership, cleanup and all legitimate rule-decision policies.

## Implementation decision and rationale

Correct the existing decision-policy function and prioritize explicit error
status in engine-to-contract classification. Do not add a separate mode flag or
change profile capability declarations. Update only the old technical fail-open
expectations in the existing owning C test; preserve its other assertions.

## Changed files

- `common/src/transaction_state.c`
- `tests/transaction_phase_contract_test.c`
- `tests/test_pr382_profile_errors.py`
- `.github/workflows/lint.yml`
- This record and its German companion.

## Commands executed

The added CI entry point is:

```sh
python -m unittest -v tests.test_pr382_profile_errors
```

It compiles actual Common state and the connector-owned registry, then checks
200 cases: ten actual profile definitions, two contract modes, two commitment
states and five technical causes. Four test methods check the cases, cause and
cleanup persistence, and unchanged status/capabilities. Execution is pending at
preparation. The full existing contract C test remains in its owning CI target.

## Security impact

A failed inspection no longer gains fail-open permission from safe mode.
After response commitment no new response status is requested by the contract.
Concrete adapters still own transport termination; no unsupported reset is
advertised and no scanner, authorization or resource limit is weakened.

## Runtime evidence

The tests exercise public Common lifecycle APIs, including companion phase
handoff/claim, failure, re-entry and cleanup. They are not ten live integrations.
The separate real-host/transport/sink matrix remains required.

## Known limitations

This closes the identified Common policy gap, not every host translation or
producer/sink path in I09-I12. Native error and log-sink owners require separate
validation. The independent secret-scan finding remains open.

## Remaining risks

This intentionally removes the old technical fail-open behavior. Deployments
that depended on continuing after an engine outage must account for denial or
stopped I/O. Valid explicit log-only and late rule policies are unchanged.

## Checks not run and rationale

No local project commands ran because the mandatory RTK wrapper is absent.
Current-head CI, exact-head Sonar zero and real transport outcomes must be
verified independently. An unchanged capability value is not a host test.

## Final diff and review status

Prepared as an atomic code/test change in Draft PR #382, preserving concurrent
work. No merge, master push, force push, dependency or Framework/MRTS changes.
