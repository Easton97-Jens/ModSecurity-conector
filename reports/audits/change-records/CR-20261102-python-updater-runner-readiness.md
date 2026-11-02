# Change Record: CR-20261102-python-updater-runner-readiness

**Language:** English | [Deutsch](CR-20261102-python-updater-runner-readiness.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261102-python-updater-runner-readiness |
| Date (UTC) | 2026-11-02 |
| Base revision | `2cfe7819655f905fb41c63b1f03c3e3d812d59bc` |

## Motivation and problem statement

A Python release may be published before its exact GitHub runner archive exists. Previously the resolver emitted candidate outputs in that state and deferred the failure to candidate setup.

## Acceptance criteria

Reject missing exact `ubuntu-26.04`/`x64` runner archives before emitting any resolver job outputs; retain the existing four outputs for an exact official stable archive.

## Implementation decision and rationale

Use `runpy.run_path` with the fixed pinned Framework `ci/tools/python_runner_builds.py` path and call `require_build(fetch_manifest(), latest)` after metadata validation. Trusted event checkout, Framework context binding, CLI/JSON interface, and downstream validation remain intact. No candidate code is imported. The paired build documentation also corrects its stale claim that this checkout omits submodules.

## Changed files

- `.github/workflows/update-python-version.yml`
- `docs/build/README.md`, `docs/build/README.de.md`
- `docs/security/ci-security-tooling.md`, `docs/security/ci-security-tooling.de.md`
- `reports/audits/change-records/CR-20261102-python-updater-runner-readiness.md`, `reports/audits/change-records/CR-20261102-python-updater-runner-readiness.de.md`

## Commands executed

- `rtk bypass env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 /root/git/ModSecurity-conector/.venv/bin/python /var/tmp/codex/ModSecurity-conector/runs/component-updater-fix-20261102/parent/verify_resolver.py .`
- `rtk bypass env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/component-updater-fix-20261102/parent /var/tmp/codex/ModSecurity-test-Framework/venv/bin/python -m unittest -v tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_manifest_rejects_wrong_platform_arch_or_release_identity tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_manifest_fetch_rejects_redirect_and_oversized_payload tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_manifest_transport_failure_is_a_blocked_metadata_input tests.ci_security.test_updater_readiness.UpdaterReadinessTests.test_previous_ubuntu_build_cannot_satisfy_new_target`
- `rtk bypass env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/parent-python-updater-20261102/modules/ModSecurity-test-Framework check-bilingual-docs check-doc-links`
- `rtk bypass git diff --check`

The offline extracted-resolver regression failed before the fix because the missing-archive case emitted all four outputs; after the fix both missing-archive/no-output and exact-archive controls passed. The four existing pinned helper tests passed (eight expanded negative cases). Documentation and whitespace results are recorded in the final review below. The helper tests ran from the pinned Framework directory; other commands ran from the Parent worktree. Explicit context was needed for Change Record generation; initial incomplete-context attempts failed without creating files, then the documented generator created both scaffolds successfully.

## Security impact

Fails closed on unavailable or invalid official runner metadata without credentials or redirects. Only the trusted pinned helper is executed; no dependency, permission, gitlink, or candidate-code execution change.

## Runtime evidence

No hosted Actions or connector runtime run. Evidence is offline extracted workflow behavior and focused helper tests at Framework `f11d4617ff98ad615c72c1b6672fc386394db41e`.

## Known limitations

The guard checks manifest identity and availability, not a download/install of the candidate archive. Local Python was 3.14; no Python 3.15 compatibility claim is made.

## Remaining risks

The public manifest and archive availability can change between resolution and setup. Existing candidate setup and independent validation remain required.

## Checks not run and rationale

No full default suite, CI dispatch, archive download, candidate install, SonarQube scan, or runtime matrix: the change is a narrow workflow guard and delivery/hosted checks are coordinated separately.

## Final diff and review status

Local implementation prepared in isolated branch `codex/python-updater-readiness-20261102`. No commit, push, PR, merge, or hosted readiness result is claimed by this record. Final review: pinned-context `make check-bilingual-docs check-doc-links` passed, including repository path references; `git diff --check` passed. Both language pairs and the narrow workflow diff were manually reviewed.
