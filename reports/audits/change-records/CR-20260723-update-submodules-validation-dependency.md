# Change Record: Read-only Update-submodules validation dependency repair

**Language:** English | [Deutsch](CR-20260723-update-submodules-validation-dependency.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-update-submodules-validation-dependency |
| Date (UTC) | 2026-07-23 |
| Base revision | ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3 |
| Boundary | Parent `Update submodules` read-only validation workflow, its Parent static CI-security contract, a CI-only PyYAML hash lock, this English/German Change Record pair, and both Change-Record indexes. Framework source, MRTS, Parent gitlink, development dependency declaration, action pins, permissions, and publisher behavior remain unchanged. |
| Finding linkage | FND-PARENT-0048: current missing validation prerequisite; FND-PARENT-0045: prior Parent HAProxy fixture repair awaiting a successful hosted candidate validation. |
| Delivery status | Draft Parent [PR #92](https://github.com/Easton97-Jens/ModSecurity-conector/pull/92) carries the corrective series. Its first head exposed the YAML-scalar regression recorded as FND-PARENT-0049; the current amendment and its exact-head checks, review, SonarQube Cloud result, merge, and resulting-master verification remain pending. |

## Motivation and problem statement

The user authorized a separate PR to complete the pending `Update submodules`
repair. The single authorized current-master workflow run
[29981644356](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29981644356)
resolved the current Framework candidate and completed its read-only checkout
and interpreter controls, but `make quick-check` failed because the fixture
syntax checker could not import the already-declared `PyYAML>=6,<7` dependency.
The narrow publisher correctly skipped.

## Acceptance criteria

- The read-only validator installs its immutable CI-only PyYAML lock after
  its interpreter contract and before `make quick-check`.
- Static CI-security coverage asserts the command and ordering while preserving
  the resolver → read-only validator → narrow publisher control flow.
- The correction uses `--require-hashes` and `--only-binary=:all:` against the
  exact Linux x86_64 artifact; it does not change the cross-platform
  development dependency declaration, action pins, permissions, secrets,
  Framework/MRTS content, or the Parent gitlink.
- Focused tests, CI-security contract, security-diff review, whitespace check,
  and exact-head PR checks are recorded truthfully.
- This task opens a PR only; the master-only workflow is not presented as
  PR-head validation and no merge is performed.

## Implementation decision and rationale

The workflow now invokes the selected Python interpreter's Pip module with a
CI-only lock derived from the existing development declaration before candidate
validation. The lock names PyYAML 6.0.3 and the official Linux x86_64 wheel
SHA-256; Pip accepts only a binary artifact that matches that hash. This closes
the new package-acquisition boundary without changing the cross-platform
development declaration, creating a local environment, or using a broader
setup target. The step remains inside the `contents: read` validator, has no
explicitly injected secret or write-capable token, and the static contract
binds it between `Verify Python interpreter contract` and `make quick-check`.
It prevents both the missing-prerequisite regression and unpinned/source-build
fallback without weakening the publisher gate.

## Changed files

- `.github/workflows/update-submodules.yml`: install the hash-locked validation
  dependency in the read-only validator.
- `ci/requirements/update-submodules-validation-linux-x86_64.txt`: CI-only
  PyYAML 6.0.3 binary/hash lock for the GitHub-hosted Linux x86_64 validator.
- `tests/test_ci_security_workflows.py`: assert the dependency-installation
  command, lock identity, hash, and required ordering.
- This English/German Change Record pair and both Change-Record indexes.

No Framework source, MRTS, Parent gitlink, cross-platform development dependency
declaration, action pin, workflow permission, secret, or publisher code is
changed.

## Commands executed

- Hosted diagnostic: run `29981644356` reached the exact Parent master
  `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3`; resolver, checkout, Python
  contract, and candidate checkout passed, while `make quick-check` exited 2
  at `check-framework-fixture-syntax` with `PyYAML is required for fixture
  syntax lint`. The publisher was skipped.
- Local validation passed: the focused update-submodules workflow-security
  test, `make check-ci-security-contract` (16 tests), and the focused
  bilingual-document suite (11 tests). `pip check`, official PyPI metadata
  comparison for the locked wheel hash, and `git diff --check` also passed.
- `make check-bilingual-docs` remains blocked by baseline missing linked files
  beneath the uninitialized Framework submodule; no Framework content was
  changed, and the focused English/German pair test passed.

## Security impact

The resolver validates a full official SHA, candidate code runs only in the
read-only validator, and the isolated writer remains gated on validation
success and revalidates the official SHA before changing only the gitlink.
The new Pip boundary is restricted to PyYAML 6.0.3's approved Linux x86_64
wheel hash and rejects source distributions. No permission, credential,
secret, action pin, candidate scope, or publisher path is broadened. The
focused supply-chain security-diff review of the CI correction completed with
complete source coverage and zero reportable findings. A final source-diff
review also covers the accompanying documentation wording before commit.

## Runtime evidence

Not applicable. This is a GitHub Actions prerequisite/contract repair; it does
not build or start a connector and does not establish an HTTP, H2, H3, or
runtime claim.

## Known limitations

The cross-platform `requirements-dev.txt` still declares the bounded PyYAML
range for local development. The CI-only lock intentionally supports the
current GitHub-hosted Linux x86_64 CPython 3.14 validator and fails closed if
that platform changes until an explicit lock update is reviewed. The hosted
`Update submodules` workflow checks out `master` by design, so it cannot
demonstrate the new PR head before a separately authorized integration.

## Remaining risks

Until a separately authorized merge and current-master workflow rerun succeed,
automated Framework candidate publication remains blocked. The existing
fail-closed validation and narrow publisher isolation prevent publication on
failure. No risk is accepted.

## Checks not run and rationale

- No local Pip installation: installing into the Parent `.venv`, system Python,
  or user site is outside this task and unnecessary for a static workflow
  contract test.
- A fresh `Update submodules` success is not runnable against this PR head
  because the workflow deliberately checks out `master`; it remains pending a
  separately authorized merge.
- Exact-head GitHub Actions, review, and SonarQube Cloud outcomes do not yet
  exist for the current amendment. The first Draft PR head exposed a YAML parse
  regression before candidate validation; that task-owned defect is being
  corrected without changing validation or publisher privileges.

## Final diff and review status

The source diff is deliberately limited to the read-only hash-locked setup
command, its static regression, and complete bilingual traceability. Local
validation, the focused security-diff review, and the final exact diff review
are complete for the initial correction. The Draft PR's YAML-scalar amendment,
its exact-head verification, and final review remain pending. No master change,
candidate PR, Framework/MRTS action, gitlink update, or branch cleanup has
occurred.
