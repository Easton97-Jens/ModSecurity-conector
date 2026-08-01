# FND-SONAR-0002 — Framework SonarQube quality-gate failure is verified resolved on current master

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-SONAR-0002` |
| Title / Titel | `Framework SonarQube quality-gate failure is verified resolved on current master` |
| Category / Kategorie | `sonarqube_finding` |
| Repository / Repository | `framework` |
| Ownership / Ownership | `sonarqube_configuration` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `verified` — current Framework master `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6` has a revision-bound SonarCloud analysis with Quality Gate `OK` and zero current leak-period open issues; the historical failed-master observations remain retained below |
| Feasibility | `already_fixed` — the current external gate condition is observed passing; this record remains `verified`, not `closed` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

### Current audit reassessment — 2026-07-26T12:12:27Z

The exact current Framework master `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6`
has SonarCloud analysis `2b78d1c9-9a3c-4497-a076-74c468eff0d8`. Its Quality
Gate is `OK`: all five conditions pass, new duplication is `0.0`, and the
current leak-period open-issue query returns zero. This rechecks the original
master-gate failure and its legitimate controls; it makes no causal claim about
which intervening Framework or MRTS change caused the result. No Parent,
Framework, or MRTS source/Git/Gitlink action is performed by this audit.

Direct GitHub and SonarQube Cloud evidence confirms that Framework masters
`9954b99a31fab0006cdf903ab477c8158c50fea8`,
`36cac3029c735dddf9f717b3ce077b9285567a6a`,
`9a729226d2e040d07d7e7a4acebf201faf06ab37`, PR #34 merge result
`3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`, PR #30 merge result
`efdbcbd98afeed0f39f8912ce1140aaa5742f507`, and PR #35 merge result
`4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` have failed SonarQube Cloud
Quality Gates. At that historical PR #35 reassessment, master
`4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` failed solely on New Security
Rating E (actual value `5`, threshold `1`);
reliability and maintainability are A (actual value `1`), duplication is `0.0`,
and hotspot review is `100.0`. All six exact-master GitHub Actions workflows
passed. The live Sonar inventory has 14 open vulnerability signals: five in
Framework-owned paths and nine below read-only `tools/MRTS/`. The inventory
does not validate any individual scanner signal as a vulnerability and does not
causally attribute the pre-existing multi-file backlog to PR #35. The historical
acceptance scope does not extend to PRs #30, #33, #34, #35, or #36.

### Current reassessment after PR #37

PR #37 source `1e9fa0d22639517193d450b05eb7b07193e41257` was normally merged
as current Framework master `f73f8842f45318e2df8aff1d31855eeb7c20a22f`.
All applicable master Actions and CodeQL checks passed, but SonarCloud failed
solely on New Security Rating C (actual `3`, threshold `1`). Reliability and
maintainability are A, duplication is `0.0`, and hotspot review is `100.0`.
The current inventory contains nine open signals, all below unchanged read-only
`tools/MRTS/` and created before PR #37. Static claim-specific triage finds
CLI/YAML-driven file/process sinks but no established untrusted Framework
invocation, so all nine are `needs_review`, not confirmed vulnerabilities or
false positives. PR #37 did not change the MRTS gitlink; its historical
PR #36-only risk acceptance is historical.  A separate current bounded
acceptance now applies only to protected PR #42 integration and does not change
the global lifecycle of this finding.

### Current reassessment after PR #43

PR #43 exact head `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` was normally
merged as Framework master `f98a8739cb13b583f23d646784b144e596b61441`.
Exact analysis `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` is terminal `ERROR`
solely on New Security Rating C (actual `3`, threshold `1`), with nine open
read-only MRTS vulnerability signals. Reliability and Maintainability are A,
duplication is `0.0`, hotspot review is `100.0`, and the four applicable
master workflows passed. The same analysis has zero open `python:S3415` issues.
No causal attribution to PR #43 is made. The historical PR #42 acceptance
remains unchanged. On 2026-07-24 the user separately accepted this documented
master-only residual only for normal exact-head-protected PR #44 delivery; the
global finding remains blocked.

### Current reassessment after PR #45

PR #45 exact head `dd7e221d903a7e2e0a59af203ba312dfca55d69c` was normally
merged with exact-head protection as Framework master
`7e9a560f3acda65510c93f649b6ed4977e4cd6cb`. The merge tree equals the
reviewed PR-head tree. CodeQL Actions/C++/Python, current-revision advisory,
common-structure, and scaffold-lint passed; the PR-only head job was
intentionally skipped on the master trigger. SonarCloud Check Run
`89757305894` failed solely on New Security Rating C (actual `3`, threshold
`1`). The current leak-period inventory has 19 open/confirmed records: nine
VULNERABILITY records under read-only `tools/MRTS/` and ten CODE_SMELL records.
The security keys are the same nine already tracked by this finding. PR #45
changes no `tools/MRTS/` path, so the evidence makes no causal attribution to
this delivery. No current user risk acceptance covers PR #45; the global
finding remains blocked and a release blocker.

### Current reassessment at the PR #47 integration gate

The exact Framework PR #47 head `cb0b810e0770a0a4d10fa5bb08031e70ac9ad9a7`
passes its separate SonarQube Cloud Quality Gate with zero bugs,
vulnerabilities, code smells, and open PR issues; all current PR checks,
including both lint triggers, pass. Before a normal merge, the current Framework
master `c27c644e088904b71b8380d16ee34f1b36f2c001` was rechecked and still
returns Quality Gate `ERROR` solely on New Security Rating C (actual `3`,
threshold `1`); reliability, maintainability, duplication, and hotspot-review
conditions pass. PR #47 has no `tools/MRTS` gitlink diff, so this does not
establish PR causality. Historical bounded acceptances apply only to the PRs
they name and do not authorize PR #47. The normal merge is therefore pending a
fresh, explicit user decision; no draft-state change or merge was performed.

### Current-user bounded acceptance for PR #47

After this exact residual was presented, the current user directed “bringe pr
47 in den master.” This accepts only the documented master-only New Security
Rating C condition for a normal, exact-head-protected Framework PR #47 merge.
Fresh PR-head checks, Sonar evidence, review/rules checks, and the normal merge
method remain mandatory. It does not authorize Parent or MRTS action, a direct
push or bypass, suppression, a scanner or Quality-Gate change, finding closure,
or any later PR/release waiver.

### Verification after the accepted PR #47 merge

PR #47 was normally merged at `2026-07-26T11:26:19Z` as
`bcb5b69f135c8b38b834e00e47b0369ae3bdb670`. Its parents are the reviewed
base `c27c644…` and exact PR head `cb0b810…`; the merge tree equals the
reviewed head tree. All resulting-master workflows bound to that commit passed,
including CodeQL, lint, CI-security checks, common structure, OpenSSF, and the
new updater’s read-only Framework validation. SonarCloud bound its analysis to
that exact commit and failed solely on the accepted New Security Rating C
condition. This consumes only the PR-#47 delivery acceptance; it does not close
the global finding.

After that verification, the updater created Draft PR #49. GitHub’s event log
attributes its later ready-for-review and merge events to the `Easton97-Jens`
account, not GitHub Actions or this session, advancing master to `ab7374…`.
That subsequent PR is outside this task and is neither attributed to PR #47
nor validated here.

## Observed behavior / Beobachtetes Verhalten

Earlier analysis `2ab6b2fe-32b1-486c-9b1d-bf5a66ee21e3` recorded 361 visible new-code issues, Security E and Reliability D on the prior master revision. After PR #25, exact master `9954b99a31fab0006cdf903ab477c8158c50fea8` again failed SonarCloud while lint, test-common/common-structure, and CodeQL succeeded. After the authorized PR #26 squash merge, exact master `36cac3029c735dddf9f717b3ce077b9285567a6a` again failed with Security E and Reliability D while CodeQL, common structure, and scaffold lint succeeded. After PR #34's normal merge, exact master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` again failed while its Actions/CodeQL workflows succeeded and its exact PR head Quality Gate passed. After PR #30 was normally merged at `2026-07-20T07:30:40Z`, exact master `efdbcbd98afeed0f39f8912ce1140aaa5742f507` failed SonarQube Cloud Check Run `88295589868` at `2026-07-20T07:31:35Z` solely on New Security Rating E (actual `5`); its New Reliability Rating is A (actual `1`). All six resulting-master GitHub Actions workflows succeeded.

