MODSECURITY_V3_DIR ?= /root/conecter/ModSecurity_V3
BUILD_DIR ?= build/v3-api-smoke
CC ?= cc
CXX ?= c++

ifeq ($(origin CC),default)
CC := cc
endif

ifeq ($(origin CXX),default)
CXX := c++
endif

SRC := v3_api_smoke.c
OBJ := $(BUILD_DIR)/v3_api_smoke.o
BIN := $(BUILD_DIR)/v3_api_smoke
HEADER := $(MODSECURITY_V3_DIR)/headers/modsecurity/modsecurity.h
LIB := $(MODSECURITY_V3_DIR)/src/.libs/libmodsecurity.so

.PHONY: all run check-prereqs clean
.NOTPARALLEL:

all: $(BIN)

check-prereqs:
	@if [ ! -f "$(HEADER)" ]; then \
		echo "v3_api_smoke: blocked missing header: $(HEADER)" >&2; \
		exit 77; \
	fi
	@if [ ! -f "$(LIB)" ]; then \
		echo "v3_api_smoke: blocked missing library: $(LIB)" >&2; \
		echo "v3_api_smoke: not building ModSecurity_V3 from this Makefile" >&2; \
		exit 77; \
	fi

$(BUILD_DIR):
	mkdir -p "$(BUILD_DIR)"

$(OBJ): $(SRC) | $(BUILD_DIR)
	$(CC) -std=c99 -Wall -Wextra -Werror \
		-I"$(MODSECURITY_V3_DIR)/headers" \
		-c "$(SRC)" \
		-o "$(OBJ)"

$(BIN): check-prereqs $(OBJ)
	$(CXX) "$(OBJ)" \
		-L"$(MODSECURITY_V3_DIR)/src/.libs" \
		-Wl,-rpath,"$(MODSECURITY_V3_DIR)/src/.libs" \
		-lmodsecurity \
		-o "$(BIN)"

run: $(BIN)
	"$(BIN)"

clean:
	rm -rf "$(BUILD_DIR)"
