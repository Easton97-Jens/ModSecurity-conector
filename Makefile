PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
MSCONNECTOR_C_STD ?= c17
MSCONNECTOR_CFLAGS ?= -std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror
MSCONNECTOR_COMPILER_ID ?= $(notdir $(firstword $(CC)))
FRAMEWORK_PYTHON := $(if $(findstring /,$(PYTHON)),$(abspath $(PYTHON)),$(PYTHON))
VERIFIED_RUN_PARENT ?= $(if $(RUNNER_TEMP),$(RUNNER_TEMP),$(if $(TMPDIR),$(TMPDIR),/var/tmp))
VERIFIED_RUN_ROOT ?= $(VERIFIED_RUN_PARENT)/ModSecurity-conector-verified
VERIFIED_STATE_ROOT ?= $(VERIFIED_RUN_ROOT)/state
VERIFIED_BUILD_ROOT ?= $(VERIFIED_RUN_ROOT)/build
VERIFIED_SOURCE_ROOT ?= $(VERIFIED_RUN_ROOT)/src
VERIFIED_TMP_ROOT ?= $(VERIFIED_RUN_ROOT)/tmp
VERIFIED_LOG_ROOT ?= $(VERIFIED_RUN_ROOT)/logs
VERIFIED_COMPONENT_CACHE ?= $(VERIFIED_RUN_ROOT)/component-cache
STATE_HOME ?= $(VERIFIED_STATE_ROOT)
SOURCE_ROOT ?= $(VERIFIED_SOURCE_ROOT)
BUILD_ROOT ?= $(VERIFIED_BUILD_ROOT)
TMP_ROOT ?= $(VERIFIED_TMP_ROOT)
LOG_ROOT ?= $(VERIFIED_LOG_ROOT)
MATRIX_ROOT ?= $(BUILD_ROOT)/full-matrix
FRAMEWORK_ROOT ?= $(CURDIR)/modules/ModSecurity-test-Framework
CONNECTOR_ROOT := $(CURDIR)
REQUESTED_VERIFIED_RUN_ID := $(VERIFIED_RUN_ID)
DEFAULT_VERIFIED_RUN_ID := $(shell date -u +%Y-%m-%dT%H-%M-%SZ)-$(shell git rev-parse --short=8 HEAD 2>/dev/null || printf unknown)
EXISTING_VERIFIED_RUN_ID := $(shell "$(PYTHON)" -c 'import json,pathlib; p=pathlib.Path("reports/testing/generated/manifest/verified-run-manifest.generated.json"); d=json.loads(p.read_text()) if p.is_file() else {}; print(d.get("verified_run_id") or d.get("metadata", {}).get("verified_run_id") or "")' 2>/dev/null)
VERIFIED_RUN_ID := $(if $(REQUESTED_VERIFIED_RUN_ID),$(REQUESTED_VERIFIED_RUN_ID),$(if $(EXISTING_VERIFIED_RUN_ID),$(EXISTING_VERIFIED_RUN_ID),$(DEFAULT_VERIFIED_RUN_ID)))
FRESH_VERIFIED_RUN_ID := $(if $(REQUESTED_VERIFIED_RUN_ID),$(REQUESTED_VERIFIED_RUN_ID),$(DEFAULT_VERIFIED_RUN_ID))
CONNECTOR_COMPONENT_CACHE ?= $(VERIFIED_COMPONENT_CACHE)
NGINX_HARNESS_PARENT ?= $(VERIFIED_RUN_ROOT)/nginx-harness
MRTS_BUILD_ROOT ?= $(BUILD_ROOT)/mrts
MRTS_NATIVE_ROOT ?= $(BUILD_ROOT)/mrts-native
MRTS_NATIVE_TARGETS ?= apache2_ubuntu nginx-pr24
MRTS_NATIVE_APACHE_PORT ?= 19080
MRTS_NATIVE_NGINX_PORT ?= 19081
MRTS_NATIVE_BACKEND_PORT ?= 19082
GO_FTW_BIN ?= go-ftw
ALBEDO_BIN ?= albedo
VERIFIED_RUN_RUNTIME_MATRIX_TIMEOUT_SECONDS ?= 1800
VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS ?= $(if $(filter undefined,$(origin VERIFIED_RUN_FULL_MATRIX_TIMEOUT_SECONDS)),7200,$(VERIFIED_RUN_FULL_MATRIX_TIMEOUT_SECONDS))
VERIFIED_RUN_REPORT_REFRESH_TIMEOUT_SECONDS ?= 1800
VERIFIED_RUN_NATIVE_MRTS_TIMEOUT_SECONDS ?= 1800
VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS ?= 3600
VERIFIED_RUN_JOB_FINALIZE_GRACE_SECONDS ?= 60
VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS ?= 14400
SKIP_RUNTIME_COMPONENT_PREPARE ?= 0
RUNTIME_COMPONENT_STRICT_VERIFY ?= 0
KEEP_RUNTIME_ARTIFACTS ?= 0
PYTHONDONTWRITEBYTECODE ?= 1
WITH_RUNTIME_COMPONENTS = SKIP_RUNTIME_COMPONENT_PREPARE=1 sh ci/with-runtime-components.sh

