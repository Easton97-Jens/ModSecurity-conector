# Change Record: non-rule event observation parity

**Language:** English | [Deutsch](CR-20260922-pr382-nonrule-observation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-nonrule-observation` |
| Date (UTC) | `2026-09-22` |
| Base revision | `7fe606c56a423f05454fe200f07a1c03d007ea3f` |

## Motivation and problem statement

I11 still allowed body-limit, unsupported-capability, client-cancel and
upstream-disconnect events to retain an executed action when their transport
observation was NULL, empty or `not_observable`. Rule and technical-error events
already handled that absence. Shared serialization did not by itself make these
other event categories consistent.

## Acceptance criteria

Clear unobserved actual actions for these known event categories without
changing their event identity, error/policy class, requested action, phase,
status observations, byte counts or transport flags. Retain observed actions and
application-owned events. The real JSONL and integrity implementations must
agree and remain idempotent. A negative control must expose the missing guard.

## Implementation decision and rationale

Apply one small observation helper after category-specific normalization and
before final message selection. No host capability, mode, sink retry policy,
public event layout or parser value changes. Non-disruptive rule-match records
retain their existing diagnostic semantics. This is an I11 implementation slice,
not a claim that every producer or physical log sink is now complete.

## Changed files

- `common/include/msconnector/event_protocol.h`
- `tests/test_event_transport_observation.py`
- This record and its German companion.

The existing focused lint step already runs the expanded test module.

## Commands executed

The CI entry point is:

```sh
python -m unittest -v tests.test_event_transport_observation
```

Execution is pending at preparation. Ten test methods include five non-rule
scenarios, three absence markers, observed controls, phase-specific causes,
family-neutral serialization and a compiled guard-removal negative control.
The fixture checks real JSONL/hash equality, idempotence and retained metadata.
No completed CI or Sonar result is claimed by this initial record.

## Security impact

A policy limit or disconnected peer is not proof that the host enforced a
requested action. This change removes that false assertion. Original-input
validation, query redaction and unsupported-profile rejection are unchanged.
It does not suppress scanner findings or change their acceptance thresholds.

## Runtime evidence

The tests compile actual Common serializer/hash code with controlled metadata.
Family labels are not six running hosts. Concrete adapter enforcement and
physical open/write/short-write failures require their own evidence.

## Known limitations

I09-I12 remain subject to their broader acceptance criteria. This patch does not
repair every source that supplies a nonempty but incorrect observation marker.
It does not establish the full direct/companion/middleware/sidecar matrix.

## Remaining risks

Consumers must accept an empty actual action for these additional known event
types. Normalized integrity values change accordingly; historical records need
the matching producer/verifier version. No prior client result is invented.

## Checks not run and rationale

Local project commands were not run because the mandatory RTK wrapper is absent.
Verification uses fresh GitHub CI; final-head Sonar zero remains required.
The independent secret-scan finding and live-host criteria remain open.

## Final diff and review status

Atomic source/test/documentation continuation in Draft PR #382. Concurrent
NGINX/Common changes are preserved. No merge, master push, force push,
dependency or Framework/MRTS changes are included.
