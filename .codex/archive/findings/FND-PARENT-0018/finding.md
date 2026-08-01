# FND-PARENT-0018 — Partial Dependabot CodeQL Action updates violate immutable-pin and init/analyze consistency

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-PARENT-0018` |
| Category | `ci_security_consistency` |
| Repository / ownership | `parent` / `parent` |
| Priority | `P1` |
| Severity / confidence | `medium` / `confirmed` |
| Status / feasibility | `closed` (archived) / `already_fixed` |
| Outcome / final disposition | `no_change` / `already_fixed_on_current_master` |
| Validated master SHA | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Delivery disposition | `not_applicable`; no product change, commit, push, or pull request is required or occurred |
| Release blocker / security relevant | `false` / `true` |
| Scope | GitHub Actions CI / CodeQL Action v4.37.1 batch |

## Summary

Dependabot PRs #48, #49, and #50 historically updated only one
`github/codeql-action` component while the immutable-action registry remained
at v4.37.0. Their exact heads proved both immutable-pin and CodeQL
configuration/action-version failures. On the selected revision
`c8ca0d92b630c18232b881855c4f5d1482568ea6`, prior commit
`635b8f603f852cff10926cd6f5449e763f6194a4` already atomically pins all ten
workflow references and the registry to v4.37.1 SHA
`7188fc363630916deb702c7fdcf4e481b751f97a`. The current revalidation finds no
remaining defect. The finding outcome is `no_change` and its final disposition
is `already_fixed_on_current_master`.

## Observed and expected behavior

The eleven retained job logs establish that all three original PR heads failed
`test_all_remote_actions_are_immutable_sha_pins` because official SHA
`7188fc363630916deb702c7fdcf4e481b751f97a` was absent from the lock. PR #48
used `init` v4.37.0 with `analyze` v4.37.1; PR #50 proved the inverse. Both
CodeQL jobs reported a configuration/action version mismatch. The current
revision has no mixed scoped reference: every CodeQL Action use and its
registry entry resolve to one official immutable release with existing controls
unchanged.

## Impact

An individual merge would create a known-invalid CI-security configuration.
This is a CI/supply-chain consistency defect; no connector-runtime exploit is
claimed.

## Remediation and validation

The historical replacement updated all ten refs and the matching registry entry
to official v4.37.1 SHA `7188fc363630916deb702c7fdcf4e481b751f97a`. This
revalidation reran the immutable-pin contract, Actionlint with ShellCheck,
offline Zizmor, and safe/unsafe Zizmor controls successfully. PR #52 exact-head
CodeQL, workflow, and SonarQube Cloud checks succeeded; the selected revision's
CodeQL and Actions checks also succeeded. No new source change is required or
made, and delivery is `not_applicable`: no commit, push, or pull request is
required or occurred.

The retained sanitized exact-head log archive is
`evidence/dependabot-failed-job-logs-retained.tar.gz`, SHA-256
`78e1f5213915163acc279e61885451e54a10f1021efb816c66fc694a4b44a8a3`.

## Administrative closure and plan disposition

The lifecycle state is `closed` only after the already-recorded `verified`
state: retained exact original PR #48/#50 evidence, the merged replacement PR
#52, current-master validation, and legitimate controls satisfy the closure
evidence available for this finding. The former worktree plan was reviewed at
SHA-256 `3d6cd95176279b513e1cc7f426a54a7f1feea4c263a84731f493518a0aea0e08`
and is not retained. It contains only operational planning facts already
preserved by the canonical finding record and the retained validation receipt
`/var/tmp/codex/ModSecurity-conector/runs/20260718T080726Z-fnd-parent-0018-4dd4e268/evidence/fnd-parent-0018-no-change-validation.md`
(SHA-256 `728c55f02d52bc394207e81ccb79bbc47ecc89a39ed430b4b86b54f784cd0233`):
source-to-sink proof, both mixed-version directions, current counterevidence,
controls, PR #52/current CI evidence, Sonar separation, and the no-delivery
rationale.

## 2026-07-21 analogous Dependabot Action transaction

The same atomic immutable-pin/lock-membership invariant recurred outside this
finding's historical CodeQL v4.37.1 scope. Dependabot PR #67 updated
`actions/setup-python` to v7.0.0 and PR #68 updated `actions/checkout` to
v7.0.1, but each exact bot head failed the immutable-action contract because
the corresponding official SHA was absent from the reviewed lock. The
task-owned atomic replacements #75 and #76 updated every affected workflow
reference and its one matching lock entry together; both exact heads passed
the six strict protected-branch contexts, SonarQube Cloud with zero new issues
and zero new hotspots, and the review-thread requirement before ordinary
protected squash merges.

Replacement #75 merged as `5c26ffb698a892ffe83b7aa1749a456eae10b956` and
#76 as current master `2ade0d40983b7af21a65b8cd2884866b85626393`. The latter
has 15 successful GitHub Actions workflow runs and 19 successful plus two
expected-skipped terminal check runs. Its sole failing check is the separate
pre-existing `FND-SONAR-0001` Sonar baseline: the same three unreviewed
`python:S5332` hotspots, Security Rating `5`, and hotspot review `0.0%`.
The original Dependabot PRs #67 and #68 were closed unmerged by
`dependabot[bot]`; this task did not close them. No new canonical ID is
allocated because this is the same independently remediable atomic
workflow-pin/lock transaction invariant. This recurrence does not retroactively
alter the historical `no_change` delivery disposition of the original
CodeQL-specific evidence.

## Residual risk and history

GitHub reports the official annotated v4.37.1 tag as `unsigned`; provenance
is limited to the official repository, release, tag target, and full SHA. The
current `master` SonarQube Cloud failure is an identical pre-existing condition
tracked as `FND-SONAR-0001`, not an FND-PARENT-0018 regression.
`FND-SONAR-0001` remains open and `blocked`; this closure does not
disposition or alter it. No risk is accepted.

- `2026-07-17T18:16:59Z`: exact original heads and failures retained and
  classified.
- `2026-07-17T18:45:07Z`: atomic local controls passed; external PR and
  `master` evidence remains pending.
- `2026-07-18T08:17:17Z`: current revision revalidated as `no_change` with
  current source, focused local controls, retained PR #48/#50 mixed-version
  evidence, and exact-SHA GitHub checks. No product change was made.
- `2026-07-18T09:17:25Z`: administratively closed with outcome `no_change`
  and final disposition `already_fixed_on_current_master`; no delivery action
  occurred. The former worktree plan was reviewed and not retained because the
  checksum-verified retained validation receipt is the sufficient canonical
  technical evidence.
- `2026-07-21T08:05:05Z`: an analogous Dependabot action-pin recurrence was
  deduplicated into this atomic immutable-pin/lock-membership finding. Exact
  bot heads #67/#68 lacked their matching reviewed lock entry; task-owned
  replacement PRs #75/#76 passed all strict exact-head contexts, Sonar PR
  gates, and thread controls before protected squash merges to
  `5c26ffb698a892ffe83b7aa1749a456eae10b956` and
  `2ade0d40983b7af21a65b8cd2884866b85626393`. The current master Actions
  evidence is successful; its separate Sonar failure remains
  `FND-SONAR-0001`. The bot closed original PRs #67/#68 unmerged; no task
  closure, bypass, force, Framework, MRTS, gitlink, ruleset, or scanner change
  occurred.
