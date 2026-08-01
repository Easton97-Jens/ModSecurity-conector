# Finding FND-SONAR-0030: Provisioning remediation for thirty-eight SonarQube Cloud findings and two duplicate blocks

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `maintainability` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `not_applicable` / `confirmed` |
| Status / feasibility | `fixed` / `requires_user_decision` |
| Release blocker / candidate integration blocker / security relevant | no / no / yes |
| Final disposition | `exact_draft_pr_226_head_b08bc69278570a02af5c0367bffb2dea47d37d7c_verified_fixed_pending_explicit_master_authorization_and_resulting_master_reproduction` |
| Initial Sonar inventory | 21 `python:S3776`, 10 `python:S1192`, 3 `pythonsecurity:S6549`, 2 `python:S3358`, 1 `python:S1066`, and 1 `python:S8786`; two duplicate blocks total 25 lines. |

## Summary and scope

The retained initial current-master inventory binds the `ci/provisioning/`
scope to Parent revision `6b4aca18d390363764b96d85cd31969b9bb114a1`. It
identified 38 SonarQube Cloud rows in
`ci/provisioning/components/prepare-runtime-components.py` and two
provisioning-side duplicate blocks between `markdown_report()` and
`ci/evidence/reports/update-runtime-reports.py`.

GitHub normal-merged PR #220's exact head
`5378ed0c29f91df7e508f13b9d860c548f882468` as resulting master
`caabf33c11d6002f9a1661f215ed195d6e141253`. All fourteen resulting-master
workflows succeeded and the resulting-master Sonar analysis is bound to that
SHA. It reports zero duplicated lines and `0.0%` duplication, but four open
source rows in the original component remain; each was created before the
retained inventory. The clean PR/New-Code result therefore does not prove that
all 38 old-master rows were remediated. No scanner rule, Quality Gate,
exclusion, suppression, `NOSONAR`, workflow, Framework/MRTS source, Gitlink,
or bypass was changed.

Exact Draft PR #224 head
`0da588ecd068f35e27ae404139906e2bebc89e14` implemented source refactors for
the four retained historical causes: the three cognitive-complexity rows in
`prepare_nginx_runtime()`, `prepare_apache_httpd()`, and
`BuildLock.__enter__()`, plus the nested-condition row in
`remove_incomplete_connector_cache_entry()`. Its focused 94-test aggregate,
local controls, all applicable GitHub checks, and SonarQube Cloud Quality Gate
pass. Sonar reports zero open PR issues, `new_violations=0`, zero security
hotspots, and `0.0%` New-Code duplication. That exact-head result justified
only a provisional `fixed` disposition pending the resulting-master
reproduction below.

## Resulting-master outcome

GitHub normal-merged exact PR #224 head
`0da588ecd068f35e27ae404139906e2bebc89e14` as resulting master
`7016a66f3702523098811b45139133c77dee88fb`. All 14 workflows for that exact
master SHA succeeded, and SonarQube Cloud's master analysis is bound to it.
The nested-condition key `AZ9cRyj3HhV2CayPTPys` and the `BuildLock` key
`AZ9cRyj3HhV2CayPTPy2` are `CLOSED/FIXED`. The two cognitive-complexity keys
`AZ9cRyj3HhV2CayPTPzB` (`prepare_apache_httpd()`) and
`AZ9cRyj3HhV2CayPTPzC` (`prepare_nginx_runtime()`) remain `OPEN`.

The master project Quality Gate is `ERROR`; this record does not attribute any
unrelated existing project finding to PR #224. The original-issue reproduction
opened the two remaining source causes, and no direct master correction is
permitted.

## Current PR #226 outcome

Exact Draft PR #226 head
`b08bc69278570a02af5c0367bffb2dea47d37d7c` centralizes the unchanged
Apache/NGINX keyed-plan staging decision in
`prepare_connector_with_optional_staging()` and retains the public entry points
as thin wrappers over their private per-plan control flow. Its 34 focused
cache-contract tests and Python compilation pass; the focused security-control
review found no plausible diff-induced reportable finding.