export BUILD_ROOT
export SOURCE_ROOT
export TMP_ROOT
export LOG_ROOT
export MATRIX_ROOT
export VERIFIED_RUN_ROOT
export VERIFIED_STATE_ROOT
export VERIFIED_BUILD_ROOT
export VERIFIED_SOURCE_ROOT
export VERIFIED_TMP_ROOT
export VERIFIED_LOG_ROOT
export VERIFIED_COMPONENT_CACHE
export VERIFIED_RUN_ID
export VERIFIED_RUN_RUNTIME_MATRIX_TIMEOUT_SECONDS
export VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS
export VERIFIED_RUN_REPORT_REFRESH_TIMEOUT_SECONDS
export VERIFIED_RUN_NATIVE_MRTS_TIMEOUT_SECONDS
export VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS
export VERIFIED_RUN_JOB_FINALIZE_GRACE_SECONDS
export VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS
export RESULTS_DIR
export FRAMEWORK_ROOT
export CONNECTOR_ROOT
export NGINX_HARNESS_PARENT
export PYTHON
export PYTHONDONTWRITEBYTECODE
export DEFAULT_BRANCH
export REFRESH
export SMOKE_CASES
export CASE_SCOPE
export FORCE_ALL_CASES
export MODSECURITY_REPO_URL
export MODSECURITY_GIT_REF
export MODSECURITY_APACHE_REPO_URL
export MODSECURITY_NGINX_REPO_URL
export ALLOW_EXTERNAL_CONNECTOR_REPOS
export MODSECURITY_SOURCE_DIR
export MODSECURITY_V3_SOURCE_DIR
export MODSECURITY_V3_ROOT
export MODSECURITY_APACHE_SOURCE_DIR
export MODSECURITY_NGINX_SOURCE_DIR
export MODSECURITY_V3_GIT_URL
export MODSECURITY_V3_GIT_REF
export MODSECURITY_APACHE_GIT_URL
export MODSECURITY_APACHE_GIT_REF
export MODSECURITY_NGINX_GIT_URL
export MODSECURITY_NGINX_GIT_REF
export MODSECURITY_TEST_VARIANT
export MODSECURITY_MRTS_VARIANT
export MODSECURITY_RULESET
export MODSECURITY_SMOKE_CASE
export CRS_SMOKE_CASE
export MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO
export MODSECURITY_MRTS_PREPARED
export EXTRA_CASE_ROOTS
export MRTS_ROOT
export MRTS_DEFINITIONS
export MRTS_RULES_OUT
export MRTS_FTW_OUT
export MRTS_LOAD_FILE
export MRTS_CASE_ROOT
export MRTS_BUILD_ROOT
export MRTS_NATIVE_ROOT
export MRTS_NATIVE_TARGETS
export MRTS_NATIVE_APACHE_PORT
export MRTS_NATIVE_NGINX_BIN
export MRTS_NATIVE_NGINX_MODULE_DIR
export MRTS_NATIVE_NGINX_PORT
export MRTS_NATIVE_BACKEND_PORT
export GO_FTW_BIN
export GO_FTW_SOURCE_URL
export GO_FTW_PROMPT_EXPECTED_LATEST
export GO_FTW_GIT_REF
export ALBEDO_BIN
export ALBEDO_SOURCE_URL
export ALBEDO_PROMPT_EXPECTED_LATEST
export ALBEDO_GIT_REF
export CRS_REPO_URL
export CRS_GIT_REF
export CRS_SOURCE_DIR
export CRS_RUNTIME_DIR
export MODSECURITY_RULE_PREAMBLE_FILE
export BUILD_HTTPD_FROM_SOURCE
export BUILD_PCRE2_FROM_SOURCE
export BUILD_NGINX_FROM_SOURCE
export NGINX_SOURCE_MODE
export NGINX_SOURCE_REPO_URL
export NGINX_SOURCE_GIT_REF
export NGINX_GITHUB_REPO
export NGINX_RELEASE_TAG
export HAPROXY_VERSION
export HAPROXY_SOURCE_URL
export HAPROXY_SHA256_URL
export HAPROXY_SHA256
export HAPROXY_SOURCE_ROOT
export HAPROXY_DOWNLOAD_DIR
export HAPROXY_SOURCE_DIR
export HAPROXY_RUNTIME_BUILD_DIR
export HAPROXY_RUNTIME_BUILD_WORKTREE
export HAPROXY_RUNTIME_DIR
export HAPROXY_BIN
export EXPAT_SOURCE_URL
export EXPAT_GIT_REF
export EXPAT_GIT_URL
export EXPAT_PROMPT_EXPECTED_LATEST
export HTTPD_VERSION
export HTTPD_SOURCE_URL
export HTTPD_SHA256
export HTTPD_SHA256_URL
export APR_VERSION
export APR_SOURCE_URL
export APR_SHA256
export APR_SHA256_URL
export APR_UTIL_VERSION
export APR_UTIL_SOURCE_URL
export APR_UTIL_SHA256
export APR_UTIL_SHA256_URL
export PCRE2_VERSION
export PCRE2_SOURCE_URL
export PCRE2_SHA256
export PCRE2_SHA256_URL
export APACHE_BIN
export APACHECTL_BIN
export APXS_BIN
export NGINX_BIN
export RESPONSE_BODY_PROBE_REPEAT
export RESPONSE_BODY_PROBE_ROOT
export RESPONSE_BODY_PROBE_CASE
export CONNECTOR_COMPONENT_CACHE
export SKIP_RUNTIME_COMPONENT_PREPARE
export RUNTIME_COMPONENT_STRICT_VERIFY
export KEEP_RUNTIME_ARTIFACTS
export DECISION_BACKEND
export ENVOY_DECISION_BACKEND
export TRAEFIK_DECISION_BACKEND
export LIGHTTPD_DECISION_BACKEND

.PHONY: check-framework prepare-runtime-components prepare-envoy-runtime prepare-traefik-runtime prepare-lighttpd-runtime prepare-lighttpd-runtime-build prepare-open-connector-runtimes runtime-components-inventory runtime-components-sources check-framework-fixture-syntax check-runtime-producer-readiness check-runtime-path-policy check-bilingual-docs refresh-connector-reports refresh-all-reports check-generated-report-layout report-governance verified-report-evidence-gate generate-system-environment-proof prove-generated-reports verified-runtime-producers verified-report-refresh verified-report-producers verified-report-consumers verified-report-checks verified-report-run verified-report-run-soft verified-report-run-smoke verified-full-matrix-job verified-case verified-native-case verified-apache-case verified-nginx-case verified-haproxy-case verified-full-matrix-resume full-matrix-single-job-runtime full-matrix-resume-runtime smoke-common smoke-apache smoke-nginx smoke-envoy smoke-envoy-modsecurity smoke-envoy-crs smoke-envoy-crs-secondary smoke-haproxy smoke-lighttpd smoke-lighttpd-modsecurity smoke-lighttpd-crs smoke-lighttpd-crs-secondary smoke-traefik smoke-traefik-modsecurity smoke-traefik-crs smoke-traefik-crs-secondary smoke-open-connectors-crs smoke-open-connectors-crs-secondary smoke-new-connectors smoke-all test test-no-crs test-with-crs test-haproxy-no-crs test-haproxy-with-crs runtime-matrix runtime-matrix-all runtime-matrix-all-runtime runtime-matrix-haproxy full-runtime-matrix full-mrts-runtime-matrix mrts-only-full-run full-matrix-parallel full-matrix-parallel-runtime generate-full-runtime-matrix generate-full-matrix-job-completeness generate-nginx-mrts-http500-cluster-analysis generate-work-queue generate-phase-work-queue generate-nolog-audit-evidence-analysis generate-response-header-hook-analysis generate-phase4-hard-abort-capability generate-intervention-blocking-analysis generate-no-mrts-intervention-nomatch-analysis generate-body-processor-analysis generate-rule-chain-semantics-analysis generate-final-consistency-audit generate-native-semantics-comparison generate-remaining-critical-batch-analysis generate-remaining-failure-analysis mrts-native-full-run mrts-native-full-run-runtime mrts-native-apache-full mrts-native-nginx-pr24-full mrts-upstream-infra-check probe-response-body connector-starter-checks lint summary case-matrix setup-dev install-dev-deps doctor doctor-quick env-check fetch-deps fetch-modsecurity-v3 fetch-crs prepare-crs bootstrap-runtime quick-check codex-check quick-all smoke-installed installed-readiness doctor-install-hints cloud-quick-check generate-test-matrix check-test-matrix mrts-generate mrts-load mrts-import test-no-mrts test-with-mrts-feature-demo test-mrts-matrix mrts-ftw
.PHONY: smoke-envoy-request-body smoke-traefik-request-body smoke-lighttpd-request-body smoke-open-connectors-request-body

