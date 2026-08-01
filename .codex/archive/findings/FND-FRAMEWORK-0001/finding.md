# FND-FRAMEWORK-0001 — Framework test-common and common-structure checks fail

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0001` |
| Title / Titel | `Framework test-common and common-structure checks fail` |
| Category / Kategorie | `ci_failure` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `framework` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `fixed` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

The current default Framework SHA reproducibly failed `test-common / common-structure`; the focused repair now passes on exact Draft PR #23 head `f869d77070dc1fe05f7ff8377d8723b8e3185849`, but it is intentionally unmerged. Unrelated workflow-hardening Draft PR #29 and CI/security Draft PR #27 reproduced the same current-head baseline failure.

## Observed behavior / Beobachtetes Verhalten

The default workflow failed `expected 141 YAML cases, found 179`. Once that stale guard was removed locally, runtime discovery exposed a catalog-only `security-data-flow` case being validated before its `former_xfail` / `connector-gap` metadata could exclude it from runtime materialization. Exact PR #23 head now has two successful `common-structure` runs. Exact PR #29 head `191b7e3d1999c7ffb39ad16bfaff7821bfc09825` and exact PR #27 head `5b2a26a41e7621e7b246aa1a060149252cfe3062` have failed `common-structure` runs with the unchanged guard.

## Expected behavior / Erwartetes Verhalten

The exact task-branch head has passed current GitHub Actions. A future master merge and rerun are required before verification/closure, neither of which is authorized in this task.

## Impact / Auswirkung

The task repair is fixed and its Draft PR is verified at the exact head. It remains unmerged by user instruction; until that independent repair or an equivalent is integrated, unrelated Draft PRs such as #29 and #27 cannot reach `verified_pr`. The independent default-branch Sonar backlog remains a release concern but did not fail PR #23's new-code Quality Gate.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `.github/workflows/test-common.yml`
- `tests/runners/runner_core.py`
- `tests/workflow_contract/test_common_structure_workflow.py`

### Symbols / Symbole

- `test-common`
- `common-structure`
- `discover_case_files`
- `is_case_applicable`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.
- Framework `master` is at `cdc91a398d6c156eaff927d742b23018a3817fb6` and the task worktree uses its clean branch base.

## Reproduction / Reproduktion

- `sed -n '181,196p;212,215p' .codex/reports/repository-full-assessment.md`
- GitHub Actions run `29527830684` logs `expected 141 YAML cases, found 179`.
- Run the literal common-structure materialization/assertion block with an external task-owned `RUNNER_TEMP`.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:181-196,212-215`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '181,196p;212,215p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/common-structure-current.md`
  - Type: `current_ci_root_cause_and_local_regression`; SHA-256: `03a39f33a6b7e3eac71e3c4d5a32cc102de8e1a6f2d41556a64945d0c5427a1f`
  - Command: `rtk make BUILD_ROOT=<task-owned> test-workflow-contract; rtk env RUNNER_TEMP=<task-owned> ... bash -eu -c '<literal common-structure block>'`
  - Working directory: `/var/tmp/codex/worktrees/framework-common-structure`; exit code: `0`
  - Observed at: `2026-07-18T09:20:00Z`; retention: `retained_task_evidence`
- Run ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/pr-23-current.md`
  - Type: `exact_draft_pr_head_ci_sonar_review_verification`; SHA-256: `c28444cfdd989b9884e367f17e0540ccda9858a3bc10b24b26dd8293b500855d`
  - Command: local/remote/PR-head equality plus read-only PR checks and thread inspection through RTK
  - Working directory: `/var/tmp/codex/worktrees/framework-common-structure`; exit code: `0`
  - Observed at: `2026-07-18T09:58:40Z`; retention: `retained_task_evidence`
- Run ID: `20260718T081429Z-framework-workflow-hardening-320e9322`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081429Z-framework-workflow-hardening-320e9322/evidence/common-structure-baseline-recheck.md`
  - Type: `baseline_ci_recheck`; SHA-256: `290001674e3974e268f1a7f63469f1c5e1dc743eeb31f440ed1297a1433d75b9`
  - Command: literal `test-common / common-structure` count gate, authoritative-checkout count, and read-only current-`master` workflow metadata through RTK
  - Working directory: `/var/tmp/codex/worktrees/framework-workflow-hardening`; exit code: `1`
  - Observed at: `2026-07-18T10:39:59Z`; retention: `retained_task_evidence`
- Run ID: `20260718T081429Z-framework-workflow-hardening-320e9322`
  - Artifact: `evidence/pr-29-common-structure-status.md`
  - Type: `current_draft_pr_ci_baseline_confirmation`; SHA-256: `9ae5cd9cb6d4b314a69d4849d880465a79f6927ba2bd8d8b5b322f6ac36b3951`
  - Command: current Draft PR metadata plus failed GitHub Actions run inspection through RTK
  - Working directory: `/var/tmp/codex/worktrees/framework-workflow-hardening`; exit code: `1`
  - Observed at: `2026-07-18T11:33:16Z`; retention: `retained_task_evidence`
