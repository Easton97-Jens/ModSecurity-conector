# Change Record: Parent full-lifecycle profile assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260724-sonar-tests-full-lifecycle-profiles-assertions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260724-sonar-tests-full-lifecycle-profiles-assertions |
| Date (UTC) | 2026-07-24 |
| Base revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Seven live Parent SonarQube Cloud `python:S3415` Code Smells: AZ-KYVRvfYmbqbBXVNFH, AZ-KYVRvfYmbqbBXVNFI, AZ-KYVRvfYmbqbBXVNFJ, AZ-KYVRvfYmbqbBXVNFK, AZ-KYVRvfYmbqbBXVNFL, AZ-KYVRvfYmbqbBXVNFM, and AZ-KYVRvfYmbqbBXVNFN. |
| Boundary | Parent test source plus this English/German traceability pair and indexes. The lifecycle-profile helper, connector behavior, Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, and generated artifacts remain unchanged. |

## Motivation and problem statement

The selected SonarQube Cloud rows report that seven existing `unittest`
assertions in the Parent full-lifecycle profile test place their expected value
before the observed result. The assertions already test the intended profile
and capability invariants; reversing only their first two operands improves
failure diagnostics without changing accepted or rejected behavior.

## Acceptance criteria

- Correct only the seven selected SonarQube Cloud assertions to actual-value
  first and expected-value second.
- Preserve every manifest fixture, profile mapping, capability state, message,
  temporary JSON write, and production source file.
- Pass the complete focused Parent unit module, selected-file syntax check,
  seven-call AST inventory, and diff hygiene check.
- Maintain complete synchronized English/German Change Records and indexes.
- Obtain exact-head GitHub and SonarQube Cloud Draft-PR evidence before
  describing the selected keys as verified.

## Implementation decision and rationale

Each selected `assertEqual` or `assertNotEqual` call now passes its existing
observed expression first and its unchanged expected literal or collection
second. No helper, fixture, expected value, assertion message, profile,
capability state, or runtime condition changed. This is the smallest
repository-native correction for `python:S3415` and preserves `unittest`
predicate semantics.

## Security impact

The focused security assessment is `not_applicable`: this is diagnostic
argument ordering in Parent test code only. Although the read-only adjacent
lifecycle helper has atomic file-writing behavior, that helper is unchanged.
The direct module uses in-memory manifests and a task-local temporary JSON
output; it does not invoke Framework, MRTS, a connector runtime, a network
client, a subprocess, or a dependency operation. No security finding is
claimed fixed.

## Changed files

- tests/test_full_lifecycle_profiles.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

The focused commands used the Parent `.venv` Python,
`PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, and a task-owned external
`TMPDIR`; selected-file syntax redirected `PYTHONPYCACHEPREFIX` outside the
checkout:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_full_lifecycle_profiles
- rtk proxy -- env ... <Parent .venv python> -m py_compile tests/test_full_lifecycle_profiles.py
- rtk proxy -- env ... <Parent .venv python> -c <AST inventory of the seven selected assertions>
- rtk proxy -- git diff --check

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused full-lifecycle profile unit module before and after the edit | passed: tests.test_full_lifecycle_profiles, 5 tests in each run. |
| Selected-file Python syntax | passed: tests/test_full_lifecycle_profiles.py compiled with pycache outside the checkout. |
| Selected-assertion AST inventory | passed: exactly seven selected anchors (60, 68, 85, 98, 103, 117, and 129) now have actual-first operands and unchanged expected values. |
| git diff --check | passed: no whitespace error. |
| Current-batch worktree bytecode scan | passed: no `*.pyc` file. |
| tests.test_bilingual_docs | passed: 11 tests. |
| Direct Change Record pair review | passed: both files have 13 level-two sections and matching ID, base revision, issue keys, and affected path literals. |
| make check-bilingual-docs | blocked_environment: exactly 20 pre-existing missing Framework-gitlink link targets; the output contains no new Change Record error. |
| make check-doc-links | blocked_environment: exactly 16 pre-existing missing Framework-gitlink link targets; no Framework source, gitlink, or generated artifact was changed. |
| Hosted-delivery checks | pending: Draft PR [#113](https://github.com/Easton97-Jens/ModSecurity-conector/pull/113) was created open and `isDraft: true` from initial remote head `8a97eb963bd16ff4c7fbc187bbe3f8396c036736`. This delivery-observation update creates a new final head, so checks, Quality Gate, PR issues, and review state must be freshly observed afterwards and are not claimed in advance. |

## Runtime evidence

No connector runtime behavior changed or is claimed. The focused module tests
only Parent lifecycle-profile transformations and a task-local atomic JSON
write; it is neither host-traffic nor production-runtime evidence.

## Checks not run and rationale

- Connector builds, configuration checks, host runtime smoke tests, protocol
  matrices, Framework checks, and MRTS checks are not applicable because no
  connector/runtime implementation changed and Framework/MRTS are excluded.
- Ruff and Pyright are not applicable: no Parent configuration is present and
  neither executable exists in the selected Parent `.venv`; no installation or
  configuration change was made merely for this diagnostic-order change.
- Draft PR #113 exists, but its final document-update head must receive fresh
  GitHub checks, SonarQube Cloud Quality Gate, PR issue, and review-state
  observation before `verified_pr`; no prior-head result is treated as final.

## Known limitations

This batch corrects only seven selected Parent SonarQube Cloud findings. It
does not claim to remediate the wider 1,474-item SonarQube Cloud backlog.

## Remaining risks

An unintended assertion-value change could weaken a profile/capability
control. The narrow diff, exact seven-call AST inventory, complete focused
module, and pending exact-head hosted validation reduce that risk. No runtime
or security behavior is inferred from this maintenance-only test change.

## Final diff and review status

The source correction and initial English/German traceability material are in
atomic commit `65c40bc`, followed by the observed-local-delivery traceability
commit `8a97eb9`, on
`codex/sonar-tests-full-lifecycle-profiles-assertions-20260724-master-5b8db00`,
whose initial parent is `5b8db00d44ab24f3a9f4216a00f7edee977b6898`. The
branch was pushed normally and opened as Draft PR #113 at initial observed
head `8a97eb963bd16ff4c7fbc187bbe3f8396c036736`; it is open and unmerged. This
document-update commit intentionally requires a fresh exact-head hosted
verification cycle. No merge, default-branch update, Framework action, MRTS
action, scanner-control change, or suppression occurred. Final delivery facts
are added only after they are observed.
