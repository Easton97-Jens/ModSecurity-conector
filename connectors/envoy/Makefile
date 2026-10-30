BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build
BRIDGE_BIN := $(BUILD_ROOT)/envoy-bridge-starter/envoy_bridge
SERVICE_BIN := $(BUILD_ROOT)/envoy-connector/msconnector_envoy_ext_authz
EXT_PROC_BIN := $(BUILD_ROOT)/envoy-ext-proc/msconnector_envoy_ext_proc
COMPOSITE_BIN := $(BUILD_ROOT)/envoy-composite/msconnector_composite
EXT_PROC_CONFIG ?= $(CURDIR)/config/envoy-ext-proc-service.json
EXT_PROC_ENVOY_CONFIG ?= $(BUILD_ROOT)/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml
EXT_PROC_RUNTIME_ROOT ?= $(BUILD_ROOT)/envoy-ext-proc/runtime-smoke
EXT_PROC_RUNTIME_EVENT_LOG_PATH ?= $(EXT_PROC_RUNTIME_ROOT)/events.jsonl
EXT_PROC_RUNTIME_CONFIG ?= $(EXT_PROC_RUNTIME_ROOT)/envoy-ext-proc-runtime.conf
EXT_PROC_TLS_CERTIFICATE ?= $(EXT_PROC_RUNTIME_ROOT)/envoy-loopback.crt
EXT_PROC_TLS_PRIVATE_KEY ?= $(EXT_PROC_RUNTIME_ROOT)/envoy-loopback.key
EXT_PROC_RULES_FILE ?= $(MSCONNECTOR_RULES_FILE)
EXT_PROC_LISTEN_PORT ?= 18080
EXT_PROC_UPSTREAM_PORT ?= 18081
EXT_PROC_LISTEN_SERVICE_PORT ?= 18083
EXT_PROC_ADMIN_PORT ?= 19001
CONFIG_FILE ?= $(CURDIR)/config/envoy-ext-authz.conf
RULES_FILE ?=
EVENT_LOG_PATH ?= $(BUILD_ROOT)/envoy-connector/events.jsonl
ENVOY_RUNTIME_ROOT ?= $(if $(RUNNER_TEMP),$(RUNNER_TEMP),$(if $(TMPDIR),$(TMPDIR),/var/tmp))/ModSecurity-conector-envoy-runtime-smoke
RUNTIME_EVENT_LOG_PATH ?= $(ENVOY_RUNTIME_ROOT)/events.jsonl
LISTEN_ADDRESS ?= 127.0.0.1
LISTEN_PORT ?= 18082
REPO_ROOT ?= ../..
FRAMEWORK_ROOT ?= $(REPO_ROOT)/modules/ModSecurity-test-Framework

# Explicit environment for pinned Framework test entrypoints.
PYTHON ?= python3
CONNECTOR_ROOT := $(abspath $(CURDIR)/../..)
CONNECTOR_REVISION := $(shell git -C "$(CONNECTOR_ROOT)" rev-parse HEAD)
TEST_ROOT := $(FRAMEWORK_ROOT)
CONNECTOR_TEST_PROFILE ?= h1
CONNECTOR_TEST_OUTPUT_ROOT ?= $(if $(RUNNER_TEMP),$(RUNNER_TEMP),$(TMP_ROOT))
export CONNECTOR_ROOT CONNECTOR_REVISION FRAMEWORK_ROOT TEST_ROOT CONNECTOR_TEST_PROFILE CONNECTOR_TEST_OUTPUT_ROOT
export PYTHONPATH := $(TEST_ROOT):$(TEST_ROOT)/connector_suite
export PYTHONSAFEPATH := 1
export PYTHONNOUSERSITE := 1
ACTIVE_TEST_RUNNER = $(PYTHON) -P -m modsecurity_test_framework.connector

