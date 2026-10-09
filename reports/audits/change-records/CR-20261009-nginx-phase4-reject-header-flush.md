# Change Record: CR-20261009-nginx-phase4-reject-header-flush

**Language:** English | [Deutsch](CR-20261009-nginx-phase4-reject-header-flush.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-phase4-reject-header-flush |
| Date (UTC) | 2026-10-09 |
| Base revision | `75686a47ba971d33c46f4f40a844bbe53d7465f1` |
| Integration parent revision | `af82baac81a5a51ed062507688494e72d6480eeb` |
| Framework revision | `4c6c21e8622840b4c218d8ea5520dd0b10b3fac9` |
| MRTS revision | `8a6bb546c4c81d8ffc7be801dceac60c6925685f` |

## Motivation and problem statement

The real R11 `phase4_body_reject` invocation recorded internal `header_sent=true` and committed status 200, but curl received an empty reply (exit 52, HTTP 0). NGINX 1.31.6 defaults to `postpone_output 1460`; the short headers remained postponed when the immediate body Reject aborted the connection. Internal commitment alone does not prove delivery to the client.

## Acceptance criteria

Only the exact `phase4_body_reject` invocation must use `postpone_output 0;`; the seven other closed Phase-4 cases retain their configuration. Inputs, case identity, URI, run ID, mode, rules, required selection and validators remain unchanged. A subsequent real Root-master/nobody-worker probe must retain HTTP 200 headers, curl exit 18 and zero body bytes before runtime completion can be claimed.

## Implementation decision and rationale

The Parent driver adds the keyword-only option `flush_response_headers=False` and selects it through a configuration-factory partial only for `phase4_body_reject`. The directive applies to that invocation's exact location. This changes test-host output scheduling without changing product source or binary semantics. Regression tests compare the complete configuration after removing the one authorized directive and cover all eight closed cases.

## Changed files

- `ci/runtime/lifecycle/run-nginx-phase4-cases.py`
- `tests/test_nginx_phase4_driver.py`
- `reports/audits/change-records/CR-20261009-nginx-phase4-reject-header-flush.md`
- `reports/audits/change-records/CR-20261009-nginx-phase4-reject-header-flush.de.md`

## Commands executed

Commands ran from the Parent worktree through RTK. `${PARENT_PYTHON}` denotes the selected Parent virtual-environment interpreter; `${FRAMEWORK_ROOT}` denotes the explicit Framework worktree. Set these to the corresponding local checkouts. These portable commands preserve the executed payloads:

```sh
rtk proxy env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p test_nginx_phase4_driver.py -v
rtk proxy env PYTHONNOUSERSITE=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p 'test_nginx_phase4_*.py' -v
rtk proxy env PYTHONNOUSERSITE=1 "${PARENT_PYTHON}" -m unittest discover -s tests -p 'test_nginx_*driver.py' -v
rtk proxy env PYTHONNOUSERSITE=1 FRAMEWORK_ROOT="${FRAMEWORK_ROOT}" "${PARENT_PYTHON}" -m unittest tests.test_nginx_common_input_fault_driver.InputFaultDriverTest.test_source_bound_protocol_selection_retains_cleanup_and_raw tests.test_nginx_driver_contract_tables -v
rtk proxy env PYTHONNOUSERSITE=1 "${PARENT_PYTHON}" -c 'from pathlib import Path; [compile(Path(name).read_bytes(), name, "exec") for name in ("ci/runtime/lifecycle/run-nginx-phase4-cases.py", "tests/test_nginx_phase4_driver.py")]'
rtk git diff --check
```

Focused RED: 11 tests, one FAIL and one ERROR, exit 1. Focused GREEN: 11 tests, exit 0. Phase-4 neighbors: 46 tests, exit 0, no skips. Driver neighbors: 138 tests, exit 0, one explicit-Framework-root prerequisite skip. The skipped control plus contract-table suite subsequently ran with explicit `FRAMEWORK_ROOT`: eight tests, exit 0, no skips. Syntax and diff checks: exit 0. The native Change Record scaffold command also exited 0. These are unit/configuration checks, not real HTTP evidence.

Documentation validation also passed: `rtk proxy "${PARENT_PYTHON}" ci/tools/new-change-record.py check`, `rtk make check-bilingual-docs PYTHON="${PARENT_PYTHON}"` and `rtk make check-doc-links PYTHON="${PARENT_PYTHON}" FRAMEWORK_ROOT="${FRAMEWORK_ROOT}"`, all exit 0. The archive check proves structure only. Manual review confirmed EN/DE factual parity; RTK version/gain verification and `rtk git diff --check` exited 0.

## Security impact

No authorization, path authority, projection freshness, Root/nobody isolation, framing validation or required evidence control changes. No Framework or MRTS change belongs to this Parent fix. No secrets or private payloads are stored in this record.

## Runtime evidence

R11 remains FAIL; its original curl exit 52/HTTP 0 observation is retained. No corrected real request has been executed for this record yet. The required bounded Root-master/nobody-worker probe must capture real raw headers, HTTP 200, curl exit 18, zero body bytes and cleanup. Unit GREEN does not establish Canonical PASS.

## Known limitations

`header_sent` describes NGINX's internal commitment rather than wire delivery. The directive is restricted to the immediate body Reject case. Other independent R11 Framework defects and the full required lifecycle remain outside this isolated scheduling change.

## Remaining risks

The real probe and a fresh integrated required run must confirm client-visible behavior with the actual NGINX 1.31.6 artifacts. Existing failed evidence cannot be relabeled as corrected evidence.

## Checks not run and rationale

The corrected real probe, fresh Full97 run, Canonical finalization, protected workflow and current-head CI/Sonar delivery checks have not been executed for this change. They require root integration after independent fixes and source binding. No commit or push was performed by the documentation task.

## Final diff and review status

The source diff is limited to the Parent Phase-4 driver and its regressions, accompanied by this EN/DE pair. Product binaries, Framework validators and required selection remain unchanged by this fix. Integration review and runtime acceptance are pending; PR #396 remains Draft.
