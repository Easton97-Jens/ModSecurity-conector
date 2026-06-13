PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
FRAMEWORK_PYTHON := $(if $(findstring /,$(PYTHON)),$(abspath $(PYTHON)),$(PYTHON))
STATE_HOME ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)
SOURCE_ROOT ?= $(STATE_HOME)/ModSecurity-conector-src
BUILD_ROOT ?= $(STATE_HOME)/ModSecurity-conector-build
TMP_ROOT ?= $(BUILD_ROOT)/tmp
LOG_ROOT ?= $(BUILD_ROOT)/logs
FRAMEWORK_ROOT ?= $(CURDIR)/modules/ModSecurity-test-Framework
CONNECTOR_ROOT := $(CURDIR)
NGINX_HARNESS_PARENT ?= $(if $(RUNNER_TEMP),$(RUNNER_TEMP),$(if $(TMPDIR),$(TMPDIR),$(if $(CONNECTOR_COMPONENT_CACHE),$(CONNECTOR_COMPONENT_CACHE),/src/ModSecurity-conector-cache)/nginx-harness))
MRTS_BUILD_ROOT ?= $(BUILD_ROOT)/mrts
MRTS_NATIVE_ROOT ?= $(BUILD_ROOT)/mrts-native
MRTS_NATIVE_TARGETS ?= apache2_ubuntu nginx-pr24
MRTS_NATIVE_APACHE_PORT ?= 19080
MRTS_NATIVE_NGINX_PORT ?= 19081
MRTS_NATIVE_BACKEND_PORT ?= 19082
GO_FTW_BIN ?= go-ftw
ALBEDO_BIN ?= albedo
CONNECTOR_COMPONENT_CACHE ?=
SKIP_RUNTIME_COMPONENT_PREPARE ?= 0
RUNTIME_COMPONENT_STRICT_VERIFY ?= 0
KEEP_RUNTIME_ARTIFACTS ?= 0
PYTHONDONTWRITEBYTECODE ?= 1
WITH_RUNTIME_COMPONENTS = SKIP_RUNTIME_COMPONENT_PREPARE=1 sh ci/with-runtime-components.sh

export BUILD_ROOT
export SOURCE_ROOT
export TMP_ROOT
export LOG_ROOT
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
export ALBEDO_BIN
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

.PHONY: check-framework prepare-runtime-components smoke-common smoke-apache smoke-nginx smoke-envoy smoke-haproxy smoke-lighttpd smoke-traefik smoke-new-connectors smoke-all test test-no-crs test-with-crs test-haproxy-no-crs test-haproxy-with-crs runtime-matrix runtime-matrix-all runtime-matrix-haproxy full-mrts-runtime-matrix full-matrix-parallel generate-full-runtime-matrix generate-work-queue generate-phase-work-queue generate-nolog-audit-evidence-analysis generate-response-header-hook-analysis generate-remaining-failure-analysis mrts-native-full-run mrts-native-apache-full mrts-native-nginx-pr24-full mrts-upstream-infra-check probe-response-body connector-starter-checks lint summary case-matrix setup-dev install-dev-deps doctor doctor-quick env-check fetch-deps fetch-modsecurity-v3 fetch-crs prepare-crs bootstrap-runtime quick-check codex-check quick-all smoke-installed installed-readiness doctor-install-hints cloud-quick-check generate-test-matrix check-test-matrix mrts-generate mrts-load mrts-import test-no-mrts test-with-mrts test-with-mrts-feature-demo test-mrts-matrix mrts-ftw

check-framework:
	@test -d "$(FRAMEWORK_ROOT)" || { \
		echo "BLOCKED: FRAMEWORK_ROOT is missing: $(FRAMEWORK_ROOT)"; \
		echo "Hint: run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; \
		exit 77; \
	}

prepare-runtime-components: check-framework
	@if [ "$(SKIP_RUNTIME_COMPONENT_PREPARE)" = "1" ]; then \
		echo "prepare-runtime-components: skipped (SKIP_RUNTIME_COMPONENT_PREPARE=1)"; \
	else \
		PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/prepare-runtime-components.sh; \
	fi

smoke-common: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=common sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"

smoke-apache: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/apache}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-apache-smoke.sh"

smoke-nginx: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/nginx}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-nginx-smoke.sh"

smoke-envoy: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-envoy-smoke.sh"

smoke-haproxy: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" RESULTS_DIR="$${RESULTS_DIR:-$(BUILD_ROOT)/results/$${MODSECURITY_TEST_VARIANT:-no-crs}/$${MODSECURITY_MRTS_VARIANT:-no-mrts}/haproxy}" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-haproxy-smoke.sh"

smoke-lighttpd: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-lighttpd-smoke.sh"

smoke-traefik: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-traefik-smoke.sh"

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
	$(WITH_RUNTIME_COMPONENTS) env CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"

test: test-no-crs test-with-crs

test-no-crs: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env MODSECURITY_TEST_VARIANT=no-crs MODSECURITY_RULE_PREAMBLE_FILE= sh -eu -c '. "$(FRAMEWORK_ROOT)/ci/common.sh"; RESULTS_DIR="$$BUILD_ROOT/results/no-crs"; export RESULTS_DIR; CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"'

