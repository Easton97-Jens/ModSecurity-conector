# Product build and pinned Framework integration entrypoints.
.DEFAULT_GOAL := test
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
CONNECTOR_ROOT := $(CURDIR)
CONNECTOR_REVISION := $(shell git -C "$(CONNECTOR_ROOT)" rev-parse HEAD)
FRAMEWORK_ROOT ?= $(CONNECTOR_ROOT)/modules/ModSecurity-test-Framework
TEST_ROOT := $(FRAMEWORK_ROOT)
CONNECTOR_TEST_PROFILE ?= h1
CONNECTOR_TEST_OUTPUT_ROOT ?= $(if $(RUNNER_TEMP),$(RUNNER_TEMP),$(TMP_ROOT))
export CONNECTOR_ROOT CONNECTOR_REVISION FRAMEWORK_ROOT TEST_ROOT
export CONNECTOR_TEST_PROFILE CONNECTOR_TEST_OUTPUT_ROOT
export NATIVE_TEST_TARGET NATIVE_TEST_MODE NATIVE_TEST_RULES_FILE TRAEFIK_ENGINE_SOCKET_TEST_PARENT GO_TEST_MODULE
export PYTHONPATH := $(TEST_ROOT):$(TEST_ROOT)/connector_suite

Makefile: ;
.PHONY: FORCE framework-native-selftest framework-go-test
FORCE:

build-envoy build-traefik build-lighttpd:
	$(MAKE) -C "$(CONNECTOR_ROOT)/connectors/$(patsubst build-%,%,$@)" build-$(patsubst build-%,%,$@)-connector

build-haproxy:
	$(MAKE) -C "$(CONNECTOR_ROOT)/connectors/haproxy" build-spoa-runtime

framework-native-selftest:
	@$(PYTHON) -P "$(TEST_ROOT)/connector_native_tests/invoke.py"

framework-go-test:
	@$(PYTHON) -P "$(TEST_ROOT)/connector_native_tests/go_invoke.py"

# Test/check targets share one implementation in the pinned Framework.
%: FORCE
	@test -f "$(TEST_ROOT)/connector_suite/connector.mk" || { echo "BLOCKED: pinned Framework connector suite is missing" >&2; exit 77; }
	@$(MAKE) --no-print-directory -f "$(TEST_ROOT)/connector_suite/connector.mk" -C "$(CONNECTOR_ROOT)" "$@"

export PYTHONSAFEPATH := 1
