# Envoy Harness

Status: bridge-starter CLI plus blocked runtime-smoke entrypoint
Runtime status: blocked / not-verified

`run_envoy_smoke.sh` exists as the connector-side entrypoint for the framework
runtime-smoke runner. It currently writes BLOCKED evidence and exits 77 because
no real Envoy server/config/runtime harness is implemented.

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

The current `run_envoy_smoke.sh` entrypoint writes BLOCKED evidence under
`/src/ModSecurity-conector-build/results/` and reports runtime not verified. It
does not run the bridge starter self-test as runtime evidence.

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
