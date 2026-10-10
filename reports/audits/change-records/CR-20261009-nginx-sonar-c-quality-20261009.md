# Change Record: CR-20261009-nginx-sonar-c-quality-20261009

**Language:** English | [Deutsch](CR-20261009-nginx-sonar-c-quality-20261009.de.md)

Bounded isolated patch; no native runtime or scanner closure evidence.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-sonar-c-quality-20261009 |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

Fresh C findings require narrow structural changes while retaining actual native observations, intervention ownership and post-return budget precedence.

## Acceptance criteria

Preserve existing caller and Common serializer controls; reject invalid socket metadata; retain all P4 completion predicates and terminal event/status behavior.

## Implementation decision and rationale

Group retained/seen/supplied/append_calls into a const input structure (seven parameters); extract only bounded Rule-ID parsing; expand nested conditionals with identical short-circuit behavior; split declarations and reduce loop-variable scope. Initialize both socket output structures without relaxing the role/socket checks.

## Changed files

`connectors/nginx/src/ngx_http_modsecurity_module.c`, `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`, `connectors/nginx/src/ngx_http_modsecurity_phase4_observation.h`; `tests/fixtures/nginx_engine_budget_fault.c`, `tests/fixtures/nginx_phase4_observation.c`, `tests/fixtures/nginx_response_body_limit.c`, `tests/fixtures/nginx_write_fault.c`; `tests/test_nginx_cleanup_observation.c`, `tests/test_nginx_native_intervention_chain.py`, `tests/test_nginx_write_fault_socket_scope.py`, and this EN/DE pair.

## Commands executed

Root integration:the existing inline Rule-ID source guard first failed after helper extraction (65 tests, one failure, exit1). The guard now inspects the actual bounded helper and call ordering, with missing/late/unbounded/gated-extraction negative controls. The integrated nine-module RTK-wrapped focus then passed66 tests/5.494s/exit0 without skips. `tests/test_nginx_upstream_security_contract.py` is additionally changed. These remain source/compiled unit checks, not fresh NGINX runtime evidence.

Final additional checks:all seven affected C fixture/cleanup files C17 syntax exit0; three changed Python files py_compile exit0; `tests.test_change_record` and `tests.test_prepare_reviewed_framework_handoff`:39 tests, exit0; record archive check exit0; path/link diagnostics on the four new records:0 errors. `make check-bilingual-docs` and `make check-doc-links` failed on existing submodule links because the isolated worktree's Framework directory is unpopulated. Explicit external FRAMEWORK_ROOT does not replace those relative links. No missing dependency was changed or check weakened.

All commands used RTK. Existing six-suite characterization:27 tests, exit0. Seven focused suites after changes:34 tests, exit0. Direct C17 cleanup compilation and executable:exit0. Suite names: `tests.test_nginx_phase4_observation`, `tests.test_nginx_phase4_native_body_source`, `tests.test_nginx_native_intervention_chain`, `tests.test_nginx_engine_budget_bridge`, `tests.test_nginx_response_body_limit`, `tests.test_nginx_common_input_fault_scope`, `tests.test_nginx_write_fault_socket_scope`. Framework environment bound to `7db219af6b6e911b73de8b437f82e63efdb06bde`; temporary files external. Documentation verification follows separately.

## Security impact

No native result, role, path, payload, status or evidence gate is weakened. Socket controls cover syscall errors, short outputs, wrong families/addresses/port, wrong UID/PPID/master and incompletely populated outputs. The constructor still requires actual Native1 and Common-completed P4.

## Runtime evidence

None. Controlled C17 host/syscall tests and actual Common serialization are not hosted native lifecycle evidence.

## Known limitations

The S836 signal does not establish a real kernel-contract violation. Zero-initialization is defensive. No scanner closure is claimed. The inherited-FD security migration has a separate record.

## Remaining risks

Fresh integrated source checks and Sonar readback remain required; extraction test fixtures must retain the actual helper.

## Checks not run and rationale

Native build/runtime and publication were excluded and remain Root-owned. No scanner was launched from the changed checkout.

## Final diff and review status

Focused tests and whitespace check passed. Changes are retained unstaged in an isolated worktree; no Git write was performed.
