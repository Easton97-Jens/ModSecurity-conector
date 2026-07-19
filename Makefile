PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
MSCONNECTOR_C_STD ?= c17
MSCONNECTOR_CFLAGS ?= -std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror
MSCONNECTOR_COMPILER_ID ?= $(notdir $(firstword $(CC)))
CLANG_TIDY ?= clang-tidy
CLANG ?= clang
CLANGXX ?= clang++
CLANG_TIDY_CHECKS ?= -*,bugprone-*,cert-*
CLANG_ANALYZER_CHECKS ?= core,unix,security,cplusplus,deadcode
FRAMEWORK_PYTHON := $(if $(findstring /,$(PYTHON)),$(abspath $(PYTHON)),$(PYTHON))
VERIFIED_RUN_PARENT ?= $(if $(RUNNER_TEMP),$(RUNNER_TEMP),$(if $(TMPDIR),$(TMPDIR),/var/tmp))
VERIFIED_RUN_ROOT ?= $(VERIFIED_RUN_PARENT)/ModSecurity-conector-verified
VERIFIED_STATE_ROOT ?= $(VERIFIED_RUN_ROOT)/state
VERIFIED_BUILD_ROOT ?= $(VERIFIED_RUN_ROOT)/build
VERIFIED_SOURCE_ROOT ?= $(VERIFIED_RUN_ROOT)/src
VERIFIED_TMP_ROOT ?= $(VERIFIED_RUN_ROOT)/tmp
VERIFIED_LOG_ROOT ?= $(VERIFIED_RUN_ROOT)/logs
# Cache-v2 is deliberately separate from ephemeral connector build/run trees.
# The shared child is the only reusable component cache passed to all targets.
CACHE_ROOT ?= $(VERIFIED_RUN_ROOT)/cache-v2
VERIFIED_COMPONENT_CACHE ?= $(CACHE_ROOT)/shared
VERIFIED_EVIDENCE_ROOT ?= $(VERIFIED_RUN_ROOT)/evidence
RUNTIME_RUN_ROOT ?= $(VERIFIED_RUN_ROOT)/runs
RUNTIME_LOG_ROOT ?= $(VERIFIED_RUN_ROOT)/run-logs
STATE_HOME ?= $(VERIFIED_STATE_ROOT)
SOURCE_ROOT ?= $(VERIFIED_SOURCE_ROOT)
BUILD_ROOT ?= $(VERIFIED_BUILD_ROOT)
# Host harnesses may create connector-local transient files and require their
# temporary root to remain below BUILD_ROOT.  Keep the legacy verified tmp
# root available for callers that need it, but make the standard target
# default build-contained so no inherited run-root tmp path can block HAProxy.
TMP_ROOT ?= $(BUILD_ROOT)/tmp
LOG_ROOT ?= $(BUILD_ROOT)/logs
MATRIX_ROOT ?= $(BUILD_ROOT)/full-matrix
FRAMEWORK_ROOT ?= $(CURDIR)/modules/ModSecurity-test-Framework
CONNECTOR_ROOT := $(CURDIR)
# Keep the six native profiles as the default, while allowing a bounded
# connector subset for isolated diagnostics without editing the Makefile.
NO_CRS_CONNECTORS ?= apache nginx haproxy envoy traefik lighttpd
EVIDENCE_ROOT ?= $(VERIFIED_EVIDENCE_ROOT)/no-crs-evidence
RUNTIME_EVIDENCE_ROOT ?= $(VERIFIED_EVIDENCE_ROOT)/runtime-evidence
CAPABILITY_PLAN_ROOT ?= $(BUILD_ROOT)/no-crs-capability-plans
CAPABILITY_REPORT_EVIDENCE_ROOT ?= $(EVIDENCE_ROOT)
CAPABILITY_REPORT_RUN_ID ?= $(NO_CRS_RUN_ID)
CAPABILITY_REPORT_OUTPUT_DIR ?= $(EVIDENCE_ROOT)/connector-capabilities
NO_CRS_RUN_ID ?=
NO_CRS_RULES_FILE ?= $(FRAMEWORK_ROOT)/tests/rules/no-crs-baseline.conf
# Optional managed client bundle for a forced modern-protocol run.  The
# canonical root runner validates that it stays inside the invocation's raw
# evidence tree before passing it to Framework finalization.
NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR ?=
# Opt in to a stage-owned protocol probe without having to pre-create the
# fresh raw-run directory.  It is non-promoting unless every protocol case,
# client observation, and host event passes the Framework's causal checks.
NO_CRS_PROTOCOL_CLIENT ?= 0
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
WITH_RUNTIME_COMPONENTS = SKIP_RUNTIME_COMPONENT_PREPARE=1 sh ci/provisioning/cache/with-runtime-components.sh

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
export CACHE_ROOT
export VERIFIED_EVIDENCE_ROOT
export RUNTIME_RUN_ROOT
export RUNTIME_LOG_ROOT
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
export EVIDENCE_ROOT
export RUNTIME_EVIDENCE_ROOT
export CAPABILITY_PLAN_ROOT
export NO_CRS_RUN_ID
export NO_CRS_RULES_FILE
export NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR
export NO_CRS_PROTOCOL_CLIENT
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

.PHONY: check-framework prepare-runtime-components prepare-envoy-runtime prepare-traefik-runtime prepare-lighttpd-runtime prepare-lighttpd-runtime-build prepare-open-connector-runtimes runtime-components-inventory runtime-components-sources check-framework-fixture-syntax check-runtime-producer-readiness check-runtime-path-policy check-bilingual-docs check-doc-links check-variable-documentation check-connector-config-reference generate-connector-config-reference refresh-connector-reports refresh-all-reports check-generated-report-layout report-governance verified-report-evidence-gate generate-system-environment-proof prove-generated-reports verified-runtime-producers verified-report-refresh verified-report-producers verified-report-consumers verified-report-checks verified-report-run verified-report-run-soft verified-report-run-smoke verified-full-matrix-job verified-case verified-native-case verified-apache-case verified-nginx-case verified-haproxy-case verified-full-matrix-resume full-matrix-single-job-runtime full-matrix-resume-runtime smoke-common smoke-apache smoke-nginx smoke-envoy smoke-envoy-modsecurity smoke-envoy-crs smoke-envoy-crs-secondary smoke-haproxy smoke-lighttpd smoke-lighttpd-modsecurity smoke-lighttpd-crs smoke-lighttpd-crs-secondary smoke-traefik smoke-traefik-modsecurity smoke-traefik-crs smoke-traefik-crs-secondary smoke-open-connectors-crs smoke-open-connectors-crs-secondary smoke-new-connectors smoke-all test test-no-crs test-with-crs test-haproxy-no-crs test-haproxy-with-crs runtime-matrix runtime-matrix-all runtime-matrix-all-runtime runtime-matrix-haproxy full-runtime-matrix full-mrts-runtime-matrix mrts-only-full-run full-matrix-parallel full-matrix-parallel-runtime generate-full-runtime-matrix generate-full-matrix-job-completeness generate-nginx-mrts-http500-cluster-analysis generate-work-queue generate-phase-work-queue generate-nolog-audit-evidence-analysis generate-response-header-hook-analysis generate-phase4-hard-abort-capability generate-intervention-blocking-analysis generate-no-mrts-intervention-nomatch-analysis generate-body-processor-analysis generate-rule-chain-semantics-analysis generate-final-consistency-audit generate-native-semantics-comparison generate-remaining-critical-batch-analysis generate-remaining-failure-analysis mrts-native-full-run mrts-native-full-run-runtime mrts-native-apache-full mrts-native-nginx-pr24-full mrts-upstream-infra-check probe-response-body connector-starter-checks lint summary case-matrix setup-dev install-dev-deps doctor doctor-quick env-check fetch-deps fetch-modsecurity-v3 fetch-crs prepare-crs bootstrap-runtime quick-check codex-check quick-all smoke-installed installed-readiness doctor-install-hints cloud-quick-check generate-test-matrix check-test-matrix mrts-generate mrts-load mrts-import test-no-mrts test-with-mrts-feature-demo test-mrts-matrix mrts-ftw
.PHONY: smoke-envoy-request-body smoke-traefik-request-body smoke-lighttpd-request-body smoke-open-connectors-request-body
.PHONY: check-compiler-guides
.PHONY: check-ci-security-contract
.PHONY: check-analysis-tools compile-db-nginx-c17 check-targeted-evaluator-cpp17 compile-db-cpp17 check-clangd-c17
.PHONY: check-clang-analysis-tools clang-tidy-baseline clang-analyzer-baseline clang-analysis-baseline
.PHONY: build-apache build-nginx build-haproxy build-envoy build-traefik build-lighttpd build-all-connectors
.PHONY: check-config-apache check-config-nginx check-config-haproxy check-config-envoy check-config-traefik check-config-lighttpd check-config-all-connectors
.PHONY: start-smoke-apache start-smoke-nginx start-smoke-haproxy start-smoke-all-connectors
.PHONY: runtime-smoke-apache runtime-smoke-nginx runtime-smoke-haproxy runtime-smoke-all-connectors
.PHONY: no-crs-baseline-apache no-crs-baseline-nginx no-crs-baseline-haproxy no-crs-baseline-envoy no-crs-baseline-traefik no-crs-baseline-lighttpd no-crs-baseline-all-connectors
.PHONY: capabilities-apache capabilities-nginx capabilities-haproxy capabilities-envoy capabilities-traefik capabilities-lighttpd capabilities-all-connectors capabilities-all-connectors-evidence
.PHONY: evidence-check-apache evidence-check-nginx evidence-check-haproxy evidence-check-envoy evidence-check-traefik evidence-check-lighttpd evidence-check-all-connectors
.PHONY: check-no-crs-result-schema check-no-crs-evidence-completeness check-no-crs-capability-consistency check-no-crs-claim-policy check-no-crs-artifact-layout check-no-crs-body-payload-absence check-no-crs-status-consistency check-no-crs-protocol-client check-no-crs-doc-consistency check-no-crs-source-normalization
.PHONY: full-lifecycle-apache full-lifecycle-nginx full-lifecycle-haproxy full-lifecycle-envoy full-lifecycle-traefik full-lifecycle-lighttpd full-lifecycle-all-connectors
.PHONY: full-lifecycle-haproxy-htx full-lifecycle-envoy-ext-proc full-lifecycle-traefik-native full-lifecycle-lighttpd-patched
.PHONY: check-first-byte-before-response-end check-no-full-response-buffering check-full-lifecycle-event-privacy check-full-lifecycle-transport check-full-lifecycle-lifecycle check-full-lifecycle-transport-hardening check-full-lifecycle-promotion check-six-connector-core-completion
.PHONY: protocol-client check-protocol-evidence test-protocol-client

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

