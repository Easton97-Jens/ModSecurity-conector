# FND-FRAMEWORK-0022 — Framework action lock lags active immutable upload-artifact pin

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0022` |
| Category | `ci_failure` |
| Repository / ownership | `framework` / `framework` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `confirmed` / `verified` |
| Feasibility | `feasible_now` |
| Release blocker | `false` |
| Security relevant | `true` |

## Summary, observation, and impact

The current Framework source uses immutable
`actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` with
release comment `v7.0.1` in three security-workflow steps. Its
repository-owned `ci/tooling/security-tools.lock.yml` still recorded the
earlier release `v5.0.0` and commit
`330a01c490aca151604b8cf639adc76d48f6c5d4`.

External Dependabot commit `61fec7cb40e0b940760c079f0e8da3f977bc9ae8`
changed the workflow uses without synchronizing the custom provenance lock.
The static CI-security contract correctly rejected the mismatch. This is a P1
release blocker because the immutable-action supply-chain contract cannot
truthfully validate the current workflows while its own inventory is stale.

It is not permission or workflow-runtime scope: no permission, artifact
retention, workflow reference, mutable tag, or checker is relaxed. The current
authorized repair updates only the stale lock record to the already active,
officially verified v7.0.1 immutable commit.

## Scope, reproduction, and evidence

Affected paths are `.github/workflows/ci-security-osv.yml`,
`.github/workflows/ci-security-scorecard.yml`, and
`ci/tooling/security-tools.lock.yml`.

```text
rtk git show --format='%H%n%s' --no-patch 61fec7cb40e0b940760c079f0e8da3f977bc9ae8
rtk gh api repos/actions/upload-artifact/git/ref/tags/v7.0.1 --jq .object.sha
rtk rg -n 'actions/upload-artifact|version: v5.0.0|330a01c490aca151604b8cf639adc76d48f6c5d4' .github/workflows ci/tooling/security-tools.lock.yml
```

The official GitHub tag API resolves `v7.0.1` to
`043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`. After the focused lock repair,
the task's local `test-ci-security-contract`, immutable workflow-pin, and
workflow-permission matrix passed (69 CI-security tests plus the 21-test pin
suite). External API and commit data remain external evidence; their hashes
are intentionally not invented.

## Root cause, expected behavior, and remediation

The Dependabot workflow update did not include the repository-specific
security-tools provenance lock. Every external action reference must match a
complete lock record: exact release, exact full commit, upstream release URL,
licence, purpose, platform, and update procedure. The contract must continue
to reject stale, mutable, short, malformed, or mismatched references.

The current task updates exactly the `actions/upload-artifact` lock record to
`v7.0.1`, the verified immutable commit, and its matching upstream release
URL. It preserves all workflow references, action-pin enforcement,
permissions, retention policy, and the established update procedure.

- [verified] The reviewed lock record matches `v7.0.1` and its exact SHA.
- [verified] The focused CI-security, action-pin, and permission checks accept
  the repaired record and still exercise rejection controls.
- [verified] Exact PR head `e94029f5b893ef6a8efa118d21698426a43c82dd` and
  resulting master `9a729226d2e040d07d7e7a4acebf201faf06ab37` passed the
  applicable hosted CI-security and immutable-action controls.

## Boundaries, related findings, and residual risk

This finding is distinct from `FND-FRAMEWORK-0021`, which owns the CPython ABI
and PyYAML wheel hash mismatch, and from `FND-FRAMEWORK-0019`, which owns
flow-style YAML contract incompatibility. It is related to the prior immutable
action-pin hardening in `FND-FRAMEWORK-0003`, but the regression is a stale
custom provenance record rather than a mutable action reference.

The local test interpreter is CPython 3.14.4, but exact hosted PR and
resulting-master controls now prove the intended action runtime. The finding is
`verified` on master `9a729226d2e040d07d7e7a4acebf201faf06ab37`; immutable
pins, permissions, retention, and mismatch rejection remain unchanged. The
separate master SonarQube Cloud backlog is `FND-SONAR-0002`. No Parent or MRTS
change was authorized or made.

- `2026-07-19T21:31:45Z`:
  `stale_action_provenance_lock_confirmed_and_remediation_started` — the
  Dependabot-induced workflow/lock drift was confirmed; the v7.0.1 tag identity
  was independently checked, the minimal lock repair was made, and the focused
  local security matrix passed. Hosted validation remains pending.
- `2026-07-19T22:18:45Z`:
  `verified_after_exact_pr33_merge_and_master_contract_controls` — Framework
  PR #33 passed exact-head GitHub Actions and SonarQube Cloud without reviews
  or threads, then merged normally at expected head
  `e94029f5b893ef6a8efa118d21698426a43c82dd` as master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37`. Master
  `actionlint-and-contract` and `zizmor` passed with the synchronized v7.0.1
  lock; permissions, retention, and immutable-pin enforcement were unchanged.
