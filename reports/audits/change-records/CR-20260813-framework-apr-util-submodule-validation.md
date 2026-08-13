# Change Record: Framework APR-util provenance and submodule candidate validation

**Language:** English | [Deutsch](CR-20260813-framework-apr-util-submodule-validation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260813-framework-apr-util-submodule-validation |
| Date (UTC) | 2026-08-13 |
| Base revision | `33973d094b3f0aeb47605f08ced16a4043f643a0` |
| Delivery status | Draft Parent PR [#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280) is open against `master`. Local validation is recorded below; hosted exact-head checks, review, merge, and cross-repository delivery are not asserted. |

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

- Productive Parent APR-util configuration uses the checked-out Framework's
  guarded provenance tuple, rejects direct `APR_UTIL_*` overrides, and validates
  the selected archive, checksum URL, and SHA-256 before cache or build use.
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
rejects every inherited `APR_UTIL_*` value, sources the checked-out Framework
`ci/lib/common.sh`, runs the Framework provenance guards, and emits only the
four shell-quoted APR-util assignments. The Parent Python loader invokes that
fixed bridge through trusted host executables, scrubs shell hooks and `PATH`,
strictly parses the selected tuple, and verifies its canonical HTTPS download
shape and 64-character SHA-256. Runtime component preparation, inventory, and
cache wrapping run the same guard before cache roots or build work. The Parent
does not restore a static fallback pin.

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

## Security impact

The change strengthens two security-relevant boundaries. APR-util provenance is
now taken from the authoritative Framework guard instead of duplicated Parent
pins, and hostile inherited shell state cannot silently override the selected
tuple. Strict archive and digest validation binds cache identity to the guarded
provenance.

Candidate validation continues to treat the Framework candidate as untrusted.
It requires full SHA values, rejects unsafe metadata paths before use, and
reports bounded JSON-escaped diagnostics only on failure. It does not broaden
publisher permissions, Gitlink staging scope, source-write authority, or the
existing isolated validator boundary.

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

## Runtime evidence

No runtime evidence was collected or claimed. No component build, cache
population, connector runtime, or hosted updater execution was used as proof
for this change.

## Checks not run and rationale

- A GitHub-hosted updater validation and PR checks for the eventual exact PR
  head were not yet available when this record was written.
- SonarQube Cloud, review, merge, resulting-`master` validation, and workspace
  restoration are not claimed; the user authorized a Draft PR only.
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
Direct Parent `APR_UTIL_*` overrides now fail early by design, rather than
altering a Framework-owned provenance tuple.

## Remaining risks

The final exact PR head still requires its applicable hosted checks, review,
and protected-branch policy evaluation. Correct APR-util values remain
dependent on the checked-out Framework guard, which is the intended ownership
model. This record deliberately makes no security-scan, hosted, merge, or
cross-repository success claim.

## Final diff and review status

The scoped Parent implementation, focused local tests, security review, and
whitespace checks were observed before delivery. Draft Parent PR
[#280](https://github.com/Easton97-Jens/ModSecurity-conector/pull/280) is open
against `master`; its current exact head and hosted-check state must be queried
after this follow-up record commit. No review, merge, or Parent Gitlink update
is asserted.
