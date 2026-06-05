# HAProxy Harness

Status: contract only
Runtime status: not-verified

Harness not implemented. This directory documents the contract only.

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

Until an executable `run_haproxy_smoke.sh` runtime harness exists here, that
target writes BLOCKED evidence under
`/src/ModSecurity-conector-build/results/` and reports runtime not verified.

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
