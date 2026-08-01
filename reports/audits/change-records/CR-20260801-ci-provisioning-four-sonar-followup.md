# Change Record: Parent CI provisioning four-item SonarQube Cloud follow-up

**Language:** English | [Deutsch](CR-20260801-ci-provisioning-four-sonar-followup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-ci-provisioning-four-sonar-followup` |
| Date (UTC) | `2026-08-01` |
| Base revision | `e1a656798efb89e77e0526ffc7698cbd02b104b1` |
| Tracking | `FND-SONAR-0030`; `AZ9cRyj3HhV2CayPTPzC`, `AZ9cRyj3HhV2CayPTPzB`, `AZ9cRyj3HhV2CayPTPys`, and `AZ9cRyj3HhV2CayPTPy2` |
| Boundary | Parent `ci/provisioning` and one direct Parent cache-contract test; Framework, MRTS, Gitlinks, `.github`, SonarQube Cloud settings, dependencies, and `master` are unchanged. |

## Motivation and problem statement

The current inventory has three `python:S3776` rows in `BuildLock.__enter__()`, `prepare_apache_httpd()`, and `prepare_nginx_runtime()`, plus one `python:S1066` row in `remove_incomplete_connector_cache_entry()`. All four are maintainability findings in `ci/provisioning/components/prepare-runtime-components.py`; the component has no open security row and reports `0.0%` duplication.

## Acceptance criteria

- Each of the four rows has a behavior-preserving source remedy without `NOSONAR`, suppression, exclusion, rule, Quality-Gate, or threshold changes.
- Lock timeout, owner-marker, and release behavior remain unchanged.
- Unmanaged incomplete cache entries remain fail-closed; marker-owned entries remain removable only under the managed root.
- Apache/NGINX keyed plans retain transactional staging, and NGINX builds only when both artifact views are unready.
- Focused controls pass; exact-head GitHub Actions and SonarQube Cloud analysis are still required for `verified_pr`.

## Implementation decision and rationale

`BuildLock.__enter__()` delegates file locking and directory-fallback waiting to private methods while keeping the same `fcntl`-then-`ImportError` fallback contract. The stale-cache condition is one equivalent fail-closed guard. Apache and NGINX share a private transactional-plan predicate, and NGINX uses a private helper for its existing “both artifacts unready” build condition.

## Security impact

The source handles cache paths, managed-root deletion, downloaded build inputs, and subprocess-adjacent data. The invariant remains unchanged: only entries authorized by managed-root and ownership controls can be removed, and existing provenance, digest, containment, staging, and fail-closed controls are retained. The direct regression preserves an unmanaged partial entry when migration is refused and removes a legitimate owned entry. No security finding is claimed.

## Changed files

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- This English/German Change Record pair.

## Tests and actual results

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -P -m py_compile ci/provisioning/components/prepare-runtime-components.py` | passed |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_prepare_runtime_components tests.test_runtime_component_cache_contract tests.test_runtime_component_cache_identity tests.test_runtime_env_snapshot_contract tests.test_runtime_artifact_utils tests.test_runtime_path_policy` | passed: 94 focused tests |
| `PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=modules/ModSecurity-test-Framework make check-runtime-path-policy` | passed |
| `PYTHON=/root/git/ModSecurity-conector/.venv/bin/python make check-bilingual-docs` | passed |
| `PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=modules/ModSecurity-test-Framework make check-doc-links` | passed |
| `git diff --check` | passed |

The first broad run stopped six Framework-fixture cases because the new worktree had no initialized submodule. The isolated worktree then initialized only its Parent-pinned `6400ee882afa0527e5c0763fa6efb850ffa403f2` test fixture; the re-run passed and made no Framework source or Gitlink change.

## Commands executed

The commands and observed outcomes in the preceding table are the complete local execution record at authoring time. The selected interpreter is `/root/git/ModSecurity-conector/.venv/bin/python` (Python `3.14.4`) with `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and `PYTHONDONTWRITEBYTECODE=1`; build and bytecode output uses the task-owned external root.

## Runtime evidence

The focused suite exercises lock, cache-marker, staging, Apache, NGINX, HAProxy, snapshot, artifact, and path-policy contracts. It does not perform a third-party download or native connector build. Framework and MRTS source remain out of scope.

## Checks not run and rationale

- A real runtime-component provision/build was not run because it downloads and compiles third-party components; that is broader than this structural remediation.
- Ruff and Pyright were not run because the selected Parent virtual environment has no `ruff` or `pyright` module. No package or dependency contract was changed.
- Exact-head GitHub Actions and SonarQube Cloud analysis are not yet run because no commit, push, or pull request exists at record authoring.

## Known limitations

Local tests cannot prove the hosted disposition of historic SonarQube Cloud rows. Final scoped diff review, documentation checks, commit, Draft PR, exact SHA comparison, and current-head hosted checks remain required.

## Remaining risks

The wider repository SonarQube Cloud backlog is out of scope. No result here authorizes a `master` integration.

## Final diff and review status

This pre-delivery record reports only observed local results. It does not claim a commit, pull request, hosted check, Quality Gate, approval, merge, or release.
