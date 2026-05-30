# Verified Runtime Run

Status: partial runtime evidence, current `/src` smokes separated by CRS mode

Date/time: 2026-05-30 17:45:08 UTC

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
| `make generate-test-matrix` | PASS | Generator exited 0; generated reporting is not runtime proof. |
| `make check-test-matrix` | PASS | Matrix check exited 0. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-apache` | PASS | Apache source-build smoke completed before the common rerun. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX all-scope: 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache common: 54 PASS; NGINX common: 54 PASS. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | FAIL | Apache 54 PASS / 1 FAIL; NGINX 60 PASS / 1 FAIL; both fail on `action_status_401_phase1_block`, expected 401 and actual 403. |

## Evidence Files

Common smoke:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`

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

CRS paths from the current run:

- CRS source: `/src/coreruleset`
- CRS runtime preamble:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

## Latest Common Smoke Counts

Latest files after `make smoke-common`:

| Connector | PASS | FAIL | BLOCKED | XFAIL | Summary path |
| --- | ---: | ---: | ---: | ---: | --- |
| Apache | 54 | 0 | 0 | 0 | `/src/ModSecurity-conector-build/results/apache-summary.json` |
| NGINX | 54 | 0 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.json` |

The earlier `make smoke-nginx` all-scope run produced NGINX 60 PASS, 0 FAIL,
and 0 BLOCKED. The shared top-level result files were later overwritten by
`make smoke-common`, as expected for that results directory.

## No-CRS Runtime Verification

Command:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs
```

Result: PASS.

| Connector | PASS | FAIL | BLOCKED | XFAIL | Summary path |
| --- | ---: | ---: | ---: | ---: | --- |
| Apache | 54 | 0 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json` |
| NGINX | 60 | 0 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json` |

No-CRS phase and area evidence:

| Connector | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Request body | Response body | Audit/log | Negative/pass-through |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | 17 PASS | 34 PASS | 2 PASS | 1 PASS | 12 PASS | 1 PASS, pass-through only | 5 PASS | 10 PASS |
| NGINX | 18 PASS | 36 PASS | 2 PASS | 4 PASS | 12 PASS | 4 PASS, pass-through/log-only only | 5 PASS | 13 PASS |

Important case evidence:

- Apache `phase1_header_block`: PASS, expected 403, actual 403.
- NGINX `phase1_header_block`: PASS, expected 403, actual 403.
- Apache `action_status_401_phase1_block`: PASS, expected 401, actual 401.
- NGINX `action_status_401_phase1_block`: PASS, expected 401, actual 401.
- Apache `response_body_pass`: PASS, expected 200, actual 200.
- NGINX `response_body_pass`: PASS, expected 200, actual 200.
- `response_body_basic_block`: not present in the No-CRS summaries.
- `crs_sqli_anomaly_block`: not present in the No-CRS summaries.

Decision: No-CRS evidence improves current runtime confidence for the executed
scope, but it does not verify response-body blocking and does not prove the
full minimum matrix.

## With-CRS Runtime Verification

Command:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
```

Result: FAIL.

CRS setup was executed by the Make target:

- `MODSECURITY_TEST_VARIANT=with-crs`
- `MODSECURITY_RULE_PREAMBLE_FILE=/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`
- CRS source path observed: `/src/coreruleset`
- CRS runtime preamble observed:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

| Connector | PASS | FAIL | BLOCKED | XFAIL | Summary path |
| --- | ---: | ---: | ---: | ---: | --- |
| Apache | 54 | 1 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json` |
| NGINX | 60 | 1 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json` |

With-CRS phase and area evidence:

| Connector | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Request body | Response body | Audit/log | Negative/pass-through | CRS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | 16 PASS, 1 FAIL | 35 PASS | 2 PASS | 1 PASS | 12 PASS | 1 PASS, pass-through only | 5 PASS | 10 PASS | 1 PASS |
| NGINX | 17 PASS, 1 FAIL | 37 PASS | 2 PASS | 4 PASS | 12 PASS | 4 PASS, pass-through/log-only only | 5 PASS | 13 PASS | 1 PASS |

Failing case for both connectors:

| Connector | Case | Expected | Actual | Path |
| --- | --- | ---: | ---: | --- |
| Apache | `action_status_401_phase1_block` | 401 | 403 | `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml` |
| NGINX | `action_status_401_phase1_block` | 401 | 403 | `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml` |

Analysis:

- Detailed report:
  `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`.
- The exact root cause is not proven.
- The most likely classification from reviewed evidence is a With-CRS
  expected-status/context mismatch, likely involving CRS/default-action
  interaction or framework testcase expectation. It is not evidenced as a
  connector-specific Apache-only or NGINX-only bug because both connectors pass
  the same case without CRS and both return 403 with CRS loaded.

CRS-specific case evidence:

| Connector | Case | Status | Expected | Actual | Path |
| --- | --- | --- | ---: | ---: | --- |
| Apache | `crs_sqli_anomaly_block` | PASS | 403 | 403 | `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml` |
| NGINX | `crs_sqli_anomaly_block` | PASS | 403 | 403 | `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml` |

Decision: With-CRS CRS loading and the CRS SQLi anomaly case have PASS
evidence for both connectors, but the overall `test-with-crs` target is FAIL
because one Phase 1 status-code case fails for both connectors.

## RESPONSE_BODY

RESPONSE_BODY blocking verified: no.

Reason:

- `response_body_pass` is pass-through evidence only.
- NGINX-specific phase-4 rows in the current summaries are pass-through or
  log-only evidence, not blocking evidence.
- `response_body_basic_block` was not present in the current No-CRS or
  With-CRS summaries.
- No current runtime evidence proves a blocking response-body trigger with a
  blocking result such as HTTP 403 for both Apache and NGINX.

## Overall Decisions

- Apache No-CRS scope: PASS, 54 PASS, 0 FAIL, 0 BLOCKED.
- NGINX No-CRS scope: PASS, 60 PASS, 0 FAIL, 0 BLOCKED.
- Apache With-CRS scope: FAIL, 54 PASS, 1 FAIL, 0 BLOCKED.
- NGINX With-CRS scope: FAIL, 60 PASS, 1 FAIL, 0 BLOCKED.
- CRS SQLi anomaly case: PASS for Apache and NGINX.
- Historical NGINX 11 BLOCKED rows: resolved in current `/src` reruns.
- Apache rating: partial.
- NGINX rating: partial.
- RESPONSE_BODY blocking: not verified.
- More than `partial`: not allowed from this run.
- Full runtime verification: no.
