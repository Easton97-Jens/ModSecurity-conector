# HAProxy Harness

Status: contract plus blocked runtime-smoke entrypoint
Runtime status: blocked / not-verified

`run_haproxy_smoke.sh` exists as the connector-side entrypoint for the framework
runtime-smoke runner. It currently writes BLOCKED evidence and exits 77 because
no real HAProxy server/config/SPOE runtime harness is implemented.

A local SPOA agent starter exists and can run a local self-test through:

```sh
make -C connectors/haproxy self-test-spoa
```

That self-test does not start HAProxy, does not parse SPOP frames, does not load
libmodsecurity, and must not be reported as a HAProxy runtime smoke.

Framework runtime-smoke entrypoint:

```sh
make smoke-haproxy
```

The current `run_haproxy_smoke.sh` entrypoint writes BLOCKED evidence under
`/src/ModSecurity-conector-build/results/` and reports runtime not verified. It
does not run the SPOA starter self-test as runtime evidence.

The entrypoint checks HAProxy runtime prerequisites before writing evidence. In
the current repository/environment it remains BLOCKED because:

- no `haproxy` binary is available to the harness;
- HAProxy source/binary acquisition is not defined in the framework `common.sh`;
- the SPOA starter binary is self-test-only and is not a runnable SPOA server;
- the HAProxy/SPOE config files are example-only, not runtime-verified config;
- no HAProxy/libmodsecurity transaction binding exists.

A future HAProxy harness must not claim runtime verification until it records:

- HAProxy binary, container, or source-build evidence
- HAProxy config file
- SPOE/SPOA config file
- starter/agent endpoint
- ModSecurity integration point
- the harness command
- result JSON path
- evidence paths
- PASS/FAIL/BLOCKED counts
- logs needed for HAProxy, connector, and audit evidence
- No-CRS and With-CRS scope separation

Executable cases and runners are framework-owned, for example:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
