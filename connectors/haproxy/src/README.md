# HAProxy Source

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block`

This directory contains local HAProxy diagnostic sources, not a productive
runtime adapter.

Current starter files:

- `haproxy_spoa_agent_starter.c`
- `haproxy_spoa_agent_starter.h`
- `haproxy_spoa_main.c`
- `haproxy_spop_diagnostic_runtime.c`
- `haproxy_modsecurity_binding.c`
- `haproxy_modsecurity_binding.h`
- `haproxy_modsecurity_binding_self_test.c`

The starter can be compiled and self-tested locally. It evaluates synthetic
in-process requests with repository-owned request/intervention/status shapes.
The diagnostic SPOP runtime handles only a minimal diagnostic SPOP handshake
subset, but it now parses live NOTIFY arguments, calls the local ModSecurity
binding, and sends the verified set-var ACK for the single
`haproxy_phase1_header_block` smoke path. CRS loading, RESPONSE_BODY handling,
and broader request/response inspection remain unimplemented.

Productive source may only be added with ORIGIN/license/metadata evidence,
including the future HAProxy source origin, license, imported files, local
changes, and build/runtime evidence.