define RUN_WITH_REFRESH_ALL
	@set +e; \
	$(1); \
	runtime_rc=$$?; \
	set -e; \
	refresh_rc=0; \
	$(MAKE) refresh-all-reports || refresh_rc=$$?; \
	if [ "$$runtime_rc" -ne 0 ]; then exit "$$runtime_rc"; fi; \
	exit "$$refresh_rc"
endef

check-framework:
	@test -d "$(FRAMEWORK_ROOT)" || { \
		echo "BLOCKED: FRAMEWORK_ROOT is missing: $(FRAMEWORK_ROOT)"; \
		echo "Hint: run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; \
		exit 77; \
	}

check-framework-fixture-syntax: check-framework
	"$(FRAMEWORK_PYTHON)" ci/check-framework-fixture-syntax.py --framework-root "$(FRAMEWORK_ROOT)"

prepare-runtime-components: check-framework
	@if [ "$(SKIP_RUNTIME_COMPONENT_PREPARE)" = "1" ]; then \
		echo "prepare-runtime-components: skipped (SKIP_RUNTIME_COMPONENT_PREPARE=1)"; \
	else \
		PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/prepare-runtime-components.sh; \
	fi

prepare-envoy-runtime: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/prepare-envoy-runtime.sh"

prepare-traefik-runtime: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/prepare-traefik-runtime.sh"

prepare-lighttpd-runtime: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/prepare-lighttpd-runtime.sh"

prepare-lighttpd-runtime-build: check-framework
	ALLOW_RUNTIME_BUILDS=1 $(MAKE) prepare-lighttpd-runtime

prepare-open-connector-runtimes: check-framework
	@rc=0; \
	for target in prepare-envoy-runtime prepare-traefik-runtime prepare-lighttpd-runtime; do \
		$(MAKE) $$target || rc=$$?; \
	done; \
	exit $$rc

runtime-components-inventory: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime-components-inventory.sh inventory

runtime-components-sources: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime-components-inventory.sh sources

check-runtime-producer-readiness: check-framework
	"$(FRAMEWORK_PYTHON)" ci/check-runtime-producer-readiness.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)"

check-runtime-path-policy: check-framework
	"$(FRAMEWORK_PYTHON)" ci/check-runtime-path-policy.py

check-bilingual-docs:
	$(PYTHON) ci/check-bilingual-docs.py

refresh-connector-reports: check-framework
	"$(FRAMEWORK_PYTHON)" ci/refresh-connector-reports.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --native-root "$(MRTS_NATIVE_ROOT)"

refresh-all-reports: check-framework
	@framework_rc=0; \
	$(MAKE) -C "$(FRAMEWORK_ROOT)" PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" OUTPUT_ROOT="$(FRAMEWORK_ROOT)" refresh-framework-reports || framework_rc=$$?; \
	connector_rc=0; \
	"$(FRAMEWORK_PYTHON)" ci/refresh-connector-reports.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --native-root "$(MRTS_NATIVE_ROOT)" --strict-inputs || connector_rc=$$?; \
	if [ "$$framework_rc" -ne 0 ]; then exit "$$framework_rc"; fi; \
	exit "$$connector_rc"

check-generated-report-layout: check-framework
	"$(FRAMEWORK_PYTHON)" ci/check-generated-report-layout.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

report-governance: check-framework
	$(MAKE) check-runtime-path-policy
	"$(FRAMEWORK_PYTHON)" ci/check-generated-report-layout.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --governance-only

verified-report-evidence-gate: check-generated-report-layout
	@echo "verified-report-evidence-gate: strict generated-report evidence gate passed"

generate-system-environment-proof: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-system-environment-proof.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-verified-runtime-mismatch-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-verified-runtime-mismatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-remaining-critical-batch-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-remaining-critical-batch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-native-semantics-comparison: check-framework
	"$(FRAMEWORK_PYTHON)" ci/run-native-case-comparison.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --verified-run-root "$(VERIFIED_RUN_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest" --report-only

prove-generated-reports:
	$(MAKE) refresh-connector-reports
	$(MAKE) check-generated-report-layout
	$(MAKE) lint
	$(MAKE) quick-check
	$(MAKE) generate-system-environment-proof

verified-runtime-producers: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase runtime-producers

verified-report-producers: verified-runtime-producers

verified-report-refresh: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase report-refresh

verified-report-consumers: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase report-refresh

verified-report-checks: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase checks

verified-report-run: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --mode strict

verified-report-run-soft: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --mode soft

verified-report-run-smoke: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --mode soft --profile smoke

verified-full-matrix-job: check-framework
	@test -n "$(CONNECTOR)" || { echo "CONNECTOR is required, e.g. CONNECTOR=nginx"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase full-matrix-job --connector "$(CONNECTOR)" --crs "$(CRS)" --mrts "$(MRTS)"

verified-case: check-framework
	@test -n "$(CONNECTOR)" || { echo "CONNECTOR is required, e.g. CONNECTOR=nginx"; exit 2; }
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	@explain_args=""; \
	case "$${EXPLAIN:-$(EXPLAIN)}$${VERIFIED_CASE_EXPLAIN:-$(VERIFIED_CASE_EXPLAIN)}" in ""|0|false|False) $(MAKE) prepare-runtime-components ;; *) explain_args="--explain" ;; esac; \
	"$(FRAMEWORK_PYTHON)" ci/run-verified-case.py --connector "$(CONNECTOR)" --case "$(CASE)" --crs "$(CRS)" --mrts "$(MRTS)" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --source-root "$(SOURCE_ROOT)" --tmp-root "$(TMP_ROOT)" --verified-run-root "$(VERIFIED_RUN_ROOT)" --python "$(FRAMEWORK_PYTHON)" $$explain_args

