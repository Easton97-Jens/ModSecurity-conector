# Change Record: locked CI test dependencies in version updaters

**Language:** English | [Deutsch](CR-20260814-locked-ci-test-dependencies.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260814-locked-ci-test-dependencies |
| Date (UTC) | 2026-08-14 |
| Base revision | `5e77de897841b62fd9e982f70cad3036fce570ef` |
| Delivery status | The current user has authorized controlled `master` integration of PR #288. Exact head, check, review, merge, resulting-`master`, and workspace facts are retained only after observation in the PR and task-completion record. |

## Motivation and problem statement

The user-supplied GitHub Actions run `31818093186` failed in `validate-go-patch`: it invoked `tests.test_ci_security_workflows`, whose import path needs PyYAML, before installing the existing hash-locked CI dependency set. Source inspection confirmed the same missing precondition in `validate-python-patch`.

`requirements-ci.lock` already pins `PyYAML==6.0.3` with hashes. This change uses that existing locked input; it does not add, update, or relax a Python dependency.

## Acceptance criteria

- Both version-updater validator jobs install `requirements-ci.lock` after their Python interpreter check and before their first import-sensitive test.
- Each installation uses `--require-hashes`, `--only-binary=:all:`, `--no-input`, and the existing lock file, then runs `python3 -m pip check`.
- Regression coverage verifies the lock file, flags, pip check, and ordering for both workflow jobs through existing job blocks and normalized shell scripts.
- No workflow permission, action pin, lockfile, package version, checkout, timeout, trigger, or test-suppression setting changes.

## Implementation decision and rationale

Each validator now has one small `Install hash-locked CI test dependency` step immediately after its existing Python interpreter contract step. The step runs `python3 -m pip install --disable-pip-version-check --no-input --only-binary=:all: --require-hashes -r requirements-ci.lock`, then `python3 -m pip check`. It establishes the dependency contract before the test module can import PyYAML and fails closed on an invalid or incomplete environment.

`tests/test_ci_security_workflows.py` adds a shared assertion using the existing `job_blocks` and `normalize_shell_script` helpers. The Go and Python updater tests each require the named install step, the locked command, pip check, and the required relative order before their first workflow test.

## Security impact

This is a CI dependency and code-execution boundary. The security invariant is that an import-sensitive workflow test receives only the pre-existing, hash-verified, binary-only dependency set and that its integrity check passes before test execution. The repair preserves the lockfile and all existing workflow controls; it does not introduce an unpinned PyYAML installation or weaken hashes, pins, permissions, or validation.

## Changed files

- `.github/workflows/update-go-version.yml`
- `.github/workflows/update-python-version.yml`
- `tests/test_ci_security_workflows.py`
- this English/German Change Record pair and its English/German archive index entries.

Local, ignored control-plane evidence is retained as `FND-PARENT-0131` under `.codex/findings/` and its matching `.codex/runs/` receipt. It is not silently force-added with unrelated local records.

## Commands executed

The repository-selected `.venv/bin/python3` was used because the Python policy requires a repository virtual environment rather than mutation of the system interpreter. The executed checks included:

- `.venv/bin/python3 -m pip install --disable-pip-version-check --no-input --only-binary=:all: --require-hashes -r requirements-ci.lock`
- `.venv/bin/python3 -m pip check`
- `.venv/bin/python -m unittest -v tests.test_ci_security_workflows`
- `.venv/bin/python3 -m compileall -q ci scripts tests`
- `PYTHON=.venv/bin/python make check-go-version-contract`
- the six-module version-updater and workflow-contract unittest invocation
- `make check-ci-security-contract`
- the checksum-verified `actionlint` fetch mechanism and both edited workflows.

## Tests and actual results

| Check | Actual result |
| --- | --- |
| Hash-locked CI dependency installation | passed; existing `PyYAML==6.0.3` lock entry satisfied |
| `python3 -m pip check` | passed; no broken requirements found |
| Focused CI workflow contracts | passed; 28 tests |
| `python3 -m compileall -q ci scripts tests` | passed, exit 0 |
| `make check-go-version-contract` | passed, exit 0 |
| Six-module version-updater/workflow contract suite | passed; 98 tests |
| `make check-ci-security-contract` | passed; 90 tests, 4 skipped |
| Checksum-verified `actionlint` (`v1.7.12`) on both edited workflows | passed, exit 0 |
| `make check-bilingual-docs` | passed; `bilingual docs ok` |
| `make check-doc-links` | passed; repository path references and documentation links passed |
| `git diff --check` | passed, exit 0 |

## Runtime evidence

The available evidence is local static workflow validation and Python contract execution. No GitHub-hosted runner, candidate-update path, or production runtime was executed or claimed.

## Checks not run and rationale

No exact-head GitHub Actions result existed when this Change Record was initially written. The controlled delivery lifecycle revalidates the exact current PR head and records hosted and resulting-`master` outcomes only after they occur; this record does not prestate them.

## Known limitations

The local checks establish the declared workflow structure and test ordering. They cannot by themselves prove a particular GitHub-hosted runner image, network condition, or cache state; protected exact-SHA hosted checks are the separate delivery evidence.

## Remaining risks

The runner-specific wheel-resolution condition is intentionally fail-closed: a missing wheel, hash mismatch, broken dependency set, or failed `pip check` stops the validator before its import-sensitive test. The exact hosted and resulting-`master` outcomes are retained separately once observed.

## Final diff and review status

The scoped source review found only the two requested workflow edits, their targeted regression coverage, and this required paired traceability record. `git diff --check`, `make check-bilingual-docs`, and `make check-doc-links` passed after the record and archive indexes were present. No hosted verification or delivery status is asserted.
