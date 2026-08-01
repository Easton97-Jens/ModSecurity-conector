# FND-PARENT-0023 — Submodule-update validation shares a workspace with later GitHub-token publishing

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | FND-PARENT-0023 |
| Title / Titel | Submodule-update validation shares a workspace with later GitHub-token publishing |
| Category / Kategorie | security_hardening |
| Repository / Repository | parent |
| Ownership / Ownership | parent |
| Priority / Priorität | P1 |
| Severity / Schweregrad | medium |
| Confidence / Konfidenz | probable |
| Status | closed (archived) |
| Feasibility status / Machbarkeitsstatus | feasible_now |
| Release blocker / Release-Blocker | false |
| Security relevance / Security-Relevanz | true |

## Summary / Zusammenfassung

Five GitHub Code Scanning Scorecard TokenPermissionsID alerts identified write permissions declared at workflow scope. In particular, update-submodules.yml recursively checked out and advanced Framework submodule content, ran make quick-check, then published a branch and pull request with GH_TOKEN in the same job. The remediation keeps restrictive workflow defaults and separates read-only validation from token-bearing publishing. The final pull-request tree and current master tree match, and the original permission-boundary reproduction plus exact-master controls verify the remediation.

## Observed behavior / Beobachtetes Verhalten

At c8ca0d92b630c18232b881855c4f5d1482568ea6, update-submodules.yml declared contents: write and pull-requests: write at top level, recursively checked out and advanced the Framework submodule, executed make quick-check, then used GH_TOKEN to force-push and create a Parent pull request. cleanup-artifacts.yml and test-full-smoke-sequential.yml declared top-level actions: write; update-actions-versions.yml declared top-level contents: write, pull-requests: write, and actions: write. The GitHub Code Scanning API reported five corresponding Scorecard alerts.

## Expected behavior / Erwartetes Verhalten

Every affected Parent workflow declares the restrictive top-level default contents: read, and each job receives only the additional capability it needs. Remote submodule content is resolved and executed only by a read-only validation job. A separate publisher validates the selected official commit, updates only the gitlink without checking out or executing submodule content, and receives contents: write and pull-requests: write only while publishing.

## Impact / Auswirkung

A compromised or unexpected submodule update could influence a workspace before a privileged workflow operation. Workflow-scoped write permissions also expand token exposure for unrelated jobs and trigger Scorecard security findings. The original assessment established a plausible trust-boundary violation, not demonstrated token exfiltration or an unauthorized repository write.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- .github/workflows/cleanup-artifacts.yml
- .github/workflows/test-full-smoke-sequential.yml
- .github/workflows/update-actions-versions.yml
- .github/workflows/update-submodules.yml
- tests/test_ci_security_workflows.py

### Symbols / Symbole

- cleanup-artifacts
- test-full-smoke-sequential
- update-actions-versions
- update-submodules

## Preconditions / Voraussetzungen

1. The scheduled or manually dispatched update-submodules workflow runs on the protected default branch.
2. The Framework submodule remote advances to a commit selected by git submodule update --remote --recursive.
3. The workflow job later performs GitHub-token-authenticated branch and pull-request publishing.

## Reproduction / Reproduktion

1. Inspect .github/workflows/update-submodules.yml at c8ca0d92b630c18232b881855c4f5d1482568ea6.
2. Observe top-level contents: write and pull-requests: write, recursive submodule checkout/update, make quick-check, and later GH_TOKEN-backed push and pull-request steps in one job.
3. Query the GitHub Code Scanning API for open Scorecard alerts and observe TokenPermissionsID alerts 2 through 6 documented by the retained evidence.

## Evidence / Evidence

1. Original source and Scorecard assessment
   - Run ID: 20260718T080138Z-harden-workflow-permissions-e804be63
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260718T080138Z-harden-workflow-permissions-e804be63/evidence/workflow-permission-trust-boundary.md
   - Artifact type: workflow_permission_and_trust_boundary_assessment
   - SHA-256: b7a702366ee7c9c7b470f5d7ef950dd4c51cb1ba504f62e1a956bc1f7f7bc6a3
   - Command: rtk gh api 'repos/Easton97-Jens/ModSecurity-conector/code-scanning/alerts?tool_name=Scorecard&state=open&per_page=100' and rtk cat .github/workflows/update-submodules.yml
   - Working directory: /root/git/ModSecurity-conector
   - Exit code: 0; observed at: 2026-07-18T08:01:38Z; retention: retained_task_evidence
