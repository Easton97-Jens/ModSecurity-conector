# HAProxy Source

**Language:** English | [Deutsch](README.de.md)

Status: live-yaml-spoa-runtime (partial)
Runtime status: live request-side YAML execution through HAProxy, SPOA/SPOP,
and libmodsecurity.

This directory contains local HAProxy starter/runtime sources. The SPOP
runtime and libmodsecurity binding now execute shared framework YAML
request-side cases live through HAProxy, but this is still not a complete
production HAProxy adapter.

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
The SPOP runtime parses live NOTIFY arguments from HAProxy, including `method`,
`uri`, `req.hdrs_bin` with a safe `req.hdrs` fallback, and `req.body`. The
binding loads the materialized rules file, processes URI, headers, optional
request body bytes, and libmodsecurity interventions, then the runtime sends
the verified set-var ACK for 403 disruptive decisions.

Live evidence currently covers request-side variables `REQUEST_URI`,
`REQUEST_HEADERS`, `REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`,
`REQUEST_COOKIES`, `REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES`, and `XML`,
plus CRS SQLi anomaly blocking in the With-CRS variant. Request-body support is
bounded by the current HAProxy request-buffered, single-frame SPOE path
(`tune.bufsize 65536`, `max-frame-size 65532`, one `req.body` argument).

Response phases, audit-log assertions, redirects, non-403 disruptive statuses,
and `RESPONSE_BODY` remain unimplemented for HAProxy runtime promotion.

Productive source may only be added with ORIGIN/license/metadata evidence,
including the future HAProxy source origin, license, imported files, local
changes, and build/runtime evidence.
