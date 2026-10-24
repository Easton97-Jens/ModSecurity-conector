CC ?= cc
CXX ?= c++
BUILD_ROOT ?= /src/ModSecurity-conector-build
REPO_ROOT ?= ../..
FRAMEWORK_ROOT ?= $(REPO_ROOT)/modules/ModSecurity-test-Framework
HAPROXY_BUILD_DIR ?= $(BUILD_ROOT)/haproxy-build-starter
HAPROXY_SPOA_RUNTIME_DIR ?= $(BUILD_ROOT)/haproxy-spoa-runtime
HAPROXY_MODSECURITY_BINDING_DIR ?= $(BUILD_ROOT)/haproxy-modsecurity-binding
HAPROXY_HTX_RUNTIME_ROOT ?= $(BUILD_ROOT)/haproxy-htx-runtime-smoke
HAPROXY_HTX_BUILD_DIR ?= $(HAPROXY_HTX_RUNTIME_ROOT)/overlay-build
HAPROXY_HTX_BIN ?= $(HAPROXY_HTX_BUILD_DIR)/worktree/haproxy
HAPROXY_HTX_EVENT_LOG_PATH ?= $(HAPROXY_HTX_RUNTIME_ROOT)/events.jsonl
HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH ?= $(HAPROXY_HTX_RUNTIME_ROOT)/host-runtime-evidence.jsonl
HAPROXY_HTX_CANONICAL_RULES_FILE ?= $(FRAMEWORK_ROOT)/tests/rules/no-crs-baseline.conf
COMMON_INCLUDE := $(REPO_ROOT)/common/include
COMMON_SRC := $(REPO_ROOT)/common/src
COMMON_CPPFLAGS := -I$(COMMON_INCLUDE)
REPO_ROOT_CPPFLAGS := -I$(abspath $(REPO_ROOT))
PROFILE_REGISTRY_SOURCE := $(REPO_ROOT)/connectors/profile_registry.c
COMMON_SDK_SRCS := $(COMMON_SRC)/config.c $(COMMON_SRC)/config_parser.c $(COMMON_SRC)/directive_spec.c $(COMMON_SRC)/directive_adapter.c $(COMMON_SRC)/request_helpers.c $(COMMON_SRC)/response_helpers.c $(COMMON_SRC)/request_mapper_contract.c $(COMMON_SRC)/response_mapper_contract.c $(COMMON_SRC)/headers.c $(COMMON_SRC)/event.c $(COMMON_SRC)/event_jsonl.c $(COMMON_SRC)/json_escape.c $(COMMON_SRC)/rule_id.c $(COMMON_SRC)/log_sanitize.c $(COMMON_SRC)/redaction.c $(COMMON_SRC)/resource_limits.c $(COMMON_SRC)/dos_guard.c $(COMMON_SRC)/error.c $(COMMON_SRC)/status.c $(COMMON_SRC)/body_policy.c $(COMMON_SRC)/crs.c $(COMMON_SRC)/memory.c $(COMMON_SRC)/modsecurity_engine.c $(COMMON_SRC)/transaction_id.c $(COMMON_SRC)/transaction_state.c $(COMMON_SRC)/decision.c $(COMMON_SRC)/decision_action.c $(COMMON_SRC)/late_intervention.c $(COMMON_SRC)/flow_guard.c $(COMMON_SRC)/integrity_event.c $(COMMON_SRC)/rule_loader.c $(COMMON_SRC)/rule_merge.c $(COMMON_SRC)/http_status.c $(COMMON_SRC)/block_statuses.c $(COMMON_SRC)/path_policy.c $(COMMON_SRC)/intervention.c $(COMMON_SRC)/rule_error.c $(COMMON_SRC)/rule_event.c $(COMMON_SRC)/artifacts.c $(COMMON_SRC)/artifact_layout.c $(COMMON_SRC)/test_result.c $(COMMON_SRC)/test_result_json.c
RESPONSE_COMPANION_SRCS := $(REPO_ROOT)/common/runtime/msconnector_runtime.c $(REPO_ROOT)/common/runtime/response_companion_transport.c $(REPO_ROOT)/common/runtime/response_companion_client.c $(PROFILE_REGISTRY_SOURCE) src/haproxy_spop_response_companion_backend.c
SPOA_STARTER_BIN := $(HAPROXY_BUILD_DIR)/haproxy-spoa-agent-starter
SPOA_RUNTIME_BIN := $(HAPROXY_SPOA_RUNTIME_DIR)/haproxy-modsecurity-spoa
MODSECURITY_BINDING_BIN := $(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy-modsecurity-binding-self-test
MODSECURITY_BINDING_LIFECYCLE_RULES := $(abspath harness/fixtures/modsecurity-binding-lifecycle.conf)
MODSECURITY_INCLUDE_CANDIDATES ?= $(MODSECURITY_INCLUDE_DIR) $(MODSECURITY_SHARED_PREFIX)/include $(BUILD_ROOT)/nginx-build/output/modsecurity/include $(BUILD_ROOT)/apache-build/output/modsecurity/include /src/ModSecurity_V3/headers
MODSECURITY_LIB_CANDIDATES ?= $(MODSECURITY_LIB_DIR) $(MODSECURITY_SHARED_PREFIX)/lib $(BUILD_ROOT)/nginx-build/output/modsecurity/lib $(BUILD_ROOT)/apache-build/output/modsecurity/lib $(BUILD_ROOT)/nginx-build/ModSecurity_V3/src/.libs $(BUILD_ROOT)/apache-build/ModSecurity_V3/src/.libs
MODSECURITY_RESOLUTION_FILE ?= $(BUILD_ROOT)/haproxy-modsecurity-binding/modsecurity-resolution.env

# Shared read-only host-runtime gate. These snapshots are exported to the
# recursive root make; the recipe itself contains no caller-controlled shell
# interpolation.
ifeq ($(origin HAPROXY_HOSTRUNTIME_PROFILE), undefined)
HAPROXY_HOSTRUNTIME_PROFILE := haproxy-htx
endif
# Do not inspect the caller-provided profile in Make conditionals. The root
# checker validates the raw profile after safe argument transport; callers may
# select narrower runtime and binary roots explicitly when needed.
override HAPROXY_HOSTRUNTIME_DEFAULT_ROOT := $(abspath $(BUILD_ROOT)/hostruntime/haproxy)
ifeq ($(origin HAPROXY_HOSTRUNTIME_LOCK), undefined)
HAPROXY_HOSTRUNTIME_LOCK := $(abspath $(FRAMEWORK_ROOT)/ci/provisioning/runtime-component-lock.json)
endif
ifeq ($(origin HAPROXY_HOSTRUNTIME_RUNTIME_ROOT), undefined)
HAPROXY_HOSTRUNTIME_RUNTIME_ROOT := $(abspath $(HAPROXY_HOSTRUNTIME_DEFAULT_ROOT))
endif
ifeq ($(origin HAPROXY_HOSTRUNTIME_BINARY_ROOT), undefined)
HAPROXY_HOSTRUNTIME_BINARY_ROOT := $(abspath $(HAPROXY_HOSTRUNTIME_DEFAULT_ROOT))
endif
ifeq ($(origin HAPROXY_HOSTRUNTIME_EXPECTED_VERSION), undefined)
HAPROXY_HOSTRUNTIME_EXPECTED_VERSION :=
endif
ifeq ($(origin HAPROXY_HOSTRUNTIME_BINARY), undefined)
HAPROXY_HOSTRUNTIME_BINARY :=
endif
ifeq ($(origin HAPROXY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR), undefined)
HAPROXY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR := $(abspath $(HAPROXY_HOSTRUNTIME_DEFAULT_ROOT)/preflight)
endif
# Command-line hostruntime values are transported explicitly by the wrapper.
# Prevent GNU Make from expanding and auto-exporting their raw text first.
unexport HAPROXY_HOSTRUNTIME_PROFILE HAPROXY_HOSTRUNTIME_LOCK \
	HAPROXY_HOSTRUNTIME_EXPECTED_VERSION HAPROXY_HOSTRUNTIME_BINARY \
	HAPROXY_HOSTRUNTIME_LOCK_ROOT HAPROXY_HOSTRUNTIME_RUNTIME_ROOT \
	HAPROXY_HOSTRUNTIME_BINARY_ROOT HAPROXY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR

.PHONY: build-metadata build-starter build-spoa-starter build-spoa-runtime build-modsecurity-binding build-htx-overlay check-htx-overlay test-htx-overlay runtime-smoke-haproxy-htx hostruntime-preflight-haproxy hostruntime-preflight-haproxy-htx hostruntime-preflight-haproxy-spoe-spop self-test self-test-spoa self-test-spoa-runtime self-test-modsecurity-binding self-test-modsecurity-binding-crs clean FORCE

# Take variable names, not their values: this preserves caller text as data,
# doubles Make metacharacters for the child Make process, and shell-quotes the
# resulting environment assignments as one argument each.
hostruntime_wrapper_escape_dollars = $(subst $$,$$$$,$(value $(1)))
hostruntime_wrapper_safe_quote = '$(subst ','"'"',$(call hostruntime_wrapper_escape_dollars,$(1)))'
hostruntime-preflight-haproxy:
	env \
		MAKEFLAGS=$(call hostruntime_wrapper_safe_quote,MFLAGS) \
		MAKEOVERRIDES='' \
		HOSTRUNTIME_CONNECTOR='haproxy' \
		HOSTRUNTIME_PROFILE=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_PROFILE) \
		HOSTRUNTIME_EXPECTED_VERSION=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_EXPECTED_VERSION) \
		HOSTRUNTIME_BINARY=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_BINARY) \
		HOSTRUNTIME_BINARY_ROOT=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_BINARY_ROOT) \
		HOSTRUNTIME_LOCK=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_LOCK) \
		HOSTRUNTIME_LOCK_PROFILE=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_PROFILE) \
		HOSTRUNTIME_RUNTIME_ROOT=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_RUNTIME_ROOT) \
		HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR=$(call hostruntime_wrapper_safe_quote,HAPROXY_HOSTRUNTIME_PREFLIGHT_OUTPUT_DIR) \
		$(MAKE) -C ../.. hostruntime-preflight

