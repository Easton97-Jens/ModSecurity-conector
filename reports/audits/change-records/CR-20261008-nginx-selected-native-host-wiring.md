# Change Record: CR-20261008-nginx-selected-native-host-wiring

**Language:** English | [Deutsch](CR-20261008-nginx-selected-native-host-wiring.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-selected-native-host-wiring |
| Date (UTC) | 2026-10-08 |
| Base revision | `b7f3bb22a8ee5ebfe78a0f3b4fb3b32238200f91` |

## Motivation and problem statement

Before editing, read-only `select_cases('nginx', manifest, catalog, 'no_crs_baseline', 'full_lifecycle', 'http1')` against current source returned 97 selected cases, including all 42 native descriptors. The host wrapper called only Framework smoke and Parent configtests; the native dispatcher was never invoked.

## Acceptance criteria

Invoke the existing closed native dispatcher after smoke and configtests, preserve selection/run/source inputs and five mandatory fault-library inputs, retain smoke > config > native exit precedence, and keep missing selected fixtures strict. Do not change the dispatcher, baseline/collector, Framework proof, artifacts or runtime policy.

## Implementation decision and rationale

`run-nginx-selected-host.sh` now calls smoke, configtests and `run-selected-nginx-native-operations.py` in that order, recording each actual exit. `run_framework_host` reasserts the provided selected IDs/fixtures, run ID, projection parent, Parent/Framework tuple fields and five fault-library variables after component provisioning. An explicit caller `NGINX_PREFIX` is reasserted conditionally; an absent caller prefix keeps the actual provisioned snapshot prefix instead of an invented empty value. BUILD_ROOT, RESULTS_DIR and FRAMEWORK_ROOT remain the same. The unchanged dispatcher derives real Git identities and creates fresh isolated projection children.

## Changed files

`ci/runtime/lifecycle/run-nginx-selected-host.sh`, `ci/runtime/lifecycle/run-connector-stage.sh`, new `tests/test_nginx_selected_native_wiring.py` and this EN/DE pair. Root-owned `run-no-crs-baseline.sh`, authority/finalizer/schema and collector integration are not changed. No Framework/MRTS/Gitlink edits.

## Commands executed

`rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_selected_native_wiring` initially exited 1 with seven failed assertions, then passed six tests. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_selected_native_wiring tests.test_nginx_native_operation_dispatch tests.test_no_crs_selected_runner_wiring.NoCrsSelectedRunnerWiringTest.test_stage_rejects_missing_selected_cases_and_preserves_dispatch_controls` passed 15 tests with exit 0 and no skips. `rtk proxy sh -n ci/runtime/lifecycle/run-nginx-selected-host.sh ci/runtime/lifecycle/run-connector-stage.sh` and `rtk git diff --check` exited 0. Parent record archive/pair checks validate document structure only.

## Security impact

No catalog-supplied subprocess is introduced: the existing closed dispatcher retains its 42-case whitelist, exact-source receipts, safe fresh outputs and mandatory missing-fault-library rejection. `NGX_NATIVE_INPUT_FAULT_LIBRARY`, `NGX_NATIVE_BEGIN_FAULT_LIBRARY`, `NGX_NATIVE_WRITE_FAULT_LIBRARY`, `NGX_NATIVE_FINISH_FAULT_LIBRARY` and `NGX_NATIVE_ENGINE_BUDGET_FAULT_LIBRARY` are forwarded without a no-fault fallback. Missing dispatchers and native failures cannot silently become success.

## Runtime evidence

Tests execute the actual Parent shell scripts with controlled smoke/config/native/provisioning collaborators. They prove invocation order, input propagation and exit behavior only; no NGINX build, native request, canonical PASS or Exact-Head evidence is claimed.

## Known limitations

The read-only 42-case selection is source planning, not proof of native execution. Actual binary/module/fault-library identity and canonical bundle proof remain Root/Framework responsibilities.

## Remaining risks

Root still must wire baseline collection authority and finalized bundle retention, provide genuine rebuilt fault libraries, and run serialized native verification. The unchanged dispatcher independently seals real P/F/M revisions rather than trusting test tuple values.

## Checks not run and rationale

Build, native runtime, full E2E, canonical Required-case verification and remote CI/Sonar were not run: this task authorizes only bounded Parent wiring and controlled tests. Existing isolated-submodule link failures are outside this slice.

## Final diff and review status

Reviewed the two owned shell scripts, focused tests and paired record. Existing smoke/config routes, strict selected-fixture guard and exit precedence remain intact. No runtime evidence or PASS was fabricated; unrelated work is preserved.
