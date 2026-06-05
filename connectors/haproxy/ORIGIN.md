# HAProxy Connector Origin

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`

No upstream HAProxy connector source has been imported into this repository.
No HAProxy source tree, HAProxy headers, or SPOE/SPOA protocol library is
vendored under `connectors/haproxy`. The repo-authored libmodsecurity binding
source is used by the local diagnostic SPOP runtime for the scoped
`haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block` smokes; it
is not a productive HAProxy runtime adapter.

## Current Source Provenance

| Path | Origin | License status | Notes |
| --- | --- | --- | --- |
| `connectors/haproxy/metadata.c` | repo-authored starter metadata | not selected | Does not implement HAProxy API, SPOE/SPOA protocol, or libmodsecurity calls. |
| `connectors/haproxy/metadata.h` | repo-authored starter metadata | not selected | Declares metadata accessors only. |
| `connectors/haproxy/Makefile` | repo-authored starter build file | not selected | Compiles metadata and local starter binaries only. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.c` | repo-authored SPOA agent starter | not selected | Local synthetic request-decision logic only; no SPOP parser or HAProxy runtime. |
| `connectors/haproxy/src/haproxy_spoa_agent_starter.h` | repo-authored SPOA agent starter | not selected | Local starter declarations only. |
| `connectors/haproxy/src/haproxy_spoa_main.c` | repo-authored SPOA agent starter CLI | not selected | Supports `--describe` and `--self-test` only. |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | repo-authored diagnostic SPOP runtime | not selected | Minimal diagnostic SPOP handshake subset with live set-var ACK enforcement for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`; not a full SPOA agent implementation. |
| `connectors/haproxy/src/haproxy_modsecurity_binding.c` | repo-authored ModSecurity binding | not selected | Uses locally verified libmodsecurity C API signatures for phase-1 header block and minimal CRS SQLi decisions. |
| `connectors/haproxy/src/haproxy_modsecurity_binding.h` | repo-authored ModSecurity binding | not selected | Declares the decision shape used by the binding self-test and diagnostic runtime. |
| `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c` | repo-authored ModSecurity binding self-test CLI | not selected | Supports `--describe` and `--self-test`; no HAProxy runtime enforcement. |
| `connectors/haproxy/docs/` | repo-authored documentation | not selected | Documents open HAProxy integration options and blockers. |
| `connectors/haproxy/harness/README.md` | repo-authored documentation | not selected | Harness contract only. |

## Upstream Selection

- HAProxy upstream source: not selected.
- HAProxy integration API/header set: not selected.
- SPOE/SPOA protocol dependency: not selected.
- SPOP frame implementation: minimal diagnostic handshake subset only.
- ModSecurity/libmodsecurity binding for HAProxy: live enforcement verified
  only for `haproxy_phase1_header_block` and
  `haproxy_crs_sqli_anomaly_block`.
- Imported productive source files: none.

## Evidence Boundary

The current starter proves only that metadata and local diagnostic binaries can
be compiled, that the SPOA starter can run a local synthetic request-decision
self-test, and that `make smoke-haproxy` can enforce
`haproxy_phase1_header_block` plus the CRS-backed
`haproxy_crs_sqli_anomaly_block` through live HAProxy, the diagnostic SPOP
agent, and libmodsecurity. It does not prove a productive HAProxy adapter
build, SPOE/SPOA protocol completeness, broader CRS behavior, RESPONSE_BODY
blocking, or the full runtime matrix.
