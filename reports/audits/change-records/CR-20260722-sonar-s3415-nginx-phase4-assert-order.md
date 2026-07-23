# Change Record: Parent NGINX Phase-4 assertion ordering for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260722-sonar-s3415-nginx-phase4-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260722-sonar-s3415-nginx-phase4-assert-order |
| Date (UTC) | 2026-07-22 |
| Base revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Tracking | Five Parent-only `python:S3415` Code Smells: AZ-KYVUffYmbqbBXVNGX, AZ-KYVUffYmbqbBXVNGY, AZ-KYVUffYmbqbBXVNGZ, AZ-KYVUffYmbqbBXVNGa, and AZ-KYVUffYmbqbBXVNGb; retained finding ID FND-SONAR-0017. |
| Boundary | Only the Parent NGINX Phase-4 wiring test and this Parent traceability pair/index; Framework, MRTS, gitlinks, fixtures, production connector/runtime code, scanner configuration, and Quality Gates remain unchanged. |

## Motivation and problem statement

The current SonarQube Cloud inventory reports 2,005 open project findings.
Five active Parent `python:S3415` observations occur in
`tests/test_nginx_phase4_runner_wiring.py`. Each assertion uses a literal
expected value as the first `unittest.TestCase.assertEqual` argument and a
fixture-derived observed value second. Equality is symmetric, but actual-first
ordering makes failure diagnostics correctly identify observed and expected
values. The correction must remain a small five-key test-only change, without
suppressions or a project-wide mechanical sweep.

## Acceptance criteria

- Reorder exactly the five live `python:S3415` calls at lines 28, 30, 31, 32,
  and 47 so that the observed value is first and the literal expected value is
  second.
- Preserve each fixture name, expected mode, expected status, expected
  transport, and test behavior.
- Do not change Framework/MRTS content, a gitlink, fixture data, runtime
  behavior, dependency metadata, SonarQube Cloud settings, or a suppression.
- Run selected-file syntax, direct changed-test controls, structural ordering,
  bilingual/Change-Record checks, and final diff validation before delivery.
- Obtain fresh exact Draft-PR SonarQube Cloud evidence before claiming the
  five keys are resolved; the PR must remain unmerged.

## Implementation decision and rationale

Only the argument order changes: `assertEqual(actual, expected)` retains the
same predicate as the old calls and improves failure output. The two affected
test methods remain the focused behavioral controls for all five observations.
No source abstraction, assertion helper, rule suppression, or broad formatting
change is justified.

## Security impact

The change is confined to Parent test diagnostics. It changes no untrusted
input handling, parser/protocol behavior, file/path operation, subprocess,
dependency, credential, privilege, logging, validation, scanner, Quality-Gate,
suppression, `NOSONAR`, or false-positive control. The focused assessment is
not applicable to a separate security-finding workflow.

## Changed files

- tests/test_nginx_phase4_runner_wiring.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| Selected Parent virtual-environment identity check | passed: `/root/git/ModSecurity-conector/.venv/bin/python`, Python `3.14.4`, and venv prefix verified. |
| Selected-file Python syntax with external bytecode cache | passed: `python -B -s -m compileall -q tests/test_nginx_phase4_runner_wiring.py`. |
| Direct changed-test controls | passed: the two methods containing all five reordered assertions passed (2 tests) in a task-owned Parent overlay. The overlay reads the existing Framework runner only because the isolated Parent worktree deliberately leaves its Framework submodule uninitialized; no Framework or MRTS path was modified. |
| AST ordering control | passed: all five target lines have the exact actual-first / expected-second argument pairs. |
| `ruff check` and `ruff format --check` applicability | blocked: the selected Parent venv has no `ruff` module; no external-tool provisioning or repository dependency change is authorized for this focused repair. |
| Pyright applicability | blocked: the selected Parent venv has no `pyright` module; no external-tool provisioning or repository dependency change is authorized for this focused repair. |
| `pip check` | not applicable: the commit changes no dependency manifest, lock, package, or environment. |
| Full focused module with changed source | failed before the changed assertions: `test_generic_case_environment_carries_only_the_reviewed_mode` raises `TypeError: write_shell_env() missing 1 required keyword-only argument: 'output_root'`; the other 5 tests pass. |
| Full focused module with unmodified `origin/master` source | failed with the identical `write_shell_env` TypeError and the same 5 passing tests, proving the local failure predates this five-assertion change. |
| Focused Change Record pair contract | passed: required headings and matching identity values. |
| `tests.test_bilingual_docs` `unittest` module | passed: 11 tests. |
| Repository bilingual-document checker | blocked: its full-checkout run exits 1 only for pre-existing links into the intentionally uninitialized Framework submodule; no new Change Record path is reported. |
| `rtk proxy git diff --check` after source and traceability files | passed. |

