# Change Record: Parent Apache intervention-cleanup assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260723-sonar-tests-apache-intervention-cleanup-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-tests-apache-intervention-cleanup-assert-order |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Two Parent-only `python:S3415` Code Smells in `tests/test_apache_intervention_cleanup.py`: `AZ-KYVR8fYmbqbBXVNFO` and `AZ-KYVR8fYmbqbBXVNFP`. |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Framework, MRTS, gitlinks, Apache production source, scanner configuration, Quality Gates, suppressions, and runtime behavior remain unchanged. |

## Motivation and problem statement

SonarQube Cloud reports two `unittest.TestCase.assertEqual` calls whose
expected and observed operands are reversed. The assertions already encode the
Apache intervention-cleanup invariants; swapping only their first two operands
aligns failure diagnostics with the project convention without changing the
comparison or pass/fail result.

## Decision

Correct the diagnostic argument order of the two existing
`unittest.assertEqual` calls in `tests/test_apache_intervention_cleanup.py`.
SonarQube Cloud identifies `AZ-KYVR8fYmbqbBXVNFO` and
`AZ-KYVR8fYmbqbBXVNFP` as `python:S3415`: the observed value must precede the
fixed expected value, so a failure reports an actionable diagnostic.

## Scope and non-goals

The patch swaps only the first two positional arguments at the two flagged
assertions. It does not change the tested C source, predicates, expected
values, fixtures, test data, Apache behavior, cleanup ownership, security
controls, Sonar configuration, Quality Gates, Framework, MRTS, or gitlinks.

The Change Record and its German companion are the only documentation changes.
The shared indexes are updated for traceability. No merge or default-branch
write is part of this change.

## Security and compatibility

This is a test-diagnostic-only correction. The test continues to exercise the
existing cleanup-ownership contract in Apache source; it does not alter the C
implementation or its assertion meaning. No security workflow is triggered by
this delta.

## Validation and delivery status

Before and after the edit, `make check-apache-intervention-cleanup` completed
all five test cases successfully on the isolated current-master worktree. An
AST operand-order inspection also confirmed that only the two selected calls
now supply actual then expected values. The targeted bilingual-documentation
test and scoped diff check passed. The full documentation commands are blocked
only by pre-existing missing Framework-gitlink targets and emitted no task
Change Record error. Exact Draft-PR-head verification remains required before
this record can claim a verified delivery result.

The intended delivery is a separate unmerged Draft PR. Hosted-check and
SonarQube Cloud results are not claimed in this record until observed for its
exact pushed head.

## Acceptance criteria

- Swap exactly the first two operands of the two selected `assertEqual` calls.
- Preserve the Apache cleanup predicates, expected values, C source, fixtures,
  and all test behavior.
- Keep both Change Record languages and both indexes equivalent.
- Obtain exact Draft-PR-head SonarQube Cloud and hosted-check evidence before
  calling either selected key resolved.

## Implementation decision and rationale

Each selected assertion now supplies its observed expression first and its
fixed expected literal or list second. No predicate, fixture, source text,
security control, or optional assertion argument changed.

## Changed files

- tests/test_apache_intervention_cleanup.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- Focused affected-module test before and after the edit: passed (5 tests).
- AST operand-order validation: passed (2 selected calls).
- `tests.test_bilingual_docs`: passed (11 tests).
- `git diff --check`: passed.
- Full documentation/link checks: blocked only by known missing
  Framework-gitlink targets; no task Change Record error was emitted.
- Full Draft-PR-hosted/SonarCloud analysis: pending because no Draft PR exists
  yet.

## Security impact

This is a test-diagnostic-only correction. The module continues to exercise
cleanup ownership after a native Apache intervention; neither the C
implementation nor the assertion's logical meaning changes. No security
finding is claimed fixed.

## Runtime evidence

No connector runtime behavior changed or was claimed. The affected test reads
the controlled Parent Apache source contract; it is not a production host
runtime deployment or a Framework/MRTS run.

## Known limitations

This batch addresses only two selected `python:S3415` observations. It does
not claim to clear the broader SonarQube Cloud backlog or validate an Apache
host build/runtime environment.

## Remaining risks

An accidental operand swap outside a selected assertion could make failure
diagnostics misleading. The two-call AST comparison, scoped diff, and complete
affected module reduce that risk; fresh hosted exact-head analysis remains
required before delivery is verified.

## Checks not run and rationale

- No full Apache build or connector/runtime matrix: the delta changes only
  test diagnostic argument order and the complete affected module passes.
- No Framework or MRTS test or modification: both are excluded from this
  Parent-only task.
- Full hosted checks and SonarQube Cloud PR analysis: no Draft PR exists yet.

## Final diff and review status

Local implementation and focused validation are complete on the Parent-only
task branch. Hosted checks, Sonar analysis, and the Quality Gate remain
pending until the separate unmerged Draft PR is pushed. No review approval,
merge, or default-branch change is claimed or authorized.