# Forward the opt-in managed protocol client and its evidence gate from the
# Framework without implying that a host build alone is protocol evidence.
protocol-client: check-framework
	$(MAKE) -C "$(FRAMEWORK_ROOT)" protocol-client CONNECTOR_ROOT="$(CURDIR)" BUILD_ROOT="$(BUILD_ROOT)"

check-protocol-evidence: check-framework
	$(MAKE) -C "$(FRAMEWORK_ROOT)" check-protocol-evidence CONNECTOR_ROOT="$(CURDIR)" BUILD_ROOT="$(BUILD_ROOT)"

test-protocol-client: check-framework
	$(MAKE) -C "$(FRAMEWORK_ROOT)" test-protocol-client CONNECTOR_ROOT="$(CURDIR)" BUILD_ROOT="$(BUILD_ROOT)"

check-framework-fixture-syntax: check-framework
	"$(FRAMEWORK_PYTHON)" ci/checks/evidence/check-framework-fixture-syntax.py --framework-root "$(FRAMEWORK_ROOT)"

prepare-runtime-components: check-framework
	@if [ "$(SKIP_RUNTIME_COMPONENT_PREPARE)" = "1" ]; then \
		echo "prepare-runtime-components: skipped (SKIP_RUNTIME_COMPONENT_PREPARE=1)"; \
	else \
		PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/provisioning/components/prepare-runtime-components.sh; \
	fi

prepare-envoy-runtime: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/provisioning/prepare-envoy-runtime.sh"

prepare-traefik-runtime: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/provisioning/prepare-traefik-runtime.sh"

prepare-lighttpd-runtime: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/provisioning/prepare-lighttpd-runtime.sh"

prepare-lighttpd-runtime-build: check-framework
	ALLOW_RUNTIME_BUILDS=1 $(MAKE) prepare-lighttpd-runtime

prepare-open-connector-runtimes: check-framework
	@rc=0; \
	for target in prepare-envoy-runtime prepare-traefik-runtime prepare-lighttpd-runtime; do \
		$(MAKE) $$target || rc=$$?; \
	done; \
	exit $$rc

runtime-components-inventory: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/provisioning/cache/runtime-components-inventory.sh inventory

runtime-components-sources: check-framework
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/provisioning/cache/runtime-components-inventory.sh sources

check-runtime-producer-readiness: check-framework
	"$(FRAMEWORK_PYTHON)" ci/checks/evidence/check-runtime-producer-readiness.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)"

check-runtime-path-policy: check-framework
	"$(FRAMEWORK_PYTHON)" ci/checks/security/check-runtime-path-policy.py

check-bilingual-docs:
	$(PYTHON) ci/checks/documentation/check-bilingual-docs.py

check-ci-security-contract:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest -v tests.test_ci_security_workflows
	$(PYTHON) ci/tools/fetch_security_tool.py --tool actionlint --validate-only
	$(PYTHON) ci/tools/fetch_security_tool.py --tool zizmor --validate-only
	$(PYTHON) ci/tools/fetch_security_tool.py --tool gitleaks --validate-only

check-variable-documentation:
	$(PYTHON) ci/checks/documentation/check-variable-documentation.py

check-compiler-guides:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" -m unittest -v tests.test_compiler_guides

check-analysis-tools:
	PYTHONDONTWRITEBYTECODE=1 CC="$(CC)" CXX="$(CXX)" sh ci/checks/analysis/check-analysis-tools.sh

check-clang-analysis-tools:
	PYTHONDONTWRITEBYTECODE=1 PYTHON="$(PYTHON)" CLANG_TIDY="$(CLANG_TIDY)" CLANG="$(CLANG)" CLANGXX="$(CLANGXX)" sh ci/checks/analysis/check-clang-analysis-tools.sh

clang-tidy-baseline:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" ci/checks/analysis/clang_analysis_baseline.py --mode tidy --compdb-output "$(COMPDB_OUTPUT)" --analysis-output "$(ANALYSIS_OUTPUT)" --clang-tidy "$(CLANG_TIDY)" --clang "$(CLANG)" --clangxx "$(CLANGXX)" --tidy-checks="$(CLANG_TIDY_CHECKS)" --analyzer-checks="$(CLANG_ANALYZER_CHECKS)"

clang-analyzer-baseline:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" ci/checks/analysis/clang_analysis_baseline.py --mode analyzer --compdb-output "$(COMPDB_OUTPUT)" --analysis-output "$(ANALYSIS_OUTPUT)" --clang-tidy "$(CLANG_TIDY)" --clang "$(CLANG)" --clangxx "$(CLANGXX)" --tidy-checks="$(CLANG_TIDY_CHECKS)" --analyzer-checks="$(CLANG_ANALYZER_CHECKS)"

clang-analysis-baseline:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" ci/checks/analysis/clang_analysis_baseline.py --mode combined --compdb-output "$(COMPDB_OUTPUT)" --analysis-output "$(ANALYSIS_OUTPUT)" --clang-tidy "$(CLANG_TIDY)" --clang "$(CLANG)" --clangxx "$(CLANGXX)" --tidy-checks="$(CLANG_TIDY_CHECKS)" --analyzer-checks="$(CLANG_ANALYZER_CHECKS)"

compile-db-nginx-c17:
	PYTHONDONTWRITEBYTECODE=1 CC="$(CC)" PYTHON="$(PYTHON)" COMPDB_OUTPUT="$(COMPDB_OUTPUT)" sh ci/checks/analysis/compile-db-nginx-c17.sh

check-targeted-evaluator-cpp17:
	PYTHONDONTWRITEBYTECODE=1 CXX="$(CXX)" CPP_BUILD_ROOT="$(CPP_BUILD_ROOT)" MODSECURITY_INCLUDE_DIR="$(MODSECURITY_INCLUDE_DIR)" MODSECURITY_LIB_DIR="$(MODSECURITY_LIB_DIR)" MODSECURITY_LIB_FILE="$(MODSECURITY_LIB_FILE)" sh ci/checks/analysis/check-targeted-evaluator-cpp17.sh

compile-db-cpp17:
	PYTHONDONTWRITEBYTECODE=1 CXX="$(CXX)" PYTHON="$(PYTHON)" COMPDB_OUTPUT="$(COMPDB_OUTPUT)" CPP_BUILD_ROOT="$(CPP_BUILD_ROOT)" MODSECURITY_INCLUDE_DIR="$(MODSECURITY_INCLUDE_DIR)" MODSECURITY_LIB_DIR="$(MODSECURITY_LIB_DIR)" MODSECURITY_LIB_FILE="$(MODSECURITY_LIB_FILE)" sh ci/checks/analysis/compile-db-cpp17.sh

