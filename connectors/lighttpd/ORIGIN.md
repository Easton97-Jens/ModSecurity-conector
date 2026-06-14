# lighttpd Connector Origin

Status: bridge-starter
Runtime status: not-verified

No upstream lighttpd connector source is imported in this repository.

## Current Source State

| Item | Value |
| --- | --- |
| Upstream lighttpd version | not selected |
| Upstream lighttpd commit | not selected |
| Upstream connector repository | not selected |
| Imported upstream source files | none |
| Local implementation source | `connectors/lighttpd/metadata.c`, `connectors/lighttpd/metadata.h`, `connectors/lighttpd/src/lighttpd_build_starter.c`, `connectors/lighttpd/src/lighttpd_bridge.h`, `connectors/lighttpd/src/lighttpd_bridge.c`, `connectors/lighttpd/src/lighttpd_bridge_main.c` |
| Source kind | repo-owned bridge-starter |
| Runtime status | not-verified |

The current C files are repository-owned metadata/probe and bridge-starter code
only. They compile against connector-neutral `common/` headers and do not include
lighttpd headers, call lighttpd APIs, call ModSecurity APIs, implement
FastCGI/SCGI, or process real lighttpd request/runtime integration.

## Public References For Future Selection

Public lighttpd references are listed in `connectors/lighttpd/docs/public-sources.md`
and in `modules/ModSecurity-test-Framework/docs/imports/sources.md`. Those
references are not imported source and do not prove a connector implementation.

## License / Attribution Status

No upstream lighttpd source has been imported, so no upstream lighttpd license
claim is made for this connector tree. If future work imports lighttpd source or
headers, this file, `connectors/lighttpd/SOURCE_MAP.json`, and repository-level
license attribution must be updated before promotion.
