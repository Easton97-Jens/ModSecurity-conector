# Change Record: Framework gitlink update to 935cf14

**Language:** English | [Deutsch](CR-20260723-framework-gitlink-935cf14.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-framework-gitlink-935cf14 |
| Date (UTC) | 2026-07-23 |
| Base revision | 91c933e19bb3c87d767c4dad9eb8a1b160d42051 |
| Boundary | Parent Framework gitlink, this English/German Change Record pair, and both Parent Change-Record indexes. Framework source, Framework delivery, MRTS, Parent connector source, workflow permissions, action pins, dependency locks, resolver behavior, and publisher behavior are unchanged. |
| Delivery status | Parent PR #94 is the expressly selected open PR. Its original automated commit 8db42f177dcc28a7cb9fb78c93e46b564aa16410 advances the gitlink; this record is a task-owned compliance follow-up on that PR. The final exact PR head, reviews, checks, SonarQube Cloud result, merge, resulting-master SHA, and resulting-master workflows are retained in observed PR/task evidence rather than claimed before they exist. |

## Motivation and problem statement

The Parent Update submodules workflow resolved the official Framework master
revision 935cf14c676a24672be5c336e92cd13457cc35c8 while the Parent recorded
784977615acfc55567e37b863309abc4a38ac877. Hosted run 29996299306 completed
its resolver, read-only candidate validator, and narrow PR publisher
successfully, and opened PR #94 with the resulting one-file Parent gitlink
diff.

The Parent gitlink is a separate delivery boundary. Its integration must retain
Parent-side scope, security, validation, and limitation facts even though the
Framework revision was already merged in the Framework repository. The original
automated PR had no Parent Change Record or bilingual PR description/record
link, so this follow-up supplies the required Parent traceability without
changing Framework content or delivery state.

## Acceptance criteria

- The Parent gitlink changes only from
  784977615acfc55567e37b863309abc4a38ac877 to
  935cf14c676a24672be5c336e92cd13457cc35c8.
- This English/German Change Record pair and both indexes describe equivalent,
  observed Parent delivery facts.
- PR #94 receives equivalent English/German description sections and this
  Change Record link before final verification.
- The existing read-only validation/publisher separation, workflow
  permissions, action pins, dependency locks, Framework source, and MRTS
  remain unchanged.
- A fresh exact-head PR check, review/conversation, SonarQube Cloud, protected
  squash-merge, and resulting-master workflow cycle is observed before the
  Parent update is reported complete.

## Implementation decision and rationale

The Parent records the exact Framework commit as a gitlink rather than copying
or modifying Framework files. 935cf14c676a24672be5c336e92cd13457cc35c8 is the
observed Framework origin/master merge commit. Its Framework-owned source
changes and Framework Change Records remain Framework evidence; this Parent
record describes only the Parent pointer and Parent delivery obligations.

The compliance follow-up adds no executable source, workflow, action, package,
or permission change. It corrects the Parent traceability gap and makes the PR
description bilingual, then deliberately restarts the exact-head verification
cycle. No historical green result is treated as evidence for the changed PR
head.

## Changed files

- modules/ModSecurity-test-Framework: Parent gitlink from
  784977615acfc55567e37b863309abc4a38ac877 to
  935cf14c676a24672be5c336e92cd13457cc35c8.
- reports/audits/change-records/CR-20260723-framework-gitlink-935cf14.md and
  .de.md: this Parent delivery record pair.
- reports/audits/change-records/README.md and .de.md: matching index entries.

No Framework source, Framework gitlink inside Framework, MRTS content, Parent
connector source, test, workflow, permission, action pin, dependency, or
generated runtime report is changed.

## Commands executed

- Passed: rtk proxy git diff --no-ext-diff
  91c933e19bb3c87d767c4dad9eb8a1b160d42051
  8db42f177dcc28a7cb9fb78c93e46b564aa16410 --
  modules/ModSecurity-test-Framework. The original PR diff contains only the
  expected gitlink update.
- Passed: rtk proxy gh run view 29996299306 --repo
  Easton97-Jens/ModSecurity-conector. The Update submodules resolver,
  read-only validator including make quick-check, and PR publisher all
  completed successfully for Parent
  91c933e19bb3c87d767c4dad9eb8a1b160d42051.
- Passed: rtk proxy git -C modules/ModSecurity-test-Framework branch --remotes
  --contains 935cf14c676a24672be5c336e92cd13457cc35c8. The selected revision is
  contained by observed Framework origin/master.
- Passed: rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp
  RUNNER_TEMP=<task-run>/tmp make check-bilingual-docs. The bilingual
  documentation checker reported bilingual docs ok after the PR-pinned
  Framework submodule was initialized non-recursively in the disposable
  worktree.
- Passed: rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp
  RUNNER_TEMP=<task-run>/tmp make check-doc-links. Parent repository path
  references and Framework documentation links both passed.
- Passed: rtk proxy git diff --cached --check. No whitespace error was reported
  for the final staged follow-up diff.
- Passed: rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-run>/tmp
  RUNNER_TEMP=<task-run>/tmp make check-ci-security-contract. All 16 workflow
  security-contract tests passed, including the read-only Update submodules
  validator versus narrow publisher separation.
- Passed: focused security review of the exact gitlink/documentation candidate
  found no validated high- or critical-severity issue. It confirms that
  read-only describes the validator GitHub-token/API permission boundary, not
  an assertion that its ephemeral runner workspace cannot write temporary
  files.
- Pending at this snapshot: all fresh exact-head hosted controls for the
  compliance follow-up. They are recorded only after execution against its
  resulting head.

## Security impact

This is a supply-chain boundary update: the Parent advances a pinned gitlink to
one exact full Framework SHA that the resolver revalidated against the official
Framework master before publication. Candidate code was validated in the
workflow's contents: read validator; the narrow publisher ran only after that
success. This record does not relax that separation or introduce a new
download, permission, secret, path, archive, action, or runtime-data handling
path.

Read-only in this record means the validator's GitHub token/API permission
boundary. It does not claim that make quick-check is incapable of creating
temporary files in the ephemeral runner workspace.

The Framework revision has broad Framework-owned CI/tooling changes, but this
Parent record makes no unverified claim about their delivery or behavior. Fresh
Parent protected-branch checks and SonarQube Cloud analysis remain required for
the final PR head.

## Runtime evidence

No runtime evidence was collected or claimed. The isolated read-only candidate
validator and Parent documentation checks are CI/static validation, not
connector, HTTP, HTTP/2, HTTP/3, or production runtime evidence.

## Known limitations

The Parent does not independently reproduce every Framework-internal validation
of 935cf14c676a24672be5c336e92cd13457cc35c8; Framework source and delivery
remain separate ownership. This Parent integration is limited to the exact
recorded gitlink, its isolated candidate validation, and its fresh Parent
protected-branch evidence.

## Remaining risks

Until the task-owned follow-up head has passed all protected-branch checks,
SonarQube Cloud, review/conversation inspection, and resulting-master workflows,
PR #94 is not eligible for merge. No branch-protection bypass, CI weakening,
Framework merge, MRTS action, or risk acceptance is used.

## Checks not run and rationale

- No Parent connector/runtime matrix or full local make quick-check run is
  claimed for this documentation/gitlink follow-up. The candidate-specific
  make quick-check already ran in the isolated read-only hosted validator;
  final eligibility still requires the new exact-head Parent workflows.
- No Framework source test, Framework branch/PR/merge, Framework checkout
  change, MRTS inspection beyond the existing read-only boundary, or MRTS test
  was run. None is required to add the Parent traceability record, and MRTS is
  strictly read-only.

## Final diff and review status

Pre-delivery review limits this PR to the exact Parent gitlink and the required
Parent traceability/documentation follow-up. Whitespace, bilingual
documentation, and documentation-link validation passed in the isolated PR
worktree. The local CI security contract passed all 16 tests, and the focused
security review found no validated high/critical issue. The previous automated head had a passing SonarQube Cloud Quality
Gate with zero new issues and zero security hotspots, but that result is
intentionally not treated as evidence for this follow-up head. Current security
diff, review, exact-head CI, SonarQube Cloud, merge, and resulting-master
dispositions are pending and must be reconciled with observed results before
completion.
