# FND-SONAR-0017 — MRTS PR #4 eliminates all task-owned SonarCloud issues on merged main

## Classification

ID: FND-SONAR-0017
Category: sonarqube_finding
Repository: mrts
Ownership: mrts_explicit_user_task
Priority: P1
Severity: not_applicable
Confidence: validated
Status: closed (archived)
Release blocker: no
Security relevant: yes
Verification status: verified_merged_main_hosted_sonar_zero
Remediation status: closed_verified_merged_main_hosted_sonar_zero

## Summary and behavior

The 12-item MRTS SonarCloud baseline was remediated without changing scanner
controls. Exact PR #4 source head 9cdfd4136286014b244f8fecfb99701681fecae4 was
head-protected Squash-merged as `main`
615b13bacbd008562c17408246c41ab27dca3104. Resulting `main` has 0 open
SonarCloud issues, Quality Gate OK, successful Push on main, Python governance,
and CodeQL workflows, and no open CodeQL alert.

Baseline issues were seven python:S5778, two python:S1172, two python:S3776,
and one pythonsecurity:S8705. The first PR analysis introduced one
python:S1192 duplicate-literal issue at mrts/mrts.py:66; GO_FTW_CONFIGURATION
removed it without behavioral change. Both the exact PR and resulting-main
queries return total 0.

Expected behavior is zero open task-owned issues and an OK Quality Gate on the
merged main revision without rule, gate, exclusion, false-positive, NOSONAR,
suppression, or security-control changes.

## Impact, scope, and reproduction

The user required zero issues before main integration. PR #4 was then merged
using the selected protected Squash method, and resulting main verification
passes. Affected files are mrts/mrts.py, tools/test_mrts_path_utils.py,
tools/test_validate_governance.py, and tools/validate-governance.py.

Query SonarCloud main issues with componentKeys=Easton97-Jens_MRTS, branch=main,
resolved=false, ps=500; query Quality Gate with projectKey=Easton97-Jens_MRTS
and branch=main; inspect PR #4 merge state, the resulting main SHA, main
workflow runs, and the CodeQL alert list.

## Evidence

- sonar-pr-issues.json: SHA-256 ee8fdf86104a53c760e40f0d42b92b51d2c13f2e289efcb6b562dce9076f6a55, total 0.
- sonar-quality-gate.json: SHA-256 1db063f467b49ec05719b0f44b2c703bc402ae52f2515452169ddafbe4343c64, Quality Gate OK.
- pr-status.json: SHA-256 cf4ad16887f3e9723292215666e48e269c4a3a4f01b319024973e2915a4fa5a6, exact head and four successful checks.
- local-validation.md: SHA-256 5fdc769af00f7c81b8839766bf6f65834b91278f65a55c00a2adc5677db743fd, 38 tests, compileall, and diff check passed.

- github-post-merge.json: SHA-256 6d77c474bdc6a8b9744dd3ac8e2b6c76195a47e47fb945caa75acb5173a1f936, protected Squash merge, resulting main, successful workflows, no open CodeQL alert, and unchanged Gitlinks.
- sonar-main-issues.json: SHA-256 58cf67de638c7b544b279c8365ac3334eb279716faed0996d6fe439a6ac9ad58, total 0 on main.
- sonar-main-quality-gate.json: SHA-256 0f88c3322a2a779ea067fcf61cbf21946c614836989b5f5d360f7c04f078e69b, main Quality Gate OK.

All are retained under .codex/runs/20260726T101017Z-mrts-sonarcloud-zero-pr4.
The resulting-main receipts are sealed under
.codex/runs/20260726T105800Z-mrts-pr4-squash-merge.

## Root cause, remediation, and validation

Assertion-call refactors, unused arguments, cognitive complexity, and a scanner
taint candidate required narrow source/test changes. Sink-local validation
created a repeated literal, then GO_FTW_CONFIGURATION removed S1192. Fixed
go-ftw argv, shell=False, path validation, error strings, and governance
predicates remain preserved. No scanner control changed.

Acceptance: resulting main has 0 issues; Quality Gate and all applicable
main workflows are green; the focused MRTS suite has 38 passing tests; no
suppression/control weakening, direct main push, Gitlink action, or
unauthorized cleanup deletion occurred.

Legitimate controls prove shell-looking existing paths remain individual Popen
argv operands with shell=False, default configuration remains accepted, missing
inputs fail before Popen, and governance negative controls retain expected
errors.

## Dependencies, blockers, related findings, residual risk, and history

There are no remaining remediation dependencies or blockers. FND-SONAR-0012
is related but has another PR and root cause. The merged remote branch and
clean task worktree are retained because no deletion/removal action class was
authorized.

No full go-ftw integration run or remote exploit is claimed. Downstream
configuration semantics and PATH trust remain separate.

- 2026-07-26T09:00:00Z: 12-issue baseline mapped.
- 2026-07-26T10:02:19Z: first PR analysis found S1192; constant extraction
  chosen instead of suppression.
- 2026-07-26T10:10:17Z: exact head verified with 0 issues, Quality Gate OK,
  and four successful checks.
- 2026-07-26T10:55:25Z: exact-head-protected Squash merge created main
  615b13bacbd008562c17408246c41ab27dca3104.
- 2026-07-26T10:58:00Z: all resulting-main workflows passed; main SonarCloud
  reported 0 open issues and Quality Gate OK; no open CodeQL alert exists.

Final disposition: closed_verified_merged_main_hosted_sonar_zero
