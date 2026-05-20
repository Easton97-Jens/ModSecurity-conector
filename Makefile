PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
STATE_HOME ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)
BUILD_ROOT ?= $(STATE_HOME)/ModSecurity-conector-build
PYTHONDONTWRITEBYTECODE ?= 1

export BUILD_ROOT
export SOURCE_ROOT
export PYTHON
export PYTHONDONTWRITEBYTECODE
export DEFAULT_BRANCH
export REFRESH
export SMOKE_CASES
export CASE_SCOPE
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

.PHONY: smoke-common smoke-apache smoke-nginx smoke-all runtime-matrix probe-response-body lint summary case-matrix setup-dev install-dev-deps doctor doctor-quick env-check fetch-deps fetch-modsecurity-v3 bootstrap-runtime quick-check codex-check quick-all smoke-installed installed-readiness doctor-install-hints cloud-quick-check generate-test-matrix check-test-matrix

smoke-common:
	CASE_SCOPE=common sh ci/run-connector-smokes.sh

smoke-apache:
	CASE_SCOPE=all sh ci/run-apache-smoke.sh

smoke-nginx:
	CASE_SCOPE=all sh ci/run-nginx-smoke.sh

smoke-all:
	CASE_SCOPE=all sh ci/run-connector-smokes.sh

runtime-matrix:
	sh ci/run-runtime-matrix.sh

probe-response-body:
	sh ci/probe-response-body-blocking.sh

lint:
	sh -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh
	if command -v bash >/dev/null 2>&1; then bash -n ci/*.sh connectors/apache/harness/*.sh connectors/nginx/harness/*.sh; else echo "bash unavailable"; fi
	PYTHONPYCACHEPREFIX="$(BUILD_ROOT)/pycache" $(PYTHON) -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py
	$(PYTHON) -m json.tool tests/import-status.json >/dev/null
	$(PYTHON) ci/check-python-deps.py
	$(PYTHON) ci/check-workflow-yaml.py
	$(PYTHON) ci/check-doc-links.py
	sh ci/check-common-helpers.sh
	sh ci/check-adapter-helpers.sh
	sh ci/check-adapter-metadata-drift.sh
	if command -v actionlint >/dev/null 2>&1; then actionlint .github/workflows/*.yml; else echo "actionlint unavailable"; fi
	git diff --check

summary:
	$(PYTHON) ci/summarize-results.py "$(BUILD_ROOT)/results/connector-summary.json"

case-matrix:
	$(PYTHON) ci/write-case-matrix.py "$(BUILD_ROOT)/results/connector-summary.json" docs/testing/case-matrix.md

install-dev-deps:
	sh ci/bootstrap-python.sh

setup-dev: install-dev-deps
	@echo "setup-dev: using PYTHON=$(PYTHON)"
	@echo "setup-dev: next steps -> make lint; make fetch-deps; make doctor; make smoke-all"



fetch-modsecurity-v3:
	sh ci/fetch-smoke-sources.sh v3

fetch-deps bootstrap-runtime:
	sh ci/fetch-smoke-sources.sh all

doctor env-check:
	sh ci/doctor.sh


print-python:
	@echo "make: using PYTHON=$(PYTHON)"

bootstrap-all: setup-dev fetch-deps doctor
	@echo "bootstrap-all complete (smoke not run)"


quick-check codex-check:
	make lint
	$(PYTHON) -m py_compile tests/normalizers/*.py tests/runners/*.py ci/*.py
	git diff --check

smoke-installed installed-readiness:
	sh ci/smoke-installed.sh

doctor-install-hints:
	@echo "Install hints (Debian/Ubuntu example):"
	@echo "  sudo apt-get update"
	@echo "  sudo apt-get install -y git make gcc clang autoconf automake libtool pkg-config apache2-dev nginx libmodsecurity-dev"
	@echo "Install hints (RHEL/Fedora example):"
	@echo "  sudo dnf install -y git make gcc clang autoconf automake libtool pkgconf-pkg-config httpd-devel nginx mod_security"
	@echo "Install hints (Alpine example):"
	@echo "  sudo apk add git make gcc clang autoconf automake libtool pkgconf apache2-dev nginx modsecurity"


doctor-quick:
	DOCTOR_MODE=quick sh ci/doctor.sh

quick-all:
	sh ci/quick-all.sh

cloud-quick-check:
	sh ci/cloud-quick-check.sh


generate-test-matrix:
	$(PYTHON) ci/generate-case-matrix.py

check-test-matrix:
	$(PYTHON) ci/generate-case-matrix.py
	@git diff --exit-code -- docs/testing/generated docs/testing/test-coverage-overview.md TEST-COVERAGE-SUMMARY.md >/dev/null || { \
		echo "Generated test matrix docs are out of date. Run make generate-test-matrix"; \
		exit 1; \
	}
