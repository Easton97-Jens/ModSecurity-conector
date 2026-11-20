# Product build and pinned Framework integration entrypoints.
.DEFAULT_GOAL := test
CONNECTOR_ROOT := $(CURDIR)
# Local runs provision .venv on demand for the exact .python-version and the
# pinned Framework's reviewed dependency locks (ci/tools/ensure-python-env.py).
# CI keeps the toolcache interpreter that its workflows install explicitly.
PYTHON_ENV_AUTO ?= $(if $(filter true,$(CI) $(GITHUB_ACTIONS)),0,1)
PYTHON_ENV_ROOT ?=
PYTHON_BASE ?=
PYTHON ?= $(if $(filter 1,$(PYTHON_ENV_AUTO)),$(CONNECTOR_ROOT)/.venv/bin/python,$(if $(wildcard .venv/bin/python),.venv/bin/python,python3))
PYTHON_ENV_MANAGED := $(and $(filter 1,$(PYTHON_ENV_AUTO)),$(filter $(CONNECTOR_ROOT)/.venv/bin/python,$(abspath $(PYTHON))))
PYTHON_ENV_HELPER = $(or $(PYTHON_BASE),python3) -P "$(CONNECTOR_ROOT)/ci/tools/ensure-python-env.py" $(if $(PYTHON_BASE),--base "$(PYTHON_BASE)")
# Local runs install the locked release and Go security tools at run time into
# the run-private $(RUNNER_TEMP)/security-tools (ci/tools/ensure-security-tools.py).
SECURITY_TOOLS_AUTO ?= $(if $(filter true,$(CI) $(GITHUB_ACTIONS)),0,1)
SECURITY_TOOLS_HELPER = $(or $(PYTHON_BASE),python3) -P "$(CONNECTOR_ROOT)/ci/tools/ensure-security-tools.py" --destination "$(RUNNER_TEMP)/security-tools"
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
.PHONY: python-env python-env-framework security-tools security-tools-auto
# Every Framework-delegated target first ensures the managed environment and
# the run-private security tools.
FORCE: python-env security-tools-auto
framework-native-selftest framework-go-test: python-env

# Explicit request: strict. Automatic step: a tool that cannot be installed is
# reported, and only the checks that need it fail with their own message.
security-tools:
	@test -n "$(RUNNER_TEMP)" || { echo "BLOCKED: security-tools: RUNNER_TEMP must select the run-private tool directory" >&2; exit 77; }
	@$(SECURITY_TOOLS_HELPER) --verbose

security-tools-auto:
ifeq ($(SECURITY_TOOLS_AUTO)$(if $(RUNNER_TEMP),set),1set)
	@$(SECURITY_TOOLS_HELPER) || echo "WARN: security-tools: not fully installed (exit $$?); checks that need a missing tool report it" >&2
else
	@:
endif

ifneq ($(PYTHON_ENV_MANAGED),)
python-env:
	@PYTHON_ENV_ROOT="$(PYTHON_ENV_ROOT)" $(PYTHON_ENV_HELPER) --role parent $(if $(filter python-env,$(MAKECMDGOALS)),--verbose)

# Locally, the managed environment replaces the Framework's unpinned bootstrap.
install-dev-deps setup-dev: python-env
	@echo "$@: managed Python environment ready: PYTHON=$(PYTHON)"
	@echo "$@: next steps -> make lint; make fetch-deps; make doctor; make smoke-all"
else
python-env:
	@$(if $(filter python-env,$(MAKECMDGOALS)),echo "python-env: not managed; using PYTHON=$(PYTHON)",:)
endif

# Separate Framework-owned environment (validated against the Framework lock);
# created only when requested, below PYTHON_ENV_ROOT.
python-env-framework:
	@PYTHON_ENV_ROOT="$(PYTHON_ENV_ROOT)" $(PYTHON_ENV_HELPER) --role framework --verbose

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
