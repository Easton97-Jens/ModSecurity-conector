# HAProxy Harness

Status: contract plus single-case runtime-smoke entrypoint
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`

`run_haproxy_smoke.sh` exists as the connector-side entrypoint for the framework
runtime-smoke runner. It live-starts local HAProxy, the diagnostic SPOP agent,
and a local backend, then verifies the narrow No-CRS
`haproxy_phase1_header_block` case and the minimal With-CRS
`haproxy_crs_sqli_anomaly_block` case.

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
DISCONNECT handling. CRS behavior is proven only by the separate
`make smoke-haproxy` With-CRS SQLi smoke; RESPONSE_BODY handling and complete
SPOA semantics are not proven.

Framework runtime-smoke entrypoint:

```sh
make smoke-haproxy
```

Framework HAProxy matrix entrypoints:

```sh
make runtime-matrix-haproxy
make test-haproxy-no-crs
make test-haproxy-with-crs
```

`make runtime-matrix-haproxy` preserves the narrow smoke as live evidence and
then writes one HAProxy row per existing framework YAML case. Split targets
write only their split directories and restore any existing combined root
matrix after their own smoke run, so root `haproxy-summary.json` remains the
combined matrix when it was already present.

The current `run_haproxy_smoke.sh` entrypoint writes PASS evidence under
`/src/ModSecurity-conector-build/results/` only when live HAProxy sends NOTIFY
to the diagnostic agent, the agent extracts request arguments, libmodsecurity
produces disruptive 403 decisions for the selected scopes, the agent sends the
locally verified set-var ACK, block probes return 403, and clean probes return
200.

The entrypoint checks HAProxy runtime prerequisites before writing evidence. If
the local HAProxy binary is missing, it attempts the framework prepare helper.
When that helper succeeds, the HAProxy binary/source-acquisition blockers are
removed from `blocked_reasons`. When all live enforcement checks pass:

- `make smoke-haproxy` live-starts HAProxy and the diagnostic SPOP agent, sends
  local HTTP requests through HAProxy, and records fresh agent-log evidence
  after a per-run marker;
- `spoe_runtime_status` is `diagnostic-enforcement-verified`;
- `modsecurity_binding_status` is `live-enforcement-verified`;
- `runtime_verified` is `true` for the recorded `verified_cases` only:
  `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`.
- `crs_verified` is `true` only when the With-CRS evidence is `PASS` with
  CRS loaded.

The ModSecurity binding self-test can be run directly:

```sh
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding-crs
```

That self-test verifies only an in-process phase-1 header block decision with
status 403, or an in-process CRS SQLi decision when the CRS target is used.
Only `make smoke-haproxy` may promote live enforcement status.

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
- NOT_EXECUTABLE reasons for unsupported framework rows
- logs needed for HAProxy, connector, and audit evidence
- broader No-CRS and With-CRS matrix evidence
- RESPONSE_BODY, negative/pass-through, and audit/log evidence

Executable cases and runners are framework-owned, for example:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
