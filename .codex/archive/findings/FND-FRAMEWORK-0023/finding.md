# FND-FRAMEWORK-0023 — Framework PR #30 adds SonarQube Cloud new-code duplication in shared safety controls

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0023 |
| Category | sonarqube_finding |
| Repository / ownership | framework / framework |
| Priority / severity | P2 / not_applicable |
| Confidence / status | confirmed / fixed |
| Feasibility | feasible_now |
| Release blocker | false |
| Security relevant | true |

## Summary, observation, expected behavior, and impact

Framework PR #30 initially had a SonarQube Cloud Quality Gate of OK, but its new-code measures reported new_lines=15461, new_duplicated_lines=182, and new_duplicated_lines_density=1.1771554233232002 (displayed as 1.2%). The current user requires that duplication to be remediated before the PR is integrated into master; the green <3% threshold is not an alternative to the requested result.

The first behavior-preserving refactor was normally pushed as `ce6c1570d3dfbe4b4da5f9560068c37a807899d3`. Its historical exact-head Sonar readback had Quality Gate `OK` but still reported `new_duplicated_lines=32` and `new_duplicated_lines_density=0.2059732234809475`.

The refreshed PR head is now normal merge commit `a448d056ef98e745d8551c198b2e56d33fe38194`, with the former PR head and current Framework master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f` as parents. Its exact SonarQube Cloud result is Quality Gate `OK`, `new_duplicated_lines=0`, and `new_duplicated_lines_density=0.0`. The local legitimate controls and every terminal non-skipped hosted check passed without a Sonar setting, threshold, exclusion, baseline, suppression, or gate change. The finding is therefore `fixed` on the verified PR head. It is not `verified` on master because the current task does not authorize a Framework-master merge.

The initial seven file contributions reconcile exactly to 182 new duplicate lines:

| Path | New duplicated lines |
| --- | ---: |
| ci/reporting/generate-phase-work-queue.py | 37 |
| ci/reporting/generate-connector-work-queue.py | 36 |
| ci/reporting/generate-mrts-native-report.py | 36 |
| ci/provisioning/import-mrts-cases.py | 36 |
| tests/security_regression/test_modsecurity_v3_git_ref_provenance.py | 18 |
| ci/reporting/generate-case-matrix.py | 14 |
| tests/protocol_client/test_check_protocol_evidence.py | 5 |

The exact `ce6c157…` residual is limited to two blocks:

| Path | New duplicated lines | Sonar pairing |
| --- | ---: | --- |
| ci/reporting/generate-case-matrix.py | 14 | lines 2947–3021 and 3146–3220 in the same file (75 lines each) |
| tests/security_regression/test_modsecurity_v3_git_ref_provenance.py | 18 | lines 162–179 paired with test_crs_git_ref_provenance.py lines 221–237 |

The paired blocks contain secure atomic report-writing helpers and private runtime-root/path validation helpers, plus narrowly duplicated test assertions. The Sonar duplication endpoint does not expose the individual new-line subset inside overlapping groups; it does identify the shared blocks. The exact final PR head must report zero new duplicated lines and 0.0% density while retaining all traversal, symlink, descriptor, secure temporary-file, atomic-replacement, provenance, and protocol controls.

Duplicated security-sensitive helpers can later drift in rejection order, failure behavior, descriptor lifetime, or confinement semantics. This is not a validated exploitable vulnerability; it is a confirmed user-blocking quality and maintainability observation that requires a behavior-preserving refactor and legitimate negative controls.

## Scope, preconditions, reproduction, and evidence

The relevant PR is Easton97-Jens/ModSecurity-test-Framework#30 (fix/sonarcloud-quality-gate → master). Its observed pre-update head is b6af3ec83011b2070f6bbe4b3f471478b373f055; the observed current Framework master is 9a729226d2e040d07d7e7a4acebf201faf06ab37. The first remediated, normally pushed head is `ce6c1570d3dfbe4b4da5f9560068c37a807899d3`; a later exact head must reach zero duplication. SonarQube Cloud analysis must be available for project Easton97-Jens_ModSecurity-test-Framework and pull request 30.

~~~
rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/measures/component?component=Easton97-Jens_ModSecurity-test-Framework&pullRequest=30&metricKeys=new_lines,new_duplicated_lines,new_duplicated_lines_density'
rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/measures/component_tree?component=Easton97-Jens_ModSecurity-test-Framework&pullRequest=30&metricKeys=duplicated_lines,new_duplicated_lines,new_duplicated_lines_density&qualifiers=FIL&ps=500'
rtk curl --fail --silent --show-error 'https://sonarcloud.io/api/duplications/show?key=Easton97-Jens_ModSecurity-test-Framework&pullRequest=30&file=ci%2Freporting%2Fgenerate-phase-work-queue.py'
~~~

The retained initial evidence is /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-initial-sonar-duplication.md with SHA-256 27dc350cc104bd804cadaf479bf2b347cee20738fab375b105637280f4575fd3. It was produced in /root/git/ModSecurity-conector by a sanitized SonarQube-Cloud measures-and-duplications API readback, exit code 0, at 2026-07-19T23:05:08Z. The retained historical residual evidence is /var/tmp/codex/ModSecurity-conector/runs/20260719T230508Z-framework-pr30-duplication-master-37469460/evidence/pr30-current-head-residual-duplication.md with SHA-256 bc2d2626510bc6f295f33cf6f8e104a1145af82db75423e577a993396b62bd0e, observed at 2026-07-20T00:34:04Z. The retained exact-head verification is /var/tmp/codex/ModSecurity-conector/runs/20260720T061746Z-framework-pr-30-refresh-remediation-f8407eef/evidence/pr30-refresh-summary.md with SHA-256 04a0b6891f92b0485c298bb939e57fb464cea2bd5872eb74c65d97f6450f4255, command `GitHub exact-head check-run/review readback and SonarQube Cloud PR #30 Quality Gate and measure queries`, working directory /root/git/ModSecurity-conector, exit code 0, observed at 2026-07-20T06:43:42Z, retention retained. It records the zero-duplication exact head, Quality Gate `OK`, and current hosted-check success.

