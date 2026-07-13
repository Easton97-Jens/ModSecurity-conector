BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build
BRIDGE_BIN := $(BUILD_ROOT)/envoy-bridge-starter/envoy_bridge
SERVICE_BIN := $(BUILD_ROOT)/envoy-connector/msconnector_envoy_ext_authz
EXT_PROC_BIN := $(BUILD_ROOT)/envoy-ext-proc/msconnector_envoy_ext_proc
EXT_PROC_CONFIG ?= $(CURDIR)/config/envoy-ext-proc-service.json
EXT_PROC_ENVOY_CONFIG ?= $(BUILD_ROOT)/envoy-ext-proc/config/envoy-ext-proc.streaming.yaml
EXT_PROC_RUNTIME_ROOT ?= $(BUILD_ROOT)/envoy-ext-proc/runtime-smoke
EXT_PROC_RUNTIME_EVENT_LOG_PATH ?= $(EXT_PROC_RUNTIME_ROOT)/events.jsonl
EXT_PROC_RUNTIME_CONFIG ?= $(EXT_PROC_RUNTIME_ROOT)/envoy-ext-proc-runtime.conf
EXT_PROC_RULES_FILE ?= $(if $(MSCONNECTOR_RULES_FILE),$(MSCONNECTOR_RULES_FILE),$(if $(NO_CRS_RULES_FILE),$(NO_CRS_RULES_FILE),$(abspath $(CURDIR)/../../modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf)))
EXT_PROC_LISTEN_PORT ?= 18080
EXT_PROC_UPSTREAM_PORT ?= 18081
EXT_PROC_LISTEN_SERVICE_PORT ?= 18083
EXT_PROC_ADMIN_PORT ?= 19001
CONFIG_FILE ?= $(CURDIR)/config/envoy-ext-authz.conf
RULES_FILE ?= $(abspath $(CURDIR)/../../common/rules/modsecurity_targeted_smoke.conf)
EVENT_LOG_PATH ?= $(BUILD_ROOT)/envoy-connector/events.jsonl
RUNTIME_EVENT_LOG_PATH ?= $(BUILD_ROOT)/envoy-connector/runtime-smoke/events.jsonl
LISTEN_ADDRESS ?= 127.0.0.1
LISTEN_PORT ?= 18082

.PHONY: build-starter self-test self-test-envoy-bridge build-envoy-connector \
	build-envoy-ext-proc test-envoy-ext-proc check-envoy-ext-proc-config \
	prepare-envoy-ext-proc-config prepare-envoy-ext-proc-runtime-config \
	build-modsecurity-bridge check-envoy-config start-smoke-envoy \
	serve-envoy-connector runtime-smoke-envoy no-crs-baseline-envoy \
	serve-envoy-ext-proc runtime-smoke-envoy-ext-proc \
	transport-cancel-smoke-envoy-ext-proc \
	self-test-modsecurity clean

build-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_metadata.sh

self-test: build-starter
	"$(BRIDGE_BIN)" --self-test

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

test-envoy-ext-proc:
	BUILD_ROOT="$(BUILD_ROOT)" \
	MODSECURITY_INCLUDE_DIR="$(MODSECURITY_INCLUDE_DIR)" \
	MODSECURITY_LIB_DIR="$(MODSECURITY_LIB_DIR)" \
	MODSECURITY_LIB_FILE="$(MODSECURITY_LIB_FILE)" \
	MODSECURITY_PREFIX="$(MODSECURITY_PREFIX)" \
	CC="$(CC)" CFLAGS="$(CFLAGS)" AR="$(AR)" \
	sh build/test_ext_proc.sh

check-envoy-ext-proc-config: build-envoy-ext-proc
	"$(EXT_PROC_BIN)" --check-config --config "$(EXT_PROC_CONFIG)"

prepare-envoy-ext-proc-config:
	OUTPUT_CONFIG="$(EXT_PROC_ENVOY_CONFIG)" \
	LISTEN_PORT="$(EXT_PROC_LISTEN_PORT)" UPSTREAM_PORT="$(EXT_PROC_UPSTREAM_PORT)" \
	EXT_PROC_PORT="$(EXT_PROC_LISTEN_SERVICE_PORT)" ADMIN_PORT="$(EXT_PROC_ADMIN_PORT)" \
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
	sh harness/serve_envoy_ext_proc.sh

