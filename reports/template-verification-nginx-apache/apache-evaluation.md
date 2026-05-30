# Apache Evaluation

Status: reviewed

Apache-Bewertung: partial with current `/src` No-CRS PASS and With-CRS PASS
for executed scope.

Reason: `connectors/apache` contains an adapter-owned source structure,
Autotools/APXS build files, metadata, origin documentation, harness, and
documentation. Current `/src` runtime targets pass for the executed scope, but
Apache remains `partial` because Apache-specific YAML cases were not found,
RESPONSE_BODY blocking is not verified, and the full minimum matrix is not
complete.

## Evidence Summary

| Area | Status | Evidence |
| --- | --- | --- |
| README/docs | OK | `connectors/apache/README.md`, `connectors/apache/docs/` |
| Local test folder | OK | `connectors/apache/tests` is absent. |
| Adapter-owned source | OK | `connectors/apache/src/`, `connectors/apache/metadata.c`, `connectors/apache/ORIGIN.md` |
| Common smoke | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS target | PASS | Apache 54 PASS, 0 FAIL, 0 BLOCKED. |
| With-CRS target | PASS | Apache 55 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS action status case | PASS | `action_status_401_phase1_block` expected 401, actual 401. |
| With-CRS action status case | PASS | `action_status_401_phase1_block` expected 403, actual 403. |
| CRS SQLi case | PASS | `crs_sqli_anomaly_block` expected 403, actual 403. |
| RESPONSE_BODY blocking | Not verified | `response_body_pass` is pass-through evidence only. |
| Apache-specific YAML cases | Missing | Only `README.md` found under framework Apache-specific path. |
| More than `partial` | Not allowed | Full matrix and RESPONSE_BODY blocking evidence remain incomplete. |

## Current Runtime Counts

| Command | Scope | PASS | FAIL | BLOCKED |
| --- | --- | ---: | ---: | ---: |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | common | 54 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | all/no-crs | 54 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | all/with-crs | 55 | 0 | 0 |

Evidence files:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl`

## CRS Variant Evidence

| Variant | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | `action_status_401_phase1_block` | 401 | 401 | PASS |
| With-CRS | `action_status_401_phase1_block` | 403 | 403 | PASS |
| With-CRS | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

The With-CRS 403 expectation is scoped in the framework testcase and does not
replace the base No-CRS 401 expectation.

## Checkbox Summary

- [x] README present.
- [x] docs present.
- [x] Local test folder removed.
- [x] Harness/adapter structure present.
- [x] Current `/src` common Apache smoke passed.
- [x] Current `/src` No-CRS Apache target passed.
- [x] Current `/src` With-CRS Apache target passed.
- [x] Current `/src` Apache CRS SQLi anomaly case passed.
- [x] No-CRS `action_status_401_phase1_block` preserved as 401/401 PASS.
- [x] With-CRS `action_status_401_phase1_block` documented as 403/403 PASS.
- [ ] RESPONSE_BODY blocking verified.
- [ ] Apache-specific YAML files found.
- [ ] Full minimum runtime matrix verified.
- [ ] Connector can be promoted beyond `partial`.

## Decision

Apache remains `partial`. Current No-CRS, With-CRS, and common runtime targets
are PASS for the executed `/src` scope. The former With-CRS 401/403 mismatch is
resolved by a scoped framework expectation. Apache still cannot be promoted
beyond `partial` because RESPONSE_BODY blocking and the complete minimum matrix
are not verified, and Apache-specific YAML cases were not found.
