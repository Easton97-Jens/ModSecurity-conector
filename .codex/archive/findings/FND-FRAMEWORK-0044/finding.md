# FND-FRAMEWORK-0044 — Framework PR #42 has 27 SonarQube Cloud code smells locally remediated pending exact-head confirmation

## Classification

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0044 |
| Category | sonarqube_finding |
| SonarQube Cloud classification | maintainability |
| Repository / ownership | framework / framework |
| Priority / severity | P2 / not_applicable |
| Confidence / status | validated / fixed |
| Feasibility | feasible_now |
| Release blocker / security relevant | true / false |
| Final disposition | local_framework_pr42_remediation_and_cpython_3_14_6_migration_fixed_pending_exact_head_hosted_confirmation |

## PR #47 follow-up — 2026-07-26

The exact initial head `3bbb2e806f4892e8f92476e35740d149b8b9b17b` of
Framework PR #47 has three task-owned maintainability diagnostics in
`ci/checks/security/check-ci-security-contract.py`: two `python:S1192`
duplicate-literal findings and one `python:S3776` cognitive-complexity
finding. They are the same bounded root causes as this canonical record, so
they are tracked here rather than receiving a duplicate finding.

The retained SonarQube Cloud inventory is
`/var/tmp/codex/ModSecurity-conector/runs/20260726T105400Z-framework-pr47-sonar-merge/evidence/sonar-pr47-initial-issue-inventory.json`,
SHA-256 `d98ef7664e411e8d6f820eec8a4b8b82e9501fcf5aabf42e9b7a1cd857006937`.
The local repair names the repeated checkout-policy literals and splits the
submodule-updater validation into bounded helpers while retaining the positive
and rejection contracts. It passed the focused CI-security contract suite and
workflow/documentation controls locally. A fresh SonarQube Cloud analysis for
the subsequently submitted exact PR head remains required; no `NOSONAR`,
suppression, rule or Quality-Gate change, exclusion, or false-positive marking
is used.

## Current PR #42 reconciliation — 2026-07-22

The retained PR #42 initial inventory at exact head
`1fd3b362e0fed9766c6920e3c7bd1939535850f2` contains 42 open or confirmed
new-code `CODE_SMELL` diagnostics. This finding owns 27 diagnostics in
`check-ci-security-contract.py`, `check-python-version.py`,
`update-python-version.py`, and the updater-exception test path; the remaining
15 `python:S3415` assertion-order diagnostics are independently owned by
`FND-FRAMEWORK-0050`.

The current 27-key ownership is limited to these four paths:

- `ci/checks/security/check-ci-security-contract.py` (7 keys)
- `ci/checks/security/check-python-version.py` (5 keys)
- `ci/tools/update-python-version.py` (14 keys)
- `tests/ci_security/test_update_python_version.py` (1 key:
  `AZ-K30-lbx6VBofpXBhy:208`)

The complete key-by-rule inventory is canonical in `finding.json` and retained
verbatim in `evidence/sonar-pr42-initial-issue-inventory.md`; it is the
acceptance set for the later exact-head no-suppression query.

The combined local patch retains the Sonar root-cause remediation and migrates
the active Framework Python contract to exact CPython `3.14.6`. Selected local
CPython `3.14.4` validation passed the 61 migration tests, the 49 direct
Sonar-remediation tests, `pip check`, contracts, documentation checks, CP314
positive and CP313-negative hash-lock controls, `git diff --check`, and the
full native `make lint` target. The complete 22-path security scan reported no
reportable finding; its report SHA-256 is
`1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36`.
The local validation receipt is
`evidence/framework-pr42-python314-local-validation.md` in run
`20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e`, SHA-256
`4f3f7967438688697da9dcca5cb57bcaf7914c700342d9af8bb07f16a8d63075`.

This is local proof only. It does not establish a target-`3.14.6` hosted job,
a live Python.org update, real package installation, GitHub Actions result,
review/branch-protection state, or SonarQube Cloud result. The next required
control is a normal task-branch submission followed by an exact-head SonarQube
Cloud query showing all 27 owned keys absent without `NOSONAR`, suppression,
false-positive marking, rule/gate change, or exclusion. The unrelated current
master condition remains `FND-SONAR-0002`; no master integration is authorized
by this local finding state.

### Current evidence

| Field | PR #42 initial SonarQube Cloud inventory |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/sonar-pr42-initial-issue-inventory.md |
| Artifact type | task_owned_sonarqube_cloud_pr42_initial_inventory |
| SHA-256 | 7d4c5cff26e885de37c1090713e7fe947e409c1478f3dcd6a69809ddd3401d44 |
| Command | rtk run curl SonarQube Cloud issues API with pullRequest=42, OPEN/CONFIRMED, sinceLeakPeriod=true, ps=500 |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-22T18:18:47Z |
| Retention status | task_owned_retained_evidence |

