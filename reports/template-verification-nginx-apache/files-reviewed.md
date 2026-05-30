# Files Reviewed

## Root and CI

- `README.md`
- `Makefile`
- `TEST-COVERAGE-SUMMARY.md`
- `ci/README.md`
- `ci/check-common-helpers.sh`
- `ci/check-adapter-helpers.sh`
- `ci/check-adapter-metadata-drift.sh`

## Template

- `connectors/_template/README.md`
- `connectors/_template/TODO.md`
- `connectors/_template/docs/architecture.md`
- `connectors/_template/docs/build.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `connectors/_template/docs/validation.md`
- `connectors/_template/harness/README.md`
- `connectors/_template/src/README.md`
- `connectors/_template/tests/` (confirmed absent)

## NGINX

- `connectors/nginx/README.md`
- `connectors/nginx/TODO.md`
- `connectors/nginx/ORIGIN.md`
- `connectors/nginx/SOURCE_MAP.json`
- `connectors/nginx/config`
- `connectors/nginx/metadata.c`
- `connectors/nginx/metadata.h`
- `connectors/nginx/docs/architecture.md`
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/coverage-decision-matrix.md`
- `connectors/nginx/docs/public-sources.md`
- `connectors/nginx/docs/validation.md`
- `connectors/nginx/harness/README.md`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `connectors/nginx/harness/nginx_smoke.conf`
- `connectors/nginx/src/`
- `connectors/nginx/tests/` (confirmed absent)

## Apache

- `connectors/apache/README.md`
- `connectors/apache/TODO.md`
- `connectors/apache/ORIGIN.md`
- `connectors/apache/SOURCE_MAP.json`
- `connectors/apache/Makefile.am`
- `connectors/apache/autogen.sh`
- `connectors/apache/configure.ac`
- `connectors/apache/metadata.c`
- `connectors/apache/metadata.h`
- `connectors/apache/build/apxs-wrapper.in`
- `connectors/apache/docs/architecture.md`
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/coverage-decision-matrix.md`
- `connectors/apache/docs/public-sources.md`
- `connectors/apache/docs/validation.md`
- `connectors/apache/harness/README.md`
- `connectors/apache/harness/run_apache_smoke.sh`
- `connectors/apache/harness/apache_smoke.conf`
- `connectors/apache/src/`
- `connectors/apache/tests/` (confirmed absent)

## Similar Connectors

- `connectors/haproxy/`
- `connectors/envoy/`
- `connectors/traefik/`
- `connectors/lighttpd/`

## Framework Paths

- `modules/ModSecurity-test-Framework/README.md`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `modules/ModSecurity-test-Framework/ci/fetch-crs.sh`
- `modules/ModSecurity-test-Framework/ci/prepare-crs.sh`
- `modules/ModSecurity-test-Framework/ci/run-nginx-smoke.sh`
- `modules/ModSecurity-test-Framework/ci/run-apache-smoke.sh`
- `modules/ModSecurity-test-Framework/ci/run-connector-smokes.sh`
- `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh`
- `modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py`
- `modules/ModSecurity-test-Framework/tests/README.md`
- `modules/ModSecurity-test-Framework/tests/runners/README.md`
- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/README.md`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/README.md`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/*.yaml`
- `modules/ModSecurity-test-Framework/tests/cases/security/crs/crs_sqli_anomaly_block.yaml`
- `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`
- `modules/ModSecurity-test-Framework/tests/cases/response/body/response_body_basic_block.yaml`
- `modules/ModSecurity-test-Framework/tests/cases/response/body/response_body_pass.yaml`
- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py`

## Runtime Evidence

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
- `/src/ModSecurity-conector-build/results/no-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/nginx.rc`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/apache.rc`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/nginx.rc`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.txt`
- `/src/coreruleset`
- `/src/coreruleset/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf`
- `/src/coreruleset/rules/REQUEST-949-BLOCKING-EVALUATION.conf`
- `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`
- `/src/ModSecurity-conector-build/crs/crs-setup.conf`
- `/src/ModSecurity-conector-build/apache-runtime/action_status_401_phase1_block/conf/modsecurity-smoke.conf`
- `/src/ModSecurity-conector-build/apache-runtime/action_status_401_phase1_block/logs/error.log`
- `/src/ModSecurity-conector-build/logs/apache-runtime/action_status_401_phase1_block/result.json`
- `/src/ModSecurity-conector-build/logs/apache-runtime/action_status_401_phase1_block/status.txt`
- `/src/ModSecurity-conector-build/logs/apache-runtime/action_status_401_phase1_block/case-assert.log`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/runtime/action_status_401_phase1_block/conf/modsecurity-smoke.conf`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/logs/action_status_401_phase1_block/error.log`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/logs/action_status_401_phase1_block/result.json`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/logs/action_status_401_phase1_block/status.txt`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/logs/action_status_401_phase1_block/case-assert.log`
- `/src/ModSecurity-conector-build/logs/nginx/`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/logs/`

## Reports

- `reports/template-verification-nginx-apache/README.md`
- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `reports/template-verification-nginx-apache/template-evaluation.md`
- `reports/template-verification-nginx-apache/nginx-evaluation.md`
- `reports/template-verification-nginx-apache/apache-evaluation.md`
- `reports/template-verification-nginx-apache/component-download-check.md`
- `reports/template-verification-nginx-apache/runtime-test-run-src.md`
- `reports/template-verification-nginx-apache/verified-runtime-run.md`
- `reports/template-verification-nginx-apache/nginx-build-fail-analysis.md`
- `reports/template-verification-nginx-apache/nginx-docroot-permission-analysis.md`
- `reports/template-verification-nginx-apache/nginx-blocked-runtime-cases.md`
- `reports/template-verification-nginx-apache/crs-action-status-401-analysis.md`
- `reports/template-verification-nginx-apache/summary.md`
- `reports/template-verification-nginx-apache/findings.md`
- `reports/template-verification-nginx-apache/files-reviewed.md`
- `reports/template-verification-nginx-apache/open-questions.md`