## Root cause and proposed remediation

The historical PR independently introduced equivalent hardened path/runtime-root and secure report-writing routines in several producer scripts, instead of placing their common semantics in a reviewed shared utility. Two test modules also repeated closely related assertion sequences. The normal master merge and first extraction removed most of the duplication. The confirmed residual is two semantically identical case-matrix runtime-snapshot sections and an immutable-commit provenance assertion sequence shared by the V3 and CRS tests; its extraction must preserve rendering order, evidence rows, no-clone/no-submodule assertions, and every negative case.

The first focused repair created shared Framework utilities for the duplicated runtime-path and secure report-writing behavior while preserving direct test call points. The remaining repair is intentionally narrower: one pure case-matrix runtime-snapshot section appender plus an ordering regression, and one immutable-commit fetch-control assertion helper used by separate V3 and CRS legitimate-control tests. It must not change the V3/CRS fake-Git fixtures or their unique negative controls, nor any SonarQube Cloud rule, gate, threshold, baseline, exclusion, coverage setting, suppression, or NOSONAR marker.

## Acceptance criteria and validation plan

- [complete] Current Framework master is merged normally into the PR #30 lineage, without force-push or history rewrite.
- [complete] Only the expected four current-master files were added or modified by the synchronization; the conflict resolution preserves both hardening paths.
- [complete] Traversal, symlink, unsafe-runtime-root, unsafe-temporary-file, atomic replacement, provenance, and protocol negative controls pass.
- [complete] Exact PR #30 head `a448d056ef98e745d8551c198b2e56d33fe38194` reports new_duplicated_lines=0, new_duplicated_lines_density=0.0, and Quality Gate OK.
- [complete] No analytical control is weakened or bypassed.
- [complete] Exact-head hosted checks and review/thread readback succeeded.
- [pending authorization] Normal Framework-master integration and resulting-master revalidation are not authorized by the current task.

