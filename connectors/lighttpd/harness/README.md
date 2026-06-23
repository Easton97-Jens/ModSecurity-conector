# lighttpd Harness

Status: sidecar_proxy runtime-smoke entrypoint
Runtime status: locally verifiable with a staged lighttpd binary

`run_lighttpd_smoke.sh` exists as the connector-side entrypoint for the
framework runtime-smoke runner. It resolves only local/common.sh-managed
`lighttpd` binaries, then delegates to the shared local runtime runner.

The local starters are not a runtime harness:

- `connectors/lighttpd/build/build_starter.sh` compiles metadata/probe code.
- `connectors/lighttpd/build/bridge_starter.sh` compiles and self-tests a local
  decision-service bridge starter.

The bridge starter does not start lighttpd, load a module, implement
FastCGI/SCGI, send real HTTP traffic through lighttpd, collect logs, or write
framework summary JSON. The runtime smoke is separate from the bridge starter.

Framework runtime-smoke entrypoint:

```sh
make smoke-lighttpd
```

With no local binary, the entrypoint writes BLOCKED evidence and reports runtime
not verified. With a staged binary, it starts local lighttpd as the upstream and
a local sidecar decision proxy. The expected runtime statuses are 200 for an
allowed request and 403 for `X-Modsec-Smoke: block`.

The harness provides:

- lighttpd binary, container, or source-build path;
- lighttpd config file;
- selected sidecar_proxy decision boundary;
- optional targeted libmodsecurity decision backend;
- generated runtime state under `$BUILD_ROOT` / `$VERIFIED_RUN_ROOT`;
- result JSON path;
- server, connector, decision, and transcript log evidence.

Still required before production-style claims:

- No-CRS and With-CRS split;
- PASS/FAIL/BLOCKED counts;
- audit log evidence;
- response-body evidence;
- sidecar hardening and lifecycle documentation.

Executable tests must remain framework-owned and use shared framework paths such
as `modules/ModSecurity-test-Framework/tests/cases/` and
`modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
