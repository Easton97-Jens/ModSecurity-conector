# Change Record: Read-only Update-submodules runtime-path validation repair

**Language:** English | [Deutsch](CR-20260723-update-submodules-runtime-path-validation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-update-submodules-runtime-path-validation |
| Date (UTC) | 2026-07-23 |
| Base revision | 95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3 |
| Boundary | Parent `Update submodules` read-only validator, its Parent runtime-path-policy checker and test coverage, this English/German Change Record pair, and both Change-Record indexes. Framework source, MRTS, the Parent Framework gitlink, workflow permissions, action pins, dependency locks, resolver ordering, and publisher behavior remain unchanged. |
| Finding linkage | FND-PARENT-0050: confirmed Parent CI failure caused by an obsolete self-test expectation. Its complete English/German/JSON canonical-import package is retained in task-owned evidence; the local canonical `.codex/findings` import is `blocked_permissions` because that mount is read-only. Related historical context: FND-PARENT-0045, FND-PARENT-0048, and FND-PARENT-0049. |
| Delivery status | Draft Parent [PR #93](https://github.com/Easton97-Jens/ModSecurity-conector/pull/93) was created from `agent/update-submodules-run19-remediation` after commits `b4eb4733706cbc555e6bb5be26492ec2058e0ec2` and `4cb226071ce3f42f5bff803a6e99ab748a2a7aef`. This Change-Record amendment is a normal follow-up commit; its exact final head is retained in the PR/task evidence rather than creating a self-referential commit loop. No exact-head CI, review, SonarQube Cloud result, merge, or resulting-master workflow result is claimed yet. The current prompt authorizes one normal Parent PR-only repair integration and its resulting-master validation only. |

## Motivation and problem statement

GitHub Actions `Update submodules` run #19 / run
[29991272761](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29991272761)
reached Parent `master` `95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3` and
resolved Framework candidate `935cf14c676a24672be5c336e92cd13457cc35c8`.
The hash-locked PyYAML validation prerequisite installed successfully, but the
read-only validator failed in `make quick-check` because the Parent shell
self-test required `assert_safe_runtime_path` to accept `/src`.

The candidate Framework correctly classifies source-checkout roots as
non-system/read-only paths rather than mutable runtime destinations. The Parent
checker conflated those two properties, so it rejected a stricter, safer
Framework candidate before the narrow publisher could run. The publisher
correctly skipped after validation failed.

## Acceptance criteria

- The checker continues to prove source roots are not system paths while no
  longer requiring them to be accepted as writable runtime paths.
- A verified runtime/cache descendant remains the positive
  `assert_safe_runtime_path` control.
- The regression fails under the former behavior by simulating a Framework
  implementation that rejects source roots as runtime-write paths.
- Resolver/validator read-only permissions, validation ordering, dependency
  locks, action pins, candidate scope, and narrow publisher isolation remain
  unchanged.
- Exact-head PR checks, review/conversation status, SonarQube Cloud when
  configured, repository-established PR-only squash merge, and a new resulting-master `Update submodules`
  run are observed before this repair is reported complete.

## Implementation decision and rationale

`check_shell_policy` now makes its positive shell assertion only for the
verified cache/runtime control. It retains separate non-system assertions for
`/src`, `/src/ModSecurity-conector-build`, the Parent checkout, and the Parent
build path. A source location may be non-system and read-only without being a
permitted mutable runtime root.

The regression uses a candidate-shell test double that rejects every source
root passed to `assert_safe_runtime_path` but accepts the verified cache path.
It asserts the checker never invokes the runtime-write predicate for source
locations. No Framework implementation, gitlink, or MRTS content is changed.

## Changed files

- `ci/checks/security/check-runtime-path-policy.py`: retain source-path
  non-system classification but remove the obsolete positive runtime-write
  expectation for source roots.
- `tests/test_runtime_path_policy.py`: add the source-root-rejection regression
  and retain the positive verified-cache control.
- This English/German Change Record pair and both Change-Record indexes.

No workflow file, Framework source, MRTS content, Parent gitlink, action pin,
workflow permission, secret, dependency lock, or publishing code is changed.

## Commands executed

- Hosted diagnosis: run `29991272761` failed at
  `check-runtime-path-policy` with `test_path is not under an allowed
  runtime/cache root: /src`; the resolver completed, the read-only validator
  reached `make quick-check`, and the publisher was skipped.
- Passed: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp .venv/bin/python -m unittest -v tests.test_runtime_path_policy` — 6 tests, including the new source-root-rejection regression.
- Passed: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp RUNNER_TEMP=<task-run>/tmp make check-runtime-path-policy` — `check-runtime-path-policy: PASS`.
- Passed: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp RUNNER_TEMP=<task-run>/tmp make check-ci-security-contract` — 16 tests; the resolver → read-only validator → narrow publisher contract remained covered.
- Blocked environment: the selected external-root `make quick-check` advanced
  through shell syntax and 66 normalization/component tests but stopped at the
  existing local Apache/APXS provisioning boundary. The Framework helper found
  unmanaged shared-cache entries and could not produce `apxs`/`apxs2`; the
  target exited 2 through `check-apache-c17-lint`. This is not a failure of the
  modified Python checker or regression, does not justify disabling the
  runtime-component control, and is superseded for acceptance by the required
  hosted resulting-master workflow.

## Security impact

This change narrows a test assumption; it does not broaden any accepted
runtime path. Source roots are explicitly no longer treated as mutable runtime
destinations. The positive cache/runtime control remains, so a Framework
candidate cannot pass by rejecting all paths. The resolver continues to validate
the official candidate SHA, candidate code stays in the `contents: read`
validator, and the separately gated publisher remains the only write-capable
path. No permissions, tokens, secrets, action pins, dependency acquisition, or
publisher gate is weakened.

## Runtime evidence

Not applicable. This is a static Parent validator/self-test repair. It makes no
connector, HTTP, HTTP/2, HTTP/3, or runtime-success claim. The only required
hosted behavior evidence is the resulting-master `Update submodules` workflow
outcome.

## Checks not run and rationale

- A local full `make quick-check` completion is not available in this checkout
  because its Apache/APXS dependency provisioner fails closed on unmanaged
  cache entries. The failure was retained as environment evidence; no cache,
  Framework, or control was modified to bypass it.
- No Framework change, Framework PR, Framework merge, Framework gitlink
  update, MRTS change, or MRTS test was run; all are out of scope.
- Exact-head GitHub checks, SonarQube Cloud, review, PR-only squash merge, and the
  resulting-master workflow are pending at this pre-delivery snapshot and must
  be recorded from observed GitHub evidence only.

## Known limitations

The local canonical finding registry cannot currently accept FND-PARENT-0050
because its `.codex` mount is read-only. The complete bilingual/JSON import
package is retained in task-owned evidence and must be imported when the
registry is writable. This does not alter the versioned Parent fix or create a
claim that the canonical finding/index/backlog/roadmap has been updated.

## Remaining risks

Until the exact task PR head is reviewed and its required checks pass, and
until a fresh `Update submodules` run succeeds on resulting `master`, automated
Framework-candidate publication remains correctly blocked. The existing
fail-closed validation and narrow publisher isolation prevent publication on a
validation failure. No risk is accepted.

## Final diff and review status

Pre-delivery review finds the intended source diff limited to the Parent
runtime-path self-test and its regression. `git diff --check`, bilingual
documentation validation, documentation-link validation, selected Python
compilation, and the focused security diff review completed successfully. The
security review found no reportable regression: source roots are not newly
write-safe, the verified cache control remains, and the read-only
resolver/validator versus narrow publisher topology is unchanged. Exact-head
CI, SonarQube Cloud, review, merge, and resulting-master workflow dispositions
remain pending and will be reconciled with observed evidence before completion.