After PR #35 was normally merged at `2026-07-20T11:57:54Z`, the exact master
`4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` again returned Quality Gate
`ERROR` at `2026-07-20T12:03:31Z`, solely because `new_security_rating` was
`5` against a threshold of `1`. Reliability and maintainability were A,
duplication was `0.0`, hotspot review was `100.0`, and all six exact-master
GitHub Actions workflows passed. The public issue inventory reported 14 open
Sonar vulnerability signals: five Framework-owned and nine under read-only
MRTS. The prior master already had Security E, so this evidence neither
causally attributes the backlog to PR #35 nor turns scanner signals into
confirmed vulnerabilities. No Parent or MRTS change occurred.

After PR #45 was normally merged at `2026-07-26T04:53:10Z`, exact Framework
master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb` has a merge tree identical
to its reviewed head `dd7e221d903a7e2e0a59af203ba312dfca55d69c`. Applicable
resulting-master GitHub checks passed, while SonarCloud failed solely on New
Security Rating C (actual `3`, threshold `1`). The public leak-period inventory
contains 19 open/confirmed records: nine VULNERABILITY records below read-only
MRTS and ten CODE_SMELL records. The nine security keys match the existing
FND-SONAR-0002 inputs. Because PR #45 changes no `tools/MRTS/` path, this
observation does not causally attribute the condition to the PR. No PR-#45-
specific user risk acceptance was requested, inferred, or used.

## Expected behavior / Erwartetes Verhalten

The exact current Framework head passes the Quality Gate and the current
leak-period query is empty. This satisfies the verification criterion for the
historical master-gate failure. This record stays `verified`, rather than
`closed`, so later gate regressions must be independently reassessed; historic
bounded acceptances do not waive future conditions.

## Impact / Auswirkung

The historical default-branch gate failure is no longer a current P1 release
blocker: exact master `a7ebf5a…` now passes with zero current leak-period open
issues. This audit does not weaken a scanner or Quality Gate, suppress an
issue, change Parent/Framework/MRTS source or delivery state, or authorize a
future release waiver.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`
- `tests/runners/synchronized_upstream.py:355`
- `ci/reporting/generate-connector-work-queue.py:486`
- `ci/checks/catalog/no_crs_baseline.py:1746` (`python:S5443` signal)
- `ci/reporting/update-runtime-snapshot.py:72` (`pythonsecurity:S8707` and `pythonsecurity:S2083` signals)
- `tests/runners/runner_core.py:636` (`pythonsecurity:S2083` signal)
- `tests/runners/case_cli.py:424` (`pythonsecurity:S2083` signal)
- `tools/MRTS/mrts/generate-rules.py:428,444`
- `tools/MRTS/mrts/mrts.py:13,14,30,53,73,83`

