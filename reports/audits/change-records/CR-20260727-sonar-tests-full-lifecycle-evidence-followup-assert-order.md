# Change Record: Parent full-lifecycle evidence follow-up assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-full-lifecycle-evidence-followup-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-full-lifecycle-evidence-followup-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVT1fYmbqbBXVNGD (168), AZ-KYVT1fYmbqbBXVNGE (197), AZ-KYVT1fYmbqbBXVNGF (239), and AZ-KYVT1fYmbqbBXVNGG (251). |
| Boundary | Parent test source, this English/German Change Record pair, and their indexes. Full-lifecycle checker/runtime behavior, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, external Sonar issue state, GitHub state, and delivery remain unchanged. |

## Motivation and problem statement

The four selected `unittest.assertEqual` calls already check the intended
values but pass their expected value before the observed result. SonarQube
Cloud rule `python:S3415` requires the diagnostic order `actual, expected`.
Correcting only that order improves failure output without changing acceptance
criteria or the exercised full-lifecycle controls.

## Acceptance criteria

- Correct only the four tracked assertion calls to `actual, expected` order.
- Preserve every fixture, input, expected value, checker invocation, test
  branch, and production source file.
- Pass the four focused Parent-only methods before and after the edit.
- Pass an exact AST map for the four retained Sonar line anchors.
- Maintain this complete English/German Change Record pair and indexes, then
  run the applicable documentation and diff-hygiene checks.

## Implementation decision and rationale

The changed calls now place the existing observed result first: the integer
from `sanitizer.main(...)` before `0`, the already-bound `errors` list before
its expected list, `checker.profile_errors(...)` before `[]`, and
`checker.main(...)` before `1`. Each former expected operand is an inert
built-in literal or list construction. Moving the observed result before it
does not add an input, branch, filesystem target, process, or comparison type;
the equality domains remain built-in `int` or list values. No helper,
abstraction, fixture, expected string, or runtime condition was changed.

## Changed files

- `tests/test_full_lifecycle_evidence.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v <four selected FullLifecycleEvidenceTest methods>` before the edit.
- The same focused unittest command after the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST exact-map predicate>` after the edit.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` and `rtk proxy rg --files -g '*.pyc' .`.

## Security impact

`not_applicable` to production behavior: this is diagnostic argument order in
Parent test code only. The selected log-sanitizer test remains a same-boundary
credential/body-redaction control and passed before and after the edit. No
parser, path policy, subprocess contract, credential handling, transport
control, or connector enforcement behavior changed.

## Runtime evidence

No connector runtime behavior changed or is claimed. The four focused methods
use temporary local fixtures and validate Parent test/checker contracts only.

## Known limitations

This local batch addresses only four current Sonar Code Smells. The publicly
rechecked project endpoint still reports 1,125 `OPEN` issues; no external
Sonar state is inferred from this uncommitted candidate.

## Remaining risks

An unintended expected-value or fixture change could weaken the evidence
controls. The minimal four-call diff, before/after focused tests, exact AST
map, and preserved redaction control reduce that risk. An exact delivered-head
Sonar analysis remains necessary before any listed key can be treated as
resolved externally.

## Checks not run and rationale

- `tests.test_bilingual_docs` passed: 13 tests in 0.034s. The direct Change
  Record-pair validator passed, and `git diff --check` passed. The scoped
  bytecode scan found no `*.pyc` files (the no-match `rg` status is expected).
- The wider full-lifecycle module, connector builds, host runtime smoke tests,
  protocol matrices, Framework, and MRTS checks are not run: the change is
  limited to four Parent-only assertion diagnostics and does not alter those
  implementation boundaries.

## Final diff and review status

The B10 candidate is local, uncommitted, and unpushed. No GitHub CI,
SonarQube Cloud PR analysis, review, pull request, merge, default-branch
update, Framework action, or MRTS action has occurred.