check-clangd-c17:
	PYTHONDONTWRITEBYTECODE=1 PYTHON="$(PYTHON)" COMPDB_OUTPUT="$(COMPDB_OUTPUT)" sh ci/checks/analysis/check-clangd-c17.sh

generate-connector-config-reference:
	$(PYTHON) ci/tools/generate-connector-config-reference.py

check-connector-config-reference:
	$(PYTHON) ci/tools/generate-connector-config-reference.py --check
	$(PYTHON) ci/checks/documentation/check-connector-config-reference.py

check-doc-links: check-framework
	$(PYTHON) ci/checks/documentation/check-repository-path-references.py
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/checks/documentation/check-doc-links.py"

refresh-connector-reports: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/refresh-connector-reports.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --native-root "$(MRTS_NATIVE_ROOT)"

refresh-all-reports: check-framework
	@framework_rc=0; \
	$(MAKE) -C "$(FRAMEWORK_ROOT)" PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" OUTPUT_ROOT="$(FRAMEWORK_ROOT)" refresh-framework-reports || framework_rc=$$?; \
	connector_rc=0; \
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/refresh-connector-reports.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --native-root "$(MRTS_NATIVE_ROOT)" --strict-inputs || connector_rc=$$?; \
	if [ "$$framework_rc" -ne 0 ]; then exit "$$framework_rc"; fi; \
	exit "$$connector_rc"

check-generated-report-layout: check-framework
	"$(FRAMEWORK_PYTHON)" ci/checks/documentation/check-generated-report-layout.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

report-governance: check-framework
	$(MAKE) check-runtime-path-policy
	"$(FRAMEWORK_PYTHON)" ci/checks/documentation/check-generated-report-layout.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --governance-only

verified-report-evidence-gate: check-generated-report-layout
	@echo "verified-report-evidence-gate: strict generated-report evidence gate passed"

generate-system-environment-proof: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-system-environment-proof.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-verified-runtime-mismatch-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-remaining-critical-batch-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-remaining-critical-batch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-native-semantics-comparison: check-framework
	"$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-native-case-comparison.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --verified-run-root "$(VERIFIED_RUN_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest" --report-only

prove-generated-reports:
	$(MAKE) refresh-connector-reports
	$(MAKE) check-generated-report-layout
	$(MAKE) lint
	$(MAKE) quick-check
	$(MAKE) generate-system-environment-proof

verified-runtime-producers: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase runtime-producers

verified-report-producers: verified-runtime-producers

verified-report-refresh: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase report-refresh

verified-report-consumers: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase report-refresh

verified-report-checks: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase checks

verified-report-run: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --mode strict

verified-report-run-soft: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --mode soft

verified-report-run-smoke: check-framework
	VERIFIED_RUN_ID="$(FRESH_VERIFIED_RUN_ID)" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --mode soft --profile smoke

verified-full-matrix-job: check-framework
	@test -n "$(CONNECTOR)" || { echo "CONNECTOR is required, e.g. CONNECTOR=nginx"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase full-matrix-job --connector "$(CONNECTOR)" --crs "$(CRS)" --mrts "$(MRTS)"

verified-case: check-framework
	@test -n "$(CONNECTOR)" || { echo "CONNECTOR is required, e.g. CONNECTOR=nginx"; exit 2; }
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	@explain_args=""; \
	case "$${EXPLAIN:-$(EXPLAIN)}$${VERIFIED_CASE_EXPLAIN:-$(VERIFIED_CASE_EXPLAIN)}" in ""|0|false|False) $(MAKE) prepare-runtime-components ;; *) explain_args="--explain" ;; esac; \
	"$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-case.py --connector "$(CONNECTOR)" --case "$(CASE)" --crs "$(CRS)" --mrts "$(MRTS)" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --source-root "$(SOURCE_ROOT)" --tmp-root "$(TMP_ROOT)" --verified-run-root "$(VERIFIED_RUN_ROOT)" --python "$(FRAMEWORK_PYTHON)" $$explain_args

verified-native-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=unicode_whitespace_normalization_gap"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CONNECTOR_ROOT="$(CURDIR)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" BUILD_ROOT="$(BUILD_ROOT)" VERIFIED_RUN_ROOT="$(VERIFIED_RUN_ROOT)" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-native-case-comparison.py --case "$(CASE)" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --verified-run-root "$(VERIFIED_RUN_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

verified-nginx-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" FORCE_ALL_CASES=1 MODSECURITY_TEST_VARIANT="$(CRS)" MODSECURITY_MRTS_VARIANT="$(MRTS)" TEST_CASE="$(CASE)" CASE_SCOPE=all RESULTS_DIR="$(BUILD_ROOT)/verified-nginx-case/$(CRS)/$(MRTS)/results" NGINX_HARNESS_WORK_ROOT="$(BUILD_ROOT)/verified-nginx-case/$(CRS)-$(MRTS)-nginx" sh "$(FRAMEWORK_ROOT)/ci/runtime/run-nginx-smoke.sh"

verified-apache-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" FORCE_ALL_CASES=1 MODSECURITY_TEST_VARIANT="$(CRS)" MODSECURITY_MRTS_VARIANT="$(MRTS)" TEST_CASE="$(CASE)" CASE_SCOPE=all RESULTS_DIR="$(BUILD_ROOT)/verified-apache-case/$(CRS)/$(MRTS)/results" APACHE_RUNTIME_LOG_DIR="$(BUILD_ROOT)/verified-apache-case/$(CRS)-$(MRTS)-apache/logs/apache-runtime" RUNTIME_BASE="$(BUILD_ROOT)/verified-apache-case/$(CRS)-$(MRTS)-apache/apache-runtime" sh "$(FRAMEWORK_ROOT)/ci/runtime/run-apache-smoke.sh"

verified-haproxy-case: check-framework prepare-runtime-components
	@test -n "$(CASE)" || { echo "CASE is required, e.g. CASE=action_deny_phase1"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" SOURCE_ROOT="$(SOURCE_ROOT)" BUILD_ROOT="$(BUILD_ROOT)" TMP_ROOT="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)-$(MRTS)-haproxy/tmp" FORCE_ALL_CASES=1 MODSECURITY_TEST_VARIANT="$(CRS)" MODSECURITY_MRTS_VARIANT="$(MRTS)" TEST_CASE="$(CASE)" RUN_ONE_CASE=1 CASE_SCOPE=all RESULTS_DIR="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)/$(MRTS)/results" LOG_ROOT="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)-$(MRTS)-haproxy/logs" RUNTIME_BASE="$(BUILD_ROOT)/verified-haproxy-case/$(CRS)-$(MRTS)-haproxy/haproxy-runtime-cases" sh "$(FRAMEWORK_ROOT)/ci/runtime/run-haproxy-smoke.sh"

verified-full-matrix-resume: check-framework
	@run_id="$${VERIFIED_RUN_ID:-$$(cat "$(BUILD_ROOT)/verified-runs/current-run-id" 2>/dev/null || true)}"; \
	if [ -z "$$run_id" ]; then run_id="$(FRESH_VERIFIED_RUN_ID)"; fi; \
	VERIFIED_RUN_ID="$$run_id" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-verified-report-run.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --phase full-matrix-resume

smoke-common: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=common sh "$(FRAMEWORK_ROOT)/ci/runtime/run-connector-smokes.sh"

smoke-apache: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/apache}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-apache-smoke.sh"

smoke-nginx: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/nginx}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-nginx-smoke.sh"

smoke-envoy: check-framework
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-envoy-smoke.sh"

smoke-envoy-modsecurity:
	DECISION_BACKEND=libmodsecurity $(MAKE) smoke-envoy

smoke-envoy-request-body:
	DECISION_BACKEND=libmodsecurity MODSECURITY_SMOKE_CASE=request_body $(MAKE) smoke-envoy

smoke-envoy-crs:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs $(MAKE) smoke-envoy

smoke-envoy-crs-secondary:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary $(MAKE) smoke-envoy

smoke-haproxy: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/haproxy}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-haproxy-smoke.sh"

smoke-lighttpd: check-framework
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-lighttpd-smoke.sh"

smoke-lighttpd-modsecurity:
	DECISION_BACKEND=libmodsecurity $(MAKE) smoke-lighttpd

smoke-lighttpd-request-body:
	DECISION_BACKEND=libmodsecurity MODSECURITY_SMOKE_CASE=request_body $(MAKE) smoke-lighttpd

