# HAProxy Build

Status: spoa-agent-starter
Runtime status: not-verified

The repository contains HAProxy metadata and a local SPOA agent starter build.
It also contains a minimal diagnostic SPOP handshake subset. It does not contain
a productive HAProxy adapter build.

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

What these targets build:

- `connectors/haproxy/metadata.c`
- `connectors/haproxy/src/haproxy_spoa_agent_starter.c`
- `connectors/haproxy/src/haproxy_spoa_main.c`
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- shared `common/src/intervention.c`
- outputs under `$(BUILD_ROOT)/haproxy-build-starter/`
  and `$(BUILD_ROOT)/haproxy-spoa-runtime/`

What they do not build:

- HAProxy itself
- a HAProxy native module/filter
- a complete SPOA service
- a full SPOA/SPOP implementation
- libmodsecurity integration
- a runnable HAProxy runtime adapter

## Productive Adapter Build Status

Productive HAProxy adapter build: BLOCKED.

Missing dependencies/evidence:

- full SPOA/SPOP implementation beyond the diagnostic handshake subset
- HAProxy runtime harness support
- HAProxy binary/container/source-build evidence
- verified HAProxy SPOE/SPOA config
- selected libmodsecurity binding strategy for HAProxy
- productive adapter build command and logs
- productive runtime artifact path

Until those items are recorded from an executed HAProxy runtime build/harness,
HAProxy productive build status remains blocked and runtime status remains
`not-verified`.
