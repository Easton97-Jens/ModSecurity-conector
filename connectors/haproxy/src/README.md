# HAProxy source

**Language:** English | [Deutsch](README.de.md)

`haproxy_spoa_agent_starter.h` / `.c` retain the local starter decision API;
`haproxy_spoa_main.c` provides `--describe`. `haproxy_spop_diagnostic_runtime.c`
implements the SPOP service and its production/legacy serving commands.
`haproxy_modsecurity_binding.h` / `.c` own libmodsecurity transaction, body,
intervention and error handling. `haproxy_modsecurity_mapper.h` / `.c` adapt the
host metadata. Productive legacy evaluation helpers remain in the binding
because the legacy SPOP server calls them.

The product build `make -C connectors/haproxy build-modsecurity-binding` creates
`libhaproxy-modsecurity-binding.a`. It no longer builds a test executable or
links the Common test-result model. SDK compatibility compile/link probes stay
in the product build; an unavailable optional Rule-ID API uses the supported
baseline rather than weakening the required API check.

Embedded starter, binding and SPOP regression definitions now belong to the
pinned Framework under `connector_native_tests/connectors/haproxy/src/`.
The standalone binding driver lives at
`connector_suite/adapters/haproxy/src/haproxy_modsecurity_binding_self_test.c`.
Product binaries no longer provide `--self-test` or `--runtime-self-test`.

From the Connector root run one named specialist target with explicit
`ON_DEMAND_TESTS=1`: `self-test-spoa`, `self-test-spoa-runtime`,
`self-test-modsecurity-binding`, or `self-test-modsecurity-binding-crs` through
`make -C connectors/haproxy`. The CRS target additionally requires
`MODSECURITY_RULE_PREAMBLE_FILE` naming an existing preamble. The Framework
requires the explicit checkout/revision and external outputs, preserves all
assertions, and does not activate these specialist suites by default.

Other harnesses and fixtures belong to Framework
`connector_suite/adapters/haproxy/`. Native HTX and SPOE/SPOP with a response
companion remain distinct runtime profiles. Source, compilation and local
self-tests alone do not establish hosted lifecycle or response-body evidence.
