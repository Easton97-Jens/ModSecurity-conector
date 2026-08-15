# Change Record: constrained Framework-style Python patch updater

**Language:** English | [Deutsch](CR-20260815-python-updater-framework-port.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260815-python-updater-framework-port |
| Date (UTC) | 2026-08-15 |
| Base revision | `55e45726a39bebd3f33aea87807419a882cd3ea8` |
| Framework reference | `Easton97-Jens/ModSecurity-test-Framework@3cb33609626ff689c54b6dc0f31fb7e9401fe75e`, `.github/workflows/check-python-version.yml` |
| Delivery status | The user authorized a feature-branch commit, push, and Draft PR only. No `master` push, merge, ready-for-review transition, or auto-merge is authorized or asserted by this record. |

## Motivation and problem statement

The Connector resolver duplicated version parsing in workflow YAML with a
double-escaped raw regular expression. It rejected ordinary valid releases
such as `3.14.6` and `3.14.7` before it could emit candidate outputs. The
legacy publisher also lacked the Framework's complete trusted-event admission,
GitHub App token isolation, current-master rebuild, qualified branch lease,
full Draft-PR identity, and explicit outcome controls.

## Acceptance criteria

- Keep one scheduled updater at `.github/workflows/update-python-version.yml`
  with only `workflow_dispatch` and cron `17 6 * * 1` triggers.
- Provide four separate jobs with read-only resolver/validator, an App-token
  publisher, and an always-running zero-permission outcome job.
- Use the existing strict updater interface rather than a second YAML/shell
  version grammar; cover accepted `3.14.6`/`3.14.7` and rejected `3.14.06`,
  `3.14.-1`, `3.15.0`, and non-ASCII input.
- Publish only `.python-version` through the exact maintenance branch and a
  matching same-repository Draft PR, never directly to `master` and never by
  merge or auto-merge.
- Preserve paired English/German documentation and traceability.

## Implementation decision and rationale

The port adapts the current Framework architecture without modifying Framework
or MRTS. `resolve-python-patch` uses the exact trusted event SHA and the
existing `--check --json` output. `validate-python-patch` independently
installs the candidate interpreter, validates the expected version, installs
the existing hash-locked test dependencies, and runs the focused contracts.

`publish-python-update` keeps its normal `GITHUB_TOKEN` at `contents: read`.
Only this job reads `WORKFLOW_UPDATER_APP_CLIENT_ID` and
`WORKFLOW_UPDATER_APP_PRIVATE_KEY`, then mints the existing pinned GitHub App
token with exactly `contents: write` and `pull-requests: write`. It rejects
unexpected branch/PR combinations; checks same-repository head/base, title,
marker, Draft state, and `auto_merge == null`; rebuilds from current
`origin/master`; stages only `.python-version`; and uses the exact
`--force-with-lease=refs/heads/$UPDATE_BRANCH:$EXPECTED_REMOTE_TIP` form only
for an already verified maintenance branch. The outcome job fails closed on
inconsistent skipped, failed, or successful states and emits bilingual summary
text.

## Security impact

The changed boundary contains GitHub Actions event trust, App credentials,
repository writes, shell/Git commands, and pull-request state. The invariant is
that only a scheduled/manual canonical non-fork `master` event can reach the
App-token publisher; it can affect only the fixed maintenance branch and a
verified Draft PR containing only `.python-version`. It cannot write workflow
files, merge, enable auto-merge, or directly push `master`.

Focused independent review found no validated secret exposure, shell injection,
path traversal, or unauthorized canonical write. It confirmed the escaped
resolver defect as the existing availability finding `FND-PARENT-0046` and
identified the now-addressed admission, lease, current-base, and PR-state
controls.

## Changed files

- `.github/workflows/update-python-version.yml`
- `ci/checks/common/check-python-version-contract.py`
- `tests/test_update_python_version.py`
- `tests/test_python_version_contract.py`
- `tests/test_ci_security_workflows.py`
- `docs/security/ci-security-tooling.md` and `.de.md`
- `docs/build/README.md` and `.de.md`
- this paired Change Record and the paired archive indexes.

## Commands executed and results

| Check | Actual result |
| --- | --- |
| Focused updater/interpreter/version/workflow suite | passed; 85 tests |
| `make check-ci-security-contract` | passed; 103 tests, 4 environment-limited skips; pinned tool inputs validated |
| `python -m compileall -q ci scripts tests` with task-owned pycache root | passed |
| YAML parse of the edited updater workflow | passed |
| `git diff --check` after final documentation/index changes | passed |
| `ci/checks/common/check-python-version-contract.py --json` | blocked by pre-existing, unrelated Parent inventory drift in current `master`; the edited Python jobs were detected without a new local violation |
| `tests.ci_security.test_ci_security_contract` and `tests.security_regression.test_workflow_security_contract` | 16 passed, 2 failed because the existing `all-connectors-no-crs.yml` is absent from both Parent workflow allowlists; no updater change touched that workflow or allowlist |
| `make check-bilingual-docs` and `make check-doc-links` | blocked in the fresh task worktree because its Framework submodule checkout is intentionally absent; failures are all existing Framework link targets |

## Runtime evidence

The evidence is local static/workflow-contract validation only. No GitHub-hosted
candidate run, App-token mint, branch update, Draft PR creation, merge, or
production runtime is claimed here.

## Known limitations

The local evidence cannot establish repository GitHub App configuration,
GitHub-hosted API behavior, or a live candidate update. The task worktree also
intentionally leaves the Framework submodule uninitialized, so repository-wide
Framework link targets are unavailable to documentation checks.

## Remaining risks

GitHub-hosted behavior still needs an observed trusted scheduled/manual run.
The state machine is deliberately fail-closed: missing App configuration,
candidate mismatch, stale branch tip, unexpected PR state, changed path, or
post-publication PR state causes the publisher/outcome to fail rather than
weaken a control. The unrelated baseline inventory/allowlist and uninitialized
submodule documentation-check limitations remain outside this updater change.

## Checks not run and rationale

No GitHub-hosted maintenance workflow was dispatched and no GitHub App token
was minted: the user authorized feature-branch delivery and a Draft PR, not a
live updater run or any merge-related action. Repository-wide documentation
checks were run, but their Framework-owned link targets are unavailable in the
intentionally uninitialized read-only submodule. The broader Python inventory
and workflow-allowlist checks were also run; their failures are separately
tracked current-base drift and not skipped updater checks.

## Final diff and review status

The implementation is limited to the requested updater, its direct contracts,
paired documentation, and traceability. Before delivery, the final scoped diff,
all required local checks, exact feature-branch head, remote destination, and
Draft-PR state must be observed and recorded separately. This record does not
prestate any delivery outcome.
