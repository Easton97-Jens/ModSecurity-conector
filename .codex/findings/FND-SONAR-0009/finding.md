# FND-SONAR-0009 — Framework PR #39 Model-1 same-repository coverage workflow is locally implemented; hosted SonarQube Cloud coverage remains externally blocked

## Classification

| Field | Value |
| --- | --- |
| ID | FND-SONAR-0009 |
| Category | sonarqube_finding |
| SonarQube Cloud classification | coverage_configuration |
| Repository / ownership | framework / sonarqube_configuration |
| Priority / severity / confidence | P1 / not_applicable / validated |
| Lifecycle status / feasibility | blocked / blocked_external_dependency |
| Release blocker / security relevant | true / true |
| Profile | Framework PR #39 Model 1 same-repository SonarQube Cloud coverage |
| Final disposition | null |

## Summary, observed behavior, and impact

The user selected Model 1. The Framework worktree now contains a local
same-repository pull-request workflow that runs focused hash-locked tests under
Coverage.py, produces transient Cobertura XML, and invokes the fixed
SonarQube Cloud scanner. The local implementation is complete, but the
finding remains blocked, not fixed or verified.

The retained initial PR #39 observation was 0.0% Coverage on New Code. The
final post-master combined direct suite passed 23 tests in 31.756s: 14
CI-security-evidence-contract tests and 9 workflow-security tests. The generic
workflow checker, the CI-security contract checker, the CI-security
evidence-contract checker, selected syntax compilation, and `make lint` also
passed. `make lint` included 90 CI-security tests, documentation checks, and
`git diff --check`.

Those local results cannot establish project token configuration, the switch
from automatic to CI-based analysis, GitHub Actions execution, scanner/import
execution, hosted coverage, a hosted Quality Gate, or exact-head delivery.
The distinct local CPython _sqlite3 blocker prevents local Cobertura XML and is
tracked in FND-HOST-0006. It must not be conflated with the hosted
configuration blocker.

## Actual Model-1 Framework scope and trust boundary

| Kind | Actual Framework path or symbol |
| --- | --- |
| Workflow | .github/workflows/ci-security-coverage.yml |
| Generic workflow control | ci/checks/security/check-github-actions-workflows.py |
| CI-security control | ci/checks/security/check-ci-security-contract.py |
| Evidence-contract control | ci/checks/security/check-ci-security-evidence-contract.py |
| Evidence-contract test | tests/ci_security/test_ci_security_evidence_contract.py |
| Workflow-security test | tests/security_regression/test_workflow_security_contract.py |
| Locked coverage dependency | requirements-ci.lock, coverage==7.15.2 |
| Evidence-contract symbols | same_repository_sonar_coverage_errors, same_repository_sonar_coverage_job_errors, same_repository_sonar_coverage_producer_errors |

The workflow is limited to a same-repository pull request, checks out the
exact pull-request head without persisted credentials, uses runner-local
coverage paths, and scopes SONAR_TOKEN only to the reviewed fixed scanner
action. Its local controls do not prove that a usable token exists in the
hosted project.

## Actual final local validation

All commands below ran in:

~~~text
/var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater
~~~

After normal synchronization with `origin/master`
`f73f8842f45318e2df8aff1d31855eeb7c20a22f`, local HEAD was merge commit
`0b0c20f686fcc2fd76a7035daf691bc17566d2e1`; `origin/master...HEAD` was
`0 5`, and task changes were restored unstaged after the merge.

| Check | Result |
| --- | --- |
| Combined direct suites | exit 0; Ran 23 tests in 31.756s; OK |
| Generic workflow checker | exit 0; output includes ok ci-security-coverage.yml |
| CI-security contract checker | exit 0; CI security contract passed. |
| CI-security evidence-contract checker | exit 0; CI security evidence contract passed. |
| Selected Model-1 checker syntax | exit 0 |
| Final `make lint` | exit 0; includes 90 CI-security tests, documentation checks, and `git diff --check` |

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-refactor-pycache .venv/bin/python -m unittest -v tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-checkers-pycache .venv/bin/python ci/checks/security/check-github-actions-workflows.py --workflow-root .github/workflows --check all
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-checkers-pycache .venv/bin/python ci/checks/security/check-ci-security-contract.py --root .
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-checkers-pycache .venv/bin/python ci/checks/security/check-ci-security-evidence-contract.py --root .
~~~

