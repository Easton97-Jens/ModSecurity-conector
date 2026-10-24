# Change Record: CR-20261008-nginx-native-mime-driver

**Language:** English | [Deutsch](CR-20261008-nginx-native-mime-driver.de.md)

Local adapter implementation; final integrated native validation remains pending.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-mime-driver |
| Date (UTC) | 2026-10-08 |
| Base revision | `70bfce7f6e776f49ae3f8160b18fed6b8fe4779a` |

## Motivation and problem statement

Four Required MIME records need genuine native requests and final wire headers, including actual Content-Type absence. Existing HTTP200/empty-log observations do not prove native completion.

## Acceptance criteria

Closed GET/body/MIME inputs, self-contained safe configuration, actual backend omission, bounded owned runtime and genuine retained wire/native artifacts. Fresh module/runtime acceptance remains coordinator work.

## Implementation decision and rationale

A thin MIME adapter delegates host invocation, roles, PIDFD cleanup and curl captures to the Phase-4 runtime's run_operation seam. The existing declarative response-header backend supplies the real missing-header contract. A loopback-only one-request thread has bounded accept/connection timeouts and retires before return. No fixture creates native events.

## Changed files

ci/runtime/lifecycle/run-nginx-mime-cases.py, tests/test_nginx_mime_driver.py and this EN/DE Change Record. The dependency run-nginx-phase4-cases.py and Framework MIME helper are owned by separate slices.

## Commands executed

RTK-wrapped Parent-owned Python: `-m unittest discover -s tests -p 'test_nginx_mime_driver.py' -v` passed3 tests, exit0; `-m unittest discover -s tests -p 'test_nginx_common_input_fault_driver.py' -v` passed2 tests, exit0. These are pure configuration/delegation controls; no native process or listener was started. Python syntax2 passed; Change Record archive structure passed. `make check-bilingual-docs` failed on existing links into the unpopulated Framework submodule in this isolated worktree; no submodule or gitlink was changed to mask that limitation.

## Security impact

Closed identities, exact marker body, safe mode, bounded loopback backend and existing header-omission validation are preserved. Receipt retains actual backend/omission source hashes, adapter hash and underlying runtime hash; canonical validation must independently authenticate artifacts and native facts.

## Runtime evidence

No native runtime was executed for this adapter. Old in/charset diagnostic events and old incomplete out/missing observations remain diagnostic evidence, not this source's acceptance.

## Known limitations

Requires the separate Phase-4 shared runtime seam and Framework MIME operation helper before invocation. Root owns dispatch, receipt registration and source-bound final module build. Source-result remains NOT_EXECUTED until independent canonical validation.

## Remaining risks

Final wire Content-Type absence, native append/completion retention and actual process cleanup need an authorized rebuilt-module run. Native rule1100301 must occur for in/charset and must not be invented for out/missing.

## Checks not run and rationale

Native build/runtime, integrated E2E, full Parent suite and remote CI/Sonar not run; coordinator reserves serialized runtime slot and owns integrated delivery.

## Final diff and review status

Only assigned MIME source/tests/paired record; local commit, no push, merge, gitlink or MRTS changes. Runtime outcome remains partial.
