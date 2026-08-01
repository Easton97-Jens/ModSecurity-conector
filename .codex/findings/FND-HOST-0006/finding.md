# FND-HOST-0006 — Task CPython 3.13.14 lacks _sqlite3, blocking local Coverage.py Cobertura XML validation

## Classification

| Field | Value |
| --- | --- |
| ID | FND-HOST-0006 |
| Category | tooling |
| Repository / ownership | host_environment / host_environment |
| Priority / severity / confidence | P2 / not_applicable / confirmed |
| Lifecycle status / feasibility | blocked / blocked_environment |
| Release blocker / security relevant | false / false |
| Profile | Framework PR #39 local CPython 3.13.14 Coverage.py/Cobertura validation |
| Final disposition | null |

## Summary, observed behavior, and impact

The task CPython 3.13.14 environment lacks the standard-library _sqlite3
module. The selected hash-locked coverage==7.15.2 import therefore fails
through:

~~~text
coverage.sqldata -> sqlite3 -> _sqlite3
~~~

The exact local Coverage.py command exited 1 before its selected Framework
tests started with:

~~~text
ModuleNotFoundError: No module named _sqlite3
~~~

No local Cobertura XML was produced, fabricated, uploaded, or retained. This
is a P2 non-security host-environment tooling blocker. It is distinct from
FND-SONAR-0009: this finding is about a local interpreter/build prerequisite,
not a dedicated SONAR_TOKEN, project analysis mode, scanner/import execution,
hosted coverage, or Quality Gate.

## Preconditions, scope, and reproduction

- Framework worktree:
  /var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater
- Required and selected interpreter lane: CPython 3.13.14.
- Locked dependency: coverage==7.15.2.
- The CPython build lacks the SQLite development headers/pkg-config discovery
  required to enable _sqlite3.
- This task explicitly excludes installation, host rebuild, and substitute
  runtime work.

Reproduce only in the selected exact environment:

~~~text
.venv/bin/python -m coverage run -m unittest -v tests.ci_security.test_framework_ci_security_contract tests.ci_security.test_python_version_contract tests.ci_security.test_update_python_version tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract
~~~

The expected current result is exit 1 before tests, not Cobertura XML. Do not
substitute CPython 3.14 or hand-copy an _sqlite3 extension; both invalidate the
exact CPython 3.13.14 hash-locked validation claim.

## Retained evidence

| Field | Value |
| --- | --- |
| Run ID | 20260721T055738Z-framework-pr39-delivery-followup-416b152c |
| Artifact path | /var/tmp/codex/ModSecurity-conector/runs/20260721T055738Z-framework-pr39-delivery-followup-416b152c/evidence/framework-pr39-coverage-sqlite-blocker.md |
| Artifact type | coverage_validation_blocker_receipt |
| SHA-256 | 15d6518ccdb7015622df3bda5d0d1c0c4726096e3e4a392314786b448157cf9e |
| Command | .venv/bin/python -m coverage run -m unittest -v tests.ci_security.test_framework_ci_security_contract tests.ci_security.test_python_version_contract tests.ci_security.test_update_python_version tests.ci_security.test_ci_security_evidence_contract tests.security_regression.test_workflow_security_contract |
| Working directory | /var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater |
| Exit code | 1 |
| Observed at | 2026-07-21T07:41:04Z |
| Retention | retained |

The external artifact exists and its SHA-256 was verified. It is retained
evidence, not an unavailable Parent .codex/runs copy and not a coverage report.

## Cause, remediation, acceptance criteria, and validation plan

The task CPython 3.13.14 build lacks the SQLite development headers/pkg-config
discovery needed to build the standard-library _sqlite3 extension. Because
Coverage.py imports sqlite3 via coverage.sqldata, the coverage command fails
before test execution and cannot create Cobertura XML.

In a separately authorized host-environment task, the safe remedy is to provide
the required SQLite development headers/pkg-config data, build a fresh external
task-owned CPython 3.13.14, create a fresh Framework virtual environment,
install only the hash-locked requirements, verify import _sqlite3, then rerun
the exact command with COVERAGE_FILE and COVERAGE_XML below a fresh external
task run.

Acceptance requires all of the following:

1. The fresh required CPython 3.13.14 environment imports _sqlite3.
2. The selected hash-locked Framework environment imports coverage==7.15.2
   without the coverage.sqldata -> sqlite3 -> _sqlite3 failure.
3. The exact Coverage.py command runs its selected tests and creates a nonempty
   Cobertura XML file below a fresh task-owned external run path.
4. No CPython 3.14 substitute, hand-copied extension, system/user-site
   installation, or unapproved host mutation is used.
5. FND-SONAR-0009 is independently verified through its hosted project/token
   configuration and exact-head scanner/import evidence.

## Dependencies, blockers, controls, and residual risk

- Dependencies: separately authorized host setup with SQLite development
  headers/pkg-config data, a fresh task-owned CPython 3.13.14 rebuild and
  Framework virtual environment, and the Framework hash-locked requirements.
- Blocked by: the selected task CPython 3.13.14 lacks _sqlite3; this task
  prohibits installation, host rebuild, and substitute runtime work; no valid
  local Cobertura XML path exists until the exact environment is rebuilt with
  SQLite support.
- Legitimate controls after a permitted setup: the exact CPython 3.13.14
  interpreter imports _sqlite3, Coverage.py starts the selected tests and writes
  nonempty Cobertura XML, and FND-SONAR-0009 remains separately hosted-tested.
- Related findings: FND-SONAR-0009 and FND-FRAMEWORK-0044.

Local Cobertura XML remains unverified. This is non-security host tooling, not
a claim about hosted GitHub Actions or SonarQube Cloud behavior. No unsafe
workaround, installation, build, configuration change, delivery action, Parent
gitlink update, or MRTS change occurred.

## History

| At | Event | Detail |
| --- | --- | --- |
| 2026-07-21T07:54:45Z | local_coverage_sqlite_blocker_recorded_separately | Allocated as a distinct P2 blocked_environment host_environment tooling finding from the retained exact CPython 3.13.14 Coverage.py import failure. It is not the FND-SONAR-0009 hosted SONAR_TOKEN/project-analysis configuration blocker. |
| 2026-07-26T17:34:26Z | current_sqlite_prerequisite_revalidation | Verified the retained exact-lane receipt SHA-256, while current `pkg-config` cannot locate sqlite3 and `/usr/include/sqlite3.h` is absent. No Framework action, installation, CPython rebuild, substitute runtime, product change, or delivery action occurred; the finding remains `blocked_environment`. Current evidence: run `20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`, SHA-256 `81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`. |