The exact local, remote, and GitHub head is identical. The PR is `OPEN`, Draft,
and `CLEAN`, with no submitted review or review decision. All 33 completed
GitHub checks passed and six context-appropriate checks were skipped.
SonarQube Cloud reports Quality Gate `OK`, zero OPEN/CONFIRMED PR issues,
`new_violations=0`, `new_security_hotspots=0`,
`new_duplicated_lines_density=0.0`, and `new_duplicated_lines=0`. The finding
is therefore `fixed`, not `verified` or `closed`: an explicitly authorized
merge and resulting-master reproduction remain required.

## Observed and expected behavior

The initial inventory concentrated cognitive complexity, repeated literals,
nested conditional flow, one regex-performance observation, path-construction
scanner leads, and two report-rendering duplicate blocks. The scoped code
contains cache, download, path, provenance, and subprocess-adjacent behavior.

Provisioning retains validated managed-root containment, provenance checks,
atomic publication, and argument-vector execution while bounded helpers,
centralized data-only literals, clarified conditional flow, and distinct report
representation remediate the maintainability causes without changing the
report contract.

## Impact and security assessment

A careless maintainability remediation could weaken a containment or
provenance invariant. The retained baseline review contains zero reportable
security findings, but its runtime-snapshot-wrapper caller-reachability
coverage remains explicitly deferred. The sealed exact-head post-change review
for `904a8fca64b35cd287348722b4bdc2260b4f64b3...cb500e3a84efe94565b7a6665dea4b94ec719501`
has complete coverage and zero reportable findings.

The exact PR #226 head also passed focused local controls and all applicable
GitHub Actions checks. The remaining historic source causes are remediated
without weakening the cache, provenance, path, or subprocess controls. The
finding is `fixed`, not `verified` or `closed`, until integration and a
resulting-master reproduction are observed.

## Affected files and symbols

Files:

- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/evidence/reports/update-runtime-reports.py`
- `tests/test_prepare_runtime_components.py`
- `tests/test_runtime_component_cache_contract.py`

Symbols:

- `validated_cache_manifest_for_entry`, `prepare_git_component`,
  `prepare_archive`, `resolve_nginx_archive`, `hash_input_paths`,
  `prepare_expat_managed_overrides`, `prepare_expat`,
  `modsecurity_build_inputs`, `prepare_shared_modsecurity`, `connector_plan`,
  `prepare_go_tool`, `rebase_apache_install_text_paths_for_publish`,
  `connector_cache_entry_complete`,
  `reuse_connector_cache_entry_if_only_commit_changed`,
  `prepare_connector_transactionally`, `prepare_apache_httpd`,
  `prepare_nginx_runtime`, `prepare_haproxy_runtime`,
  `remove_incomplete_connector_cache_entry`, `BuildLock.__enter__`,
  `known_tool_source`, `markdown_report`, `main`, and
  `map_expat_build_failure`.

## Preconditions and reproduction

Preconditions:

- The initial inventory remains bound to Parent revision
  `6b4aca18d390363764b96d85cd31969b9bb114a1`.
- The task remains confined to Parent provisioning remediation, directly
  necessary Parent tests, versioned change records, and local control-plane
  evidence.
- No SonarQube Cloud rule, Quality Gate, exclusion, suppression, `NOSONAR`,
  workflow, Framework/MRTS source, Gitlink, or direct master change is used.

The exact PR-head New-Code analysis was clean without changing analysis
controls. GitHub then normal-merged exact head
`5378ed0c29f91df7e508f13b9d860c548f882468` as resulting master
`caabf33c11d6002f9a1661f215ed195d6e141253`; all fourteen resulting-master
workflows succeeded. The Sonar master analysis is bound to that SHA and has
zero duplicate lines and `0.0%` duplication. It also retains four OPEN rows:
`AZ9cRyj3HhV2CayPTPzC` (`python:S3776`, `prepare_nginx_runtime()`),
`AZ9cRyj3HhV2CayPTPzB` (`python:S3776`, `prepare_apache_httpd()`),
`AZ9cRyj3HhV2CayPTPys` (`python:S1066`,
`remove_incomplete_connector_cache_entry()`), and
`AZ9cRyj3HhV2CayPTPy2` (`python:S3776`, `BuildLock.__enter__()`). Their
creation dates precede the retained inventory. PR #224 closed the latter two
keys, but the Apache and NGINX cognitive-complexity keys remain open on
resulting master; remediate those two source causes and rerun the original
reproduction before moving to `fixed` or `verified`.

## Retained evidence

- Historical initial current-master Sonar inventory and task-plan path
  `.codex/plans/ci-provisioning-sonar-remediation-20260801.md` (not distributed
  in this reconciliation checkout)
  — SHA-256 `4cab13eaecb863922524318c350a85baeb57f72db6a32cd86cbcae3bd9005274`;
  read-only inventory; exit `0`; observed `2026-08-01T11:08:22Z`.
- Sealed baseline scoped security review (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/security-scan-6b4aca18-20260801/report.md`)
  — SHA-256 `d4eb095bd927350ea1a1a9c349750abd3bba0e1960721cd83fa6446e0aaa8503`;
  partial baseline coverage, zero reportable findings, and one deferred
  caller-reachability question; exit `0`; observed `2026-08-01T10:25:41Z`.
