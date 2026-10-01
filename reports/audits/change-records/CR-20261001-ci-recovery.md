# Change Record: CR-20261001-ci-recovery

**Language:** English | [Deutsch](CR-20261001-ci-recovery.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261001-ci-recovery |
| Date (UTC) | 2026-10-01 |
| Base revision | `b0f3bdab429717b5b0311c30c5b4d1153c672ac0` |

## Motivation and problem statement

Recover the failures reported in Parent run [36906913089](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36906913089) and Framework run [36703337419](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/36703337419), and inspect current CI for related failures. Parent maintenance wrongly applied the single-bot-commit rule to a reviewed, merged maintenance branch. Additional gaps included long Unix socket paths, rejection of the provisioned Traefik host stage, broker permission/tag-fetch contracts, incomplete updater inventory/copied-tree inputs, and transient artifact cleanup API failures.

## Acceptance criteria

Regression checks must cover the original defects without weakening publisher identity, runtime isolation, immutable pins, or deny-default permissions. Current hosted Framework publication and its PR checks must succeed. Parent hosted validation and protected broker activation remain required before claiming all workflows work.

## Implementation decision and rationale

Keep open maintenance branches constrained to the configured App; allow reuse of reviewed merged remediation history only after checking PR identity, merge ancestry, and current branch guards. Allocate private, short socket directories while retaining revision-bound artifact roots. Admit only the exact provisioned Traefik host path. Accept the broker caller's exact empty permission mapping and independently acquire/check the approved CRS tag. Complete the explicit updater publisher inventory and read-only copied baseline; run focused inventory coverage in Make and the full suite in CI to avoid recursive candidate validation. Derive action-pin assertions from the central lock. Retry artifact cleanup API calls three times.

## Changed files

- `.github/workflows/ci-security-workflow-lint.yml`
- `.github/workflows/cleanup-artifacts.yml`
- `.github/workflows/nginx-root-broker.yml`
- `.github/workflows/test-envoy.yml`
- `.github/workflows/test-traefik.yml`
- `.github/workflows/update-submodules.yml`
- `.github/workflows/update-workflow-tools.yml`
- `Makefile`
- `ci/runtime/broker/nginx_root_broker.py`
- `ci/runtime/lifecycle/run-connector-stage.sh`
- `ci/tools/update-workflow-tools.py`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `connectors/envoy/harness/run_envoy_connector_runtime.sh`
- `connectors/envoy/harness/start_envoy_connector.sh`
- `connectors/traefik/scripts/runtime_smoke.py`
- `docs/reference/variables.de.md`
- `docs/reference/variables.md`
- `docs/security/ci-security-tooling.de.md`
- `docs/security/ci-security-tooling.md`
- `docs/security/trusted-nginx-root-broker.de.md`
- `docs/security/trusted-nginx-root-broker.md`
- `tests/ci_security/test_update_workflow_tools.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_nginx_root_broker.py`
- `tests/test_nginx_root_broker_workflow.py`
- `tests/test_runtime_env_snapshot_contract.py`
- `tests/test_traefik_runtime_smoke_security.py`
- `tests/test_update_submodules_local_git.py`
- `ci/runtime/lifecycle/with-private-sockets.py`
- `reports/audits/change-records/CR-20261001-ci-recovery.de.md`
- `reports/audits/change-records/CR-20261001-ci-recovery.md`
- `tests/test_private_runtime_sockets.py`

## Commands executed

All local command entry points used RTK. `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-ci-security-contract`: PASS, 175 tests, five existing environment skips, plus actionlint/zizmor/gitleaks provenance validation. The updater suite passed 38 tests, including real proposed-tree validation; workflow contracts passed 31 tests. Coordinated integrated regression validation passed 118 tests. Actionlint passed all 31 workflows. Quick-check timed out after 600 seconds at the HAProxy check; this is not a full quick-check pass.



```sh
rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -q tests.test_private_runtime_sockets tests.test_nginx_root_broker tests.test_nginx_root_broker_workflow tests.test_nginx_root_broker_crs_profile tests.ci_security.test_update_workflow_tools
rtk proxy bash -c '/root/go/bin/actionlint .github/workflows/*.yml'
```

The integrated 118-test run completed in 98.147 seconds. Task evidence is retained in `/var/tmp/codex/ModSecurity-conector/ci-recovery-inventory.md`, `/var/tmp/codex/ModSecurity-conector/ci-recovery-20261001-plan.md`, and `/var/tmp/codex/ModSecurity-conector/ci-recovery-ci-contract.log`.

The bounded repeat of `rtk proxy env CI=true ... timeout 600 make quick-check`, using the same external build/log roots and interpreters, passed (exit 0, 275 tests). Native lint explicitly skipped NGINX and HAProxy C17 compilation because their headers were absent. The earlier local timeout occurred during automatic prerequisite provisioning before HAProxy compiler probes. These results do not prove the two skipped compiler checks. The repeat log is `/var/tmp/codex/ModSecurity-conector/ci-recovery-quick-check-ci.log`.



```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python check-bilingual-docs check-doc-links
rtk git diff --check
```

Record structure, bilingual documentation, repository path references, documentation links, and diff whitespace checks passed.

## Security impact

Publisher identity, merged-PR ancestry, explicit write scope, deny-default permissions, immutable action pins, and runtime isolation remain enforced. The Traefik stage admission is exact rather than a general build-directory trust extension. Socket roots are private and validated. No Framework/MRTS source changes or gitlink updates are part of this change.

## Runtime evidence

Framework fresh publisher run [36908638390](https://github.com/Easton97-Jens/ModSecurity-test-Framework/actions/runs/36908638390) succeeded from master `6948ec5` and created Draft [PR 134](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/134), head `51c70128693f0e836d8bff8af947232bca0691fc`. All 20 checks finished without failures, with three advisory skips; Sonar reported OK. This is Framework publisher/PR evidence, not fresh Parent connector runtime evidence. Parent hosted validation remains pending.

## Known limitations

Local privilege-dependent namespace integration had five existing skips. CI-mode quick-check passed with the two missing-header compiler skips; the ordinary local attempt timed out. The protected broker caller remains pinned to `49c40779a7b6de9f699391bcd524ea069787df42`; the updated broker source is not activated by this patch alone.

## Remaining risks

A reviewed protected broker activation/repin and real evidence for both selected broker profiles are still required. Hosted Parent execution may expose additional runner-specific failures. Current explicit updater inventory prevents silent publication gaps; new workflows must be reviewed and added to both inventory and staging.

## Checks not run and rationale

A full Parent hosted pass and both protected broker runtime profiles are outstanding. Parent master integration was not authorized, so neither integration nor protected activation/repin was performed. NGINX and HAProxy C17 compiler checks lack local header prerequisites.

## Final diff and review status

Local repair and regression verification are available for review; overall recovery remains partial pending Parent hosted evidence and protected activation. Original gitlinks are preserved. No Parent master integration or Framework/MRTS source edit is claimed. Both record language versions preserve the same values and limitations.
