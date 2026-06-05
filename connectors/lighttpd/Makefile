BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build

.PHONY: build-starter self-test build-bridge-starter self-test-bridge clean

build-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_starter.sh

self-test: build-starter

build-bridge-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/bridge_starter.sh

self-test-bridge: build-bridge-starter

clean:
	rm -rf "$(BUILD_ROOT)/lighttpd-build-starter" "$(BUILD_ROOT)/lighttpd-bridge-starter"