verified-native-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=unicode_whitespace_normalization_gap"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CONNECTOR_ROOT="$(CURDIR)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" BUILD_ROOT="$(BUILD_ROOT)" VERIFIED_RUN_ROOT="$(VERIFIED_RUN_ROOT)" "$(FRAMEWORK_PYTHON)" ci/run-native-case-comparison.py --case "$(CASE)" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --verified-run-root "$(VERIFIED_RUN_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

verified-nginx-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" FORCE_ALL_CASES=1 MODSECURITY_TEST_VARIANT="$(CRS)" MODSECURITY_MRTS_VARIANT="$(MRTS)" TEST_CASE="$(CASE)" CASE_SCOPE=all RESULTS_DIR="$(BUILD_ROOT)/verified-nginx-case/$(CRS)/$(MRTS)/results" NGINX_HARNESS_WORK_ROOT="$(BUILD_ROOT)/verified-nginx-case/$(CRS)-$(MRTS)-nginx" sh "$(FRAMEWORK_ROOT)/ci/run-nginx-smoke.sh"

verified-apache-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" FORCE_ALL_CASES=1 MODSECURITY_TEST_VARIANT="$(CRS)" MODSECURITY_MRTS_VARIANT="$(MRTS)" TEST_CASE="$(CASE)" CASE_SCOPE=all RESULTS_DIR="$(BUILD_ROOT)/verified-apache-case/$(CRS)/$(MRTS)/results" APACHE_RUNTIME_LOG_DIR="$(BUILD_ROOT)/verified-apache-case/$(CRS)-$(MRTS)-apache/logs/apache-runtime" RUNTIME_BASE="$(BUILD_ROOT)/verified-apache-case/$(CRS)-$(MRTS)-apache/apache-runtime" sh "$(FRAMEWORK_ROOT)/ci/run-apache-smoke.sh"

verified-haproxy-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" SOURCE_ROOT="$(SOURCE_ROOT)" BUILD_ROOT="$(BUILD_ROOT)" TMP_ROOT="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)-$(MRTS)-haproxy/tmp" FORCE_ALL_CASES=1 MODSECURITY_TEST_VARIANT="$(CRS)" MODSECURITY_MRTS_VARIANT="$(MRTS)" TEST_CASE="$(CASE)" RUN_ONE_CASE=1 CASE_SCOPE=all RESULTS_DIR="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)/$(MRTS)/results" LOG_ROOT="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)-$(MRTS)-haproxy/logs" RUNTIME_BASE="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)-$(MRTS)-haproxy/haproxy-runtime-cases" sh "$(FRAMEWORK_ROOT)/ci/run-haproxy-smoke.sh"

verified-full-matrix-resume: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase full-matrix-resume

smoke-common: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=common sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"

smoke-apache: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/apache}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-apache-smoke.sh"

smoke-nginx: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/nginx}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-nginx-smoke.sh"

smoke-envoy: check-framework
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-envoy-smoke.sh"

smoke-envoy-modsecurity:
	DECISION_BACKEND=libmodsecurity $(MAKE) smoke-envoy

smoke-envoy-request-body:
	DECISION_BACKEND=libmodsecurity MODSECURITY_SMOKE_CASE=request_body $(MAKE) smoke-envoy

smoke-envoy-crs:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs $(MAKE) smoke-envoy

smoke-envoy-crs-secondary:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary $(MAKE) smoke-envoy

smoke-haproxy: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/haproxy}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-haproxy-smoke.sh"

smoke-lighttpd: check-framework
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-lighttpd-smoke.sh"

smoke-lighttpd-modsecurity:
	DECISION_BACKEND=libmodsecurity $(MAKE) smoke-lighttpd

smoke-lighttpd-request-body:
	DECISION_BACKEND=libmodsecurity MODSECURITY_SMOKE_CASE=request_body $(MAKE) smoke-lighttpd

smoke-lighttpd-crs:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs $(MAKE) smoke-lighttpd

smoke-lighttpd-crs-secondary:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary $(MAKE) smoke-lighttpd

smoke-traefik: check-framework
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-traefik-smoke.sh"

smoke-traefik-modsecurity:
	DECISION_BACKEND=libmodsecurity $(MAKE) smoke-traefik

smoke-traefik-request-body:
	DECISION_BACKEND=libmodsecurity MODSECURITY_SMOKE_CASE=request_body $(MAKE) smoke-traefik

smoke-traefik-crs:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs $(MAKE) smoke-traefik

smoke-traefik-crs-secondary:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary $(MAKE) smoke-traefik

smoke-open-connectors-crs:
	$(MAKE) smoke-envoy-crs
	$(MAKE) smoke-traefik-crs
	$(MAKE) smoke-lighttpd-crs

smoke-open-connectors-request-body:
	$(MAKE) smoke-envoy-request-body
	$(MAKE) smoke-traefik-request-body
	$(MAKE) smoke-lighttpd-request-body

smoke-open-connectors-crs-secondary:
	$(MAKE) smoke-envoy-crs-secondary
	$(MAKE) smoke-traefik-crs-secondary
	$(MAKE) smoke-lighttpd-crs-secondary

