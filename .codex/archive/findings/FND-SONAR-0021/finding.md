# Finding FND-SONAR-0021: PR #177 inner Sonar S131 issue remediated and verified on master

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `sonarqube_finding` |
| Repository / ownership | `parent` / `parent` |
| Priority | `P2` |
| Security severity / relevance | `not_applicable` / `false` |
| Confidence / status | `confirmed` / `closed` |
| Feasibility | `already_fixed` |
| Release blocker | `false` |
| Candidate-integration blocker | `false` |
| Profile | Historical baseline `d0cd2970-18e5-4a3b-ad84-eb4f91a13855` for `fda62539…`; exact master analysis `a9e18381-2f71-4627-a750-731ceb8dd1c3` for `a1c8394e…` |

## Closed disposition — 2026-07-29T22:41:32Z

PR #177 final head `da4dc5d77c0695182b58b116d55a285156992c15` added the fail-closed default at the actual inner S131 boundary and was integrated by a SHA-bound squash as master `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345`. The resulting master tree equals that exact candidate tree. All fourteen observed master workflows completed successfully.

The latest SonarCloud analysis `a9e18381-2f71-4627-a750-731ceb8dd1c3` records exactly that master revision; the original unresolved `shelldre:S131` query now returns zero issues. The fresh retained evidence is sealed externally (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-postmerge-20260729T223327Z/manifest.md`). No `NOSONAR`, suppression, rule, Quality-Gate, exclusion, bypass, or direct master push was used. The remaining `ERROR` project Quality Gate is only the separately accepted `FND-SONAR-0001` security-rating/hotspot baseline; it is not attributed to this closed S131 finding.

## Historical summary and observed behavior

The retained SonarQube Cloud issue readback reports one OPEN `shelldre:S131`
`CODE_SMELL`, key `AZ7uz_BiBV84XD89pXti`, at
`common/scripts/run_blocked_runtime_smoke.sh:119`.

The exact analyzer message is:

> Add a default case (*) to handle unexpected values.

Sonar labels the rule `CRITICAL` and its maintainability impact `HIGH`. This
local record is nevertheless non-security (`severity: not_applicable`): no
attacker-to-runtime security path is asserted.

The issue response records `lastChangeAnalysisUuid`
`833494ef-5342-4c6e-8bcb-c92cb3e665e0`. Separately, the project-analyses
readback lists `d0cd2970-18e5-4a3b-ad84-eb4f91a13855`, dated
`2026-07-29T20:43:20+0000`, for revision
`fda62539b6f0a710865707e3003b73ed4469f20e`; this record does not claim that
the different UUIDs are identical.

PR #177 candidate `8a95d22db11576d337743c8131af65a08a9449a8` changes only the
outer `case` default at lines 184–194. The confirmed issue targets the
unchanged inner `case` at line 119, so the candidate is blocked from
integration as the claimed S131 remediation.

## Historical expected behavior and impact

The actual inner `case` at the reported location must have an explicit
fail-closed `*)` branch for unexpected values. Focused regression coverage and
the English/German tracking must identify that inner branch, rather than the
outer default, as the S131 remediation.

This is not a release blocker, but it is a candidate-integration blocker. The
candidate cannot truthfully be credited or delivered as the remediation for
`AZ7uz_BiBV84XD89pXti` until the actual inner case is corrected and a fresh
exact-head scan and hosted SonarQube Cloud evidence exist. Do not change a
Sonar rule, Quality Gate, exclusion, `NOSONAR`, suppression, or risk
acceptance.

## Affected scope and preconditions

- Affected file: `common/scripts/run_blocked_runtime_smoke.sh`
- Affected symbol / boundary: inner `case` statement at line `119`
- Candidate comparison: the outer default is at lines `184`–`194` in
  `8a95d22db11576d337743c8131af65a08a9449a8`
- Preconditions: the retained issue query returns the OPEN S131 issue; the
  retained analysis query lists revision `fda62539b6f0a710865707e3003b73ed4469f20e`;
  and the candidate's outer-only change remains distinct from the reported
  inner location.

## Reproduction and evidence

Run ID: `20260729T204320Z-fnd-sonar-0021-blocked-smoke-s131`. The supplied
read-only commands ran from `/root/git/ModSecurity-conector` with exit `0`.
The recorded time is the supplied Sonar analysis date, not a claim of a new
network query during this tracking update.

| Artifact | SHA-256 | Command / result |
| --- | --- | --- |
| `issue.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/evidence/issue.json`) | `854c3a863b37013cbfa4ebc918e650fcbb3a3eefb0d0383f4e5ba79cfe29708e` | `rtk curl -fsS 'https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&rules=shelldre%3AS131&resolved=false&ps=500'`; one OPEN `shelldre:S131` at `common/scripts/run_blocked_runtime_smoke.sh:119`. |
| `analysis.json` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/evidence/analysis.json`) | `462ee987c4213297fa0e0ff1ffa3714e97b14a25ce471e5682ea629cbffaa32a` | `rtk curl -fsS 'https://sonarcloud.io/api/project_analyses/search?project=Easton97-Jens_ModSecurity-conector&ps=3'`; analysis `d0cd2970-18e5-4a3b-ad84-eb4f91a13855` has revision `fda62539b6f0a710865707e3003b73ed4469f20e`. |
| `receipt.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/evidence/receipt.md`) | `9bd53db9f102c827469f81400cccc34117d2e3f390823189e6ab241cf5e601bd` | Bounded command, candidate-comparison, non-duplication, and candidate-integration-blocker receipt. |