- Sealed exact-head security review (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/security-diff-904a8fca-cb500e3a-20260801/report.md`)
  — SHA-256 `6b9ce34f771a3b7f8799b0ba9addcbc5e649005efeb932955cd7734a4f64bd6a`;
  complete coverage and zero reportable findings; exit `0`; observed
  `2026-08-01T13:10:39Z`.
- Exact-head hosted verification receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/hosted-verification-pr-220-cb500e3a.md`)
  — SHA-256 `d129af2ad25db78f85623c8b1d14149ad03192257a7fa70c7d4be4b223bd1d8f`;
  exact PR #220 head, GitHub Actions, and SonarQube Cloud evidence; exit `0`;
  observed `2026-08-01T13:20:09Z`.
- Resulting-master integration and Sonar reproduction receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-sonar-remediation-20260801/master-integration-verification-caabf33c-20260801.md`)
  — SHA-256 `351639d5a70189bf776063414c8ea8b23060dc863b6177cea2638415f450a55d`;
  normal merge, tree identity, fourteen successful master workflows, and the
  exact resulting-master Sonar reproduction; exit `0`; observed
  `2026-08-01T14:13:10Z`.
- PR #224 exact-head hosted verification receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-four-sonar-followup-20260801/hosted-verification-pr-224.md`)
  — SHA-256 `975675e0ae13027d05f7a219c884b24428ff03eb0f82f43d64b4f97073f69647`;
  Draft PR #224 exact-head GitHub-check, review, and SonarQube Cloud evidence;
  exit `0`; observed `2026-08-01T15:46:12Z`.
- PR #224 resulting-master verification receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-four-sonar-followup-20260801/master-integration-verification-7016a66f.md`)
  — SHA-256 `44324bf23b19bebd8523056dbd6834d77eea9e2113ddc96e96cdf525328688bd`;
  normal merge, exact-master workflows, and original-issue SonarQube Cloud
  reproduction; exit `0`; observed `2026-08-01T16:03:41Z`.

## Root cause and remediation

Provisioning cache, acquisition, component, reporting, and CLI
responsibilities accumulated in one primary module. This created high-
complexity control flow, repeated literals, local nested branches, and a
duplicated report-rendering representation.

The completed remediation, including PR #224, preserves cache, path,
provenance, and subprocess safety contracts while extracting bounded helpers,
centralizing data-only literals, simplifying selected flow, preserving
`pythonsecurity:S6549` controls, and making the provisioning-side markdown
representation distinct. PR #224 reduces the cognitive complexity of
`prepare_nginx_runtime()`, `prepare_apache_httpd()`, and `BuildLock.__enter__()`
and simplifies the nested conditional in
`remove_incomplete_connector_cache_entry()` without changing scanner controls
or merely moving code to alter metrics.

## Acceptance criteria and validation plan

Completed partial-remediation evidence:

- The 91 focused Parent provisioner/cache/environment/artifact/path-policy
  tests passed, together with Python compilation, `make check-runtime-path-policy`,
  bilingual documentation, documentation links, and `git diff --check`.
