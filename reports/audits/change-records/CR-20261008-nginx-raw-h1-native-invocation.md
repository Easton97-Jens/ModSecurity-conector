# Change Record: CR-20261008-nginx-raw-h1-native-invocation

**Language:** English | [Deutsch](CR-20261008-nginx-raw-h1-native-invocation.de.md)

Native invocation producer; unit verification only.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-raw-h1-native-invocation |
| Date (UTC) | 2026-10-08 |
| Base revision | `883693506efa4ce64a016e2a440ac20ace367efd` |

## Motivation and problem statement

Provide an owned native host invocation for the four closed malformed HTTP/1 request contracts without manufacturing Engine events for core-parser rejection.

## Acceptance criteria

Capture exact bounded request/response bytes, one path-bound native access entry, bounded parser diagnostics, positive control and genuine host role/cleanup receipts. Keep canonical_status NOT_EXECUTED.

## Implementation decision and rationale

Reuse owned host role/start/cleanup helpers and closed Framework raw-H1 contracts. Snapshot binary/module/rules, bind loopback listeners, run root master/nobody worker, preserve fault/control wire bytes and receipt hashes. Observation validity is not canonical PASS.

## Changed files

ci/runtime/lifecycle/run-nginx-raw-h1.py; tests/test_nginx_raw_h1_driver.py; this EN/DE pair.

## Commands executed

RTK-wrapped Parent .venv unittest tests.test_nginx_raw_h1_driver passes 3 tests (stream-c-parent-raw.log): generated loopback/root-nobody configuration, actual bounded socket send/receive capture, and exact single access-entry selection with missing/foreign/duplicate negatives. In-memory syntax passes both Python files. ci/tools/new-change-record.py check, make check-bilingual-docs and make check-doc-links (explicit current Framework checkout) pass; diff whitespace is clean.

## Security impact

Closed wire contracts and bounded captures avoid arbitrary input or log retention; role-aware cleanup is reused. Host-core rejection never invents an Engine rule event or canonical result.

## Runtime evidence

No fresh native runtime executed. The 3 unit controls include a real local test socket, not NGINX. Earlier four-case old-build 400/diagnostic probes are not fresh coverage for this commit.

## Known limitations

The source receipt remains NOT_EXECUTED until independent retained-byte/source/build/host and canonical integration checks pass.

## Remaining risks

Fresh integrated build and runtime evidence, source administrative authority and canonical result generation remain coordinator-owned.

## Checks not run and rationale

No build, native NGINX runtime, E2E, remote CI, Sonar or push under this bounded task.

## Final diff and review status

Reviewed the standalone raw host invocation and controlled seam tests; separate four-file commit with generated paired record. Other concurrent files remain untouched.
