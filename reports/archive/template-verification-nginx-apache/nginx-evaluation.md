> Status: Historical
> Superseded by: [../../current/six-connector-core-completion.md](../../current/six-connector-core-completion.md)
> Date: retained as a historical report during repository organization on 2026-07-12
> Evidence boundary: historical planning, assessment, or snapshot; not current canonical evidence.

# NGINX Evaluation

**Language:** English | [Deutsch](nginx-evaluation.de.md)

Status: reviewed

NGINX rating: partial with current `/src` No-CRS PASS and With-CRS PASS for
executed scope.

Template alignment: aligned for scaffold, origin/license, metadata, build,
harness, external-test references, and executed No-CRS/With-CRS runtime scope.
Detailed phase-by-phase alignment:
`reports/archive/template-verification-nginx-apache/nginx-template-alignment.md`.

Reason: `connectors/nginx` contains an adapter-owned source tree, metadata,
origin documentation, harness files, and connector docs. Current `/src`
runtime targets pass for the executed scope, including the CRS-specific
expectation for `action_status_401_phase1_block`. NGINX remains `partial`
because RESPONSE_BODY blocking is not verified and the full minimum runtime
matrix is not complete.

## Evidence Summary

| Area | Status | Evidence |
| --- | --- | --- |
| README/docs | OK | `connectors/nginx/README.md`, `connectors/nginx/docs/` |
| Local test folder | OK | `connectors/nginx/tests` is absent. |
| Adapter-owned source | OK | `connectors/nginx/src/`, `connectors/nginx/metadata.c`, `connectors/nginx/ORIGIN.md` |
| NGINX build include contract | OK | `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` is supported by `connectors/nginx/config`. |
| Common smoke | PASS | NGINX 54 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS target | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| With-CRS target | PASS | NGINX 61 PASS, 0 FAIL, 0 BLOCKED. |
| No-CRS action status case | PASS | `action_status_401_phase1_block` expected 401, actual 401. |
| With-CRS action status case | PASS | `action_status_401_phase1_block` expected 403, actual 403. |
| CRS SQLi case | PASS | `crs_sqli_anomaly_block` expected 403, actual 403. |
| Historical 11 BLOCKED rows | Resolved | Documented as environment/docroot permission blocker in earlier reports. |
| RESPONSE_BODY blocking | Not verified | Current response-body rows are pass-through or log-only evidence. |
| More than `partial` | Not allowed | Full matrix and RESPONSE_BODY blocking evidence remain incomplete. |
| Template phase alignment | Aligned | See `nginx-template-alignment.md`. |

## Current Runtime Counts

| Command | Scope | PASS | FAIL | BLOCKED |
| --- | --- | ---: | ---: | ---: |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | common | 54 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | all/no-crs | 60 | 0 | 0 |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | all/with-crs | 61 | 0 | 0 |

Evidence files:

- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl`

## CRS Variant Evidence

| Variant | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | `action_status_401_phase1_block` | 401 | 401 | PASS |
| With-CRS | `action_status_401_phase1_block` | 403 | 403 | PASS |
| With-CRS | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

The With-CRS 403 expectation is scoped in the framework testcase and does not
replace the base No-CRS 401 expectation.

## Historical Blocker

The earlier NGINX common run had 43 PASS and 11 BLOCKED. Those rows were not
treated as PASS for the historical run. They were rerun after the docroot work
parent was moved below `BUILD_ROOT`; current `/src` runs record 0 BLOCKED.
Details are in `nginx-docroot-permission-analysis.md` and
`nginx-blocked-runtime-cases.md`.

## Checklist

- [x] README present.
- [x] Docs present.
- [x] Local test folder removed.
- [x] Harness/adapter structure present.
- [x] NGINX build can find `common/include/msconnector/rule_load_stats.h`.
- [x] Current `/src` NGINX common smoke passed.
- [x] Current `/src` NGINX No-CRS target passed.
- [x] Current `/src` NGINX With-CRS target passed.
- [x] Current `/src` NGINX CRS SQLi anomaly case passed.
- [x] No-CRS `action_status_401_phase1_block` preserved as 401/401 PASS.
- [x] With-CRS `action_status_401_phase1_block` documented as 403/403 PASS.
- [x] Historical 11 BLOCKED rows documented and rerun.
- [ ] RESPONSE_BODY blocking verified.
- [ ] Full minimum runtime matrix verified.
- [ ] Connector can be promoted beyond `partial`.

## Decision

NGINX remains `partial`. Current No-CRS, With-CRS, and common runtime targets
are PASS for the executed `/src` scope. The former With-CRS 401/403 mismatch is
resolved by a scoped framework expectation. NGINX still cannot be promoted
beyond `partial` because RESPONSE_BODY blocking and the complete minimum matrix
are not verified.
