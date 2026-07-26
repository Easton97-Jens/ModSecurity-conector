# Change Record: Parent runtime-matrix cache owner-root hand-off

**Language:** English | [Deutsch](CR-20260726-runtime-matrix-cache-owner-root.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260726-runtime-matrix-cache-owner-root |
| Date (UTC) | 2026-07-26 |
| Base revision | 6ca7e1536ce7e93da68099db9c586b88852ff13e |
| Boundary | Parent runtime-matrix shell hand-off, a Parent regression test, and this English/German Change Record pair/index. The carried Framework Gitlink is already merged on Parent `master`; no Framework or MRTS source changes are made here. |
| Finding linkage | FND-CROSS-0008; FND-CROSS-0001 remains open until fresh legitimate runtime evidence passes the strict terminal gate. |

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
ownership. No cleanup, `REFRESH` disablement, suppression, Quality Gate change,
or branch-protection bypass is used.

## Changed files

- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`: derives, validates, and
  dispatches the narrow connector-cache owner root for Apache and NGINX.
- `tests/test_full_matrix_cache_owner_root.py`: controlled same-boundary
  positive and outside-owner rejection tests.
- `modules/ModSecurity-test-Framework`: the normal merge from current Parent
  master carries its already-integrated Gitlink.
- `reports/audits/change-records/README.md`, `README.de.md`, and this paired
  Change Record.

## Commands executed

- `sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh` — passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_full_matrix_cache_owner_root`
  — passed (two tests). The positive control invokes the real matrix shell
  runner with a controlled `make` boundary and verifies explicit Apache and
  NGINX owner roots while `REFRESH=1`. The negative control uses an outside
  build root and verifies rejection before `make`.
- `git diff --check` — passed.

## Security impact

This is a path-containment correction at the Parent-to-Framework hand-off. It
keeps a cache build within its declared owner root and preserves the Framework
deletion guard as the final fail-closed sink. No trusted boundary is broadened.

## Runtime evidence

The controlled regression invokes the real Parent matrix shell runner and
observes its connector dispatch environment. It is not a native connector
build, host deployment, or complete runtime-evidence producer; those remain
required on the updated exact PR #74 head.

## Known limitations

The local controls replace `make` only at the final connector smoke boundary,
so they do not claim an Apache or NGINX build. Framework's corresponding
owner-root deletion controls were separately merged and validated. The strict
Parent evidence gate has not yet run on this future #74 head.

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

The local diff is limited to the Parent matrix hand-off, its focused regression
test, the normal master Gitlink update, and this bilingual record/index. It has
passed local syntax, focused security/path, CI-security-contract,
documentation-link, and whitespace checks. It still requires fresh exact-head
hosted validation and review before a protected merge.
