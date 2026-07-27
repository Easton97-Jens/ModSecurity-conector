# Change Record: Parent runtime-matrix cache owner-root hand-off

**Language:** English | [Deutsch](CR-20260726-runtime-matrix-cache-owner-root.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260726-runtime-matrix-cache-owner-root |
| Date (UTC) | 2026-07-26 |
| Base revision | 6ca7e1536ce7e93da68099db9c586b88852ff13e |
| Boundary | Parent runtime-matrix and prepared runtime-environment-snapshot hand-offs, Parent regression tests, and this English/German Change Record pair/index. The carried Framework Gitlink is already merged on Parent `master`; no Framework or MRTS source changes are made here. |
| Finding linkage | FND-CROSS-0008; FND-PARENT-0056; FND-CROSS-0001 remains open until fresh legitimate runtime evidence passes the strict terminal gate. |

## Motivation and problem statement

The full Parent runtime matrix keeps its per-job `BUILD_ROOT` for logs,
temporary files, results, and isolated connector execution. Cache-backed Apache
and NGINX connector builds are not owned by that job root, however. The runner
now derives one narrow owner root from the verified component cache:

```text
CONNECTOR_COMPONENT_CACHE/builds/connectors
```

It validates both that root and each Apache/NGINX build path before invoking
the connector. A cache-backed path outside the derived root is rejected before
`make` runs. For an accepted path, the runner supplies the same explicit root
as `APACHE_BUILD_OWNER_ROOT` or `NGINX_BUILD_OWNER_ROOT`; it does not widen
`BUILD_ROOT` and does not disable the Framework deletion guard.

The direct `runtime-matrix-all-runtime` target reaches the Framework runner
through a prepared invocation-local runtime-environment snapshot. That
snapshot now publishes the same narrow owner root for both connectors, so the
direct runner cannot fall back to its unrelated job `BUILD_ROOT` during a
legitimate cache refresh.

Parent PR #125 already carries Framework commit
`a7ebf5a1d9cad2b0a65a7603476a1434fdb16cf6`, which includes the Framework
NGINX owner-root capability. This change consumes that capability through the
Parent-owned matrix boundary; it does not alter the Gitlink beyond the normal
branch update from `master`.

## Acceptance criteria

- Apache and NGINX cache-backed refreshes receive the same explicit owner root
  derived from `CONNECTOR_COMPONENT_CACHE/builds/connectors`.
- A connector build path outside that narrow root fails before `make` is
  invoked.
- The isolated per-job `BUILD_ROOT` remains separate from the cache owner root.
- The invocation-local runtime-environment snapshot publishes the same narrow
  Apache and NGINX owner roots for direct runtime-matrix execution.
- On a hosted producer failure, the bounded NGINX `configure` log is emitted
  only from its fixed expected path after the existing regular-file and
  non-symlink check.
- No deletion guard, strict evidence gate, SonarQube Cloud policy, or branch
  protection is relaxed.
- The updated exact PR #74 head still requires its full hosted producer,
  terminal-gate, SonarQube Cloud, review, and protected-integration evidence.

## Implementation decision and rationale

The affected sink is the Framework refresh-deletion guard. The enforced
invariant is that a refresh target must be an absolute, safe generated path
under the explicit connector-cache build owner root. The Parent check uses the
Framework canonical-path containment helper before dispatch; the Framework
guard still rejects unsafe, relative, symlinked, sibling, or system paths at
the deletion boundary.

Legitimate prepared cache builds remain refreshable. A non-cache build root is
now rejected instead of reaching a connector provisioning path with unrelated
ownership. The Parent snapshot, rather than a mutable shared export or an
implicit `BUILD_ROOT` default, carries the connector-specific authority into
the direct Framework runtime runner. No cleanup, `REFRESH` disablement,
suppression, Quality Gate change, or branch-protection bypass is used.

## Changed files

- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`: derives, validates, and
  dispatches the narrow connector-cache owner root for Apache and NGINX.
- `ci/provisioning/components/prepare-runtime-components.py`: supplies the
  same narrow owner root while building cache entries and in the prepared
  invocation-local runtime environment snapshot.
- `tests/test_full_matrix_cache_owner_root.py`: controlled same-boundary
  positive and outside-owner rejection tests, plus direct runtime-matrix
  snapshot propagation coverage.
- `tests/test_runtime_component_cache_contract.py`: verifies both connector
  build provisioners receive the narrow owner root.
- `.github/workflows/verified-report-governance.yml`: retains the existing
  bounded failure-summary helper and applies it to the fixed NGINX `configure`
  log path, so a later source-build failure has its actionable diagnostic.
- `tests/test_ci_security_workflows.py`: verifies that the NGINX log remains
  on the same regular-file/non-symlink and command-masking diagnostic path.
- `modules/ModSecurity-test-Framework`: the normal merge from current Parent
  master carries its already-integrated Gitlink.
- `reports/audits/change-records/README.md`, `README.de.md`, and this paired
  Change Record.

## Commands executed

- `sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_full_matrix_cache_owner_root`
  — passed (three tests). The controls invoke the real matrix shell runner and
  the direct Framework runtime-matrix runner through the controlled
  invocation-local snapshot. They verify explicit Apache and NGINX owner roots
  while `REFRESH=1`; the negative control verifies rejection before `make`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_runtime_component_cache_contract`
  — passed (27 tests), including cache-provisioner owner-root assertions.
- `git diff --check` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_ci_security_workflows`
  — passed (20 tests), including the bounded NGINX failure-diagnostic control.
- `make check-ci-security-contract` — passed (20 workflow-security tests and
  validation of the pinned actionlint, zizmor, and gitleaks tools).

## Security impact

This is a path-containment correction at the Parent-to-Framework hand-off. It
keeps a cache build within its declared owner root and preserves the Framework
deletion guard as the final fail-closed sink. No trusted boundary is broadened.

The follow-up failure diagnostic uses no discovery, glob, or derived log path.
It tails at most 300 lines from the fixed `$BUILD_ROOT/logs/nginx/nginx-configure.log`
only when that path is a regular non-symlink, inside the existing
`::stop-commands::` boundary. It does not expose credentials, enable a
privileged workflow, or affect the NGINX build command.

## Runtime evidence

The controlled regressions invoke the real Parent full-matrix shell runner and
the direct Framework runtime-matrix runner through the same invocation-local
snapshot boundary used by the hosted producer. They are not native connector
builds, host deployments, or complete runtime-evidence producers; those remain
required on the updated exact PR #74 head.

## Known limitations

The local controls replace `make` only at the final connector smoke boundary,
so they do not claim an Apache or NGINX build. Framework's corresponding
owner-root deletion controls were separately merged and validated. The
previous exact-head hosted producer exposed the missing direct snapshot
handoff; the strict Parent evidence gate must now run again on the successor
#74 head.

The predecessor head reached the NGINX source-build `configure` command rather
than the prior owner-root guard, but its failure summary omitted that command's
fixed log. The new bounded diagnostic is necessary to classify the remaining
source-build failure; it is not a claim that the NGINX runtime producer passes.

## Remaining risks

FND-CROSS-0008 and FND-CROSS-0001 remain open until the hosted exact-head
producer demonstrates legitimate cache-backed evidence through the strict
gate. No risk is accepted.

## Checks not run and rationale

No local full connector build or real host/runtime matrix is claimed. It needs
the authoritative hosted producer environment and remains required for the
updated exact Parent PR #74 head, together with the strict terminal evidence
gate, SonarQube Cloud issue/duplication readback, reviews, and protected merge
preconditions.

No Framework or MRTS source test or modification is part of this Parent change.
Framework owner-root controls were independently merged before this hand-off.

## Final diff and review status

The local diff is limited to the Parent matrix/snapshot hand-offs, focused
regression tests, the normal master Gitlink update, and this bilingual
record/index. It has passed focused security/path and cache-provisioner tests;
the broader local checks and fresh exact-head hosted validation must be rerun
for the successor commit before protected merge.

## Continuation: ready NGINX snapshot Common-source hand-off

The bounded exact-head NGINX `configure` log on Parent #74 identifies the
remaining failure: `MSCONNECTOR_COMMON_SRC` is present during managed-cache
preparation but absent from the later invocation-local snapshot used by the
direct runtime matrix. Parent now derives the value only from the resolved,
reviewed `CONNECTOR_ROOT/common/src` and publishes it for a ready NGINX entry.
It does not forward a job-supplied value, introduce a fallback, widen either
cache owner root, or alter the Framework missing-source fail-closed behavior.

`tests/test_runtime_env_snapshot_contract.py` verifies that a ready NGINX
entry publishes exactly that Common source root and a blocked entry publishes
no NGINX runtime values. The direct matrix fixture also proves that the
Framework runner receives the value through the same sourceable local snapshot
boundary as the owner roots. The focused command
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_runtime_env_snapshot_contract tests.test_full_matrix_cache_owner_root tests.test_runtime_component_cache_contract`
passed all 38 tests. This is not native NGINX success: the new exact Parent PR
#74 head still requires its hosted producer, strict terminal gate, SonarQube
Cloud readback, review/protection evidence, and protected integration.

## Continuation: exact CI interpreter identity and all-core visibility

Hosted Parent PR #74 head
`ef0b6ab27162e9735e9ff9d8beb3516446eed1ff` created the intended
hash-locked `verified-report-python` venv and installed Framework
`PyYAML==6.0.3`, but exported the bare selector `PYTHON=python3`. The Parent
Makefile, verified-run dispatcher, and Framework runtime runner correctly
forward that selector; it can nevertheless resolve outside the venv when a
later runtime helper changes `PATH`. The exact hosted run `30222002129` / job
`89845969175` consequently failed at
`update-runtime-snapshot.py` with `ModuleNotFoundError: No module named
'yaml'`. The failed strict producer remains rejected; this is additional
cause evidence for `FND-CROSS-0001`, not successful runtime evidence.

The workflow now retains the `PATH` convenience export but passes the exact
created interpreter as `PYTHON=$venv/bin/python`, after a direct `import yaml`
check. This preserves the verified setup-python, hash lock, `--only-binary`,
`--require-hashes`, no-write permission, and fail-closed import contracts; it
does not change Framework source, its lock, MRTS, or a Gitlink.

The full-matrix runner already derives its default cap from `nproc`, then
`getconf _NPROCESSORS_ONLN`, then `1`; a fixed workflow value would disable
that host-aware behavior. Its new read-only
`--print-effective-parallelism` mode reports the real selected cap and whether
it is auto-detected or explicit, before any Python process, runtime path,
build, port, or matrix action. The workflow invokes that mode visibly before
the strict producer, and the normal scheduling message keeps the same source
marker.

Changed continuation files:

- `.github/workflows/verified-report-governance.yml`
- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`
- `tests/test_ci_security_workflows.py`
- `tests/test_full_matrix_parallel_scheduler.py`
- `docs/reference/variables.md` and `docs/reference/variables.de.md`
- this paired Change Record

Actual focused validation after this continuation:

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_ci_security_workflows tests.test_full_matrix_parallel_scheduler` — passed, 32 tests. It proves the workflow retains its hash-locked dependency contract, exports the exact venv interpreter rather than the bare selector, invokes the visible diagnostic, rejects no existing workflow-security control, and exercises auto-detected/explicit cap diagnostics plus normal scheduler behavior.

The final exact-head hosted `report-governance`, terminal evidence gate,
SonarQube Cloud readback, review/thread, and protected-merge checks are not
yet run for this successor commit. The local result is therefore
`remediation_required`, not a claim that `FND-CROSS-0001` is fixed or that the
PR can be merged.

The local `check-python-interpreter-contract.py` control is
`blocked_environment`: this task venv is CPython 3.14.4 while `.python-version`
requires 3.14.6, and its shell cannot model the `actions/setup-python` PATH.
It is not substituted with a different interpreter; the successor hosted
workflow remains the authoritative compatibility control.