hostruntime-preflight-haproxy-htx:
	$(MAKE) HAPROXY_HOSTRUNTIME_PROFILE=haproxy-htx hostruntime-preflight-haproxy

hostruntime-preflight-haproxy-spoe-spop:
	$(MAKE) HAPROXY_HOSTRUNTIME_PROFILE=haproxy-spoe-spop hostruntime-preflight-haproxy

build-metadata: $(HAPROXY_BUILD_DIR)/metadata.o
	@echo "HAProxy build-starter: metadata object built at $(HAPROXY_BUILD_DIR)/metadata.o"
	@echo "HAProxy build-starter only; no HAProxy API, SPOE/SPOA protocol, libmodsecurity, or runtime adapter is built."

build-starter: build-metadata build-spoa-starter
	@echo "HAProxy starter build complete: metadata object and SPOA agent starter binary built."
	@echo "Scope: local starter binaries only; no HAProxy runtime compatibility is claimed."

build-spoa-starter: $(SPOA_STARTER_BIN)
	@echo "HAProxy SPOA agent starter built at $(SPOA_STARTER_BIN)"
	@echo "Scope: local request-decision starter only; no SPOP frame parser or HAProxy runtime harness is built."

self-test: self-test-spoa

self-test-spoa: $(SPOA_STARTER_BIN)
	"$(SPOA_STARTER_BIN)" --self-test

