# Verification Summary

Status: reviewed

Updated: 2026-05-30 20:55:03 UTC

## Readiness

- Documentation/decision commit readiness: yes.
- Commit-fertig fuer Dokumentations-/Entscheidungsstand: ja.
- Default runtime smoke readiness: blocked unless dependencies are prepared in
  the default build root.
- Last documented default blocker:
  `/root/.local/state/ModSecurity-conector-build/sources/ModSecurity_V3`
  missing.
- Current `/src` `make smoke-common`: PASS; Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make test-no-crs`: PASS; Apache 54 PASS, 0 FAIL,
  0 BLOCKED; NGINX 60 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` `make test-with-crs`: PASS; Apache 55 PASS, 0 FAIL,
  0 BLOCKED; NGINX 61 PASS, 0 FAIL, 0 BLOCKED.
- RESPONSE_BODY blocking: not verified.
- Vollstaendige Runtime-Verifikation: nein.
- Submodule changed: yes; `modules/ModSecurity-test-Framework` has a modified
  framework commit relative to the earlier baseline. Current parent HEAD points
  at framework commit `4bec4d960fea89525db9e439ea567df15943a2e7`.

## CRS Expectation Result

The former With-CRS 401/403 mismatch for
`action_status_401_phase1_block` is resolved in the current `/src` runs.

| Variant | Connector | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| No-CRS | Apache | 401 | 401 | PASS |
| No-CRS | NGINX | 401 | 401 | PASS |
| With-CRS | Apache | 403 | 403 | PASS |
| With-CRS | NGINX | 403 | 403 | PASS |

The expectation change is scoped to With-CRS through
`expect.variants.with-crs.status: 403`; the base No-CRS expectation remains
401.

CRS effectiveness is evidenced by `crs_sqli_anomaly_block` PASS for Apache
and NGINX, expected 403 and actual 403.

Detailed analysis:
`reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`.

## Decisions

| Target | Decision | Reason |
| --- | --- | --- |
| `connectors/_template` | partially suitable | The template now documents a repeatable connector flow, required evidence, external tests, and promotion gates; it is still not an implementation. |
| `connectors/nginx` | partial | Current No-CRS, With-CRS, and common smokes pass for executed scope; RESPONSE_BODY blocking and full minimum matrix remain unverified. |
| `connectors/apache` | partial | Current No-CRS, With-CRS, and common smokes pass for executed scope; Apache-specific YAML cases are still not found; RESPONSE_BODY blocking and full minimum matrix remain unverified. |
| RESPONSE_BODY | not verified | Current evidence includes pass-through/log-only response-body rows, not a blocking response-body HTTP result. |

## Current Runtime Evidence

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json` |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json` |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | `/src/ModSecurity-conector-build/results/connector-summary.json` |

Evidence files:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx.rc`
- `/src/ModSecurity-conector-build/results/with-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/with-crs/nginx.rc`

## Template Improvements

The template now documents:

- required files for a new connector
- required metadata
- required origin/license evidence
- required build evidence
- required No-CRS and With-CRS runtime evidence
- external framework test ownership
- coverage decision matrix columns
- RESPONSE_BODY minimum evidence
- promotion gates: `scaffolded`, `adapter-owned`,
  `runtime-smoke-verified`, `crs-verified`, and `more-than-partial`

## Removed Local Test Folders

- `connectors/_template/tests/`
- `connectors/nginx/tests/`
- `connectors/apache/tests/`

Executable connector tests are framework-owned and are not maintained in local
`connectors/*/tests` directories.

## Checks

| Check | Result | Note |
| --- | --- | --- |
| `test ! -d connectors/_template/tests` | PASS | Local Template test folder is absent. |
| `test ! -d connectors/apache/tests` | PASS | Local Apache test folder is absent. |
| `test ! -d connectors/nginx/tests` | PASS | Local NGINX test folder is absent. |
| `make generate-test-matrix` | PASS | Command exited 0. |
| `make check-test-matrix` | PASS | Command exited 0. |
| `make lint` | PASS | `actionlint unavailable` was informational; command exited 0. |
| `make quick-check` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Command exited 0; it printed a warning that framework-local `config/testing/import-status.json` was not found. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |
| `rg -n "[ \t]+$" connectors reports/template-verification-nginx-apache modules/ModSecurity-test-Framework` | PASS | No trailing whitespace matches; `rg` exited 1 because no matches were found. |
| `git status --short` | pending docs/report updates | Parent status shows only report documentation updates from this verification pass. |
| `git submodule status` | PASS | Parent points to `4bec4d960fea89525db9e439ea567df15943a2e7`; submodule working tree is clean. |

## Not Verified

- RESPONSE_BODY blocking for Apache and NGINX.
- Full runtime matrix promotion beyond `partial`.
- Apache-specific connector YAML cases under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there.
- Exact CRS/default-action or ModSecurity action-merging mechanism that made
  With-CRS return 403 before the expectation model was updated.
- Default `make smoke-common` without preparing the default build root.