~~~text
rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/tmp/model-one-refactor-pycache .venv/bin/python -m compileall -q ci/checks/security/check-github-actions-workflows.py ci/checks/security/check-ci-security-evidence-contract.py
~~~

~~~text
make lint
~~~

These are direct local checks only. They are not hosted scanner, report-import,
Quality-Gate, or delivery evidence.

## Evidence and reproduction

| Field | Initial coverage observation | Local Coverage.py blocker receipt |
| --- | --- | --- |
| Run ID | 20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8 | 20260721T055738Z-framework-pr39-delivery-followup-416b152c |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T044827Z-framework-pr39-sonar-remediation-56e8f9d8/evidence/sonar-pr39-initial-inventory.md | /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-coverage-sqlite-blocker.md |
| Artifact type | markdown | coverage_validation_blocker_receipt |
| SHA-256 | f9feb36fe34055f6c17f47ed0011803d70b3128a2104d483bad9b01be54dcddd | 15d6518ccdb7015622df3bda5d0d1c0c4726096e3e4a392314786b448157cf9e |
| Working directory | /root/git/ModSecurity-conector | /var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater |
| Exit code | 0 | 1 |
| Observed at | 2026-07-21T04:40:00Z | 2026-07-21T07:41:04Z |
| Retention | retained | retained |

The local blocker receipt records this exact Coverage.py command:

~~~text
.venv/bin/python -m coverage run -m unittest -v tests.ci_security.test_framework_ci_security_contract tests.ci_security.test_python_version_contract tests.ci_security.test_update_python_version tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract
~~~

It exited 1 before tests because coverage.sqldata imports sqlite3, whose
standard-library import then failed with ModuleNotFoundError for _sqlite3.
The receipt exists at the recorded external path and its SHA-256 was verified.
It is retained, not a fabricated Cobertura report.

### Renewed delivery-preflight receipt

The secret-safe renewed receipt is retained at
`.codex/runs/20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2/evidence/framework-pr39-renewed-sonar-delivery-preflight-receipt.json`.
Its SHA-256 is
`8141302e6bbd8303c7b86e2bdf50f35ebd7e669aaefb9faf9aa1f4d41cde5863`.
The sealed run manifest and non-self-referential hash inventory are
`.codex/runs/20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2/manifest.json`
and
`.codex/runs/20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2/hash-inventory.json`.

| Field | Renewed preflight observation |
| --- | --- |
| Run ID | 20260721T101159Z-framework-pr39-sonar-delivery-preflight-d47e17f2 |
| Framework local HEAD / included `origin/master` | 0b0c20f686fcc2fd76a7035daf691bc17566d2e1 / f73f8842f45318e2df8aff1d31855eeb7c20a22f |
| Remote PR #39 head / state | 0b0c20f686fcc2fd76a7035daf691bc17566d2e1 / draft, `mergeable=true`, and `UNSTABLE` because one check fails |
| Repository Actions secrets | list exit 0 and reported empty; API count 0; no credential value retained |
| Public Sonar setting | inherited `sonar.autoscan.enabled=true` |
| Current PR metrics | no coverage measure returned; only `new_duplicated_lines_density=0.0` |
| New-code issues | 25 `OPEN`/`CONFIRMED` issues |
| Current gate | `OK` on the exact current PR #39 head, with no coverage condition |

The receipt records parent-supplied result summaries only. It does not retain a
raw endpoint response, replay or reconstruct endpoint commands, or invent the
exact older Quality-Gate SHA. The repository Actions-secret result is limited
to the reported repository list and API count; it does not prove that
organization, environment, or other external credential configuration is
absent.

This renewed evidence confirms the existing disposition rather than changing
it: the exact current remote head is available, but no coverage measure or
Model-1 scanner/import run has been observed. Its current `OK` Quality Gate has
no coverage condition. The lifecycle therefore remains `blocked` /
`blocked_external_dependency`, the release blocker remains true, and no risk
is accepted.

## Cause, remediation, acceptance criteria, and validation plan

The original condition had two independent causes. Model 1 remedies the local
workflow/configuration absence as a completed sub-remediation. The remaining
hosted condition is an external
project dependency: the project owner must configure a dedicated
least-privilege SONAR_TOKEN and switch the existing SonarQube Cloud project
from automatic to CI-based analysis. Neither action occurred in this task.

Acceptance requires all of the following:

1. The listed local Model-1 workflow and controls remain passing.
2. The project owner configures a dedicated least-privilege SONAR_TOKEN without
   disclosing its value.
