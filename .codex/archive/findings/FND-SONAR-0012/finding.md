# FND-SONAR-0012 — MRTS PR #3 SonarQube Cloud validator signals are resolved by merged PR #4

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-SONAR-0012` |
| Category | `sonarqube_finding` |
| Repository / ownership | `mrts` / `mrts` |
| Priority / severity / confidence | `P1` / `not_applicable` / `confirmed` |
| Status / feasibility | `closed` / `feasible_now` |
| Release blocker / security relevance | `false` / `true` |
| Affected revisions | historical PR #3 `e8bb04edf9e0cea03786e834c1f516f367d6136a`; remediation PR #4 `9cdfd4136286014b244f8fecfb99701681fecae4`; current main `615b13bacbd008562c17408246c41ab27dca3104` |

## Summary, behavior, and impact

Historical Draft MRTS PR #3 head `e8bb04edf9e0cea03786e834c1f516f367d6136a`
failed `new_security_rating`: actual `4` (D), required `1` (A), with seven
task-owned signals in `tools/validate-governance.py`.

MRTS PR #4 head `9cdfd4136286014b244f8fecfb99701681fecae4` remediated that
condition, passed Analyze (python), CodeQL, Python 3.14 governance, and
SonarCloud Code Analysis, and was Squash-merged as current main
`615b13bacbd008562c17408246c41ab27dca3104`. Hash-valid retained receipts and
the current live SonarQube Cloud recheck for PR #3, PR #4, and main report
Quality Gate `OK` and zero vulnerabilities.

The former CI/quality-gate blocker is closed. This disposition is limited to
the seven historical PR #3 validator signals and does not close unrelated
SonarQube Cloud coverage or Framework findings.

## Boundary, source/control/sink assessment

The affected file remains a local, read-only governance CLI. The focused PR #4
remediation and retained tests preserve the no-Git/no-shell/no-network/no-
cleanup-execution, containment, symlink, UTF-8 JSON, and exact cleanup
invariants. No scanner rule, Quality Gate, exclusion, false-positive
disposition, `NOSONAR`, suppression, or security-control weakening was used.

## Preconditions and reproduction

- The retained historical PR #3 receipt documents the former failure.
- PR #4 is merged and `615b13bacbd008562c17408246c41ab27dca3104` is current
  MRTS `main`.
- The PR #4 and resulting-main receipts remain hash-valid, and current public
  SonarQube Cloud and GitHub readbacks are available.

```text
rtk gh pr checks 4 --repo Easton97-Jens/MRTS
rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_MRTS&pullRequest=4'
rtk proxy curl --fail --silent --show-error 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_MRTS&pullRequest=4&resolved=false&types=VULNERABILITY&ps=100'
```

The current checks pass; the historical receipt remains the original-failure
proof.

## Evidence

- Historical failure receipt: `.codex/runs/20260724T170026Z-worktree-cleanup-governance/sonar-pr3-quality-gate.json`, SHA-256 `164f994006807455abe42da8b2b563eeb4a8032e04287d9a9bc3a5f42a6bbcf7`, exit `1`.
- PR #4 issue/gate receipts: `.codex/runs/20260726T101017Z-mrts-sonarcloud-zero-pr4/sonar-pr-issues.json` and `sonar-quality-gate.json`, SHA-256 `ee8fdf86104a53c760e40f0d42b92b51d2c13f2e289efcb6b562dce9076f6a55` and `1db063f467b49ec05719b0f44b2c703bc402ae52f2515452169ddafbe4343c64`, exit `0`.
- Resulting-main receipts: `.codex/runs/20260726T105800Z-mrts-pr4-squash-merge/github-post-merge.json`, `sonar-main-issues.json`, and `sonar-main-quality-gate.json`, SHA-256 `6d77c474bdc6a8b9744dd3ac8e2b6c76195a47e47fb945caa75acb5173a1f936`, `58cf67de638c7b544b279c8365ac3334eb279716faed0996d6fe439a6ac9ad58`, and `0f88c3322a2a779ea067fcf61cbf21946c614836989b5f5d360f7c04f078e69b`, exit `0`.

## Root cause and remediation boundary

The original PR #3 validator shape triggered Sonar taint rules for local
manifest paths. PR #4 applied the focused repository-native remediation and
test coverage. The exact hosted and resulting-main receipts demonstrate closure
without weakening scanner rules, the Quality Gate, containment, symlink,
remote, Gitlink, or cleanup controls.

## Acceptance, validation, and residual risk

- PR #4 passed Analyze (python), CodeQL, Python 3.14 governance, and
  SonarCloud Code Analysis; it was merged as `615b13bacbd008562c17408246c41ab27dca3104`.
- The retained local validation passed 38 focused tests, Python compileall, and
  `git diff --check`; legitimate controls preserve metacharacter-safe argv,
  `shell=False`, and pre-`Popen` validation failures.
- PR #4 and resulting main report Quality Gate `OK` and zero open
  vulnerabilities, with no forbidden Sonar or security-control shortcut.

Residual risk: future validator changes require fresh exact-head SonarQube
Cloud/GitHub evidence. This archived record does not resolve
`FND-SONAR-0009`. Related findings: `FND-CROSS-0007`,
`FND-FRAMEWORK-0055`, `FND-SONAR-0017`.

## History and final disposition

- `2026-07-24T18:30:00Z` — exact Draft PR #3 Sonar gate failed with seven
  task-owned scanner signals.
- `2026-07-24T18:30:00Z` — static triage found no evidence of a supported
  remote attacker or runtime sink; no source/scanner change was made.
- `2026-07-26T10:10:17Z` through `2026-07-26T10:58:00Z` — PR #4 and resulting
  main receipts established a passing gate and zero vulnerabilities after the
  focused remediation and merge.
- `2026-07-26T17:45:32Z` — current public SonarQube Cloud/GitHub recheck
  confirmed the closed state; the complete triplet is eligible for local
  archival.

Final disposition: `closed_verified_by_merged_mrts_pr4_and_live_sonar_reconciliation_20260726`.
