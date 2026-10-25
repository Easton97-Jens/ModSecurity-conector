# Change Record: CR-20261025-sonarqube-multilanguage

**Language:** English | [Deutsch](CR-20261025-sonarqube-multilanguage.de.md)

> **Historical master #420 snapshot**
> This record retains the original #420 revisions and results. The PR #382 integration uses Python3.15.1/Go1.27.3, the unified active inventory and genuine generic Python/native plus native Go reports; see [current integration](../../../docs/pr-382-merge-readiness.md#integration-of-master-420). Its standalone coverage.py/Go selections below are historical, not an additional automatic catalog.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261025-sonarqube-multilanguage |
| Date (UTC) | 2026-10-25 |
| Base revision | `9913026c1feec85a1862d22987689a1ebcef6d97` |

## Motivation and problem statement

The automatic Parent analysis reported no explicit Python target version and
recognized tests without `sonar.tests`. Distributed tests, independent native
binaries and maintained build/CI scripts need one consistent Parent scan.
The user requires full-repository Sonar analyses for C++20 and C++23 as advisory results, not component-only compiler checks.

## Acceptance criteria

Use Python `3.14` from pin `3.14.7`, preserve all intended Parent components and
four Go modules, keep CFamily tests in source scope, document exclusions and
limits, generate real supported reports, and verify the actual PR revision.
Full-Parent C++20/C++23 Sonar scans must be visible but non-decisive; C++17 remains
authoritative. Do not change submodule contents, rules, or Quality Gates.

## Implementation decision and rationale

Three full-Parent manual SonarScanner CLI `8.1.0.6389` variants use the immutable Action `v8.3.0`
(`d209202bc7d53ff1cc128f7f907dac145c9d6ae9`). Organization `easton97-jens` and
already-disabled Cloud Automatic Analysis were verified through the canonical
wrapper. Explicit scanner autoconfiguration is disabled. CFamily AutoConfig
retains all 136 translation units because existing real compilation-database
producers cover subsets. C++17 reporting rules remain authoritative.

Narrow Python/Go test patterns preserve CFamily tests and maintained connector
`build/` scripts. Exclusions cover independent `modules/**`, root outputs,
`reports/testing/generated/**`, and exact YAML workflow-fixture patterns.
JSON/YAML use the documented opt-in. The validator rejects version/scope drift.

Four pre-existing Go scenarios generate native profiles in their modules.
Coverage `7.17.0` uses an official, hash-pinned universal wheel, Apache-2.0,
Python >=3.11, and no dependencies. A separate external virtual environment
executes the real checker CLI and eight focused unit-test methods, combines
branch data and emits relative-path Cobertura XML. Two unexecuted analysis
scripts remain at genuine zero; no coverage exclusions or fake reports are used.

The PR security contract admits only the exact same-repository predicate and
step-local token on the immutable scanner Action. Generic PR secret bans remain;
negative controls reject guard bypasses, global/shell secrets, other Actions,
and bracket/bare secret-context access. The first scan's three maintainability
findings were addressed by splitting validation responsibilities, removing a
redundant exception class and separating test assertions.

The same complete source/test configuration and Python/Go coverage producers run
in three variants. C++17 uses the required canonical project. C++20/C++23 use
`sonar.cfamily.reportingCppStandardOverride` with separate public projects
`Easton97-Jens_ModSecurity-conector_cpp20_advisory` and
`Easton97-Jens_ModSecurity-conector_cpp23_advisory`. Both projects were manually
created through the canonical wrapper and read back as unbound, Automatic
Analysis false, main branch `master`. Their relevant profile keys and `Sonar way`
gate match the canonical project. A redundant setting-write attempt was rejected
by the API; readback established the already-correct disabled state.

The explicit advisory main-branch parameter avoids canonical PR routing.
`continue-on-error` derives only from the fixed advisory matrix; C++17 remains
required and every scanner still waits for its actual gate. Per-project
serialization and task/SHA summaries retain traceability. No partial source
scope, alternate properties file, per-component compilation database or
compiler-only advisory job remains. The matrix contract and negative gating
control are tested.

## Changed files

- `sonar-project.properties`; `.github/workflows/sonarqube.yml`.
- `ci/checks/analysis/check-sonar-scope.py`; `tests/test_sonar_scope.py`.
- `ci/requirements/sonar-coverage.txt`; `ci/sonar-coverage.ini`.
- `tests/test_ci_security_workflows.py`;
  `ci/checks/common/check-python-version-contract.py`; `tests/test_python_version_contract.py`.
- `ci/tooling/security-tools.lock.yml`; `ci/tools/update-workflow-tools.py`;
  `.github/workflows/update-workflow-tools.yml`.
- `docs/sonarqube-analysis.md`; `docs/sonarqube-analysis.de.md`;
  `docs/README.md`; `docs/README.de.md`;
  `docs/security/ci-security-tooling.md`; `docs/security/ci-security-tooling.de.md`.
- `reports/audits/change-records/CR-20261025-sonarqube-multilanguage.md`;
  `reports/audits/change-records/CR-20261025-sonarqube-multilanguage.de.md`.

No Framework/MRTS content or Gitlink changed.

## Commands executed