build-spoa-runtime: $(SPOA_RUNTIME_BIN)
	@echo "HAProxy ModSecurity SPOA production agent built at $(SPOA_RUNTIME_BIN)"
	@echo "Scope: selected SPOP agent path with request phases, response headers, and audit/decision logging; response-body Phase 4 is disabled."

self-test-spoa-runtime: $(SPOA_RUNTIME_BIN)
	@set -eu; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	LD_LIBRARY_PATH="$$MODSECURITY_LIB_DIR:$${LD_LIBRARY_PATH:-}" "$(SPOA_RUNTIME_BIN)" --runtime-self-test --tmp-root "$(BUILD_ROOT)/tmp/haproxy" --log-root "$(BUILD_ROOT)/logs/haproxy"

build-modsecurity-binding: $(MODSECURITY_BINDING_BIN)
	@echo "HAProxy ModSecurity binding self-test built at $(MODSECURITY_BINDING_BIN)"
	@echo "Scope: libmodsecurity binding self-tests only; no HAProxy runtime enforcement or RESPONSE_BODY verification is claimed."

check-htx-overlay:
	python3 "$(REPO_ROOT)/ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py"

test-htx-overlay: check-htx-overlay
	python3 harness/test_haproxy_htx_smoke_helper.py

build-htx-overlay: check-htx-overlay build-modsecurity-binding
	@set -eu; \
	source_dir="$(HAPROXY_HTX_SOURCE_DIR)"; \
	build_dir="$(HAPROXY_HTX_BUILD_DIR)"; \
	: "$${source_dir:?set HAPROXY_HTX_SOURCE_DIR to a verified HAProxy source tree}"; \
	: "$${build_dir:?set HAPROXY_HTX_BUILD_DIR to an empty path outside the checkout}"; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	CONNECTOR_ROOT="$(abspath $(REPO_ROOT))" \
	HAPROXY_HTX_SOURCE_DIR="$$source_dir" \
	HAPROXY_HTX_BUILD_DIR="$$build_dir" \
	MODSECURITY_INCLUDE_DIR="$$MODSECURITY_INCLUDE_DIR" \
	MODSECURITY_LIB_DIR="$$MODSECURITY_LIB_DIR" \
	HAPROXY_MODSECURITY_BINDING_CPPFLAGS="$$HAPROXY_MODSECURITY_BINDING_CPPFLAGS" \
	MAKE_JOBS="$${MAKE_JOBS:-2}" \
	sh htx-overlay/build-overlay.sh

