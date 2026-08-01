# FND-GITHUB-0006 — Framework master Advanced CodeQL uploads fail while GitHub Default Setup remains enabled

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-GITHUB-0006` |
| Category | `ci_failure` |
| Repository / ownership | `framework` / `github_configuration` |
| Priority / severity | `P1` / `not_applicable` |
| Confidence / status | `confirmed` / `accepted_risk` |
| Feasibility | `out_of_scope` |
| Release blocker | `true` |
| Security relevant | `true` |

## Summary, observation, and impact

On exact Framework master `6de40c1714410241e917e9083ee890a82fb2fdbb`, PR #27's trusted Advanced CodeQL workflow failed for Actions, C/C++, and Python. Each language analyzed source, then GitHub rejected SARIF processing because Default Setup remains enabled. The three Default Setup analyses for the same SHA succeeded and the Code Scanning API reports zero open alerts.

This is an external GitHub configuration/control conflict, not a demonstrated Framework-code vulnerability. It prevents a claim that the reviewed trusted Advanced uploader succeeded and blocks a fully verified master-integration result, even though Default Setup supplies alternative coverage.

After this task's merge evidence was captured, external commits advanced Framework
`master` to `8572da580e11bc3c62f6ef559152f49b30650056`. A read-only GitHub
readback then reported Default Setup `not-configured` and successful Advanced
CodeQL jobs for Actions, C/C++, and Python. This task did not make the setting
transition or the later commits. The later state does not retroactively convert
the exact `6de40c...` failed upload into a pass, and it does not establish that
the current configuration is the configuration explicitly authorized by the
user.

## Scope, reproduction, and evidence

- Affected workflow: `.github/workflows/ci-security-codeql.yml`; controls: `analyze-trusted`, `github/codeql-action/analyze`, `upload: always`, and job-scoped `security-events: write`.
- Preconditions: Default Setup is configured for Actions, C/C++, and Python; the trusted workflow runs on `push` to `master`.
- Failed run: [CodeQL analysis `29701466354`](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/29701466354); jobs `88231112053`, `88231112086`, and `88231112094`.
- Retained evidence: `pr27-master-6de40c-post-merge-verification.md` (`/var/tmp/codex/ModSecurity-conector/runs/20260719T180448Z-framework-pr27-sonar-remediation-72a73203/evidence/pr27-master-6de40c-post-merge-verification.md`), SHA-256 `3b65d40a065d9c3459c5f83be92a09d12ea7709601a12964f4dbdbfa9e540d80`.

```text
Code Scanning could not process the submitted SARIF file:
CodeQL analyses from advanced configurations cannot be processed when the default setup is enabled
```

The retained evidence records read-only commands for the failed run, exact-master check-runs, Default Setup state, and exact-SHA Code Scanning analyses; all exited `0`.

Later external-state readback (not retained as a local artifact) used:

```text
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/code-scanning/default-setup
rtk gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/8572da580e11bc3c62f6ef559152f49b30650056/check-runs --paginate
```

It observed `state: not-configured` and terminal-success Advanced CodeQL jobs
for all three languages. This is current-state evidence only; it neither
attributes nor authorizes the external configuration change.

## Root cause and expected behavior

GitHub Default Setup and the repository-owned trusted Advanced workflow are both configured to upload CodeQL results for the same master languages. GitHub rejects Advanced SARIF processing while Default Setup remains enabled. Exactly one compatible configuration must upload each language and the selected trusted workflow must complete successfully without suppressing or weakening a control.

## Remediation, acceptance, and validation

An authorized owner must choose a configuration on a new reviewed normal Framework PR: disable Default Setup and retain the reviewed Advanced uploader, or redesign/remove the Advanced uploader while retaining independently verified compatible scanning. Do not direct-push master, bypass controls, weaken permissions, suppress failures, or change Parent/MRTS.

- [pending] GitHub readback proves the explicitly authorized configuration; the later external `not-configured` state is not that authorization.
- [historical failure / later success] The `6de40c...` Advanced uploads failed; the later external `8572da...` Advanced jobs succeeded, but this does not validate the historical merge result.
- [passed] Default Setup produced Actions, C/C++, and Python analyses for `6de40c171...` and zero open alerts.
- [pending] The Advanced uploader succeeds or is replaced through an authorized, independently verified design.

Regression/control checks: exact-master CodeQL run `29701466354`; Default Setup analyses for all three languages; zero open Code Scanning alerts; and the retained trusted workflow's job-scoped `security-events: write` with no `pull_request` trigger.

## Dependencies, blockers, related findings, residual risk, and history

Dependencies: an authorized GitHub Code Scanning configuration decision, a new reviewed Framework PR if a repository change is needed, and GitHub-hosted CodeQL processing. Blockers: the later externally observed `not-configured` state is not an explicit authorized configuration disposition and contradicts the earlier retain-Default-Setup decision for PR #27; the exact `6de40c...` failed upload remains historical evidence. Related findings: `FND-FRAMEWORK-0017`, `FND-FRAMEWORK-0020`, `FND-GITHUB-0005`, and `FND-SONAR-0002`; this record is distinct from each.

The user authorized this particular PR #27 merge after disclosure, but that does not convert the observed Advanced failure into a pass or authorize a corrective setting/workflow change. The later external configuration state may permit Advanced uploads, but it remains unapproved and unverified for persistence. The separate master SonarCloud failure remains limited accepted risk `FND-SONAR-0002` and does not waive this finding.

- `2026-07-19T20:00:39Z`: resulting_master_advanced_codeql_upload_failure_confirmed — PR #27 merged at `6de40c1714410241e917e9083ee890a82fb2fdbb`; all three Advanced uploads failed after analysis because Default Setup is enabled, while all three Default Setup analyses succeeded.
- `2026-07-19T20:32:09Z`: external_post_merge_code_scanning_state_change_observed — Framework master had externally advanced to `8572da580e11bc3c62f6ef559152f49b30650056`; API readback reports Default Setup `not-configured` and successful Advanced CodeQL jobs. No setting or master commit was made by this task, and the original exact-SHA failure remains historical evidence pending a current authorized configuration disposition.

## Current user accepted-risk archive disposition — 2026-07-26

At `2026-07-26T14:18:25Z`, the current user explicitly accepted this exact
residual risk for local archival. The exact resulting-master Advanced CodeQL
failure is not a pass, and the later externally observed `not-configured`
Default Setup state with successful Advanced jobs does not prove an
intentional, durable, authorized selected configuration. This status is
`accepted_risk`, not `closed`; restore and revalidate the record before
production, publication, or release use.