- Managed Expat marked-child acceptance and external-path, canonical-traversal,
  and symlink-escape rejection controls passed before cache filesystem or build
  sinks. The silent nonzero Git-submodule-failure and bounded NGINX
  profile-propagation controls also passed.
- The sealed exact-head security review has complete coverage and zero
  reportable findings.
- At the exact PR head, all named required GitHub Actions checks succeeded and
  SonarQube Cloud reported Quality Gate `OK`, zero open PR issues,
  `new_violations=0`, `new_security_hotspots=0`,
  `new_duplicated_lines_density=0.0`, and `duplicated_lines_density=0.0`.
- GitHub normal-merged exact head `5378ed0c29f91df7e508f13b9d860c548f882468`
  as `caabf33c11d6002f9a1661f215ed195d6e141253`; all fourteen exact-master
  workflows passed and the resulting-master Sonar analysis has zero duplicate
  lines and `0.0%` duplication.

Completed follow-up condition: PR #224 remediates the nested-condition and
BuildLock causes. The focused 94-test aggregate, Python compilation,
`make check-runtime-path-policy`, bilingual documentation, documentation links,
and `git diff --check` pass; the exact-head GitHub checks pass and SonarQube
Cloud reports Quality Gate `OK`, zero PR issues, and `0.0%` New-Code
duplication.

Resulting-master verification completed: all 14 workflows pass, but original
keys `AZ9cRyj3HhV2CayPTPzB` and `AZ9cRyj3HhV2CayPTPzC` remain open. Exact Draft
PR #226 now centralizes their unchanged keyed-plan staging decision in
`prepare_connector_with_optional_staging()` and retains the Apache/NGINX
per-plan control flow. Python compilation and 34 focused cache-contract tests
pass; the focused source/control review found no plausible diff-induced
reportable security issue. Its exact head is verified; only resulting-master
reproduction remains before `verified` or `closed`.

## Dependencies, blockers, and related findings

- Dependency: an explicit current-user `master`-integration authorization,
  followed by resulting-master reproduction of the two original keys.
- Blockers: source work is complete; delivery requires the user decision.
- Duplicates: none.
- Related findings: `FND-SONAR-0016`, `FND-SONAR-0029`.
- Source runs: `ci-provisioning-sonar-remediation-20260801`,
  `ci-provisioning-four-sonar-followup-20260801`, and
  `ci-provisioning-two-cognitive-sonar-remediation-20260801`.

## Residual risk

The baseline review retains a deferred runtime-snapshot-wrapper
caller-reachability question, although the focused PR #226 review found no
reportable diff-induced security finding. Two pre-inventory maintainability
causes are `CLOSED/FIXED`; the last two are fixed in exact Draft PR #226 but
remain open on current master. The finding is `fixed`, not `verified` or
`closed`.

## History

- `2026-08-01T11:08:22Z`: allocated after the revision-matched initial
  inventory identified 38 current `ci/provisioning` rows and two
  provisioning-side duplicate blocks. No code completion, commit, PR, merge,
  scanner-control, Framework/MRTS, Gitlink, or master action was claimed.
- `2026-08-01T11:36:00Z`: a sealed working-tree post-change review completed
  with complete coverage and zero reportable findings. This was local evidence
  only and did not claim a commit, PR, merge, hosted analysis, or closure.
- `2026-08-01T13:20:09Z`: exact Draft PR #220 head verification completed.
  Base is `904a8fca64b35cd287348722b4bdc2260b4f64b3`; matching local, remote,
  and GitHub head is `cb500e3a84efe94565b7a6665dea4b94ec719501`. The final
  security review has complete coverage and zero reportable findings, 91
  focused local tests and controls pass, required exact-head GitHub Actions
  succeed with `quick-framework-check` expected skipped, and SonarQube Cloud
  reports Quality Gate `OK` with zero open PR issues and `0.0` duplication.
  No master merge was authorized or attempted, so the lifecycle transition is
  `fixed`, not `verified` or `closed`.