# This target is deliberately independent of runtime-smoke-haproxy and the
# selected SPOE/SPOP path. It uses the Framework's canonical No-CRS rules for
# real host requests and proves local P1/P3 native replies (including 429).
# It remains non-promoted until a Common-runtime bridge and canonical evidence
# selection approve the path; P2/P4 are recorded only as host observations.
runtime-smoke-haproxy-htx: test-htx-overlay build-htx-overlay
	HAPROXY_BIN="$(HAPROXY_HTX_BIN)" \
	RUNTIME_ROOT="$(HAPROXY_HTX_RUNTIME_ROOT)" \
	EVENT_LOG_PATH="$(HAPROXY_HTX_EVENT_LOG_PATH)" \
	HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH="$(HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH)" \
	FRAMEWORK_ROOT="$(FRAMEWORK_ROOT)" \
	HAPROXY_HTX_CANONICAL_RULES_FILE="$(abspath $(HAPROXY_HTX_CANONICAL_RULES_FILE))" \
	PYTHON="$(PYTHON)" sh harness/run_haproxy_htx_runtime.sh

self-test-modsecurity-binding: $(MODSECURITY_BINDING_BIN)
	@set -eu; \
	mkdir -p "$(BUILD_ROOT)/logs/haproxy"; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	log="$(BUILD_ROOT)/logs/haproxy/modsecurity-binding-self-test.log"; \
	set +e; \
	LD_LIBRARY_PATH="$$MODSECURITY_LIB_DIR:$${LD_LIBRARY_PATH:-}" "$(MODSECURITY_BINDING_BIN)" --self-test "$(MODSECURITY_BINDING_LIFECYCLE_RULES)" >"$$log" 2>&1; \
	rc=$$?; \
	set -e; \
	cat "$$log"; \
	exit "$$rc"

self-test-modsecurity-binding-crs: $(MODSECURITY_BINDING_BIN)
	@set -eu; \
	mkdir -p "$(BUILD_ROOT)/logs/haproxy"; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	preamble="$${MODSECURITY_RULE_PREAMBLE_FILE:-$(BUILD_ROOT)/crs/modsecurity-crs-preamble.conf}"; \
	log="$(BUILD_ROOT)/logs/haproxy/modsecurity-binding-crs-self-test.log"; \
	if [ ! -f "$$preamble" ]; then \
		echo "BLOCKED: CRS preamble missing: $$preamble" | tee "$$log"; \
		exit 77; \
	fi; \
	set +e; \
	LD_LIBRARY_PATH="$$MODSECURITY_LIB_DIR:$${LD_LIBRARY_PATH:-}" "$(MODSECURITY_BINDING_BIN)" --self-test-crs "$$preamble" >"$$log" 2>&1; \
	rc=$$?; \
	set -e; \
	cat "$$log"; \
	exit "$$rc"

