# Change Record: CR-20261025-sonarqube-multilanguage

**Language:** English | [Deutsch](CR-20261025-sonarqube-multilanguage.de.md)

This record separates implemented configuration, observed local checks, and
Cloud confirmation. It does not claim a verified PR or a successful Cloud scan.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261025-sonarqube-multilanguage |
| Date (UTC) | 2026-10-25 |
| Base revision | `9913026c1feec85a1862d22987689a1ebcef6d97` |

## Motivation and problem statement

The previous automatic Parent analysis reported both an unspecified Python
target version and detected tests without `sonar.tests`. The Parent contains
distributed Python and Go tests alongside C/C++ tests, maintained build scripts,
and configuration. A language-blind test pattern or incomplete compilation
database would silently remove part of the intended analysis. This change
provides one maintainable Parent-wide CI analysis without crossing Framework or
MRTS ownership boundaries.

## Acceptance criteria

- Use a single project, explicit source/test scope, and Python major/minor `3.14`
  derived from the checked-in `3.14.7` pin.
- Preserve all Parent components, four Go module descriptors, and CFamily test
  translation units; document precise exclusions and unsupported formats.
- Use pinned scanner interfaces, least-privilege CI permissions, and coverage
  reports actually generated for the analyzed revision.
- Provide scope-drift checks, equivalent EN/DE guidance, and truthful local
  validation results.
- Before claiming Cloud verification, observe the exact PR-head server task,
  warnings, and Quality Gate. This final criterion is not yet demonstrated by
  the local evidence recorded here.

## Implementation decision and rationale

One CI-based SonarScanner CLI `8.1.0.6389` scan uses
`sonar-project.properties` and immutable scan action `v8.3.0` at
`d209202bc7d53ff1cc128f7f907dac145c9d6ae9`. The organization key
`easton97-jens` was confirmed through the authenticated project API. Cloud
Automatic Analysis was already disabled when inspected; no external setting
was changed. `sonar.scanner.autoconfig.enabled=false` keeps the explicit manual
classification active. CFamily AutoConfig is independent of that setting and
retains all source translation units; existing compilation-database producers
cover only subsets. The C++17 reporting override controls applicable rules, not
compiler flags or proof of a native build.

Python files under `tests/`, distributed connector Python tests, and Go
`*_test.go` files are tests. C/C++ tests and fixtures remain sources because
CFamily does not support `sonar.tests`. Maintained connector `build/` scripts
are retained. Exclusions cover the independent `modules/**` boundary,
SCM-ignored root outputs, generated `reports/testing/generated/**` evidence,
and only YAML files in the three workflow-fixture directories. Their maintained
generators and Python/C fixtures remain included. Generic JSON/YAML analysis
uses the documented opt-in; its real execution still requires scanner evidence.

CI generates four focused native Go coverage profiles inside the corresponding
module, verifies each profile with `go tool cover`, and passes their actual
external paths to the scanner. No placeholder report, Python coverage
dependency, or native C/C++ coverage pipeline is added. Exact test-name guards
prevent a renamed selector from producing a false zero-test success.

## Changed files

- `sonar-project.properties`; `.github/workflows/sonarqube.yml`.
- `ci/checks/analysis/check-sonar-scope.py`; `tests/test_sonar_scope.py`.
- `ci/checks/common/check-python-version-contract.py`;
  `tests/test_python_version_contract.py` (37 normal Python jobs).
- `ci/tooling/security-tools.lock.yml`; `ci/tools/update-workflow-tools.py`;
  `.github/workflows/update-workflow-tools.yml` (central Action lock,
  updater allowlist, and explicit publisher staging).
- `docs/sonarqube-analysis.md`; `docs/sonarqube-analysis.de.md`.
- `docs/README.md`; `docs/README.de.md`.
- `docs/security/ci-security-tooling.md`;
  `docs/security/ci-security-tooling.de.md`.
- This Change Record and its German companion.

No submodule content or Gitlink is changed.

## Commands executed

All local project commands use RTK. `.venv/bin/python` below is the portable
name of the existing Parent interpreter actually selected through its absolute
path. The following are observed results, not inferences from the configuration:

