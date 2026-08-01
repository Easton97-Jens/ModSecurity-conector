# FND-FRAMEWORK-0021 — External Python-version change breaks Framework hash-locked CI dependency contract

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0021` |
| Category | `ci_failure` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `confirmed` / `verified` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary, observation, and impact

After the user-authorized PR #27 merge, external Framework-master commits
beginning at `6cfe9cdb97d807ec265aec45da3d13fa4f2c28a7` and continuing through
`4dee26fcff988fd408bc7df577de772373c4b765` changed twelve reviewed
`actions/setup-python` values across eight workflows from `3.12.13` to `3.13`.
They did not update
`requirements-ci.lock`, whose header and sole PyYAML entry explicitly bind the
CI contract to CPython `3.12.13`, the CP312 wheel, and SHA-256
`ba1cc08a7ccde2d2ec775841541641e4548226580ab850948cbfda66a1befcdc`.

On exact later master `4dee26fcff988fd408bc7df577de772373c4b765`, the hosted
runner uses Python `3.13.14`, downloads PyYAML 6.0.3's CP313 wheel, and
correctly rejects its SHA-256
`0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6` as not
matching the CP312-only lock. `actionlint-and-contract`, `zizmor`, and
`scaffold-lint`, and `current-revision-advisory` all fail at **Install
hash-locked CI dependency**, before their intended controls execute.

This is a later external master regression, not a defect in PR #27's merged
tree. The strict hash control is working fail closed. It is a P1 release
blocker because four mandatory controls do not run, but it is not grounds to
delete `--require-hashes`, trust the CP313 wheel under the CP312 digest, or
weaken any workflow or security check.

## Scope, reproduction, and evidence

Affected files are the eight externally changed workflow files
`.github/workflows/ci-security-workflow-lint.yml`, `.github/workflows/lint.yml`,
`.github/workflows/check-action-versions.yml`,
`.github/workflows/check-common-versions.yml`, `.github/workflows/ci-security-osv.yml`,
`.github/workflows/ci-security-quality.yml`,
`.github/workflows/ci-security-scorecard.yml`,
`.github/workflows/ci-security-secrets.yml`, and `requirements-ci.lock`.
Affected controls are the `actions/setup-python` `python-version` values and
the hash-locked install step.

Read-only reproductions:

```text
rtk git -C /var/tmp/codex/worktrees/framework-ci-security show --format= --unified=20 6cfe9cdb97d807ec265aec45da3d13fa4f2c28a7
rtk git -C /var/tmp/codex/worktrees/framework-ci-security show --format= --unified=20 8572da580e11bc3c62f6ef559152f49b30650056
rtk git -C /var/tmp/codex/worktrees/framework-ci-security show 8572da580e11bc3c62f6ef559152f49b30650056:requirements-ci.lock
rtk gh run view 29702454427 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
rtk gh run view 29702454412 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
```

The GitHub evidence is external and was intentionally not copied into a local
artifact, so its `sha256` is `null` rather than invented. The failed job pages
are [CI security workflow lint `29702454427`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29702454427)
and [lint `29702454412`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29702454412).
The later current snapshot also retains it at exact master `4dee26...` in
`actionlint-and-contract`, `zizmor`, `scaffold-lint`, and
`current-revision-advisory`.

## Root cause and expected behavior

The later workflow edits treated `3.13` as a drop-in replacement for the
explicitly reviewed `3.12.13` interpreter across eight workflows without updating the
interpreter-specific PyYAML wheel lock metadata and validating every consumer.
PyPI correctly provides a different CP313 wheel, whose digest cannot match the
CP312 lock entry.

Every interpreter version and wheel hash must be one reviewed, internally
consistent contract. All three controls must install their intended reviewed
artifact and then run. A mismatched interpreter/artifact pair must continue to
be rejected by `pip --require-hashes`.

## Remediation, acceptance, and validation

The current user authorized a normal Framework master-integration PR and the
task selected the coherent CPython `3.13.14` path: all twelve active
`setup-python` values use exact `3.13.14` with `check-latest: false`, and the
lock header and sole PyYAML entry use the reviewed CP313 artifact hash
`0f29edc409a6392443abf94b9cf89ce99889a1dd5376d94316ae5145dfedd5d6`.

It preserves `--require-hashes`, security-tooling review, workflow
permissions, Parent boundaries, and the MRTS read-only boundary. It does not
direct-push `master`, suppress the failure, or trust a mismatched artifact.

- [verified] Framework PR #33 made the interpreter and lock contract
  consistent without weakening `--require-hashes`.
- [verified] Exact PR head `e94029f5b893ef6a8efa118d21698426a43c82dd` passed
  the applicable Actions, CodeQL, and SonarQube Cloud Quality Gate with no
  review or review thread.
- [verified] Exact resulting master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37` reran and passed
  `actionlint-and-contract`, `zizmor`, `scaffold-lint`, and
  `current-revision-advisory` after the intended artifact installed.
- [verified] The CP313 lock resolves under `--require-hashes`, while the
  existing negative contract suite continues to reject a deliberate
  provisioning mismatch.

## Dependencies, blockers, related findings, residual risk, and history

The completed remediation depended on the reviewed interpreter/PyYAML artifact
decision, GitHub-hosted Linux wheel availability, exact-head validation, and
resulting-master verification. It was delivered through a normal exact-head PR
merge; it did not authorize or perform a direct push, GitHub setting change,
Parent update, or MRTS mutation.

`FND-FRAMEWORK-0017` and `FND-FRAMEWORK-0020` remain distinct prior PR #27
controls. Their original source evidence is not invalidated; their broad
current-master verification is simply not a substitute for the later failed
controls here. This finding is not a duplicate of either record.

Residual risk: no defect from this finding remains on Framework master
`9a729226d2e040d07d7e7a4acebf201faf06ab37`. The strict lock stays fail closed,
and hosted CPython 3.13.14 controls now pass. The independent master SonarQube
Cloud backlog is tracked separately as `FND-SONAR-0002` and is not attributed
to this repair.

- `2026-07-19T20:32:09Z`: `external_post_merge_python_lock_regression_validated`
  — external commits changed reviewed `3.12.13` workflow values to `3.13`
  while retaining the CP312-only lock. Exact master `8572da...` failed all
  three named controls at the strict install. No remediation was performed or
  authorized in this task.
- `2026-07-19T20:47:56Z`: `external_master_ci_regression_reconfirmed_and_expanded`
  — further external commits advanced master to `4dee26...`, changed twelve
  reviewed values across eight workflows, and reproduced the same strict
  mismatch in `actionlint-and-contract`, `zizmor`, `scaffold-lint`, and
  `current-revision-advisory`. This task did not author, merge, or remediate
  those changes.
- `2026-07-19T21:31:45Z`: `authorized_python_313_14_lock_remediation_started`
  — the current user authorized normal Framework integration. The task bound
  all twelve active workflow uses to exact `3.13.14` with `check-latest: false`,
  updated the lock to the verified CP313 PyYAML digest, and passed the focused
  local CI-security matrix and target-wheel `--require-hashes` resolution.
  Exact-head and resulting-master hosted evidence remain pending.
- `2026-07-19T22:18:45Z`: `verified_after_exact_pr33_merge_and_master_reproduction`
  — Framework PR #33 passed its exact-head Actions and SonarQube Cloud Quality
  Gate without reviews or threads, then merged normally at expected head
  `e94029f5b893ef6a8efa118d21698426a43c82dd` as master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37`. The original four affected
  controls all passed; the CP313-versus-CP312 mismatch no longer reproduces.
  No hash, permission, Parent, or MRTS control was weakened.
