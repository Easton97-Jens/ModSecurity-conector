# HAProxy Build

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`

The repository contains HAProxy metadata and a local SPOA agent starter build.
It also contains a minimal diagnostic SPOP handshake subset and a local
libmodsecurity binding used by the `haproxy_phase1_header_block` runtime smoke.
The binding also has a CRS self-test path used by the minimal
`haproxy_crs_sqli_anomaly_block` runtime smoke.
It does not contain a productive HAProxy adapter build for broader scopes.

## Build Targets

Metadata command:

```sh
make -C connectors/haproxy build-metadata
```

SPOA starter command:

```sh
make -C connectors/haproxy build-spoa-starter
```

Combined local starter command:

```sh
make -C connectors/haproxy build-starter
```

Local self-test command:

```sh
make -C connectors/haproxy self-test-spoa
```

Diagnostic SPOP subset commands:

```sh
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-spoa-runtime
```

ModSecurity binding self-test commands:

```sh
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding-crs
```

What these targets build:

- `connectors/haproxy/metadata.c`
- `connectors/haproxy/src/haproxy_spoa_agent_starter.c`
- `connectors/haproxy/src/haproxy_spoa_main.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding_self_test.c`
- shared `common/src/intervention.c`
- outputs under `$(BUILD_ROOT)/haproxy-build-starter/`,
  `$(BUILD_ROOT)/haproxy-spoa-runtime/`, and
  `$(BUILD_ROOT)/haproxy-modsecurity-binding/`

What they do not build:

- HAProxy itself
- a HAProxy native module/filter
- a complete SPOA service
- a full SPOA/SPOP implementation
- broader CRS or RESPONSE_BODY runtime handling
- a productive HAProxy runtime adapter for the full framework matrix

## Productive Adapter Build Status

Productive HAProxy adapter build: BLOCKED.

Missing dependencies/evidence:

- full SPOA/SPOP implementation beyond the diagnostic handshake subset
- broader HAProxy runtime harness support
- Framework cases beyond `haproxy_phase1_header_block` and
  `haproxy_crs_sqli_anomaly_block`
- broader CRS runtime evidence
- RESPONSE_BODY runtime evidence
- productive adapter build command and logs
- productive runtime artifact path

Until those items are recorded from executed HAProxy runtime builds/harnesses,
HAProxy productive build status remains blocked and runtime status remains
partial.