2. Historical exact-head verification
   - Run ID: 20260718T080138Z-harden-workflow-permissions-e804be63
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260718T080138Z-harden-workflow-permissions-e804be63/evidence/pr-54-a9719b8-exact-head-verification.md
   - Artifact type: pull_request_exact_head_verification
   - SHA-256: fd516aa371cf5bb13a8de6d402a97aa088703a2488fb4a406e150dddfb9a2aae
   - Command: rtk gh pr view 54 --repo Easton97-Jens/ModSecurity-conector and rtk gh run view for exact head a9719b89f5a37f6added5b10920eccbd0e405217
   - Working directory: /var/tmp/codex/worktrees/parent-workflow-permissions
   - Exit code: 0; observed at: 2026-07-18T09:32:05Z; retention: retained_task_evidence
3. Final exact-head verification and Sonar remediation
   - Run ID: 20260719T103749Z-parent-pr-53-60-integration-a7b98a59
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260719T103749Z-parent-pr-53-60-integration-a7b98a59/evidence/pr54-d4318ce-exact-head-verification.md
   - Artifact type: pull_request_exact_head_verification_and_sonar_remediation
   - SHA-256: f0f757e73a26c0ead915e399b755a200e51ded593fd9308dad0978609d88ffb6
   - Command: rtk make check-ci-security-contract; rtk git diff --check origin/master..HEAD; rtk gh pr checks 54 --required; GitHub Checks API; SonarCloud Quality Gate and open-issue API
   - Working directory: /var/tmp/codex/worktrees/parent-workflow-permissions
   - Exit code: 0; observed at: 2026-07-19T11:02:11Z; retention: retained_task_evidence
4. Post-merge master verification
   - Run ID: 20260719T103749Z-parent-pr-53-60-integration-a7b98a59
   - Artifact path: /var/tmp/codex/ModSecurity-conector/runs/20260719T103749Z-parent-pr-53-60-integration-a7b98a59/evidence/pr54-master-verification-63819e4.md
   - Artifact type: post_merge_master_reproduction_and_workflow_verification
   - SHA-256: e0db6fba0aee9629dd11b71e154c7c2f3daa9d15549c94e3fdf7ee0fb7990b71
   - Command: rtk git rev-parse/diff/grep; rtk make check-ci-security-contract; rtk gh pr view/run list/api Scorecard alerts for PR #54 and master 63819e416984294792bbbe68aa5d84503791baab
   - Working directory: /root/git/ModSecurity-conector
   - Exit code: 0; observed at: 2026-07-19T11:18:33Z; retention: retained_task_evidence

## Root-cause analysis / Grundursachenanalyse

Write permissions were granted at workflow scope even though only individual jobs needed them. update-submodules combined remote submodule selection, submodule code execution, and token-bearing publication in one workspace/job. The repository-level Actions default was write, so workflows without an explicit restrictive default also inherited excessive authority.

## Proposed remediation / Vorgeschlagene Remediation

Set contents: read at each affected workflow top level. Move actions: write to isolated artifact-cleanup jobs. Scope update-actions-versions writes to its single publisher job while retaining persist-credentials: false. Split update-submodules into read-only resolution/validation and a separate minimal-permission publisher that validates the official remote commit and updates only the gitlink without checking out or executing the submodule. Preserve security-events: write for SARIF-upload jobs and add the permission-contract fixtures and regressions.

## Acceptance criteria / Akzeptanzkriterien

- All Parent workflow files declare exactly the restrictive top-level default contents: read.
- No job with checkout, project execution, recursive submodule access, or untrusted pull-request execution has a write-scoped GitHub token, named secret, or persisted checkout credentials unless separately justified and proven safe.
- update-submodules validates remote content in a contents: read job and publishes only from a distinct job that does not check out or execute submodule content.
- CodeQL and other legitimate SARIF uploads retain only the required security-events: write permission alongside contents: read.
- The workflow-permission contract tests, safe/unsafe fixtures, actionlint, ShellCheck, zizmor, secret scanning, OSV, Scorecard, CodeQL/SARIF, and git diff --check provide the strongest applicable evidence.

## Validation plan / Validierungsplan

