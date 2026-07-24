# Change Record: Parent full-lifecycle evidence assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260724-sonar-tests-full-lifecycle-evidence-assertions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260724-sonar-tests-full-lifecycle-evidence-assertions |
| Date (UTC) | 2026-07-24 |
| Base revision | 8e36b86ac17bce06003b0505fe26f6bb60c3cec7 |
| Tracking | Five live Parent SonarQube Cloud `python:S3415` Code Smells: AZ-KYVT1fYmbqbBXVNF-, AZ-KYVT1fYmbqbBXVNF_, AZ-KYVT1fYmbqbBXVNGA, AZ-KYVT1fYmbqbBXVNGB, and AZ-KYVT1fYmbqbBXVNGC. |
| Boundary | Parent test source plus this English/German traceability pair and indexes. Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, full-lifecycle checker/runtime behavior, and generated artifacts remain unchanged. |

## Motivation and problem statement

The selected SonarQube Cloud rows report that five existing
`unittest.assertEqual` calls in the Parent full-lifecycle evidence test place
their expected value before the actual result. The assertions already test the
right values and control paths; reversing only their operand order improves
failure diagnostics without changing what the test accepts or rejects.

## Acceptance criteria

- Correct only the five selected assertions to actual-value first and
  expected-value second.
- Preserve every fixture, expected string/list, checker invocation, test
  branch, and production source file.
- Pass the direct Parent full-lifecycle evidence unit module, a source/AST
  inventory of the five calls, and diff hygiene checks.
- Maintain a complete English/German Change Record pair and indexes.
- Obtain exact-head GitHub and SonarQube Cloud Draft-PR evidence before
  describing the selected keys as verified.

## Implementation decision and rationale

Each selected call now passes the existing checker expression as the first
`assertEqual` argument and the unchanged expected list as the second. No new
helper, abstraction, fixture, expected value, assertion message, or runtime
condition was introduced. This is the smallest repository-native correction
for `python:S3415` and preserves normal `unittest` semantics.

## Security impact

The focused security assessment is `not_applicable`: this change affects only
diagnostic argument order in Parent test code. It does not change a parser,
filesystem/path sink, subprocess, credential, permission, network/CI control,
security validation, or connector enforcement behavior. The existing
full-lifecycle negative tests and the log-sanitizer control remain unchanged
and pass in the focused module run. No security finding is claimed fixed.

## Changed files

- tests/test_full_lifecycle_evidence.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

The focused commands used the Parent `.venv` Python,
`PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, and a task-owned external
`TMPDIR`:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_full_lifecycle_evidence
- rtk proxy -- env ... <Parent .venv python> -c <AST inventory of the five selected assertEqual calls>
- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_bilingual_docs
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-bilingual-docs
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-doc-links
- rtk proxy -- git diff --check
- rtk proxy -- find <current batch worktree> -name '*.pyc' -type f
- rtk proxy -- gh pr checks 112 --repo Easton97-Jens/ModSecurity-conector --watch --interval 15
- rtk proxy -- curl -fsSL <official SonarQube Cloud PR, Quality Gate, and PR-issue endpoints>

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused full-lifecycle evidence unit module before and after the edit | passed: tests.test_full_lifecycle_evidence, 17 tests each run. |
| Selected-assertion AST inventory | passed: exactly five selected line anchors now have checker expressions as actual values and unchanged expected lists. |
| git diff --check | passed: no whitespace error. |
| Current-batch worktree bytecode scan | passed: no `*.pyc` file. The shared overall run temporary directory contains six pre-existing bytecode files from earlier batch worktrees, which are outside this batch scope. |
| tests.test_bilingual_docs | passed: 11 tests. |
| Direct Change Record pair review | passed: both files have 13 aligned level-two sections and all IDs, issue keys, paths, commands, and non-translated technical literals match. |
| make check-bilingual-docs | blocked_environment: exactly 20 pre-existing missing Framework-gitlink link targets; the output identifies no new Change Record error. |
| make check-doc-links | blocked_environment: exactly 16 pre-existing missing Framework-gitlink link targets; no Framework source, gitlink, or generated artifact was changed. |

## Runtime evidence

No connector runtime behavior changed or is claimed. The focused test validates
Parent evidence/checker contracts with temporary local fixtures; it is neither
host-traffic nor production-runtime evidence.

## Checks not run and rationale

- Connector builds, configuration checks, host runtime smoke tests, protocol
  matrices, Framework, and MRTS checks are not applicable because no
  connector/runtime implementation changed and Framework/MRTS are excluded.
- Initial exact-head Draft-PR verification for
  `726f56d7787289b8c9f91b68a7b315e5b35a410e` passed: 33 GitHub checks
  succeeded, 6 were scope-appropriate skips, and none failed, remained
  pending, cancelled, or unknown. The official SonarQube Cloud Quality Gate
  was `OK` with zero open PR issues; reviews, inline review comments, and
  review threads each total zero. This traceability commit creates a newer PR
  head, which is independently reverified after push and retained in the PR
  and task receipt rather than claimed in advance here.

## Known limitations

This batch corrects only five selected Parent SonarQube Cloud findings. It
does not claim to remediate the wider 1,474-item SonarQube Cloud backlog.

## Remaining risks

An unintended assertion-value change could weaken an evidence control. The
scoped diff, five-call AST inventory, and complete focused 17-test module
reduce that risk; exact-head hosted analysis remains required before the keys
are verified.

## Current-master update and final local verification

Normal no-rewrite merge `1c8a2b9` incorporated current Parent master
`8e36b86ac17bce06003b0505fe26f6bb60c3cec7` into the isolated PR branch. It
resolved only the paired Change Record indexes. The inherited master history
includes the already-present Framework gitlink transition under the user's
narrow authorization; Framework and MRTS were not checked out, changed,
tested, merged, or delivered, and the final PR diff has no gitlink,
Framework, or MRTS path.

On that exact pre-record-correction tree,
`tests.test_full_lifecycle_evidence` passed all 17 tests,
`tests.test_bilingual_docs` passed all 11 tests, the five-call AST inventory
verified actual-first checker calls at the selected anchors, and
`git diff --check origin/master...HEAD` passed. This documentation correction
creates a new PR head, so all hosted exact-head checks, SonarQube Cloud
Quality Gate, and review/conversation evidence must be freshly revalidated
before the Draft PR can be marked ready.

## Final diff and review status

The source implementation remains in initial commit
`726f56d7787289b8c9f91b68a7b315e5b35a410e`; this Change Record is updated
without embedding a self-referential final head. Draft PR #112 remains open,
Draft, and unmerged until its final exact head has current base, local,
hosted, SonarQube Cloud, and review evidence. No merge, default-branch update,
Framework action, or MRTS action is authorized or performed by this record.
