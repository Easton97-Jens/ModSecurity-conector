# FND-GITHUB-0008 — Framework workflow-tool publisher remains blocked until its dedicated GitHub App is configured

## Identity

| Field | Value |
| --- | --- |
| Category | `ci_failure` |
| Repository / ownership | `framework` / `github_configuration` |
| Priority / severity / confidence | `P1` / `not_applicable` / `confirmed` |
| Status / feasibility | `accepted_risk` / `out_of_scope` |
| Release blocker / security relevant | `true` / `true` |
| Historical run / source revision | `30190898961` / `7e9a560f3acda65510c93f649b6ed4977e4cd6cb` |
| Current run / source revision | `30195702432` / `c27c644e088904b71b8380d16ee34f1b36f2c001` |
| Current failing job / step | `89776795329` / `Mint repository-limited workflow publisher App token` |

## Summary

The original native-token failure is fixed in source: Framework PR
[#46](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/46)
was merged as `c27c644e088904b71b8380d16ee34f1b36f2c001`. Its source keeps the
native publisher token at `contents: read` and uses a pinned, short-lived
repository-limited GitHub App token only in four reviewed publisher consumers.

The manual `workflow_dispatch` run #2 reached the publisher after successful
resolver and validator jobs, then failed closed before issuing any token. Its
required `WORKFLOW_UPDATER_APP_CLIENT_ID` input is empty. The secret-free
name-only inventory also returned no repository variable or secret names. This
is the same external GitHub-App configuration lifecycle as the first failure,
not a new Framework source defect. Parent, its Framework gitlink, and MRTS
remain out of scope and unchanged.

## Observed and expected behavior

Historical run `30190898961` validated a five-file candidate but GitHub
rejected its native `github.token` workflow-file push for missing App-level
`Workflows: write`. The merged source remediation then replaced that native
publisher path with:

```yaml
permissions:
  contents: read
uses: actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1 # v3.2.0
with:
  client-id: ${{ vars.WORKFLOW_UPDATER_APP_CLIENT_ID }}
  private-key: ${{ secrets.WORKFLOW_UPDATER_APP_PRIVATE_KEY }}
  owner: ${{ github.repository_owner }}
  repositories: ${{ github.repository }}
  permission-contents: write
  permission-pull-requests: write
  permission-workflows: write
```

Current run `30195702432` (run #2, `workflow_dispatch`, Framework `master`
`c27c644e088904b71b8380d16ee34f1b36f2c001`) completed resolver and validator.
Publisher job `89776795329` failed only at token minting; all later API,
branch, push, and Draft-PR steps were skipped. GitHub reported:

```text
The 'client-id' (or deprecated 'app-id') input must be set to a non-empty string.
If using a secret or variable, ensure it is available in this workflow context.
```

Expected behavior is that, after authorized external configuration, a valid
allowlisted workflow-pin candidate mints the constrained App token, pushes only
the fixed maintenance branch, and creates or updates exactly one matching Draft
PR. Resolver and validator must remain read-only and credential-free; `master`
must not be changed by the updater.

## Impact, affected surface, and preconditions

Automated publication of reviewed immutable Action/tool maintenance remains
unavailable until the external App configuration is completed. The workflow's
fail-closed behavior prevents a broad token, direct `master` push, or accidental
secret exposure from substituting for that configuration.

Affected source is `.github/workflows/update-workflow-tools.yml`; the relevant
symbols are `Mint repository-limited workflow publisher App token`,
`WORKFLOW_UPDATER_APP_CLIENT_ID`, and `WORKFLOW_UPDATER_APP_PRIVATE_KEY`.
Preconditions are successful resolver/validator completion and a publisher
attempt to mint the dedicated App token. A later candidate may modify an
allowlisted `.github/workflows/*` path.

## Evidence and reproduction

| Field | Historical run #1 | Current run #2 |
| --- | --- | --- |
| Run ID | `20260726T063152Z-framework-update-pinned-workflow-tools-1` | `20260726T090147Z-framework-update-pinned-workflow-tools-2` |
| GitHub run | `30190898961` | `30195702432` |
| Artifact path | `.codex/runs/20260726T063152Z-framework-update-pinned-workflow-tools-1/evidence/framework-update-pinned-workflow-tools-run-1-receipt.md` | `/var/tmp/codex/ModSecurity-conector/runs/20260726T090147Z-framework-update-pinned-workflow-tools-2/evidence/framework-update-pinned-workflow-tools-run-2-receipt.md` |
| Artifact type | `github_actions_workflow_publisher_permission_failure_receipt` | `github_actions_workflow_publisher_missing_client_id_receipt` |
| SHA-256 | `310ff8dc82ce5b3bb58d1da7ed93b16b8fb5231b757af6000f6125a71df9254f` | `537bf3001c99be6615a9ea0c02b091556baa3ef0a5758177d28ec8931c890592` |
| Observed at | `2026-07-26T06:31:52Z` | `2026-07-26T09:07:01Z` |
| Retention | `retained_sealed_local_control_plane` | `retained_sealed_external_task_evidence` |

The current receipt was retained under the task-owned external root because the
canonical `.codex/runs` mount is read-only; the canonical finding records its
exact path and checksum. Neither receipt retains a credential value.

Reproduce safely with `rtk proxy -- gh run view 30195702432 --repo
Easton97-Jens/ModSecurity-test-Framework --log-failed`, `rtk proxy -- git
show origin/master:.github/workflows/update-workflow-tools.yml`, `rtk proxy --
gh variable list --repo Easton97-Jens/ModSecurity-test-Framework`, and `rtk
proxy -- gh secret list --repo Easton97-Jens/ModSecurity-test-Framework`.
The inventories are name-only and must never be used to read or infer secret
values.

## Root cause and remediation

The previous native-token authority defect was corrected by merged PR #46.
Run #2 proves that the present source stops at its first external prerequisite:
the repository variable `WORKFLOW_UPDATER_APP_CLIENT_ID` is absent. The private
key secret, dedicated App installation, and precise App permissions remain
unverified because token minting cannot begin without that client ID.

An authorized repository owner must:

1. Create or configure a dedicated GitHub App and install it **only** on
   `Easton97-Jens/ModSecurity-test-Framework`.
2. Give it exactly `Contents: write`, `Pull requests: write`, and
   `Workflows: write` repository permissions.
3. Add repository Actions variable `WORKFLOW_UPDATER_APP_CLIENT_ID` and
   repository Actions secret `WORKFLOW_UPDATER_APP_PRIVATE_KEY` without
   exposing the private key to Codex, source, logs, or evidence.
4. Rerun the updater and verify its constrained maintenance branch and matching
   Draft PR.

Do not reintroduce `github.token` or `GITHUB_TOKEN` as a publisher fallback,
use a personal access token, grant broader installation scope, weaken the
workflow checks, or push `master` directly.

## Acceptance criteria and validation plan

1. The dedicated App is installed only on this repository with `Contents`,
   `Pull requests`, and `Workflows` write permission; no credential value
   reaches source, evidence, logs, resolver, or validator.
2. The authorized owner configures `WORKFLOW_UPDATER_APP_CLIENT_ID` and
   `WORKFLOW_UPDATER_APP_PRIVATE_KEY` without revealing the private key.
3. `master` retains the pinned App-token source and has no `github.token` or
   `GITHUB_TOKEN` publishing fallback.
4. A new updater run creates or updates exactly one matching Draft PR via the
   constrained maintenance branch, with no direct `master` change.
5. The Draft PR remains within the validated allowlisted candidate surface.

Validation is the name-only configuration readback, source review, and a new
controlled updater run. The security control case is a workflow-pin candidate
that creates the Draft PR without exposing the credential or changing `master`.
The regression evidence is PR #46's CI-security/action-pin validation and the
six successful merge-triggered Framework `master` push workflows at
`c27c644e088904b71b8380d16ee34f1b36f2c001`; those do not replace the required
end-to-end updater rerun.

## Dependencies, blockers, related findings, and residual risk

Dependencies are current repository-owner authorization for GitHub App
installation plus Actions variable/secret configuration, and a repository-
limited App with the stated permissions. Blockers are the absent
`WORKFLOW_UPDATER_APP_CLIENT_ID`, the empty name-only secret inventory (so
`WORKFLOW_UPDATER_APP_PRIVATE_KEY` is not configured), and unverified App
installation/permissions.

Related findings are `FND-GITHUB-0005`, `FND-FRAMEWORK-0047`, and
`FND-FRAMEWORK-0048`. Residual risk is the continuing absence of the automated
security-maintenance publication path. No risk acceptance, source workaround,
GitHub setting, secret, branch, PR, merge, Parent gitlink, or MRTS change was
performed by this current diagnostic task.

## Source-remediation and history update

PR #46 final head `781b5603975369dd9b9a1661edc417dd37f5dfa7` was merged at
`2026-07-26T08:58:11Z` as Framework `master`
`c27c644e088904b71b8380d16ee34f1b36f2c001`. Its normal exact-head PR checks
passed; all six merge-triggered `master` push workflows also passed. The
manual updater run #2 is a separate `workflow_dispatch` event and remains the
required end-to-end validation.

- `2026-07-26T06:21:44Z`: Historical publisher push was rejected for missing
  native App `Workflows: write` authority.
- `2026-07-26T08:58:11Z`: PR #46 merged the source-only App-token boundary.
- `2026-07-26T09:01:47Z`–`2026-07-26T09:02:36Z`: Run #2 failed closed because
  `WORKFLOW_UPDATER_APP_CLIENT_ID` was empty; no later publisher action ran.
- `2026-07-26T09:07:01Z`: Secret-free receipt and this canonical finding were
  updated. The historical status remained `blocked` / `blocked_permissions`.

## Current user accepted-risk archive disposition — 2026-07-26

At `2026-07-26T14:18:25Z`, the current user explicitly accepted this exact
residual risk for local archival. Automated publication of reviewed immutable
workflow/tool maintenance updates remains unavailable because the dedicated
GitHub App, client-ID variable, and private-key secret are not configured. The
fail-closed workflow must not gain a `github.token`, personal-token, pin,
validation, scope, credential-isolation, or default-branch-protection
workaround. This status is `accepted_risk`, not `closed`; restore and
revalidate the record before production, publication, or release use.
