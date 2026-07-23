# Change Record: Parent runtime-producer-readiness assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260723-sonar-tests-runtime-producer-readiness-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-tests-runtime-producer-readiness-assert-order |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Five Parent-only `python:S3415` Code Smells in `tests/test_runtime_producer_readiness_path_policy.py`: `AZ-KYVWWfYmbqbBXVNJa`, `AZ-KYVWWfYmbqbBXVNJb`, `AZ-KYVWWfYmbqbBXVNJc`, `AZ-KYVWWfYmbqbBXVNJd`, and `AZ-KYVWWfYmbqbBXVNJe`. |
| Boundary | Parent test source plus this English/German Change Record pair and indexes. Framework, MRTS, gitlinks, production source, scanner configuration, Quality Gates, suppressions, and runtime behavior remain unchanged. |

## Motivation and problem statement

SonarQube Cloud reports five `unittest.TestCase.assertEqual` calls whose
expected and actual operands are reversed. The assertions already express the
intended path-policy predicates; swapping only their first two operands aligns
failure diagnostics with the project convention without changing comparison or
pass/fail outcome.

## Decision

Correct the diagnostic argument order of five existing `unittest.assertEqual`
calls in `tests/test_runtime_producer_readiness_path_policy.py`. SonarQube
Cloud identifies `AZ-KYVWWfYmbqbBXVNJa`, `AZ-KYVWWfYmbqbBXVNJb`,
`AZ-KYVWWfYmbqbBXVNJc`, `AZ-KYVWWfYmbqbBXVNJd`, and
`AZ-KYVWWfYmbqbBXVNJe` as `python:S3415`: actual values must precede expected
values so a failure reports an actionable diagnostic.

## Scope and non-goals

The patch swaps only the first two positional arguments at the five flagged
assertions. It does not change predicates, expected statuses, path-policy
behavior, fixtures, mocked environment data, production code, security
controls, Sonar configuration, Quality Gates, Framework, MRTS, or gitlinks.

The Change Record and its German companion are the only documentation changes.
The shared indexes are updated for traceability. No merge or default-branch
write is part of this change.

## Security and compatibility

This is a test-diagnostic-only correction. The affected test continues to
exercise the existing source-root and system-write path controls; it does not
alter their implementation or assertion meaning. No security workflow is
triggered by this delta.

## Validation and delivery status

Before the edit, the focused module completed all four tests successfully on
the isolated current-master worktree. Post-change focused test, AST, syntax,
diff, bilingual-documentation, and exact Draft-PR-head verification evidence
are required before the record can claim a verified delivery result.

The intended delivery is a separate unmerged Draft PR. Hosted-check and
SonarQube Cloud results are not claimed in this record until observed for its
exact pushed head.

## Acceptance criteria

- Swap exactly the first two operands of the five selected `assertEqual` calls.
- Preserve predicates, fixtures, mocked environment data, expected statuses,
  and all path-policy behavior.
- Keep both Change Record languages and both indexes equivalent.
- Obtain exact Draft-PR-head SonarQube Cloud and hosted-check evidence before
  calling any selected key resolved.

## Implementation decision and rationale

Each selected assertion now supplies the observed status mapping value first
and its fixed expected status second. No predicate, fixture, test data,
production source, path resolver, security check, or optional assertion
argument changed.

## Changed files

- tests/test_runtime_producer_readiness_path_policy.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

- Focused affected-module test before and after the edit: passed (4 tests).
- AST operand-order and in-memory syntax validation: passed (5 selected calls).
- `tests.test_bilingual_docs`: passed (11 tests).
- `git diff --check`: passed.
- Full documentation/link checks: the repaired Change Record has no reported
  record-specific violation; both commands are blocked only by existing missing
  Framework-gitlink targets outside this task.

## Security impact

This is a test-diagnostic-only correction. The affected module continues to
exercise source-root and system-write path controls; neither their
implementation nor their assertion meaning changes. No security workflow is
triggered, and no security finding is claimed fixed.

## Runtime evidence

No connector runtime behavior changed or was claimed. The affected test uses
mocked environment data and temporary test paths; it is not a production host
runtime deployment or a Framework/MRTS run.

## Known limitations

This batch addresses only five selected `python:S3415` observations. It does
not claim to clear the larger SonarQube Cloud backlog or validate unavailable
runtime environments.

## Remaining risks

An accidental operand swap outside a selected assertion could make failure
diagnostics misleading. The exact five-call AST comparison and affected-module
test reduce that risk; fresh hosted exact-head analysis remains required before
delivery is verified.

## Checks not run and rationale

- No full connector build or host/runtime matrix: the delta only changes test
  diagnostic argument order and the complete affected module passes.
- No Framework or MRTS test or modification: both are excluded from this
  Parent-only task.
- Full hosted checks and SonarQube Cloud PR analysis: no Draft PR exists yet.

## Final diff and review status

Local implementation and focused validation are complete on the Parent-only
task branch. Hosted checks, Sonar analysis, and the Quality Gate remain pending
until a separate unmerged Draft PR is pushed. No review approval, merge, or
default-branch change is claimed or authorized.
