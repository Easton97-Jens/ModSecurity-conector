# lighttpd source

**Language:** English | [Deutsch](README.de.md)

The native plugin lifecycle and Common runtime callsites live in
`../module/mod_msconnector.c`. `lighttpd_modsecurity_mapper.h` / `.c` translate
host request/response metadata to Common SDK types. The non-host mapper stub
allows compile checks without provisioning lighttpd headers;
`../build/build_module.sh` selects the real host implementation with
`MSCONNECTOR_LIGHTTPD_HOST_API`, pinned host headers and generated `config.h`.

`lighttpd_build_starter.c` remains a metadata probe. `lighttpd_bridge.h` / `.c`
and `lighttpd_bridge_main.c` retain the historical decision-service starter.
The bridge binary provides `--status`; its `--self-test` command and embedded
assertions were removed from the product.

The same assertions now live in the pinned Framework under
`connector_native_tests/connectors/lighttpd/src/lighttpd_bridge.inc`.
From the Connector root run
`make -C connectors/lighttpd self-test-lighttpd-bridge ON_DEMAND_TESTS=1`.
Connector-specific fixtures, native smoke harnesses and Python tests belong to
Framework `connector_suite/adapters/lighttpd/`.

The Framework runner requires an explicit Connector checkout/revision and
external output directory. These specialist tests do not enlarge default
selection. Compilation and local starter checks do not prove hosted behavior;
stock sidecar and patched native plugin remain separate runtime profiles.