smoke-new-connectors: check-framework prepare-runtime-components
	@$(WITH_RUNTIME_COMPONENTS) sh -eu -c 'set +e; \
	passed=0; blocked=0; failed=0; \
	for connector in envoy haproxy lighttpd traefik; do \
		echo "smoke-new-connectors: running $$connector"; \
		CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-$$connector-smoke.sh"; \
		rc=$$?; \
		echo "smoke-new-connectors: $$connector rc=$$rc"; \
		if [ "$$rc" -eq 0 ]; then \
			passed=$$((passed + 1)); \
		elif [ "$$rc" -eq 77 ]; then \
			blocked=$$((blocked + 1)); \
		else \
			failed=$$((failed + 1)); \
		fi; \
	done; \
	echo "smoke-new-connectors: PASS=$$passed BLOCKED=$$blocked FAIL=$$failed"; \
	if [ "$$failed" -ne 0 ]; then \
		echo "smoke-new-connectors: FAIL"; \
		exit 1; \
	fi; \
	if [ "$$passed" -eq 0 ]; then \
		echo "smoke-new-connectors: BLOCKED - Runtime not verified"; \
		exit 77; \
	fi; \
	if [ "$$blocked" -ne 0 ]; then \
		echo "smoke-new-connectors: BLOCKED - some new connectors remain runtime not verified"; \
		exit 77; \
	fi; \
	echo "smoke-new-connectors: PASS - runtime smoke verified"; \
	exit 0'

smoke-all: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh")

test: test-no-crs test-with-crs

test-no-crs: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env MODSECURITY_TEST_VARIANT=no-crs MODSECURITY_RULE_PREAMBLE_FILE= sh -eu -c '. "$(FRAMEWORK_ROOT)/ci/common.sh"; RESULTS_DIR="$$BUILD_ROOT/results/no-crs"; export RESULTS_DIR; CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"')

test-with-crs: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env MODSECURITY_TEST_VARIANT=with-crs sh -eu -c '. "$(FRAMEWORK_ROOT)/ci/common.sh"; sh "$(FRAMEWORK_ROOT)/ci/fetch-crs.sh"; sh "$(FRAMEWORK_ROOT)/ci/prepare-crs.sh"; MODSECURITY_RULE_PREAMBLE_FILE="$$CRS_RUNTIME_DIR/modsecurity-crs-preamble.conf"; RESULTS_DIR="$$BUILD_ROOT/results/with-crs"; export MODSECURITY_RULE_PREAMBLE_FILE RESULTS_DIR; CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"')

mrts-generate: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-generate

mrts-load: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-load

mrts-import: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-import

test-no-mrts: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-no-mrts)

test-with-mrts: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-with-mrts)

test-with-mrts-feature-demo: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-with-mrts-feature-demo)

test-mrts-matrix: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-mrts-matrix)

mrts-ftw: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-ftw

runtime-matrix: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" sh "$(FRAMEWORK_ROOT)/ci/run-runtime-matrix.sh"

runtime-matrix-all: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FORCE_ALL_CASES=1 sh "$(FRAMEWORK_ROOT)/ci/run-runtime-matrix.sh")

runtime-matrix-all-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FORCE_ALL_CASES=1 sh "$(FRAMEWORK_ROOT)/ci/run-runtime-matrix.sh"

runtime-matrix-haproxy: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" HAPROXY_MATRIX_VARIANT=all sh "$(FRAMEWORK_ROOT)/ci/run-haproxy-runtime-matrix.sh"

full-mrts-runtime-matrix: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-full-mrts-runtime-matrix.sh)

mrts-only-full-run: full-mrts-runtime-matrix

full-runtime-matrix: full-matrix-parallel

full-matrix-parallel: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-full-matrix-parallel.sh)

full-matrix-parallel-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-full-matrix-parallel.sh

full-matrix-single-job-runtime: check-framework prepare-runtime-components
	@test -n "$(CONNECTOR)" || { echo "CONNECTOR is required, e.g. CONNECTOR=nginx"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" "$(FRAMEWORK_PYTHON)" ci/run-full-matrix-job.py --connector "$(CONNECTOR)" --crs "$(CRS)" --mrts "$(MRTS)" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --timeout-seconds "$(VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS)"

full-matrix-resume-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" "$(FRAMEWORK_PYTHON)" ci/run-full-matrix-resume.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --job-timeout-seconds "$(VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS)" --total-timeout-seconds "$(VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS)"

generate-full-runtime-matrix: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-full-runtime-matrix.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --log-root "$(LOG_ROOT)"

generate-full-matrix-job-completeness: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-full-matrix-job-completeness.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest" --rewrite-manifest

generate-nginx-mrts-http500-cluster-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-nginx-mrts-http500-cluster-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-work-queue: check-framework
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/generate-connector-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/canonical/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/generate-phase-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --connector-work-queue "$(CURDIR)/reports/testing/generated/work-queues/connector-work-queue.generated.json" --phase-coverage "$(CURDIR)/reports/testing/generated/coverage/phase-coverage.generated.md" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/canonical/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" ci/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-phase4-hard-abort-capability.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/generate-intervention-blocking-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-no-mrts-intervention-nomatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-body-processor-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-rule-chain-semantics-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-final-consistency-audit.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-phase-work-queue: check-framework
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/generate-phase-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --connector-work-queue "$(CURDIR)/reports/testing/generated/work-queues/connector-work-queue.generated.json" --phase-coverage "$(CURDIR)/reports/testing/generated/coverage/phase-coverage.generated.md" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/canonical/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" ci/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-phase4-hard-abort-capability.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/generate-intervention-blocking-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-no-mrts-intervention-nomatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-body-processor-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-rule-chain-semantics-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-final-consistency-audit.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-nolog-audit-evidence-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-response-header-hook-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-phase4-hard-abort-capability: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-phase4-hard-abort-capability.py --connector-root "$(CURDIR)"

generate-intervention-blocking-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-intervention-blocking-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-no-mrts-intervention-nomatch-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-no-mrts-intervention-nomatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-body-processor-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-body-processor-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-rule-chain-semantics-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-rule-chain-semantics-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-final-consistency-audit: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-final-consistency-audit.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-remaining-failure-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"

mrts-native-full-run: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-mrts-native-full.sh)

mrts-native-full-run-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-mrts-native-full.sh

mrts-native-apache-full: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env MRTS_NATIVE_TARGETS=apache2_ubuntu PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-mrts-native-full.sh

mrts-native-nginx-pr24-full: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env MRTS_NATIVE_TARGETS=nginx-pr24 PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-mrts-native-full.sh

mrts-upstream-infra-check: check-framework
	@sh -eu -c ' \
		MRTS_ROOT="$${MRTS_ROOT:-$(FRAMEWORK_ROOT)/tools/MRTS}"; \
		test -d "$$MRTS_ROOT/config_infra/apache2_ubuntu" || { echo "BLOCKED: missing $$MRTS_ROOT/config_infra/apache2_ubuntu"; exit 77; }; \
		test -d "$(FRAMEWORK_ROOT)/tests/mrts/infra-overlays/nginx-pr24" || { echo "BLOCKED: missing Framework NGINX PR24 overlay"; exit 77; }; \
		test -f "$(FRAMEWORK_ROOT)/tests/mrts/infra-overlays/nginx-pr24/metadata.yaml" || { echo "BLOCKED: missing NGINX PR24 overlay metadata"; exit 77; }; \
		echo "MRTS upstream/native infrastructure inputs present"; \
	'