| Field | CPython 3.14 local validation |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/evidence/framework-pr42-python314-local-validation.md |
| Artifact type | framework_pr42_cpython3146_local_validation_receipt |
| SHA-256 | 4f3f7967438688697da9dcca5cb57bcaf7914c700342d9af8bb07f16a8d63075 |
| Command | Selected CPython 3.14.4 focused tests, contracts, CP314 hash-lock dry runs, full native make lint, and diff hygiene for the configured CPython 3.14.6 migration |
| Working directory | framework-worktree-v4 |
| Exit code | 0 |
| Observed at | 2026-07-22T20:14:50Z |
| Retention status | task_owned_retained_evidence |

| Field | Sealed combined 22-path security scan |
| --- | --- |
| Run ID | 20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260722T153352Z-framework-pr-39-41-consolidation-54ccc60e/analysis/security-diff-pr42-python314-20260722T200333Z/report.md |
| Artifact type | sealed_codex_security_diff_scan_report |
| SHA-256 | 1b85288ff20d4c4f04443a9f2e4ba6ce07b69967e165dcc2d3c02257dfc6da36 |
| Command | Complete 22-path Codex Security diff scan of the combined local PR #42 remediation and CPython 3.14.6 migration |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-22T20:14:50Z |
| Retention status | sealed_task_evidence |

### Current history

| At | Event | Detail |
| --- | --- | --- |
| 2026-07-22T20:14:50Z | framework_pr42_sonar_remediation_and_cpython3146_local_validation_reconciled | The 27 owned PR #42 code-smell remediations and coupled exact CPython 3.14.6 migration are locally fixed. Selected CPython 3.14.4 focused validation, direct Sonar-remediation tests, full native make lint, CP314 positive/negative hash-lock controls, and the complete 22-path security scan passed. No hosted Sonar, GitHub, live-update, real-installation, or CPython-3.14.6 hosted-job evidence is claimed. |

## Historical PR #39 record

The remaining PR #39 material is retained as historical evidence only. It does
not describe the current PR #42 delivery state or create a dependency on
`FND-SONAR-0009` for this task.

### Historical PR #39 summary, observed behavior, and impact

The retained initial SonarQube Cloud PR #39 inventory reports 25 open new-code
CODE_SMELL issues in the six listed Framework files. At 2026-07-21T04:40:00Z
the public query returned total 25, all CODE_SMELL issues. The local
remediation is fixed, but hosted confirmation is intentionally not inferred
from local source, test, or scan evidence.

At 2026-07-21T06:13:56Z, the retained Framework-specific CPython 3.13.14
qualification passed hash-locked PyYAML-6.0.3 installation and pip check, 30
direct affected tests, make test-ci-security-contract with 89 tests, workflow
and documentation checks, python -m compileall -q ci tests, the response-body
guard, and make lint. This qualifies the local diff only: no hosted SonarQube
Cloud or GitHub confirmation occurred, and no coverage, scanner, Quality Gate,
rule, exclusion, suppression, or hosted-service configuration changed.

This is a non-security maintainability finding: severity is not_applicable and
security_relevant is false. It remains a release blocker because a fresh
exact-head hosted analysis is an acceptance condition. The sealed local
security review is evidence for the Framework code change only; it does not
prove a hosted SonarQube Cloud result.

### Historical PR #39 expected behavior and proposed remediation

The focused local refactors must preserve CI-security and Python-version
contracts while eliminating the 25 original maintainability issues. Retain the
behavior-preserving local refactors and associated tests, submit the exact
remediation head through the authorized Framework delivery path, and obtain a
matching SonarQube Cloud PR analysis. Every original key must be absent without
NOSONAR, suppression, rule change, Quality Gate change, or exclusion.

### Historical PR #39 affected files and symbols

Affected files:

- ci/checks/security/check-ci-security-contract.py
- ci/checks/security/check-python-version.py
- ci/tools/update-python-version.py
- tests/ci_security/test_framework_ci_security_contract.py
- tests/ci_security/test_python_version_contract.py
- tests/ci_security/test_update_python_version.py

Affected rule or query identifiers: python:S6035, python:S1066, python:S1192,
python:S8786, python:S3776, python:S6353, python:S5713, python:S5778, and
SonarQube Cloud PR #39 issue query.

### Historical PR #39 original issue inventory

All 25 original open or confirmed CODE_SMELL keys are retained by path and
rule. The suffix after each key is its source line.

- ci/checks/security/check-ci-security-contract.py
  - python:S1192: AZ-BJmy21Sm1F-_jUkdY:54, AZ-BJmy21Sm1F-_jUkdX:536
  - python:S6035: AZ-BreILltpcPPRUrDMO:71
  - python:S8786: AZ-BJmy21Sm1F-_jUkdZ:83
  - python:S3776: AZ-BJmy21Sm1F-_jUkda:684