### Symbols / Symbole

- `Sonar check 87720680094`
- `Security Rating E`
- `Reliability Rating D`
- `Reliability Rating A on efdbcbd98afeed0f39f8912ce1140aaa5742f507`
- `Sonar check 88295589868`
- `Security Rating E on 4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5`
- `14 open Sonar vulnerability signals (5 Framework-owned; 9 MRTS)`
- `Security Rating C on f73f8842f45318e2df8aff1d31855eeb7c20a22f`
- `Sonar check 89757305894`
- `Security Rating C on 7e9a560f3acda65510c93f649b6ed4977e4cd6cb`
- `19 current leak-period issues (9 VULNERABILITY; 10 CODE_SMELL)`
- Nine current read-only MRTS issue keys `AZ84XDED2YUGB8FZMhlm`,
  `AZ84XDED2YUGB8FZMhln`, `AZ84XDDw2YUGB8FZMhle`, `AZ84XDDw2YUGB8FZMhlb`,
  `AZ84XDDw2YUGB8FZMhlY`, `AZ84XDDw2YUGB8FZMhlc`, `AZ84XDDw2YUGB8FZMhlZ`,
  `AZ84XDDw2YUGB8FZMhld`, and `AZ84XDDw2YUGB8FZMhla`
- `analysis 2ab6b2fe-32b1-486c-9b1d-bf5a66ee21e3`
- `python:S5779`
- `python:S3923`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.
- SonarQube Cloud public API and GitHub check decoration remain readable for the exact current Framework SHA.

## Reproduction / Reproduktion

- `sed -n '187,196p;212,215p' .codex/reports/repository-full-assessment.md`
- Query current exact-master Actions, Sonar project status, and issue inventory
  for Framework master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb`.

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:187-196,212-215`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '187,196p;212,215p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/sonar-quality-gate-current.md`
  - Type: `current_sonarqube_cloud_gate_inventory`; SHA-256: `659ef53f520c6d62a17d9b5860babdf183cd849baa057c7239d02b636c3bf418`
  - Command: `rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-test-Framework&branch=master'`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-18T09:20:00Z`; retention: `retained_task_evidence`
- Run ID: `20260718T081746Z-framework-common-structure-d6ee7cec`
  - Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260718T081746Z-framework-common-structure-d6ee7cec/evidence/pr-23-current.md`
  - Type: `pr_new_code_sonar_gate_disposition`; SHA-256: `c28444cfdd989b9884e367f17e0540ccda9858a3bc10b24b26dd8293b500855d`
  - Command: read-only PR check rollup and thread inspection through RTK
  - Working directory: `/var/tmp/codex/worktrees/framework-common-structure`; exit code: `0`
  - Observed at: `2026-07-18T09:58:40Z`; retention: `retained_task_evidence`
- Run ID: `20260720T042405Z-framework-pr-34-master-integration-31a1528d`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T042405Z-framework-pr-34-master-integration-31a1528d/evidence/master-postmerge-verification.md`
  - Type: `exact_framework_master_sonar_failure_after_pr34_merge`; SHA-256:
    `7471054c232a5e2ad26c3327894535ff9d2245e3ec0f37ec60e077a57caea19a`
  - Exact master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` failed the
    SonarQube Cloud check with Reliability D (actual 4) and Security E
    (actual 5), while its exact PR #34 head passed the separate Quality Gate.
- Run ID: `framework-pr-30-master-sonar-20260720T073135Z`
  - Artifact: GitHub check-runs API for
    `efdbcbd98afeed0f39f8912ce1140aaa5742f507` and the public SonarQube Cloud
    `project_status` endpoint for branch `master`; no local copy was retained.
  - Type: `external_sonarqube_cloud_current_master_gate_reassessment`;
    SHA-256: `not_retained_external_api_readback`
  - Command: `rtk proxy gh api repos/Easton97-Jens/ModSecurity-test-Framework/commits/efdbcbd98afeed0f39f8912ce1140aaa5742f507/check-runs --paginate`; `rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/qualitygates/project_status?projectKey=Easton97-Jens_ModSecurity-test-Framework&branch=master'`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-20T07:31:35Z`; retention:
    `not_retained_external_api_readback`
  - Exact master `efdbcbd98afeed0f39f8912ce1140aaa5742f507` failed Check Run
    `88295589868` solely on New Security Rating E (actual `5`); Reliability is
    A (actual `1`), and all six resulting-master GitHub Actions workflows
    succeeded. The preceding PR #34 master already failed with Security E, so
    no causal attribution to PR #30 is made.
- Run ID: `20260720T113905Z-framework-pr35-36-integration-de98515c`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260720T113905Z-framework-pr35-36-integration-de98515c/analysis/master-sonar-after-pr35.json`
  - Type: `exact_framework_master_sonar_reassessment_after_pr35_merge`;
    SHA-256: `7b62f2b918059d816fcfccafcbff16fdd6e1f92d33191862c406d22d414df988`
  - Command: GitHub exact-master ref/workflow readback and public SonarQube
    Cloud project-status and issue-inventory endpoints through RTK.
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-20T12:03:31Z`; retention:
    `retained_task_evidence`
  - Exact master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` has a Quality Gate
    `ERROR` solely on Security E (actual `5`), while six Actions workflows,
    reliability, maintainability, duplication, and hotspot review pass. The
    inventory has 14 untriaged vulnerability signals (five Framework-owned,
    nine MRTS); it establishes no individual vulnerability or PR #35 causality.
