BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build

.PHONY: build-starter self-test build-lighttpd-bridge build-bridge-starter \
	self-test-lighttpd-bridge self-test-bridge build-lighttpd-connector \
	check-lighttpd-config start-smoke-lighttpd runtime-smoke-lighttpd clean

build-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_starter.sh

self-test: build-starter
	BUILD_ROOT="$(BUILD_ROOT)" sh build/self_test_starter.sh

build-lighttpd-bridge:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/bridge_starter.sh

build-bridge-starter: build-lighttpd-bridge

self-test-lighttpd-bridge: build-lighttpd-bridge
	BUILD_ROOT="$(BUILD_ROOT)" sh build/self_test_bridge.sh

self-test-bridge: self-test-lighttpd-bridge

build-lighttpd-connector:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_module.sh

check-lighttpd-config: build-lighttpd-connector
	BUILD_ROOT="$(BUILD_ROOT)" sh harness/check_lighttpd_config.sh

start-smoke-lighttpd: build-lighttpd-connector
	BUILD_ROOT="$(BUILD_ROOT)" sh harness/start_lighttpd_smoke.sh

runtime-smoke-lighttpd: build-lighttpd-connector
	BUILD_ROOT="$(BUILD_ROOT)" sh harness/runtime_lighttpd_smoke.sh

clean:
	rm -rf "$(BUILD_ROOT)/lighttpd-build-starter" \
		"$(BUILD_ROOT)/lighttpd-bridge-starter" \
		"$(BUILD_ROOT)/lighttpd-connector"
