# Change Record: Framework APR-util provenance and submodule candidate validation

**Language:** English | [Deutsch](CR-20260813-framework-apr-util-submodule-validation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260813-framework-apr-util-submodule-validation |
| Date (UTC) | 2026-08-13 |
| Base revision | `33973d094b3f0aeb47605f08ced16a4043f643a0` |
| Delivery status | Draft Parent PR [#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280) is open against `master`. The task-owned SonarCloud S8707 result was observed on head `3fbba306ddedf86acd3d01929a077cee33f66ed7`; completed local `GITHUB_ENV` containment hardening and its local validation are documented below. This follow-up record will create a later PR head, for which fresh hosted Sonar analysis remains pending. Review, merge, and cross-repository delivery are not asserted. |

## Motivation and problem statement

Parent duplicated a static APR-util version, archive URL, SHA-256, and checksum
URL even though the checked-out Framework owns the approved APR-util
provenance. That duplication could drift from the authoritative Framework
tuple, and inherited `APR_UTIL_*` environment values could blur the ownership
boundary.

The submodule-updater validator also treated its deliberate checkout of a
Framework candidate SHA as a Parent source mutation. At that point the Parent
index correctly still contains the current Gitlink, while the Framework
worktree intentionally contains the candidate. A parent-wide status check
therefore rejected valid candidate validation before the later source-inventory
baseline could distinguish the expected transition from an actual mutation.

## Acceptance criteria

- Productive Parent APR-util configuration rejects direct `APR_UTIL_*`
  overrides. A full canonical tuple may propagate only internally between
  Parent and Child after an independent comparison with the checked-out
  Framework; partial, empty, mismatched, or alternate tuples fail closed
  before cache or build use. Parent owns no APR-util version or SHA-256.
- Cache identities include the authoritative APR-util provenance inputs.
- The updater accepts an unchanged candidate as a no-op and a valid forward
  descendant, while rejecting malformed, wrong-ref, non-descendant, or
  historically malformed Gitlink candidates.
- Candidate-state validation permits only the expected Framework candidate
  checkout transition and fails closed for Parent, Framework, or initialized
  nested-submodule mutations and unsafe metadata paths.
- English and German reader documentation and Change Records describe the same
  behavior. Framework and MRTS source, the Parent Gitlink, and any merge stay
  out of scope.

## Implementation decision and rationale

`ci/tools/print-framework-apr-util-env.sh` is a fixed `/bin/sh` bridge. It
records and clears inherited `APR_UTIL_*` state, sources the checked-out
Framework `ci/lib/common.sh`, runs the Framework provenance guards, and emits
only the four shell-quoted APR-util assignments. The Parent Python loader
invokes that fixed bridge through trusted host executables, scrubs shell hooks
and `PATH`, strictly parses a full canonical tuple, and independently compares
the captured input with the checked-out Framework result. Only an absent input
or a matching non-empty full tuple may propagate internally between Parent and
Child; partial, empty, mismatched, or alternate tuples fail closed. The
canonical HTTPS download shape and 64-character SHA-256 are revalidated before
use. Runtime component preparation, inventory, and cache wrapping run the
same guard before cache roots or build work. The Parent owns no APR-util
version or SHA-256 and does not restore a static fallback pin.

`ci/tools/validate-submodule-candidate-state.py` captures a deterministic
Parent baseline before candidate checkout, then validates the exact candidate
state after checkout. It validates full immutable revisions, parent HEAD,
hooks and `.gitmodules` fingerprints, the recorded Framework Gitlink, tracked,
staged, and untracked state outside the Framework worktree, Framework
cleanliness, and recursively initialized nested-submodule state. Unsafe
absolute, traversal, or pathspec-magic metadata is rejected before Git or path
operations. The workflow calls this helper around the existing isolated
validator so the expected candidate worktree/Gitlink difference is no longer a
false mutation while all other mutations remain fail-closed.

The completed local `GITHUB_ENV` containment hardening in remediation commit
`646eec7edf3165c1bc8b82273c1fd5490738fc11` addresses the path from
the workflow's `--github-env "$GITHUB_ENV"` argument through
`capture_parent_baseline`, `_open_github_environment_file`, and the final
`os.fdopen(..., "a")` baseline write. Before that sink is opened, the helper
requires a normalized absolute target strictly below `RUNNER_TEMP`, traverses
every directory through descriptors opened with `O_NOFOLLOW`, and requires
each directory to be owned by the effective user and not group- or
world-writable. The final target must be a one-link regular file owned by the
effective user, not group- or world-writable, and is opened for append with
`O_NOFOLLOW | O_NONBLOCK` relative to the verified directory descriptor.
`O_NONBLOCK` prevents a FIFO from blocking the write path, while the regular-
file check rejects it. Every failed invariant returns `GITHUB_ENV_INVALID`
before the baseline is written.

## Security impact

The change strengthens two security-relevant boundaries. APR-util provenance is
now taken from the authoritative Framework guard instead of duplicated Parent
pins, and hostile inherited shell state cannot silently override the selected
tuple. A full canonical tuple may cross the internal Parent/Child boundary
only after independent Framework comparison; partial, empty, mismatched, and
alternate tuples fail closed. Strict archive and digest validation binds cache
identity to the guarded provenance.

Candidate validation continues to treat the Framework candidate as untrusted.
It requires full SHA values, rejects unsafe metadata paths before use, and
reports bounded JSON-escaped diagnostics only on failure. It does not broaden
publisher permissions, Gitlink staging scope, source-write authority, or the
existing isolated validator boundary.

At PR #280 head `3fbba306ddedf86acd3d01929a077cee33f66ed7`, the task-owned
SonarCloud result reported S8707 for this `GITHUB_ENV` write path. This record
does not classify that result as a false positive and does not claim a
suppression. The containment implementation is complete locally; fresh hosted
Sonar analysis is pending only after the follow-up commit creates its new PR
head.

## Changed files

The Parent changes are:

- workflow/build integration: `.github/workflows/ci-security-workflow-lint.yml`,
  `.github/workflows/update-submodules.yml`, `Makefile`, and
  `ci/tools/update-workflow-tools.py`;
- APR-util provenance and cache flow:
  `ci/tools/print-framework-apr-util-env.sh`,
  `ci/provisioning/components/prepare-runtime-components.py`,
  `ci/provisioning/components/prepare-runtime-components.sh`,
  `ci/provisioning/cache/runtime-components-inventory.sh`, and
  `ci/provisioning/cache/with-runtime-components.sh`;
- submodule candidate validation:
  `ci/tools/validate-submodule-candidate-state.py`;
- generated-source and reader documentation:
  `scripts/generate_compiler_guides.py`, `docs/build/compilers/apache.md`,
  `docs/build/compilers/apache.de.md`, `docs/reference/variables.md`, and
  `docs/reference/variables.de.md`;
- tests and fixtures: `tests/test_ci_security_workflows.py`,
  `tests/test_collect_no_crs_source.py`,
  `tests/test_runtime_env_snapshot_contract.py`,
  `tests/test_apr_util_static_contract.py`,
  `tests/test_framework_apr_util_provenance.py`,
  `tests/test_update_submodules_local_git.py`,
  `tests/test_validate_submodule_candidate_state.py`, and
  `tests/fixtures/apr-util-static-allowlist.txt`; and
- this paired Change Record and its bilingual archive index entries.

No Framework or MRTS source, Parent Gitlink, generated runtime report, secret,
or cache artifact is included.

## Commands executed

### Tests and actual results

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned temporary directory> .venv/bin/python -m unittest -v tests.test_ci_security_workflows tests.test_validate_submodule_candidate_state tests.test_update_submodules_local_git tests.test_apr_util_static_contract tests.test_framework_apr_util_provenance tests.test_runtime_env_snapshot_contract tests.test_runtime_component_cache_identity tests.test_prepare_runtime_components` — passed: 116 tests on the shared checkout with the existing checked-out Framework. The copied product files were byte-compared with the external PR worktree.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_apr_util_static_contract` — passed: 5 tests in the external PR worktree, including clean-checkout scan coverage.
- `rtk make check-ci-security-contract` — passed: 74 tests and three expected
  capability skips; the target also validated pinned security-tool lock
  records.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_validate_submodule_candidate_state tests.test_update_submodules_local_git` — passed: 13 tests after the completed local containment hardening.
- `rtk make check-ci-security-contract` — passed: 77 tests and three expected
  skips after the completed local containment hardening.
- The initial hosted Security workflow lint run
  [31710687331](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31710687331)
  at PR head `905555264c46da1742d27110cef05b908c910c4f` failed three local-Git
  candidate-state tests because the cloned fixture submodule did not inherit a
  Git identity. The fixture now configures that local clone explicitly; the
  external PR worktree reran `rtk make check-ci-security-contract` successfully
  (74 tests, three expected capability skips). A fresh hosted exact-head result
  remains pending.
- `rtk make lint` — passed. Its restricted `PATH` did not discover actionlint;
  the separate checksum-verified actionlint invocation with
  `-shellcheck=/usr/bin/shellcheck` passed for workflows and fixtures.
- `rtk make check-compiler-guides`, `rtk make check-variable-documentation`,
  and `rtk make check-bilingual-docs` — passed during the prior
  content-validation round. The external PR worktree also passed
  `check-variable-documentation`; its current `check-bilingual-docs` and
  `check-doc-links` invocation reached the new Change Record without a record
  error but remained blocked by missing Framework link targets because that
  worktree deliberately has no initialized submodule. Shell syntax checks,
  ShellCheck for the new bridge, Python compilation, and `git diff --check`
  also passed.

These are local source, contract, lint, and fixture results. They are not
runtime evidence.

### SonarCloud follow-up

- The task owner observed an S8707 result for the `GITHUB_ENV` write path on
  PR #280 at head `3fbba306ddedf86acd3d01929a077cee33f66ed7`. The descriptor-
  containment implementation is complete locally and the two local commands
  above passed after it. No fresh hosted Sonar analysis was run or observed for
  the later PR head that this follow-up commit will create, so this record
  makes no resolved, clean, false-positive, or suppression claim.
- Local regression coverage for the containment invariant is in
  `ValidateSubmoduleCandidateStateTests.test_capture_rejects_github_env_outside_runner_temp_or_via_symlink` and
  `ValidateSubmoduleCandidateStateTests.test_capture_rejects_missing_runner_temp_and_accepts_runner_file`.
  The cases reject an outside target, lexical traversal, a symlink target, a
  hard link, a symlinked directory, a missing or unsafe `RUNNER_TEMP`, and
  accept a regular runner-owned file. The completed path also opens with
  `O_NONBLOCK`, preventing FIFO blocking while the regular-file invariant
  rejects FIFO targets.

## Runtime evidence

No runtime evidence was collected or claimed. No component build, cache
population, connector runtime, or hosted updater execution was used as proof
for this change.

## Checks not run and rationale

- Fresh GitHub-hosted updater validation and PR checks for the eventual exact
  PR head are pending after the local-Git fixture identity repair.
- S8707 was observed on `3fbba306ddedf86acd3d01929a077cee33f66ed7`. Fresh
  SonarCloud analysis is pending after this follow-up commit creates a later
  PR head. Until that analysis is observed, no hosted-resolved, hosted-clean,
  false-positive, or suppression claim is made.
- Review, merge, resulting-`master` validation, and workspace restoration are
  not claimed; the user authorized a Draft PR only.
- Full component builds and connector runtime matrices were not run because
  their downloads and runtime environments are broader than the provenance and
  workflow contracts changed here.
- Final external-worktree `check-bilingual-docs` and `check-doc-links` are
  blocked by intentionally uninitialized Framework links. Framework policy
  forbids automatically initializing or changing that external submodule in
  this Parent-only delivery task.

## Known limitations

The local Git fixtures exercise resolver and candidate-state behavior but do
not prove GitHub-hosted runner behavior. The bridge requires a checked-out
Framework `common.sh`; that Framework remains externally owned and unchanged.
Direct Parent `APR_UTIL_*` overrides fail early by design, rather than altering
a Framework-owned provenance tuple. Parent owns no APR-util version or
SHA-256; the internally propagated tuple remains valid only after its
independent comparison with the checked-out Framework.

The `GITHUB_ENV` containment hardening is complete locally and has local
regression coverage, but still requires fresh hosted Sonar analysis after the
follow-up commit to establish the hosted disposition of S8707 for its later PR
head.

## Remaining risks

The final exact PR head still requires its applicable hosted checks, review,
and protected-branch policy evaluation. Correct APR-util values remain
dependent on the checked-out Framework guard, which is the intended ownership
model. The pending hosted S8707 disposition for the later PR head is an
additional delivery risk.
This record deliberately makes no security-scan, hosted, merge, or
cross-repository success claim.

## Final diff and review status

The scoped Parent implementation, focused local tests, security review, and
whitespace checks were observed before delivery. Draft Parent PR
[#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280) is open
against `master`; its exact new head and hosted-check state must be queried
after this follow-up record commit. The observed S8707 result belongs to prior
head `3fbba306ddedf86acd3d01929a077cee33f66ed7`; fresh hosted Sonar analysis
is still required for the later follow-up head. No review, merge, or Parent
Gitlink update is asserted.

## Local SonarCloud New-Issues follow-up

This follow-up resolves six SonarCloud New Issues in the local Parent changes.
It updates only the following implementation and focused-test paths:

- `ci/provisioning/components/prepare-runtime-components.py`: the relevant
  regular expression is explicitly ASCII with `re.ASCII`, and the loader
  helpers were refactored without changing their fail-closed behavior.
- `ci/tools/print-framework-apr-util-env.sh`: a shell-quote arity guard rejects
  an invalid quoting result before it is emitted.
- `ci/tools/validate-submodule-candidate-state.py`: the hook inventory logic
  was split into a helper and the `.gitmodules` path is represented by a
  constant.
- `tests/test_framework_apr_util_provenance.py` and
  `tests/test_validate_submodule_candidate_state.py`: focused coverage was
  added or updated for those changes.

Local validation observed for this follow-up:

- the selected validator tests passed: 11 tests;
- the selected APR-util/cache tests passed: 13 tests;
- `rtk make check-ci-security-contract` passed: 78 tests with three expected
  skips;
- `sh -n ci/tools/print-framework-apr-util-env.sh` passed; and
- a sealed local security-diff scan found 0 reportable findings across the
  five changed code/test paths.

These are local results only. No fresh hosted SonarCloud result has been
observed for the follow-up head; hosted analysis remains pending until after
the follow-up is committed and pushed.

## Hosted delivery result (observed before this documentation-only follow-up commit)

This section corrects the earlier pending-hosted-analysis status. Source
remediation commit `2a962b43615b8ff078a00828b1fb3338ce441abd` is the exact PR
head analyzed by SonarCloud at `2026-08-13T15:51:30+0000`: the Quality Gate
reported `OK`, `codeSmells` was `0`, and the API query reported `0` total open
New Issues. The exact-head GitHub check suite was terminal, with no pending or
unsuccessful checks. Draft Parent PR [#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280)
remains open against `master`.

These facts precede this documentation-only follow-up commit, which does not
claim a self-referential final SHA. No merge, auto-merge, Parent Gitlink
update, or Framework/MRTS delivery occurred or is asserted.
