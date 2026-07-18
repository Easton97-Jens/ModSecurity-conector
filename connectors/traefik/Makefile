PYTHON ?= python3

# BUILD_ROOT is supplied by direct callers and the lifecycle runner. Freeze it
# before export so a command-line value cannot retain active Make syntax.
override BUILD_ROOT := $(value BUILD_ROOT)
override MODSECURITY_INCLUDE_DIR := $(value MODSECURITY_INCLUDE_DIR)
override MODSECURITY_LIB_DIR := $(value MODSECURITY_LIB_DIR)
override MODSECURITY_PREFIX := $(value MODSECURITY_PREFIX)

# Build the repository-owned default from the frozen raw BUILD_ROOT, but
# preserve a caller-provided root literally below. External text must never
# become active Make syntax.
ifeq ($(origin TRAEFIK_NATIVE_RUNTIME_ROOT), undefined)
TRAEFIK_NATIVE_RUNTIME_ROOT := $(value BUILD_ROOT)/traefik-native-middleware/runtime-smoke
else
override TRAEFIK_NATIVE_RUNTIME_ROOT := $(value TRAEFIK_NATIVE_RUNTIME_ROOT)
endif

.PHONY: build-connector build-traefik-connector build-forwardauth-service check-config check-traefik-config start-smoke start-smoke-traefik runtime-smoke runtime-smoke-traefik runtime-smoke-traefik-native no-crs-baseline-traefik build-starter build-decision-service build-forwardauth-starter self-test self-test-decision-service self-test-forwardauth build-native-middleware build-traefik-native-middleware test-native-middleware test-traefik-native-middleware check-native-middleware build-engine-service test-engine-service clean

build-connector:
	build/build-connector.sh

build-traefik-connector: build-connector build-native-middleware

build-forwardauth-service: build-connector

check-config: build-connector
	scripts/check-config.sh

check-traefik-config: check-config

start-smoke: build-connector
	scripts/start-smoke.sh

start-smoke-traefik: start-smoke

runtime-smoke: build-connector
	scripts/runtime-smoke.sh

runtime-smoke-traefik: runtime-smoke

# This route is intentionally separate from forwardAuth compatibility smoke.
# It proves the pinned Traefik host selects the local plugin and its private
# persistent UDS Common/libmodsecurity engine. It remains non-promoted targeted
# evidence rather than a capability declaration.
override TRAEFIK_BIN := $(value TRAEFIK_BIN)
override TRAEFIK_ENGINE_SOCKET_PARENT := $(value TRAEFIK_ENGINE_SOCKET_PARENT)
override PYTHON := $(value PYTHON)
export BUILD_ROOT MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR MODSECURITY_PREFIX
export TRAEFIK_BIN TRAEFIK_NATIVE_RUNTIME_ROOT TRAEFIK_ENGINE_SOCKET_PARENT PYTHON
runtime-smoke-traefik-native:
	sh scripts/runtime-native-middleware.sh

no-crs-baseline-traefik: export MSCONNECTOR_NO_CRS_BASELINE := 1
no-crs-baseline-traefik: runtime-smoke-traefik

build-starter:
	build/build-starter.sh build-starter

build-decision-service:
	build/build-starter.sh build-decision-service

build-forwardauth-starter: build-connector

self-test: self-test-decision-service

self-test-decision-service:
	build/build-starter.sh self-test-decision-service

self-test-forwardauth: self-test-decision-service

# The native Go middleware is selected only by the separate non-promoted
# full-lifecycle host probe. These source-build targets never start its engine
# or replace/invoke the C forwardAuth compatibility service targets above.
build-native-middleware:
	build/build-native-middleware.sh build

build-traefik-native-middleware: build-native-middleware

test-native-middleware:
	build/build-native-middleware.sh test

test-traefik-native-middleware: test-native-middleware

check-native-middleware: test-native-middleware

build-engine-service:
	build/build-engine-service.sh build

test-engine-service:
	build/build-engine-service.sh test
	build/test-engine-service-runtime.sh

clean:
	build/build-starter.sh clean
	build/build-connector.sh clean
	build/build-native-middleware.sh clean
	build/build-engine-service.sh clean