# Shared read-only host-runtime gate. These snapshots are exported to the
# recursive root make; the recipe itself contains no caller-controlled shell
# interpolation.
ifeq ($(origin ENVOY_HOSTRUNTIME_PROFILE), undefined)
ENVOY_HOSTRUNTIME_PROFILE := envoy-ext-authz
endif
# Do not inspect the caller-provided profile in Make conditionals. The root
# checker validates the raw profile after safe argument transport; callers may
# select narrower runtime and binary roots explicitly when needed.
override ENVOY_HOSTRUNTIME_DEFAULT_ROOT := $(abspath $(BUILD_ROOT)/hostruntime/envoy)
override ENVOY_HOSTRUNTIME_DEFAULT_BINARY_ROOT := $(abspath $(BUILD_ROOT)/hostruntime/envoy)
ifeq ($(origin ENVOY_HOSTRUNTIME_LOCK), undefined)
ENVOY_HOSTRUNTIME_LOCK := $(abspath $(FRAMEWORK_ROOT)/ci/provisioning/runtime-component-lock.json)
endif
ifeq ($(origin ENVOY_HOSTRUNTIME_RUNTIME_ROOT), undefined)
ENVOY_HOSTRUNTIME_RUNTIME_ROOT := $(abspath $(ENVOY_HOSTRUNTIME_DEFAULT_ROOT))
endif
ifeq ($(origin ENVOY_HOSTRUNTIME_BINARY_ROOT), undefined)
ENVOY_HOSTRUNTIME_BINARY_ROOT := $(abspath $(ENVOY_HOSTRUNTIME_DEFAULT_BINARY_ROOT))
endif
ifeq ($(origin ENVOY_HOSTRUNTIME_EXPECTED_VERSION), undefined)
ENVOY_HOSTRUNTIME_EXPECTED_VERSION :=
endif
ifeq ($(origin ENVOY_HOSTRUNTIME_BINARY), undefined)
ENVOY_HOSTRUNTIME_BINARY :=
endif
ifeq ($(origin ENVOY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR), undefined)
ENVOY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR := $(abspath $(ENVOY_HOSTRUNTIME_DEFAULT_ROOT)/preflight)
endif
# Command-line hostruntime values are transported explicitly by the wrapper.
# Prevent GNU Make from expanding and auto-exporting their raw text first.
unexport ENVOY_HOSTRUNTIME_PROFILE ENVOY_HOSTRUNTIME_LOCK \
	ENVOY_HOSTRUNTIME_EXPECTED_VERSION ENVOY_HOSTRUNTIME_BINARY \
	ENVOY_HOSTRUNTIME_LOCK_ROOT ENVOY_HOSTRUNTIME_RUNTIME_ROOT \
	ENVOY_HOSTRUNTIME_BINARY_ROOT ENVOY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR

.PHONY: build-starter self-test self-test-envoy-bridge build-envoy-connector \
	build-envoy-ext-proc build-envoy-composite test-envoy-ext-proc check-envoy-ext-proc-config \
	prepare-envoy-ext-proc-config prepare-envoy-ext-proc-runtime-config \
	build-modsecurity-bridge check-envoy-config start-smoke-envoy \
	serve-envoy-connector runtime-smoke-envoy no-crs-baseline-envoy \
	response-phase-smoke-envoy \
	serve-envoy-ext-proc runtime-smoke-envoy-ext-proc \
	transport-cancel-smoke-envoy-ext-proc \
	self-test-modsecurity hostruntime-preflight-envoy hostruntime-preflight-envoy-ext-authz hostruntime-preflight-envoy-ext-proc clean

# Take variable names, not their values: this preserves caller text as data,
# doubles Make metacharacters for the child Make process, and shell-quotes the
# resulting environment assignments as one argument each.
hostruntime_wrapper_escape_dollars = $(subst $$,$$$$,$(value $(1)))
hostruntime_wrapper_safe_quote = '$(subst ','"'"',$(call hostruntime_wrapper_escape_dollars,$(1)))'
hostruntime-preflight-envoy:
	env \
		MAKEFLAGS=$(call hostruntime_wrapper_safe_quote,MFLAGS) \
		MAKEOVERRIDES='' \
		HOSTRUNTIME_CONNECTOR='envoy' \
		HOSTRUNTIME_PROFILE=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_PROFILE) \
		HOSTRUNTIME_EXPECTED_VERSION=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_EXPECTED_VERSION) \
		HOSTRUNTIME_BINARY=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_BINARY) \
		HOSTRUNTIME_BINARY_ROOT=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_BINARY_ROOT) \
		HOSTRUNTIME_LOCK=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_LOCK) \
		HOSTRUNTIME_LOCK_PROFILE=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_PROFILE) \
		HOSTRUNTIME_RUNTIME_ROOT=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_RUNTIME_ROOT) \
		HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR=$(call hostruntime_wrapper_safe_quote,ENVOY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR) \
		$(MAKE) -C ../.. hostruntime-preflight