- ci/checks/security/check-python-version.py
  - python:S6353: AZ-BJmyl1Sm1F-_jUkdS:19, AZ-BJmyl1Sm1F-_jUkdT:32,
    AZ-BJmyl1Sm1F-_jUkdU:35, AZ-BJmyl1Sm1F-_jUkdV:39
  - python:S3776: AZ-BJmyl1Sm1F-_jUkdW:281
- ci/tools/update-python-version.py
  - python:S6353: AZ-BJmyc1Sm1F-_jUkdE:32, AZ-BJmyc1Sm1F-_jUkdF:33,
    AZ-BJmyc1Sm1F-_jUkdG:34, AZ-BJmyc1Sm1F-_jUkdH:36,
    AZ-BJmyc1Sm1F-_jUkdI:36, AZ-BJmyc1Sm1F-_jUkdJ:36,
    AZ-BJmyc1Sm1F-_jUkdK:36, AZ-BJmyc1Sm1F-_jUkdL:36,
    AZ-BJmyc1Sm1F-_jUkdM:36, AZ-BJmyc1Sm1F-_jUkdN:36
  - python:S5713: AZ-BJmyc1Sm1F-_jUkdO:232
  - python:S3776: AZ-BJmyc1Sm1F-_jUkdP:262, AZ-BJmyc1Sm1F-_jUkdQ:568
  - python:S1066: AZ-BreDOltpcPPRUrDMN:470
- tests/ci_security/test_update_python_version.py
  - python:S5778: AZ-BJmv31Sm1F-_jUkdC:208

### Historical PR #39 preconditions and reproduction

- The retained inventory is for SonarQube Cloud project
  Easton97-Jens_ModSecurity-test-Framework and pull request 39.
- The local remediation is limited to the six affected Framework files.
- Hosted confirmation requires a submitted remediation head and a fresh
  SonarQube Cloud PR analysis for that exact head.

Use the retained query command:

rtk proxy python3 -c 'import json, urllib.request; data=json.load(urllib.request.urlopen("https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-test-Framework&pullRequest=39&issueStatuses=OPEN%2CCONFIRMED&sinceLeakPeriod=true&ps=500")); print(data["total"])'

Read /var/tmp/codex/ModSecurity-conector/runs/20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8/evidence/sonar-pr39-initial-inventory.md
and compare SHA-256 f9feb36fe34055f6c17f47ed0011803d70b3128a2104d483bad9b01be54dcddd.
After authorized submission, repeat the query for the exact head and verify
that all original keys are absent.

### Historical PR #39 evidence

| Field | Initial SonarQube Cloud inventory |
| --- | --- |
| Run ID | 20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8 |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8/evidence/sonar-pr39-initial-inventory.md |
| Artifact type | markdown |
| SHA-256 | f9feb36fe34055f6c17f47ed0011803d70b3128a2104d483bad9b01be54dcddd |
| Command | rtk proxy python3 -c 'import json, urllib.request; data=json.load(urllib.request.urlopen("https://sonarcloud.io/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-test-Framework&pullRequest=39&issueStatuses=OPEN%2CCONFIRMED&sinceLeakPeriod=true&ps=500")); print(data["total"])' |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-21T04:40:00Z |
| Retention status | retained |

| Field | Sealed local security diff scan |
| --- | --- |
| Run ID | security-diff-ee513e45-20260721t042538z |
| Artifact path | /var/tmp/codex/ModSecurity-conector/codex-security-scans/ModSecurity-test-Framework/ee513e45_20260721T042538Z.UwIsr9/report.md |
| Artifact type | sealed_codex_security_diff_scan_report |
| SHA-256 | 23e40aeb939a82f90c02662c02817775177cc9467cb6dc22857f6a7aed2e986c |
| Command | Codex Security diff review of the local PR #39 Sonar code-smell remediation patch; retained report records 0 reportable findings. |
| Working directory | /root/git/ModSecurity-conector |
| Exit code | 0 |
| Observed at | 2026-07-21T04:25:38Z |
| Retention status | sealed_task_evidence |

The second evidence object supports only the local Framework code-change
security review. It is not evidence that a hosted SonarQube Cloud analysis,
Quality Gate, or exact-head key query has completed.

| Field | Framework-specific CPython 3.13.14 qualification |
| --- | --- |
| Run ID | 20260721T055738Z-framework-pr39-delivery-followup-416b152c |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-cpython313-validation.md |
| Artifact type | framework_pr39_cpython31314_local_qualification |
| SHA-256 | 2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30 |
| Command | Framework PR #39 CPython 3.13.14 qualification receipt: hash-locked PyYAML-6.0.3 installation and pip check; 30 direct affected tests; make test-ci-security-contract (89 tests); make check-python-version; make check-github-actions-workflows; make test-workflow-security-contract (7 tests); make check-documentation; python -m compileall -q ci tests; worktree-scoped response-body guard; make lint. |
| Working directory | framework-python-updater |
| Exit code | 0 |
| Observed at | 2026-07-21T06:13:56Z |
| Retention status | retained |

