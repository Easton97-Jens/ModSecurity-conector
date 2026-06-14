BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build
BRIDGE_BIN := $(BUILD_ROOT)/envoy-bridge-starter/envoy_bridge

.PHONY: build-starter self-test build-modsecurity-bridge self-test-modsecurity clean

build-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_metadata.sh

self-test: build-starter
	"$(BRIDGE_BIN)" --self-test

build-modsecurity-bridge:
	@echo "envoy_modsecurity_bridge: BLOCKED - libmodsecurity headers/libs were not found under /src/ModSecurity-conector-build or /src/ModSecurity_V3"
	@exit 77

self-test-modsecurity: build-modsecurity-bridge

clean:
	rm -rf "$(BUILD_ROOT)/envoy-build-starter" "$(BUILD_ROOT)/envoy-bridge-starter"