test-with-crs: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env MODSECURITY_TEST_VARIANT=with-crs sh -eu -c '. "$(FRAMEWORK_ROOT)/ci/common.sh"; sh "$(FRAMEWORK_ROOT)/ci/fetch-crs.sh"; sh "$(FRAMEWORK_ROOT)/ci/prepare-crs.sh"; MODSECURITY_RULE_PREAMBLE_FILE="$$CRS_RUNTIME_DIR/modsecurity-crs-preamble.conf"; RESULTS_DIR="$$BUILD_ROOT/results/with-crs"; export MODSECURITY_RULE_PREAMBLE_FILE RESULTS_DIR; CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"'

mrts-generate: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-generate

mrts-load: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-load

mrts-import: check-framework
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-import

test-no-mrts: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-no-mrts

test-with-mrts: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-with-mrts

test-with-mrts-feature-demo: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-with-mrts-feature-demo

test-mrts-matrix: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" test-mrts-matrix

mrts-ftw: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" mrts-ftw

runtime-matrix: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" sh "$(FRAMEWORK_ROOT)/ci/run-runtime-matrix.sh"

runtime-matrix-all: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FORCE_ALL_CASES=1 sh "$(FRAMEWORK_ROOT)/ci/run-runtime-matrix.sh"

runtime-matrix-haproxy: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" HAPROXY_MATRIX_VARIANT=all sh "$(FRAMEWORK_ROOT)/ci/run-haproxy-runtime-matrix.sh"

full-mrts-runtime-matrix: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-full-mrts-runtime-matrix.sh

full-matrix-parallel: check-framework prepare-runtime-components
	$(WITH_RUNTIME_COMPONENTS) env PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" sh ci/run-full-matrix-parallel.sh

generate-full-runtime-matrix: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-full-runtime-matrix.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --build-root "$(BUILD_ROOT)" --log-root "$(LOG_ROOT)"

generate-work-queue: check-framework
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/generate-connector-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/generate-phase-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --connector-work-queue "$(CURDIR)/reports/testing/generated/connector-work-queue.generated.json" --phase-coverage "$(CURDIR)/reports/testing/generated/phase-coverage.generated.md" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" ci/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"

generate-phase-work-queue: check-framework
	"$(FRAMEWORK_PYTHON)" "$(FRAMEWORK_ROOT)/ci/generate-phase-work-queue.py" --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)" --output-root "$(CURDIR)" --connector-work-queue "$(CURDIR)/reports/testing/generated/connector-work-queue.generated.json" --phase-coverage "$(CURDIR)/reports/testing/generated/phase-coverage.generated.md" --full-runtime-matrix "$(CURDIR)/reports/testing/generated/full-runtime-matrix.generated.json"
	"$(FRAMEWORK_PYTHON)" ci/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"
	"$(FRAMEWORK_PYTHON)" ci/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"

generate-nolog-audit-evidence-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-nolog-audit-evidence-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-response-header-hook-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-response-header-hook-analysis.py --connector-root "$(CURDIR)" --framework-root "$(FRAMEWORK_ROOT)"

generate-remaining-failure-analysis: check-framework
	"$(FRAMEWORK_PYTHON)" ci/generate-remaining-failure-analysis.py --connector-root "$(CURDIR)"

mrts-native-full-run: check-framework prepare-runtime-components
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

lint: check-framework
	sh -n ci/*.sh connectors/*/harness/*.sh connectors/traefik/build/*.sh
	if command -v bash >/dev/null 2>&1; then bash -n ci/*.sh connectors/*/harness/*.sh connectors/traefik/build/*.sh; else echo "bash unavailable"; fi
	PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile "$(FRAMEWORK_ROOT)"/tests/normalizers/*.py "$(FRAMEWORK_ROOT)"/tests/runners/*.py "$(FRAMEWORK_ROOT)"/ci/*.py
	PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile ci/*.py
	$(PYTHON) -m json.tool config/testing/import-status.json >/dev/null
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-python-deps.py"
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-workflow-yaml.py"
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-doc-links.py"
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
	PYTHON="$(FRAMEWORK_PYTHON)" FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" CONNECTOR_ROOT="$(CURDIR)" OUTPUT_ROOT="$(CURDIR)" $(MAKE) -C "$(FRAMEWORK_ROOT)" generate-test-matrix

check-test-matrix: generate-test-matrix
	@test ! -f TEST-COVERAGE-SUMMARY.md || { \
		echo "Generated root coverage summary moved to $(FRAMEWORK_ROOT)/TEST-COVERAGE-SUMMARY.md; remove parent TEST-COVERAGE-SUMMARY.md"; \
		exit 1; \
	}
	@git diff --exit-code -- reports/testing >/dev/null || { \
		echo "Generated test matrix docs are out of date. Run make generate-test-matrix"; \
		exit 1; \
	}
	@git -C "$(FRAMEWORK_ROOT)" diff --exit-code -- TEST-COVERAGE-SUMMARY.md >/dev/null || { \
		echo "Framework coverage summary is out of date. Run make generate-test-matrix"; \
		exit 1; \
	}
