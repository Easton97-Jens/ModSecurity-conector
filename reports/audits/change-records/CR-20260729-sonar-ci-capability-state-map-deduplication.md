# Change Record: Parent CI capability-state map deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-ci-capability-state-map-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260729-sonar-ci-capability-state-map-deduplication` |
| Date (UTC) | `2026-07-29` |
| Base revision | `a1c8394e528bfcd7b54bc3e0aac4cdf3430d1345` |
| Source revision assessed | Current local task-working-tree diff from the base revision; the rebased implementation commit is `b25dcb4d487a648e019d323cdaef957aff342ce9`. No push, pull request, hosted check, or merge is claimed at record authoring. |
| Boundary | Only Parent `ci/evidence/collectors/connector_capabilities.py`, its direct Parent test, this English/German Change Record pair, and paired Change-Record indexes. No `.github/`, `scripts/`, Framework, MRTS, Gitlink, manifest, scanner configuration, Quality Gate, exclusion, suppression, or default-branch change is included. |
| SonarQube Cloud linkage | Targets the current duplicated Envoy/Traefik host-model-state block in `_validate_relationships()`. The change centralizes only the common eleven `unsupported_by_host_model` state requirements and retains every connector-specific override. |

## Motivation and problem statement

The Parent CI capability collector contains duplicate fixed state assignments
for the pre-upstream Envoy `ext_authz` and Traefik `ForwardAuth` host models.
Those declarations are a fail-closed contract: a capability that cannot observe
the later upstream response must remain exactly `unsupported_by_host_model`,
not merely some arbitrary non-verified state. The duplicate must be reduced
without making expected states configurable or weakening the rejection path.

## Implementation decision and rationale

`connector_capabilities.py` now owns the shared eleven-capability response and
Phase-4 map once. `MappingProxyType` makes that shared map, each connector map,
and the outer connector mapping immutable after import. Envoy retains
`request_body_buffered` and `phase2` as `configured_not_exercised`; Traefik
retains `request_body_buffered` and `phase2` as `not_implemented` plus its
separate `request_body_streaming` requirement. The unchanged Lighttpd map is
also represented as an immutable static map so that the complete policy owner
cannot be modified during validation.

No validator parameter, CLI option, environment input, manifest-derived policy,
or dynamic documentation URL was introduced. `_validate_relationships()` still
uses the fixed selected connector map, emits the identical
`host-model invariant requires ...` error, and keeps the separate exact
Traefik ForwardAuth reference check.

## Acceptance criteria

- The shared Envoy/Traefik eleven-capability response and Phase-4 map has one
  immutable Parent source owner; the exact connector-specific states remain
  distinct.
- Every Envoy and Traefik host-model state mutation fails through the real
  `validate_manifest()` path with the exact expected host-model error.
- Canonical Envoy and Traefik manifests remain valid, and removal of the
  versioned official ForwardAuth reference fails closed.
- The future exact pull-request head must report zero new SonarQube Cloud
  issues, zero new duplicated lines, and `0.0%` New-Code duplication without
  changing scanner policy.
- No default-branch integration occurs without separate explicit user
  authorization.

## Changed files

- `ci/evidence/collectors/connector_capabilities.py`
- `tests/test_connector_capabilities.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-capability-state-map-deduplication.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-capability-state-map-deduplication.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| Focused host-model, deep-immutability, and ForwardAuth-reference tests | passed: `3` tests. The test iterates every Envoy/Traefik state requirement against a deep copy of the canonical manifest and asserts the exact fail-closed error. |
| `ci/evidence/collectors/connector_capabilities.py check` | passed: six connectors and 60 capabilities. |
| Selected-file `py_compile` with a task-owned bytecode cache | passed. |
| `git diff --check` | passed. |
| Full `tests.test_connector_capabilities` module | blocked external dependency: 15 tests passed; the pre-existing `test_framework_validator_is_required_for_each_runtime_result` fails because the isolated worktree lacks `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py` before its mocked subprocess path is reached. No test or Framework boundary was weakened. |
| Ruff and Pyright | not run: neither is installed in the selected Parent virtual environment, and no optional-tool provisioning is authorized or needed to replace the project-native checks. |
| Full `make lint` | blocked external dependency after both Shell syntax checks and compilation of all Parent `ci/` Python files passed: `check-no-crs-source-normalization` imports the absent Framework file `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`. The task-owned `BUILD_ROOT` remained external; no check was weakened. |
| `make check-bilingual-docs` | blocked external dependency: every reported missing link target is under the absent Framework submodule; no changed Change Record error is reported. |
| `make check-doc-links` | blocked external dependency: its repository-path phase reports the same absent Framework link targets before the Framework-owned link checker can run. |

## Security impact

The input is a versioned connector capability manifest. The nearest control is
the static expected-state map in `_validate_relationships()`; a mismatch flows
to `main()` as a diagnostic and exit code `1` before successful checking or
report generation. A weakened map could let a pre-upstream integration claim
response-, Phase-4-, or late-intervention capability it cannot provide.

The map remains source-authored and deeply immutable. New direct tests cover
the actual validation path for all 27 Envoy/Traefik requirements, valid
canonical controls, outer and inner map mutation rejection, and the independent
versioned ForwardAuth-reference gate. The source/security preflight and final
scoped diff review found no plausible diff-induced candidate.

## Runtime evidence

No connector server, network, runtime matrix, or generated repository artifact
was run or claimed. This is a deterministic manifest-validator refactor; the
focused tests operate on in-memory deep copies of the canonical Parent
manifests and call the production validation function directly.

## Known limitations

- This record covers one independent CI duplication cluster, not the complete
  Parent CI SonarQube Cloud backlog.
- The isolated task worktree does not contain the Framework validator required
  by one pre-existing test and broader Make targets. That missing external
  dependency is not hidden or patched here.
- Hosted GitHub Actions and SonarQube Cloud evidence must be obtained for the
  exact future pull-request head.

## Remaining risks

The static capability declaration remains a source-contract assertion. This
patch neither claims a live Envoy/Traefik runtime result nor alters the existing
separate runtime-evidence/promotion controls. Its risk is limited to the
existing trusted source and CI policy boundary; no new filesystem, network,
process, credential, or Framework/MRTS dependency path is introduced.

## Checks not run and rationale

- Full Framework-dependent tests and the remaining lint/documentation layers
  are blocked by the absent Framework checkout/validator in the isolated task
  worktree. Their actual results are recorded above; no control is bypassed.
- No runtime smoke or full matrix was run because it would not provide a more
  direct proof of the deterministic host-model state-map contract.

## Final diff and review status

Focused tests, the all-connector manifest check, selected compilation,
whitespace validation, and final focused security review have passed. A full
module test plus full lint and documentation checks are externally blocked as
described above. A local rebased implementation commit exists; a push, Draft
PR, hosted checks, SonarQube Cloud result, review state, and merge are not
claimed at record authoring. No default-branch action is authorized or
implied.
