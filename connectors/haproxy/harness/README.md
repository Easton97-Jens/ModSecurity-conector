# HAProxy Harness

Status: contract plus single-case runtime-smoke entrypoint
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block`

`run_haproxy_smoke.sh` exists as the connector-side entrypoint for the framework
runtime-smoke runner. It live-starts local HAProxy, the diagnostic SPOP agent,
and a local backend, then verifies the narrow
`haproxy_phase1_header_block` case.

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
agent implementation. It verifies local HELLO/AGENT-HELLO, NOTIFY request
argument parsing, verified `set-var txn.blocked true` ACK encoding, and
DISCONNECT handling. It does not prove CRS behavior, RESPONSE_BODY handling, or
complete SPOA semantics.

Framework runtime-smoke entrypoint:

```sh
make smoke-haproxy
```

The current `run_haproxy_smoke.sh` entrypoint writes PASS evidence under
`/src/ModSecurity-conector-build/results/` only when live HAProxy sends NOTIFY
to the diagnostic agent, the agent extracts `method`, `path`, and
`test_header`, libmodsecurity produces a disruptive 403 decision, the agent
sends the locally verified set-var ACK, the block probe returns 403, and the
clean probe returns 200.

The entrypoint checks HAProxy runtime prerequisites before writing evidence. If
the local HAProxy binary is missing, it attempts the framework prepare helper.
When that helper succeeds, the HAProxy binary/source-acquisition blockers are
removed from `blocked_reasons`. When all live enforcement checks pass:

- `make smoke-haproxy` live-starts HAProxy and the diagnostic SPOP agent, sends
  local HTTP requests through HAProxy, and records fresh agent-log evidence
  after a per-run marker;
- `spoe_runtime_status` is `diagnostic-enforcement-verified`;
- `modsecurity_binding_status` is `live-enforcement-verified`;
- `runtime_verified` is `true` for `haproxy_phase1_header_block` only.

The ModSecurity binding self-test can be run directly:

```sh
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding
```

That self-test verifies only an in-process phase-1 header block decision with
status 403. It may set `modsecurity_binding_status: self-test-verified`, but
only `make smoke-haproxy` may promote the live enforcement status.

Future HAProxy promotion beyond the current single-case runtime smoke still
requires:

- HAProxy binary, container, or source-build evidence
- HAProxy config file
- SPOE/SPOA config file
- starter/agent endpoint
- ModSecurity integration point
- the harness command
- result JSON path
- evidence paths
- PASS/FAIL/BLOCKED counts for broader scopes
- logs needed for HAProxy, connector, and audit evidence
- No-CRS and With-CRS scope separation
- CRS, RESPONSE_BODY, negative/pass-through, and audit/log evidence

Executable cases and runners are framework-owned, for example:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