This receipt establishes local qualification only. It does not establish
hosted SonarQube Cloud, GitHub, review, branch-protection, push, or merge
evidence, and it does not change coverage or scanner configuration.

### Historical PR #39 root cause

The initial analysis identified rule-specific maintainability debt in tightly
coupled CI-security checks, Python-version validation, updater metadata
handling, and a unit-test exception assertion. Only a fresh hosted analysis can
show that the original scanner findings no longer reproduce on the submitted
head.

### Historical PR #39 acceptance criteria and validation plan

1. A fresh SonarQube Cloud PR analysis is bound to the exact submitted
   Framework PR #39 remediation head.
2. Every one of the 25 original keys is absent in that exact-head analysis.
3. No NOSONAR, suppression, rule change, Quality Gate change, exclusion,
   false-positive disposition, or risk acceptance is used.
4. The Framework-specific CPython 3.13.14 qualification retains hash-locked
   PyYAML-6.0.3, pip check, 30 direct affected tests, 89 make
   test-ci-security-contract tests, workflow and documentation checks, python
   -m compileall -q ci tests, the response-body guard, and make lint.
5. SHA-addressed evidence and English, German, index, backlog, and roadmap
   records remain synchronized.

Review the exact submitted diff, retain the
20260721T055738Z-framework-pr39-delivery-followup-416b152c
Framework-specific CPython 3.13.14 qualification receipt, obtain the current
FND-SONAR-0009 user decision selecting and authorizing the external CI and
SonarQube Cloud coverage-authentication scope and owner, then observe the
fresh hosted analysis, query the complete original key set, and inspect
scanner and project configuration history for prohibited control changes.
Do not treat the local qualification receipt as hosted SonarQube Cloud,
GitHub, review, branch-protection, push, or merge evidence.

### Historical PR #39 regression and legitimate-control tests

Regression tests:

- tests/ci_security/test_framework_ci_security_contract.py
- tests/ci_security/test_python_version_contract.py
- tests/ci_security/test_update_python_version.py

Legitimate controls:

- Valid CI-security contract inputs remain accepted while invalid workflow or
  context inputs remain rejected.
- Valid Python-version workflow and release metadata inputs retain their
  acceptance and failure behavior.
- The updater retains strict metadata parsing, check-only non-writing behavior,
  and controlled atomic update behavior.

### Historical PR #39 dependencies, blockers, related findings, and residual risk

- Dependencies: FND-SONAR-0009, a current user decision selecting and
  authorizing the external CI and SonarQube Cloud coverage-authentication scope
  and owner, an authorized Framework submission, and a fresh SonarQube Cloud
  PR analysis for that exact head.
- Blocked by: FND-SONAR-0009 requires that current user decision before
  delivery can continue; exact-head hosted SonarQube Cloud confirmation has not
  yet been observed after that decision and an authorized submission.
- Related findings: FND-FRAMEWORK-0033, FND-FRAMEWORK-0037,
  FND-FRAMEWORK-0038, FND-FRAMEWORK-0039, and FND-SONAR-0009.
- Residual risk: one or more original keys could remain open or a new
  task-owned issue could appear until FND-SONAR-0009 receives its required
  current user decision and the exact submitted head has a fresh hosted
  analysis. No risk is accepted, and neither the local CPython 3.13.14
  qualification nor the local security scan waives the exact-head hosted
  requirement.

### Historical PR #39 history

| At | Event | Detail |
| --- | --- | --- |
| 2026-07-21T04:48:27Z | framework_pr39_code_smell_remediation_finding_created | Allocated as a distinct Framework P2 non-security SonarQube Cloud finding after SHA-256 verification of the retained initial 25-key inventory. Local remediation is fixed; all original keys still require fresh exact-head hosted confirmation without scanner-control changes. |
| 2026-07-21T06:13:56Z | framework_pr39_cpython31314_local_qualification_reconciled | The retained receipt 20260721T055738Z-framework-pr39-delivery-followup-416b152c, SHA-256 2825f5278dcf241dcdb8e501fccb85b9f9fc710e5b24406259a396af7cd3ee30, establishes a Framework-specific CPython 3.13.14 virtual environment, hash-locked PyYAML-6.0.3 installation and pip check, 30 direct affected tests, 89 make test-ci-security-contract tests, workflow and documentation checks, python -m compileall -q ci tests, the response-body guard, and make lint. It supersedes the local blocked_environment premise. Status remains fixed; FND-SONAR-0009 still requires the current coverage-authentication user decision, and exact-head hosted SonarQube Cloud confirmation remains pending. |