test-haproxy-no-crs: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" HAPROXY_MATRIX_VARIANT=no-crs sh "$(FRAMEWORK_ROOT)/ci/run-haproxy-runtime-matrix.sh"

test-haproxy-with-crs: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" HAPROXY_MATRIX_VARIANT=with-crs sh "$(FRAMEWORK_ROOT)/ci/run-haproxy-runtime-matrix.sh"

probe-response-body: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" sh "$(FRAMEWORK_ROOT)/ci/probe-response-body-blocking.sh"

connector-starter-checks: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env SOURCE_ROOT="$(SOURCE_ROOT)" BUILD_ROOT="$(BUILD_ROOT)" TMP_ROOT="$(TMP_ROOT)" LOG_ROOT="$(LOG_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/run-connector-starter-checks.sh"

.PHONY: check-apache-common-adoption check-apache-c-standard-wiring check-apache-c-standards check-apache-c17 check-apache-c17-lint check-apache-c23 check-apache-future-c check-apache-c20 check-apache-c26 check-nginx-common-adoption check-nginx-c-standard-wiring check-nginx-c-standards check-nginx-c17 check-nginx-c17-lint check-nginx-c23 check-nginx-future-c check-nginx-c20 check-nginx-c26 check-haproxy-common-adoption check-haproxy-c-standard-wiring check-haproxy-c-standards check-haproxy-c17 check-haproxy-c17-lint check-haproxy-c23 check-haproxy-future-c check-haproxy-c20 check-haproxy-c26 check-common-helpers check-common-helpers-c17 check-common-helpers-c23 check-common-helpers-future-c check-common-helpers-c20 check-common-helpers-c26 check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity check-adapter-contracts check-directive-parity check-remaining-connectors-common-adoption check-envoy-common-adoption check-traefik-common-adoption check-lighttpd-common-adoption check-remaining-connectors-host-integration check-remaining-connectors-build-wiring check-remaining-connectors-start-wiring check-remaining-connectors-claim-policy check-remaining-connectors-c-standard-wiring check-remaining-connectors-c-standards check-remaining-connectors-c17 check-remaining-connectors-c17-lint check-remaining-connectors-c23 check-remaining-connectors-future-c check-block-status-generator build-envoy-connector check-envoy-config start-smoke-envoy runtime-smoke-envoy build-traefik-connector check-traefik-config start-smoke-traefik runtime-smoke-traefik build-lighttpd-connector build-lighttpd-bridge self-test-lighttpd-bridge check-lighttpd-config start-smoke-lighttpd runtime-smoke-lighttpd build-remaining-connectors start-smoke-remaining-connectors runtime-smoke-remaining-connectors readiness-remaining-connectors

build-envoy-connector:
	sh ci/run-remaining-connector-target.sh envoy build-envoy-connector

check-envoy-config: build-envoy-connector
	sh ci/run-remaining-connector-target.sh envoy check-envoy-config

start-smoke-envoy: check-envoy-config
	sh ci/run-remaining-connector-target.sh envoy start-smoke-envoy

runtime-smoke-envoy: build-envoy-connector
	sh ci/run-remaining-connector-target.sh envoy runtime-smoke-envoy

build-traefik-connector:
	sh ci/run-remaining-connector-target.sh traefik build-traefik-connector

check-traefik-config: build-traefik-connector
	sh ci/run-remaining-connector-target.sh traefik check-traefik-config

start-smoke-traefik: check-traefik-config
	sh ci/run-remaining-connector-target.sh traefik start-smoke-traefik

runtime-smoke-traefik: build-traefik-connector
	sh ci/run-remaining-connector-target.sh traefik runtime-smoke-traefik

build-lighttpd-connector:
	sh ci/run-remaining-connector-target.sh lighttpd build-lighttpd-connector

build-lighttpd-bridge:
	sh ci/run-remaining-connector-target.sh lighttpd build-lighttpd-bridge

self-test-lighttpd-bridge: build-lighttpd-bridge
	sh ci/run-remaining-connector-target.sh lighttpd self-test-lighttpd-bridge

check-lighttpd-config: build-lighttpd-connector
	sh ci/run-remaining-connector-target.sh lighttpd check-lighttpd-config

start-smoke-lighttpd: check-lighttpd-config
	sh ci/run-remaining-connector-target.sh lighttpd start-smoke-lighttpd

runtime-smoke-lighttpd: build-lighttpd-connector
	sh ci/run-remaining-connector-target.sh lighttpd runtime-smoke-lighttpd

build-remaining-connectors: build-envoy-connector build-traefik-connector build-lighttpd-connector

start-smoke-remaining-connectors: start-smoke-envoy start-smoke-traefik start-smoke-lighttpd

runtime-smoke-remaining-connectors: runtime-smoke-envoy runtime-smoke-traefik runtime-smoke-lighttpd

readiness-remaining-connectors: check-envoy-common-adoption check-traefik-common-adoption check-lighttpd-common-adoption check-remaining-connectors-host-integration check-remaining-connectors-build-wiring check-remaining-connectors-start-wiring check-remaining-connectors-claim-policy
	$(PYTHON) ci/check-bilingual-docs.py

check-remaining-connectors-common-adoption:
	$(PYTHON) ci/check-remaining-connectors-common-adoption.py

check-envoy-common-adoption:
	$(PYTHON) ci/check-remaining-connectors-common-adoption.py --connector envoy

check-traefik-common-adoption:
	$(PYTHON) ci/check-remaining-connectors-common-adoption.py --connector traefik

check-lighttpd-common-adoption:
	$(PYTHON) ci/check-remaining-connectors-common-adoption.py --connector lighttpd

check-remaining-connectors-host-integration:
	$(PYTHON) ci/check-remaining-connectors-host-integration.py

check-remaining-connectors-build-wiring:
	$(PYTHON) ci/check-remaining-connectors-build-wiring.py

check-remaining-connectors-start-wiring:
	$(PYTHON) ci/check-remaining-connectors-start-wiring.py

