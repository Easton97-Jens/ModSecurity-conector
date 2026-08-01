# FND-GITHUB-0004 — Platform-managed GitHub Advanced Security Code Scanning AI runs fail with an unsupported model

## Identity

| Field | Value |
| --- | --- |
| ID | FND-GITHUB-0004 |
| Title | Platform-managed GitHub Advanced Security Code Scanning AI runs fail with an unsupported model |
| Category | github_governance |
| Repository | framework |
| Ownership | github_configuration |
| Priority | P1 |
| Severity | not_applicable |
| Confidence | confirmed |
| Status | accepted_risk |
| Feasibility | out_of_scope |
| Release blocker | true |
| Security relevance | true |

## Summary, observed behavior, and impact

GitHub's platform-managed GitHub Advanced Security / Code Scanning AI workflow fails before completing its requested analysis because its configured model is unsupported. This is a GitHub-side runtime/configuration condition, not a Framework source, workflow, Parent-gitlink, or MRTS defect. It prevents a claim that this dynamic security control has passed for an affected exact PR head; it must not be hidden, waived, or represented as a successful scan.

On Framework PR #26 exact head 63c42e97b86acbae1374efa9f1c4209ce2ce673b, dynamic run 29680055620 and check 88174464227 / github-advanced-security completed with failure. Its Processing Request (Linux) output records:

~~~text
The requested model is not supported.
code=model_not_supported
param=model
~~~

The run identifies sweagent-capi:claude-opus-4.6 as the configured model. The earlier PR #25 head c5e7553cf5f3eb7c5535e392798e03ae21f81981 has a separate failed Code scanning AI findings run 29659308388; its available annotation says only Process completed with exit code 1. The new PR #25 head c6ba5e11359d6eb30e8717b766d49697f9bed74f has a successful dynamic CodeQL run but no matching Code Scanning-AI run, so the old failure cannot be called a pass and the absent run cannot be inferred to be a failure.

An affected Framework PR cannot truthfully claim successful GitHub Advanced Security Code Scanning AI coverage. The condition is a release-readiness and security-evidence blocker, separate from NGINX release provenance and regular current-head CodeQL/SonarCloud results. It does not establish a Framework-code vulnerability and does not authorize a workaround in Framework security workflows.

## Expected behavior, affected scope, preconditions, and reproduction

GitHub must supply a supported model or an authorized owner must make and prove a platform configuration decision. The platform-managed check must then succeed for every applicable exact current head without weakening, suppressing, or misrepresenting the control.

No Framework source file is identified as faulty. Affected external symbols are GitHub Advanced Security, dynamic/agents/github-advanced-security, github-advanced-security, Processing Request (Linux), model_not_supported, and sweagent-capi:claude-opus-4.6.

Preconditions: the dynamic Code Scanning AI / GitHub Advanced Security workflow is enabled, chooses the observed model, creates a run for an exact Framework PR head, and Actions metadata remains readable.

~~~text
rtk gh run view 29680055620 --repo Easton97-Jens/ModSecurity-test-Framework --log-failed
rtk gh run view 29680055620 --repo Easton97-Jens/ModSecurity-test-Framework --json databaseId,name,event,status,conclusion,headSha,workflowName,url,jobs
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/63c42e97b86acbae1374efa9f1c4209ce2ce673b/check-runs
rtk gh run view 29659308388 --repo Easton97-Jens/ModSecurity-test-Framework --json databaseId,event,headSha,status,conclusion,workflowName,jobs,url
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/check-runs/88119051677/annotations
~~~

## Evidence

- Run ID: 20260719T081017Z-framework-pr-resolution-20260719-840082e0
  - Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/github-advanced-security-pr26-63c42e9.md
  - Type: github_advanced_security_exact_head_external_platform_failure
  - SHA-256: 7cb69c72059872f0bf6e2a5319d0846cc9f398c0fdb2584e675fd57dd58f6161
  - Command: rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/63c42e97b86acbae1374efa9f1c4209ce2ce673b/check-runs; rtk gh run view 29680055620 --json databaseId,name,event,status,conclusion,headSha,headBranch,workflowName,url,jobs; rtk gh run view 29680055620 --log-failed
  - Working directory: /root/git/ModSecurity-conector; exit code: 0; observed at 2026-07-19T08:35:08Z; retention: retained_task_evidence.