The secret-free inventory is sealed in
`manifest.md` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/manifest.md`)
and `SHA256SUMS` (`/var/tmp/codex/ModSecurity-conector/pr-integration-173-182-20260729T121317Z/fnd-sonar-0021-blocked-smoke-s131/SHA256SUMS`).

## Root cause and proposed remediation

The outer-case default recorded in PR #177 is a different control-flow
boundary from the inner case reported by Sonar. The candidate therefore leaves
the actual S131 location default-free and the previous issue-to-remediation
mapping was incomplete.

Add a fail-closed `*)` branch to the actual inner `case`, update focused
regression coverage for that inner unexpected-value path, and align the
English/German tracking. Then obtain a fresh exact-head scan and hosted
SonarQube Cloud evidence. Do not suppress the rule or alter SonarQube Cloud
configuration.

## Acceptance criteria and validation plan

1. The actual inner case reported at
   `common/scripts/run_blocked_runtime_smoke.sh:119` has an explicit
   fail-closed `*)` branch.
2. Focused structural regression coverage asserts the actual inner
   unexpected-value default while valid named inner-case source paths remain
   preserved.
3. The English and German tracking records cite the same issue, location,
   actual remediation branch, and validation limitation.
4. No `NOSONAR`, suppression, rule, Quality-Gate, exclusion, or risk-
   acceptance change is introduced.
5. A fresh exact PR #177 head scan and hosted SonarQube Cloud evidence
   demonstrate the disposition of `AZ7uz_BiBV84XD89pXti` before candidate
   integration is reconsidered.

## Closed disposition, related findings, and residual risk

There are no remaining dependencies or blockers for this closed finding. The focused structural test truthfully asserts the actual inner default; an independent outer-default test and the successful exact-master controls retain the legitimate controlled-skip behavior. The original Sonar reproduction no longer occurs.

Historically, the repair needed a task-owned focused Parent PR #177 change and
fresh exact-head hosted/SonarQube Cloud evidence. Those conditions were met
before the SHA-bound integration and are retained below only as chronology.

- `FND-SONAR-0001` is related current Quality-Gate context, not a duplicate:
  it owns the bounded accepted security-hotspot baseline.
- `FND-SONAR-0016` is related aggregate Draft-PR context, not a duplicate.
- `FND-SONAR-0020` is a separate, now closed event-serializer Cognitive
  Complexity finding, not a duplicate.

No `FND-SONAR-0021`-specific residual integration risk remains. This closure does not broaden, replace, or re-accept `FND-SONAR-0001`.

## History

- `2026-07-29T20:43:20Z` — allocated stable ID `FND-SONAR-0021` after retained
  data confirmed the independently remediable OPEN inner-case S131 issue and
  the PR #177 candidate-integration blocker.
- `2026-07-29T22:19:19Z` — exact PR #177 head `da4dc5d…` fixed the actual inner-case default, passed the complete sealed Security Diff Scan and exact-head hosted SonarCloud evidence.
- `2026-07-29T22:41:32Z` — resulting master `a1c8394e…` was confirmed tree-identical to `da4dc5d…`; fourteen master workflows passed, the latest SonarCloud analysis bound to that SHA, and the original unresolved S131 query returned zero. Status is therefore `closed`.

## Current reconciliation confirmation — 2026-08-01

[PR #177](https://github.com/Easton97-Jens/ModSecurity-conector/pull/177)
merged normally as `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345`, reachable from
current `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c`. Current
SonarCloud API readback for `AZ7uz_BiBV84XD89pXti` remains `CLOSED` / `FIXED`;
the current inner case retains its default branch and the exact PR checks
report 33 passed and 0 failed.
