# Envoy Harness

Status: bridge-starter CLI only
Runtime status: not-verified

No Envoy runtime harness is implemented.

The current local CLI self-test is:

```sh
make -C connectors/envoy self-test
```

That command builds and runs the local sidecar/HTTP bridge decision model. It
is not an Envoy runtime harness and does not execute framework YAML cases,
No-CRS, With-CRS, CRS, or RESPONSE_BODY checks.

Framework runtime-smoke entrypoint:

```sh
make smoke-envoy
```

Until an executable `run_envoy_smoke.sh` runtime harness exists here, that target
writes BLOCKED evidence under `/src/ModSecurity-conector-build/results/` and
reports runtime not verified.

A future Envoy harness must document:

- Envoy binary, container, or source-build input;
- Envoy configuration file;
- bridge, ext_proc, or native filter integration point;
- the harness command;
- result JSON paths;
- PASS/FAIL/BLOCKED counts;
- No-CRS and With-CRS results as separate evidence;
- CRS loaded/effective evidence for With-CRS;
- RESPONSE_BODY evidence as a separate gate.

The global harness and runtime gates are documented in
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md`.
