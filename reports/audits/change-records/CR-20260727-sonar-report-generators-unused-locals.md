# Change Record: Parent report-generator unused-local cleanup for SonarQube Cloud S1481

**Language:** English | [Deutsch](CR-20260727-sonar-report-generators-unused-locals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-report-generators-unused-locals |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1481` Code Smells AZ7K5CQgixFPtcnbna1K (443) and AZ7K5CR4ixFPtcnbna1Z (376). |
| Boundary | Parent report-generator source, this English/German Change Record pair, and their indexes. Framework/MRTS repository content, Gitlinks, report inputs/outputs, command execution, path validation, scanner configuration, Quality Gates, suppressions, external Sonar issue state, GitHub state, and delivery remain unchanged. |

## Motivation and problem statement

Two Parent report generators retain dead local bindings: the missing-command
error returned by `command_exists(...)` in a path that uses only resolution
and return code, and a report-directory path constructed before the actual
queue/report path is selected. SonarQube Cloud rule `python:S1481` reports both
as unused, which obscures the values that actually drive behavior.

## Acceptance criteria

- Change only the one ignored tuple element to `_` and remove only the one
  unused `report_dir` assignment.
- Preserve command-resolution result handling, missing-tool records, queue
  selection, evidence reads, and intervention-record construction.
- Pass controlled no-command resolution and empty-queue checks before and
  after the edit.
- Pass no-write in-memory syntax compilation and an exact AST mapping.
- Maintain this complete English/German Change Record pair and indexes, then
  run applicable documentation and diff-hygiene checks.

## Implementation decision and rationale

`resolve_candidate_list(...)` now discards the unused second tuple element as
`_`; it still reads the same `resolved` value and `rc` result before creating a
missing-tool record or resolving a tool. `build_records(...)` no longer
constructs unused `report_dir`; its existing `report_path(...)` call remains
the source of the queue path. No command, report file, Framework path, or
MRTS content is newly selected or omitted.

## Changed files

- `ci/evidence/reports/generate-system-environment-proof.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <in-memory compile of both sources>` before and after the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <registered-import mocked missing-command resolution>` before and after the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <mocked empty intervention-queue check>` before and after the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST exact no-dead-local predicate>` after the edit.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` and `rtk proxy rg --files -g '*.pyc' .`.

## Security impact

`not_applicable` to the product diff: the tuple discard does not change which
command candidates are evaluated, and the removed report-directory construction
never mediated a read/write. The focused resolution check mocks a missing
command and confirms the same `missing` record without invoking a process. The
focused intervention check mocks an empty queue and confirms no evidence path
is read. No command, path, ownership, or publication control changed.

## Runtime evidence

No system-environment discovery command, report generator, connector, NGINX,
Framework, MRTS, or host runtime was executed. All controls use in-memory
source compilation or mocked Parent function inputs only.

## Known limitations

The first direct dynamic import of `generate-system-environment-proof.py`
failed before the target function because the test harness did not register the
dataclass-bearing module in `sys.modules`. Registering it before execution is
the standard importlib setup; the corrected before/after check passed. This is
a harness setup observation, not a product failure. This batch addresses only
two current Sonar Code Smells; the public project endpoint still reports 1,125
`OPEN` issues, and this uncommitted candidate changes no external Sonar state.

## Remaining risks

An unrecognized consumer of a removed binding could alter a generator result.
The direct reference review, controlled before/after behavior checks, and
exact AST mapping reduce that risk. An exact delivered-head Sonar analysis
remains necessary before the listed keys can be treated as resolved externally.

## Checks not run and rationale

- `tests.test_bilingual_docs` passed: 13 tests in 0.036s. The direct Change
  Record-pair validator passed, and `git diff --check` passed. The scoped
  bytecode scan found no `*.pyc` files (the no-match `rg` status is expected).
- Full report generation, command discovery, evidence reads, connector builds,
  matrices, Framework, and MRTS checks are not run because they would consume
  unrelated external/runtime inputs and no implementation contract changed.

## Final diff and review status

The B13 candidate is local, uncommitted, and unpushed. No GitHub CI,
SonarQube Cloud PR analysis, review, pull request, merge, default-branch
update, Framework action, or MRTS action has occurred.