All shell procedures used RTK and the existing Parent interpreter selected by
absolute path (Python `3.14.4`), or task-owned external coverage environments.

| Actual command or bounded procedure | Observed result |
| --- | --- |
| `rtk bypass .venv/bin/python ci/checks/analysis/check-sonar-scope.py --json` (Parent interpreter selector) | Passed: 1339 sources, 239 tests (216 Python / 23 Go), 136 CFamily units, four modules. Manifest: `/var/tmp/codex/ModSecurity-conector/analysis/sonar-config-pr/scope-manifest-final.json`. |
| Scoped combined `unittest -v` selection for scope, Python inventory, immutable pins, permissions, YAML, updater allowlist and Sonar secret controls | 21 test methods passed, including all parameterized negative variants; no full default suite was selected locally. |
| Execute the actual Python coverage workflow block extracted from YAML | Passed: isolated binary/hash-required install, real CLI, eight test methods, combine and XML. Checker 91.94% lines, 88.33% branches, 90.76% combined. |
| Execute the guarded Go coverage workflow block extracted from YAML | Passed: four existing one-scenario tests; four valid native profiles. Selected-package statements 17.2%, 23.6%, 5.4%, 6.8%. |
| `rtk bypass actionlint .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Passed. |
| `rtk bypass zizmor --offline .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Passed; no findings, seven existing suppressions. |
| `rtk bypass make check-bilingual-docs check-doc-links PYTHON=<Parent interpreter>` | Passed, including new staged documents. |
| `rtk bypass git diff --check` | Passed. |
| Full Python-version checker compared against unchanged base | Exit 1 in both trees, identical 19 baseline diagnostics; neither new workflow adds a diagnostic. |


The portable `.venv/bin/python` label above denotes the existing Parent
interpreter, not a new environment in the task worktree. Exact current-head
hosted results are recorded in PR #420 rather than inferred from local checks.

## Security impact

The scanner job has only `contents: read`; workflow defaults deny permissions.
Checkout credentials are not persisted. Only the fixed scanner step receives
`SONAR_TOKEN`; fork PRs do not run that job. Signature verification, rules and
Quality Gates remain enabled. Coverage tooling is isolated and hash-pinned.
All variants have read-only GitHub permissions. Only their pinned scanner step receives the existing analysis token; fork PRs are excluded. No production
runtime, authorization or logging behavior changes.

## Runtime evidence

No runtime evidence was collected or claimed. Object compilation, tests,
coverage and static scanning do not qualify hosted connector behavior.

## Known limitations

First scan revision `b3c7785fd7033fc57394c1e4562d627e2b294c4f`, run
`40218724634`, completed server task `AaF0Nx8EdkEpBguA0kbW` successfully as
analysis `8436e500-b997-4b7a-b428-b577aca20a43`. Effective Python `3.14`, explicit
tests and CLI `8.1.0.6389` were read back against that SHA. Both original Python
warnings disappeared; the CE warning list was empty. Its gate failed only on
new-code coverage `0.0 < 80`, leading to genuine Python coverage integration.
This is historical first-head evidence, not final-head gate confirmation.

The scanner fully analyzed all 136 CFamily units with quality score 77.52/100,
loaded four Go reports and executed Python, Go, Shell, Actions, YAML and JSON
sensors. AutoConfig does not reproduce all host builds and disables C/C++ taint
analysis. Header and independent-binary limitations remain. Six existing Shell
parse warnings, ignored Go-test duplication messages and 44 invalid labels in
the saved Python architecture perspective remain documented in the guide.
`warningCount=0` does not imply warning-free scanner logs.

Coverage is focused, not full-repository test execution. C/C++ coverage and
test-execution reports are absent. Static standard variants do not establish native compilation, linking or runtime behavior. Local Python `3.14.4`/Go `1.27.3` differ from CI pins.

## Remaining risks

A project administrator must reconcile the saved `py Intended Model` with the
Parent-only source/test scope; no model or architecture check was removed to
hide warnings. Shell parsing and CFamily fidelity remain analyzer limitations.
Automatic Analysis must stay disabled. Revision `ed2c9c7cb6739f802aba3d842f46e18e9f3d414c` completed canonical task
`AaF0TdarwSmsgR9Bxtvb`, analysis `f474f764-2b07-48dc-9f5e-248f5f891140`,
with gate OK and 90.8% new-code coverage; its current-head CI passed. The final
three-standard matrix still requires fresh hosted project/SHA/gate readback.

## Checks not run and rationale

No full native host build, linking or runtime qualification was required for
this configuration task. No unrelated baseline Python-workflow migration or
historical I12 campaign was run. The first hosted pin/scope/Go steps succeeded;
the final full-repository standard matrix outcomes must be evaluated
at the actual new PR head. Existing gates were not weakened to obtain a pass.

## Final diff and review status

Implementation, focused local tests and bilingual documentation are reviewed.
Independent review validated coverage mapping and secret boundaries; its
alternate-secret-access concern was fixed and negatively tested. Initial
commit `b3c7785fd7033fc57394c1e4562d627e2b294c4f` is published in Draft PR #420;
follow-up changes preserve normal history. No merge or master change occurred.
Final delivery state belongs to exact-head PR evidence, not this pre-push record.
