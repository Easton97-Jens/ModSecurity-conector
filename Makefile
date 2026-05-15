BUILD_ROOT ?= /src/ModSecurity-conector-build

export BUILD_ROOT
export REFRESH
export SMOKE_CASES
export MODSECURITY_V3_SOURCE_DIR
export MODSECURITY_APACHE_SOURCE_DIR
export MODSECURITY_NGINX_SOURCE_DIR
export BUILD_HTTPD_FROM_SOURCE
export BUILD_PCRE2_FROM_SOURCE
export BUILD_NGINX_FROM_SOURCE
export NGINX_SOURCE_MODE
export NGINX_GITHUB_REPO
export NGINX_RELEASE_TAG

.PHONY: smoke-apache smoke-nginx smoke-all

smoke-apache:
	sh ci/run-apache-smoke.sh

smoke-nginx:
	sh ci/run-nginx-smoke.sh

smoke-all:
	sh ci/run-connector-smokes.sh