- Run ID: `20260721T060210Z-framework-pr-37-master-integration-6be553a4`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260721T060210Z-framework-pr-37-master-integration-6be553a4/analysis/postmerge-master-sonar-triage.md`
  - Type: `exact_framework_master_sonar_reassessment_and_read_only_mrts_claim_triage_after_pr37_merge`; SHA-256:
    `a9a312f1ba760030ceb45644ced6b0d533fe01b9a4d2f8e19c1e832dc54b5830`.
  - Exact master `f73f8842f45318e2df8aff1d31855eeb7c20a22f` failed solely on
    Security C (actual `3`, threshold `1`) while applicable Actions/CodeQL
  checks passed. All nine current gate-driving signals are unchanged
  read-only MRTS inputs, predate PR #37, and are `needs_review` after static
  source/control/sink triage; no PR #37 causality or risk acceptance exists.
- Run ID: `20260726T050327Z-framework-pr45-master-integration`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T050327Z-framework-pr45-master-integration/evidence/postmerge-master-verification.md`
  - Type: `framework_pr45_resulting_master_verification_and_sonar_reassessment`;
    SHA-256: `21a8bb0c5cf83ac6ca0156d3285e5829ca1d871754dc9019516844ef9c94695d`
  - Command: RTK GitHub PR/ref/tree/compare/check-run reads and public
    SonarQube Cloud Quality Gate and leak-period issue-inventory queries after
    the normal exact-head-protected PR #45 merge.
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-26T05:03:27Z`; retention:
    `sealed_local_evidence`
  - Exact master `7e9a560f3acda65510c93f649b6ed4977e4cd6cb` has the same tree
    as reviewed head `dd7e221d903a7e2e0a59af203ba312dfca55d69c`. Applicable
    master checks pass; SonarCloud fails solely on Security C (actual `3`,
    threshold `1`). The current inventory has 19 open/confirmed records: the
    same nine MRTS VULNERABILITY signals and ten CODE_SMELL records. No
    PR-#45-specific risk acceptance was used.
- Run ID: `20260726T051835Z-framework-pr45-boundary-snapshot`
  - Artifact:
    `/var/tmp/codex/ModSecurity-conector/runs/20260726T051835Z-framework-pr45-boundary-snapshot/evidence/final-boundary-snapshot.md`
  - Type: `framework_pr45_final_parent_framework_mrts_boundary_snapshot`;
    SHA-256: `07da9852d035d0be72a3260258d0d05b350d7a1b1e49c5acd7e6f229f39b13d9`
  - Command: RTK read-only Parent/Framework/MRTS status, gitlink, commit,
    diff-stat, path, and mtime reads after the PR #45 merge.
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-26T05:18:35Z`; retention:
    `sealed_local_evidence`
  - Parent's gitlink and embedded/MRTS commits were not changed by the task.
    The snapshot preserves three unattributed dirty MRTS working-tree paths;
    no task command wrote, restored, staged, committed, pushed, or attributed
    them.

## Root-cause analysis / Grundursachenanalyse

The quality gate is a pre-existing external SonarQube Cloud multi-file backlog.
The current leak-period inventory has nine gate-driving VULNERABILITY claims
below read-only MRTS and ten additional CODE_SMELL records. The security claims
have CLI/YAML-derived file/process sinks, but current Framework evidence does
not establish an untrusted caller. PR #45 changes no `tools/MRTS/` path, so no
causal link to that delivery is established.

## Proposed remediation / Vorgeschlagene Remediation

Triage each gate-driving security/reliability issue with claim-specific source/control/sink evidence, remediate only separately authorized confirmed items, and rerun the current Framework gate without suppression, exclusion, or Quality Gate weakening.

## Acceptance criteria / Akzeptanzkriterien

- The Framework current gate passes or every remaining item has a current authorized disposition.
- Directly sourced issue detail is retained without original MRTS traversal.
- The current task's common-structure patch remains causally separate from Sonar remediation.

## Validation plan / Validierungsplan

- Verify the exact current SHA and retain the current gate result.
- Triage the visible current security/reliability inputs before treating scanner signals as confirmed vulnerabilities.
- Rerun the Quality Gate on a separately authorized remediation head.

## Regression tests / Regressionstests

- Add a claim-specific regression only after a validated individual Sonar finding is selected for remediation.

## Legitimate control tests / Legitime Kontrolltests

- Preserve passing maintainability, duplication, and hotspot-review gate conditions while remediating a selected issue.

## Dependencies / Abhängigkeiten

- `FND-FRAMEWORK-0001` common-structure repair is separate and cannot remediate this Quality Gate backlog.

## Blockers / Blocker