hostruntime-preflight-envoy-ext-authz:
	$(MAKE) ENVOY_HOSTRUNTIME_PROFILE=envoy-ext-authz hostruntime-preflight-envoy

hostruntime-preflight-envoy-ext-proc:
	$(MAKE) ENVOY_HOSTRUNTIME_PROFILE=envoy-ext-proc hostruntime-preflight-envoy

build-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_metadata.sh

self-test:
	$(MAKE) -C ../.. framework-native-selftest NATIVE_TEST_TARGET=envoy-bridge

self-test-envoy-bridge: self-test

build-envoy-connector: build-envoy-ext-proc
	BUILD_ROOT="$(BUILD_ROOT)" \
	MODSECURITY_INCLUDE_DIR="$(MODSECURITY_INCLUDE_DIR)" \
	MODSECURITY_LIB_DIR="$(MODSECURITY_LIB_DIR)" \
	MODSECURITY_LIB_FILE="$(MODSECURITY_LIB_FILE)" \
	MODSECURITY_PREFIX="$(MODSECURITY_PREFIX)" \
	CC="$(CC)" CFLAGS="$(CFLAGS)" LDFLAGS="$(LDFLAGS)" LDLIBS="$(LDLIBS)" \
	sh build/build_connector.sh

# The ext_proc service is intentionally independent of the ext_authz C service.
# Its actual executable links the connector-local CGo bridge to Common Runtime
# and libmodsecurity, but remains non-promoted until canonical evidence review.
build-envoy-ext-proc:
	BUILD_ROOT="$(BUILD_ROOT)" \
	MODSECURITY_INCLUDE_DIR="$(MODSECURITY_INCLUDE_DIR)" \
	MODSECURITY_LIB_DIR="$(MODSECURITY_LIB_DIR)" \
	MODSECURITY_LIB_FILE="$(MODSECURITY_LIB_FILE)" \
	MODSECURITY_PREFIX="$(MODSECURITY_PREFIX)" \
	CC="$(CC)" CFLAGS="$(CFLAGS)" AR="$(AR)" \
	sh build/build_ext_proc.sh

# The composite command retains a single Common/libmodsecurity transaction
# across ext_authz/forwardAuth and its response companion. It is intentionally
# a separate executable, not a replacement for the standalone ext_proc path.
build-envoy-composite:
	BUILD_ROOT="$(BUILD_ROOT)" \
	MODSECURITY_INCLUDE_DIR="$(MODSECURITY_INCLUDE_DIR)" \
	MODSECURITY_LIB_DIR="$(MODSECURITY_LIB_DIR)" \
	MODSECURITY_LIB_FILE="$(MODSECURITY_LIB_FILE)" \
	MODSECURITY_PREFIX="$(MODSECURITY_PREFIX)" \
	CC="$(CC)" CFLAGS="$(CFLAGS)" AR="$(AR)" \
	sh build/build_composite.sh

test-envoy-ext-proc:
	$(MAKE) -C ../.. framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc

check-envoy-ext-proc-config: build-envoy-ext-proc prepare-envoy-ext-proc-runtime-config
	"$(EXT_PROC_BIN)" --check-config --config "$(EXT_PROC_CONFIG)" --runtime-config "$(EXT_PROC_RUNTIME_CONFIG)"

prepare-envoy-ext-proc-config:
	OUTPUT_CONFIG="$(EXT_PROC_ENVOY_CONFIG)" \
	LISTEN_PORT="$(EXT_PROC_LISTEN_PORT)" UPSTREAM_PORT="$(EXT_PROC_UPSTREAM_PORT)" \
	EXT_PROC_PORT="$(EXT_PROC_LISTEN_SERVICE_PORT)" ADMIN_PORT="$(EXT_PROC_ADMIN_PORT)" \
	TLS_CERTIFICATE="$(EXT_PROC_TLS_CERTIFICATE)" TLS_PRIVATE_KEY="$(EXT_PROC_TLS_PRIVATE_KEY)" \
	sh config/prepare_envoy_ext_proc_config.sh

