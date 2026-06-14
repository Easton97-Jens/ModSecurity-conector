# Files Reviewed

## Root and CI

- `README.md`
- `Makefile`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
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
- `modules/ModSecurity-test-Framework/Makefile`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `modules/ModSecurity-test-Framework/ci/fetch-crs.sh`
- `modules/ModSecurity-test-Framework/ci/prepare-crs.sh`
- `modules/ModSecurity-test-Framework/ci/run-nginx-smoke.sh`
- `modules/ModSecurity-test-Framework/ci/run-apache-smoke.sh`
- `modules/ModSecurity-test-Framework/ci/run-haproxy-runtime-matrix.sh`
- `modules/ModSecurity-test-Framework/ci/write-haproxy-runtime-matrix.py`
- `modules/ModSecurity-test-Framework/ci/update-runtime-snapshot.py`
- `modules/ModSecurity-test-Framework/ci/generate-case-matrix.py`
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
- `reports/template-verification-nginx-apache/apache-template-alignment.md`
- `reports/template-verification-nginx-apache/nginx-template-alignment.md`
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

## Envoy Scaffold Files

- `connectors/envoy/README.md`
- `connectors/envoy/TODO.md`
- `connectors/envoy/docs/architecture.md`
- `connectors/envoy/docs/build.md`
- `connectors/envoy/docs/validation.md`
- `connectors/envoy/docs/coverage-decision-matrix.md`
- `connectors/envoy/docs/public-sources.md`
- `connectors/envoy/harness/README.md`
- `connectors/envoy/harness/run_envoy_smoke.sh`
- `connectors/envoy/src/README.md`
- `reports/template-verification-nginx-apache/envoy-template-alignment.md`

## Envoy Build-Starter Files

- `connectors/envoy/Makefile`
- `connectors/envoy/ORIGIN.md`
- `connectors/envoy/SOURCE_MAP.json`
- `connectors/envoy/metadata.c`
- `connectors/envoy/metadata.h`
- `connectors/envoy/build/build_metadata.sh`

## Envoy Bridge-Starter Files

- `connectors/envoy/src/envoy_bridge.c`
- `connectors/envoy/src/envoy_bridge.h`
- `connectors/envoy/src/envoy_bridge_main.c`
## HAProxy Scaffold

- `connectors/haproxy/README.md`
- `connectors/haproxy/TODO.md`
- `connectors/haproxy/docs/architecture.md`
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
- `connectors/haproxy/docs/coverage-decision-matrix.md`
- `connectors/haproxy/harness/README.md`
- `connectors/haproxy/harness/run_haproxy_smoke.sh`
- `/src/ModSecurity-conector-build/results/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/haproxy-results.jsonl`
- `/src/ModSecurity-conector-build/results/haproxy-summary.txt`
- `/src/ModSecurity-conector-build/results/no-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/haproxy-results.jsonl`
- `/src/ModSecurity-conector-build/results/no-crs/haproxy-summary.txt`
- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/haproxy-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.txt`
- `/src/ModSecurity-conector-build/results/haproxy-smoke-summary.json`
- `/src/ModSecurity-conector-build/results/haproxy-smoke-results.jsonl`
- `/src/ModSecurity-conector-build/logs/haproxy/<run-id>/diagnostic-agent.log`
- `/src/ModSecurity-conector-build/logs/haproxy/<run-id>/haproxy-runtime.stderr.log`
- `/src/ModSecurity-conector-build/logs/haproxy/<run-id>/backend.stderr.log`
- `/src/ModSecurity-conector-build/logs/haproxy/<run-id>/with-crs/diagnostic-agent.log`
- `/src/ModSecurity-conector-build/logs/haproxy/<run-id>/with-crs/haproxy-runtime.stderr.log`
- `/src/ModSecurity-conector-build/logs/haproxy/<run-id>/with-crs/http-probe.log`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime-smoke/modsecurity-binding-build.log`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime-smoke/modsecurity-binding-self-test.log`
- `/src/ModSecurity-conector-build/logs/haproxy-runtime-smoke/modsecurity-binding-crs-self-test.log`
- `/src/ModSecurity-conector-build/haproxy-runtime/spoe/<run-id>/haproxy.cfg`
- `/src/ModSecurity-conector-build/haproxy-runtime/spoe/<run-id>/spoe-agent.conf`
- `/src/ModSecurity-conector-build/haproxy-runtime/spoe/<run-id>/with-crs/haproxy.cfg`
- `/src/ModSecurity-conector-build/haproxy-runtime/spoe/<run-id>/with-crs/spoe-agent.conf`
- `/src/ModSecurity-conector-build/haproxy-modsecurity-binding/haproxy-modsecurity-binding-self-test`
- `connectors/haproxy/src/README.md`
- `reports/template-verification-nginx-apache/haproxy-template-alignment.md`

## HAProxy Build-Starter Files

- `connectors/haproxy/Makefile`
- `connectors/haproxy/ORIGIN.md`
- `connectors/haproxy/SOURCE_MAP.json`
- `connectors/haproxy/metadata.c`
- `connectors/haproxy/metadata.h`
- `common/include/msconnector/origin.h`

## HAProxy SPOA Agent Starter Files

- `connectors/haproxy/src/haproxy_spoa_agent_starter.c`
- `connectors/haproxy/src/haproxy_spoa_agent_starter.h`
- `connectors/haproxy/src/haproxy_spoa_main.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.h`
- `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`
- `common/src/intervention.c`
## lighttpd Bridge-Starter Files

- `connectors/lighttpd/ORIGIN.md`
- `connectors/lighttpd/SOURCE_MAP.json`
- `connectors/lighttpd/metadata.c`
- `connectors/lighttpd/metadata.h`
- `connectors/lighttpd/build/build_starter.sh`
- `connectors/lighttpd/src/lighttpd_bridge_main.c`
- `connectors/lighttpd/src/lighttpd_bridge.c`
- `connectors/lighttpd/src/lighttpd_bridge.h`
- `connectors/lighttpd/build/bridge_starter.sh`
- `connectors/lighttpd/Makefile`
- `connectors/lighttpd/src/lighttpd_build_starter.c`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/TODO.md`
- `connectors/lighttpd/docs/architecture.md`
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
- `connectors/lighttpd/docs/coverage-decision-matrix.md`
- `connectors/lighttpd/docs/public-sources.md`
- `connectors/lighttpd/harness/README.md`
- `connectors/lighttpd/harness/run_lighttpd_smoke.sh`
- `connectors/lighttpd/src/README.md`
- `reports/template-verification-nginx-apache/lighttpd-template-alignment.md`

