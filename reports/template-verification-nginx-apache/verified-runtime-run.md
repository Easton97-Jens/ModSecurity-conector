# Verified Runtime Run

Status: partial runtime evidence, current `/src` No-CRS and With-CRS targets
passing for executed scope

Updated: 2026-05-30 20:55:03 UTC

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

Framework root:

```text
/root/git/ModSecurity-conector/modules/ModSecurity-test-Framework
```

## Commands Executed

| Command | Result | Notes |
| --- | --- | --- |
| `make generate-test-matrix` | PASS | Generator exited 0; generated reporting is not runtime proof. |
| `make check-test-matrix` | FAIL | Exited 2 because generated reports intentionally differ from HEAD in this uncommitted HAProxy matrix update. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS; NGINX 61 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache common 54 PASS; NGINX common 54 PASS; both 0 FAIL and 0 BLOCKED. |

Framework-local checks:

| Command | Result | Notes |
| --- | --- | --- |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Command exited 0; it printed a warning that framework-local `config/testing/import-status.json` was not found. |

Earlier `/src` connector smokes are still documented in other reports, but the
current target evidence above is the basis for this file.

## Evidence Files

Common smoke:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/nginx.rc`

No-CRS target:

- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx.rc`

With-CRS target:

- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/with-crs/nginx.rc`

CRS paths:

- CRS source: `/src/coreruleset`
- CRS runtime preamble:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

## Summary Counts

| Target | Connector | PASS | FAIL | BLOCKED | Result file |
| --- | --- | ---: | ---: | ---: | --- |
| `smoke-common` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/apache-summary.txt` |
| `smoke-common` | NGINX | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.txt` |
| `test-no-crs` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt` |
| `test-no-crs` | NGINX | 60 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt` |
| `test-with-crs` | Apache | 55 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt` |
| `test-with-crs` | NGINX | 61 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt` |

All listed `.rc` files for these targets contain `0`.

## No-CRS Runtime Verification

Command:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs
```

Result: PASS.

Important case evidence:

- Apache `action_status_401_phase1_block`: PASS, expected 401, actual 401.
- NGINX `action_status_401_phase1_block`: PASS, expected 401, actual 401.
- Apache `phase1_header_block`: PASS, expected 403, actual 403.
- NGINX `phase1_header_block`: PASS, expected 403, actual 403.
- Apache `response_body_pass`: PASS, expected 200, actual 200.
- NGINX `response_body_pass`: PASS, expected 200, actual 200.

`response_body_pass` is pass-through evidence only and does not prove
RESPONSE_BODY blocking.

## With-CRS Runtime Verification

Command:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
```

Result: PASS.

CRS setup evidence:

- `MODSECURITY_TEST_VARIANT=with-crs`
- CRS source: `/src/coreruleset`
- CRS runtime preamble:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

Important case evidence:

| Connector | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| Apache | `action_status_401_phase1_block` | 403 | 403 | PASS |
| NGINX | `action_status_401_phase1_block` | 403 | 403 | PASS |
| Apache | `crs_sqli_anomaly_block` | 403 | 403 | PASS |
| NGINX | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

The With-CRS 403 expectation for `action_status_401_phase1_block` is scoped
through the framework case's `expect.variants.with-crs.status`. The base
No-CRS expectation remains 401.

## RESPONSE_BODY

RESPONSE_BODY blocking verified: no.

Reason:

- `response_body_pass` is pass-through evidence only.
- NGINX-specific phase-4 rows in the current summaries are pass-through or
  log-only evidence, not blocking evidence.
- No current runtime evidence proves a blocking response-body trigger with a
  blocking result such as HTTP 403 for both Apache and NGINX.

## Overall Decisions

- Apache No-CRS scope: PASS, 54 PASS, 0 FAIL, 0 BLOCKED.
- NGINX No-CRS scope: PASS, 60 PASS, 0 FAIL, 0 BLOCKED.
- Apache With-CRS scope: PASS, 55 PASS, 0 FAIL, 0 BLOCKED.
- NGINX With-CRS scope: PASS, 61 PASS, 0 FAIL, 0 BLOCKED.
- CRS SQLi anomaly case: PASS for Apache and NGINX.
- Former With-CRS `action_status_401_phase1_block` mismatch: resolved by a
  scoped With-CRS expectation.
- Apache rating: partial.
- NGINX rating: partial.
- RESPONSE_BODY blocking: not verified.
- More than `partial`: not allowed from this run.
- Full runtime verification: no.