check-remaining-connectors-claim-policy:
	$(PYTHON) ci/check-remaining-connectors-claim-policy.py

check-remaining-connectors-c-standard-wiring:
	$(PYTHON) ci/check-remaining-connectors-c-standard-wiring.py

check-remaining-connectors-c-standards:
	sh ci/check-remaining-connectors-c-standards.sh

check-remaining-connectors-c17:
	CONNECTOR_C_STD_PROFILE=c17 sh ci/check-remaining-connectors-c-standards.sh

check-remaining-connectors-c17-lint:
	@CONNECTOR_C_STD_PROFILE=c17 sh ci/check-remaining-connectors-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: remaining connector C17 check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-remaining-connectors-c23:
	CONNECTOR_C_STD_PROFILE=c23 sh ci/check-remaining-connectors-c-standards.sh

check-remaining-connectors-future-c:
	CONNECTOR_C_STD_PROFILE=c2y sh ci/check-remaining-connectors-c-standards.sh

check-block-status-generator:
	$(PYTHON) ci/check-block-status-generator.py

check-apache-common-adoption:
	$(PYTHON) ci/check-apache-common-adoption.py

check-apache-c-standard-wiring:
	$(PYTHON) ci/check-apache-c-standard-wiring.py

check-apache-c-standards:
	sh ci/check-apache-c-standards.sh

check-apache-c17:
	APACHE_C_STD_PROFILE=c17 sh ci/check-apache-c-standards.sh

check-apache-c17-lint:
	@APACHE_C_STD_PROFILE=c17 sh ci/check-apache-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: apache C17 compile check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-apache-c23:
	APACHE_C_STD_PROFILE=c23 sh ci/check-apache-c-standards.sh

check-apache-future-c:
	APACHE_C_STD_PROFILE=c2y sh ci/check-apache-c-standards.sh

check-apache-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-apache-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-nginx-common-adoption:
	$(PYTHON) ci/check-nginx-common-adoption.py

check-nginx-c-standard-wiring:
	$(PYTHON) ci/check-nginx-c-standard-wiring.py

check-nginx-c-standards:
	sh ci/check-nginx-c-standards.sh

check-nginx-c17:
	NGINX_C_STD_PROFILE=c17 sh ci/check-nginx-c-standards.sh

check-nginx-c17-lint:
	@NGINX_C_STD_PROFILE=c17 sh ci/check-nginx-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: nginx C17 compile check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-nginx-c23:
	NGINX_C_STD_PROFILE=c23 sh ci/check-nginx-c-standards.sh

check-nginx-future-c:
	NGINX_C_STD_PROFILE=c2y sh ci/check-nginx-c-standards.sh

check-nginx-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-nginx-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-haproxy-common-adoption:
	$(PYTHON) ci/check-haproxy-common-adoption.py

check-haproxy-c-standard-wiring:
	$(PYTHON) ci/check-haproxy-c-standard-wiring.py

check-haproxy-c-standards:
	sh ci/check-haproxy-c-standards.sh

check-haproxy-c17:
	HAPROXY_C_STD_PROFILE=c17 sh ci/check-haproxy-c-standards.sh

check-haproxy-c17-lint:
	@HAPROXY_C_STD_PROFILE=c17 sh ci/check-haproxy-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: haproxy C17 compile check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-haproxy-c23:
	HAPROXY_C_STD_PROFILE=c23 sh ci/check-haproxy-c-standards.sh

check-haproxy-future-c:
	HAPROXY_C_STD_PROFILE=c2y sh ci/check-haproxy-c-standards.sh

check-haproxy-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-haproxy-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-common-helpers:
	MSCONNECTOR_C_STD="$(MSCONNECTOR_C_STD)" MSCONNECTOR_CFLAGS="$(MSCONNECTOR_CFLAGS)" sh ci/check-common-helpers.sh

check-common-helpers-c17:
	$(MAKE) check-common-helpers MSCONNECTOR_C_STD=c17

check-common-helpers-c23:
	@flag="$$(python3 ci/detect-c-standard.py --profile c23 --compiler "$(MSCONNECTOR_COMPILER_ID)")" || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: optional C23 check — compiler does not support c23 or c2x"; exit 0; fi; exit "$$rc"; }; \
	$(MAKE) check-common-helpers CC="$(MSCONNECTOR_COMPILER_ID)" MSCONNECTOR_C_STD=c23 MSCONNECTOR_CFLAGS="$$flag -Wall -Wextra -Werror"

check-common-helpers-future-c:
	@flag="$$(python3 ci/detect-c-standard.py --profile c2y --compiler "$(MSCONNECTOR_COMPILER_ID)")" || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: optional future C check — compiler does not support c2y or gnu2y"; exit 0; fi; exit "$$rc"; }; \
	$(MAKE) check-common-helpers CC="$(MSCONNECTOR_COMPILER_ID)" MSCONNECTOR_C_STD=c2y MSCONNECTOR_CFLAGS="$$flag -Wall -Wextra -Werror"

check-common-helpers-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-common-helpers-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-common-sdk-contract:
	$(PYTHON) ci/check-common-sdk-contract.py

check-common-security-contract:
	$(PYTHON) ci/check-common-security-contract.py

check-common-memory-safety:
	sh ci/check-common-memory-safety.sh

check-common-flow-integrity:
	$(PYTHON) ci/check-common-flow-integrity.py

check-adapter-contracts:
	$(PYTHON) ci/check-adapter-contracts.py

check-directive-parity:
	$(PYTHON) ci/check-directive-parity.py

