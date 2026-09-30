# Change Record: exact Sonar finding counts

**Language:** English | [Deutsch](CR-20260922-pr382-sonar-counts.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-sonar-counts` |
| Date (UTC) | `2026-09-22` |
| Base revision | `e8d5e5081f166e8a9b01bbb84ce4baf6530109d9` |

## Motivation and problem statement

The remote summary uses `1 New issue`, not the plural expected by the guard.
The guard failed correctly, but before printing the bounded issue location.
Accepted issue counts were not yet part of its enforced zero requirement.

## Acceptance criteria

Parse singular and plural labels unambiguously. Reject every nonzero new,
accepted, hotspot or annotation count. Missing evidence still fails. Report the
bounded annotations for a singular issue without exposing source excerpts.

## Implementation decision and rationale

Use fixed label patterns, count both spellings together, and require accepted
issue evidence rather than assuming zero. No scanner configuration is changed.

## Changed files

- `ci/checks/common/check-sonar-zero.py`
- `tests/test_sonar_zero_gate.py`
- This record and its German companion.

## Commands executed

The existing CI entry point runs:

```sh
python -m unittest -v tests.test_sonar_zero_gate
```

Four added regressions cover singular diagnostics, accepted findings, ambiguous
mixed labels and missing accepted counts. Execution is pending at preparation.

## Security impact

This strengthens the zero-finding gate. It never accepts, hides or suppresses a
finding and preserves exact-head/provider checks and bounded read-only access.

## Runtime evidence

This is a CI evidence parser, not connector runtime evidence.

## Known limitations

The source issue reported by Sonar still requires a separate fix. This parser
repair alone cannot satisfy the zero-finding requirement or I09-I12.

## Remaining risks

Any further Sonar summary format change must fail closed until investigated.

## Checks not run and rationale

No local project tests were run because the required RTK wrapper is absent.
Remote CI and Sonar results must be read for the exact resulting commit.

## Final diff and review status

Prepared as a focused follow-up in Draft PR #382. No merge, force push, scanner
exception, issue acceptance or Framework/MRTS write.
