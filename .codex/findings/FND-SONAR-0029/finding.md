# Finding FND-SONAR-0029: Common scripts contain twenty-seven current SonarQube Cloud findings

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `sonarqube_finding` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P1` / `medium` / `confirmed` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / candidate integration blocker / security relevant | no / no / yes |
| Sonar inventory | 15 Security and 12 Maintainability rows; no component duplicate block. |

## Summary and scope

The retained current-master receipt binds the `common/scripts/` inventory to
Parent revision `6b4aca18d390363764b96d85cd31969b9bb114a1`. It records 27
current rows in the three named sources. Remediation is confined to local
smoke protocol/input boundaries, lifecycle decomposition, C++17 RAII cleanup,
direct tests, and paired Change Records. Sonar policy, suppression, exclusion,
`NOSONAR`, workflow, Framework/MRTS, Gitlink, and master changes are excluded.

## Current disposition

Earlier resulting-master evidence retained OPEN `pythonsecurity:S8705` issue
`AZ7z-HdL4L5Jot4fEMXc` at `common/scripts/run_local_runtime_smoke.py:1551`.
GitHub normal-merged [PR #221](https://github.com/Easton97-Jens/ModSecurity-conector/pull/221)
at exact reviewed head `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d`, producing
Parent master `3270ab5bdcc86ddab50e9be00db7611aae7fd937` at
`2026-08-01T13:36:33Z`. All 14 push workflows for that exact master revision
completed successfully. The direct resulting-master SonarQube Cloud recheck at
`2026-08-01T13:39:56Z` reports original issue
`AZ7z-HdL4L5Jot4fEMXc` as `FIXED/CLOSED` at `2026-08-01T13:37:19Z`.

The finding is `verified`. The separate project-wide `FND-SONAR-0001`
new-security-rating baseline keeps the master Quality Gate at `ERROR`; no
scanner or security control was weakened or changed.

## Retained evidence

- Scoped Sonar inventory (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/evidence/sonar-inventory.md`)
- Sealed security-diff review (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/security-diff-scan/report.md`)
- Terminal sealed security-diff review (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/security-diff-scan-terminal-amendment/report.md`)
- Resulting-master SonarQube Cloud receipt (`/var/tmp/codex/ModSecurity-conector/runs/common-scripts-sonar-remediation-20260801/evidence/post-merge-master-sonar-20260801.md`)
- PR #221 exact-head verification (`/root/git/ModSecurity-conector/.codex/runs/parent-common-sonar-remediation-20260801/evidence/pr221-exact-head-verification.md`)
- PR #221 merge/master verification (`/root/git/ModSecurity-conector/.codex/runs/parent-common-sonar-remediation-20260801/evidence/pr221-merge-master-verification.md`)

## History

- `2026-08-01T10:40:00Z`: finding allocated from the current, revision-bound
  scope receipt; no commit, PR, merge, scanner-control, or master change
  existed at allocation.
- `2026-08-01T10:54:10Z`: the initial Draft PR #218 Sonar readback had 12
  task-owned rows and 0.0% New-Code duplication. The local amendment has 56
  passing focused tests, a C++17 compile control, and a second sealed security
  review; fresh amended-head hosted evidence is pending.
- `2026-08-01T11:16:50Z`: exact-head SonarQube Cloud returns zero open rows,
  Quality Gate `OK`, zero new violations, and 0.0% New-Code duplication; all
  applicable GitHub checks succeeded. The finding is `fixed`; no merge was
  authorized or performed.
- `2026-08-01T11:36:41Z`: PR #218 was merged as
  `a7e2e70f307c91bc3da702b7240a1c4218cb2b79` and all 14 resulting-master
  workflows succeeded. The direct resulting-master SonarQube Cloud query
  retains pre-existing OPEN `pythonsecurity:S8705`
  `AZ7z-HdL4L5Jot4fEMXc` at line 1551. Static review has not established a
  supported HTTP-to-CLI boundary, so the candidate is `triaged` rather than
  accepted, fixed, verified, or closed.
- `2026-08-01T13:12:18Z`: exact Draft PR #221 head
  `482ba035ed53b3668009b7158c656214d6924e6f` verifies private regular
  evaluator inputs, rejects unsafe linker/ownership cases before process
  creation, and directly links the verified selected library file. Applicable
  hosted checks passed; SonarQube Cloud reports zero open PR issues, zero new
  violations, and `0.0%` New-Code duplication; the complete security-diff
  review has zero reportable findings. The finding is `fixed`, pending an
  authorized merge and resulting-master reproduction before `verified` or
  `closed`.
- `2026-08-01T13:39:56Z`: GitHub normal-merged exact PR #221 head
  `dcfc64044d0f34b852a1b5cbc0cecd66cf6d1f9d` as resulting master
  `3270ab5bdcc86ddab50e9be00db7611aae7fd937`; all 14 exact-master workflows
  succeeded. The direct SonarQube Cloud recheck records original
  `AZ7z-HdL4L5Jot4fEMXc` / `pythonsecurity:S8705` as `FIXED/CLOSED` at
  `2026-08-01T13:37:19Z`. The finding is `verified`; `FND-SONAR-0001` remains
  separate.
