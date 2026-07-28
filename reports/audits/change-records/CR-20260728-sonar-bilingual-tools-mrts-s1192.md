# Change Record: Parent `tools/MRTS` literal extraction and direct Git-fixture coverage for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260728-sonar-bilingual-tools-mrts-s1192.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-bilingual-tools-mrts-s1192 |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Tracking | Parent SonarQube Cloud `python:S1192` candidate for the repeated `tools/MRTS` operational literal. The current task designates a Parent-only PR #157 candidate; it does not establish a hosted pull request or an external SonarQube Cloud resolution. |
| Boundary | Parent `ci/checks/documentation/check-bilingual-docs.py`, Parent `tests/test_bilingual_docs.py`, this English/German Change Record pair, and their indexes. Framework/MRTS content and Gitlinks, scanner configuration, Quality Gates, suppressions, external SonarQube Cloud state, GitHub state, connector/runtime behavior, and delivery are outside this bounded Parent-only candidate. |

## Motivation and problem statement

`check_tools_mrts_clean()` used the fixed `tools/MRTS` path string at three
operational locations: the Parent `git status` pathspec, the Framework-presence
guard, and the Framework `git status` pathspec. SonarQube Cloud rule
`python:S1192` identifies that repeated literal. The extraction must preserve
the existing pathspec ordering and all diagnostics, while direct fixtures must
prove that the checker ignores unrelated dirt and reports Parent and Framework
`tools/MRTS` dirt through real Git repositories.

## Acceptance criteria

- Define `TOOLS_MRTS = "tools/MRTS"` and use it only at the three existing
  operational locations in `check_tools_mrts_clean()`.
- Preserve the Parent and Framework `git status` argument order and the exact
  `tools/MRTS` diagnostics.
- Add direct temporary nested-Git fixtures covering unrelated dirt, Parent
  `tools/MRTS` dirt, and Framework `tools/MRTS` dirt.
- Assert the complete ordered `CHECKER.git_status` calls, including their
  working-directory `Path` arguments, in each direct fixture test.
- Maintain this English/German Change Record pair and both indexes, without
  asserting unobserved hosted PR, CI, SonarQube Cloud, review, or merge facts.

## Implementation decision and rationale

`TOOLS_MRTS = "tools/MRTS"` is a module-level owner for the duplicated
operational path literal. It replaces the Parent status pathspec, the Framework
directory-presence join, and the Framework status pathspec only. The combined
Parent Framework pathspec remains
`modules/ModSecurity-test-Framework/tools/MRTS`, so command ordering and
existing error text remain unchanged.

The additive tests initialize temporary Parent and nested Framework Git
repositories with committed, tracked baselines, including the Parent Framework
Gitlink, then wrap the real `CHECKER.git_status`. They cover unrelated dirty
Markdown files as the legitimate clean control, a dirty Parent
`tools/MRTS/.gitkeep`, and a dirty Framework `tools/MRTS/.gitkeep`. Each
compares the full ordered `call_args_list`, including the actual `cwd` `Path`
values, and hard-codes the expected Git arguments and diagnostics rather than
deriving them from `TOOLS_MRTS` or testing only a mock-specific helper.

## Changed files

- `ci/checks/documentation/check-bilingual-docs.py`
- `tests/test_bilingual_docs.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_bilingual_docs` passed from the isolated Parent worktree: 21 tests in 0.259s, `OK`.
- `rtk proxy -- git diff --check` passed for the final complete candidate after the source/test changes, this documentation pair, and both index updates; it produced no whitespace diagnostics.
- `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/checks/documentation/check-bilingual-docs.py` exited 1, `blocked_external_dependency`: it reported only missing `modules/ModSecurity-test-Framework` documentation/rule link targets in this isolated worktree, with no error for the changed Change Record pair or indexes.
- `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/checks/documentation/check-repository-path-references.py` exited 2, `blocked_external_dependency`, for the same missing Framework link targets and with no error for the changed Change Record pair or indexes.
- A no-write narrow structural check that loads `check-bilingual-docs.py` passed: required Change Record headings and identities, reciprocal language switches, both index references, and the selected shared technical literals are present.
- A disposable exact-candidate Parent/Framework overlay passed the full documentation route: Parent bilingual documentation (`bilingual docs ok`), Parent repository-path references (`repository path references: PASS`), and Framework documentation links (`doc links ok`). It used only the read-only Parent-pinned Framework archive `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` and temporary local Git baselines needed by the checker; it changed neither Framework source nor a Gitlink.