$(HAPROXY_BUILD_DIR)/metadata.o: metadata.c metadata.h $(COMMON_INCLUDE)/msconnector/origin.h
	@mkdir -p "$(HAPROXY_BUILD_DIR)"
	$(CC) $(CPPFLAGS) $(COMMON_CPPFLAGS) $(CFLAGS) -c metadata.c -o "$@"

$(SPOA_STARTER_BIN): src/haproxy_spoa_main.c src/haproxy_spoa_agent_starter.c src/haproxy_spoa_agent_starter.h $(COMMON_INCLUDE)/msconnector/request.h $(COMMON_INCLUDE)/msconnector/intervention.h $(COMMON_INCLUDE)/msconnector/status.h $(COMMON_SRC)/intervention.c
	@mkdir -p "$(HAPROXY_BUILD_DIR)"
	$(CC) $(CPPFLAGS) $(COMMON_CPPFLAGS) $(CFLAGS) -Iconnectors/haproxy/src -Isrc \
		src/haproxy_spoa_main.c src/haproxy_spoa_agent_starter.c "$(COMMON_SRC)/intervention.c" \
		-o "$@"

$(SPOA_RUNTIME_BIN): FORCE src/haproxy_spop_diagnostic_runtime.c src/haproxy_modsecurity_binding.c src/haproxy_modsecurity_binding.h src/haproxy_modsecurity_mapper.c src/haproxy_modsecurity_mapper.h $(COMMON_SDK_SRCS) $(RESPONSE_COMPANION_SRCS) $(MODSECURITY_BINDING_BIN)
	@set -eu; \
	mkdir -p "$(HAPROXY_SPOA_RUNTIME_DIR)"; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	$(CC) $(CPPFLAGS) $(CFLAGS) $$HAPROXY_MODSECURITY_BINDING_CPPFLAGS -I"$$MODSECURITY_INCLUDE_DIR" $(REPO_ROOT_CPPFLAGS) $(COMMON_CPPFLAGS) -Isrc -c src/haproxy_modsecurity_binding.c -o "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_modsecurity_binding.o" || { \
		echo "FAIL: HAProxy ModSecurity binding source did not compile for diagnostic SPOP runtime" >&2; \
		exit 1; \
	}; \
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$$MODSECURITY_INCLUDE_DIR" $(COMMON_CPPFLAGS) -I"$(REPO_ROOT)/common/runtime" -Isrc -c src/haproxy_spop_diagnostic_runtime.c -o "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_spop_diagnostic_runtime.o" || { \
		echo "FAIL: HAProxy ModSecurity SPOA runtime source did not compile" >&2; \
		exit 1; \
	}; \
	common_objects=""; \
	for src in src/haproxy_modsecurity_mapper.c $(COMMON_SDK_SRCS) $(RESPONSE_COMPANION_SRCS); do \
		obj="$(HAPROXY_SPOA_RUNTIME_DIR)/$$(printf '%s' "$$src" | tr '/.' '__').o"; \
		$(CC) $(CPPFLAGS) $(COMMON_CPPFLAGS) $(CFLAGS) -I"$$MODSECURITY_INCLUDE_DIR" -I"$(REPO_ROOT)/common/runtime" -Isrc -c "$$src" -o "$$obj" || { \
			echo "FAIL: HAProxy Common SDK source did not compile: $$src" >&2; \
			exit 1; \
		}; \
		common_objects="$$common_objects $$obj"; \
	done; \
	$(CXX) $(LDFLAGS) "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_spop_diagnostic_runtime.o" "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_modsecurity_binding.o" $$common_objects "$$MODSECURITY_LIBRARY" -Wl,-rpath,"$$MODSECURITY_LIB_DIR" $(LDLIBS) -o "$@" || { \
		echo "FAIL: HAProxy ModSecurity SPOA runtime did not link with libmodsecurity" >&2; \
		exit 1; \
	}