# This is deliberately separate from runtime-smoke-envoy: it exercises the
# native Envoy ext_proc gRPC filter and the real Common/libmodsecurity bridge.
# It still does not promote connector capabilities by itself.
runtime-smoke-envoy-ext-proc: build-envoy-ext-proc
	EXT_PROC_BIN="$(EXT_PROC_BIN)" EXT_PROC_CONFIG="$(EXT_PROC_CONFIG)" \
	BUILD_ROOT="$(BUILD_ROOT)" RUNTIME_ROOT="$(EXT_PROC_RUNTIME_ROOT)" \
	EVENT_LOG_PATH="$(EXT_PROC_RUNTIME_EVENT_LOG_PATH)" ENVOY_BIN="$(ENVOY_BIN)" \
	EXT_PROC_RUNTIME_CONFIG="$(EXT_PROC_RUNTIME_CONFIG)" RULES_FILE="$(EXT_PROC_RULES_FILE)" \
	PYTHON="$(PYTHON)" sh harness/run_envoy_ext_proc_runtime.sh

# The cancellation probe is deliberately opt-in: it uses a real downstream
# connection close after the first body byte and remains non-promoting even
# when its ext_proc completion sidecar is present.
transport-cancel-smoke-envoy-ext-proc:
	$(MAKE) ENVOY_TRANSPORT_CANCEL_PROBE=1 runtime-smoke-envoy-ext-proc

build-modsecurity-bridge: build-envoy-connector

check-envoy-config: build-envoy-connector check-envoy-ext-proc-config prepare-envoy-ext-proc-config
	SERVICE_BIN="$(SERVICE_BIN)" CONFIG_FILE="$(CONFIG_FILE)" RULES_FILE="$(RULES_FILE)" \
	EVENT_LOG_PATH="$(EVENT_LOG_PATH)" LISTEN_ADDRESS="$(LISTEN_ADDRESS)" LISTEN_PORT="$(LISTEN_PORT)" \
	sh config/check_envoy_config.sh

start-smoke-envoy: build-envoy-connector
	SERVICE_BIN="$(SERVICE_BIN)" CONFIG_FILE="$(CONFIG_FILE)" RULES_FILE="$(RULES_FILE)" \
	EVENT_LOG_PATH="$(EVENT_LOG_PATH)" LISTEN_ADDRESS="$(LISTEN_ADDRESS)" LISTEN_PORT="$(LISTEN_PORT)" \
	ENVOY_BIN="$(ENVOY_BIN)" PYTHON="$(PYTHON)" sh harness/start_envoy_connector.sh

serve-envoy-connector: build-envoy-connector
	SERVICE_BIN="$(SERVICE_BIN)" CONFIG_FILE="$(CONFIG_FILE)" RULES_FILE="$(RULES_FILE)" \
	EVENT_LOG_PATH="$(EVENT_LOG_PATH)" LISTEN_ADDRESS="$(LISTEN_ADDRESS)" LISTEN_PORT="$(LISTEN_PORT)" \
	sh harness/serve_envoy_connector.sh

runtime-smoke-envoy: build-envoy-connector
	SERVICE_BIN="$(SERVICE_BIN)" BUILD_ROOT="$(BUILD_ROOT)" CONFIG_FILE="$(CONFIG_FILE)" \
	RULES_FILE="$(RULES_FILE)" EVENT_LOG_PATH="$(RUNTIME_EVENT_LOG_PATH)" ENVOY_BIN="$(ENVOY_BIN)" \
	PYTHON="$(PYTHON)" sh harness/run_envoy_connector_runtime.sh

no-crs-baseline-envoy: export MSCONNECTOR_NO_CRS_BASELINE := 1
no-crs-baseline-envoy: runtime-smoke-envoy

self-test-modsecurity: check-envoy-config

clean:
	rm -rf "$(BUILD_ROOT)/envoy-build-starter" "$(BUILD_ROOT)/envoy-bridge-starter" "$(BUILD_ROOT)/envoy-connector"
