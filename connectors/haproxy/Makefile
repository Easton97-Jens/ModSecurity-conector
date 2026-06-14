CC ?= cc
CXX ?= c++
BUILD_ROOT ?= /src/ModSecurity-conector-build
REPO_ROOT ?= ../..
HAPROXY_BUILD_DIR ?= $(BUILD_ROOT)/haproxy-build-starter
HAPROXY_SPOA_RUNTIME_DIR ?= $(BUILD_ROOT)/haproxy-spoa-runtime
HAPROXY_MODSECURITY_BINDING_DIR ?= $(BUILD_ROOT)/haproxy-modsecurity-binding
COMMON_INCLUDE := $(REPO_ROOT)/common/include
COMMON_SRC := $(REPO_ROOT)/common/src
SPOA_STARTER_BIN := $(HAPROXY_BUILD_DIR)/haproxy-spoa-agent-starter
SPOA_RUNTIME_BIN := $(HAPROXY_SPOA_RUNTIME_DIR)/haproxy-modsecurity-spoa
MODSECURITY_BINDING_BIN := $(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy-modsecurity-binding-self-test
MODSECURITY_INCLUDE_CANDIDATES ?= $(MODSECURITY_INCLUDE_DIR) $(MODSECURITY_SHARED_PREFIX)/include $(BUILD_ROOT)/nginx-build/output/modsecurity/include $(BUILD_ROOT)/apache-build/output/modsecurity/include /src/ModSecurity_V3/headers
MODSECURITY_LIB_CANDIDATES ?= $(MODSECURITY_LIB_DIR) $(MODSECURITY_SHARED_PREFIX)/lib $(BUILD_ROOT)/nginx-build/output/modsecurity/lib $(BUILD_ROOT)/apache-build/output/modsecurity/lib $(BUILD_ROOT)/nginx-build/ModSecurity_V3/src/.libs $(BUILD_ROOT)/apache-build/ModSecurity_V3/src/.libs

.PHONY: build-metadata build-starter build-spoa-starter build-spoa-runtime build-modsecurity-binding self-test self-test-spoa self-test-spoa-runtime self-test-modsecurity-binding self-test-modsecurity-binding-crs clean FORCE

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
	@echo "Scope: production SPOP agent path with request phases, response headers, bounded experimental response body, audit/decision logging."

self-test-spoa-runtime: $(SPOA_RUNTIME_BIN)
	@set -eu; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	LD_LIBRARY_PATH="$$MODSECURITY_LIB_DIR:$${LD_LIBRARY_PATH:-}" "$(SPOA_RUNTIME_BIN)" --runtime-self-test --tmp-root "$(BUILD_ROOT)/tmp/haproxy" --log-root "$(BUILD_ROOT)/logs/haproxy"

build-modsecurity-binding: $(MODSECURITY_BINDING_BIN)
	@echo "HAProxy ModSecurity binding self-test built at $(MODSECURITY_BINDING_BIN)"
	@echo "Scope: libmodsecurity binding self-tests only; no HAProxy runtime enforcement or RESPONSE_BODY verification is claimed."

self-test-modsecurity-binding: $(MODSECURITY_BINDING_BIN)
	@set -eu; \
	mkdir -p "$(BUILD_ROOT)/logs/haproxy"; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	log="$(BUILD_ROOT)/logs/haproxy/modsecurity-binding-self-test.log"; \
	set +e; \
	LD_LIBRARY_PATH="$$MODSECURITY_LIB_DIR:$${LD_LIBRARY_PATH:-}" "$(MODSECURITY_BINDING_BIN)" --self-test >"$$log" 2>&1; \
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
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$(COMMON_INCLUDE)" -c metadata.c -o "$@"

$(SPOA_STARTER_BIN): src/haproxy_spoa_main.c src/haproxy_spoa_agent_starter.c src/haproxy_spoa_agent_starter.h $(COMMON_INCLUDE)/msconnector/request.h $(COMMON_INCLUDE)/msconnector/intervention.h $(COMMON_INCLUDE)/msconnector/status.h $(COMMON_SRC)/intervention.c
	@mkdir -p "$(HAPROXY_BUILD_DIR)"
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$(COMMON_INCLUDE)" -Iconnectors/haproxy/src -Isrc \
		src/haproxy_spoa_main.c src/haproxy_spoa_agent_starter.c "$(COMMON_SRC)/intervention.c" \
		-o "$@"

$(SPOA_RUNTIME_BIN): FORCE src/haproxy_spop_diagnostic_runtime.c src/haproxy_modsecurity_binding.c src/haproxy_modsecurity_binding.h $(MODSECURITY_BINDING_BIN)
	@set -eu; \
	mkdir -p "$(HAPROXY_SPOA_RUNTIME_DIR)"; \
	. "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"; \
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$$MODSECURITY_INCLUDE_DIR" -Isrc -c src/haproxy_modsecurity_binding.c -o "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_modsecurity_binding.o" || { \
		echo "BLOCKED: HAProxy ModSecurity binding source did not compile for diagnostic SPOP runtime" >&2; \
		exit 77; \
	}; \
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$$MODSECURITY_INCLUDE_DIR" -Isrc -c src/haproxy_spop_diagnostic_runtime.c -o "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_spop_diagnostic_runtime.o" || { \
		echo "BLOCKED: HAProxy ModSecurity SPOA runtime source did not compile" >&2; \
		exit 77; \
	}; \
	$(CXX) $(LDFLAGS) "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_spop_diagnostic_runtime.o" "$(HAPROXY_SPOA_RUNTIME_DIR)/haproxy_modsecurity_binding.o" -L"$$MODSECURITY_LIB_DIR" -Wl,-rpath,"$$MODSECURITY_LIB_DIR" -lmodsecurity $(LDLIBS) -o "$@" || { \
		echo "BLOCKED: HAProxy ModSecurity SPOA runtime did not link with libmodsecurity" >&2; \
		exit 77; \
	}

$(MODSECURITY_BINDING_BIN): FORCE src/haproxy_modsecurity_binding.c src/haproxy_modsecurity_binding.h src/haproxy_modsecurity_binding_self_test.c
	@set -eu; \
	mkdir -p "$(HAPROXY_MODSECURITY_BINDING_DIR)"; \
	include_dir=; \
	for candidate in $(MODSECURITY_INCLUDE_CANDIDATES); do \
		if [ -f "$$candidate/modsecurity/modsecurity.h" ] && \
				[ -f "$$candidate/modsecurity/rules_set.h" ] && \
				[ -f "$$candidate/modsecurity/transaction.h" ]; then \
			include_dir=$$candidate; \
			break; \
		fi; \
	done; \
	if [ -z "$$include_dir" ]; then \
		echo "BLOCKED: libmodsecurity headers missing under /src or BUILD_ROOT" >&2; \
		exit 77; \
	fi; \
	lib_dir=; \
	for candidate in $(MODSECURITY_LIB_CANDIDATES); do \
		if [ -f "$$candidate/libmodsecurity.so" ] || [ -f "$$candidate/libmodsecurity.a" ]; then \
			lib_dir=$$candidate; \
			break; \
		fi; \
	done; \
	if [ -z "$$lib_dir" ]; then \
		echo "BLOCKED: libmodsecurity library missing under BUILD_ROOT" >&2; \
		exit 77; \
	fi; \
	probe="$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_api.c"; \
	printf '%s\n' \
		'#include <stddef.h>' \
		'#include <stdint.h>' \
		'#include <modsecurity/modsecurity.h>' \
		'#include <modsecurity/rules_set.h>' \
		'#include <modsecurity/transaction.h>' \
		'int main(void) {' \
		'    ModSecurity *(*fn_msc_init)(void) = msc_init;' \
		'    void (*fn_msc_cleanup)(ModSecurity *) = msc_cleanup;' \
		'    void (*fn_msc_set_connector_info)(ModSecurity *, const char *) = msc_set_connector_info;' \
		'    RulesSet *(*fn_msc_create_rules_set)(void) = msc_create_rules_set;' \
		'    int (*fn_msc_rules_add)(RulesSet *, const char *, const char **) = msc_rules_add;' \
		'    int (*fn_msc_rules_add_file)(RulesSet *, const char *, const char **) = msc_rules_add_file;' \
		'    void (*fn_msc_rules_error_cleanup)(const char *) = msc_rules_error_cleanup;' \
		'    int (*fn_msc_rules_cleanup)(RulesSet *) = msc_rules_cleanup;' \
		'    Transaction *(*fn_msc_new_transaction)(ModSecurity *, RulesSet *, void *) = msc_new_transaction;' \
		'    Transaction *(*fn_msc_new_transaction_with_id)(ModSecurity *, RulesSet *, const char *, void *) = msc_new_transaction_with_id;' \
		'    int (*fn_msc_process_connection)(Transaction *, const char *, int, const char *, int) = msc_process_connection;' \
		'    int (*fn_msc_process_uri)(Transaction *, const char *, const char *, const char *) = msc_process_uri;' \
		'    int (*fn_msc_add_request_header)(Transaction *, const unsigned char *, const unsigned char *) = msc_add_request_header;' \
		'    int (*fn_msc_process_request_headers)(Transaction *) = msc_process_request_headers;' \
		'    int (*fn_msc_append_request_body)(Transaction *, const unsigned char *, size_t) = msc_append_request_body;' \
		'    int (*fn_msc_process_request_body)(Transaction *) = msc_process_request_body;' \
		'    int (*fn_msc_add_response_header)(Transaction *, const unsigned char *, const unsigned char *) = msc_add_response_header;' \
		'    int (*fn_msc_process_response_headers)(Transaction *, int, const char *) = msc_process_response_headers;' \
		'    int (*fn_msc_append_response_body)(Transaction *, const unsigned char *, size_t) = msc_append_response_body;' \
		'    int (*fn_msc_process_response_body)(Transaction *) = msc_process_response_body;' \
		'    int (*fn_msc_intervention)(Transaction *, ModSecurityIntervention *) = msc_intervention;' \
		'    void (*fn_msc_intervention_cleanup)(ModSecurityIntervention *) = msc_intervention_cleanup;' \
		'    int (*fn_msc_process_logging)(Transaction *) = msc_process_logging;' \
		'    void (*fn_msc_transaction_cleanup)(Transaction *) = msc_transaction_cleanup;' \
		'    size_t (*fn_msc_get_rules_messages_rule_ids)(const Transaction *, int64_t *, size_t) = msc_get_rules_messages_rule_ids;' \
		'    return fn_msc_init == 0 || fn_msc_cleanup == 0 || fn_msc_set_connector_info == 0 || fn_msc_create_rules_set == 0 || fn_msc_rules_add == 0 || fn_msc_rules_add_file == 0 || fn_msc_rules_error_cleanup == 0 || fn_msc_rules_cleanup == 0 || fn_msc_new_transaction == 0 || fn_msc_new_transaction_with_id == 0 || fn_msc_process_connection == 0 || fn_msc_process_uri == 0 || fn_msc_add_request_header == 0 || fn_msc_process_request_headers == 0 || fn_msc_append_request_body == 0 || fn_msc_process_request_body == 0 || fn_msc_add_response_header == 0 || fn_msc_process_response_headers == 0 || fn_msc_append_response_body == 0 || fn_msc_process_response_body == 0 || fn_msc_intervention == 0 || fn_msc_intervention_cleanup == 0 || fn_msc_process_logging == 0 || fn_msc_transaction_cleanup == 0 || fn_msc_get_rules_messages_rule_ids == 0;' \
		'}' > "$$probe"; \
	$(CC) $(CPPFLAGS) -I"$$include_dir" -Werror=implicit-function-declaration -Werror=incompatible-pointer-types -c "$$probe" -o "$(HAPROXY_MODSECURITY_BINDING_DIR)/verify_modsecurity_api.o" || { \
		echo "BLOCKED: local libmodsecurity C API signatures do not match binding requirements" >&2; \
		exit 77; \
	}; \
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$$include_dir" -Isrc -c src/haproxy_modsecurity_binding.c -o "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding.o" || { \
		echo "BLOCKED: HAProxy ModSecurity binding source did not compile" >&2; \
		exit 77; \
	}; \
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$$include_dir" -Isrc -c src/haproxy_modsecurity_binding_self_test.c -o "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding_self_test.o" || { \
		echo "BLOCKED: HAProxy ModSecurity binding self-test source did not compile" >&2; \
		exit 77; \
	}; \
	$(CXX) $(LDFLAGS) "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding.o" "$(HAPROXY_MODSECURITY_BINDING_DIR)/haproxy_modsecurity_binding_self_test.o" -L"$$lib_dir" -Wl,-rpath,"$$lib_dir" -lmodsecurity $(LDLIBS) -o "$@" || { \
		echo "BLOCKED: HAProxy ModSecurity binding self-test did not link" >&2; \
		exit 77; \
	}; \
	printf '%s\n' "MODSECURITY_INCLUDE_DIR=$$include_dir" "MODSECURITY_LIB_DIR=$$lib_dir" "MODSECURITY_BINDING_BIN=$@" > "$(HAPROXY_MODSECURITY_BINDING_DIR)/paths.env"

clean:
	rm -rf "$(HAPROXY_BUILD_DIR)" "$(HAPROXY_SPOA_RUNTIME_DIR)" "$(HAPROXY_MODSECURITY_BINDING_DIR)"

FORCE:
