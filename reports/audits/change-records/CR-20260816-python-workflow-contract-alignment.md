# Change Record: Python workflow contract alignment

**Language:** English | [Deutsch](CR-20260816-python-workflow-contract-alignment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260816-python-workflow-contract-alignment |
| Date (UTC) | 2026-08-16 |
| Base revision | 4cd60d4fef492fcaa8522b902886bea6e0256f87 |
| Delivery status | A focused Parent Draft PR is authorized for the linked Actions job. No merge, direct master write, force action, bypass, or auto-merge is authorized. |

## Motivation and problem statement

GitHub Actions run 31926824164, job 95115630935, failed only in Run focused
Python version contracts on Parent master 4cd60d4fef492fcaa8522b902886bea6e0256f87.
The current checker reproduced 27 violations: a stale verified-report inventory
identity, six real Python jobs missing canonical interpreter-contract shape, and
two current shell forms outside the scanner's stable static subset. The failure
prevented the requested updater validation from reaching its focused tests.

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
- One task-owned Parent Draft PR is created with exact-head evidence; no merge
  is performed.

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

## Runtime evidence

The original GitHub-hosted failure is retained in the linked run and in the
task evidence root. Local validation demonstrates source and contract behavior
only. No live workflow dispatch, publisher token mint, maintenance-branch
update, merge, or resulting-master proof is claimed.

## Known limitations

GitHub-hosted Actions execution and exact PR checks are not available until the
task-owned Draft PR is pushed. The local check-ci-security-contract suite
skipped four namespace or identity tests because this environment lacks their
required capabilities; the non-skipped controls passed.

## Remaining risks

The strict parser deliberately continues to reject unsupported future shell
forms. The new source shapes are constrained to its static subset, but hosted
execution remains necessary to verify GitHub Actions syntax and repository
policy under the exact PR head. FND-PARENT-0062, FND-PARENT-0162, and
FND-PARENT-0163 cannot move beyond local fixed status until that evidence exists.

## Checks not run and rationale

No live updater dispatch, App-token mint, merge, or resulting-master rerun was
run: the user authorized a new corrective PR, not operational publication or
integration. Full connector runtime matrices are unrelated to these
workflow-contract-only changes. The final bilingual and documentation-link
checks, final diff review, commit, push, and exact-head hosted checks remain
pending and will be recorded from observed results only.

## Final diff and review status

The scoped source change is limited to the linked Actions failure, its direct
workflow-contract coverage, and required bilingual traceability. Local source,
security, and contract checks above pass. The task is not complete until the
Draft PR is created and its exact remote head and applicable hosted checks are
observed; no merge is authorized or implied.
