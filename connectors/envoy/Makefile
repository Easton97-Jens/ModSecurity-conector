BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build
BRIDGE_BIN := $(BUILD_ROOT)/envoy-bridge-starter/envoy_bridge
SERVICE_BIN := $(BUILD_ROOT)/envoy-connector/msconnector_envoy_ext_authz
CONFIG_FILE ?= $(CURDIR)/config/envoy-ext-authz.conf
RULES_FILE ?= $(abspath $(CURDIR)/../../common/rules/modsecurity_targeted_smoke.conf)
EVENT_LOG_PATH ?= $(BUILD_ROOT)/envoy-connector/events.jsonl
RUNTIME_EVENT_LOG_PATH ?= $(BUILD_ROOT)/envoy-connector/runtime-smoke/events.jsonl
LISTEN_ADDRESS ?= 127.0.0.1
LISTEN_PORT ?= 18082

.PHONY: build-starter self-test self-test-envoy-bridge build-envoy-connector \
	build-modsecurity-bridge check-envoy-config start-smoke-envoy \
	serve-envoy-connector runtime-smoke-envoy self-test-modsecurity clean

build-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_metadata.sh

self-test: build-starter
	"$(BRIDGE_BIN)" --self-test

self-test-envoy-bridge: self-test

build-envoy-connector:
	BUILD_ROOT="$(BUILD_ROOT)" \
	MODSECURITY_INCLUDE_DIR="$(MODSECURITY_INCLUDE_DIR)" \
	MODSECURITY_LIB_DIR="$(MODSECURITY_LIB_DIR)" \
	MODSECURITY_LIB_FILE="$(MODSECURITY_LIB_FILE)" \
	MODSECURITY_PREFIX="$(MODSECURITY_PREFIX)" \
	CC="$(CC)" CFLAGS="$(CFLAGS)" LDFLAGS="$(LDFLAGS)" LDLIBS="$(LDLIBS)" \
	sh build/build_connector.sh

build-modsecurity-bridge: build-envoy-connector

check-envoy-config: build-envoy-connector
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

self-test-modsecurity: check-envoy-config

clean:
	rm -rf "$(BUILD_ROOT)/envoy-build-starter" "$(BUILD_ROOT)/envoy-bridge-starter" "$(BUILD_ROOT)/envoy-connector"