- `2026-08-01T14:13:10Z`: GitHub normal-merged exact PR #220 head
  `5378ed0c29f91df7e508f13b9d860c548f882468` as resulting master
  `caabf33c11d6002f9a1661f215ed195d6e141253`. All fourteen resulting-master
  workflows succeeded and the master Sonar analysis is bound to that SHA with
  zero duplicate lines and `0.0%` duplication. The original reproduction also
  retains four OPEN rows created before the retained inventory:
  `AZ9cRyj3HhV2CayPTPzC`, `AZ9cRyj3HhV2CayPTPzB`,
  `AZ9cRyj3HhV2CayPTPys`, and `AZ9cRyj3HhV2CayPTPy2`. The earlier clean
  PR/New-Code evidence therefore cannot establish full historical remediation;
  the canonical status is corrected to `in_progress` and no scanner control,
  Framework/MRTS source, Gitlink, bypass, or direct master write was used.
- `2026-08-01T15:46:12Z`: exact Draft PR #224 head
  `0da588ecd068f35e27ae404139906e2bebc89e14` was verified against base
  `62f7e13f35edd3f73661f724fd5208dcf1584d18`. It remediates the four retained
  historical source causes. The focused 94-test aggregate and local checks
  passed; all applicable exact-head GitHub checks passed; SonarQube Cloud
  reports Quality Gate `OK`, zero open PR issues, `new_violations=0`, zero
  security hotspots, and `0.0%` New-Code duplication. The only issue comment
  is the successful Sonar bot notification; no review comments or submitted
  reviews remain. No merge was authorized or attempted. The status is `fixed`
  pending user-authorized integration and resulting-master reproduction.
- `2026-08-01T16:03:41Z`: GitHub normal-merged exact PR #224 head
  `0da588ecd068f35e27ae404139906e2bebc89e14` as resulting master
  `7016a66f3702523098811b45139133c77dee88fb`. All 14 workflows for that exact
  master SHA succeeded. The Sonar master analysis is bound to that SHA:
  `AZ9cRyj3HhV2CayPTPys` and `AZ9cRyj3HhV2CayPTPy2` are `CLOSED/FIXED`, but
  `AZ9cRyj3HhV2CayPTPzB` and `AZ9cRyj3HhV2CayPTPzC` remain `OPEN`. The project
  Quality Gate is `ERROR`; no unrelated project finding is attributed to this
  PR. The original-issue reproduction returns the status to `in_progress`.
- `2026-08-01T16:33:12Z`: a fresh read-only SonarQube Cloud query confirms
  exactly the two remaining current-master keys, `AZ9cRyj3HhV2CayPTPzB` and
  `AZ9cRyj3HhV2CayPTPzC`, both `python:S3776` at cognitive complexity 16 where
  15 is allowed. The task-owned Parent branch centralizes the unchanged
  keyed-plan transactional entry decision in
  `prepare_connector_with_optional_staging()`; public Apache/NGINX wrappers
  preserve private per-plan control flow. Python compilation and 34 focused
  cache-contract tests pass, and the focused review finds no plausible
  diff-induced reportable security issue. No commit, push, PR, hosted analysis,
  scanner-control change, Framework/MRTS source, Gitlink, or master action is
  claimed.
- `2026-08-01T16:59:29Z`: exact Draft PR #226 head
  `b08bc69278570a02af5c0367bffb2dea47d37d7c` is identical locally, remotely,
  and on GitHub. It is open, Draft, and `CLEAN`, with no submitted review or
  review decision. All 33 completed GitHub checks pass and six expected checks
  are skipped. SonarQube Cloud reports Quality Gate `OK`, zero OPEN/CONFIRMED
  PR issues, `new_violations=0`, `new_security_hotspots=0`, and zero New-Code
  duplication. The finding is `fixed` pending explicit master authorization and
  resulting-master reproduction; no merge or scanner-control change occurred.

## Latest retained evidence

- PR #226 exact-head hosted verification receipt (`/var/tmp/codex/ModSecurity-conector/runs/ci-provisioning-two-cognitive-sonar-remediation-20260801/hosted-verification-pr-226-b08bc692.md`)
  — SHA-256 `92cee447f5fb36bfa536681b85c8d6a04d9b9d7f74c2f79db0bfa3e8666b2e5a`;
  matching exact head, full GitHub-check disposition, and SonarQube Cloud PR
  evidence; observed `2026-08-01T16:59:29Z`.