prepare-envoy-ext-proc-runtime-config:
	OUTPUT_CONFIG="$(EXT_PROC_RUNTIME_CONFIG)" RULES_FILE="$(EXT_PROC_RULES_FILE)" \
	EVENT_PATH="$(EXT_PROC_RUNTIME_EVENT_LOG_PATH)" \
	sh config/prepare_envoy_ext_proc_runtime_config.sh

serve-envoy-ext-proc: build-envoy-ext-proc prepare-envoy-ext-proc-runtime-config
	EXT_PROC_BIN="$(EXT_PROC_BIN)" EXT_PROC_CONFIG="$(EXT_PROC_CONFIG)" \
	EXT_PROC_RUNTIME_CONFIG="$(EXT_PROC_RUNTIME_CONFIG)" \
	EVENT_LOG_PATH="$(EXT_PROC_RUNTIME_EVENT_LOG_PATH)" LISTEN_ADDRESS="$(LISTEN_ADDRESS)" \
	LISTEN_PORT="$(EXT_PROC_LISTEN_SERVICE_PORT)" \
	sh scripts/serve_envoy_ext_proc.sh

# This is deliberately separate from runtime-smoke-envoy: it exercises the
# native Envoy ext_proc gRPC filter and the real Common/libmodsecurity bridge.
# It still does not promote connector capabilities by itself.
runtime-smoke-envoy-ext-proc: EXT_PROC_RULES_FILE = $(if $(MSCONNECTOR_RULES_FILE),$(MSCONNECTOR_RULES_FILE),$(abspath $(FRAMEWORK_ROOT)/tests/rules/no-crs-baseline.conf))
runtime-smoke-envoy-ext-proc: build-envoy-ext-proc
	@if [ "$(ON_DEMAND_TESTS)" != 1 ]; then \
		[ "$${MSCONNECTOR_CRS_RUNTIME:-0}" = 1 ] || { echo "FAIL: specialist native lifecycle requires explicit ON_DEMAND_TESTS=1" >&2; exit 2; }; \
		$(ACTIVE_TEST_RUNNER) --check --execution runtime.crs.envoy; \
	fi
	EXT_PROC_BIN="$(EXT_PROC_BIN)" EXT_PROC_CONFIG="$(EXT_PROC_CONFIG)" \
	BUILD_ROOT="$(BUILD_ROOT)" RUNTIME_ROOT="$(EXT_PROC_RUNTIME_ROOT)" \
	EVENT_LOG_PATH="$(EXT_PROC_RUNTIME_EVENT_LOG_PATH)" ENVOY_BIN="$(ENVOY_BIN)" \
	EXT_PROC_RUNTIME_CONFIG="$(EXT_PROC_RUNTIME_CONFIG)" RULES_FILE="$(EXT_PROC_RULES_FILE)" \
	PYTHON="$(PYTHON)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/envoy/harness/run_envoy_ext_proc_runtime.sh"

# The cancellation probe is deliberately opt-in: it uses a real downstream
# connection close after the first body byte and remains non-promoting even
# when its ext_proc completion sidecar is present.
transport-cancel-smoke-envoy-ext-proc:
	$(if $(filter 1,$(ON_DEMAND_TESTS)),,$(error transport-cancel specialist campaign requires explicit ON_DEMAND_TESTS=1))
	$(MAKE) ENVOY_TRANSPORT_CANCEL_PROBE=1 runtime-smoke-envoy-ext-proc

build-modsecurity-bridge: build-envoy-connector

