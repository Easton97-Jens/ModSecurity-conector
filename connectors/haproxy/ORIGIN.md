# HAProxy Connector Origin

Status: spoa-agent-starter
Runtime status: not-verified

No upstream HAProxy connector source has been imported into this repository.
No HAProxy source tree, HAProxy headers, SPOE/SPOA protocol library, or
libmodsecurity adapter implementation is vendored under `connectors/haproxy`.

## Current Source Provenance

| Path | Origin | License status | Notes |
| --- | --- | --- | --- |
| `connectors/haproxy/metadata.c` | repo-authored starter metadata | not selected | Does not implement HAProxy API, SPOE/SPOA protocol, or libmodsecurity calls. |
| `connectors/haproxy/metadata.h` | repo-authored starter metadata | not selected | Declares metadata accessors only. |
| `connectors/haproxy/Makefile` | repo-authored starter build file | not selected | Compiles metadata and local starter binaries only. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | repo-authored SPOA agent starter | not selected | Local synthetic request-decision logic only; no SPOP parser or HAProxy runtime. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | repo-authored SPOA agent starter | not selected | Local starter declarations only. |
| `connectors/haproxy/src/haproxy_spoa_main.c` | repo-authored SPOA agent starter CLI | not selected | Supports `--describe` and `--self-test` only. |
| `connectors/haproxy/docs/` | repo-authored documentation | not selected | Documents open HAProxy integration options and blockers. |
| `connectors/haproxy/harness/README.md` | repo-authored documentation | not selected | Harness contract only. |

## Upstream Selection

- HAProxy upstream source: not selected.
- HAProxy integration API/header set: not selected.
- SPOE/SPOA protocol dependency: not selected.
- SPOP frame implementation: not implemented.
- ModSecurity/libmodsecurity binding for HAProxy: not implemented.
- Imported productive source files: none.

## Evidence Boundary

The current starter proves only that metadata and a local SPOA agent starter can
be compiled, and that the starter can run a local synthetic request-decision
self-test. It does not prove a HAProxy adapter build, SPOE/SPOA protocol
compatibility, runtime integration, request inspection through HAProxy, response
inspection, intervention mapping in HAProxy, logging, CRS behavior, or
RESPONSE_BODY blocking.
