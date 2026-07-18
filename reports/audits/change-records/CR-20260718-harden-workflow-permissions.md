# Change Record: Harden GitHub workflow permissions

**Language:** English | [Deutsch](CR-20260718-harden-workflow-permissions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-harden-workflow-permissions` |
| Date (UTC) | `2026-07-18` |
| Base revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Boundary | Parent workflow configuration, static contracts, fixtures, and traceability only; Framework, MRTS, connector source, secrets, and gitlinks unchanged. |

## Motivation and problem statement

GitHub Code Scanning reported five open Scorecard `TokenPermissionsID` alerts
for workflow-level write permissions. The scheduled submodule updater also
advanced a recursive remote submodule, ran `make quick-check`, and later used
`GH_TOKEN` to publish from the same job. This is a plausible trust-boundary
concern, although direct token exfiltration was not demonstrated.

The external setting `default_workflow_permissions: write` remains tracked by
`FND-GITHUB-0001`. Changing that setting is outside this Parent pull request,
so every current workflow now declares an explicit restrictive default.

## Acceptance criteria

- Every Parent workflow has top-level `permissions: contents: read`.
- Additional permissions are job-scoped and limited to documented cleanup,
  trusted publishing, or SARIF uploads.
- Recursive execution is separated from write-token publishing; every checkout
  disables persisted credentials.
- CodeQL, OSV, and Scorecard retain narrow `security-events: write` uploads.
- Static contracts and safe/unsafe fixtures cover the permission, PR-trigger,
  credential, submodule, cleanup, and SARIF boundaries.

## Implementation decision and rationale

- `cleanup-artifacts.yml` grants `actions: write` only to a checkout-free job.
- `test-full-smoke-sequential.yml` runs artifact cleanup in an independent,
  checkout-free `actions: write` matrix job. The heavy recursive-submodule job
  has only `contents: read` and runs after cleanup.
- `update-actions-versions.yml` defaults to `contents: read` and scopes its
  existing `contents`, `pull-requests`, and `actions` writes to its trusted
  scheduled/manual maintenance job. Its secret use is unchanged.
- `update-submodules.yml` resolves and validates the official remote SHA in
  `contents: read` jobs. A separate publisher revalidates the SHA, checks out
  no submodule, stages only the gitlink with `git update-index`, and has
  `contents: write` plus `pull-requests: write` only for publishing.
- A standard-library contract test and paired fixtures enforce the boundary.
  `actionlint` parses the fixtures with ShellCheck integration; zizmor must
  accept the safe fixture and reject the unsafe fixture.

## Security impact

The update-submodules publisher no longer shares a job or workspace with
remote submodule execution. It accepts a job output only after format
validation and an exact `git ls-remote` comparison with the official branch.
A failed read-only `make quick-check` now prevents PR publication. No
`pull_request_target`, named secret, persistent credential, release/deployment
permission, `id-token`, `attestations`, `checks`, `issues`, or `packages`
write permission is added.

## Changed files

- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/cleanup-artifacts.yml`
- `.github/workflows/test-full-smoke-sequential.yml`
- `.github/workflows/update-actions-versions.yml`
- `.github/workflows/update-submodules.yml`
- `ci/fixtures/workflow-permission-contract/safe.yml`
- `ci/fixtures/workflow-permission-contract/unsafe.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260718-harden-workflow-permissions.md`
- `reports/audits/change-records/CR-20260718-harden-workflow-permissions.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result at the current local change set |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_ci_security_workflows` | passed: 13 focused tests. |
| `make check-ci-security-contract` | passed: 13 tests and three checksum-lock validation checks. |
| Checksum-verified `actionlint -shellcheck=/usr/bin/shellcheck` over workflows and fixtures | passed. |
| Checksum-verified `zizmor --offline .github/workflows` | passed: no findings; 70 configured suppressions reported. |
| Existing and new safe/unsafe zizmor fixtures | passed: safe fixtures accepted; unsafe fixtures rejected with exit code `14`. |
| Checksum-verified `gitleaks git --staged --redact=100 --no-banner` | passed: no leaks in the 12 staged task files. |
| `make check-bilingual-docs` | blocked: the worktree lacks existing Framework documentation-link targets; the checker reports those pre-existing missing targets before completion. |
| `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile tests/test_ci_security_workflows.py` | blocked: `py_compile` attempts to create `tests/__pycache__`, which is read-only in this worktree. The bytecode-disabled unit suite passed. |
| `git diff --check` | passed at the current local change set. |

## Runtime evidence

Not applicable. This change modifies GitHub Actions configuration and static
contracts only; it establishes no connector, protocol, CRS, Framework, MRTS,
or host-runtime evidence.

## Checks not run and rationale

OSV, Scorecard, CodeQL/SARIF upload, GitHub secret scanning, and fork-runtime
behavior are asserted only from the focused pull request's current exact head;
they are not claimed by this static Change Record. `make check-doc-links` is
not run because it invokes Framework validation outside the Parent-only scope.
No connector build, runtime, protocol, sanitizer, CRS, Framework, or MRTS
check applies to this workflow-only change.

## Known limitations

The external Actions default remains `write`; explicit workflow defaults cover
the current workflows but cannot protect a future workflow that omits one.
Changing the setting needs separate administrator authorization. The trusted
`update-actions-versions.yml` maintenance job still needs its existing
`SUBMODULE_UPDATE_TOKEN` for module publishing; this change does not alter or
expose it.

## Remaining risks

Static contracts cannot prove GitHub's runtime fork-token policy or the
behavior of a future remote submodule commit. The publisher revalidates and
does not execute the selected commit; remaining runner/action risk needs exact
PR checks and ongoing review. No risk acceptance is recorded.

## Final diff and review status

Local implementation, final staged diff review, and redacted staged Gitleaks
are complete. The bilingual checker is blocked by pre-existing missing
Framework targets in this worktree. Delivery evidence is deliberately bounded
to the focused PR's current head because any follow-up commit invalidates older
results; consult that PR and `FND-PARENT-0023` for the current delivery state.
No merge is authorized or performed.
