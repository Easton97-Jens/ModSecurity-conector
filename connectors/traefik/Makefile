PYTHON ?= python3
TRAEFIK_NATIVE_RUNTIME_ROOT ?= $(BUILD_ROOT)/traefik-native-middleware/runtime-smoke

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
runtime-smoke-traefik-native:
	TRAEFIK_BIN="$(TRAEFIK_BIN)" \
	TRAEFIK_NATIVE_RUNTIME_ROOT="$(TRAEFIK_NATIVE_RUNTIME_ROOT)" \
	PYTHON="$(PYTHON)" sh scripts/runtime-native-middleware.sh

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
	PYTHON="$(PYTHON)" build/test-engine-service-runtime.sh

clean:
	build/build-starter.sh clean
	build/build-connector.sh clean
	build/build-native-middleware.sh clean
	build/build-engine-service.sh clean
