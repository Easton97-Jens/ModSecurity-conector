# Change Record: manual Framework updater without a fixed structure gate

**Language:** English | [Deutsch](CR-20260930-manual-framework-updater.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-manual-framework-updater |
| Date (UTC) | 2026-09-30 |
| Base revision | `9bc87cbdb600b09c6edd02667a75b117a1f09eea` |
| Related delivery | Parent Draft PR #398; Framework Draft PR #132 |

## Motivation and problem statement

[Updater job 109955091216](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36735191087/job/109955091216) rejected a later Framework candidate solely because its `common.sh` skeleton no longer matched a fixed Parent digest. The user wants the Parent updater to run only when manually dispatched and to accept new Framework structure without that fixed digest gate. The earlier direct-pin revision of PR #398 also exposed a stale ModSecurity nested Gitlink in the Framework; its separate correction is Framework PR #132.

## Acceptance criteria

The Parent updater has only `workflow_dispatch`, never a schedule. A manually started publishing run may validate and propose a new Framework structure without changing an approved digest. Candidate Git-state, official origin/lineage, bounded source-data syntax, Parent NGINX handoff, isolated validation, narrow publisher permissions, and Draft/no-auto-merge behavior remain required. No current Framework candidate is directly pinned by this Parent PR.

## Implementation decision and rationale

Remove the fixed-digest comparison from both active Parent checks while retaining bounded UTF-8 reads, source-data parsing and the independent NGINX/Parent contracts. Reject known indirect shell-target writes as well as existing `eval` and direct assignment mutations. Remove the weekly trigger and require `workflow_dispatch` in the resolver gate and its regression contract. Restore the Parent gitlink and projections to the base revision so the user can run the updater after Framework PR #132 is separately reviewed and merged.

## Changed files

- `.github/workflows/update-submodules.yml`
- `ci/tools/verify-framework-candidate-contract.py`
- `ci/tools/check-reviewed-version-handoff.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_update_submodules_local_git.py`
- `tests/test_verify_framework_candidate_contract.py`
- `tests/test_reviewed_version_handoff.py`
- `docs/reviewed-version-upgrades.md`
- `docs/reviewed-version-upgrades.de.md`
- `reports/audits/change-records/CR-20260930-manual-framework-updater.md`
- `reports/audits/change-records/CR-20260930-manual-framework-updater.de.md`

## Commands executed

The workflow, two active digest checks, relevant tests, Parent/Framework revisions and the failed PR jobs were inspected through the GitHub connection. The official ModSecurity v3.0.17 Git tree independently confirmed the Framework Gitlink mismatch. No local repository command or test is claimed as passed. Current-head hosted checks remain required after the follow-up commit.

## Security impact

This intentionally removes the fixed executable-shell-structure approval gate at the user's explicit direction. Manual dispatch does not make arbitrary Framework shell changes safe; static checks cannot prove all indirect mutations absent. The candidate still runs in the read-only validation sandbox and the updater only creates a Draft PR. Its complete diff, provenance, CI, and runtime evidence require human review before merge. Other provenance, NGINX, token, path, permission, and no-auto-merge controls are not relaxed.

## Runtime evidence

No new connector runtime pass is established. The prior Parent PR head failed NGINX provisioning with `modsecurity_v3_framework_provisioning_failed`; Framework PR #132 addresses one statically confirmed nested Gitlink cause. A new Parent updater PR and its exact-head runtime checks are needed after Framework integration.

## Known limitations

A manual updater is not an unconditional success guarantee: invalid candidate data, NGINX drift, sandbox failure, dependency incompatibility, or an unsafe maintenance-branch state may still block a run. The separate Framework PR #132 is unmerged. Until this Parent PR reaches `master`, the existing weekly schedule remains active.

## Remaining risks

Without the fixed structure digest, future shell-control-flow changes can reach sandbox validation and, if a generated Draft PR is merged without full review, later runtime execution. The targeted indirect-write pattern blocks known cases but is not a complete shell parser. Human review and current-head CI are essential residual controls.

## Checks not run and rationale

Local secrets scanning, repository-native unit/lint/documentation checks, `git diff --check`, and runtime tests were not run in this projectless Windows task; the SonarQube CLI was not newly authorized. Hosted GitHub Actions and SonarCloud on the final PR head must be inspected separately. Static GitHub-source checks do not substitute for executed tests.

## Final diff and review status

Keep Parent PR #398 as Draft and do not merge. The final cumulative diff must contain only the manual-updater policy change, its tests and EN/DE documentation/record; the earlier direct Framework pin is reversed in a normal follow-up commit. Framework PR #132 and subsequent manual updater delivery remain separate.