$(MODSECURITY_BINDING_BIN): FORCE src/haproxy_modsecurity_binding.c src/haproxy_modsecurity_binding.h src/haproxy_modsecurity_mapper.c src/haproxy_modsecurity_mapper.h src/haproxy_modsecurity_binding_self_test.c $(MODSECURITY_BINDING_LIFECYCLE_RULES) $(COMMON_SDK_SRCS) $(PROFILE_REGISTRY_SOURCE)
	@set -eu; \
	mkdir -p "$(HAPROXY_MODSECURITY_BINDING_DIR)"; \
	resolver_include="$${MODSECURITY_INCLUDE_DIR:-}"; \
	if [ -z "$$resolver_include" ]; then \
		for candidate in $(MODSECURITY_INCLUDE_CANDIDATES); do \
			if [ -f "$$candidate/modsecurity/modsecurity.h" ]; then resolver_include="$$candidate"; break; fi; \
		done; \
	fi; \
	resolver_lib="$${MODSECURITY_LIB_DIR:-}"; \
	if [ -z "$$resolver_lib" ]; then \
		for candidate in $(MODSECURITY_LIB_CANDIDATES); do \
			if [ -f "$$candidate/libmodsecurity.so" ] || [ -f "$$candidate/libmodsecurity.a" ] || ls "$$candidate"/libmodsecurity.so.* >/dev/null 2>&1; then resolver_lib="$$candidate"; break; fi; \
		done; \
	fi; \
	MODSECURITY_INCLUDE_DIR="$$resolver_include" MODSECURITY_LIB_DIR="$$resolver_lib" \
		sh "$(abspath htx-overlay/resolve-modsecurity.sh)" "$(MODSECURITY_RESOLUTION_FILE)"; \
	. "$(MODSECURITY_RESOLUTION_FILE)"; \
	include_dir="$$MODSECURITY_INCLUDE_DIR"; \
	lib_dir="$$MODSECURITY_LIB_DIR"; \
	modsecurity_library="$$MODSECURITY_LIBRARY"; \
	baseline_probe="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_baseline_api.c"; \
	baseline_object="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_baseline_api.o"; \
	baseline_binary="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_baseline_api"; \
	optional_probe="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_optional_rule_ids_api.c"; \
	optional_object="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_optional_rule_ids_api.o"; \
	optional_binary="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_optional_rule_ids_api"; \
	optional_compile_log="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_optional_rule_ids_compile.log"; \
	optional_link_log="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_optional_rule_ids_link.log"; \
	binding_cppflags=; \
	optional_rule_ids_api=unavailable; \
	printf '%s\n' \
		'#include <stddef.h>' \
		'#include <stdint.h>' \
		'#include <modsecurity/modsecurity.h>' \
		'#include <modsecurity/rules_set.h>' \
		'#include <modsecurity/transaction.h>' \
		'static ModSecurity *(*volatile fn_msc_init)(void) = msc_init;' \
		'static void (*volatile fn_msc_cleanup)(ModSecurity *) = msc_cleanup;' \
		'static void (*volatile fn_msc_set_connector_info)(ModSecurity *, const char *) = msc_set_connector_info;' \
		'static RulesSet *(*volatile fn_msc_create_rules_set)(void) = msc_create_rules_set;' \
		'static int (*volatile fn_msc_rules_add)(RulesSet *, const char *, const char **) = msc_rules_add;' \
		'static int (*volatile fn_msc_rules_add_file)(RulesSet *, const char *, const char **) = msc_rules_add_file;' \
		'static void (*volatile fn_msc_rules_error_cleanup)(const char *) = msc_rules_error_cleanup;' \
		'static int (*volatile fn_msc_rules_cleanup)(RulesSet *) = msc_rules_cleanup;' \
		'static Transaction *(*volatile fn_msc_new_transaction)(ModSecurity *, RulesSet *, void *) = msc_new_transaction;' \
		'static Transaction *(*volatile fn_msc_new_transaction_with_id)(ModSecurity *, RulesSet *, const char *, void *) = msc_new_transaction_with_id;' \
		'static int (*volatile fn_msc_process_connection)(Transaction *, const char *, int, const char *, int) = msc_process_connection;' \
		'static int (*volatile fn_msc_process_uri)(Transaction *, const char *, const char *, const char *) = msc_process_uri;' \
		'static int (*volatile fn_msc_add_request_header)(Transaction *, const unsigned char *, const unsigned char *) = msc_add_request_header;' \
		'static int (*volatile fn_msc_process_request_headers)(Transaction *) = msc_process_request_headers;' \
		'static int (*volatile fn_msc_append_request_body)(Transaction *, const unsigned char *, size_t) = msc_append_request_body;' \
		'static int (*volatile fn_msc_process_request_body)(Transaction *) = msc_process_request_body;' \
		'static int (*volatile fn_msc_add_response_header)(Transaction *, const unsigned char *, const unsigned char *) = msc_add_response_header;' \
		'static int (*volatile fn_msc_process_response_headers)(Transaction *, int, const char *) = msc_process_response_headers;' \
		'static int (*volatile fn_msc_append_response_body)(Transaction *, const unsigned char *, size_t) = msc_append_response_body;' \
		'static int (*volatile fn_msc_process_response_body)(Transaction *) = msc_process_response_body;' \
		'static int (*volatile fn_msc_intervention)(Transaction *, ModSecurityIntervention *) = msc_intervention;' \
		'static void (*volatile fn_msc_intervention_cleanup)(ModSecurityIntervention *) = msc_intervention_cleanup;' \
		'static int (*volatile fn_msc_process_logging)(Transaction *) = msc_process_logging;' \
		'static void (*volatile fn_msc_transaction_cleanup)(Transaction *) = msc_transaction_cleanup;' \
		'int main(void) {' \
		'    return fn_msc_init == 0 || fn_msc_cleanup == 0 || fn_msc_set_connector_info == 0 || fn_msc_create_rules_set == 0 || fn_msc_rules_add == 0 || fn_msc_rules_add_file == 0 || fn_msc_rules_error_cleanup == 0 || fn_msc_rules_cleanup == 0 || fn_msc_new_transaction == 0 || fn_msc_new_transaction_with_id == 0 || fn_msc_process_connection == 0 || fn_msc_process_uri == 0 || fn_msc_add_request_header == 0 || fn_msc_process_request_headers == 0 || fn_msc_append_request_body == 0 || fn_msc_process_request_body == 0 || fn_msc_add_response_header == 0 || fn_msc_process_response_headers == 0 || fn_msc_append_response_body == 0 || fn_msc_process_response_body == 0 || fn_msc_intervention == 0 || fn_msc_intervention_cleanup == 0 || fn_msc_process_logging == 0 || fn_msc_transaction_cleanup == 0;' \
		'}' > "$$baseline_probe"; \
	printf '%s\n' \
		'#include <stddef.h>' \
		'#include <stdint.h>' \
		'#include <modsecurity/modsecurity.h>' \
		'#include <modsecurity/transaction.h>' \
		'static size_t (*volatile fn_msc_get_rules_messages_rule_ids)(const Transaction *, int64_t *, size_t) = msc_get_rules_messages_rule_ids;' \
		'int main(void) {' \
		'    return fn_msc_get_rules_messages_rule_ids == 0;' \
		'}' > "$$optional_probe"; \
	if ! $(CC) $(CPPFLAGS) -I"$$include_dir" -Werror=implicit-function-declaration -Werror=incompatible-pointer-types -c "$$baseline_probe" -o "$$baseline_object"; then \
		echo "FAIL: The HAProxy connector requires the public libModSecurity API available in version 3.0.14 or newer. The detected headers and library do not provide the required baseline API or do not match." >&2; \
		exit 1; \
	fi; \
	if ! $(CXX) $(LDFLAGS) "$$baseline_object" "$$modsecurity_library" -Wl,-rpath,"$$lib_dir" $(LDLIBS) -o "$$baseline_binary"; then \
		echo "FAIL: The HAProxy connector requires the public libModSecurity API available in version 3.0.14 or newer. The detected headers and library do not provide the required baseline API or do not match." >&2; \
		exit 1; \
	fi; \
	if $(CC) $(CPPFLAGS) -I"$$include_dir" -Werror=implicit-function-declaration -Werror=incompatible-pointer-types -c "$$optional_probe" -o "$$optional_object" > "$$optional_compile_log" 2>&1; then \
		if $(CXX) $(LDFLAGS) "$$optional_object" "$$modsecurity_library" -Wl,-rpath,"$$lib_dir" $(LDLIBS) -o "$$optional_binary" > "$$optional_link_log" 2>&1; then \
			binding_cppflags=-DHAPROXY_HAVE_MSC_GET_RULES_MESSAGES_RULE_IDS=1; \
			optional_rule_ids_api=available; \
			echo "INFO: msc_get_rules_messages_rule_ids compile-and-link probe passed; enabling optional Rule-ID metadata."; \
		else \
			echo "INFO: msc_get_rules_messages_rule_ids declaration compiled but the selected library did not link it; using the supported 3.0.14 baseline Rule-ID path."; \
			sed -n '1,8p' "$$optional_link_log"; \
		fi; \
	else \
		echo "INFO: msc_get_rules_messages_rule_ids is unavailable for the selected libModSecurity headers; using the supported 3.0.14 baseline Rule-ID path."; \
		sed -n '1,8p' "$$optional_compile_log"; \
	fi; \
	$(CC) $(CPPFLAGS) $(CFLAGS) $$binding_cppflags -I"$$include_dir" $(REPO_ROOT_CPPFLAGS) $(COMMON_CPPFLAGS) -Isrc -c src/haproxy_modsecurity_binding.c -o "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding.o" || { \
		echo "FAIL: HAProxy ModSecurity binding source did not compile" >&2; \
		exit 1; \
	}; \
	$(CC) $(CPPFLAGS) $(CFLAGS) $$binding_cppflags -I"$$include_dir" $(COMMON_CPPFLAGS) -Isrc -c src/haproxy_modsecurity_binding_self_test.c -o "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding_self_test.o" || { \
		echo "FAIL: HAProxy ModSecurity binding self-test source did not compile" >&2; \
		exit 1; \
	}; \
	common_objects=""; \
	for src in src/haproxy_modsecurity_mapper.c $(COMMON_SDK_SRCS) $(PROFILE_REGISTRY_SOURCE); do \
		obj="$(HAPROXY_MODSECURITY_BINDING_DIR)/$$(printf '%s' "$$src" | tr '/.' '__').o"; \
		$(CC) $(CPPFLAGS) $(COMMON_CPPFLAGS) $(CFLAGS) -Isrc -c "$$src" -o "$$obj" || { \
			echo "FAIL: HAProxy Common SDK source did not compile: $$src" >&2; \
			exit 1; \
		}; \
		common_objects="$$common_objects $$obj"; \
	done; \
	$(CXX) $(LDFLAGS) "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding.o" "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding_self_test.o" $$common_objects "$$modsecurity_library" -Wl,-rpath,"$$lib_dir" $(LDLIBS) -o "$@" || { \
		echo "FAIL: HAProxy ModSecurity binding self-test did not link" >&2; \
		exit 1; \
	}; \
	printf '%s\n' "MODSECURITY_INCLUDE_DIR=$$include_dir" "MODSECURITY_LIB_DIR=$$lib_dir" "MODSECURITY_LIBRARY=$$modsecurity_library" "HAPROXY_MODSECURITY_RULE_IDS_API=$$optional_rule_ids_api" "HAPROXY_MODSECURITY_BINDING_CPPFLAGS=$$binding_cppflags" "MODSECURITY_BINDING_BIN=$@" > "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"

clean:
	rm -rf "$(HAPROXY_BUILD_DIR)" "$(HAPROXY_SPOA_RUNTIME_DIR)" "$(HAPROXY_MODSECURITY_BINDING_DIR)" "$(HAPROXY_HTX_RUNTIME_ROOT)"

FORCE:
