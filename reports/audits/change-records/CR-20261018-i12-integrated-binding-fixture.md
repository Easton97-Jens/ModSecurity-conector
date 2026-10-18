# Change Record: CR-20261018-i12-integrated-binding-fixture

**Language:** English | [Deutsch](CR-20261018-i12-integrated-binding-fixture.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-integrated-binding-fixture |
| Date (UTC) | 2026-10-18 |
| Base revision | `f9a5ed7112c1c8ab468892d813ac60891567dcab` |

## Motivation and problem statement

The integrated HAProxy binding now reads request.http_version. Its synthetic evaluation fixture omitted that field and failed compilation before running any test, also blocking the integrated Traefik PR checks.

The I09 host-result fixture also lacked its newly extracted response-abort dependency. Its caller regression now models that transport dependency with the existing shutdown counter; this unit test does not claim to exercise HTX queue or transport internals.

## Acceptance criteria

Restore the synthetic request layout and initialize the HTTP version explicitly. Retain compiler warnings, evaluation ordering, all error-path tests and product behavior.

## Implementation decision and rationale

Add only the missing const char pointer and the fixture value 1.1. No production behavior changes or new HAProxy feature work.

## Changed files

tests/test_haproxy_binding_refactor.py, tests/test_haproxy_host_native_results.py and this EN/DE Change Record pair.

## Commands executed

RTK-wrapped Parent-venv unittest tests.test_haproxy_binding_refactor reproduced the missing-member compiler error before the fix (zero tests executed); after the fix all eight tests passed. Exact commands, exits and log hashes are retained as root-haproxy-fixture-before-20261018 and root-haproxy-fixture-after-20261018 receipts in the acceptance run.

The second compiler failure was separately reproduced and retained as root-haproxy-host-fixture-before-20261018. The combined two-module retake passed all nine tests; root-haproxy-fixtures-integrated-after-20261018 retains its exact command and hashes. EN/DE, links and Change Record checks passed separately.

## Security impact

The fixture again compiles and exercises the existing binding cleanup/error paths. No security control, warning or test is removed.

## Runtime evidence

No host execution or original-case qualification is claimed by this synthetic fixture repair.

## Known limitations

The fixture remains a unit-level evaluation model; real host lifecycle evidence remains separately required.

## Remaining risks

Final hosted checks must run on the subsequently integrated published head.

## Checks not run and rationale

No additional host run was needed to establish this compile-only fixture defect. Hosted CI and Sonar await publication.

## Final diff and review status

The bounded two-line fixture change was reviewed against the current binding and passed its eight tests. Integration preserves published history.
