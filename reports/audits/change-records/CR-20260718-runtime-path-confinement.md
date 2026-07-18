# Change Record: Runtime path-confinement hardening

**Language:** English | [Deutsch](CR-20260718-runtime-path-confinement.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-runtime-path-confinement` |
| Date (UTC) | `2026-07-18` |
| Base revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0026` |
| Boundary | Parent runtime-path policy and lifecycle resolver only; Framework and MRTS unchanged. |

## Motivation and problem statement

`REPO_ROOT`, `CONNECTOR_ROOT`, and `FRAMEWORK_ROOT` were treated as writable
project anchors by the Parent runtime-path helper. Setting them to `/` could
therefore authorize `/etc/evidence-escape` and `/root/evidence-escape`.
The lifecycle resolver also accepted narrow-looking bases below system-owned
locations and resolved symlinks into `/root` without an invocation-root
containment check. The readiness report repeated the mutable project-root
exception.

## Acceptance criteria

- Mutable project-root values cannot authorize system paths or broaden the
  runtime allowlist.
- Broad, system-owned, traversal, and symlink-resolved lifecycle bases are
  rejected.
- Each of the five lifecycle writable bases remains inside one validated,
  canonical invocation root.
- The resolver records that invocation root in its structured output.
- Canonical checkout and `/src` paths remain available only as read-only source
  paths; they are not writable runtime roots.
- Existing narrow external configuration, including
  `MATRIX_ROOT=/var/tmp/codex/ModSecurity-conector/matrix`, remains supported.

## Implementation decision and rationale

The Parent helper now derives repository source roots from its own canonical
module location and ignores mutable project-root environment values for write
authorization. It rejects broad, system, `/root`, and source roots for runtime
writes, while separately recognizing canonical source paths as read-only.

`resolve-runtime-paths.py` requires `--invocation-root`, validates it as a
narrow external root, and verifies that evidence, build, raw-run, log, and
cache bases are all descendants before it emits shell assignments. The Parent
No-CRS lifecycle caller passes `CANONICAL_VERIFIED_RUN_ROOT` explicitly.

The stricter single-invocation binding is intentionally applied to the
canonical lifecycle resolver rather than forcing every legacy configurable
runtime root below `VERIFIED_RUN_ROOT`. Repository evidence shows that
`MATRIX_ROOT=/var/tmp/codex/ModSecurity-conector/matrix` is a legitimate,
narrow external configuration. Generic runtime roots are still individually
validated as non-broad, non-system, and non-source locations.

The readiness reporter derives its accepted source roots from the already
validated `VERIFIED_SOURCE_ROOT` and `SOURCE_ROOT` defaults. A later
`runtime-env.sh` value is checked against those roots; it cannot mint an
additional source location. This preserves the documented narrow external
source-root control without restoring a mutable-project-root exception.

## Changed files

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/common/resolve-runtime-paths.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/checks/evidence/check-runtime-producer-readiness.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_runtime_path_policy.py`
- `tests/test_resolve_runtime_paths.py`
- `tests/test_runtime_producer_readiness_path_policy.py`
- `reports/audits/change-records/CR-20260718-runtime-path-confinement.md`
- `reports/audits/change-records/CR-20260718-runtime-path-confinement.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command | Result |
| --- | --- |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_path_policy.RuntimePathPolicyTest.test_mutable_project_roots_cannot_authorize_system_runtime_paths tests.test_runtime_path_policy.RuntimePathPolicyTest.test_broad_runner_parent_cannot_expand_runtime_allowlist tests.test_resolve_runtime_paths.ResolveRuntimePathsTest.test_rejects_broad_system_and_symlink_base_escapes` | failed before the fix as expected: mutable `/` project roots, broad `RUNNER_TEMP`, system bases, and a symlink resolving under `/root` were accepted. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_producer_readiness_path_policy` | failed before the readiness-report fix as expected: `connector_root=/` authorized `/etc/evidence-escape`. |
| Focused 13-test Parent `unittest` selection covering `tests.test_runtime_producer_readiness_path_policy`, `tests.test_resolve_runtime_paths`, and the new runtime-path-policy tests | passed after the fix. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_producer_readiness_path_policy tests.test_runtime_path_policy.RuntimePathPolicyTest.test_mutable_project_roots_cannot_authorize_system_runtime_paths tests.test_runtime_path_policy.RuntimePathPolicyTest.test_broad_runner_parent_cannot_expand_runtime_allowlist tests.test_runtime_path_policy.RuntimePathPolicyTest.test_verified_runtime_paths_reject_broad_or_system_writable_roots tests.test_runtime_path_policy.RuntimePathPolicyTest.test_python_path_policy_selftest_accepts_only_writable_run_paths tests.test_resolve_runtime_paths` | passed: 16 focused tests. The new control accepts a canonical narrow external source root; a system override and a different safe sibling remain blocked. |
| `rtk make check-runtime-producer-readiness` | expected `BLOCKED` because required NGINX, Apache, and HAProxy components and caches are absent; every reported runtime path, including `SOURCE_ROOT=/var/tmp/codex/ModSecurity-conector/source`, passed confinement. |
| `rtk env TMPDIR=<task-owned-temp-root> PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_bilingual_docs` | passed: 11 bilingual-documentation checker tests. |
| `rtk sh -n ci/runtime/lifecycle/run-no-crs-baseline.sh` and `rtk git diff --check` | passed. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_runtime_path_policy` | blocked by the isolated worktree: `modules/ModSecurity-test-Framework/ci/lib/common.sh` is absent, so the existing shell half of the checker cannot run. The Python-only self-test passed. |

## Security impact

The corrected boundary prevents environment-controlled project roots, broad
temporary parents, system-root descendants, and symlink escapes from being
treated as writable runtime evidence locations. A structured resolver output
now carries the selected invocation root, and a readiness report no longer
accepts a caller-provided project root as a write exception.
It also cannot turn its false rejection of a canonical narrow source root into
a reason to bypass runtime readiness: only canonical validated source roots
are accepted, while later overrides remain fail-closed.

## Runtime evidence

Not applicable. The validation is side-effect-free path-policy and resolver
coverage; no connector host, traffic, CRS, MRTS, or protocol runtime run was
started or claimed.

## Known limitations

The existing full shell policy self-test cannot run in this isolated worktree
until the separate Framework checkout is available at its recorded path. This
does not authorize a Framework modification. The original draft PR #58 head
`4f028f911807def8b771faaa3b16c58a513e0385` had 33 passing GitHub checks,
including CodeQL and SonarQube Cloud. This record accompanies a focused
follow-up, so its new exact head requires a fresh CI/quality review before any
`verified_pr` claim.

## Remaining risks

The policy validates path identity and confinement; it does not prove host
filesystem permissions or establish runtime-host evidence. A separately
configured narrow external root remains a configuration boundary, while the
canonical lifecycle resolver retains the stricter invocation-root binding.

## Checks not run and rationale

No connector build, host runtime, protocol run, CRS/MRTS matrix, or Framework
change was run by this remediation. The original draft PR #58 was committed,
pushed, and checked; the current follow-up is intentionally not treated as
delivered until its own exact-head CI, CodeQL, SonarQube Cloud, and review
cycle completes. No merge is authorized.

## Final diff and review status

Focused local regression coverage, the 11-test bilingual checker, shell syntax,
and final whitespace-diff validation passed. The full shell policy check remains
blocked only by the absent Framework checkout. The original implementation was
delivered through draft PR #58; this source-root follow-up remains
`remediation_required` until the new exact PR head is pushed and independently
verified. No merge occurred.
