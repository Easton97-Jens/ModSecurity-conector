# lighttpd Harness

Status: contract plus blocked runtime-smoke entrypoint
Runtime status: blocked / not-verified

`run_lighttpd_smoke.sh` exists as the connector-side entrypoint for the
framework runtime-smoke runner. It currently writes BLOCKED evidence and exits
77 because no real lighttpd server/config/runtime harness is implemented.

The local starters are not a runtime harness:

- `connectors/lighttpd/build/build_starter.sh` compiles metadata/probe code.
- `connectors/lighttpd/build/bridge_starter.sh` compiles and self-tests a local
  decision-service bridge starter.

The bridge starter does not start lighttpd, load a module, implement
FastCGI/SCGI, send real HTTP traffic through lighttpd, collect logs, or write
framework summary JSON.

Framework runtime-smoke entrypoint:

```sh
make smoke-lighttpd
```

The current `run_lighttpd_smoke.sh` entrypoint writes BLOCKED evidence under
`/src/ModSecurity-conector-build/results/` and reports runtime not verified. It
does not run bridge-starter scripts as runtime evidence.

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