- Run ID: 20260719T081017Z-framework-pr-resolution-20260719-840082e0
  - Artifact: /var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr25-c6ba5e1-final-merge-preflight.md
  - Type: pr25_current_head_and_related_dynamic_security_disposition
  - SHA-256: ba337d271ba9b033383a8d27394eaa6e9b5d5eef4207b7dd61a564e9e091c98a
  - Command: rtk gh pr view 25; rtk gh api commits/c6ba5e11359d6eb30e8717b766d49697f9bed74f/check-runs; rtk gh api actions/runs?head_sha=<sha>; rtk gh run view 29659308388
  - Working directory: /root/git/ModSecurity-conector; exit code: 0; observed at 2026-07-19T09:33:15Z; retention: retained_task_evidence.

## Root cause, remediation, and acceptance criteria

The retained exact-head failure identifies a GitHub-platform model selection that is unsupported. Repository-owned code and workflow controls completed before the platform-managed processing step failed. The historical #25 failure is consistent with the same delivery boundary but lacks the specific model error in the accessible annotation.

An authorized GitHub repository owner or platform administrator must select or enable a supported model, or provide an evidence-backed supported-platform disposition. Then rerun or observe GitHub Advanced Security on every applicable exact Framework PR head. Do not remove, suppress, make advisory, rename, or weaken a repository-owned security control as a substitute. This task has no authority to modify GitHub platform configuration, subscription, model availability, or secrets.

Acceptance criteria:

- Concrete evidence proves a supported model is selected and usable for the Framework repository.
- GitHub Advanced Security Code Scanning AI succeeds for every applicable exact current Framework PR head.
- The record distinguishes a current successful CodeQL run, an absent Code Scanning-AI run, and a successful Code Scanning-AI run; none substitutes for another.
- No Framework security check, policy, permissions boundary, Parent gitlink, or MRTS content is weakened or changed as a workaround.

## Validation, dependencies, blockers, related findings, residual risk, and history

Validate by querying exact-head dynamic run inventory/raw check runs, inspecting GitHub-available job logs or annotations, and rechecking PR SHA, required checks, SonarCloud, reviews, review threads, and branch/ruleset state. Current CodeQL success is a legitimate separate control, not Code Scanning-AI coverage.

Dependency: GitHub platform/model availability and a repository-owner or platform-administrator decision. The task does not authorize GitHub platform configuration, subscription, model, or secret changes.

Related findings: FND-GITHUB-0002 is a distinct Dependency Graph capability gap; FND-SONAR-0002 is a distinct pre-existing Framework default-branch Quality-Gate backlog; FND-FRAMEWORK-0006 is a distinct NGINX archive provenance remediation.

Before the current user's 2026-07-26 archive decision, no risk was accepted. Current exact-head CodeQL, SonarCloud, and repository-owned CI results remain separate evidence and must not be described as a successful Code Scanning-AI run.

- 2026-07-19T08:35:08Z: platform_model_failure_confirmed — PR #26 dynamic GitHub Advanced Security run 29680055620 failed with code=model_not_supported for sweagent-capi:claude-opus-4.6.
- 2026-07-19T09:33:15Z: pr25_related_dynamic_run_reconciled — old PR #25 dynamic Code Scanning-AI run 29659308388 is failed, while new head c6ba5e11359d6eb30e8717b766d49697f9bed74f has a successful CodeQL dynamic run and no matching Code Scanning-AI run. The historical state was blocked_external_dependency; no run is hidden or reclassified as successful.

## Current user accepted-risk archive disposition — 2026-07-26

At `2026-07-26T14:18:25Z`, the current user explicitly accepted this exact
residual risk for local archival. GitHub has not proven a supported model or a
successful applicable Code Scanning-AI run. CodeQL, SonarCloud, and
repository-owned CI remain separate evidence and must not be described as
Code-Scanning-AI success. This status is `accepted_risk`, not `closed`;
restore and revalidate the record before production, publication, or release
use.
