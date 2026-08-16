# Change Record: Python workflow contract alignment

**Language:** English | [Deutsch](CR-20260816-python-workflow-contract-alignment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260816-python-workflow-contract-alignment |
| Date (UTC) | 2026-08-16 |
| Base revision | 4cd60d4fef492fcaa8522b902886bea6e0256f87 |
| Delivery status | The current user explicitly authorized remediation of task-owned PR #296 and protected integration into `master`. The merge remains conditional on fresh exact-head review, checks, SonarQube Cloud evidence, ruleset compliance, and resulting-master verification; direct master writes, force actions, bypasses, and auto-merge remain prohibited. |

## Motivation and problem statement

GitHub Actions run 31926824164, job 95115630935, failed only in Run focused
Python version contracts on Parent master 4cd60d4fef492fcaa8522b902886bea6e0256f87.
The current checker reproduced 27 violations: a stale verified-report inventory
identity, six real Python jobs missing canonical interpreter-contract shape, and
two current shell forms outside the scanner's stable static subset. The failure
prevented the requested updater validation from reaching its focused tests.

The Draft PR's first exact-head hosted analysis reported one task-owned New
Issue despite a passing Quality Gate: `python:S1192` at
`ci/checks/common/check-python-version-contract.py:104` asks to deduplicate
`update-workflow-tools.yml` across its existing publisher, resolver, and
validator inventory entries. The current user explicitly asked for this issue
to be fixed and the corrected task-owned PR to reach `master`.

## Acceptance criteria

- The stale verified-report identity is removed while the single
  report-governance workflow topology remains unchanged.
- Each of the six real Python jobs is explicitly inventoried and uses the
  immutable setup-python action, id setup-python, canonical .python-version,
  and exact verifier before Python or pip.
- The CodeQL Go guard and submodule path allowlist are parser-safe while
  retaining their exact restrictive semantics.
- The real Python contract checker, focused unit/security contracts, actionlint,
  and offline ZiZmor checks pass without a parser suppression or control
  weakening.
- The exact PR head has zero open task-owned SonarQube Cloud New Issues without
  a suppression, issue acceptance, `NOSONAR`, exclusion, or Quality-Gate
  relaxation.
- The user-authorized PR #296 integration uses the repository-approved
  protected workflow and receives resulting-master verification.

## Implementation decision and rationale

The correction removes only the obsolete FND-PARENT-0062 inventory identity and
adds exactly the six detected normal Python job identities, changing the
explicit normal inventory from 33 to 38 jobs. It inserts only the existing
immutable setup-python and verifier shape in the affected workflows, retaining
their triggers, permissions, tokens, and publisher state machines.

The parser itself remains fail-closed. The CodeQL Bash regular-expression guard
is expressed as an exact static awk validation, including a one-line input
requirement. The submodule publisher replaces a dynamic case arm with the same
fixed-string, whole-line path allowlist. These decisions address
FND-PARENT-0062, FND-PARENT-0162, and FND-PARENT-0163 without broad exceptions.

The Sonar follow-up adds the closed constant
`UPDATE_WORKFLOW_TOOLS_WORKFLOW` and replaces only the three repeated filename
literals. The `JobIdentity` values, inventory order/cardinality, parser,
setup/verifier checks, and fail-closed rejection paths remain unchanged. This
addresses local finding `FND-SONAR-0042` with source-native remediation rather
than a scanner shortcut.

## Changed files

- .github/workflows/ci-security-codeql.yml
- .github/workflows/test-apache.yml
- .github/workflows/test-haproxy.yml
- .github/workflows/update-submodules.yml
- .github/workflows/update-workflow-tools.yml
- ci/checks/common/check-python-version-contract.py
- tests/test_python_version_contract.py
- tests/test_ci_security_workflows.py
- this paired Change Record and its paired archive indexes

## Commands executed

| Check | Actual result |
| --- | --- |
| Current-master pre-fix checker | passed as a reproduction of failure: exit 1, 43 detected jobs, 27 violations |
| Real checker after fix | passed: status valid, 42 detected jobs, 0 violations |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-python-version-contract | passed |
| Focused Python contract/interpreter/CI-security suite | passed: 59 tests |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract | passed: 103 tests, 4 environment-limited skips, pinned-tool validation passed |
| python -m compileall -q ci scripts tests with task-owned pycache | passed |
| actionlint for all .github/workflows YAML files | passed |
| Offline ZiZmor for the five changed workflow files | passed: no findings, 24 repository suppressions |
| git diff --check before this record | passed |
| Public SonarQube Cloud PR #296 issue query before the follow-up | passed as static reproduction: exactly one OPEN `python:S1192` at `ci/checks/common/check-python-version-contract.py:104` |
| Focused `tests.test_python_version_contract` after the constant-only follow-up | passed: 24 tests, including the 38-entry inventory and fail-closed negative controls |
| Real checker after the constant-only follow-up | passed: status valid, 42 detected jobs, 0 violations |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-python-version-contract after the follow-up | passed |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract after the follow-up | passed: 103 tests, 4 environment-limited skips, pinned-tool validation passed |
| python -m compileall -q ci/checks/common tests/test_python_version_contract with external pycache | passed |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs | blocked: exit 2 only because the intentionally uninitialized Framework submodule leaves pre-existing referenced files absent; no changed Change-Record path is reported |
| make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-doc-links | blocked: exit 2 for the same pre-existing absent Framework-submodule targets; no changed Change-Record path is reported |
| git diff --check after source and documentation follow-up | passed |

## Security impact

The affected boundary is GitHub Actions workflow selection, Python interpreter
provenance, static shell recognition, and a submodule maintenance publisher.
The fix preserves immutable action pins, least privilege, read-only checkout
credentials, the exact path allowlist, Draft-PR state controls, and fail-closed
rejection of unknown shell syntax. No credential, token, workflow permission,
trigger, direct master write, merge, or auto-merge behavior is added or widened.

No exploit or unauthorized write is claimed. FND-PARENT-0162 and
FND-PARENT-0163 are security-relevant CI-contract findings because a broad
workaround would weaken the existing safety boundary.

`python:S1192` itself is a maintainability finding, not a vulnerability. The
constant-only extraction does not change trusted inputs, accepted jobs,
permissions, triggers, tokens, publisher behavior, or any security decision.

## Runtime evidence

The original GitHub-hosted failure is retained in the linked run and in the
task evidence root. Local validation demonstrates source and contract behavior
only. No live workflow dispatch, publisher token mint, maintenance-branch
update, merge, or resulting-master proof is claimed.

## Known limitations

The first hosted check set belongs to the predecessor exact head. A new commit
requires a fresh PR-head SonarQube Cloud analysis and all applicable hosted
checks before merge. The local check-ci-security-contract suite skipped four
namespace or identity tests because this environment lacks their required
capabilities; the non-skipped controls passed.

## Remaining risks

The strict parser deliberately continues to reject unsupported future shell
forms. The new source shapes are constrained to its static subset, but hosted
execution remains necessary to verify GitHub Actions syntax and repository
policy under the exact PR head. FND-PARENT-0062, FND-PARENT-0162, and
FND-PARENT-0163 cannot move beyond local fixed status until that evidence exists.
The exact issue `AaAJBpj4Kije7nS9rbMB` remains open until successor-head
analysis proves the constant-only repair.

## Checks not run and rationale

No live updater dispatch or App-token mint was run; those operational actions
are outside this static inventory repair. Full connector runtime matrices are
unrelated. Commit, push, a fresh exact-head hosted check set, protected merge,
resulting-master workflows, and workspace restoration remain pending and will
be recorded from observed results only. The complete bilingual/documentation-
link checks were run but are blocked by the intentionally uninitialized
Framework submodule's pre-existing referenced paths; this repair does not
modify Framework or suppress the checks.

## Final diff and review status

The scoped source change is limited to the linked Actions failure, its direct
workflow-contract coverage, the one SonarQube Cloud duplicate-literal follow-up,
and required bilingual traceability. Local source, security, syntax, and
contract checks above pass. The task is not complete until the successor exact
remote/PR head, hosted checks, Sonar disposition, protected merge,
resulting-master checks, and safe Parent restoration are observed.