3. The existing project is switched from automatic to CI-based analysis.
4. An exact-head same-repository workflow run produces and imports a nonempty
   Cobertura XML report.
5. The matching fresh SonarQube Cloud analysis exposes the imported coverage
   and its actual Quality Gate result.
6. No threshold reduction, relevant exclusion, suppression, false-positive
   disposition, rule/gate change, or risk acceptance is used.

Validation after the owner action is: rerun the local focused controls; once
FND-HOST-0006 is resolved, rerun the exact local Coverage.py command with the
required CPython 3.13.14 environment; then inspect the exact-head GitHub
Actions run, scanner/import logs, SonarQube Cloud report import, coverage, and
Quality Gate.

## Dependencies, blockers, controls, and residual risk

- Dependencies: project-owner configuration of a dedicated least-privilege
  SONAR_TOKEN; conversion of the existing project from automatic to CI-based
  analysis; an exact-head hosted same-repository workflow; and hosted
  SonarQube Cloud access for verification.
- Blocked by: none of the project-owner token/configuration actions, an
  exact-head Model-1 hosted workflow, scanner/import log, or imported coverage
  result has been observed. The current remote head
  `0b0c20f686fcc2fd76a7035daf691bc17566d2e1` is exact but precedes the
  unstaged local Model-1 source changes; its Quality Gate is `OK` without a
  coverage condition.
- Local legitimate controls: the 23 selected tests, the generic workflow
  checker, the CI-security contract checker, and the CI-security
  evidence-contract checker all passed; the latter controls enforce the
  same-repository guard and single reviewed SONAR_TOKEN scanner-action mapping.
- Related findings: FND-FRAMEWORK-0044, FND-HOST-0006, FND-SONAR-0002, and
  FND-SONAR-0004.

The exact residual trust assumption is: same-repository PR initiators are
authorized for the project analysis token. This is not a risk acceptance. No
hosted configuration, token provisioning, scanner/import execution, coverage
result, Quality Gate, PR delivery, Framework delivery, Parent gitlink update,
or MRTS change is claimed.

## History

| At | Event | Detail |
| --- | --- | --- |
| 2026-07-21T04:48:27Z | framework_pr39_coverage_ingestion_blocker_created | Allocated as a distinct P1 blocked SonarQube Cloud configuration finding after retained evidence confirmed 0.0% Coverage on New Code and no local coverage producer or import path. |
| 2026-07-21T07:54:45Z | model_one_selected_locally_fixed_and_hosted_verification_blocked | The user selected Model 1. Local same-repository implementation and final focused static/direct validation passed. Dedicated least-privilege SONAR_TOKEN configuration and automatic-to-CI-based SonarQube Cloud project conversion remain unobserved external project-owner dependencies. FND-HOST-0006 tracks the distinct local CPython _sqlite3 blocker. |
| 2026-07-21T08:13:50Z | post_master_sync_local_validation_recorded | After normal synchronization with origin/master `f73f8842f45318e2df8aff1d31855eeb7c20a22f`, local HEAD `0b0c20f686fcc2fd76a7035daf691bc17566d2e1` was ahead by five commits. The generic workflow checker, final 23-test combined suite (31.756s), and `make lint` passed. Hosted SONAR_TOKEN/project-analysis prerequisites and FND-HOST-0006 remain unresolved. |
| 2026-07-21T08:22:13Z | lifecycle_reconciled_as_externally_blocked | The canonical lifecycle is `blocked` / `blocked_external_dependency`: no hosted exact-head scan, imported coverage, or hosted Quality Gate was observed. The locally implemented Model-1 workflow is a completed sub-remediation, not a hosted fix or verification. |
| 2026-07-21T10:21:06Z | renewed_remote_delivery_preflight_recorded | Retained secret-safe receipt `8141302e6bbd8303c7b86e2bdf50f35ebd7e669aaefb9faf9aa1f4d41cde5863` records matching Framework local, origin task-branch, and remote PR #39 head `0b0c20f686fcc2fd76a7035daf691bc17566d2e1`, including `origin/master` `f73f8842f45318e2df8aff1d31855eeb7c20a22f`; the PR is draft, `mergeable=true`, and `UNSTABLE` because one check fails. It also records an empty reported repository Actions-secret list/API count 0, inherited `sonar.autoscan.enabled=true`, no coverage measure (only `new_duplicated_lines_density=0.0`), 25 `OPEN`/`CONFIRMED` new-code issues, and current `OK` Quality Gate without a coverage condition. It does not verify imported coverage. |
