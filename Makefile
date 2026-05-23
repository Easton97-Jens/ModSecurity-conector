PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
STATE_HOME ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)
BUILD_ROOT ?= $(STATE_HOME)/ModSecurity-conector-build
FRAMEWORK_ROOT ?= $(CURDIR)/modules/ModSecurity-test-Framework
CONNECTOR_ROOT := $(CURDIR)
PYTHONDONTWRITEBYTECODE ?= 1

export BUILD_ROOT
export FRAMEWORK_ROOT
export CONNECTOR_ROOT
export SOURCE_ROOT
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
export BUILD_HTTPD_FROM_SOURCE
export BUILD_PCRE2_FROM_SOURCE
export BUILD_NGINX_FROM_SOURCE
export NGINX_SOURCE_MODE
export NGINX_SOURCE_REPO_URL
export NGINX_SOURCE_GIT_REF
export NGINX_GITHUB_REPO
export NGINX_RELEASE_TAG
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

.PHONY: check-framework smoke-common smoke-apache smoke-nginx smoke-all runtime-matrix runtime-matrix-all probe-response-body lint summary case-matrix setup-dev install-dev-deps doctor doctor-quick env-check fetch-deps fetch-modsecurity-v3 bootstrap-runtime quick-check codex-check quick-all smoke-installed installed-readiness doctor-install-hints cloud-quick-check generate-test-matrix check-test-matrix

check-framework:
	@test -d "$(FRAMEWORK_ROOT)" || { \
		echo "BLOCKED: FRAMEWORK_ROOT is missing: $(FRAMEWORK_ROOT)"; \
		echo "Hint: run git submodule update --init --recursive or set FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework"; \
		exit 77; \
	}

smoke-common: check-framework
	CASE_SCOPE=common sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"

smoke-apache: check-framework
	CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-apache-smoke.sh"

smoke-nginx: check-framework
	CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-nginx-smoke.sh"

smoke-all: check-framework
	CASE_SCOPE=all sh "$(FRAMEWORK_ROOT)/ci/run-connector-smokes.sh"

runtime-matrix: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/run-runtime-matrix.sh"

runtime-matrix-all: check-framework
	FORCE_ALL_CASES=1 sh "$(FRAMEWORK_ROOT)/ci/run-runtime-matrix.sh"

probe-response-body: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/probe-response-body-blocking.sh"

lint: check-framework
	sh -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh
	if command -v bash >/dev/null 2>&1; then bash -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh; else echo "bash unavailable"; fi
	PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -P -m py_compile "$(FRAMEWORK_ROOT)"/tests/normalizers/*.py "$(FRAMEWORK_ROOT)"/tests/runners/*.py "$(FRAMEWORK_ROOT)"/ci/*.py
	$(PYTHON) -m json.tool config/testing/import-status.json >/dev/null
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-python-deps.py"
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-workflow-yaml.py"
	CONNECTOR_ROOT="$(CURDIR)" $(PYTHON) "$(FRAMEWORK_ROOT)/ci/check-doc-links.py"
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

fetch-deps bootstrap-runtime: check-framework
	sh "$(FRAMEWORK_ROOT)/ci/fetch-smoke-sources.sh" all

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
	$(PYTHON) "$(FRAMEWORK_ROOT)/ci/generate-case-matrix.py" --framework-root "$(FRAMEWORK_ROOT)" --connector-root "$(CURDIR)" --output-root "$(CURDIR)"

check-test-matrix: check-framework
	$(PYTHON) "$(FRAMEWORK_ROOT)/ci/generate-case-matrix.py" --framework-root "$(FRAMEWORK_ROOT)" --connector-root "$(CURDIR)" --output-root "$(CURDIR)"
	@git diff --exit-code -- reports/testing TEST-COVERAGE-SUMMARY.md >/dev/null || { \
		echo "Generated test matrix docs are out of date. Run make generate-test-matrix"; \
		exit 1; \
	}
