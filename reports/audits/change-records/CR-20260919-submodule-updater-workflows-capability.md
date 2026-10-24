# Change Record

**Language:** English | [Deutsch](CR-20260919-submodule-updater-workflows-capability.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260919-submodule-updater-workflows-capability |
| Date (UTC) | 2026-09-19 |
| Base revision | 1bc48cd23abc3178e302108b62f68c74434b80e6 |

## Motivation and problem statement

GitHub Actions run [35454150502](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35454150502)
validated a Framework candidate and then failed while its publisher pushed the
approved static Parent projection. The remote rejected
`.github/workflows/test-connectors-with-crs-no-mrts.yml` because the publisher
used the ambient `github.token`, which cannot update workflow files in this
repository configuration.

That workflow projection is required: it updates the closed CRS/no-MRTS static
SHA consumers and its test fixture after the current Parent state has been
verified. Removing it would leave those consumers stale rather than repairing
publication.

## Acceptance criteria

- The publisher has no ambient write permission and uses only a short-lived,
  repository-limited App token with the exact `contents`, `pull-requests`, and
  `workflows` write scopes needed for its approved maintenance commit.
- Resolver, validator, and outcome jobs remain free of the App credential and
  secrets.
- The closed CRS/no-MRTS workflow and test-fixture projection, its pre- and
  post-projection validation, and unexpected-path rejection remain intact.
- A fallback to `github.token`, an unrelated App scope, a different repository
  target, or restored ambient write permission fails the static contract.
- Focused and repository-native CI-security checks pass locally; exact-head
  hosted evidence is recorded only after it exists.

## Implementation decision and rationale

`create-submodule-update-pr` now has only `contents: read` as its ambient job
permission. After the existing trusted default-branch and successful-validator
gate, it checks the already configured `WORKFLOW_UPDATER` App inputs and mints
one token through the pinned
`actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1`
action. The token is limited to the current repository and requests exactly
`permission-contents: write`, `permission-pull-requests: write`, and
`permission-workflows: write`. The publisher alone supplies that output as
`GH_TOKEN` to its existing GitHub CLI and Git publication path.

The existing App configuration was not created, rotated, inspected, or
broadened. Historical successful run
[32544278902](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/32544278902)
already minted this bounded token and published workflow-file changes. The
repair reuses that established pattern rather than granting broad workflow
write access to `GITHUB_TOKEN`.

## Security impact

This change affects a CI supply-chain and publication boundary. The write-capable
credential remains confined to the publisher, which is reachable only after
the existing trusted resolver/validator gates. The App token is scoped to one
repository and its declared three capabilities; it cannot be obtained by
resolver, validator, outcome, or pull-request code. The registered workflow
projection remains a closed target checked before and after synchronization.

No Framework or MRTS source, Gitlink, NGINX ownership boundary, App
installation, repository setting, credential value, token secret, Quality Gate,
or branch-protection rule changes.

A fresh independent post-patch security review found no reportable bypass or
regression in this source boundary. It confirmed the protected trigger/gate,
publisher-only credential exposure, no secret-printing path, closed projection,
and pre/post-projection path guards. It did not dispatch a hosted workflow and
therefore does not claim live App-token enforcement.

## Changed files

- `.github/workflows/update-submodules.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/CR-20260919-submodule-updater-workflows-capability.md`
- `reports/audits/change-records/CR-20260919-submodule-updater-workflows-capability.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

- `python -m unittest -v
  tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_update_submodules_separates_validation_from_publishing
  tests.test_ci_security_workflows.CiSecurityWorkflowTest.test_job_write_permissions_are_exactly_allowlisted`
- `python -m unittest -q tests.test_update_framework_versions`
- `python -m unittest -q tests.test_verify_framework_candidate_contract`
- `python -m unittest -q tests.test_ci_security_workflows`
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract`

All commands used the selected Parent virtual-environment interpreter with
user-site packages disabled and without installing or changing dependencies.

## Tests and actual results

- Focused `tests.test_ci_security_workflows` publisher and write-permission
  contracts: passed (2 tests).
- `tests.test_update_framework_versions`: passed (21 tests).
- `tests.test_verify_framework_candidate_contract`: passed (27 tests).
- `tests.test_ci_security_workflows`: passed (30 tests).
- `make PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
  check-ci-security-contract`: passed (155 tests, 5 expected
  namespace/identity integration skips).
- `git diff --check`: passed.

Expected diagnostics emitted by negative tests are fail-closed control cases,
not test failures.

## Runtime evidence

The original hosted failure is run
[35454150502](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35454150502),
publisher job
[105926592805](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35454150502/job/105926592805).
It reached the required projection and was rejected specifically for lacking
workflow-file capability.

No current-task hosted run, push, pull request, or merge is claimed at this
recording point. Local contracts cannot prove the live App installation remains
unchanged after the historical successful run; any exact-head hosted outcome
must be observed separately.

## Checks not run and rationale

No workflow dispatch or rerun has been performed: starting a GitHub-hosted run
is an external action outside this source-change record. No runtime connector
matrix is applicable because no connector or runtime behavior changed.

`make check-bilingual-docs` and `make check-doc-links` were run but are blocked
in this isolated worktree by pre-existing repository links into the deliberately
uninitialized `modules/ModSecurity-test-Framework` submodule. After correcting
the record's initial required-heading errors, the bilingual checker reported no
task-record error; every remaining failure named only those absent Framework
targets. Initializing or modifying that separate repository is out of scope.

## Known limitations

Local tests cannot exercise GitHub App token issuance, remote workflow-file
authorization, branch protection, scheduler behavior, or a real future
Framework candidate. They instead prove the source-level least-privilege and
closed-projection contracts.

## Remaining risks

If the existing App installation is removed or its `Workflows` permission is
revoked, the publisher will fail closed at token minting or publication rather
than falling back to `github.token`. A future change to the publisher must keep
the credential confined to its trusted gate and retain the exact static tests.

## Final diff and review status

Local implementation, focused security-contract validation, bilingual record
structure, scoped diff review, and the fresh independent security review are
complete. The source-level finding is fixed; authorized exact-head PR delivery,
hosted checks, SonarQube Cloud evidence, and live App-token enforcement remain
pending. No merge is authorized or asserted.
