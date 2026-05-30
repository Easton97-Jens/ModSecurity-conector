# Findings

All findings below are based on files, paths, or commands reviewed in this
repository and the local `/src/ModSecurity-conector-build` result tree.

## Repository And Framework State

- Parent repository path: `/root/git/ModSecurity-conector`.
- Parent commit captured before documentation edits:
  `e795c9b feat(apache): add modsecurity_use_error_log directive`.
- Framework submodule commit:
  `b7f9bdc9831f9a8d14294cfb8fcb129a183d5d18`.
- Parent and submodule working trees were clean before these documentation
  updates.

## New Test Targets

- `Makefile` defines `test-no-crs`.
- `Makefile` defines `test-with-crs`.
- `test-no-crs` sets `MODSECURITY_TEST_VARIANT=no-crs`,
  clears `MODSECURITY_RULE_PREAMBLE_FILE`, sets
  `RESULTS_DIR=$BUILD_ROOT/results/no-crs`, and runs framework
  `ci/run-connector-smokes.sh` with `CASE_SCOPE=all`.
- `test-with-crs` sets `MODSECURITY_TEST_VARIANT=with-crs`, runs framework
  `ci/fetch-crs.sh` and `ci/prepare-crs.sh`, sets
  `MODSECURITY_RULE_PREAMBLE_FILE=$CRS_RUNTIME_DIR/modsecurity-crs-preamble.conf`,
  sets `RESULTS_DIR=$BUILD_ROOT/results/with-crs`, and runs framework
  `ci/run-connector-smokes.sh` with `CASE_SCOPE=all`.
- Framework `README.md` states that `no-crs` loads local YAML-case rules only,
  while `with-crs` loads OWASP CRS before local YAML-case rules.

## CRS Evidence

- Framework `ci/common.sh` pins CRS to `CRS_GIT_REF=v4.26.0`.
- Framework `ci/common.sh` defines default `CRS_SOURCE_DIR=$SOURCE_ROOT/coreruleset`.
- Framework `ci/common.sh` defines default `CRS_RUNTIME_DIR=$BUILD_ROOT/crs`.
- Current With-CRS run observed CRS source at `/src/coreruleset`.
- Current With-CRS run observed CRS preamble at
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml`
  exists.
- `crs_sqli_anomaly_block` PASS for Apache and NGINX in the current With-CRS
  run, expected 403 and actual 403.

## Template

- `connectors/_template/README.md` defines a generic connector template and is
  not a productive connector implementation.
- `connectors/_template/TODO.md` uses checkbox-style status labels.
- `connectors/_template/docs/coverage-decision-matrix.md` documents the
  generic matrix and runtime-promotion rules.
- `connectors/_template/tests` is absent. Executable Template tests are not
  maintained connector-locally.

## External Tests

- Framework testcases are under `modules/ModSecurity-test-Framework/tests/cases/`.
- Connector-specific framework paths are under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`.
- NGINX-specific YAML files exist under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- The NGINX-specific path contains seven YAML files, including
  `nginx_phase4_strict_connection_abort.yaml`.
- `nginx_phase4_strict_connection_abort.yaml` exists but was not present in the
  current No-CRS or With-CRS summary JSON files.
- Apache-specific YAML files were not found under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there.
- New connector scaffolds must not create local `connectors/<name>/tests`
  directories.

## Current Runtime Results

| Command | Result | Evidence |
| --- | --- | --- |
| `make generate-test-matrix` | PASS | Generator exited 0; generated reporting is not runtime proof. |
| `make check-test-matrix` | PASS | Matrix check exited 0. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-apache` | PASS | Apache smoke completed before later result refreshes. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS; NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | FAIL | Apache 54 PASS / 1 FAIL; NGINX 60 PASS / 1 FAIL. |

Current With-CRS failing case for both connectors:

- `action_status_401_phase1_block`
- Expected status: 401.
- Actual status: 403.
- Path:
  `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`.

## NGINX

- `connectors/nginx/` is present and adapter-owned.
- `connectors/nginx/src/`, `connectors/nginx/config`,
  `connectors/nginx/metadata.c`, and `connectors/nginx/ORIGIN.md` are present.
- `connectors/nginx/tests` is absent.
- `common/include/msconnector/rule_load_stats.h` exists.
- The NGINX build contract uses
  `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`.
- The current parent runtime contract uses
  `NGINX_HARNESS_PARENT=$(BUILD_ROOT)`.
- Current `/src` NGINX all-scope smoke passed: 60 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` NGINX No-CRS target passed: 60 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` NGINX With-CRS target failed: 60 PASS, 1 FAIL, 0 BLOCKED.
- The historical 11 NGINX BLOCKED rows are documented in
  `nginx-blocked-runtime-cases.md` and classified as an environment/docroot
  permission blocker.
- RESPONSE_BODY blocking remains not verified for NGINX. Current response-body
  rows are pass-through or log-only evidence.

## Apache

- `connectors/apache/` is present and adapter-owned.
- `connectors/apache/src/`, `connectors/apache/Makefile.am`,
  `connectors/apache/configure.ac`, `connectors/apache/metadata.c`, and
  `connectors/apache/ORIGIN.md` are present.
- `connectors/apache/tests` is absent.
- `connectors/apache/build/apxs-wrapper.in` contains a common include fallback
  based on `CONNECTOR_ROOT`.
- Current `/src` Apache common smoke passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` Apache No-CRS target passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` Apache With-CRS target failed: 54 PASS, 1 FAIL, 0 BLOCKED.
- RESPONSE_BODY blocking remains not verified for Apache. `response_body_pass`
  is pass-through evidence only.

## Similar Connectors

- `connectors/haproxy/README.md` identifies HAProxy as scaffolded and not
  implemented.
- `connectors/envoy/README.md` identifies Envoy as scaffolded and not
  implemented.
- `connectors/traefik/README.md` identifies Traefik as scaffolded and not
  implemented.
- `connectors/lighttpd/README.md` identifies Lighttpd as scaffolded and not
  implemented.

## Decisions

- `connectors/_template`: partially suitable.
- `connectors/apache`: partial.
- `connectors/nginx`: partial.
- No-CRS runtime evidence: PASS for both connectors in current `/src` run.
- With-CRS runtime evidence: FAIL for both connectors in current `/src` run.
- CRS SQLi anomaly case: PASS for both connectors.
- RESPONSE_BODY blocking: not verified.
- Full runtime verification: no.