smoke-lighttpd-crs:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs $(MAKE) smoke-lighttpd

smoke-lighttpd-crs-secondary:
	DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary $(MAKE) smoke-lighttpd

smoke-traefik: check-framework
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-traefik-smoke.sh"

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
		CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-$$connector-smoke.sh"; \
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
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-connector-smokes.sh")

test: test-no-crs test-with-crs

test-no-crs: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env MODSECURITY_TEST_VARIANT=no-crs MODSECURITY_RULE_PREAMBLE_FILE= sh -eu -c '. "$(FRAMEWORK_ROOT)/ci/lib/common.sh"; RESULTS_DIR="$$BUILD_ROOT/results/no-crs"; export RESULTS_DIR; CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-connector-smokes.sh"')

test-with-crs: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env MODSECURITY_TEST_VARIANT=with-crs sh -eu -c '. "$(FRAMEWORK_ROOT)/ci/lib/common.sh"; sh "$(FRAMEWORK_ROOT)/ci/provisioning/fetch-crs.sh"; sh "$(FRAMEWORK_ROOT)/ci/provisioning/prepare-crs.sh"; MODSECURITY_RULE_PREAMBLE_FILE="$$CRS_RUNTIME_DIR/modsecurity-crs-preamble.conf"; RESULTS_DIR="$$BUILD_ROOT/results/with-crs"; export MODSECURITY_RULE_PREAMBLE_FILE RESULTS_DIR; CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-connector-smokes.sh"')

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
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" sh "$(FRAMEWORK_ROOT)/ci/runtime/run-runtime-matrix.sh"

runtime-matrix-all: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FORCE_ALL_CASES=1 sh "$(FRAMEWORK_ROOT)/ci/runtime/run-runtime-matrix.sh")

runtime-matrix-all-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FORCE_ALL_CASES=1 sh "$(FRAMEWORK_ROOT)/ci/runtime/run-runtime-matrix.sh"

runtime-matrix-haproxy: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" HAPROXY_MATRIX_VARIANT=all sh "$(FRAMEWORK_ROOT)/ci/runtime/run-haproxy-runtime-matrix.sh"

full-mrts-runtime-matrix: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime/lifecycle/run-full-mrts-runtime-matrix.sh)

mrts-only-full-run: full-mrts-runtime-matrix

full-runtime-matrix: full-matrix-parallel

full-matrix-parallel: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime/lifecycle/run-full-matrix-parallel.sh)

full-matrix-parallel-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime/lifecycle/run-full-matrix-parallel.sh

full-matrix-single-job-runtime: check-framework prepare-runtime-components
	@test -n "$(CONNECTOR)" || { echo "CONNECTOR is required, e.g. CONNECTOR=nginx"; exit 2; }
	@test -n "$(CRS)" || { echo "CRS is required, e.g. CRS=with-crs"; exit 2; }
	@test -n "$(MRTS)" || { echo "MRTS is required, e.g. MRTS=with-mrts"; exit 2; }
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-full-matrix-job.py --connector "$(CONNECTOR)" --crs "$(CRS)" --mrts "$(MRTS)" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --timeout-seconds "$(VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS)"

full-matrix-resume-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" "$(FRAMEWORK_PYTHON)" ci/runtime/lifecycle/run-full-matrix-resume.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --job-timeout-seconds "$(VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS)" --total-timeout-seconds "$(VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS)"

generate-full-runtime-matrix: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-full-runtime-matrix.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --log-root "$(LOG_ROOT)"

generate-full-matrix-job-completeness: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-full-matrix-job-completeness.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest" --rewrite-manifest

generate-nginx-mrts-http500-cluster-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --output-dir "$(CURDIR)/reports/testing/generated/manifest"

generate-work-queue: check-framework
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/reporting/generate-connector-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/canonical/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/reporting/generate-phase-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --connector-work-queue "$(CURDIR)/reports/testing/generated/work-queues/connector-work-queue.generated.json" --phase-coverage "$(CURDIR)/reports/testing/generated/coverage/phase-coverage.generated.md" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/canonical/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-phase4-hard-abort-capability.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-intervention-blocking-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-body-processor-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-rule-chain-semantics-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-final-consistency-audit.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-phase-work-queue: check-framework
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/reporting/generate-phase-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --connector-work-queue "$(CURDIR)/reports/testing/generated/work-queues/connector-work-queue.generated.json" --phase-coverage "$(CURDIR)/reports/testing/generated/coverage/phase-coverage.generated.md" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/canonical/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-phase4-hard-abort-capability.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-intervention-blocking-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-body-processor-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-rule-chain-semantics-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-final-consistency-audit.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-nolog-audit-evidence-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-response-header-hook-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-phase4-hard-abort-capability: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-phase4-hard-abort-capability.py --connector-root "$(CURDIR)"

generate-intervention-blocking-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-intervention-blocking-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-no-mrts-intervention-nomatch-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-body-processor-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-body-processor-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-rule-chain-semantics-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-rule-chain-semantics-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-final-consistency-audit: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-final-consistency-audit.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-remaining-failure-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/evidence/reports/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"

mrts-native-full-run: check-framework prepare-runtime-components
	$(call RUN_WITH_REFRESH_ALL,$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime/lifecycle/run-mrts-native-full.sh)

mrts-native-full-run-runtime: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime/lifecycle/run-mrts-native-full.sh

mrts-native-apache-full: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env MRTS_NATIVE_TARGETS=apache2_ubuntu PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime/lifecycle/run-mrts-native-full.sh

mrts-native-nginx-pr24-full: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env MRTS_NATIVE_TARGETS=nginx-pr24 PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/runtime/lifecycle/run-mrts-native-full.sh

mrts-upstream-infra-check: check-framework
	@sh -eu -c ' \
		MRTS_ROOT="$${MRTS_ROOT:-$(FRAMEWORK_ROOT)/tools/MRTS}"; \
		test -d "$$MRTS_ROOT/config_infra/apache2_ubuntu" || { echo "BLOCKED: missing $$MRTS_ROOT/config_infra/apache2_ubuntu"; exit 77; }; \
		test -d "$(FRAMEWORK_ROOT)/tests/mrts/infra-overlays/nginx-pr24" || { echo "BLOCKED: missing Framework NGINX PR24 overlay"; exit 77; }; \
		test -f "$(FRAMEWORK_ROOT)/tests/mrts/infra-overlays/nginx-pr24/metadata.yaml" || { echo "BLOCKED: missing NGINX PR24 overlay metadata"; exit 77; }; \
		echo "MRTS upstream/native infrastructure inputs present"; \
	'

test-haproxy-no-crs: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" HAPROXY_MATRIX_VARIANT=no-crs sh "$(FRAMEWORK_ROOT)/ci/runtime/run-haproxy-runtime-matrix.sh"

test-haproxy-with-crs: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" HAPROXY_MATRIX_VARIANT=with-crs sh "$(FRAMEWORK_ROOT)/ci/runtime/run-haproxy-runtime-matrix.sh"

probe-response-body: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" sh "$(FRAMEWORK_ROOT)/ci/runtime/probe-response-body-blocking.sh"

connector-starter-checks: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env SOURCE_ROOT="$(SOURCE_ROOT)" BUILD_ROOT="$(BUILD_ROOT)" TMP_ROOT="$(TMP_ROOT)" LOG_ROOT="$(LOG_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh "$(FRAMEWORK_ROOT)/ci/runtime/run-connector-starter-checks.sh"

# Canonical connector stages. These targets deliberately keep build,
# configuration loading, request-free startup, runtime traffic, and the
# capability-driven no-CRS baseline as separate invocations.
build-apache build-nginx build-haproxy build-envoy build-traefik build-lighttpd: build-%: check-framework
	sh ci/runtime/lifecycle/run-connector-stage.sh "$*" build

check-config-apache check-config-nginx check-config-haproxy check-config-envoy check-config-traefik check-config-lighttpd: check-config-%: check-framework
	sh ci/runtime/lifecycle/run-connector-stage.sh "$*" config_load

start-smoke-apache start-smoke-nginx start-smoke-haproxy: start-smoke-%: check-framework
	sh ci/runtime/lifecycle/run-connector-stage.sh "$*" start_smoke

runtime-smoke-apache runtime-smoke-nginx runtime-smoke-haproxy: runtime-smoke-%: check-framework
	EVIDENCE_ROOT="$(RUNTIME_EVIDENCE_ROOT)" sh ci/runtime/lifecycle/run-no-crs-baseline.sh "$*" minimal_runtime_smoke

