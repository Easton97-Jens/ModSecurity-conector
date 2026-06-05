# HAProxy Harness

Status: contract plus blocked runtime-smoke entrypoint
Runtime status: blocked / not-verified

`run_haproxy_smoke.sh` exists as the connector-side entrypoint for the framework
runtime-smoke runner. It writes BLOCKED evidence and exits 77 because no real
HAProxy to SPOA to ModSecurity Framework-case runtime is implemented.

The framework can prepare a local HAProxy binary without global installation
through `modules/ModSecurity-test-Framework/ci/prepare-haproxy-runtime.sh`.
HAProxy `3.2.19` is pinned only in framework `ci/common.sh`; its official
checksum file and source Makefile were verified before adding the pin. The
prepared binary path is:

```text
/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy
```

A local SPOA agent starter exists and can run a local self-test through:

```sh
make -C connectors/haproxy self-test-spoa
```

That self-test does not start HAProxy, does not parse SPOP frames, does not load
libmodsecurity, and must not be reported as a HAProxy runtime smoke.

A separate diagnostic runtime binary can be built through:

```sh
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-spoa-runtime
```

This binary is a minimal diagnostic SPOP handshake subset, not a full SPOA
agent implementation. It verifies only local HELLO/AGENT-HELLO,
NOTIFY-to-empty-ACK, and DISCONNECT handling. It does not prove ModSecurity
processing, CRS behavior, RESPONSE_BODY handling, or complete SPOA semantics.

Framework runtime-smoke entrypoint:

```sh
make smoke-haproxy
```

The current `run_haproxy_smoke.sh` entrypoint writes BLOCKED evidence under
`/src/ModSecurity-conector-build/results/` and reports runtime not verified. It
runs the diagnostic SPOP subset self-test only as protocol diagnostic evidence,
not as full runtime-smoke evidence.

The entrypoint checks HAProxy runtime prerequisites before writing evidence. If
the local HAProxy binary is missing, it attempts the framework prepare helper.
When that helper succeeds, the HAProxy binary/source-acquisition blockers are
removed from `blocked_reasons`. When the diagnostic SPOP subset self-test
passes, the SPOA runtime-missing blocker is removed, but runtime still remains
BLOCKED because:

- the generated SPOE/HAProxy config is syntax-valid only; `spoe_runtime_status`
  remains `not-verified`;
- HAProxy has not been live-started and observed communicating with the
  diagnostic SPOP subset;
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