- Run ID: `20260718T083435Z-expand-framework-ci-security-32892be1`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T083435Z-expand-framework-ci-security-32892be1/evidence/ci-security/framework-pr27-final-blockers.txt`
  - Type: `exact_framework_pr_head_common_structure_duplicate_evidence`; SHA-256: `1686ed164f9a892c08c6749ed5d9922269a7a026a442ddd477d62bd240848b5f`
  - Command: `rtk proxy gh run view 29645450445 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed`
  - Working directory: `/var/tmp/codex/worktrees/framework-ci-security`; exit code: `0` (retrieval; the observed job failed)
  - Observed at: `2026-07-18T13:13:38Z`; retention: `retained_task_evidence`

## Root-cause analysis / Grundursachenanalyse

The original fixed count was introduced in `b7f9bdc9831f9a8d14294cfb8fcb129a183d5d18` when the corpus had 141 YAML files; later valid additions raised it to 179. The prior `discover_case_files()` implementation called full `load_case()` before applicability filtering, so a catalog-only `former_xfail` case without runtime `rules` failed before the intended non-runtime exclusion.

## Proposed remediation / Vorgeschlagene Remediation

Use dynamic non-empty discovery, filter non-runtime catalog metadata before runtime-only schema validation, retain validation/materialization for selected runtime cases, and verify the exact task-branch head in GitHub Actions without changing Sonar controls.

## Acceptance criteria / Akzeptanzkriterien

- Current Framework test-common and common-structure checks succeed at the target SHA.
- A regression distinguishes the repaired behavior from the failing baseline.
- Empty corpus and empty Apache common selection still fail explicitly.
- Catalog-only security-data-flow cases remain covered by their dedicated static check and do not reach materialization.

## Validation plan / Validierungsplan

- Run `make test-workflow-contract` and the literal common-structure control locally.
- Rerun the exact task-branch GitHub Actions workflow and preserve current-head evidence.
- Run the legitimate dedicated security-data-flow catalog checker as a control.

## Regression tests / Regressionstests

- `tests/workflow_contract/test_common_structure_workflow.py` covers dynamic guards and catalog-only exclusion.

## Legitimate control tests / Legitime Kontrolltests

- Selected Apache common cases still materialize and assert their expected statuses.

## Dependencies / Abhängigkeiten

- `FND-SONAR-0002` remains independent and must not be mixed into this Framework patch.

## Blockers / Blocker

- No merge authorization exists; policy requires post-merge reproduction before closure. The independent default-branch Sonar backlog remains a release blocker despite the passing PR new-code Quality Gate.

## Related findings / Verwandte Findings

- `FND-SONAR-0002`
- `FND-CROSS-0005`

## Residual risk / Restrisiko

The focused repair is verified only on the unmerged Draft PR head. No risk has been accepted; future master integration and the independent default-branch Sonar backlog remain outside this task.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T09:27:57Z`: current_task_root_cause_and_repair_in_progress — Current-SHA evidence proved the stale cardinality guard and the masked discovery-ordering defect; focused local regression and literal control passed. No PR-head verification or closure has occurred.
- `2026-07-18T09:58:40Z`: exact_draft_pr_head_verified_fixed — Draft PR #23 is clean, exact-head equal locally/remotely/in PR, has six successful checks including two `common-structure` and SonarCloud runs, and has no reviews or review threads. It is intentionally not merged, so the finding is fixed rather than closed.
- `2026-07-18T10:39:59Z`: workflow_hardening_baseline_recheck_deduplicated — The separate workflow-hardening task reran the unchanged count gate: it still exits `1` with `expected 141 YAML cases, found 179`. The authoritative checkout has the same count, and current `master` run `29527830684` remains failed at `cdc91a398d6c156eaff927d742b23018a3817fb6`. This is duplicate confirmation, not a task-owned remediation.
- `2026-07-18T11:33:16Z`: workflow_hardening_draft_pr_ci_baseline_confirmation — Draft PR #29 head `191b7e3d1999c7ffb39ad16bfaff7821bfc09825` passed `check-action-versions` and `scaffold-lint`, but both current-head `common-structure` runs failed with the unchanged `expected 141 YAML cases, found 179` guard. This task does not change `tests/cases` or common structure, so this is duplicate baseline evidence only.
- `2026-07-18T13:13:38Z`: ci_security_draft_pr_baseline_recheck_deduplicated — Exact Draft PR #27 head `5b2a26a41e7621e7b246aa1a060149252cfe3062` has two failed `common-structure` checks with the unchanged `expected 141 YAML cases, found 179` guard. The CI/security expansion does not change `tests/cases` or common structure, so this is duplicate baseline evidence only; status remains `fixed` pending the separate unmerged repair.
- `2026-07-18T14:26:12Z`: final_ci_security_draft_pr_baseline_recheck_deduplicated — Final exact Draft PR #27 head `66d90872cfc0125536267d574b776d2e88d26b23` again failed `common-structure` run `29647958875` with unchanged `expected 141 YAML cases, found 179`. This task still does not change `tests/cases` or common structure; status remains `fixed` and the new evidence is a duplicate baseline confirmation only.

## Current exact-head duplicate evidence

`framework-pr27-final-remote-status.md` retains the exact final-head run,
SHA-256 `ccedabbe5e020bf43eb91ccf93b1e1484b8d11471e2817b6d078a95eeddb3552`.
It confirms that this unrelated gate blocks PR #27 delivery without reopening,
weakening, or changing the separate fixed finding.

## 2026-07-19 direct stale-PR reintroduction hazard

The direct two-tree comparisons from current Framework `master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` show that stale, unmerged PR
heads #24, #27, and #29 remove the merged dynamic non-empty common-structure
control and restore the fixed count/order failure. This is a merge blocker,
not a reopening of the finding: the current master remains `fixed` and no
control was weakened.

Retained evidence: run `20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
observed `2026-07-19T12:01:55Z` by RTK-prefixed direct-diff and GitHub gate
readback.