- No current blocker is observed for this historical Quality-Gate failure.
  Future non-OK analyses or non-empty leak-period results require a fresh
  reassessment; this verification does not close unrelated MRTS or GitHub
  findings.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0001`
- `FND-CROSS-0005`

## Residual risk / Restrisiko

The observed passing state is current only at exact master `a7ebf5a…` and its
bound analysis `2b78d1c9-9a3c-4497-a076-74c468eff0d8`; a later external change
can reintroduce a gate failure. The audit does not classify historic scanner
signals as false positives or attribute their disappearance to a particular
change. Unrelated open findings retain their own status and acceptance criteria.

## History / Historie

- `2026-07-26T12:12:27Z`: current_master_quality_gate_verified — Exact
  Framework master `a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6` has bound
  SonarCloud analysis `2b78d1c9-9a3c-4497-a076-74c468eff0d8` with Quality Gate
  `OK`, all five conditions passing, `0.0` new duplication, and zero current
  leak-period open issues. This reruns the original master-gate outcome and
  legitimate controls, so the finding is `verified` / `already_fixed` and no
  longer a release blocker. The audit makes no causal attribution and performs
  no Parent, Framework, or MRTS source, Git, or Gitlink action.

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-18T09:27:57Z`: current_task_direct_sonar_inventory — Direct current-SHA gate/issue evidence was retained. The gate is confirmed independent of common-structure; its multi-file remediation is not mixed into that patch.
- `2026-07-18T09:58:40Z`: pr_new_code_gate_distinguished — Exact Draft PR #23 head passed SonarCloud with zero new issues/hotspots. This does not remediate the default-branch E/D backlog, but proves it does not block the PR's verified status.
- `2026-07-19T09:52:00Z`: current_master_gate_reconfirmed_after_pr25_merge —
  Framework master `9954b99a31fab0006cdf903ab477c8158c50fea8` again has a
  failed SonarCloud Code Analysis check while lint, test-common/common-
  structure, and CodeQL are successful. The retained post-merge receipt
  SHA-256 is `fdda0551354ccc8cb28794a1f7ca8e35f6aa333a9d6272743e15e7e12aacca34`.
  The receipt does not establish that the NGINX provenance merge caused the
  existing multi-file backlog; the finding remains independently `blocked`.
