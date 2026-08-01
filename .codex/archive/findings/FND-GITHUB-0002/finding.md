# FND-GITHUB-0002 — Framework Dependency Review is unavailable without Dependency Graph access

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-GITHUB-0002` |
| Title | `Framework Dependency Review is unavailable without Dependency Graph access` |
| Category | `github_governance` |
| Repository | `framework` |
| Ownership | `github_configuration` |
| Priority | `P1` |
| Severity | `not_applicable` |
| Confidence | `confirmed` |
| Status | `closed` |
| Release blocker | `true` |
| Security relevance | `true` |

## Summary

Exact Framework Draft PR #27 head `66d90872cfc0125536267d574b776d2e88d26b23` has a correctly pinned, least-privilege Dependency Review job, but GitHub rejected it because Dependency Review is unsupported for this repository. The prior related Dependency Graph SBOM endpoint readback returned HTTP `404`. This is a GitHub configuration/access blocker, not a Framework workflow defect that may be hidden or weakened.

## Observed behavior

GitHub Actions run `29647958872` on exact PR #27 head `66d90872cfc0125536267d574b776d2e88d26b23` reported: `Dependency review is not supported on this repository. Please ensure that Dependency graph is enabled`. A prior read-only request to `repos/Easton97-Jens/ModSecurity-test-Framework/dependency-graph/sbom` returned HTTP `404 Not Found`. The other task-owned security checks for the exact current head passed or were trigger-skipped as designed.

## Expected behavior

The Framework repository provides the Dependency Graph capability needed by GitHub Dependency Review, and a rerun on the exact PR #27 head succeeds without suppressing the job, changing its fail policy, broadening permissions, or bypassing review controls.

## Impact

The Draft PR cannot reach `verified_pr` while a required security/dependency check fails. Dependency and license changes can therefore lack the repository-native GitHub review intended by the workflow until the external configuration/access condition is resolved.

## Affected files and symbols

- `.github/workflows/ci-security-dependency-review.yml`
- `dependency-review`
- `actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294`
- GitHub Dependency Graph and its SBOM endpoint

## Preconditions

- Framework Draft PR #27 remains open at `66d90872cfc0125536267d574b776d2e88d26b23`.
- GitHub Actions and the Dependency Graph API remain reachable.
- A repository owner or administrator can make the configuration decision.

## Reproduction

```text
rtk gh run view 29647958872 --log-failed
rtk proxy gh api -i repos/Easton97-Jens/ModSecurity-test-Framework/dependency-graph/sbom
```

## Evidence

- Run ID: `20260718T083435Z-expand-framework-ci-security-32892be1`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T083435Z-expand-framework-ci-security-32892be1/evidence/ci-security/framework-pr27-final-blockers.txt`
  - Type: `exact_framework_pr_head_ci_and_dependency_graph_readback`
  - SHA-256: `1686ed164f9a892c08c6749ed5d9922269a7a026a442ddd477d62bd240848b5f`
  - Working directory: `/var/tmp/codex/worktrees/framework-ci-security`; exit code: `1`
  - Observed at: `2026-07-18T13:13:38Z`; retention: `retained_task_evidence`
- Run ID: `20260718T084030Z-expand-framework-ci-security-be8fb24d`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T084030Z-expand-framework-ci-security-be8fb24d/evidence/framework-pr27-final-remote-status.md`
  - Type: `exact_final_pr_head_external_blocker_disposition`
  - SHA-256: `ccedabbe5e020bf43eb91ccf93b1e1484b8d11471e2817b6d078a95eeddb3552`
  - Working directory: `/var/tmp/codex/worktrees/framework-ci-security`; exit code: `0`
  - Observed at: `2026-07-18T14:26:12Z`; retention: `retained_task_evidence`

## Root-cause analysis

GitHub Dependency Review reported that the repository capability it requires is unsupported. The SBOM HTTP `404` establishes that the Dependency Graph endpoint is unavailable at the observed access/configuration state; it does not alone distinguish a disabled feature from another GitHub-side entitlement or visibility condition.

## Proposed remediation

An authorized repository owner or administrator must enable or otherwise make Dependency Graph available, verify the setting/readback, and rerun Dependency Review on the unchanged exact PR #27 head. Do not disable, make advisory, skip, or weaken the workflow as a substitute.

## Acceptance criteria

- Authorized GitHub configuration evidence proves Dependency Graph is available for `Easton97-Jens/ModSecurity-test-Framework`.
- Dependency Review completes successfully for exact PR #27 head `66d90872cfc0125536267d574b776d2e88d26b23` or a later explicitly verified task-owned head.
- The immutable action pin, dependency/license policy, least permissions, and fail-closed enforcement remain unchanged.

## Validation plan

- Read the capability with authorized GitHub API evidence.
- Observe a successful exact-head Dependency Review rerun after the configuration change.
- Recheck PR SHA equality, all current checks, SonarQube Cloud, reviews, and review threads before any `verified_pr` claim.

## Regression and legitimate control tests

- Dependency Review reaches `completed/success` on the exact current PR head.
- A benign dependency-manifest change is evaluated by the pinned action without extra permissions or a token bypass.

## Dependencies and blockers

- Dependency: GitHub repository owner or administrator decision and configuration access.
- Blocker: The current task does not authorize GitHub repository-setting changes.
- Blocker: GitHub currently reports Dependency Review as unsupported and the SBOM endpoint as unavailable.

## Related findings

- `FND-FRAMEWORK-0001` is a separate PR-gate blocker; it is not the same technical cause.

## Residual risk

No risk is accepted. The PR remains a Draft and cannot be described as `verified_pr` until this externally blocked check succeeds on an exact current head.

## Current GitHub reconciliation and closure — 2026-07-26

This section supersedes the active-blocker statements above while retaining
them as historical evidence. The read-only Framework Dependency Graph SBOM
endpoint now returns HTTP 200 with an SPDX-2.3 document containing 12 packages.
Framework PR #42 is merged, and its later head
`dc6cf411e78b3f37f1e4be52edef59894560b1ae` completed Dependency Review
run 29978759046 and job 89116042141 successfully.

The current workflow still uses the immutable dependency-review action pin,
contents-read permission, high severity and runtime/development failure policy,
license and vulnerability checks, and warn-only false. Nothing was disabled,
made advisory, skipped, or given broader permissions.

The earlier PR #27 HTTP-404/unsupported failure remains historical evidence;
it is not rewritten into a pass. The now-available GitHub capability and later
successful fail-closed execution satisfy the Finding's allowed later-head
criterion. Status is therefore `closed` and the complete triplet is archived.
Reopen it if Dependency Graph or the fail-closed workflow regresses.

## History

- `2026-07-18T13:13:38Z`: `exact_pr_head_dependency_review_blocker_recorded` — Exact Framework Draft PR #27 head `5b2a26a41e7621e7b246aa1a060149252cfe3062` failed GitHub Actions run `29645450452` because Dependency Review is unsupported; the read-only Dependency Graph SBOM endpoint returned HTTP `404`. This record is blocked pending an authorized GitHub configuration/access disposition and is not a workflow-code remediation authorization.
- `2026-07-18T14:26:12Z`: `final_exact_pr_head_blocker_reconfirmed` — Exact Framework Draft PR #27 head `66d90872cfc0125536267d574b776d2e88d26b23` again failed Dependency Review run `29647958872` with the same unsupported-repository/enable-Dependency-Graph message. All task-owned security gates otherwise passed; status remains `blocked` pending authorized GitHub configuration or access resolution.
