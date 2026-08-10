# Change Record

**Language:** English | [Deutsch](CR-20260810-trusted-nginx-broker-artifact-limit-crs-umask.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260810-trusted-nginx-broker-artifact-limit-crs-umask |
| Date (UTC) | 2026-08-10 |
| Base revision | 2d1efe0c10b62131bb1a6897aa46a8ba9e85d1db |
| Framework gitlink | 03880bf66b3905940466ff10b3a431a27ecc6b26 |

## Motivation and problem statement

Protected resulting-master run `31368594208` stopped before every root action in both profiles. No-CRS job `93392350727` rejected the verified canonical `libmodsecurity.so.3` under the generic 8 MiB evidence-file limit although the retained protected producer artifact measured 60,085,848 bytes. With-CRS job `93392350719` stopped before root because outer `umask 077` can produce fresh CRS sources that do not meet the broker's exact protected-source modes.

The failures were fail-closed but prevented legitimate candidate creation. The repair retains finite, descriptor-bound admission; it does not broaden generic evidence limits or relax CRS source-mode checks.

## Acceptance criteria

Only canonical `libmodsecurity.so.3` receives a fixed code-owned finite limit: `MAX_TRUSTED_MODSECURITY_LIBRARY_BYTES = 64 * 1024 * 1024`. The retained artifact leaves 7,023,016 bytes of headroom. The generic 8 MiB per-file and 20 MiB aggregate evidence limits remain in force for evidence, the NGINX binary, and module. Provenance and the already-opened no-follow descriptor both enforce the library limit before hashing or copying.

The outer workflow umask remains `077`. Only the exact `fetch-crs.sh` invocation runs in a subshell with `umask 022`; the workflow checks the outer umask before and after the fetch and preserves a failure status. It does not change the global umask or use recursive permission changes. The protected CRS contract still requires the source root and `rules` directory, plus `plugins` when present, at `0755` and selected source files at `0644`.

The shell contract accepts both canonical renderings `077`/`0077` and
`022`/`0022`, so the verification does not accidentally depend on one
shell spelling.

## Technical decisions

The library ceiling is a fixed broker-code policy value, applied at provenance
validation and again to the opened descriptor. The mode exception is limited
to the exact fixed CRS-fetch command in its subshell. The repair changes no
schema, caller input, public interface, generic evidence limit, Framework
Gitlink, or generated artifact.

## Implementation decision and rationale

The provenance validator receives an explicit maximum per protected artifact. Candidate copying repeats that maximum against metadata from the opened descriptor, closing the interval before digesting or copying. The library-only maximum is supplied only for canonical `libmodsecurity.so.3`; the NGINX binary and module retain the generic maximum. Broker CRS validation now explicitly checks the source-root mode as well as the required rules and optional plugins modes.

## Changed files

- .github/workflows/nginx-root-broker.yml
- ci/runtime/broker/nginx_root_broker.py
- tests/test_nginx_root_broker.py
- tests/test_nginx_root_broker_crs_profile.py
- tests/test_nginx_root_broker_workflow.py
- docs/security/trusted-nginx-root-broker.md and docs/security/trusted-nginx-root-broker.de.md
- this Change Record and CR-20260810-trusted-nginx-broker-artifact-limit-crs-umask.de.md

## Tests and actual results

Before the repair, four focused regression tests failed as expected: a valid library larger than 8 MiB was rejected by provenance, the library-specific copy limit was absent, CRS directories at `0700` were accepted, and the workflow lacked the scoped-umask contract.

After the repair, eight direct broker, CRS-profile, and workflow tests passed. They cover the separate library bound and opened-descriptor enforcement, replacement resistance before candidate creation, retained evidence caps, legitimate and unsafe CRS modes, and the scoped workflow umask contract, including a hermetic failed-fetch execution that preserves outer `077` and propagates failure.

The final broker, caller, workflow, CI-security, and Python-contract suite passed
123 tests. The cache-contract and cache-identity suite passed 46 tests. The
full snapshot module passed nine tests and reported one environmental failure
in `RuntimeEnvironmentSnapshotContractTest.test_with_runner_consumes_the_prepared_snapshot_without_reading_shared_env`: this external Parent worktree does not contain `modules/ModSecurity-test-Framework/ci/lib/common.sh`. The failure was not suppressed; Framework was not initialized or modified in this Parent-only phase.

## Commands executed

The following commands were actually executed from the Phase-A worktree. `../tmp` is the registered task-owned external temporary directory; no private build or cache path is recorded here.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow
```

Result: PASS, 63 tests.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_ready_nginx_snapshot_values_bind_the_parent_common_source_root tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_unready_nginx_does_not_publish_runtime_snapshot_values tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_snapshot_is_unique_local_atomic_and_keeps_shared_compatibility_export tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_snapshot_writer_rejects_a_path_outside_the_invocation_report_root tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_protected_nginx_broker_snapshot_uses_only_canonical_plan_outputs tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_native_comparison_uses_the_wrapper_snapshot_not_shared_env tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_native_comparison_does_not_fallback_to_shared_env_for_an_invalid_snapshot tests.test_runtime_env_snapshot_contract.RuntimeEnvironmentSnapshotContractTest.test_central_runners_use_the_exact_local_snapshot_not_shared_runtime_env
```

Result: PASS, 8 tests.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_nginx_root_broker tests.test_nginx_root_broker_crs_profile tests.test_nginx_root_broker_workflow tests.test_protected_nginx_broker_caller tests.test_ci_security_workflows tests.test_python_version_contract
```

Result: PASS, 123 tests.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest tests.test_runtime_component_cache_contract tests.test_runtime_component_cache_identity
```

Result: PASS, 46 tests.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_runtime_env_snapshot_contract
```

Result: nine tests passed; the one unsuppressed failure is the absent Framework
`ci/lib/common.sh` fixture described above.

```sh
rtk proxy env TMPDIR=../tmp PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -m unittest -v tests.test_python_version_contract
```

Result: PASS, 24 tests.

```sh
rtk proxy make PYTHON=python3 check-ci-security-contract
```

Result: PASS, 26 CI-security workflow tests and checksum-record validation for actionlint, zizmor, and gitleaks.

```sh
rtk proxy make PYTHON=python3 check-bilingual-docs
rtk proxy make PYTHON=python3 check-doc-links
```

Result: both exited nonzero only because this Parent-only external worktree
intentionally lacks the Framework Gitlink's local documentation targets. No
new changed document or Change Record diagnostic was reported; Framework was
not initialized or modified to make the global checks pass.

Checksum-verified actionlint plus ShellCheck passed over all workflow and permission-fixture YAML. Offline zizmor passed over the workflows and safe fixture; it correctly rejected the intentionally unsafe `pull_request_target` fixture. The bare Python-version-contract CLI was also run and reported 21 inherited workflow-inventory violations outside this diff; it reported no Phase-A-specific violation.

```sh
rtk proxy git diff --check
```

Result: exit 0 for the final tracked Phase-A diff.

## Hosted delivery evidence for immutable code head

Not run. No Phase-A commit, push, pull request, hosted check, SonarQube Cloud analysis, or protected lifecycle success is claimed by this record.

## Security impact

The repair retains a fail-closed pre-root boundary: admission is bounded and occurs before copying, candidate creation, or root action. No caller, manifest, environment variable, or evidence input can select a larger limit. The scoped fetch umask preserves private surrounding workflow state while enabling only broker-required fresh CRS source modes.

## Runtime evidence

Run `31368594208` is pre-repair failure evidence only. Both jobs stopped before candidate creation, root admission, `sudo`, NGINX startup, audit, evidence readback, and cleanup verification. No successful no-CRS or `owasp-crs` protected lifecycle is available for this change.

## Known limitations

The available local interpreter is CPython 3.14.4 while `.python-version` requires CPython 3.14.6. Local tests are source/static evidence, not hosted CI-equivalent or protected-root runtime proof. The full snapshot suite has the unsuppressed external-worktree Framework-source error recorded above.

## Remaining risks

This branch still requires final local validation, security review, immutable-head hosted checks, and an explicit SHA-bound merge before a separate caller repin. The findings remain in progress until a resulting-master lifecycle passes both profiles with required evidence and cleanup verification.

## Checks not run and rationale

No local `make fetch-deps`, CRS network fetch, candidate admission, root action, NGINX start, audit, evidence projection, or cleanup run was attempted. Those require the protected resulting-master workflow and are not substitutes for the later Phase-C lifecycle.

## Final diff and review status

Status: in progress. This record is not delivery approval or integration evidence.
