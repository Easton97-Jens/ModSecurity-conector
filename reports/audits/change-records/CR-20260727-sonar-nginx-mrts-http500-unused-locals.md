# Change Record: Parent NGINX MRTS HTTP-500 report unused-local cleanup for SonarQube Cloud S1481

**Language:** English | [Deutsch](CR-20260727-sonar-nginx-mrts-http500-unused-locals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-nginx-mrts-http500-unused-locals |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1481` Code Smells AZ7PU4lam6NRVhQ0A9r8 (332), AZ7PU4lam6NRVhQ0A9r9 (334), and AZ7PU4lam6NRVhQ0A9sA (428). |
| Boundary | Parent report-generator source, this English/German Change Record pair, and their indexes. Framework/MRTS repository content, Gitlinks, report semantics, path validation, scanner configuration, Quality Gates, suppressions, external Sonar issue state, GitHub state, and delivery remain unchanged. |

## Motivation and problem statement

Three local variables in the Parent NGINX MRTS HTTP-500 cluster report are
constructed but never consumed. SonarQube Cloud rule `python:S1481` reports
the unused `env_path`, `runtime_conf`, and `example` bindings. Keeping them
obscures which derived paths and report fields actually influence the payload.

## Acceptance criteria

- Remove only the three tracked unused local assignments.
- Preserve all used evidence paths, harness-root derivation, payload fields,
  report inputs, and verified-run-ID validation.
- Pass the focused invalid-run-ID control before and after the edit.
- Pass a no-write in-memory syntax compile and AST check proving no selected
  local assignment remains.
- Maintain this complete English/German Change Record pair and indexes, then
  run applicable documentation and diff-hygiene checks.

## Implementation decision and rationale

`env_path` and `runtime_conf` in `representative_cases(...)` and `example` in
`build_payload(...)` had no reads after their assignments. The change deletes
only those assignments. The used `evidence_path`, `harness_root`, case
configuration paths, `reps`, input metadata, report payload, and calls to
`validate_verified_run_id(...)` are unchanged. The file is Parent-owned even
though it describes MRTS evidence; no Framework or MRTS source is modified.

## Changed files

- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_runtime_path_security.RuntimePathSecurityTest.test_run_id_is_checked_before_lifecycle_and_report_path_joins` before the edit.
- The same focused run-ID-control test after the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <in-memory compile(source_text, filename, "exec")>` before and after the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST no-selected-local-store predicate>` after the edit.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` and `rtk proxy rg --files -g '*.pyc' .`.

## Security impact

`not_applicable` to the product diff: the removed variables did not mediate a
filesystem, subprocess, network, or report-publication operation. The same
focused security control still rejects traversal and absolute verified-run IDs
before `build_payload(...)` joins any report/runtime path. No path-validation,
ownership, symlink, or publication control changed.

## Runtime evidence

No NGINX, CRS, MRTS, connector, report-generation, or host runtime was
executed. The focused test uses an invalid run ID and intentionally fails
before consuming a Framework path or report input; it is Parent test-contract
evidence only.

## Known limitations

`python -B -m py_compile` is `blocked_environment` in this mounted worktree:
the standard-library command attempts to create the source-adjacent
`ci/evidence/reports/__pycache__`, which is read-only. No cache was created.
The recorded in-memory `compile(...)` check validates syntax without writing
outside the task-owned temporary root. This batch addresses only three current
Sonar Code Smells; the public project endpoint still reports 1,125 `OPEN`
issues, and this uncommitted candidate changes no external Sonar state.

## Remaining risks

An unrecognized read of a deleted local could change report construction. The
direct reference review, no-store AST check, before/after run-ID control, and
in-memory syntax check reduce that risk. An exact delivered-head Sonar analysis
remains necessary before the listed keys can be treated as resolved externally.

## Checks not run and rationale

- `tests.test_bilingual_docs` passed: 13 tests in 0.035s. The direct Change
  Record-pair validator passed, and `git diff --check` passed. The scoped
  bytecode scan found no `*.pyc` files (the no-match `rg` status is expected).
- The full report generator, NGINX/CRS/MRTS matrix, connector builds, and
  Framework/MRTS checks are not run because the change deletes dead Parent
  locals only; running them would consume unrelated runtime inputs.

## Final diff and review status

The B12 candidate is local, uncommitted, and unpushed. No GitHub CI,
SonarQube Cloud PR analysis, review, pull request, merge, default-branch
update, Framework action, or MRTS action has occurred.
