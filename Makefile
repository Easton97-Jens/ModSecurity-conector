BUILD_ROOT ?= /src/ModSecurity-conector-build

export BUILD_ROOT
export REFRESH
export SMOKE_CASES
export CASE_SCOPE
export MODSECURITY_V3_SOURCE_DIR
export MODSECURITY_APACHE_SOURCE_DIR
export MODSECURITY_NGINX_SOURCE_DIR
export BUILD_HTTPD_FROM_SOURCE
export BUILD_PCRE2_FROM_SOURCE
export BUILD_NGINX_FROM_SOURCE
export NGINX_SOURCE_MODE
export NGINX_GITHUB_REPO
export NGINX_RELEASE_TAG
export RESPONSE_BODY_PROBE_REPEAT
export RESPONSE_BODY_PROBE_ROOT
export RESPONSE_BODY_PROBE_CASE

.PHONY: smoke-common smoke-apache smoke-nginx smoke-all probe-response-body

smoke-common:
	CASE_SCOPE=common sh ci/run-connector-smokes.sh

smoke-apache:
	CASE_SCOPE=all sh ci/run-apache-smoke.sh

smoke-nginx:
	CASE_SCOPE=all sh ci/run-nginx-smoke.sh

smoke-all:
	CASE_SCOPE=all sh ci/run-connector-smokes.sh

probe-response-body:
	sh ci/probe-response-body-blocking.sh
