# Change Record: Parent full-lifecycle evidence assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260724-sonar-tests-full-lifecycle-evidence-assertions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260724-sonar-tests-full-lifecycle-evidence-assertions |
| Date (UTC) | 2026-07-24 |
| Base revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
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
- Git commit/push/Draft-PR creation, hosted GitHub checks, review inspection,
  and SonarQube Cloud exact-head verification are pending the delivery
  milestone; no result is claimed here in advance.

## Known limitations

This batch corrects only five selected Parent SonarQube Cloud findings. It
does not claim to remediate the wider 1,474-item SonarQube Cloud backlog.

## Remaining risks

An unintended assertion-value change could weaken an evidence control. The
scoped diff, five-call AST inventory, and complete focused 17-test module
reduce that risk; exact-head hosted analysis remains required before the keys
are verified.

## Final diff and review status

Local implementation and focused validation are complete on a task branch
based on `5b8db00d44ab24f3a9f4216a00f7edee977b6898`. Commit, normal push,
Draft PR creation, and exact-head GitHub/SonarQube Cloud/review evidence are
still pending. No merge, default-branch update, Framework action, or MRTS
action is authorized or performed.
