# Findings

All findings below are based on files, paths, commands, or local `/src`
runtime results reviewed in this repository.

## Repository And Framework State

- Parent repository path: `/root/git/ModSecurity-conector`.
- Framework submodule path: `modules/ModSecurity-test-Framework`.
- Framework submodule base commit:
  `b7f9bdc9831f9a8d14294cfb8fcb129a183d5d18`.
- Framework submodule working tree is modified for the CRS expectation work.
- No Apache or NGINX adapter source files were changed for this task.

## CRS Expectation Change

- Testcase path:
  `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`.
- Base expectation remains No-CRS: expected 401.
- With-CRS expectation is now variant-specific:
  `expect.variants.with-crs.status: 403`.
- Framework runner paths updated to resolve variant expectations:
  `modules/ModSecurity-test-Framework/tests/runners/runner_core.py` and
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- Framework docs updated:
  `modules/ModSecurity-test-Framework/tests/README.md` and
  `modules/ModSecurity-test-Framework/tests/runners/README.md`.

## Current Runtime Results

| Command | Result | Evidence |
| --- | --- | --- |
| `make generate-test-matrix` | PASS | Generator exited 0; generated reporting is not runtime proof. |
| `make check-test-matrix` | PASS | Matrix check exited 0. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS; NGINX 61 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |

Evidence files:

- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/nginx-summary.txt`

## Action Status 401 Case

- No-CRS Apache: `action_status_401_phase1_block` PASS, expected 401, actual
  401.
- No-CRS NGINX: `action_status_401_phase1_block` PASS, expected 401, actual
  401.
- With-CRS Apache: `action_status_401_phase1_block` PASS, expected 403, actual
  403.
- With-CRS NGINX: `action_status_401_phase1_block` PASS, expected 403, actual
  403.

Detailed report:
`reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`.

## CRS Evidence

- Framework `ci/common.sh` pins CRS to `CRS_GIT_REF=v4.26.0`.
- Current With-CRS run observed CRS source at `/src/coreruleset`.
- Current With-CRS run observed CRS preamble at
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml`
  exists.
- `crs_sqli_anomaly_block` PASS for Apache and NGINX in the current With-CRS
  run, expected 403 and actual 403.

## Template

- `connectors/_template/README.md` now documents a repeatable connector flow,
  required evidence, No-CRS/With-CRS validation, coverage matrix, promotion
  gates, and claims that must not be made.
- `connectors/_template/TODO.md` is organized into phases 0 through 7.
- `connectors/_template/docs/coverage-decision-matrix.md` separates framework
  cases, No-CRS status, With-CRS status, evidence path, and decision.
- `connectors/_template/tests` is absent. Executable Template tests are not
  maintained connector-locally.

## External Tests

- Framework testcases are under `modules/ModSecurity-test-Framework/tests/cases/`.
- Connector-specific framework paths are under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`.
- NGINX-specific YAML files exist under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- Apache-specific YAML files were not found under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there.
- New connector scaffolds must not create local `connectors/<name>/tests`
  directories.

## NGINX

- `connectors/nginx/` is present and adapter-owned.
- `connectors/nginx/tests` is absent.
- Current `/src` NGINX common smoke passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` NGINX No-CRS target passed: 60 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` NGINX With-CRS target passed: 61 PASS, 0 FAIL, 0 BLOCKED.
- `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include` remains the accepted
  NGINX build include contract.
- RESPONSE_BODY blocking remains not verified for NGINX. Current response-body
  rows are pass-through or log-only evidence.

## Apache

- `connectors/apache/` is present and adapter-owned.
- `connectors/apache/tests` is absent.
- Current `/src` Apache common smoke passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` Apache No-CRS target passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` Apache With-CRS target passed: 55 PASS, 0 FAIL, 0 BLOCKED.
- Apache-specific framework YAML files were not found.
- RESPONSE_BODY blocking remains not verified for Apache. `response_body_pass`
  is pass-through evidence only.

## Decisions

- `connectors/_template`: partially suitable as a repeatable scaffold, not an
  implementation.
- `connectors/apache`: partial.
- `connectors/nginx`: partial.
- No-CRS runtime evidence: PASS for both connectors in current `/src` run.
- With-CRS runtime evidence: PASS for both connectors in current `/src` run.
- CRS SQLi anomaly case: PASS for both connectors.
- RESPONSE_BODY blocking: not verified.
- Full runtime verification: no.
