# Change Record: Parent connector-capabilities terminal assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-connector-capabilities-terminal-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-connector-capabilities-terminal-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVU7fYmbqbBXVNHA (376), AZ-KYVU7fYmbqbBXVNHB (387), AZ-KYVU7fYmbqbBXVNHC (425), AZ-KYVU7fYmbqbBXVNHD (432), AZ-KYVU7fYmbqbBXVNHE (433), AZ-KYVU7fYmbqbBXVNHF (434), and AZ-KYVU7fYmbqbBXVNHI (469). |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Connector-capabilities production behavior, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and decision

Seven selected assertions put literal/list/dictionary/name expected values
before observed merge, result, payload, or return-code values. This change
reverses only those first two arguments to `actual, expected`. The adjacent
validator rows at lines 450 and 454 remain unchanged: the first has a genuine
Framework-Gitlink environment blocker and the second has a `command.index()`
operand requiring separate evaluation-order review.

## Validation

| Check | Result |
| --- | --- |
| Four focused Parent-only methods before the edit | passed: 4 tests in 0.281s. |
| The same methods after the edit | passed: 4 tests in 0.282s. |
| Five-method preflight including line 450 | blocked_environment: exactly the uninitialized Framework canonical validator is missing; line 450 was excluded without a source edit. |
| Structural AST inventory | passed: exactly seven selected lines are actual-first; lines 450 and 454 remain original-order exclusions. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.035s. |
| `git diff --check` | passed after the full B09 traceability pair and indexes were added. |

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
The overlay/validation integrity assertions and Framework-boundary refusal are
retained. The local candidate is uncommitted; no hosted Sonar analysis, GitHub
CI, commit, push, pull request, or master merge has occurred. The listed keys
remain OPEN until a delivered head is analyzed.

## Runtime evidence

No additional runtime evidence is claimed by this structural correction; the
existing validation retains only its recorded Parent test-method scope.

## Known limitations

The record retains the explicit blocked Framework-validator prerequisite and
does not treat its absence as a successful aggregate test result.

## Remaining risks

No new risk is introduced by record normalization. Hosted analysis remains
limited to results actually observed for a later delivery head.

## Checks not run and rationale

No additional connector runtime, missing-Framework-validator aggregate suite,
or hosted check is run for this documentation-only correction.

## Final diff and review status

The earlier delivery wording is a snapshot of the original local validation.
This record does not assert a final PR verification, merge, or Sonar issue
closure for a later delivery head.
