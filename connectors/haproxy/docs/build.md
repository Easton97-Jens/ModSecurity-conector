# HAProxy Build

Status: spoa-agent-starter
Runtime status: not-verified

The repository contains HAProxy metadata and a local SPOA agent starter build.
It does not contain a productive HAProxy adapter build.

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

What these targets build:

- `connectors/haproxy/metadata.c`
- `connectors/haproxy/src/haproxy_spoa_agent_starter.c`
- `connectors/haproxy/src/haproxy_spoa_main.c`
- shared `common/src/intervention.c`
- outputs under `$(BUILD_ROOT)/haproxy-build-starter/`

What they do not build:

- HAProxy itself
- a HAProxy native module/filter
- a complete SPOA service
- a SPOP frame parser
- libmodsecurity integration
- a runnable HAProxy runtime adapter

## Productive Adapter Build Status

Productive HAProxy adapter build: BLOCKED.

Missing dependencies/evidence:

- selected SPOP frame parser or SPOE/SPOA protocol library
- HAProxy runtime harness support
- HAProxy binary/container/source-build evidence
- verified HAProxy SPOE/SPOA config
- selected libmodsecurity binding strategy for HAProxy
- productive adapter build command and logs
- productive runtime artifact path

Until those items are recorded from an executed HAProxy runtime build/harness,
HAProxy productive build status remains blocked and runtime status remains
`not-verified`.