## Security impact

This is security-relevant checker maintenance: `check_tools_mrts_clean()`
invokes `git` subprocesses and protects the Parent/Framework/MRTS cleanliness
boundary. A focused command/path-integrity review was required and approved.
Its invariant is that source-controlled pathspecs run at the exact Parent and
Framework working directories, report dirty protected paths, and do not widen
the checked scope. The review found that `TOOLS_MRTS` is source-controlled and
that the exact existing argv ordering, `cwd` values, diagnostics, and
fail-closed dirty-path controls are preserved. The direct Git fixtures exercise
the legitimate unrelated-dirt control and both protected dirty-path failures.
No new finding was identified.

A pre-existing silent-nonzero-`git` edge case, in which a failed command could
return neither stdout nor stderr to `git_status()`, is unchanged and out of
scope for this literal-only candidate. This record does not claim that edge
case was remediated. The fixtures use local temporary repositories with no
credentials or network access.

## Runtime evidence

No connector, protocol, host, Framework, MRTS, report-generator, or production
runtime was run or changed. The focused unit suite exercises static checker
logic and temporary local Git repositories only; it is not runtime evidence.

## Known limitations

The direct fixture tests require a local `git` executable; it was available in
the observed focused run. They do not exercise a hosted PR, GitHub Actions,
SonarQube Cloud, a production connector, or a deployed Framework/MRTS runtime.
The full Parent bilingual and repository-path scripts are blocked in this
isolated worktree by absent Framework documentation/rule link targets. The
same exact candidate passed those checks in the disposable Parent/Framework
overlay recorded above; the isolated-worktree result therefore does not
establish a failure in the changed Change Record pair or indexes.
A pre-existing silent-nonzero-`git` edge case remains unchanged and outside
this literal-only scope.

## Remaining risks

An untested Git implementation, status presentation, or caller outside the
three tested cases could expose a behavior not represented by the temporary
fixtures. The direct fixtures preserve and assert the exact current calls and
diagnostics for the bounded Parent/Framework cases. The `python:S1192`
candidate cannot be described as resolved externally until SonarQube Cloud
analyzes the exact delivered head.

## Checks not run and rationale

- Full builds, linters, integration/runtime matrices, and unrelated test suites
  are outside this small Parent-only documentation/checker candidate.
- `make check-doc-links` is not run because it first invokes `check-framework`
  and the Framework documentation-link checker; the current scope is
  Parent-only. Its Parent repository-path static checker was run directly, but
  is blocked by the same absent Framework link targets.
- No GitHub CI, remote SonarQube Cloud PR analysis, hosted pull request, review,
  commit, push, merge, default-branch update, Framework action, MRTS action, or
  Gitlink update has occurred as part of this candidate.

## Final diff and review status

This is a local Parent-only candidate on
`agent/sonar-652-bilingual-tools-mrts-s1192-20260728`, based on
`8e8acb8dab1cd03723de269cab7da7dd62e5e010`. Delivery is pending. The task's
PR #157 designation is a candidate label only: no hosted PR, remote head SHA,
CI result, Quality Gate, review, or merge evidence is asserted. Before this
candidate is described as externally verified, the local, remote, and hosted
PR-head SHAs must be observed equal and the required hosted checks must be
recorded for that exact head. No staging, commit, push, merge, Parent-`master`
change, Framework/MRTS change, or Gitlink update is performed by this
documentation contribution.