| Command or bounded procedure | Observed result |
| --- | --- |
| `rtk bypass .venv/bin/python ci/checks/analysis/check-sonar-scope.py --json` | Passed on the staged inventory: 1337 source files, 239 tests (216 Python, 23 Go), 136 CFamily translation units, four Go modules. Full scope manifest: `/var/tmp/codex/ModSecurity-conector/analysis/sonar-config-pr/scope-manifest.json`. |
| `rtk bypass .venv/bin/python -m unittest -v tests.test_sonar_scope` | Four scope regression tests passed. |
| `rtk bypass .venv/bin/python -m unittest -v tests.test_sonar_scope tests.test_python_version_contract.PythonVersionContractTest.test_expected_inventory_has_37_normal_jobs_and_one_special_job tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_all_remote_actions_are_immutable_sha_pins tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_all_workflows_default_deny_and_declare_job_permissions tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_workflow_and_lock_yaml_reject_forbidden_indirection tests.ci_security.test_update_workflow_tools.WorkflowToolUpdaterTests.test_all_locked_action_references_are_in_the_publisher_allowlist` | Nine focused tests passed with the existing Parent environment, Python `3.14.4`. This is not evidence of execution with the exact CI pin `3.14.7`. |
| `rtk bypass actionlint .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Passed, exit 0. |
| `rtk bypass zizmor --offline .github/workflows/sonarqube.yml .github/workflows/update-workflow-tools.yml` | Passed, exit 0; no findings, eight diagnostics suppressed by existing configuration. |
| Execute the Go coverage shell block extracted from workflow YAML with local Go `1.27.3` | Four existing one-case tests passed; all four profiles parsed. Package statement coverage was 17.2%, 23.6%, 5.4%, and 6.8%, respectively. These are sparse selected-package measurements, not whole-repository coverage. The complete workflow block was subsequently re-executed with the `-list` guards and per-module profile parsing; exit 0. |
| Full Python-version contract checker, task versus clean base | Both exited 1 with the same 19 diagnostics, byte-identical. No additional Sonar-job diagnostic was introduced. Evidence: `/var/tmp/codex/ModSecurity-conector/analysis/sonar-config-pr/python-contract-task.txt` and `python-contract-baseline.txt`. |
| `rtk bypass git diff --check` | Passed, exit 0 on the integrated task state. |
| `rtk bypass make check-doc-links PYTHON=<Parent interpreter>` | Passed, exit 0, including the post-staging check of new documents. |
| `rtk bypass make check-bilingual-docs PYTHON=<Parent interpreter>` | Passed, exit 0 after correcting the German guide language switch. |

Authenticated Sonar discovery used `/usr/local/bin/sonar-with-env` through RTK;
query CLI `1.10.1` connected successfully. Project identity and disabled
Automatic Analysis were read back. GitHub secret-name discovery confirmed
`SONAR_TOKEN` exists without reading its value or proving its scanner permission.

## Security impact

The scan job has only `contents: read`; default workflow permissions are empty.
Checkout does not persist credentials or initialize submodules. The existing
`SONAR_TOKEN` secret is supplied only to the immutable scanner step. Fork PRs
cannot run the privileged job, and no `pull_request_target` path is introduced.
Scanner signature verification remains enabled. Rules, Quality Gates, secret
values, application authorization, and runtime defaults are unchanged. Workflow
and tooling changes extend the existing central lock and publisher boundaries
instead of bypassing them.

## Runtime evidence

No runtime evidence was collected or claimed. Local configuration checks,
focused unit tests, coverage generation, and workflow static analysis do not
qualify hosted connector behavior.

## Known limitations

CFamily AutoConfig infers host options; it does not reproduce every independent
connector build, generated header, define, or optional profile. Headers require
an including translation unit. Cross-translation-unit and whole-project rules
may lose precision when independent executables share one project. The shell
template `connectors/apache/build/apxs-wrapper.in` has no confirmed Shell-analyzer
recognition. Other host configuration and build formats do not all have
dedicated semantic analyzers.

Python and C/C++ coverage and test-execution-report imports are not provided.
The four Go profiles cover selected existing tests only. Local Python `3.14.4`
and Go `1.27.3` differ from CI pins `3.14.7` and `1.27.1`; exact-pin execution
requires hosted CI. Existing baseline Python-contract inconsistencies remain.

## Remaining risks

The existing `SONAR_TOKEN` may still lack valid analysis permission. External
Automatic Analysis must stay disabled to avoid competing scan modes. New
analyzer/configuration warnings, baseline code findings, or a failed Quality
Gate may appear in the real scan; none is suppressed or accepted by this change.
Scope-check success alone does not prove that each analyzer processed every
scoped file or that the two original Cloud warnings have disappeared.

## Checks not run and rationale

The bilingual and post-staging link checks passed. Independent static review found no actionable correctness or security issue in the configuration, workflow, scope checker, or updater integration.
The staged scope enumeration and guarded Go coverage block have passed. A real hosted scan, exact-head
server completion, warning readback, and Quality Gate are not yet available
before PR delivery. A local scanner was not launched: the mandatory
`/usr/local/bin/sonar-with-env` launches the query CLI, not an arbitrary scanner.
No host-native build or runtime qualification was required for this configuration
change. No empty reports or substitute passing results were generated.

## Final diff and review status

Configuration and CI integration are implemented. Scope enumeration, the nine
focused tests, guarded Go coverage, workflow lint, bilingual documentation,
links, and diff checks passed. Independent static review found no actionable
correctness/security issue. The full Python workflow checker still has exactly
the same 19 baseline diagnostics. No unrelated change, secret, submodule content,
or Gitlink is included. No commit, PR number, merge, Cloud analysis ID, or gate
success is invented here. The PR description and task evidence must record
exact-head hosted outcomes before claiming `verified_pr`.