capabilities-apache capabilities-nginx capabilities-haproxy capabilities-envoy capabilities-traefik capabilities-lighttpd: capabilities-%: check-framework
	@run_id="$${NO_CRS_RUN_ID:-$(DEFAULT_VERIFIED_RUN_ID)}"; \
	case "$$run_id" in [A-Za-z0-9]*) ;; *) echo "FAIL: unsafe capability-plan run id: $$run_id" >&2; exit 1 ;; esac; \
	case "$$run_id" in *[!A-Za-z0-9._-]*) echo "FAIL: unsafe capability-plan run id: $$run_id" >&2; exit 1 ;; esac; \
	[ "$${#run_id}" -le 128 ] || { echo "FAIL: capability-plan run id is too long" >&2; exit 1; }; \
	run_dir="$(CAPABILITY_PLAN_ROOT)/$*/$$run_id"; \
	mkdir -p "$$run_dir"; \
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/checks/catalog/no_crs_baseline.py" select \
		--connector "$*" \
		--capabilities "connectors/$*/capabilities.json" \
		--output "$$run_dir/plan.json"

no-crs-baseline-apache no-crs-baseline-nginx no-crs-baseline-haproxy no-crs-baseline-envoy no-crs-baseline-traefik no-crs-baseline-lighttpd: no-crs-baseline-%: check-framework
	sh ci/runtime/lifecycle/run-no-crs-baseline.sh "$*"

# The strict profile requires the complete canonical artifact set, including
# sanitized host logs.  Every target carries an explicit selected host profile
# and target identity into the run manifest.  In particular, the four legacy
# compatibility routes below can no longer be mislabeled as full-lifecycle
# evidence merely because they share a connector name.
full-lifecycle-apache: check-framework
	NO_CRS_ARTIFACT_PROFILE=full_lifecycle FULL_LIFECYCLE_HOST_PROFILE=native-httpd-module FULL_LIFECYCLE_EXECUTED_TARGET=full-lifecycle-apache sh ci/runtime/lifecycle/run-no-crs-baseline.sh apache no_crs_baseline

full-lifecycle-nginx: check-framework
	NO_CRS_ARTIFACT_PROFILE=full_lifecycle FULL_LIFECYCLE_HOST_PROFILE=native-nginx-http-module FULL_LIFECYCLE_EXECUTED_TARGET=full-lifecycle-nginx sh ci/runtime/lifecycle/run-no-crs-baseline.sh nginx no_crs_baseline

full-lifecycle-haproxy-htx: check-framework
	NO_CRS_ARTIFACT_PROFILE=full_lifecycle FULL_LIFECYCLE_HOST_PROFILE=native-htx-filter FULL_LIFECYCLE_EXECUTED_TARGET=full-lifecycle-haproxy-htx sh ci/runtime/lifecycle/run-no-crs-baseline.sh haproxy no_crs_baseline

full-lifecycle-envoy-ext-proc: check-framework
	NO_CRS_ARTIFACT_PROFILE=full_lifecycle FULL_LIFECYCLE_HOST_PROFILE=ext_proc FULL_LIFECYCLE_EXECUTED_TARGET=full-lifecycle-envoy-ext-proc sh ci/runtime/lifecycle/run-no-crs-baseline.sh envoy no_crs_baseline

full-lifecycle-traefik-native: check-framework
	NO_CRS_ARTIFACT_PROFILE=full_lifecycle FULL_LIFECYCLE_HOST_PROFILE=native-middleware FULL_LIFECYCLE_EXECUTED_TARGET=full-lifecycle-traefik-native sh ci/runtime/lifecycle/run-no-crs-baseline.sh traefik no_crs_baseline

full-lifecycle-lighttpd-patched: check-framework
	NO_CRS_ARTIFACT_PROFILE=full_lifecycle FULL_LIFECYCLE_HOST_PROFILE=patched-native FULL_LIFECYCLE_EXECUTED_TARGET=full-lifecycle-lighttpd-patched sh ci/runtime/lifecycle/run-no-crs-baseline.sh lighttpd no_crs_baseline

# Preserve the historical user-facing names, but route them only to their
# selected native profile.  Compatibility smoke remains under runtime-smoke-*
# and no-crs-baseline-* and is never full-lifecycle evidence.
full-lifecycle-haproxy: full-lifecycle-haproxy-htx
full-lifecycle-envoy: full-lifecycle-envoy-ext-proc
full-lifecycle-traefik: full-lifecycle-traefik-native
full-lifecycle-lighttpd: full-lifecycle-lighttpd-patched

full-lifecycle-all-connectors: check-framework
	NO_CRS_ARTIFACT_PROFILE=full_lifecycle sh ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh

evidence-check-apache evidence-check-nginx evidence-check-haproxy evidence-check-envoy evidence-check-traefik evidence-check-lighttpd: evidence-check-%: check-framework
	@run_id="$(NO_CRS_RUN_ID)"; \
	if [ -z "$$run_id" ]; then \
		latest="$(EVIDENCE_ROOT)/$*/latest-run-id"; \
		[ -f "$$latest" ] || { echo "FAIL: no latest canonical run for $*: $$latest" >&2; exit 1; }; \
		IFS= read -r run_id < "$$latest"; \
	fi; \
	[ -n "$$run_id" ] || { echo "FAIL: empty canonical run id for $*" >&2; exit 1; }; \
	case "$$run_id" in [A-Za-z0-9]*) ;; *) echo "FAIL: unsafe canonical run id for $*: $$run_id" >&2; exit 1 ;; esac; \
	case "$$run_id" in *[!A-Za-z0-9._-]*) echo "FAIL: unsafe canonical run id for $*: $$run_id" >&2; exit 1 ;; esac; \
	[ "$${#run_id}" -le 128 ] || { echo "FAIL: canonical run id is too long for $*" >&2; exit 1; }; \
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/checks/catalog/no_crs_baseline.py" validate \
		--evidence-root "$(EVIDENCE_ROOT)/$*/$$run_id" \
		--connector "$*" \
		--check all

build-all-connectors: check-framework
	@status=0; blocked=0; \
	for connector in $(NO_CRS_CONNECTORS); do \
		sh ci/runtime/lifecycle/run-connector-stage.sh "$$connector" build || { rc=$$?; if [ "$$rc" -eq 77 ]; then blocked=1; else status=1; fi; }; \
	done; \
	[ "$$status" -eq 0 ] || exit 1; \
	[ "$$blocked" -eq 0 ] || exit 77

check-config-all-connectors: check-framework
	@status=0; blocked=0; \
	for connector in $(NO_CRS_CONNECTORS); do \
		sh ci/runtime/lifecycle/run-connector-stage.sh "$$connector" config_load || { rc=$$?; if [ "$$rc" -eq 77 ]; then blocked=1; else status=1; fi; }; \
	done; \
	[ "$$status" -eq 0 ] || exit 1; \
	[ "$$blocked" -eq 0 ] || exit 77

start-smoke-all-connectors: check-framework
	@status=0; blocked=0; \
	for connector in $(NO_CRS_CONNECTORS); do \
		sh ci/runtime/lifecycle/run-connector-stage.sh "$$connector" start_smoke || { rc=$$?; if [ "$$rc" -eq 77 ]; then blocked=1; else status=1; fi; }; \
	done; \
	[ "$$status" -eq 0 ] || exit 1; \
	[ "$$blocked" -eq 0 ] || exit 77

runtime-smoke-all-connectors: check-framework
	@status=0; blocked=0; run_id="$(NO_CRS_RUN_ID)"; \
	if [ -z "$$run_id" ]; then run_id="$$(date -u +%Y-%m-%dT%H-%M-%SZ)-$$(git rev-parse --short=8 HEAD 2>/dev/null || printf unknown)"; fi; \
	for connector in $(NO_CRS_CONNECTORS); do \
		NO_CRS_RUN_ID="$$run_id" EVIDENCE_ROOT="$(RUNTIME_EVIDENCE_ROOT)" sh ci/runtime/lifecycle/run-no-crs-baseline.sh "$$connector" minimal_runtime_smoke || { rc=$$?; if [ "$$rc" -eq 77 ]; then blocked=1; else status=1; fi; }; \
	done; \
	[ "$$status" -eq 0 ] || exit 1; \
	[ "$$blocked" -eq 0 ] || exit 77

