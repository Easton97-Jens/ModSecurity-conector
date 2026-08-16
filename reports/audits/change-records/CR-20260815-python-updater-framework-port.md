# Change Record: constrained Framework-style Python patch updater

**Language:** English | [Deutsch](CR-20260815-python-updater-framework-port.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260815-python-updater-framework-port |
| Date (UTC) | 2026-08-15 |
| Base revision | `55e45726a39bebd3f33aea87807419a882cd3ea8` |
| Framework reference | `Easton97-Jens/ModSecurity-test-Framework@3cb33609626ff689c54b6dc0f31fb7e9401fe75e`, `.github/workflows/check-python-version.yml` |
| Delivery status | On 2026-08-16 the current user explicitly authorized protected integration of Parent PR #295 into `master`. The pre-integration evidence is recorded below; no direct `master` push, force action, bypass, or auto-merge is authorized or asserted. |

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

Focused independent review found no validated secret exposure, path traversal,
or unauthorized canonical write. The first GitHub-hosted ZiZmor run on the
Draft-PR head reported direct template expansion of the publisher's `changed`
output in a shell guard. The final revision bridges that output through an
environment variable, accepts only literal `true`, and has a regression
contract; focused local ZiZmor then reported no findings. The review also
confirmed the escaped resolver defect as the existing availability finding
`FND-PARENT-0046` and identified the now-addressed admission, lease,
current-base, and PR-state controls.

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
| Offline ZiZmor against `update-python-version.yml` | passed after the environment-bridge remediation; no findings (six repository suppressions) |
| `python -m compileall -q ci scripts tests` with task-owned pycache root | passed |
| YAML parse of the edited updater workflow | passed |
| `git diff --check` after final documentation/index changes | passed |
| `ci/checks/common/check-python-version-contract.py --json` | blocked by pre-existing, unrelated Parent inventory drift in current `master`; the edited Python jobs were detected without a new local violation |
| `tests.ci_security.test_ci_security_contract` and `tests.security_regression.test_workflow_security_contract` | 16 passed, 2 failed because the existing `all-connectors-no-crs.yml` is absent from both Parent workflow allowlists; no updater change touched that workflow or allowlist |
| `make check-bilingual-docs` and `make check-doc-links` | blocked in the fresh task worktree because its Framework submodule checkout is intentionally absent; failures are all existing Framework link targets |

## Pre-integration delivery evidence

- Current user authorization (2026-08-16): “bringe ihn in den master rein”.
  It selects only the task-owned Parent PR #295 and no Framework, MRTS, direct
  `master` push, force action, administrator bypass, or auto-merge action.
- PR: [#295](https://github.com/Easton97-Jens/ModSecurity-conector/pull/295),
  `fix/port-framework-python-updater` to `master`, same repository, with
  initial implementation commit `640a622c0a3ffc245f42cda60350f817555da08c`
  and scanner-remediation commit
  `bbf906aa17d6e866d6e37557c279fe5d0c50dd13`.
- Before this traceability follow-up, local, `origin`, and PR metadata agreed
  on source head `bbf906aa17d6e866d6e37557c279fe5d0c50dd13`; the base was
  `55e45726a39bebd3f33aea87807419a882cd3ea8`, the PR was open/Draft, cleanly
  mergeable, and had `autoMergeRequest = null`.
- The active `Protect master` ruleset permits a PR with zero approving reviews
  but requires resolved review threads and current-head `actions`,
  `bounded-c-cpp`, `envoy-go`, `traefik-go`, `actionlint`, and `zizmor` checks.
  The source head passed every listed context; it also passed SonarCloud,
  CodeQL, OSV, secret scanning, and the remaining applicable PR checks. There
  were zero submitted reviews and zero review threads, so no required review
  or conversation was outstanding.
- This follow-up adds the required Delivery/Change-Record linkage. Its new PR
  head and newly triggered checks must be re-read from the authoritative PR
  before the exact-head-protected squash merge; the final head and merge facts
  are retained in PR and integration evidence rather than invented here.

## Runtime evidence

The Draft PR supplies a GitHub-hosted workflow-lint signal; its initial ZiZmor
run identified the direct shell-template expansion described above. No
GitHub-hosted maintenance candidate run, App-token mint, maintenance-branch
update, merge, or production runtime is claimed here.

## Known limitations

The local evidence cannot establish repository GitHub App configuration,
GitHub-hosted API behavior beyond the observed lint result, or a live candidate
update. The task worktree also intentionally leaves the Framework submodule
uninitialized, so repository-wide Framework link targets are unavailable to
documentation checks.

## Remaining risks

GitHub-hosted behavior still needs an observed trusted scheduled/manual run.
The state machine is deliberately fail-closed: missing App configuration,
candidate mismatch, stale branch tip, unexpected PR state, changed path, or
post-publication PR state causes the publisher/outcome to fail rather than
weaken a control. The unrelated baseline inventory/allowlist and uninitialized
submodule documentation-check limitations remain outside this updater change.

## Checks not run and rationale

No GitHub-hosted maintenance workflow was dispatched and no GitHub App token
was minted: the current user now authorizes only the protected integration of
PR #295, not a live updater run. Repository-wide documentation checks were
run, but their Framework-owned link targets are unavailable in the intentionally
uninitialized read-only submodule. The broader Python inventory and
workflow-allowlist checks were also run; their failures are separately tracked
current-base drift and not skipped updater checks.

## Final diff and review status

The implementation is limited to the requested updater, its direct contracts,
paired documentation, and traceability. At this traceability update the PR
remains Draft until its corrected head has passed a fresh verification round.
The current user authorizes only the subsequent protected, exact-head squash
merge of PR #295; this record neither authorizes a direct `master` push nor
auto-merge. The final scoped diff, exact final PR head, remote destination,
checks, merge result, and resulting-master evidence must be observed before
they are reported.
