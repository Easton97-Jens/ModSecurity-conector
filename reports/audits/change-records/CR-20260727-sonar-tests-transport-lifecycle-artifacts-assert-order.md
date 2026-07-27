# Change Record: Parent transport-lifecycle artifacts assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-transport-lifecycle-artifacts-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-transport-lifecycle-artifacts-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVOjfYmbqbBXVNC1 (61), AZ-KYVOjfYmbqbBXVNC2 (62), AZ-KYVOjfYmbqbBXVNC3 (64), AZ-KYVOjfYmbqbBXVNC4 (68), AZ-KYVOjfYmbqbBXVNC5 (69), AZ-KYVOjfYmbqbBXVNC6 (70), AZ-KYVOjfYmbqbBXVNC7 (71), AZ-KYVOjfYmbqbBXVNC8 (72), AZ-KYVOjfYmbqbBXVNC9 (76), AZ-KYVOjfYmbqbBXVNC- (77), AZ-KYVOjfYmbqbBXVNDA (151), and AZ-KYVOjfYmbqbBXVNDB (177). |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Transport artifact production helpers, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

Twelve selected assertions put literals before observed artifact fields or
in-memory counts. This change reverses only those first two arguments to
`actual, expected`. The Framework-subprocess assertion at line 126 remains
unchanged, and the line-178 assertion with a `source.read_bytes()` expected
operand remains deferred for separate evaluation-order review.

## Validation

| Check | Result |
| --- | --- |
| Three focused Parent-only methods before the edit | passed: 3 tests in 0.004s. |
| The same methods after the edit | passed: 3 tests in 0.004s. |
| Structural AST inventory | passed: exactly the 12 selected lines are actual-first; lines 126 and 178 remain in their original order. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.035s. |
| `git diff --check` | passed after the full B07 traceability pair and indexes were added. |

## Motivation and problem statement

The concrete Sonar rule, Parent test scope, and behavior-preservation rationale
are recorded in the preceding `## Motivation and decision` section. This
structural correction does not change the documented source or test behavior.

## Acceptance criteria

- Preserve the exact remediation and focused validation already recorded.
- Retain equivalent technical facts in this English/German Change Record pair.
- Do not convert blocked, unrun, or pending hosted evidence into a pass.

## Implementation decision and rationale

Keep the existing rationale and validation intact, and restore the canonical
Change Record headings instead of weakening the documentation checker or
creating a record-specific exception.

## Changed files

The original versioned scope is recorded in `## Identity` and the preceding
implementation narrative. This follow-up changes only the structure of this
Change Record pair.

## Commands executed

The exact commands and observed outcomes remain in `## Validation`; this
structural correction does not reclassify any result.

## Security impact

The existing section below remains authoritative for this record's specific
boundary. This normalization changes no security control.

## Security impact and limitations

`not_applicable` to production code: this is test-diagnostic ordering only.
Payload-redaction, hash-only retention, and forbidden-payload assertions remain
intact and passed before and after the edit. The local candidate is uncommitted;
no hosted Sonar analysis, GitHub CI, commit, push, pull request, or master
merge has occurred. The listed keys remain OPEN until a delivered head is
analyzed.

## Runtime evidence

No additional runtime evidence is claimed by this structural correction; the
existing validation retains only its recorded Parent test-method scope.

## Known limitations

The record's focused validation remains narrower than a complete runtime
matrix and hosted analysis.

## Remaining risks

No new risk is introduced by record normalization. Hosted analysis remains
limited to results actually observed for a later delivery head.

## Checks not run and rationale

No additional connector runtime matrix or hosted check is run for this
documentation-only correction.

## Final diff and review status

The earlier delivery wording is a snapshot of the original local validation.
This record does not assert a final PR verification, merge, or Sonar issue
closure for a later delivery head.
