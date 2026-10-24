# Change Record: CR-20261008-nginx-event-boundary-serialized-callback

**Language:** English | [Deutsch](CR-20261008-nginx-event-boundary-serialized-callback.de.md)

Bounded serialized-event correction; no current native runtime or E2E claim.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-event-boundary-serialized-callback |
| Date (UTC) | 2026-10-08 |
| Base revision | `1940c1dbda6b371248a37f257c19df9b60fd836d` |

## Motivation and problem statement

Common's serializer emits `rule_match`/`allow`, not the producer struct's `request_rule_match`/`pass`. The event-boundary driver otherwise ignores the real Rule1100402 callback before its strict Framework validation.

## Acceptance criteria

Select the actual serialized Phase1 Rule1100402 callback. Wrong Rule, old struct vocabulary and malformed JSON remain rejected. Preserve original JSONL bytes and all existing source, host, bounded-metadata and canonical checks.

## Implementation decision and rationale

Change only the event-name predicate to `rule_match`. Use a Source-shaped serialized allow fixture and explicitly reject the previous struct name. No Common/product semantic change or fallback event is introduced.

## Changed files

`ci/runtime/lifecycle/run-nginx-event-boundary-cases.py`, `tests/test_nginx_event_boundary_driver.py`, and this generated EN/DE record pair.

## Commands executed

The real serialized-callback control initially failed (zero callbacks). `rtk proxy ... python -m unittest tests.test_nginx_event_boundary_driver` then passed three controlled tests, exit0. The added old-name negative is rerun before commit. Archive and whitespace checks are recorded by the coordinator; this record itself claims no later run.

## Security impact

Evidence fidelity correction, not a security remediation. No checks or limits are removed; the strict Framework reader still validates callback identity, phase, Rule, original bytes and explicit source/artifact authority.

## Runtime evidence

None for this commit. Controlled fixtures are not runtime events. All97 selected Required records remain unchanged; the45 baseline gaps require final integrated runtime evidence.

## Known limitations

The driver predicate is not Canonical acceptance. Fresh source-bound module/binary, actual Root/nobody invocations, complete captured events and offline validation are still required.

## Remaining risks

Final native E2E and remote revision-bound CI/Sonar are pending. The Draft PR remains Draft; protected Trusted Base/host administration is a separate unresolved layer.

## Checks not run and rationale

No native build or full E2E while central Canonical integration is incomplete. Full lint is not certified; no missing tools are installed.

## Final diff and review status

Only the predicate, its focused fixture/negative and this generated pair. No Gitlink, MRTS, generic validator or security-guard changes. Coordinator reviews the staged diff before a separate normal commit.