- `2026-07-20T07:31:35Z`: master_sonar_reassessed_after_pr30_merge_scope_not_extended — Exact Framework master `efdbcbd98afeed0f39f8912ce1140aaa5742f507` failed Check Run `88295589868` solely on New Security Rating E (actual `5`); Reliability is A (actual `1`). PR #30's exact head and all six resulting-master GitHub Actions workflows passed. The preceding master already failed Security E, so the evidence makes no causal attribution to PR #30 and does not extend the historical acceptance.
- `2026-07-20T12:03:31Z`: master_sonar_reassessed_after_pr35_merge_scope_not_extended — Exact Framework master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` returned Quality Gate `ERROR` solely on New Security Rating E (actual `5`); Reliability and Maintainability were A, duplication was `0.0`, hotspot review was `100.0`, and six exact-master Actions workflows passed. The public inventory has 14 untriaged vulnerability signals (five Framework-owned and nine MRTS). The preceding master already had Security E, so no causal attribution to PR #35 is made and the historical acceptance is not extended.
- `2026-07-20T12:50:36Z`: current_user_bounded_risk_acceptance_for_pr36_master_integration — After the exact master-only Sonar result was presented, the user directly instructed integration of PR #36. The retained acceptance explicitly covers only protected Framework PR #36 integration after normal refresh and fresh exact-head controls; it does not waive PR-head Sonar, other gates, Parent, MRTS, a direct push/bypass, or the general FND-SONAR-0002 release blocker.
- `2026-07-21T07:28:49Z`: master_sonar_reassessed_after_pr37_merge_and_mrts_inputs_triaged — exact PR #37 source `1e9fa0d…` merged normally as master `f73f884…`; exact-head Sonar and resulting-master Actions/CodeQL passed, but master Sonar failed solely on Security C. The nine pre-existing unchanged MRTS inputs are `needs_review`; no PR #37 causality, MRTS action, suppression, or current risk acceptance is claimed.
- `2026-07-23T07:01:16Z`: current_user_bounded_risk_acceptance_for_pr42_master_integration — the current user explicitly directed that `FND-SONAR-0002` be left out while PR #42 is integrated. Fresh master evidence still reports only Security C (`3` versus threshold `1`) and the same nine `needs_review` read-only MRTS signals. The acceptance is limited to protected PR #42 delivery and waives no PR-head gate, Cloudflare disposition, merge-method choice, Parent/MRTS action, direct push/bypass, control change, future condition, or finding closure.
- `2026-07-23T11:25:34Z`: master_sonar_reassessed_after_pr43_merge_scope_not_extended — exact PR #43 source `4c55bb2…` merged normally as Framework master `f98a873…`. Exact master analysis `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` failed solely on Security C (actual `3`, threshold `1`) while the four applicable master Actions workflows passed. The inventory has nine read-only MRTS vulnerability signals and zero `python:S3415` issues. No causal attribution to PR #43 is made, and the PR-#42-only acceptance is not extended.
- `2026-07-24T03:56:04Z`: current_user_bounded_risk_acceptance_for_pr44_master_integration — after the exact current master-only Sonar result and the fully reviewed Framework PR #44 state were presented, the user replied “ja” directly to the precise acceptance request. Fresh PR #44 head `3b67efb…` remains green with no reviews or threads; current master `f98a873…` still fails solely on Security C (`3` versus threshold `1`) and the public API reports nine open vulnerability signals. The acceptance permits only normal exact-head-protected PR #44 delivery; it does not waive controls, Parent/MRTS boundaries, later conditions, or finding closure.
- `2026-07-24T04:16:09Z`: protected_pr44_integration_completed_master_sonar_reassessed_under_bounded_acceptance — PR #44 exact head `3b67efb…` normally merged with exact-head protection as Framework master `4c975329…`; its tree equals the reviewed head. Resulting-master CodeQL, advisory, common-structure, and lint controls passed, while SonarCloud failed solely on the same Security C (`3` versus `1`) condition and the inventory remains nine `needs_review` read-only MRTS signals. The bounded acceptance was used only for this result; no finding closure, false-positive claim, Parent, or MRTS action occurred.
- `2026-07-26T05:03:27Z`: master_sonar_reassessed_after_pr45_merge_scope_not_extended — PR #45 exact head `dd7e221…` normally merged with exact-head protection as Framework master `7e9a560…`; its tree equals the reviewed head. CodeQL, advisory, common-structure, and scaffold-lint passed, while SonarCloud Check Run `89757305894` failed solely on Security C (`3` versus `1`). The current leak-period inventory has 19 open/confirmed records, including the same nine read-only MRTS VULNERABILITY signals and ten CODE_SMELL records. PR #45 changes no `tools/MRTS/` path, so no causal attribution is made. No PR-#45-specific risk acceptance was requested, inferred, or used; no task-authored Parent/MRTS Gitlink or commit action occurred and the global finding stays blocked.
- `2026-07-26T05:18:35Z`: final_boundary_snapshot_preserves_unattributed_mrts_worktree_state — a read-only final snapshot confirms that the Parent-recorded Framework gitlink, embedded Framework commit, and MRTS commit were not changed by this task. It preserves three unattributed dirty MRTS working-tree paths without restoring, staging, committing, pushing, merging, or attributing them. This does not alter the PR #45 merge result or FND-SONAR-0002 lifecycle.

## Current-user reconciliation-only risk acceptance

At `2026-07-19T12:34:25Z`, the current user explicitly instructed Codex that
the failed **Framework master** `SonarCloud Code Analysis` may be ignored while
correcting PRs #24, #26, #27, and #29 to preserve the NGINX provenance control.
The immutable acceptance artifact is
`/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/analysis/sonar-master-risk-acceptance.md`
with SHA-256
`109222be8968799f2fef2fa59c7172e2cf57cee3077446bc5472261664133679`.

The separate current user integration instruction then authorized the named
Framework PRs for conditional exact-head PR delivery; it did not weaken this
acceptance. The resulting master `36cac3029c735dddf9f717b3ce077b9285567a6a`
was re-evaluated in retained receipt
`fnd-sonar-0002-36cac-master-reassessment.md`, SHA-256
`e548fde741694abca18528f4836f68f1dfcd52e76d2dd45f2b8500ec68829ddf`.

This narrowly accepts the residual risk that the known default-branch
security/reliability backlog could contain genuine unresolved defects on the
resulting masters of this one sequential reconciliation. It does not accept,
suppress, or bypass a SonarCloud result for a new exact PR head; any other CI,
review, security, documentation, conflict, or exact-head requirement; a direct
master push; Parent-gitlink delivery; or an MRTS change. Reassess the
disposition if the master gate meaningfully changes or the requested scope
changes. Separate authorized Sonar triage/remediation remains required.

## Reassessment after PR #26

- `2026-07-19T14:46:13Z`: exact Framework master
  `36cac3029c735dddf9f717b3ce077b9285567a6a` failed SonarCloud Check Run
  `88203518811` with Security E and Reliability D while CodeQL, common-
  structure, and scaffold-lint succeeded.
- The current Framework-only sequential scope retains only this master-only
  residual risk. Fresh PR-head Sonar gates and every other control remain
  mandatory.

## Reassessment after PR #33

- `2026-07-19T22:18:45Z`: exact Framework master
  `9a729226d2e040d07d7e7a4acebf201faf06ab37` has a completed failed
  SonarCloud Code Analysis check. The public Quality Gate reports New
  Reliability D (actual `4`) and New Security E (actual `5`), while new
  duplication is `0.4` and hotspot review is `100.0`.
- PR #33's exact head passed its separate SonarQube Cloud Quality Gate, and
  the resulting master Actions/CodeQL controls passed. The master backlog is
  not attributed to the Python-3.13 repair.
- The retained acceptance is expressly limited to PRs #24, #26, #27, and #29.
  It is not automatically extended to PR #33; no source, scanner, quality-gate,
  Parent, or MRTS control was weakened.

## Reassessment after PR #34

- `2026-07-20T04:52:04Z`: exact Framework master
  `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` again failed SonarQube Cloud.
  The public gate reports New Reliability D (actual `4`) and New Security E
  (actual `5`), while new duplication is `0.4` and hotspot review is `100.0`.
- PR #34's exact head passed its separate Quality Gate, and resulting-master
  Actions/CodeQL controls passed. The master backlog is not attributed to the
  Phase-4 workload-identity remediation.
- The stored user acceptance names only PRs #24, #26, #27, and #29. It is not
  automatically extended to PR #34, so this finding is `blocked` for current
  master-integration verification without a new user decision or separately
  authorized SonarQube Cloud remediation.

## Reassessment after PR #30

- `2026-07-20T07:31:35Z`: after PR #30 was normally merged at
  `2026-07-20T07:30:40Z`, exact Framework master
  `efdbcbd98afeed0f39f8912ce1140aaa5742f507` failed SonarQube Cloud Check Run
  `88295589868` solely on New Security Rating E (actual `5`). New Reliability
  Rating is A (actual `1`); duplication and hotspot-review conditions pass.
- PR #30's exact head passed its separate Quality Gate, and all six
  resulting-master GitHub Actions workflows succeeded. The immediately
  preceding PR #34 master already had Security E, so this observation does not
  establish a causal attribution to PR #30. No Parent or MRTS change occurred.
- The stored user acceptance remains limited to PRs #24, #26, #27, and #29. It
  is not automatically extended to PR #30, so this finding remains `blocked`
  for current PR #30 master-integration verification without a new user
  decision or separately authorized SonarQube Cloud remediation.

## Reassessment after PR #35

- `2026-07-20T12:03:31Z`: after PR #35 was normally merged at
  `2026-07-20T11:57:54Z`, exact Framework master
  `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5` returned SonarQube Cloud Quality
  Gate `ERROR` solely on New Security Rating E (actual `5`, threshold `1`).
  Reliability and Maintainability were A, duplication was `0.0`, and hotspot
  review was `100.0`.
- All six exact-master GitHub Actions workflows passed. The public inventory
  has 14 untriaged vulnerability signals: five in Framework-owned paths and
  nine under read-only MRTS. This does not confirm an individual vulnerability
  or establish that PR #35 caused the existing master backlog.
- The stored user acceptance remains limited to PRs #24, #26, #27, and #29.
  It is not automatically extended to PR #35 or current PR #36. PR #36 must
  remain unmerged until the user makes a new exact risk decision or separately
  authorizes a scoped remediation.

## Current-user bounded acceptance for PR #36

- `2026-07-20T12:50:36Z`: after the current exact master-only Sonar result was
  presented, the user directly instructed integration of Framework PR #36. The
  retained acceptance artifact is
  `/var/tmp/codex/ModSecurity-conector/runs/20260720T113905Z-framework-pr35-36-integration-de98515c/analysis/pr36-master-sonar-risk-acceptance.md`,
  SHA-256 `5e280a0b832b7ecef6109f297602c137fe3fdb3b2687252163a0b774769fb162`.
- It conditionally authorizes only current Framework PR #36 after a normal
  non-rewriting refresh from master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5`
  and fresh exact-head CI, Sonar, review, conflict, documentation, and security
  evidence. Its merge must remain protected by exact-head verification.
