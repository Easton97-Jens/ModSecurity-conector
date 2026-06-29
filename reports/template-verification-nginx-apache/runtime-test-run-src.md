# Runtime Test Run Under `/src`

**Language:** English | [Deutsch](runtime-test-run-src.de.md)

Status: current `/src` smokes PASS for No-CRS and With-CRS executed scope

## Current Environment

```text
SOURCE_ROOT=/src
BUILD_ROOT=/src/ModSecurity-conector-build
REFRESH=1
```

Working directory:

```text
/root/git/ModSecurity-conector
```

## Commands

| Command | Result | Summary |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-apache` | PASS | Apache source-build smoke completed before later result directories were refreshed. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED; NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS, 0 FAIL, 0 BLOCKED; NGINX 61 PASS, 0 FAIL, 0 BLOCKED. |

## Evidence Files

Common smoke:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`

No-CRS:

- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`

With-CRS:

- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`

## No-CRS

- Apache: 54 PASS, 0 FAIL, 0 BLOCKED.
- NGINX: 60 PASS, 0 FAIL, 0 BLOCKED.
- Apache `phase1_header_block`: PASS, expected 403, actual 403.
- NGINX `phase1_header_block`: PASS, expected 403, actual 403.
- Apache `response_body_pass`: PASS, expected 200, actual 200.
- NGINX `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not present in the No-CRS summaries.

## With-CRS

- CRS source observed: `/src/coreruleset`.
- CRS runtime preamble observed:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- Apache: 55 PASS, 0 FAIL, 0 BLOCKED.
- NGINX: 61 PASS, 0 FAIL, 0 BLOCKED.
- Apache `crs_sqli_anomaly_block`: PASS, expected 403, actual 403.
- NGINX `crs_sqli_anomaly_block`: PASS, expected 403, actual 403.
- Apache `action_status_401_phase1_block`: PASS, expected 403, actual 403.
- NGINX `action_status_401_phase1_block`: PASS, expected 403, actual 403.

The With-CRS target is therefore PASS for the current `/src` executed scope.
The base No-CRS expectation remains 401; the With-CRS 403 expectation is
variant-specific.

## Historical NGINX Docroot Blocker

The prior `/src` report state had 11 NGINX BLOCKED rows. That state is
preserved in `nginx-blocked-runtime-cases.md`. The current reruns resolved the
BLOCKED rows after the NGINX harness work parent was placed below
`BUILD_ROOT`.

## RESPONSE_BODY

RESPONSE_BODY blocking verified: no.

`response_body_pass` is a pass-through case. NGINX phase-4 pass-through/log-only
rows are not blocking evidence. The current No-CRS and With-CRS summaries do
not include `response_body_basic_block`.

## Decisions

- Apache remains `partial`.
- NGINX remains `partial`.
- No-CRS runtime target: PASS.
- With-CRS runtime target: PASS.
- CRS SQLi anomaly case: PASS for both connectors.
- Full runtime verification: no.