The validation sequence is: inspect and manually resolve the normal master merge; run the focused producer/security-regression modules, protocol-client tests if its module changes, workflow-contract tests, targeted Python compilation, git diff --check, and applicable linting with task-owned output roots; perform a focused security-diff review; then require exact local/remote/PR-head equality, fresh CI, review, issue/hotspot, Quality Gate, and zero-duplication evidence. After the authorized squash merge, read back the resulting Framework master SHA and applicable master checks. Parent and MRTS remain unchanged throughout.

## Regression and legitimate-control tests

Direct regression scope:

- tests/security_regression/test_generate_case_matrix_sonar.py
- tests/security_regression/test_generate_phase_work_queue_sonar.py
- tests/security_regression/test_generate_connector_work_queue_sonar.py
- tests/security_regression/test_import_mrts_cases_sonar.py
- tests/security_regression/test_runtime_snapshot_sonar.py
- tests/security_regression/test_modsecurity_v3_git_ref_provenance.py
- tests/security_regression/test_second_remediation.py
- tests/protocol_client/test_check_protocol_evidence.py

Legitimate controls must continue to reject traversal, symlink components, unsafe runtime roots, and unsafe temporary-file conditions; distinguish valid from invalid provenance and protocol inputs; preserve descriptor-relative secure creation and atomic replacement; and obtain zero new Sonar duplication without an analytical-control workaround.

## Dependencies, boundaries, related findings, and residual risk

Dependencies are a clean task-owned Framework worktree, current origin/master, exact-head GitHub Actions and SonarQube Cloud analyses, and the authorized normal PR #30 merge. No external implementation dependency is known; this record has no current blocked_by entries and no duplicates.

This is distinct from FND-SONAR-0002, which owns the pre-existing Framework master multi-file Quality Gate backlog and its scoped historical risk decision. That backlog is neither the cause of this reproducible PR #30 result nor automatically waived here. The Sonar block API's lack of individual new-line ranges is an evidence limitation, and the final current-head metric must be read again after the refactor.

The original PR-specific Sonar result no longer reproduces on the exact PR head, so this finding is fixed. The only delivery gap is the deliberately absent Framework-master integration and resulting-master revalidation; neither is implied by this finding or authorized by the current user. No Parent gitlink update or MRTS modification is authorized.

## History

- 2026-07-19T23:05:08Z — confirmed_pr30_new_code_duplication_tracked: retained SonarQube Cloud evidence recorded 182 new duplicated lines and 1.1771554233232002% density across seven files. Normal branch update, focused shared-helper extraction, local controls, exact-head remote validation, and master integration remain pending.
- 2026-07-20T00:34:04Z — first_remediation_reduced_but_did_not_clear_duplication: the normal non-rewriting push of `ce6c1570d3dfbe4b4da5f9560068c37a807899d3` reduced the exact PR #30 Sonar result to 32 new duplicated lines and 0.2059732234809475% density with Quality Gate OK. The two remaining blocks are confirmed and block merge until a later exact head reports zero.
- 2026-07-20T06:43:42Z — exact_refreshed_pr_head_clears_duplication: normal merge commit `a448d056ef98e745d8551c198b2e56d33fe38194` refreshed PR #30 with Framework master `3d6f51a2a2eeff6f3bcecff203f1e6ed1e240e4f`. Exact-head SonarQube Cloud reports Quality Gate `OK`, `new_duplicated_lines=0`, and `new_duplicated_lines_density=0.0`; local legitimate controls and all terminal non-skipped hosted checks passed. The finding is fixed on the verified PR head; master integration remains unauthorized.
