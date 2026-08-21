# Change Record: Parent-only workflow maintenance bundle

**Language:** English | [Deutsch](CR-20260821-parent-only-workflow-maintenance-bundle.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260821-parent-only-workflow-maintenance-bundle |
| Date (UTC) | 2026-08-21 |
| Base revision | \`aaeb7c550d8943a584d21f0f5ca5a11cc3706cbf\` |
| Delivery status | The existing Parent-only pull request [#311](https://github.com/Easton97-Jens/ModSecurity-conector/pull/311) is the sole delivery vehicle. Applicable hosted checks must pass for its exact current head before any verified or merge claim; merge is not authorized. PRs #306–#308 are not modified or closed by this task. |

## Motivation and problem statement

The user requires one Parent-only workflow-maintenance operation, rather than
separate partial Action updates that can omit a related CodeQL component or the
central lock and make CI red.

## Acceptance criteria

- One updater owns GitHub-Action and locked workflow-tool maintenance; the
  legacy checker/updater workflows and scripts are retired.
- A candidate updates the central lock together with every reviewed matching
  Action reference, including every CodeQL \`init\`, \`analyze\`, and
  \`upload-sarif\` suffix occurrence.
- The candidate covers every Parent \`.github/workflows/*.yml\` file explicitly,
  so a newly added local-only wrapper cannot be forgotten silently.
- Dependabot does not create separate \`github-actions\` update PRs; its existing
  Python dependency updates remain enabled.
- The maintenance boundary is Parent-only: no recursive submodule checkout,
  Framework/MRTS path, module token, external remote, Gitlink update, or
  external-module PR path remains.
- A failed candidate application restores its allowed files byte-for-byte, and
  Action identity matching is exact rather than substring-based.

## Implementation decision and rationale

- Removed \`check-actions-versions.yml\`, \`update-actions-versions.yml\`, their
  Python scripts and tests, and their legacy branch/report ignore rule.
- Made \`update-workflow-tools.yml\` the single canonical four-job resolver,
  validator, publisher, and outcome workflow. Its publisher is explicitly
  gated to the canonical Parent repository, non-fork default \`master\` branch,
  and a successful resolver result.
- Disabled only Dependabot's \`github-actions\` ecosystem entry. The one central
  lock and updater now prepare a complete candidate instead of accepting three
  independent partial PRs.
- Hardened \`ci/tools/update-workflow-tools.py\` with exact remote Action parsing,
  full Parent workflow-inventory equality, explicit inclusion of the
  local-only \`all-connectors-no-crs.yml\` wrapper, and rollback across every
  allowed update file.
- Tightened native workflow pin tests to resolve each remote \`owner/repo\` to
  its exact central-lock SHA. The regression suite proves a CodeQL candidate
  changes its central lock plus all ten \`init\`/\`analyze\`/\`upload-sarif\`
  references as one unit.
- Removed the obsolete common-scaffold assertion for the retired legacy updater
  test and made the Parent-only maintenance regression reject that stale
  reference going forward.
- Corrected the stale hard-coded Python inventory after retiring the two legacy
  jobs: 36 normal and 40 total Python-executing workflow jobs. The regression
  now also asserts that both retired workflow-job identifiers remain absent.

## Security impact

The retired legacy updater checked out submodules recursively, accepted a
module token, derived a submodule remote, and could write or open a PR outside
the Parent repository. Its removal eliminates that validated privilege and
repository-boundary violation. The remaining updater stays allow-listed,
fail-closed, SHA-pinned, and uses the single Parent candidate boundary.

A separate medium-confidence hardening follow-up retains explicit response and
archive-size limits for release metadata/assets. It does not justify retaining
the retired module path or splitting updates, and is tracked separately as
\`FND-PARENT-0205\`.

## Changed files

- \`.github/dependabot.yml\`
- \`.github/workflows/update-workflow-tools.yml\`
- \`.github/workflows/test-common.yml\`
- \`.gitignore\`
- \`ci/checks/common/check-python-version-contract.py\`
- \`ci/tools/update-workflow-tools.py\`
- \`docs/build/README.md\` and \`README.de.md\`
- \`docs/security/ci-security-tooling.md\` and \`.de.md\`
- \`tests/ci_security/test_ci_security_contract.py\`
- \`tests/ci_security/test_update_workflow_tools.py\`
- \`tests/security_regression/test_workflow_security_contract.py\`
- \`tests/test_ci_security_workflows.py\`
- retired legacy Actions-maintenance workflows, scripts, and tests
- `tests/test_python_version_contract.py`
- this paired Change Record and paired archive indexes

## Commands executed

| Check | Actual result |
| --- | --- |
| \`tests.test_ci_security_workflows\` | passed: 28 tests |
| \`tests.ci_security.test_update_workflow_tools\` | passed: 37 tests, including the full CodeQL bundle and rollback controls |
| \`tests.ci_security.test_ci_security_contract\` | passed: 13 tests |
| \`tests.security_regression.test_workflow_security_contract\` | passed: 5 tests |
| \`make check-ci-security-contract\` | passed: 122 tests, 5 expected capability skips, and locked tool metadata validation |
| \`make check-python-version-contract\` | passed: Python 3.14.7 and 40 Python-executing workflow jobs |
| Parse all workflow YAML | passed |
| `tests.test_hostruntime_workflow_evidence_contract`, `tests.test_collect_hostruntime_preflight_evidence`, and `tests.test_python_version_contract` | passed: 30 tests after the Python-inventory correction |
| `python3 ci/checks/common/check-python-version-contract.py` | passed: Python 3.14.7 and 40 Python-executing workflow jobs |
| `make check-ci-security-contract` (current local successor) | passed: 122 tests, 5 expected capability skips, and locked tool metadata validation |
| actionlint with ShellCheck | passed |
| offline zizmor | passed: no findings; 86 existing suppressions honored |
| `make check-bilingual-docs` | blocked only by pre-existing missing targets in the intentionally uninitialized Framework Gitlink; this paired record passes its required-section checks |

## Runtime evidence

The updater's synthetic candidates exercised the real copied-tree contract.
One valid CodeQL candidate changes the central lock and every reviewed
init/analyze/upload-sarif reference; an injected later write failure restores
each allowed file. No live maintenance dispatch, token mint, external module
write, or submodule initialization was performed.

## Known limitations

No Framework or MRTS source, Gitlink, submodule state, token, module remote,
legacy Dependabot PR, or merge is modified. \`make check-bilingual-docs\` remains
blocked by pre-existing missing targets inside the intentionally uninitialized
Framework Gitlink; the task does not initialize or alter that separate
repository. Hosted checks on the exact successor head of PR #311 remain
required before any verified or merge claim.

## Remaining risks

The local correction is not verified until the exact successor PR #311 head
passes applicable hosted checks and, after an authorized merge, the original
controls pass on resulting master. The separate medium-confidence response/
asset/archive resource-limit hardening follow-up is retained as FND-PARENT-0205.

## Checks not run and rationale

No live maintenance workflow dispatch, GitHub App token mint, external module
write, submodule initialization, PR #306–#308 mutation, or merge was run. Each
would exceed the Parent-only maintenance scope or require separate authority.

## Final diff and review status

The local source, test, workflow, and security review is complete. Hosted
checks are evaluated only against the exact current PR #311 head; the task
does not authorize a merge. The follow-up only corrects the Python
workflow-inventory test contract and does not modify the separate NGINX
workflow. The task does not claim that PRs #306–#308 are closed, merged, or
superseded remotely.
