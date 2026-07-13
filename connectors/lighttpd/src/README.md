# lighttpd Source

**Language:** English | [Deutsch](README.de.md)

Status: native Phase-1 mapper plus retained legacy starters

Primary native source:

- `../module/mod_msconnector.c`: lighttpd plugin lifecycle and Common runtime
  callsites;
- `lighttpd_modsecurity_mapper.h/.c`: real request/response metadata and header
  mapping from pinned lighttpd types to Common SDK types.

The mapper has a non-host stub so repository-wide Common C-standard checks can
compile without provisioning lighttpd headers. `build/build_module.sh` defines
`MSCONNECTOR_LIGHTTPD_HOST_API` and compiles the real implementation against the
pinned host source and generated `config.h`.

`lighttpd_build_starter.c` remains a metadata probe.
`lighttpd_bridge.h/.c` and `lighttpd_bridge_main.c` remain a separate historical
decision-service bridge starter. Its self-test is not native-host evidence.

The native source currently maps headers only. It intentionally maps no request
or response body and makes no body, CRS, production, security, or full-matrix
claim.
