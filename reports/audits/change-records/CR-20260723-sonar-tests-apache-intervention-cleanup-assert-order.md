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

The current Parent-only integration branch was checked after its normal,
non-rewriting update from current Parent master. The focused module completed
five tests successfully, and an AST inspection confirmed that exactly the two
selected `assertEqual` calls place the observed expression before the fixed
expected value.

### Current Parent-master update — 2026-07-24

Existing Draft PR #105 remains the delivery vehicle. Its previous remote head
`60b8254e45b00ddbac556ff78cd0af3490e26ff2` was normally updated without a
rebase by merging Parent master
`053a9ca5b0f9351319c96d359107c53ba8f9d3a1`. The resulting local merge commit
`709493f9b219db246701a8023ed853e86a3026e7` resolves only the shared English
and German Change Record indexes. It does not modify Framework or MRTS; it
only inherits existing master history. The current PR-base diff remains this
Parent test, this English/German Change Record pair, and those indexes, with
no Framework, MRTS, gitlink, production-source, scanner, Gate, suppression,
or security-control change authored by this PR update.

Hosted-check, SonarQube Cloud, Quality Gate, review, readiness, and merge
results are claimed only through observed exact-head PR delivery metadata.
This record neither transfers old-head results to the new head nor invents a
later delivery result.

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

- Current merged-tree focused affected-module test: passed (5 tests).
- Current merged-tree AST operand-order validation: passed (2 selected calls).
- Current Parent-master update and conflict resolution: passed; normal,
  non-rewriting merge `709493f9b219db246701a8023ed853e86a3026e7` resolves only
  the paired Change Record indexes.
- Targeted bilingual-documentation test: passed (11 tests).
- Scoped `git diff --check`: passed.

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
- Hosted checks and SonarQube Cloud PR analysis are external delivery evidence:
  only an observed current exact remote head may satisfy this requirement
  before protected merge.

## Final diff and review status

The existing Parent-only PR #105 is the delivery vehicle. Its task-owned
branch contains the normal current-master update merge
`709493f9b219db246701a8023ed853e86a3026e7` and paired delivery-evidence
documentation. This record claims neither review approval, merge, nor a
default-branch change. Before protected merge, the PR must be non-draft and
its current exact remote head must have passing hosted checks and SonarQube
Cloud analysis plus refreshed review state; those observed facts belong to
delivery metadata rather than an unobserved claim in this record.