no-crs-baseline-all-connectors: check-framework
	@status=0; blocked=0; run_id="$(NO_CRS_RUN_ID)"; \
	if [ -z "$$run_id" ]; then run_id="$$(date -u +%Y-%m-%dT%H-%M-%SZ)-$$(git rev-parse --short=8 HEAD 2>/dev/null || printf unknown)"; fi; \
	for connector in $(NO_CRS_CONNECTORS); do \
		NO_CRS_RUN_ID="$$run_id" sh ci/runtime/lifecycle/run-no-crs-baseline.sh "$$connector" || { rc=$$?; if [ "$$rc" -eq 77 ]; then blocked=1; else status=1; fi; }; \
	done; \
	[ "$$status" -eq 0 ] || exit 1; \
	[ "$$blocked" -eq 0 ] || exit 77

capabilities-all-connectors: capabilities-apache capabilities-nginx capabilities-haproxy capabilities-envoy capabilities-traefik capabilities-lighttpd
	"$(PYTHON)" ci/evidence/collectors/connector_capabilities.py check
	"$(PYTHON)" ci/evidence/collectors/connector_capabilities.py generate \
		--output-dir "$(CURDIR)/reports/testing/generated/canonical"

# Keep the checked-in catalog source-contract-only.  This separate target
# renders a disposable report view from one explicit, fully validated current
# canonical No-CRS run, so local/stale latest-run-id files are never selected.
capabilities-all-connectors-evidence: check-framework
	@run_id="$(CAPABILITY_REPORT_RUN_ID)"; \
	[ -n "$$run_id" ] || { echo "FAIL: CAPABILITY_REPORT_RUN_ID (or NO_CRS_RUN_ID) is required" >&2; exit 1; }; \
	"$(PYTHON)" ci/evidence/collectors/connector_capabilities.py check; \
	"$(PYTHON)" ci/evidence/collectors/connector_capabilities.py generate \
		--evidence-root "$(CAPABILITY_REPORT_EVIDENCE_ROOT)" \
		--run-id "$$run_id" \
		--output-dir "$(CAPABILITY_REPORT_OUTPUT_DIR)"

evidence-check-all-connectors: evidence-check-apache evidence-check-nginx evidence-check-haproxy evidence-check-envoy evidence-check-traefik evidence-check-lighttpd

define RUN_NO_CRS_EVIDENCE_CHECK
	@set -eu; \
	for connector in $(NO_CRS_CONNECTORS); do \
		run_id="$(NO_CRS_RUN_ID)"; \
		if [ -z "$$run_id" ]; then \
			latest="$(EVIDENCE_ROOT)/$$connector/latest-run-id"; \
			[ -f "$$latest" ] || { echo "FAIL: no latest canonical run for $$connector: $$latest" >&2; exit 1; }; \
			IFS= read -r run_id < "$$latest"; \
		fi; \
		[ -n "$$run_id" ] || { echo "FAIL: empty canonical run id for $$connector" >&2; exit 1; }; \
		case "$$run_id" in [A-Za-z0-9]*) ;; *) echo "FAIL: unsafe canonical run id for $$connector: $$run_id" >&2; exit 1 ;; esac; \
		case "$$run_id" in *[!A-Za-z0-9._-]*) echo "FAIL: unsafe canonical run id for $$connector: $$run_id" >&2; exit 1 ;; esac; \
		[ "$${#run_id}" -le 128 ] || { echo "FAIL: canonical run id is too long for $$connector" >&2; exit 1; }; \
		"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/checks/catalog/no_crs_baseline.py" validate \
			--evidence-root "$(EVIDENCE_ROOT)/$$connector/$$run_id" \
			--connector "$$connector" --check $(1); \
	done
endef

check-no-crs-result-schema: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,schema)

check-no-crs-evidence-completeness: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,completeness)

check-no-crs-capability-consistency: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,capability)

check-no-crs-claim-policy: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,claim-policy)

check-no-crs-artifact-layout: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,layout)

check-no-crs-body-payload-absence: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,body-payload)

check-no-crs-protocol-client: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,protocol-client)

check-no-crs-status-consistency: check-framework
	$(call RUN_NO_CRS_EVIDENCE_CHECK,status)

define RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK
	@set -eu; \
	for connector in $(NO_CRS_CONNECTORS); do \
		"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/checks/evidence/check_full_lifecycle_evidence.py" \
			--run-dir "$(EVIDENCE_ROOT)/$$connector/$(NO_CRS_RUN_ID)" --check $(1); \
	done; \
	"$(PYTHON)" ci/checks/evidence/check-full-lifecycle-evidence.py \
		--connector-root "$(CURDIR)" --evidence-root "$(EVIDENCE_ROOT)" \
		--run-id "$(NO_CRS_RUN_ID)" --check profile --connectors $(NO_CRS_CONNECTORS)
endef

# Transport sidecars are inventory only until a case is promoted.  The
# Framework's dedicated checker is nevertheless always part of the selected
# full-lifecycle promotion gate, so a future PASS cannot bypass its causal
# event/observation/lifecycle correlation requirements.
define RUN_TRANSPORT_HARDENING_EVIDENCE_CHECK
	@set -eu; \
	for connector in $(NO_CRS_CONNECTORS); do \
		$(MAKE) -C "$(FRAMEWORK_ROOT)" check-transport-hardening-evidence \
			PYTHON="$(FRAMEWORK_PYTHON)" \
			CONNECTOR="$$connector" \
			NO_CRS_RUN_DIR="$(EVIDENCE_ROOT)/$$connector/$(NO_CRS_RUN_ID)"; \
	done
endef

check-first-byte-before-response-end: check-framework
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(call RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK,first-byte)

check-no-full-response-buffering: check-framework
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(call RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK,no-full-response-buffering)

check-full-lifecycle-event-privacy: check-framework
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(call RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK,event-privacy)

check-full-lifecycle-transport: check-framework
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(PYTHON) ci/checks/evidence/check-full-lifecycle-evidence.py \
		--connector-root "$(CURDIR)" --evidence-root "$(EVIDENCE_ROOT)" \
		--run-id "$(NO_CRS_RUN_ID)" --check transport --connectors $(NO_CRS_CONNECTORS)
	$(call RUN_TRANSPORT_HARDENING_EVIDENCE_CHECK)

check-full-lifecycle-lifecycle: check-framework
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(PYTHON) ci/checks/evidence/check-full-lifecycle-evidence.py \
		--connector-root "$(CURDIR)" --evidence-root "$(EVIDENCE_ROOT)" \
		--run-id "$(NO_CRS_RUN_ID)" --check lifecycle --connectors $(NO_CRS_CONNECTORS)

check-full-lifecycle-transport-hardening: check-framework
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(call RUN_TRANSPORT_HARDENING_EVIDENCE_CHECK)

check-full-lifecycle-promotion: check-framework
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(call RUN_STRICT_FULL_LIFECYCLE_EVIDENCE_CHECK,promotion)
	$(call RUN_TRANSPORT_HARDENING_EVIDENCE_CHECK)

# Read-only compact acceptance gate.  It consumes one already finalized
# canonical run and cannot change capability manifests or case outcomes.
check-six-connector-core-completion:
	@test -n "$(NO_CRS_RUN_ID)" || { echo "NO_CRS_RUN_ID is required" >&2; exit 2; }
	$(PYTHON) ci/checks/evidence/check-six-connector-core-completion.py \
		--connector-root "$(CURDIR)" --evidence-root "$(EVIDENCE_ROOT)" \
		--run-id "$(NO_CRS_RUN_ID)"

check-no-crs-doc-consistency:
	"$(PYTHON)" ci/checks/documentation/check-no-crs-doc-consistency.py

check-no-crs-source-normalization:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" -m unittest -v \
		tests.test_collect_no_crs_source \
		tests.test_full_lifecycle_evidence \
		tests.test_prepare_runtime_components \
		tests.test_runtime_component_cache_identity

.PHONY: check-apache-common-adoption check-apache-c-standard-wiring check-apache-c-standards check-apache-c17 check-apache-c17-lint check-apache-c23 check-apache-future-c check-apache-c20 check-apache-c26 check-apache-request-transaction-cleanup check-apache-request-transaction-cleanup-lint check-optional-prerequisite-status check-nginx-common-adoption check-nginx-c-standard-wiring check-nginx-c-standards check-nginx-c17 check-nginx-c17-lint check-nginx-c23 check-nginx-future-c check-nginx-c20 check-nginx-c26 check-haproxy-common-adoption check-haproxy-c-standard-wiring check-haproxy-c-standards check-haproxy-c17 check-haproxy-c17-lint check-haproxy-c23 check-haproxy-future-c check-haproxy-c20 check-haproxy-c26 check-haproxy-htx-overlay check-common-helpers check-common-helpers-c17 check-common-helpers-c23 check-common-helpers-future-c check-common-helpers-c20 check-common-helpers-c26 check-common-sdk-contract check-common-security-contract check-common-memory-safety check-common-flow-integrity check-adapter-contracts check-directive-parity check-remaining-connectors-common-adoption check-envoy-common-adoption check-traefik-common-adoption check-lighttpd-common-adoption check-remaining-connectors-host-integration check-remaining-connectors-build-wiring check-remaining-connectors-start-wiring check-remaining-connectors-claim-policy check-remaining-connectors-c-standard-wiring check-remaining-connectors-c-standards check-remaining-connectors-c17 check-remaining-connectors-c17-lint check-remaining-connectors-c23 check-remaining-connectors-future-c check-block-status-generator build-envoy-connector check-envoy-config start-smoke-envoy runtime-smoke-envoy build-traefik-connector check-traefik-config start-smoke-traefik runtime-smoke-traefik build-lighttpd-connector build-lighttpd-bridge self-test-lighttpd-bridge check-lighttpd-config start-smoke-lighttpd runtime-smoke-lighttpd build-remaining-connectors start-smoke-remaining-connectors runtime-smoke-remaining-connectors readiness-remaining-connectors

