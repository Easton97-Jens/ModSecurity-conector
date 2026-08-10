# Change Record

**Language:** English | [Deutsch](CR-20260810-protected-nginx-broker-modsecurity-loader.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260810-protected-nginx-broker-modsecurity-loader |
| Date (UTC) | 2026-08-10 |
| Base revision | e24527eb729584aac3d815cbf32ef6b7026f729c |
| Framework gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation and problem statement

Protected resulting-master run `31344894963` bound the caller, broker, and
Framework revisions successfully, but both profiles stopped in the unprivileged
build step before candidate creation. The producer selected Libtool's
`libmodsecurity.so` alias as the protected artifact; that alias is a symlink,
so the existing no-follow producer control correctly rejected it.

The reviewed ModSecurity object uses the ABI name `libmodsecurity.so.3`.
Copying only an unversioned root artifact would therefore move the failure to
the dynamic loader. Separately, an NGINX module with a Runner-cache
`DT_RPATH` or `DT_RUNPATH` could bypass the admitted library directory. Both
defects must remain outside the root boundary.

## Acceptance criteria

The protected producer preserves ordinary Libtool aliases for generic
link-time consumers but publishes a regular, contained
`prefix/lib/libmodsecurity.so.3` artifact for protected provenance. Its cache
identity changes so an older alias-only prefix cannot be reused. Each expected
alias must have a direct basename target, and descriptor-relative resolution
must bind both aliases to one regular terminal object before the protected copy
is made from the descriptor tied to that terminal.

The broker binds that exact regular artifact name in the provenance record,
snapshot, candidate, root layout, and loader environment. It rejects a
symlink, outside-root path, metadata/digest mismatch, or dynamic section with
`DT_RPATH`, `DT_RUNPATH`, slash-bearing `DT_NEEDED`, `DT_AUDIT`,
`DT_DEPAUDIT`, `DT_FILTER`, or `DT_AUXILIARY` before candidate creation. The
fixed inspection has a real bounded deadline. The protected workflow sets the
fixed `NGX_IGNORE_RPATH=YES` selection before `make fetch-deps`.

## Technical decisions

The repair does not accept a symlink at any protected producer, candidate, or
root boundary. It resolves the Libtool aliases descriptor-relatively, requires
direct basename alias targets, and verifies that both expected aliases resolve
to the same regular terminal object. It materializes the separate
regular ABI-name copy through the descriptor tied to that terminal; nested
symlink escape or replacement is rejected.

The existing `NGX_IGNORE_RPATH=YES` opt-in takes precedence only in the
explicit ModSecurity-library branch of `connectors/nginx/config`; ordinary
connector behavior is unchanged when that opt-in is absent. The broker uses
the fixed absolute `/usr/bin/readelf` with an empty `PATH`, bounded output, a
real bounded deadline, and no shell to inspect the admitted source module and
library before candidate creation.

A local follow-up remediates two PR #271 Sonar findings: the
producer alias resolver's cognitive-complexity issue (`python:S3776`) and the
broker dynamic parser's regex issue (`python:S8786`). This is local remediation
evidence only; it is not a post-fix hosted Sonar analysis result.

## Implementation decision and rationale

`MODSECURITY_OUTPUT_LAYOUT_VERSION` is part of the ModSecurity cache identity,
which prevents an old completed cache entry from satisfying the new protected
artifact contract. The generic `libmodsecurity.so` readiness/linker name stays
unchanged. The protected record instead selects the materialized regular
`libmodsecurity.so.3` copy.

The broker's fixed artifact-name map, snapshot reader, candidate copy, root
admission, final-manifest validation, and `LD_LIBRARY_PATH` now use that same
ABI name. It performs no ambient lookup for the inspection tool and fails
closed if either verified ELF has `DT_RPATH`, `DT_RUNPATH`, slash-bearing
`DT_NEEDED`, `DT_AUDIT`, `DT_DEPAUDIT`, `DT_FILTER`, or `DT_AUXILIARY`, or
cannot be inspected within the bounded deadline. All inspection is
unprivileged and occurs before candidate creation and every `sudo` action.

## Changed files

- .github/workflows/nginx-root-broker.yml
- ci/provisioning/components/prepare-runtime-components.py
- ci/runtime/broker/nginx_root_broker.py
- connectors/nginx/config
- tests/test_runtime_env_snapshot_contract.py
- tests/test_runtime_component_cache_contract.py
- tests/test_nginx_root_broker.py
- tests/test_nginx_root_broker_crs_profile.py
- tests/test_nginx_root_broker_workflow.py
- docs/security/trusted-nginx-root-broker.md and docs/security/trusted-nginx-root-broker.de.md
- this Change Record and CR-20260810-protected-nginx-broker-modsecurity-loader.de.md

## Tests and actual results

The initial focused producer, cache, broker, CRS-profile, workflow, and
CI-security suite passed 83 tests locally after the initial loader repair.
After the expanded security discovery and remediation, a later broker/CRS
suite passed 43 tests and the focused remediation passed 2 tests. The producer
focused matrix passed 5 tests. These cover direct-basename Libtool aliases,
descriptor-tied regular ABI artifact publication, and the expanded pre-
candidate dynamic-section rejection with a legitimate control.

The full owning cache module passed 38 tests and had one known
isolated-worktree fixture error. The error was
`test_nginx_discards_marker_owned_partial_root_before_build`, caused by the
missing isolated fixture file
`connector/common/src/header_validation_internal.h`. The error was not
suppressed or represented as a pass.

After the PR #271 Sonar findings were remediated locally, the expanded focused
suite passed 88 tests. The local follow-up also passed syntax compilation for
the producer and broker modules, the CI-security-contract check, and the
tracked-diff whitespace check. These are local results, not hosted
PR, Sonar, runtime, or cleanup evidence.

## Commands executed

The 83-, 43-, 2-, and 5-test results above are earlier historical local
observations; their exact command lines are not reconstructed here. The
following later commands and results were actually observed:

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=../tmp python3 -m unittest -v \
  tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_protected_nginx_broker_snapshot_uses_only_canonical_plan_outputs \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_output_layout_version_changes_the_cache_identity \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_materialize_a_regular_runtime_soname \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_unsafe_or_ambiguous_libtool_chains \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_nested_symlink_parent_escape \
  tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_runtime_copy_remains_bound_to_verified_inode \
  tests.test_nginx_root_broker \
  tests.test_nginx_root_broker_crs_profile \
  tests.test_nginx_root_broker_workflow \
  tests.test_ci_security_workflows
```

Result: PASS, 86 tests passed.

```sh
rtk proxy sh -n connectors/nginx/config
```

Result: exit 0.

```sh
rtk proxy shellcheck --shell=sh --severity=error connectors/nginx/config
```

Result: exit 0.

```sh
rtk proxy make check-ci-security-contract
```

Result: exit 0, 26 tests passed.

```sh
rtk proxy git diff --check
```

Result: exit 0 for the current tracked diff.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=../tmp python3 -m unittest -v tests.test_runtime_component_cache_contract
```

Result: 38 tests passed and 1 error occurred in
`test_nginx_discards_marker_owned_partial_root_before_build` because the
isolated fixture lacked `connector/common/src/header_validation_internal.h`.
The error was not suppressed.

The following commands were then executed for the local Sonar
remediation follow-up:

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=../tmp python3 -m unittest -v tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_protected_nginx_broker_snapshot_uses_only_canonical_plan_outputs tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_output_layout_version_changes_the_cache_identity tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_materialize_a_regular_runtime_soname tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_unsafe_or_ambiguous_libtool_chains tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_nested_symlink_parent_escape tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_runtime_copy_remains_bound_to_verified_inode tests.test_runtime_component_cache_contract.RuntimeComponentCacheContractTest.test_modsecurity_outputs_reject_cyclic_and_nonregular_libtool_chains tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow tests.test_ci_security_workflows
```

Result: PASS, 88 tests passed.

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m py_compile ci/provisioning/components/prepare-runtime-components.py ci/runtime/broker/nginx_root_broker.py
```

Result: passed.

```sh
rtk proxy make check-ci-security-contract
```

Result: passed.

```sh
rtk proxy git diff --check
```

Result: passed.

## Security impact

The original run remains fail-closed: both profiles stopped before candidate
creation, root admission, every `sudo` action, NGINX startup, evidence, and
cleanup verification. The repair preserves that ordering and additionally
prevents an otherwise verified module or shared library from retaining a
Runner-cache dynamic search path, slash-bearing dependency, or dynamic audit
or filter hook. Descriptor-relative direct-basename alias resolution and the
descriptor-tied protected copy reject nested symlink escape and replacement.
No system NGINX, ambient `PATH`, symlink, caller-provided artifact path, or root
shell is introduced. These controls execute before candidate creation and
remain unprivileged/pre-root.

## Runtime evidence

Run `31344894963` is failure evidence only. It reached the then-current
protected snapshot and immutable binding checks but stopped before the loader
contract could pass.
There is no successful root, worker, no-CRS, CRS, audit, evidence-readback, or
cleanup result for this candidate.

## Known limitations

The available local interpreter is CPython 3.14.4 while `.python-version`
requires CPython 3.14.6. Local tests are source/static evidence, not
CI-equivalent interpreter or hosted-root evidence. The canonical local finding
store is mounted read-only, so the distinct proposed FND-PARENT-0117 record
could not be created there; no competing record was created. FND-PARENT-0113
remains blocked. PR #271's prior Sonar analysis reported `python:S3776` and
`python:S8786`; their local remediation has not yet received a post-fix hosted
Sonar analysis.

## Remaining risks

The broker repair must still receive a new immutable commit, exact-head
hosted checks, CodeQL, SonarQube Cloud, review, and normal merge. A separate
caller repin must then bind that new broker commit and its Framework gitlink.
Only a resulting-master protected no-CRS and `owasp-crs` lifecycle with
evidence readback and cleanup can unblock PR #240.

## Checks not run and rationale

No local `make fetch-deps`, root action, NGINX start, CRS fetch, audit, or
cleanup run was attempted. Those actions require the protected resulting-master
workflow, real hosted runner isolation, and the separate post-merge caller
repin. Hosted PR checks and SonarQube Cloud are also not yet available because
this repair has not been committed or published.

## Final review status

This is local repair evidence only. It neither creates a pull request nor
asserts a delivery, merge, caller-repin, or successful Phase-D lifecycle.

## Final diff and review status

The task-owned branch begins at `e24527eb729584aac3d815cbf32ef6b7026f729c`.
The intended diff is Parent-only and does not alter Framework source, the
Framework Gitlink, MRTS, caller pins, root action allowlists, triggers, or
permissions. A final scoped security-diff review and all applicable local
checks remain required before publication.