lint: check-framework
	sh -n ci/*.sh
	find connectors/envoy connectors/traefik connectors/lighttpd -type f -name '*.sh' -exec sh -n {} +
	if command -v bash >/dev/null 2>&1; then bash -n ci/*.sh; find connectors/envoy connectors/traefik connectors/lighttpd -type f -name '*.sh' -exec bash -n {} +; else echo "bash unavailable"; fi
	PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile ci/*.py
	$(MAKE) check-apache-common-adoption
	$(MAKE) check-apache-c-standard-wiring
	$(MAKE) check-apache-c17-lint
	$(MAKE) check-nginx-common-adoption
	$(MAKE) check-nginx-c-standard-wiring
	$(MAKE) check-nginx-c17-lint
	$(MAKE) check-haproxy-common-adoption
	$(MAKE) check-haproxy-c-standard-wiring
	$(MAKE) check-haproxy-c17-lint
	$(MAKE) check-remaining-connectors-common-adoption
	$(MAKE) check-remaining-connectors-host-integration
	$(MAKE) check-remaining-connectors-build-wiring
	$(MAKE) check-remaining-connectors-start-wiring
	$(MAKE) check-remaining-connectors-claim-policy
	$(MAKE) check-remaining-connectors-c-standard-wiring
	$(MAKE) check-remaining-connectors-c17-lint
	$(MAKE) check-common-sdk-contract
	$(MAKE) check-common-security-contract
	$(MAKE) check-common-memory-safety
	$(MAKE) check-common-flow-integrity
	$(MAKE) check-adapter-contracts
	$(MAKE) check-directive-parity
	$(MAKE) check-framework-fixture-syntax
	$(MAKE) report-governance
	$(PYTHON) -m json.tool config/testing/import-status.json >/dev/null
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-python-deps.py"
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-workflow-yaml.py"
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-doc-links.py"
	$(MAKE) check-bilingual-docs
	sh "$(FRAMEWORK_ROOT)/ci/check-crs-version-pinning.sh"
	sh ci/check-common-helpers.sh
	sh ci/check-adapter-helpers.sh
	sh ci/check-adapter-metadata-drift.sh
	if command -v actionlint >/dev/null 2>&1; then actionlint .github/workflows/*.yml; else echo "actionlint unavailable"; fi
	git diff --check

summary: check-framework
	$(PYTHON) "$(FRAMEWORK_ROOT)/ci/summarize-results.py" "$(BUILD_ROOT)/results/connector-summary.json"

case-matrix: check-framework
	$(PYTHON) "$(FRAMEWORK_ROOT)/ci/write-case-matrix.py" "$(BUILD_ROOT)/results/connector-summary.json" reports/testing/case-matrix.md

install-dev-deps: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/bootstrap-python.sh"

setup-dev: install-dev-deps
	@echo "setup-dev: using PYTHON=$(PYTHON)"
	@echo "setup-dev: test framework -> $(FRAMEWORK_ROOT)"
	@echo "setup-dev: next steps -> make lint; make fetch-deps; make doctor; make smoke-all"

fetch-modsecurity-v3: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/fetch-smoke-sources.sh" v3

fetch-deps bootstrap-runtime: prepare-runtime-components
	@echo "fetch-deps: runtime components prepared in CONNECTOR_COMPONENT_CACHE=$${CONNECTOR_COMPONENT_CACHE:-auto}"

fetch-crs: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/fetch-crs.sh"

prepare-crs: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/prepare-crs.sh"

doctor env-check: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/doctor.sh"

print-python:
	@echo "make: using PYTHON=$(PYTHON)"

bootstrap-all: setup-dev fetch-deps doctor
	@echo "bootstrap-all complete (smoke not run)"

quick-check codex-check: lint
	PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile "$(FRAMEWORK_ROOT)"/tests/normalizers/*.py "$(FRAMEWORK_ROOT)"/tests/runners/*.py "$(FRAMEWORK_ROOT)"/ci/*.py
	git diff --check

smoke-installed installed-readiness: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/smoke-installed.sh"

doctor-install-hints:
	@echo "Install hints (Debian/Ubuntu example):"
	@echo "  sudo apt-get update"
	@echo "  sudo apt-get install -y git make gcc clang autoconf automake libtool pkg-config apache2-dev nginx libmodsecurity-dev"
	@echo "Install hints (RHEL/Fedora example):"
	@echo "  sudo dnf install -y git make gcc clang autoconf automake libtool pkgconf-pkg-config httpd-devel nginx mod_security"
	@echo "Install hints (Alpine example):"
	@echo "  sudo apk add git make gcc clang autoconf automake libtool pkgconf apache2-dev nginx modsecurity"

doctor-quick: check-framework
	DOCTOR_MODE=quick sh "$(FRAMEWORK_ROOT)/ci/doctor.sh"

quick-all: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/quick-all.sh"

cloud-quick-check: setup-dev lint generate-test-matrix check-test-matrix quick-check
	PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile "$(FRAMEWORK_ROOT)"/tests/normalizers/*.py "$(FRAMEWORK_ROOT)"/tests/runners/*.py "$(FRAMEWORK_ROOT)"/ci/*.py
	git diff --check
	@echo "INFO: Cloud check is framework/generator only and not runtime compatibility evidence."

generate-test-matrix: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" OUTPUT_ROOT="$(CURDIR)" SKIP_ROOT_SUMMARY=1 $(MAKE) -C "$(FRAMEWORK_ROOT)" generate-test-matrix
	$(PYTHON) ci/ensure-test-matrix-language-switches.py

TEST_MATRIX_DIFF_PATHS = reports/testing/generated/coverage reports/testing/generated/runtime reports/testing/test-coverage-overview.md

check-test-matrix: check-framework
	@test ! -f TEST-COVERAGE-SUMMARY.md || { \
		echo "Generated root coverage summary moved to $(FRAMEWORK_ROOT)/TEST-COVERAGE-SUMMARY.md; remove parent TEST-COVERAGE-SUMMARY.md"; \
		exit 1; \
	}
	@mkdir -p "$(BUILD_ROOT)/check-test-matrix"
	@before="$(BUILD_ROOT)/check-test-matrix/before.diff"; \
	after="$(BUILD_ROOT)/check-test-matrix/after.diff"; \
	framework_before="$(BUILD_ROOT)/check-test-matrix/framework-before.diff"; \
	framework_after="$(BUILD_ROOT)/check-test-matrix/framework-after.diff"; \
	git diff --binary -- $(TEST_MATRIX_DIFF_PATHS) > "$$before"; \
	git -C "$(FRAMEWORK_ROOT)" diff --binary -- TEST-COVERAGE-SUMMARY.md > "$$framework_before"; \
	$(MAKE) generate-test-matrix; \
	git diff --binary -- $(TEST_MATRIX_DIFF_PATHS) > "$$after"; \
	git -C "$(FRAMEWORK_ROOT)" diff --binary -- TEST-COVERAGE-SUMMARY.md > "$$framework_after"; \
	if ! cmp -s "$$before" "$$after" || ! cmp -s "$$framework_before" "$$framework_after"; then \
		echo "Generated test matrix docs are out of date. Run make generate-test-matrix"; \
		exit 1; \
	fi