These files were reviewed/updated as bridge-starter documentation and repo-owned
metadata/probe/bridge code only. No local `connectors/lighttpd/tests` folder exists.
## Traefik Decision-Service Starter Files

- `connectors/traefik/README.md`
- `connectors/traefik/ORIGIN.md`
- `connectors/traefik/SOURCE_MAP.json`
- `connectors/traefik/metadata.c`
- `connectors/traefik/metadata.h`
- `connectors/traefik/build/build-starter.sh`
- `connectors/traefik/Makefile`
- `connectors/traefik/src/traefik_decision_service.h`
- `connectors/traefik/src/traefik_decision_service.c`
- `connectors/traefik/src/traefik_decision_service_main.c`
- `connectors/traefik/TODO.md`
- `connectors/traefik/docs/architecture.md`
- `connectors/traefik/docs/build.md`
- `connectors/traefik/docs/validation.md`
- `connectors/traefik/docs/coverage-decision-matrix.md`
- `connectors/traefik/docs/public-sources.md`
- `connectors/traefik/harness/README.md`
- `connectors/traefik/harness/run_traefik_smoke.sh`
- `connectors/traefik/src/README.md`
- `reports/template-verification-nginx-apache/traefik-template-alignment.md`

Shared files used by the Traefik decision-service starter documentation:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

## Connector-Starter Framework Files

- `Makefile`
- `modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`
- `connectors/envoy/docs/validation.md`
- `connectors/haproxy/docs/validation.md`
- `connectors/lighttpd/docs/validation.md`
- `connectors/traefik/docs/validation.md`
- `/src/ModSecurity-conector-build/results/connector-starters/summary.json`
- `/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`

The result files are local evidence artifacts and are not committed.

## New Connector Runtime-Smoke Files

- `Makefile`
- `connectors/envoy/harness/run_envoy_smoke.sh`
- `connectors/haproxy/harness/run_haproxy_smoke.sh`
- `connectors/lighttpd/harness/run_lighttpd_smoke.sh`
- `connectors/traefik/harness/run_traefik_smoke.sh`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `modules/ModSecurity-test-Framework/ci/connector-smoke-common.sh`
- `modules/ModSecurity-test-Framework/ci/prepare-haproxy-runtime.sh`
- `modules/ModSecurity-test-Framework/ci/run-envoy-smoke.sh`
- `modules/ModSecurity-test-Framework/ci/run-haproxy-smoke.sh`
- `modules/ModSecurity-test-Framework/ci/run-lighttpd-smoke.sh`
- `modules/ModSecurity-test-Framework/ci/run-traefik-smoke.sh`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py`
- `/src/ModSecurity-conector-build/results/envoy-summary.json`
- `/src/ModSecurity-conector-build/results/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/lighttpd-summary.json`
- `/src/ModSecurity-conector-build/results/traefik-summary.json`