check-envoy-config: build-envoy-connector check-envoy-ext-proc-config prepare-envoy-ext-proc-config
	@if [ "$(ON_DEMAND_TESTS)" != 1 ]; then $(ACTIVE_TEST_RUNNER) --check --execution runtime.config.envoy; fi
	SERVICE_BIN="$(SERVICE_BIN)" CONFIG_FILE="$(CONFIG_FILE)" RULES_FILE="$(RULES_FILE)" \
	EVENT_LOG_PATH="$(EVENT_LOG_PATH)" LISTEN_ADDRESS="$(LISTEN_ADDRESS)" LISTEN_PORT="$(LISTEN_PORT)" \
	sh config/check_envoy_config.sh

start-smoke-envoy: RULES_FILE = $(if $(MSCONNECTOR_RULES_FILE),$(MSCONNECTOR_RULES_FILE),$(abspath $(FRAMEWORK_ROOT)/connector_suite/common/rules/modsecurity_targeted_smoke.conf))
start-smoke-envoy: build-envoy-connector
	$(if $(filter 1,$(ON_DEMAND_TESTS)),,$(error standalone lifecycle diagnostic is archived; explicit ON_DEMAND_TESTS=1 is required))
	SERVICE_BIN="$(SERVICE_BIN)" CONFIG_FILE="$(CONFIG_FILE)" RULES_FILE="$(RULES_FILE)" \
	EVENT_LOG_PATH="$(EVENT_LOG_PATH)" LISTEN_ADDRESS="$(LISTEN_ADDRESS)" LISTEN_PORT="$(LISTEN_PORT)" \
	ENVOY_BIN="$(ENVOY_BIN)" PYTHON="$(PYTHON)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/envoy/harness/start_envoy_connector.sh"

serve-envoy-connector: build-envoy-connector
	SERVICE_BIN="$(SERVICE_BIN)" CONFIG_FILE="$(CONFIG_FILE)" RULES_FILE="$(RULES_FILE)" \
	EVENT_LOG_PATH="$(EVENT_LOG_PATH)" LISTEN_ADDRESS="$(LISTEN_ADDRESS)" LISTEN_PORT="$(LISTEN_PORT)" \
	sh scripts/serve_envoy_connector.sh

runtime-smoke-envoy: build-envoy-connector
	@if [ "$(ON_DEMAND_TESTS)" != 1 ]; then $(ACTIVE_TEST_RUNNER) --check --execution runtime.no-crs.envoy; fi
	SERVICE_BIN="$(SERVICE_BIN)" BUILD_ROOT="$(BUILD_ROOT)" CONFIG_FILE="$(CONFIG_FILE)" \
	RULES_FILE="$(if $(RULES_FILE),$(RULES_FILE),$(if $(MSCONNECTOR_RULES_FILE),$(MSCONNECTOR_RULES_FILE),$(abspath $(FRAMEWORK_ROOT)/connector_suite/common/rules/modsecurity_targeted_smoke.conf)))" RUNTIME_ROOT="$(ENVOY_RUNTIME_ROOT)" \
	EVENT_LOG_PATH="$(RUNTIME_EVENT_LOG_PATH)" ENVOY_BIN="$(ENVOY_BIN)" \
	PYTHON="$(PYTHON)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/envoy/harness/run_envoy_connector_runtime.sh"

no-crs-baseline-envoy: export MSCONNECTOR_NO_CRS_BASELINE := 1
no-crs-baseline-envoy: runtime-smoke-envoy

# This opt-in companion check is deliberately separate from the P1 default
# smoke target.  The runner enables its P3/P4 assertions only when the
# matching response-phase rule fixture is selected explicitly.
ifeq ($(ON_DEMAND_TESTS),1)
response-phase-smoke-envoy: override RULES_FILE := $(abspath $(FRAMEWORK_ROOT)/connector_suite/common/rules/modsecurity_response_companion_smoke.conf)
response-phase-smoke-envoy: override export MSCONNECTOR_RESPONSE_PHASE_SMOKE := 1
response-phase-smoke-envoy: runtime-smoke-envoy
else
response-phase-smoke-envoy:
	$(error specialist response-phase profile requires explicit ON_DEMAND_TESTS=1 authorization)
endif

self-test-modsecurity: check-envoy-config

clean:
	rm -rf "$(BUILD_ROOT)/envoy-build-starter" "$(BUILD_ROOT)/envoy-bridge-starter" "$(BUILD_ROOT)/envoy-connector"
