# lighttpd Connector Origin

Status: bridge-starter plus sidecar_proxy runtime-smoke path
Runtime status: locally verifiable with a staged lighttpd binary

No upstream lighttpd connector source is imported in this repository. The
upstream lighttpd runtime component is pinned for opt-in local download/build by
`modules/ModSecurity-test-Framework/ci/common.sh`; that source tarball is staged
under the local component cache and is not committed into this connector tree.

## Current Source State

| Item | Value |
| --- | --- |
| Upstream lighttpd version | `1.4.84` |
| Upstream lighttpd commit | release tarball, no repository commit selected |
| Upstream connector repository | not selected |
| Upstream runtime source URL | `https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.84.tar.xz` |
| Imported upstream source files | none |
| Local implementation source | `connectors/lighttpd/metadata.c`, `connectors/lighttpd/metadata.h`, `connectors/lighttpd/src/lighttpd_build_starter.c`, `connectors/lighttpd/src/lighttpd_bridge.h`, `connectors/lighttpd/src/lighttpd_bridge.c`, `connectors/lighttpd/src/lighttpd_bridge_main.c` |
| Source kind | repo-owned bridge-starter plus external pinned runtime component |
| Runtime status | sidecar_proxy local smoke path |

The current C files are repository-owned metadata/probe and bridge-starter code
only. They compile against connector-neutral `common/` headers and do not include
lighttpd headers, call lighttpd APIs, call ModSecurity APIs, or implement
FastCGI/SCGI. Runtime traffic for Phase 1 is handled by the framework-owned
sidecar_proxy smoke, not by these starter sources.

## Public References For Future Selection

Public lighttpd references are listed in `connectors/lighttpd/docs/public-sources.md`
and in `modules/ModSecurity-test-Framework/docs/imports/sources.md`. Those
references are not imported source and do not prove a connector implementation.

## License / Attribution Status

No upstream lighttpd source has been imported into this connector tree, so no
upstream lighttpd license claim is made for committed connector source. If future
work imports lighttpd source or headers, this file,
`connectors/lighttpd/SOURCE_MAP.json`, and repository-level license attribution
must be updated before promotion.