build-envoy-connector:
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh envoy build-envoy-connector

check-envoy-config: build-envoy-connector
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh envoy check-envoy-config

start-smoke-envoy: check-framework
	sh ci/runtime/lifecycle/run-connector-stage.sh envoy start_smoke

runtime-smoke-envoy: check-framework
	EVIDENCE_ROOT="$(RUNTIME_EVIDENCE_ROOT)" sh ci/runtime/lifecycle/run-no-crs-baseline.sh envoy minimal_runtime_smoke

build-traefik-connector:
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh traefik build-traefik-connector

check-traefik-config: build-traefik-connector
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh traefik check-traefik-config

start-smoke-traefik: check-framework
	sh ci/runtime/lifecycle/run-connector-stage.sh traefik start_smoke

runtime-smoke-traefik: check-framework
	EVIDENCE_ROOT="$(RUNTIME_EVIDENCE_ROOT)" sh ci/runtime/lifecycle/run-no-crs-baseline.sh traefik minimal_runtime_smoke

build-lighttpd-connector:
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh lighttpd build-lighttpd-connector

build-lighttpd-bridge:
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh lighttpd build-lighttpd-bridge

self-test-lighttpd-bridge: build-lighttpd-bridge
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh lighttpd self-test-lighttpd-bridge

check-lighttpd-config: build-lighttpd-connector
	sh ci/runtime/lifecycle/run-remaining-connector-target.sh lighttpd check-lighttpd-config

start-smoke-lighttpd: check-framework
	sh ci/runtime/lifecycle/run-connector-stage.sh lighttpd start_smoke

runtime-smoke-lighttpd: check-framework
	EVIDENCE_ROOT="$(RUNTIME_EVIDENCE_ROOT)" sh ci/runtime/lifecycle/run-no-crs-baseline.sh lighttpd minimal_runtime_smoke

build-remaining-connectors: build-envoy-connector build-traefik-connector build-lighttpd-connector

start-smoke-remaining-connectors: start-smoke-envoy start-smoke-traefik start-smoke-lighttpd

runtime-smoke-remaining-connectors: runtime-smoke-envoy runtime-smoke-traefik runtime-smoke-lighttpd

readiness-remaining-connectors: check-envoy-common-adoption check-traefik-common-adoption check-lighttpd-common-adoption check-remaining-connectors-host-integration check-remaining-connectors-build-wiring check-remaining-connectors-start-wiring check-remaining-connectors-claim-policy
	$(PYTHON) ci/checks/documentation/check-bilingual-docs.py

check-remaining-connectors-common-adoption:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-common-adoption.py

check-envoy-common-adoption:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-common-adoption.py --connector envoy

check-traefik-common-adoption:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-common-adoption.py --connector traefik

check-lighttpd-common-adoption:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-common-adoption.py --connector lighttpd

check-remaining-connectors-host-integration:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-host-integration.py

check-remaining-connectors-build-wiring:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-build-wiring.py

check-remaining-connectors-start-wiring:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-start-wiring.py

check-remaining-connectors-claim-policy:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-claim-policy.py

check-remaining-connectors-c-standard-wiring:
	$(PYTHON) ci/checks/connectors/all/check-remaining-connectors-c-standard-wiring.py

check-remaining-connectors-c-standards:
	sh ci/checks/connectors/all/check-remaining-connectors-c-standards.sh

check-remaining-connectors-c17:
	CONNECTOR_C_STD_PROFILE=c17 sh ci/checks/connectors/all/check-remaining-connectors-c-standards.sh

check-remaining-connectors-c17-lint:
	@CONNECTOR_C_STD_PROFILE=c17 sh ci/checks/connectors/all/check-remaining-connectors-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: remaining connector C17 check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-remaining-connectors-c23:
	CONNECTOR_C_STD_PROFILE=c23 sh ci/checks/connectors/all/check-remaining-connectors-c-standards.sh

check-remaining-connectors-future-c:
	CONNECTOR_C_STD_PROFILE=c2y sh ci/checks/connectors/all/check-remaining-connectors-c-standards.sh

check-block-status-generator:
	$(PYTHON) ci/checks/common/check-block-status-generator.py

check-apache-common-adoption:
	$(PYTHON) ci/checks/connectors/apache/check-apache-common-adoption.py

check-apache-c-standard-wiring:
	$(PYTHON) ci/checks/connectors/apache/check-apache-c-standard-wiring.py

check-apache-c-standards:
	sh ci/checks/connectors/apache/check-apache-c-standards.sh

check-apache-c17:
	APACHE_C_STD_PROFILE=c17 sh ci/checks/connectors/apache/check-apache-c-standards.sh

check-apache-c17-lint:
	@APACHE_C_STD_PROFILE=c17 sh ci/checks/connectors/apache/check-apache-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: apache C17 compile check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-apache-request-transaction-cleanup:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" -m unittest -v tests.test_apache_request_transaction_cleanup
	sh ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh

check-apache-request-transaction-cleanup-lint:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" -m unittest -v tests.test_apache_request_transaction_cleanup
	"$(PYTHON)" ci/tools/run-check-status.py --check apache_request_transaction_cleanup --allow-blocked-reason apache_development_prerequisite --blocked-if-missing-apache-development -- sh ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh

check-optional-prerequisite-status:
	PYTHONDONTWRITEBYTECODE=1 "$(PYTHON)" -m unittest -v tests.test_optional_prerequisite_status

check-apache-c23:
	APACHE_C_STD_PROFILE=c23 sh ci/checks/connectors/apache/check-apache-c-standards.sh

check-apache-future-c:
	APACHE_C_STD_PROFILE=c2y sh ci/checks/connectors/apache/check-apache-c-standards.sh

check-apache-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-apache-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-nginx-common-adoption:
	$(PYTHON) ci/checks/connectors/nginx/check-nginx-common-adoption.py

check-nginx-c-standard-wiring:
	$(PYTHON) ci/checks/connectors/nginx/check-nginx-c-standard-wiring.py

check-nginx-c-standards:
	sh ci/checks/connectors/nginx/check-nginx-c-standards.sh

check-nginx-c17:
	NGINX_C_STD_PROFILE=c17 sh ci/checks/connectors/nginx/check-nginx-c-standards.sh

check-nginx-c17-lint:
	@NGINX_C_STD_PROFILE=c17 sh ci/checks/connectors/nginx/check-nginx-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: nginx C17 compile check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-nginx-c23:
	NGINX_C_STD_PROFILE=c23 sh ci/checks/connectors/nginx/check-nginx-c-standards.sh

check-nginx-future-c:
	NGINX_C_STD_PROFILE=c2y sh ci/checks/connectors/nginx/check-nginx-c-standards.sh

check-nginx-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-nginx-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-haproxy-common-adoption:
	$(PYTHON) ci/checks/connectors/haproxy/check-haproxy-common-adoption.py

check-haproxy-c-standard-wiring:
	$(PYTHON) ci/checks/connectors/haproxy/check-haproxy-c-standard-wiring.py

check-haproxy-c-standards:
	sh ci/checks/connectors/haproxy/check-haproxy-c-standards.sh

check-haproxy-htx-overlay:
	$(MAKE) -C connectors/haproxy check-htx-overlay

check-haproxy-c17:
	HAPROXY_C_STD_PROFILE=c17 sh ci/checks/connectors/haproxy/check-haproxy-c-standards.sh

check-haproxy-c17-lint:
	@HAPROXY_C_STD_PROFILE=c17 sh ci/checks/connectors/haproxy/check-haproxy-c-standards.sh || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: haproxy C17 compile check blocked in lint environment"; exit 0; fi; exit "$$rc"; }

