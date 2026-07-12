# Envoy Connector Build

**Language:** English | [Deutsch](build.de.md)

Status: C17 compile/link verified; targeted ext_authz request path is
`minimal_runtime_smoke` / `connector-gap`.

## Connector service

```sh
make -C connectors/envoy build-envoy-connector \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

`MODSECURITY_PREFIX` or `MODSECURITY_LIB_FILE` may be used instead. The build
accepts Framework-resolved values through the same variables. It compiles with
`-std=c17 -Wall -Wextra -Werror`, links Common SDK/runtime, the Envoy profile and
thin mappers, and records a local rpath to the explicitly selected
libmodsecurity directory.

Output:

```text
${BUILD_ROOT}/envoy-connector/msconnector_envoy_ext_authz
```

`BUILD_ROOT` must be absolute and outside the checkout. The build target does
not execute the binary, validate config, start a process, or send a request.

## Separate gates

```sh
make -C connectors/envoy check-envoy-config RULES_FILE=/absolute/rules.conf
make -C connectors/envoy start-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy RULES_FILE=/absolute/rules.conf
make -C connectors/envoy runtime-smoke-envoy \
  ENVOY_BIN=/absolute/path/envoy RULES_FILE=/absolute/rules.conf
```

The older `build-starter` and `self-test` targets remain isolated compatibility
checks for the local bridge CLI and do not build or verify the connector service.

## Separate ext_proc Common/libmodsecurity build target

The non-promoted Go external-processing service is independently pinned. Its
normal executable uses CGo to link the connector-local bridge, Common Runtime,
and libmodsecurity, so explicit libmodsecurity paths are required:

```sh
make -C connectors/envoy build-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy test-envoy-ext-proc \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-runtime-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc \
  ENVOY_BIN=/absolute/path/to/envoy \
  MODSECURITY_INCLUDE_DIR=/absolute/prefix/include \
  MODSECURITY_LIB_DIR=/absolute/prefix/lib
```

`go.mod`/`go.sum` pin Envoy's official generated Go API and gRPC dependencies.
`config/envoy-ext-proc-versions.env` pins the intended Envoy release. The build
uses `go mod verify`, compiles a private Common archive, and builds with
`-tags libmodsecurity`; the config materializers only write outside the
checkout. The test target runs source-only Go tests and, when the paths are
available, tagged CGo lifecycle tests. The runtime smoke validates the
materialized YAML and executes real Envoy-to-ext_proc/Common/libmodsecurity
rule evaluation with raw Common JSONL. It remains non-promoted: it does not by
itself establish canonical collection, timeout/reset semantics, HTTP/2, or
production interoperability.
