# Change Record: Python updater publisher dependency

**Language:** English | [Deutsch](CR-20260816-python-updater-publisher-dependency.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260816-python-updater-publisher-dependency |
| Date (UTC) | 2026-08-16 |
| Base revision | e1e3bc9bbd2a412721d4e4107e060160b75d01a6 |
| Delivery status | The current user authorized a focused Parent fix, commit, push, and a new Draft PR. Hosted pull-request validation remains pending. No master merge, direct master write, force action, bypass, or workflow rerun is authorized. |
| Finding | FND-PARENT-0164; source failure: GitHub Actions run 31935744923, job 95137374091 |

## Motivation and problem statement

The privileged publisher job of the Python patch updater imported tests that require PyYAML, but did not install the repository's hash-locked CI dependencies. Its mandatory revalidation therefore failed before it could create an update pull request.

## Acceptance criteria

- The publisher installs the existing hash-locked CI dependencies before its privileged App-token and revalidation stages.
- The installation uses `--require-hashes` and finishes with `python3 -m pip check`.
- A regression test proves the dependency step remains ordered before token minting and CI-security revalidation.

## Implementation decision and rationale

The publisher now uses the same locked dependency-installation contract already used by the unprivileged validator job. No package version, GitHub App permission, branch-protection rule, or quality gate was weakened or changed.

## Security impact

This preserves the fail-closed publisher boundary: CI-security revalidation must succeed before the job mints its repository-limited token or can create a branch and pull request. The change does not bypass tests, hashes, or privileged controls.

## Changed files

- `.github/workflows/update-python-version.yml`
- `tests/test_ci_security_workflows.py`

## Commands executed

- Targeted workflow-security regression test: passed after the workflow change; it failed first against the pre-fix workflow as intended.
- Focused Python workflow and contract tests: 85 passed.
- `ci/checks/common/check-python-version-contract.py --json`: passed, with 42 detected jobs and no violations.
- `make check-ci-security-contract`: passed, with 103 tests passed and 4 expected capability-limited skips.

## Runtime evidence

The referenced publisher job failed with `ModuleNotFoundError: No module named 'yaml'` while running `make check-ci-security-contract`. The installer adds PyYAML only through the existing hash-locked `requirements-ci.lock` contract.

## Known limitations

Hosted pull-request checks remain the next delivery gate. The first eligible post-merge publisher invocation will provide the end-to-end runtime confirmation; until then, the finding is fixed locally but not runtime-verified.

## Remaining risks

The publisher's master-only admission is an intentional control, so local and PR validation cannot substitute for its first eligible hosted execution. The locked dependency contract and focused workflow-security regression test provide the strongest pre-merge evidence without weakening that boundary.

## Checks not run and rationale

No live updater dispatch, App-token mint, publisher branch creation, or master merge was run. The publisher admission policy intentionally permits only master schedule or manual-dispatch runs, and the user did not authorize a merge or rerun. Full connector runtime matrices are unrelated to this CI-only change.

## Final diff and review status

The scoped final diff contains only the publisher locked-dependency step, its
ordering regression, and this paired traceability record/index. `git diff
--check` passed. Commit, Draft PR creation, and hosted pull-request checks are
the remaining delivery steps for this revision.
