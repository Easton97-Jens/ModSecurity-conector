# Verified Runtime Run

Status: partial runtime evidence, current `/src` smokes PASS

Date/time: 2026-05-30 15:49:59 UTC

## Environment

Working directory:

```text
/root/git/ModSecurity-conector
```

Runtime environment:

```text
SOURCE_ROOT=/src
BUILD_ROOT=/src/ModSecurity-conector-build
REFRESH=1
```

`FRAMEWORK_ROOT` used the parent Makefile default:

```text
/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework
```

## Commands Executed

| Command | Result | Notes |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX built and ran 60 cases: 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache common: 54 PASS; NGINX common: 54 PASS. |

## Evidence Files

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/nginx.rc`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.txt`

## Latest Summary Counts

Latest files after `make smoke-common`:

| Connector | PASS | FAIL | BLOCKED | XFAIL | Summary path |
| --- | ---: | ---: | ---: | ---: | --- |
| Apache | 54 | 0 | 0 | 0 | `/src/ModSecurity-conector-build/results/apache-summary.json` |
| NGINX | 54 | 0 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.json` |

The earlier `make smoke-nginx` all-scope run produced:

| Connector | PASS | FAIL | BLOCKED | XFAIL | Summary path |
| --- | ---: | ---: | ---: | ---: | --- |
| NGINX | 60 | 0 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.json` at the time of that run |

The all-scope NGINX summary was later overwritten by the final common run, as
expected for the shared results directory.

## Apache Result

Apache verified scope for the current final common run:

- 54 common cases PASS.
- `phase1_header_block`: PASS, expected 403, actual 403.
- `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not executed in this run.

Decision: Apache remains `partial`. This run verifies the listed common cases,
but does not verify response-body blocking and does not prove the full minimum
matrix.

## NGINX Result

NGINX verified scope for the current final common run:

- 54 common cases PASS.
- 0 common cases FAIL.
- 0 common cases BLOCKED.
- `phase1_header_block`: PASS, expected 403, actual 403.
- `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not executed in this run.

Decision: NGINX remains `partial`. The prior 11 BLOCKED rows were resolved by
using a traversable build-root work parent for the generated docroot, but the
run still does not verify response-body blocking or the full minimum matrix.

## Prior NGINX BLOCKED Rows

The prior `/src` report state had NGINX 43 PASS, 0 FAIL, and 11 BLOCKED. That
state is preserved and classified in
`reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`.
The current result files now show NGINX 54 PASS, 0 FAIL, 0 BLOCKED for common
scope.

## RESPONSE_BODY

RESPONSE_BODY blocking verified: no.

Reason:

- `response_body_pass` is pass-through evidence only.
- `response_body_basic_block` was not executed in the current run.
- No current runtime evidence proves a blocking response-body trigger with a
  blocking result such as HTTP 403 for both Apache and NGINX.

## Overall Decisions

- Apache verified scope: current `/src` common runtime cases, 54 PASS.
- NGINX verified scope: current `/src` common runtime cases, 54 PASS.
- Historical NGINX 11 BLOCKED rows: resolved in current `/src` reruns.
- Apache rating: partial.
- NGINX rating: partial.
- RESPONSE_BODY blocking: not verified.
- More than `partial`: not allowed from this run.
- Full runtime verification: no.
