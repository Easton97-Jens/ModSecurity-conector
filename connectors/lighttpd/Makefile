BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build

.PHONY: build-starter self-test build-lighttpd-bridge build-bridge-starter \
	self-test-lighttpd-bridge self-test-bridge build-lighttpd-connector \
	check-lighttpd-core-patch apply-lighttpd-core-patch \
	build-lighttpd-patched-connector \
	check-lighttpd-config start-smoke-lighttpd runtime-smoke-lighttpd \
	no-crs-baseline-lighttpd clean

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

check-lighttpd-core-patch:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/apply_core_patch.sh --check

apply-lighttpd-core-patch:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/apply_core_patch.sh --apply

build-lighttpd-patched-connector: apply-lighttpd-core-patch
	BUILD_ROOT="$(BUILD_ROOT)" \
	LIGHTTPD_MSCONNECTOR_CORE_MODE=patched \
	LIGHTTPD_SOURCE_DIR="$(BUILD_ROOT)/lighttpd-core-patched/lighttpd-1.4.84" \
	sh build/build_module.sh

check-lighttpd-config: build-lighttpd-connector
	BUILD_ROOT="$(BUILD_ROOT)" sh harness/check_lighttpd_config.sh

start-smoke-lighttpd: build-lighttpd-connector
	BUILD_ROOT="$(BUILD_ROOT)" sh harness/start_lighttpd_smoke.sh

runtime-smoke-lighttpd: build-lighttpd-connector
	BUILD_ROOT="$(BUILD_ROOT)" sh harness/runtime_lighttpd_smoke.sh

no-crs-baseline-lighttpd: export MSCONNECTOR_NO_CRS_BASELINE := 1
no-crs-baseline-lighttpd: runtime-smoke-lighttpd

clean:
	rm -rf "$(BUILD_ROOT)/lighttpd-build-starter" \
		"$(BUILD_ROOT)/lighttpd-bridge-starter" \
		"$(BUILD_ROOT)/lighttpd-connector" \
		"$(BUILD_ROOT)/lighttpd-core-patched"