check-haproxy-c23:
	HAPROXY_C_STD_PROFILE=c23 sh ci/checks/connectors/haproxy/check-haproxy-c-standards.sh

check-haproxy-future-c:
	HAPROXY_C_STD_PROFILE=c2y sh ci/checks/connectors/haproxy/check-haproxy-c-standards.sh

check-haproxy-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-haproxy-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-common-helpers:
	MSCONNECTOR_C_STD="$(MSCONNECTOR_C_STD)" MSCONNECTOR_CFLAGS="$(MSCONNECTOR_CFLAGS)" sh ci/checks/common/check-common-helpers.sh

check-common-helpers-c17:
	$(MAKE) check-common-helpers MSCONNECTOR_C_STD=c17

check-common-helpers-c23:
	@flag="$$(python3 ci/provisioning/toolchains/detect-c-standard.py --profile c23 --compiler "$(MSCONNECTOR_COMPILER_ID)")" || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: optional C23 check — compiler does not support c23 or c2x"; exit 0; fi; exit "$$rc"; }; \
	$(MAKE) check-common-helpers CC="$(MSCONNECTOR_COMPILER_ID)" MSCONNECTOR_C_STD=c23 MSCONNECTOR_CFLAGS="$$flag -Wall -Wextra -Werror"

check-common-helpers-future-c:
	@flag="$$(python3 ci/provisioning/toolchains/detect-c-standard.py --profile c2y --compiler "$(MSCONNECTOR_COMPILER_ID)")" || { rc="$$?"; if [ "$$rc" = "77" ]; then echo "SKIPPED: optional future C check — compiler does not support c2y or gnu2y"; exit 0; fi; exit "$$rc"; }; \
	$(MAKE) check-common-helpers CC="$(MSCONNECTOR_COMPILER_ID)" MSCONNECTOR_C_STD=c2y MSCONNECTOR_CFLAGS="$$flag -Wall -Wextra -Werror"

check-common-helpers-c20:
	@echo "SKIPPED: c20 is not a C standard mode; use c23/c2x for C or c++20 for C++."

check-common-helpers-c26:
	@echo "SKIPPED: c26 is not a C standard mode; use c2y/gnu2y for future C or c++26 for C++."

check-common-sdk-contract:
	$(PYTHON) ci/checks/common/check-common-sdk-contract.py

check-common-security-contract:
	$(PYTHON) ci/checks/common/check-common-security-contract.py

check-common-memory-safety:
	sh ci/checks/common/check-common-memory-safety.sh

check-common-flow-integrity:
	$(PYTHON) ci/checks/common/check-common-flow-integrity.py

check-adapter-contracts:
	$(PYTHON) ci/checks/common/check-adapter-contracts.py

check-directive-parity:
	$(PYTHON) ci/checks/common/check-directive-parity.py

lint: check-framework
	find ci -type f -name '*.sh' -print0 | xargs -0 -r sh -n
	find connectors/envoy connectors/traefik connectors/lighttpd -type f -name '*.sh' -exec sh -n {} +
	if command -v bash >/dev/null 2>&1; then find ci -type f -name '*.sh' -print0 | xargs -0 -r bash -n; find connectors/envoy connectors/traefik connectors/lighttpd -type f -name '*.sh' -exec bash -n {} +; else echo "bash unavailable"; fi
	find ci -type f -name '*.py' -print0 | xargs -0 -r env PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile
	$(MAKE) check-no-crs-source-normalization
	$(MAKE) check-apache-common-adoption
	$(MAKE) check-apache-c-standard-wiring
	$(MAKE) check-apache-c17-lint
	$(MAKE) check-apache-request-transaction-cleanup-lint
	$(MAKE) check-optional-prerequisite-status
	$(MAKE) check-nginx-common-adoption
	$(MAKE) check-nginx-c-standard-wiring
	$(MAKE) check-nginx-c17-lint
	$(MAKE) check-haproxy-common-adoption
	$(MAKE) check-haproxy-c-standard-wiring
	$(MAKE) check-haproxy-c17-lint
	$(MAKE) check-haproxy-htx-overlay
	$(MAKE) check-remaining-connectors-common-adoption
	$(MAKE) check-remaining-connectors-host-integration
	$(MAKE) check-remaining-connectors-build-wiring
	$(MAKE) check-remaining-connectors-start-wiring
	$(MAKE) check-remaining-connectors-claim-policy
	"$(PYTHON)" ci/evidence/collectors/connector_capabilities.py check
	"$(PYTHON)" ci/checks/documentation/check-no-crs-doc-consistency.py
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/checks/catalog/no_crs_baseline.py" catalog-check
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
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/tools/check-python-deps.py"
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/checks/documentation/check-workflow-yaml.py"
	$(MAKE) check-doc-links
	$(MAKE) check-bilingual-docs
	$(MAKE) check-variable-documentation
	$(MAKE) check-compiler-guides
	$(MAKE) check-connector-config-reference
	sh "$(FRAMEWORK_ROOT)/ci/checks/catalog/check-crs-version-pinning.sh"
	sh ci/checks/common/check-common-helpers.sh
	sh ci/checks/common/check-adapter-helpers.sh
	sh ci/checks/common/check-adapter-metadata-drift.sh
	if command -v actionlint >/dev/null 2>&1; then actionlint .github/workflows/*.yml; else echo "actionlint unavailable"; fi
	git diff --check

summary: check-framework
	$(PYTHON) "$(FRAMEWORK_ROOT)/ci/reporting/summarize-results.py" "$(BUILD_ROOT)/results/connector-summary.json"

case-matrix: generate-test-matrix
	@echo "case matrix: reports/testing/generated/coverage/case-matrix.generated.md"

install-dev-deps: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/tools/bootstrap-python.sh"

setup-dev: install-dev-deps
	@echo "setup-dev: using PYTHON=$(PYTHON)"
	@echo "setup-dev: test framework -> $(FRAMEWORK_ROOT)"
	@echo "setup-dev: next steps -> make lint; make fetch-deps; make doctor; make smoke-all"

fetch-modsecurity-v3: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/provisioning/fetch-smoke-sources.sh" v3

fetch-deps bootstrap-runtime: prepare-runtime-components
	@echo "fetch-deps: runtime components prepared in CONNECTOR_COMPONENT_CACHE=$${CONNECTOR_COMPONENT_CACHE:-auto}"

fetch-crs: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/provisioning/fetch-crs.sh"

prepare-crs: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/provisioning/prepare-crs.sh"

doctor env-check: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/tools/doctor.sh"

print-python:
	@echo "make: using PYTHON=$(PYTHON)"

bootstrap-all: setup-dev fetch-deps doctor
	@echo "bootstrap-all complete (smoke not run)"

quick-check codex-check: lint
	find "$(FRAMEWORK_ROOT)"/tests/normalizers "$(FRAMEWORK_ROOT)"/tests/runners "$(FRAMEWORK_ROOT)"/ci -type f -name '*.py' -print0 | xargs -0 -r env PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile
	git diff --check

smoke-installed installed-readiness: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/runtime/smoke-installed.sh"

doctor-install-hints:
	@echo "Install hints (Debian/Ubuntu example):"
	@echo "  sudo apt-get update"
	@echo "  sudo apt-get install -y git make gcc clang autoconf automake libtool pkg-config apache2-dev nginx libmodsecurity-dev"
	@echo "Install hints (RHEL/Fedora example):"
	@echo "  sudo dnf install -y git make gcc clang autoconf automake libtool pkgconf-pkg-config httpd-devel nginx mod_security"
	@echo "Install hints (Alpine example):"
	@echo "  sudo apk add git make gcc clang autoconf automake libtool pkgconf apache2-dev nginx modsecurity"

doctor-quick: check-framework
	DOCTOR_MODE=quick sh "$(FRAMEWORK_ROOT)/ci/tools/doctor.sh"

quick-all: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/tools/quick-all.sh"

cloud-quick-check: setup-dev lint generate-test-matrix check-test-matrix quick-check
	find "$(FRAMEWORK_ROOT)"/tests/normalizers "$(FRAMEWORK_ROOT)"/tests/runners "$(FRAMEWORK_ROOT)"/ci -type f -name '*.py' -print0 | xargs -0 -r env PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile
	git diff --check
	@echo "INFO: Cloud check is framework/generator only and not runtime compatibility evidence."

generate-test-matrix: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" OUTPUT_ROOT="$(CURDIR)" SKIP_ROOT_SUMMARY=1 $(MAKE) -C "$(FRAMEWORK_ROOT)" generate-test-matrix
	$(PYTHON) ci/checks/documentation/ensure-test-matrix-language-switches.py

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
