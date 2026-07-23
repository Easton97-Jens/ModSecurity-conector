# Change Record: Optional-prerequisite assertion diagnostic order for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260723-sonar-tests-optional-prerequisite-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-tests-optional-prerequisite-assert-order |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | FND-SONAR-0020; 77 current python:S3415 findings in tests/test_optional_prerequisite_status.py, from AZ-KYVRgfYmbqbBXVND6 through AZ-KYVRgfYmbqbBXVNFG. |
| Boundary | Parent test source, this English/German Change Record pair, and their indexes. Framework, MRTS, gitlinks, runtime product code, scanner configuration, Quality Gates, suppressions, exclusions, issue state, and default branch remain unchanged. |

## Motivation and problem statement

The 77 equality and inequality assertions in the optional-prerequisite status test
presented a fixed expected operand before the observed operand. The predicates
were correct, but their failure diagnostics did not follow the repository
actual-before-expected convention.

The current official query identifies 73 assertEqual calls and four
assertNotEqual calls in this exact Parent file. This is a maintainability
remediation only; it changes no optional-prerequisite classification,
status-file behavior, Apache preflight behavior, or runtime execution.

## Acceptance criteria

- All 77 selected assertion sites present observed actual values first and
  fixed expected values second.
- The assertion method, predicate, line association, and every optional third
  diagnostic argument remain unchanged.
- The full affected test module retains its valid, blocked, failed, symlink,
  and status-channel controls.
- No rule, Quality Gate, exclusion, suppression, NOSONAR, or issue state is
  changed.
- Fresh exact-head SonarQube Cloud and hosted-check evidence is required before
  the findings are declared verified on an unmerged Draft PR.

## Implementation decision and rationale

Only the first two operands of the 77 existing unittest assertions are
swapped. Equality and inequality truth values are preserved because the
relations are symmetric, while a failure now reports the observed value in the
conventional first position.

No helper, status-runner command, fixture, subprocess invocation, status JSON
field, or assertion message is refactored or removed. The base-to-candidate
AST mapping accounts for all 77 sites: 73 assertEqual and four assertNotEqual,
with no unselected equality or inequality assertion call in the file.

## Changed files

- tests/test_optional_prerequisite_status.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Security impact

This change is not applicable as a runtime security modification: it changes
only test diagnostic operand order. It leaves the status writer runtime-root,
symlink, status-channel, optional-prerequisite, and blocked-result controls
intact. No security or scanner control is weakened.

## Commands executed

- Focused tests.test_optional_prerequisite_status: all 20 tests passed before
  and after the operand-order correction.
- In-memory base-to-candidate AST mapping: all 77 selected calls passed the
  method, operand-swap, assertion-shape, and optional-message checks.
- git diff --check: passed for the source-only candidate before this record
  pair was added.

## Runtime evidence

The focused module uses its existing synthetic dependent-check fixtures to
validate success, accepted and unapproved blocked states, status persistence,
symlink rejection, and same-user path-swap protection. Those controls are
unchanged; no live Apache, Framework, MRTS, or connector runtime is claimed.

## Validation status

The affected module passed all 20 tests before and after the correction. The
source mapping proves that each selected Sonar site has only its first two
operands swapped and any third diagnostic argument preserved. Targeted
bilingual documentation, final scoped diff, and exact-head delivery evidence
remain required after this record is included in the Draft-PR candidate.

## Known limitations and follow-up

This record verifies only the 77 current Parent S3415 findings in the named
test file. It does not claim that the project-wide 1,474-item inventory or
other test, CI, Common, Scripts, or connector findings are resolved.

## Remaining risks

The test behavior is intentionally unchanged. The remaining delivery risk is
external: the source must still pass fresh SonarQube Cloud analysis and hosted
checks on the exact unmerged Draft-PR head.

## Checks not run and rationale

- No Framework or MRTS test or modification: both are outside this Parent-only
  batch.
- No live Apache or full connector runtime: the assertion-order-only change is
  covered by the complete direct test module.
- Hosted checks and exact-head SonarQube Cloud analysis: unavailable until the
  branch is committed, pushed, and opened as an unmerged Draft PR.

## Delivery status

The candidate is prepared on an isolated Parent task branch based on the
recorded master revision. It may be committed, pushed, and opened only as an
unmerged Draft PR after final local validation. No merge, default-branch
update, rebase, force-push, or Framework/MRTS change is authorized.

## Final diff and review status

The source-only diff contains 77 operand-pair swaps and no behavioral test
logic change. Final documentation validation, staged diff review, and fresh
exact-head delivery evidence are pending; this record makes no premature
Quality Gate or PR-status claim.
