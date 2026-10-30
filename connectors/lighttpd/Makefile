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
BUILD_ROOT ?= $(if $(XDG_STATE_HOME),$(XDG_STATE_HOME),$(HOME)/.local/state)/ModSecurity-conector-build

.PHONY: build-starter self-test build-lighttpd-bridge build-bridge-starter \
	self-test-lighttpd-bridge self-test-bridge build-lighttpd-connector \
	check-lighttpd-core-patch apply-lighttpd-core-patch \
	build-lighttpd-patched-core build-lighttpd-patched-host \
	build-lighttpd-patched-connector check-lighttpd-patched-host \
	runtime-smoke-lighttpd-patched \
	build-lighttpd-stock-sidecar self-test-lighttpd-stock-sidecar \
	self-test-lighttpd-stock-real-backend \
	check-lighttpd-config start-smoke-lighttpd runtime-smoke-lighttpd \
	no-crs-baseline-lighttpd clean

build-starter:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_starter.sh

self-test: build-starter
	@test "$(ON_DEMAND_TESTS)" = 1 || { echo "FAIL: specialist self-test is archived; explicit ON_DEMAND_TESTS=1 is required" >&2; exit 2; }
	BUILD_ROOT="$(BUILD_ROOT)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/build/self_test_starter.sh"

build-lighttpd-bridge:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/bridge_starter.sh

build-bridge-starter: build-lighttpd-bridge

self-test-lighttpd-bridge:
	$(MAKE) -C ../.. framework-native-selftest NATIVE_TEST_TARGET=lighttpd-bridge

self-test-bridge: self-test-lighttpd-bridge

build-lighttpd-connector:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_module.sh

check-lighttpd-core-patch:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/apply_core_patch.sh --check

apply-lighttpd-core-patch:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/apply_core_patch.sh --apply

build-lighttpd-patched-core:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_patched_core.sh

build-lighttpd-patched-host: build-lighttpd-patched-core
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_patched_host.sh

build-lighttpd-patched-connector: build-lighttpd-patched-host

check-lighttpd-patched-host: build-lighttpd-patched-host
	BUILD_ROOT="$(BUILD_ROOT)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/harness/check_patched_lifecycle_host.sh"

runtime-smoke-lighttpd-patched: build-lighttpd-patched-host
	@if [ "$(ON_DEMAND_TESTS)" != 1 ]; then \
		[ "$${MSCONNECTOR_CRS_RUNTIME:-0}" = 1 ] || { echo "FAIL: specialist native lifecycle requires explicit ON_DEMAND_TESTS=1" >&2; exit 2; }; \
		$(ACTIVE_TEST_RUNNER) --check --execution runtime.crs.lighttpd; \
	fi
	BUILD_ROOT="$(BUILD_ROOT)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/harness/run_patched_lifecycle_smoke.sh"

build-lighttpd-stock-sidecar:
	BUILD_ROOT="$(BUILD_ROOT)" sh build/build_stock_sidecar.sh

self-test-lighttpd-stock-sidecar: build-lighttpd-stock-sidecar
ifeq ($(ON_DEMAND_TESTS),1)
	PYTHONDONTWRITEBYTECODE=1 MSCONNECTOR_STOCK_SIDECAR_BINARY="$(BUILD_ROOT)/lighttpd-stock-sidecar/lighttpd-stock-sidecar" \
		$(PYTHON) -P "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/tests/test_stock_sidecar_contract.py"
else
	$(ACTIVE_TEST_RUNNER) --group lighttpd
endif

self-test-lighttpd-stock-real-backend: build-lighttpd-stock-sidecar
	@test "$(ON_DEMAND_TESTS)" = 1 || { echo "FAIL: specialist self-test is archived; explicit ON_DEMAND_TESTS=1 is required" >&2; exit 2; }
	mkdir -p "$(BUILD_ROOT)/stock-real-backend"
	chmod 700 "$(BUILD_ROOT)/stock-real-backend"
	@test_manifest=$$($(PYTHON) -P -m connector_suite.adapters.lighttpd.build.build_runtime_begin_smoke \
		--sidecar-binary "$(BUILD_ROOT)/lighttpd-stock-sidecar/lighttpd-stock-sidecar" \
		--output-root "$(BUILD_ROOT)/stock-real-backend") || exit $$?; \
	PYTHONDONTWRITEBYTECODE=1 STOCK_SIDECAR_TEST_MANIFEST="$$test_manifest" \
		STOCK_LIGHTTPD_BIN="$(STOCK_LIGHTTPD_BIN)" \
		STOCK_LIGHTTPD_MODULE_DIR="$(STOCK_LIGHTTPD_MODULE_DIR)" \
		STOCK_SIDECAR_ARTIFACT_ATTESTATION="$(STOCK_SIDECAR_ARTIFACT_ATTESTATION)" \
		MSCONNECTOR_STOCK_SIDECAR_BINARY="$(BUILD_ROOT)/lighttpd-stock-sidecar/lighttpd-stock-sidecar" \
		STOCK_SIDECAR_RUNTIME_ROOT="$(BUILD_ROOT)/stock-real-backend" \
		STOCK_SIDECAR_RECEIPT_PATH="$(BUILD_ROOT)/stock-real-backend/real-backend-receipt.json" \
		$(PYTHON) -P "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/harness/run_stock_sidecar_real_backend.py"

check-lighttpd-config: build-lighttpd-connector
	$(if $(filter 1,$(ON_DEMAND_TESTS)),,$(error standalone lifecycle diagnostic is archived; explicit ON_DEMAND_TESTS=1 is required))
	BUILD_ROOT="$(BUILD_ROOT)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/harness/check_lighttpd_config.sh"

start-smoke-lighttpd: build-lighttpd-connector
	$(if $(filter 1,$(ON_DEMAND_TESTS)),,$(error standalone lifecycle diagnostic is archived; explicit ON_DEMAND_TESTS=1 is required))
	BUILD_ROOT="$(BUILD_ROOT)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/harness/start_lighttpd_smoke.sh"

runtime-smoke-lighttpd: build-lighttpd-connector
	@if [ "$(ON_DEMAND_TESTS)" != 1 ]; then $(ACTIVE_TEST_RUNNER) --check --execution runtime.no-crs.lighttpd; fi
	BUILD_ROOT="$(BUILD_ROOT)" sh "$(FRAMEWORK_ROOT)/connector_suite/adapters/lighttpd/harness/runtime_lighttpd_smoke.sh"

no-crs-baseline-lighttpd: export MSCONNECTOR_NO_CRS_BASELINE := 1
no-crs-baseline-lighttpd: runtime-smoke-lighttpd

clean:
	rm -rf "$(BUILD_ROOT)/lighttpd-build-starter" \
		"$(BUILD_ROOT)/lighttpd-bridge-starter" \
		"$(BUILD_ROOT)/lighttpd-connector" \
		"$(BUILD_ROOT)/lighttpd-core-patched"