This record does not claim an unobserved PR, CI, SonarQube Cloud, review, or
delivery result.

## Runtime evidence

No connector runtime path, Phase-4 behavior, fixture data, or production
implementation changes. The two direct Parent test methods are the behavioral
controls for the reordered diagnostics; they prove neither a connector build
nor a runtime lifecycle.

## Checks not run and rationale

- The complete local test module has a known baseline failure outside the five
  changed assertions. Its current `origin/master` source fails identically
  because the Parent test invokes `write_shell_env` without the required
  `output_root` argument from the read-only Framework runner. The current
  Parent gitlink is `784977615acfc55567e37b863309abc4a38ac877`; the available
  read-only Framework checkout is `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b`.
  Framework remediation is outside this Parent-only Sonar batch. Exact-head
  hosted checks remain required to validate the configured checkout pair.
- A connector build/runtime or CRS/MRTS matrix is not applicable: no connector
  source, production lifecycle, transport behavior, Framework file, or MRTS
  file changes.
- The repository-wide bilingual-document checker is blocked locally by the
  uninitialized Framework submodule; the focused record-pair contract and its
  11 checker tests pass. No Framework checkout is initialized or changed to
  turn that environmental prerequisite into an apparent documentation pass.
- Ruff and Pyright are unavailable from the selected Parent venv. They are
  optional quality tools for this scope and are not installed incidentally;
  the focused syntax, direct test, AST, documentation, and hosted quality-gate
  path remain the selected validation route.
- A full repository Sonar sweep is not local evidence. SonarQube Cloud PR
  analysis for the exact head is the required hosted decision point.

## Known limitations

This change treats five current Parent observations, not all 2,005 project
findings. The configured CI lane is Python `3.13.14` from `.python-version`,
while the available local Parent venv is Python `3.14.4`; exact-lane execution
remains a hosted requirement. The current local full-module baseline failure is
recorded rather than hidden or patched outside scope.

## Remaining risks

The broad Parent-only SonarQube Cloud backlog remains. Hosted exact-head
GitHub Actions, SonarQube Cloud Quality Gate, selected-key queries, and review
evidence are required before a Draft PR can be called verified; the PR must
remain unmerged.

## Current-master integration amendment (2026-07-23)

The historical 2026-07-22 baseline result above is retained for traceability.
After the Parent moved to master `b348c7ef78bfbce058dae06794e80b5f77515907`
with Framework gitlink `935cf14c676a24672be5c336e92cd13457cc35c8`, the
same full focused module reproduced the pre-existing `write_shell_env`
`output_root` API mismatch. The Parent-only test now passes its existing
`TemporaryDirectory` as `output_root`, preserving the Framework contained-write
control and changing neither Framework nor MRTS content. The complete focused
module passes all 6 tests after this adjustment. It is a compatibility repair
needed for current-master integration in addition to the five S3415 assertion
order changes.

This amendment supersedes the earlier prospective Draft/unmerged delivery
wording. Fresh exact-head hosted checks, SonarQube Cloud evidence, and review
evidence remain required before a protected merge.

## Final diff and review status

The intended source diff only swaps argument order in five `assertEqual` calls
and adds bilingual traceability. Before delivery, the final scoped diff,
documentation checks, exact local/remote/PR SHA relationship, applicable
GitHub checks, SonarQube Cloud Quality Gate, all-five-key query, and Draft PR
state must be rechecked for the actual head.
