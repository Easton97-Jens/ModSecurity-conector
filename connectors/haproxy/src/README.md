# HAProxy Source

Status: spoa-agent-starter
Runtime status: not-verified

This directory contains a local HAProxy SPOA agent starter, not a productive
runtime adapter.

Current starter files:

- `haproxy_spoa_agent_starter.c`
- `haproxy_spoa_agent_starter.h`
- `haproxy_spoa_main.c`

The starter can be compiled and self-tested locally. It evaluates synthetic
in-process requests with repository-owned request/intervention/status shapes.
It does not implement SPOP frame parsing, HAProxy network handling,
libmodsecurity transaction handling, CRS loading, request or response inspection
through HAProxy, HAProxy intervention mapping, logging, or runtime behavior.

Productive source may only be added with ORIGIN/license/metadata evidence,
including the future HAProxy source origin, license, imported files, local
changes, and build/runtime evidence.