1. Parse all workflow YAML through actionlint with ShellCheck integration.
2. Run the focused CI-security workflow contract, including safe and unsafe fixtures, fork/untrusted pull-request modelling, submodule trust boundaries, and SARIF-upload permissions.
3. Run zizmor over production workflows and verify its insecure fixture still fails while its safe fixture passes.
4. Run Gitleaks, OSV, and Scorecard/CodeQL workflow checks through the focused pull request and verify the exact head SHA in GitHub Actions and Code Scanning.
5. Run git diff --check and inspect the final Parent-only diff.

## Regression tests / Regressionstests

- tests/test_ci_security_workflows.py
- ci/fixtures/workflow-permission-contract/safe.yml
- ci/fixtures/workflow-permission-contract/unsafe.yml

## Legitimate control tests / Legitime Kontrolltests

- CodeQL, OSV, and Scorecard retain security-events: write only in SARIF-upload jobs and retain contents: read.
- Artifact-cleanup jobs retain actions: write without checkout or project execution.
- The update-submodules publishing job can create the expected Parent pull request after read-only validation selected a verified official remote commit.

## Dependencies, blockers, and related findings / Abhängigkeiten, Blocker und verwandte Findings

### Dependencies / Abhängigkeiten

- GitHub Actions runners and GitHub Code Scanning execute the focused pull-request checks.
- FND-GITHUB-0001 remains tracked separately because repository-level default-workflow-permission configuration is outside this Parent pull request.

### Blockers / Blocker

- None / Keine.

### Related findings / Verwandte Findings

- FND-GITHUB-0001

## Current remediation disposition and residual risk / Aktuelle Behebungsdisposition und Restrisiko

PR #54 final head d4318cef184a1cdeb70858cc18861d7e5649037b was squash-merged as 63819e416984294792bbbe68aa5d84503791baab. The master tree equals the final PR tree; the original source/permission-boundary reproduction no longer reports TokenPermissionsID; and all 14 observed exact-master workflows, including OpenSSF Scorecard, passed. The repository-level default_workflow_permissions now reads read; separate remaining governance alerts stay in FND-GITHUB-0001. No risk acceptance exists. This finding is verified, not closed; closure requires a separate lifecycle decision.

## History / Historie

- 2026-07-18T08:01:38Z — finding_created_from_scorecard_and_source_assessment: recorded five open Scorecard TokenPermissionsID alerts and the plausible update-submodules validation-to-publishing trust boundary before remediation.
- 2026-07-18T09:32:05Z — fixed_on_exact_pull_request_head: PR #54 head a9719b89f5a37f6added5b10920eccbd0e405217 passed CodeQL, OSV SARIF upload, Scorecard, secret scanning, workflow lint, and SonarQube quality gate; it remained fixed pending merge and default-branch reproduction.
- 2026-07-19T11:05:11Z — post_master_sync_sonar_delivery_blocker_remediated: after normal merge of a589cb662fb03deb764f78eefbb1056bc64d63e2, PR #54 replaced the equivalent literal two-space JOB_HEADER prefix with {2}. Final head d4318cef184a1cdeb70858cc18861d7e5649037b passed required checks, CodeQL, OSV, report-governance, and SonarCloud with zero open PR issues and zero security hotspots.
- 2026-07-19T11:18:33Z — current_master_reproduction_verified: PR #54 merged as 63819e416984294792bbbe68aa5d84503791baab; its tree equals final head d4318cef184a1cdeb70858cc18861d7e5649037b; the original reproduction no longer reports TokenPermissionsID; and all 14 observed exact-master workflows passed. The finding is verified, not closed.
- 2026-07-19T11:58:56Z — canonical_category_and_bilingual_record_normalized: normalized the canonical category to security_hardening and restored historical exact-head evidence with SHA-256 fd516aa371cf5bb13a8de6d402a97aa088703a2488fb4a406e150dddfb9a2aae to the complete English and German records. Status, severity, confidence, release-blocker disposition, and master-verification evidence are unchanged.
- 2026-07-26T14:09:02Z — closed_by_current_user_after_current_master_validation: the current user authorized closure and archival; `tests.test_ci_security_workflows` passed on Parent master `6ca7e1536ce7e93da68099db9c586b88852ff13e` as part of the 144-test control suite. The separate repository-default governance finding remains active.