- It accepts only the documented master-only Security E gate and untriaged
  14-signal inventory. It does not close this finding; classify scanner signals
  as false positives; waive a fresh PR-head gate or any other control; authorize
  Parent or MRTS work; or extend to another PR, future master state, or release.

## Reassessment after PR #36

- `2026-07-20T13:06:39Z`: Framework PR #36 exact head
  `1608352912a755f0f8639eddfa2350436446067e` was normally merged with
  exact-head protection as master `784977615acfc55567e37b863309abc4a38ac877`.
  The PR-head Actions, CodeQL, SonarQube Cloud Quality Gate, documentation,
  review, conflict, and security evidence all passed before merge. Parent and
  MRTS remained unchanged.
- The resulting master completed CodeQL Actions/Python/C++, lint, test-common,
  and OpenSSF successfully. Its SonarCloud Code Analysis failed solely on New
  Security Rating E (actual `5`, threshold `1`); Reliability and
  Maintainability were A, duplication was `0.0`, and hotspot review was
  `100.0`. The non-PR `pull-request-head` job was intentionally skipped.
- The immediately preceding master `4907f6ca6ea996f8d4bc6e426d7875bd4c0805d5`
  already had the same Security E condition. The retained artifact
  `analysis/master-sonar-after-pr36.json`, SHA-256
  `5ba2c4ea093419fcf6b1b066c85dd37b7d2a08b29ee23525119e641d2e0093ef`,
  therefore makes no causal attribution to PR #36. It records the bounded
  current-user acceptance as used for this protected delivery only; the P1
  global finding remains `blocked` and requires separate issue triage or a
  passing master Quality Gate.

## Reassessment after PR #38

- `2026-07-20T18:05:00Z`: PR #38's exact head passed its distinct SonarQube
  Cloud Quality Gate with zero new issues and zero security hotspots. The
  resulting Framework master `9dab40c2b8799dc1e4597cb2a2c223ec3f6cd72b`
  nevertheless failed Check Run `88432322185` solely on Security Rating on New
  Code E; Actions and CodeQL on the resulting master passed.
- The immediate predecessor `784977615acfc55567e37b863309abc4a38ac877` already
  had the same master-only failure. No causal attribution is made to the
  action-pin repair. The earlier bounded risk acceptance applies only to PR
  #36 and is not extended to PR #38 or later integrations.

## Reassessment after PR #37

- `2026-07-21T07:28:49Z`: normal exact-head-protected merge of PR #37 source
  `1e9fa0d22639517193d450b05eb7b07193e41257` produced current Framework master
  `f73f8842f45318e2df8aff1d31855eeb7c20a22f`. The PR head passed its separate
  SonarQube Cloud Quality Gate; all applicable resulting-master Actions and
  CodeQL checks passed.
- Resulting-master SonarCloud failed solely on New Security Rating C (actual
  `3`, threshold `1`). The nine open gate-driving inputs are unchanged
  read-only MRTS records created before PR #37. Static source/control/sink
  triage classifies all nine `needs_review`: CLI/YAML-controlled file/process
  sinks exist, but no current untrusted Framework invocation is established.
- The retained post-merge artifact is `analysis/postmerge-master-sonar-triage.md`,
  SHA-256 `a9a312f1ba760030ceb45644ced6b0d533fe01b9a4d2f8e19c1e832dc54b5830`.
  The historic PR #36-only acceptance is not extended; FND-SONAR-0002 remains
  blocked without an MRTS action, a scanner/gate change, or a new risk decision.

## Current-user bounded acceptance for PR #42

- `2026-07-23T07:01:16Z`: the user explicitly instructed: “kannst den
  FND-SONAR-0002 ausen vor lassen und den pr 42 in den master übernehmen”.
  The retained, payload-safe acceptance receipt is
  `/var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/fnd-sonar-0002-pr42-risk-acceptance.md`,
  SHA-256 `5f087611098d039da1c73f128bc442efecf24f25df9f145fcef2a97ec6107642`.
- It accepts only current Framework master
  `f73f8842f45318e2df8aff1d31855eeb7c20a22f` failing the master-only
  SonarQube Cloud Quality Gate solely on Security C (actual `3`, threshold
  `1`), with nine pre-existing read-only MRTS signals still `needs_review` and
  potentially real in another trust context.
