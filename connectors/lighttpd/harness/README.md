# lighttpd Harness

Status: contract only
Runtime status: not-verified

No lighttpd runtime harness is implemented. This directory documents the
contract only.

The local starters are not a runtime harness:

- `connectors/lighttpd/build/build_starter.sh` compiles metadata/probe code.
- `connectors/lighttpd/build/bridge_starter.sh` compiles and self-tests a local
  decision-service bridge starter.

The bridge starter does not start lighttpd, load a module, implement
FastCGI/SCGI, send real HTTP traffic through lighttpd, collect logs, or write
framework summary JSON.

A future harness must provide and document:

- lighttpd binary, container, or source-build path;
- lighttpd config file;
- selected module/FastCGI/SCGI/bridge config;
- bridge endpoint if a service/sidecar path is selected;
- selected ModSecurity integration point;
- No-CRS and With-CRS split;
- generated runtime state under `$BUILD_ROOT`;
- result JSON path;
- PASS/FAIL/BLOCKED counts;
- server, connector, audit, and access log evidence.

Executable tests must remain framework-owned and use shared framework paths such
as `modules/ModSecurity-test-Framework/tests/cases/` and
`modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
