# Change Record: CR-20261009-nginx-driver-contract-construction

**Language:** English | [Deutsch](CR-20261009-nginx-driver-contract-construction.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-driver-contract-construction |
| Date (UTC) | 2026-10-09 |
| Base revision | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |

## Motivation and problem statement

Sonar identified repeated rejection fields and sequence schedules between Parent producers and independent Framework contracts. Remove repetition inside Parent construction while preserving that independence. Do not import validator expectations into a producer.

## Acceptance criteria

Preserve all nine full rejection dictionaries, field types and key order, and all 22 sequence identifiers, status tuples and invocation order. Independent Framework parity and changed-value controls must pass. No selection, validator, observation, receipt, freshness or runtime behavior change.

## Implementation decision and rationale

The local pure `rejection_contract` constructor centralizes fixed config-only rejection fields and creates a separate diagnostic list per call. Case-specific directives, values and diagnostics remain explicit. Sequence schedules group only adjacent equal inputs before flattening into the existing ordered dictionary. Producer expectations remain independently authored; validators are unchanged. No new helper source file or source-capture boundary.

## Changed files

- `ci/runtime/lifecycle/run-nginx-configtest.py`
- `ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`
- `tests/test_nginx_driver_contract_tables.py`
- `reports/audits/change-records/CR-20261009-nginx-driver-contract-construction.md`
- `reports/audits/change-records/CR-20261009-nginx-driver-contract-construction.de.md`

## Commands executed

All commands use `rtk proxy`, the selected Parent virtual-environment Python, external `TMPDIR` / `PYTHONPYCACHEPREFIX`, and `PYTHONNOUSERSITE=1`. `$PARENT_PYTHON` denotes that interpreter.

- Before refactoring: `$PARENT_PYTHON -m unittest -v tests.test_nginx_driver_contract_tables`: exit 0, six tests. Full baseline snapshots, independent Framework parity and changed-value/order negative controls passed on unchanged drivers.
- Native scaffold: `ci/tools/new-change-record.py create --name nginx-driver-contract-construction --base-revision 240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee --date 2026-10-09`: exit 0.

Post-refactor: `$PARENT_PYTHON -m unittest -v tests.test_nginx_driver_contract_tables tests.test_nginx_configtest_driver tests.test_nginx_selected_configtest_wiring tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases tests.test_nginx_native_operation_dispatch`: exit 0, 87 tests in 71.165s, no skips. Both `FRAMEWORK_ROOT` and `NGINX_NATIVE_REGISTRY_FRAMEWORK_ROOT` explicitly name the existing pinned Framework checkout. The earlier 86-test run passed with one registry-check skip; the final run executed that check and the new constructor independence test.

`$PARENT_PYTHON -m py_compile` on the three Python files, `ci/tools/new-change-record.py check`, and `git diff --check`: all exit 0. The archive check validates structure only. Logs: `driver-contract-characterization-before.log`, `driver-contract-focus-after.log`, `driver-contract-focus-final.log`, `driver-contract-static.log`, with observed exit files in the external task analysis root. These are input-contract/unit checks, not a native NGINX execution.

## Security impact

No authorization, isolation or validation controls change. The constructor creates inputs only. Observed exits, diagnostics, identities and fault receipts still require independent checks. No synthetic PASS or runtime evidence.

## Runtime evidence

None in this isolated refactor. Controlled unit executables are not genuine NGINX runtime proof. Root integration owns the subsequent real Exact-Head run.

## Known limitations

The isolated worktree has no populated Framework submodule. Parity tests explicitly read the existing exact-pinned standalone Framework checkout. This does not populate missing documentation-link targets or prove runtime behavior.

## Remaining risks

Fresh integrated checks and Sonar readback remain required before delivery claims. Expected inputs remain independent of producer observations and Framework validators.

## Checks not run and rationale

No builds, runtime probes, privileged runs, ports, full E2E, scanner publication, Git commit/push or Framework/MRTS writes. Full documentation checks require populated Framework integration; archive structure and manual EN/DE parity are separate checks. No dependency/toolchain installation.

## Final diff and review status

Only the two producer files, new characterization module and EN/DE record pair changed. Root review/integration remain required. No profile reduction, exclusions, identifier-only evasion or weakened Quality Gate.