- The acceptance applies only to normal protected Framework PR #42 integration
  after fresh exact-head verification. It does not waive PR-head Sonar, Actions,
  CodeQL, reviews, documentation, security, `FND-GITHUB-0007` Cloudflare,
  merge-method selection, resulting-master validation, Parent/MRTS boundaries,
  direct-push/bypass prohibitions, scanner/gate controls, future conditions, or
  finding closure. The global finding remains `blocked` and `release_blocker`.

## Resulting-master verification after PR #42

- 2026-07-23T07:51:09Z: PR #42 exact head
  dc6cf411e78b3f37f1e4be52edef59894560b1ae was normally merged with
  exact-head protection as Framework master
  935cf14c676a24672be5c336e92cd13457cc35c8. Its tree equals the reviewed PR
  head; eight exact-master GitHub Actions workflows completed successfully.
- SonarQube Cloud analysis dda3ea04-2721-4ee6-a9c1-74bd2925f139 is bound to
  the exact resulting revision. Its Quality Gate is terminal ERROR solely on
  New Security Rating C (actual 3, threshold 1); reliability and
  maintainability are A, duplication is 0.0, and hotspot review is 100.0.
  This is the same documented residual condition accepted only for this
  completed PR #42 delivery, not a false-positive disposition or closure.
- Retained post-merge receipt:
  /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-20260723-postmerge-verification.md,
  SHA-256 0a0421f70cf39df8f6f31ef12b4a461f05bd9875fb61775094c5031aef489ce1.
  Parent, its Framework gitlink, and MRTS remained unchanged. The global P1
  finding remains blocked and a release blocker for every other scope.

## Current-user bounded acceptance for PR #44

- `2026-07-24T03:51:41Z`: after the precise current master-only residual and
  normal-merge scope were presented, the user replied “ja”. In this direct
  conversational context, that accepts only normal exact-head-protected
  Framework PR #44 delivery.
- The retained acceptance receipt is
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a/evidence/pr44-master-sonar-risk-acceptance-retained.md`,
  SHA-256 `bd07be75f13798ab168cfb6994961c453a035b9781ab657cb72a69d0b1302819`.
- Fresh final pre-merge evidence at `2026-07-24T03:56:04Z` records exact PR
  #44 head `3b67efb8534fb56a93f085897417ada449ff1a39`, a passed PR Quality
  Gate and green applicable checks, no reviews/threads, and current master
  `f98a8739cb13b583f23d646784b144e596b61441` still failing only on Security C
  (actual `3`, threshold `1`). The public issue API reports nine open
  vulnerability signals; they remain `needs_review`, not false positives.
- The retained pre-merge receipt is
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a/evidence/pr44-final-premerge-readback.md`,
  SHA-256 `d677a3638802a06251d91b3d1d2f00634bd34814baf041eb1c472619d9efaf2c`.
- GitHub normally merged the exact reviewed head with `--match-head-commit` at
  `2026-07-24T04:11:49Z` as Framework master
  `4c9753291d26d92f2d7e51ae425dedb79666fd5e`; its tree equals the reviewed
  head. Resulting-master CodeQL actions/C++/Python, current-revision advisory,
  common-structure, and scaffold-lint passed; the PR-only head job was
  intentionally skipped. SonarCloud failed only on the same Security C
  condition (`3` versus `1`), with nine `needs_review` read-only MRTS signals.
- Retained resulting-master receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T201023Z-framework-pr44-review-master-integration-2a51bd2a/evidence/pr44-resulting-master-verification.md`,
  SHA-256 `71228129d8b0a24706a35219fb568679ef7be0e7a47a615cb7f5abcc167c1f3f`.
- This does not waive PR-head CI/Sonar/review/documentation/security controls,
  exact-head protection, post-merge validation, Parent/MRTS boundaries, direct
  push/bypass prohibitions, scanner/gate changes, future heads/master states,
  or finding closure. The global finding remains `blocked` and
  `release_blocker`.

## Resulting-master verification after PR #43

- `2026-07-23T11:24:30Z`: GitHub normally merged PR #43 exact head
  `4c55bb2855b8e0196fe54cb0c6f90f43aa993962` with exact-head protection as
  Framework master `f98a8739cb13b583f23d646784b144e596b61441`.
- Exact master analysis `77e255d6-17a2-4e8a-bb29-6438e91e6fa8` is bound to
  that revision. It is `ERROR` solely on New Security Rating C (actual `3`,
  threshold `1`); Reliability and Maintainability are A, duplication is `0.0`,
  hotspot review is `100.0`, and the inventory has nine read-only MRTS
  vulnerability signals. `test-common`, OpenSSF Scorecard, lint, and CodeQL
  analysis completed successfully; the PR-only head job was skipped on the
  non-PR trigger.
- The same analysis has zero open `python:S3415` issues, so the Quality Gate
  condition is independent of the PR #43 assertion-order remediation. The
  PR-#42-only risk acceptance expressly excludes future PRs and master
  conditions; it does not cover #43 or `f98a873…`. No Parent or MRTS action,
  scanner/gate change, suppression, false-positive disposition, or finding
  closure occurred. The finding remains globally `blocked` and a P1 release
  blocker pending a passing gate, separately authorized external remediation,
  or a current exact-scope user risk decision.
- Retained receipt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260723T092456Z-framework-sonarqube-test-issues-507-10387697/evidence/framework-pr43-postmerge-master-verification.md`,
  SHA-256 `d8a63662d10def3118b5795c90474a0c63ab9a96a82d5e93debb8436c79bd79c`.
