# Change Record: Parent CI provisioning final cognitive-complexity remediation

**Language:** English | [Deutsch](CR-20260801-ci-provisioning-two-cognitive-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-ci-provisioning-two-cognitive-remediation` |
| Date (UTC) | `2026-08-01` |
| Base revision | `7016a66f3702523098811b45139133c77dee88fb` |
| Tracking | `FND-SONAR-0030`; `AZ9cRyj3HhV2CayPTPzB`; `AZ9cRyj3HhV2CayPTPzC` |
| Boundary | Parent `ci/provisioning` and one direct Parent cache-contract test; Framework, MRTS, Gitlinks, `.github`, SonarQube Cloud settings, dependencies, and `master` remain unchanged. |

## Motivation and problem statement

The current `master` SonarQube Cloud analysis has two remaining `python:S3776`
Maintainability rows in `ci/provisioning/components/prepare-runtime-components.py`:
`prepare_apache_httpd()` and `prepare_nginx_runtime()` each have cognitive
complexity 16 where 15 is allowed. The requested directory has zero Security,
zero Reliability, and zero duplicate-line findings.

## Acceptance criteria

- The two exact rows receive behavior-preserving source remediation without
  `NOSONAR`, suppression, exclusion, rule, Quality-Gate, or threshold changes.
- Keyed Apache and NGINX plans continue to use validated transactional staging;
  unkeyed plans continue directly.
- Existing cache, provenance, containment, command-construction, publication,
  record, and failure semantics remain unchanged.
- Focused tests and applicable local checks pass; exact-head GitHub Actions and
  SonarQube Cloud analysis remain required for `verified_pr`.

## Implementation decision and rationale

`prepare_connector_with_optional_staging()` owns the already shared decision:
a keyed non-transactional plan enters the existing
`prepare_connector_transactionally()` path, while an unkeyed or already staged
plan invokes its prepare callback directly. The public Apache and NGINX entry
points delegate to private per-plan implementations that retain their prior
body and control-flow order. Two direct tests prove direct/unkeyed and
transactional/keyed delegation; existing Apache and NGINX cache-contract tests
continue to exercise actual staging and publication.

## Security impact

The source is security-relevant because it handles cache paths, downloads,
provenance, publication, and subprocess-adjacent data. The preserved invariant
is that keyed connector plans remain inside the existing validated managed-root
staging/publication control, while unkeyed plans remain direct. The focused
source/control review found no plausible diff-induced security regression or
reportable security finding. It is not a full repository security scan or
runtime build result.

## Changed files

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_runtime_component_cache_contract.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- This English/German Change Record pair.

## Tests and actual results

| Command | Result |
| --- | --- |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m py_compile ci/provisioning/components/prepare-runtime-components.py tests/test_runtime_component_cache_contract.py` | passed |
| `PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_runtime_component_cache_contract` | passed: 34 tests |
| `git diff --check` | passed before final documentation validation; final scoped repeat remains required before delivery |

The selected interpreter is `/root/git/ModSecurity-conector/.venv/bin/python`
(Python `3.14.4`), with `PYTHONNOUSERSITE=1`,
`PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and
`PYTHONDONTWRITEBYTECODE=1`. Test temporary state is task-owned external
storage.

## Commands executed

The commands and outcomes in the preceding table are the complete local
execution record at authoring time. `make check-no-crs-source-normalization`
and `make check-bilingual-docs` were also executed; their exact blocked and
remediation states are recorded under **Checks not run and rationale** and in
the task plan. No build, dependency installation, commit, push, PR, or merge
command has been executed at record authoring.

## Runtime evidence

The passing suite exercises Apache keyed staging, NGINX marker-owned
partial-root rebuilding, atomic publication visibility, managed-root removal
rejection, digest-before-publish, and the new direct/unkeyed plus keyed/staged
delegation controls. No third-party download or native connector build ran.

## Checks not run and rationale

- `make check-no-crs-source-normalization` was attempted but blocked during
  collection: the isolated Parent worktree intentionally has no Framework
  submodule file
  `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`.
  Initializing or modifying Framework is outside this Parent-only task.
- `make check-bilingual-docs` and `make check-doc-links` both reached the new
  Change Record successfully but are blocked by the same intentionally absent
  Framework targets referenced by pre-existing repository documents. No
  task-owned document link failed.
- `make check-runtime-path-policy` was attempted with the selected Parent
  interpreter and is blocked because its shell control imports the same absent
  `modules/ModSecurity-test-Framework/ci/lib/common.sh`; it did not exercise a
  changed runtime-path control.
- A real runtime-component provision/build was not run because it downloads and
  compiles third-party components, beyond this structural remediation.
- Ruff and Pyright were not run because the selected Parent virtual environment
  contains neither tool; no package or dependency contract changed.
- Exact-head GitHub Actions and SonarQube Cloud analysis are not yet run because
  no commit, push, or pull request exists at record authoring.

## Known limitations

Local checks cannot prove the hosted disposition of the two historical
SonarQube Cloud rows. Exact-head PR analysis must show their closure, zero new
issues, and zero new-code duplication before the draft PR can reach
`verified_pr`.

## Remaining risks

The wider repository SonarQube Cloud backlog is out of scope. This change does
not authorize a `master` integration.

## Final diff and review status

This pre-delivery record reports observed local results only. It does not claim
a commit, pull request, hosted check, Quality Gate, approval, merge, or
release.
