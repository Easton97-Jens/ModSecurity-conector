CC ?= cc
BUILD_ROOT ?= $(HOME)/.local/state/ModSecurity-conector-build
REPO_ROOT ?= ../..
HAPROXY_BUILD_DIR ?= $(BUILD_ROOT)/haproxy-build-starter
COMMON_INCLUDE := $(REPO_ROOT)/common/include
COMMON_SRC := $(REPO_ROOT)/common/src
SPOA_STARTER_BIN := $(HAPROXY_BUILD_DIR)/haproxy-spoa-agent-starter

.PHONY: build-metadata build-starter build-spoa-starter self-test self-test-spoa clean

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

$(HAPROXY_BUILD_DIR)/metadata.o: metadata.c metadata.h $(COMMON_INCLUDE)/msconnector/origin.h
	@mkdir -p "$(HAPROXY_BUILD_DIR)"
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$(COMMON_INCLUDE)" -c metadata.c -o "$@"

$(SPOA_STARTER_BIN): src/haproxy_spoa_main.c src/haproxy_spoa_agent_starter.c src/haproxy_spoa_agent_starter.h $(COMMON_INCLUDE)/msconnector/request.h $(COMMON_INCLUDE)/msconnector/intervention.h $(COMMON_INCLUDE)/msconnector/status.h $(COMMON_SRC)/intervention.c
	@mkdir -p "$(HAPROXY_BUILD_DIR)"
	$(CC) $(CPPFLAGS) $(CFLAGS) -I"$(COMMON_INCLUDE)" -Iconnectors/haproxy/src -Isrc \
		src/haproxy_spoa_main.c src/haproxy_spoa_agent_starter.c "$(COMMON_SRC)/intervention.c" \
		-o "$@"

clean:
	rm -rf "$(HAPROXY_BUILD_DIR)"
