# FND-FRAMEWORK-0024 — Framework PR #30 Change Record pair violates the current canonical heading contract

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0024 |
| Category | ci_failure |
| Repository / ownership | framework / framework |
| Priority / severity | P1 / not_applicable |
| Confidence / status | reproduced / fixed |
| Feasibility | feasible_now |
| Release blocker | false |
| Security relevant | false |

## Summary, observation, expected behavior, and impact

After the normal Framework-master update for PR #30, the current CI-security
Change Record contract rejected both existing records:
reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.md
and its .de.md companion. Each record already has the canonical thirteen
level-2 sections, but then adds four historical follow-up narratives as more
level-2 sections. The current contract requires the canonical section sequence
exactly.

make test-ci-security-contract ran 69 tests: 68 passed and
ChangeRecordContractTest.test_checked_in_change_records_pass failed. The exact
diagnostic was: English Change Record headings do not match the template; German
Change Record headings do not match the template.

Both records must retain every historical narrative, reciprocal language link,
and Change ID while exposing exactly the canonical thirteen level-2 headings.
The repair must not change the checker, test, template, or CI-security
enforcement. This was a reproducible required CI failure, not a validated
vulnerability.

At refreshed exact PR head `a448d056ef98e745d8551c198b2e56d33fe38194`, the
unchanged CI-security suite passed all 69 tests, documentation checks passed,
and every terminal non-skipped hosted check succeeded. The finding is therefore
`fixed` on the verified PR head without a checker, template, traceability
control, or exception change. It is not `verified` on master because the
current task does not authorize a Framework-master merge.

## Scope, preconditions, reproduction, and evidence

The affected files are the paired PR #30 Change Records. The relevant contract
is ci/checks/documentation/check-change-records.py and its test is
tests/ci_security/test_change_record_contract.py. Preconditions are current
Framework master 9a729226d2e040d07d7e7a4acebf201faf06ab37 in the task worktree
and the existing records' four extra level-2 history headings.

~~~
rtk proxy env <task-owned roots> make -C <Framework PR30 worktree> test-ci-security-contract
rtk rg -n '^## ' reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.md reports/audits/change-records/20260719-01-remediate-framework-sonarcloud-quality-gate.de.md
rtk sed -n '1,160p' ci/checks/documentation/check-change-records.py
~~~

Retained evidence:
- Run: 20260719T230508Z-framework-pr30-duplication-master-37469460
- Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-merge-change-record-contract-failure.md
- SHA-256: 1b0055525f231fc5584fff88b49e357ffbb92228f77a56ae0736a78ee1e321da
- Working directory: /root/git/ModSecurity-conector
- Exit code: 2
- Observed: 2026-07-19T23:35:54Z
- Retention: retained

- Run: 20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef
- Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef/evidence/pr30-refresh-summary.md
- SHA-256: 04a0b6891f92b0485c298bb939e57fb464cea2bd5872eb74c65d97f6450f4255
- Command: Task-root CI-security and documentation checks plus GitHub exact-head check-run/review readback
- Working directory: /root/git/ModSecurity-conector
- Exit code: 0
- Observed: 2026-07-20T06:43:42Z
- Retention: retained
- Result: exact PR #30 head `a448d056ef98e745d8551c198b2e56d33fe38194`
  passed the unchanged 69-test CI-security suite, documentation checks, and all
  terminal non-skipped hosted checks.

## Root cause and proposed remediation

The historical PR #30 pair predates the strict current Change Record checker. It
placed later historical updates at level 2 rather than as level-3 subsections
under the required final review section.

Demote only these four extra history headings in each language from level 2 to
level 3. Preserve all text, language links, Change IDs, the canonical thirteen
headings, and English/German parity. Do not alter the checker or any control.

## Acceptance criteria and validation plan

- [complete] Both records expose exactly the canonical thirteen level-2 headings.
- [complete] The four historical updates remain present as level-3 subsections.
- [complete] Reciprocal English/German links and matching Change IDs remain valid.
- [complete] The direct Change Record contract and the unchanged 69-test CI-security suite pass.
- [complete] The refreshed PR head passed all terminal non-skipped hosted checks.
- [pending authorization] Framework-master integration and resulting-master revalidation are not authorized by the current task.

Inspect headings before and after the repair; run the direct contract and the
complete CI-security suite with task-owned roots; review EN/DE parity and the
scoped diff; then require exact-head hosted CI after the normal push.

## Regression and legitimate-control tests

Regression tests are:
- tests/ci_security/test_change_record_contract.py
- make test-ci-security-contract

The unchanged checker must continue to reject noncanonical or missing headings,
and accept the repaired canonical pair with valid reciprocal links and Change
IDs.

## Dependencies, boundaries, related findings, and residual risk

Dependencies are current Framework-master Change Record controls, the isolated
PR #30 worktree, and exact-head hosted CI after the normal push. There are no
current blockers or duplicate records.

This is distinct from FND-FRAMEWORK-0023, which owns PR #30 Sonar duplication
and source/test refactoring. This finding owns the independent Change Record
format failure exposed by the normal master update.

The original failure no longer reproduces on the exact PR head, so this finding
is fixed. The only delivery gap is the deliberately absent Framework-master
integration and resulting-master revalidation; neither is implied by this
finding or authorized by the current user. No checker, traceability control,
Parent gitlink, or MRTS state is changed or waived.

## History

- 2026-07-19T23:35:54Z —
  change_record_contract_failure_confirmed_after_normal_master_update: current
  master CI-security ran 69 tests and only the paired PR #30 Change Record
  heading contract failed. The planned repair is a level-2-to-level-3 heading
  adjustment in both records, with no checker or control change.
- 2026-07-20T06:43:42Z — exact_refreshed_pr_head_passes_unchanged_contract:
  exact PR #30 head `a448d056ef98e745d8551c198b2e56d33fe38194` passed the
  unchanged 69-test CI-security suite, documentation checks, and every terminal
  non-skipped hosted check. The finding is fixed on the verified PR head;
  master integration remains unauthorized.
