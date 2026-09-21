# Getting started

**Language:** English | [Deutsch](getting-started.de.md)

This guide is the shortest path from a fresh clone to a correctly oriented
development checkout. It deliberately stops before making any production or
runtime-quality claim.

## 1. Clone and initialize

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
```

If you cloned without submodules, run `git submodule update --init --recursive`
before `make check-framework`.

## 2. Validate the checkout

```sh
make quick-check
```

This checks repository contracts, documentation, and selected structural
requirements. It does **not** build every host, send traffic through every
connector, or create canonical lifecycle evidence.

## 3. Choose a host and logical profile

| Host family | Start with | Additional logical profile |
| --- | --- | --- |
| Apache | `apache` | — |
| NGINX | `nginx` | — |
| HAProxy | `haproxy-htx` | `haproxy-spoe-spop` |
| Envoy | `envoy-ext-proc` | `envoy-ext-authz` |
| Traefik | `traefik-native-uds` | `traefik-forwardauth` |
| lighttpd | `lighttpd-patched` | `lighttpd-stock` |

Read the [connector index](connectors/README.md) before choosing an alternate
logical profile. Alternate profiles can have different request/response
visibility and different runtime limitations.

## 4. Choose an example profile

Open the [examples index](../examples/README.md) and choose the matching logical
solution. As a practical rule:

- `safe` is the best starting point for understanding the complete checked-in
  P1–P4 configuration shape without assuming a late client-visible abort.
- `off` disables the extra connector-owned cumulative Phase-4 budget; it does
  not disable configured libmodsecurity response-body inspection.
- `strict` expresses the strict late-action policy but is only runnable where
  the selected host/profile supports the required action.
- `all` is the comprehensive source-backed configuration layout. It selects
  valid settings (typically including `strict`); `all` is not a fourth
  Phase-4 mode.

Also keep `DetectionOnly`, engine `Off`, and a disabled connector distinct:
they change different layers.

## 5. Build or check one selected host

Use the root Makefile rather than invoking a connector harness directly. For
example:

```sh
make build-nginx
make check-config-nginx
```

Replace `nginx` with one of the six host-family names documented by the root
Makefile where the target exists. Build success proves only the build stage;
configuration success proves only that the selected host accepted its
configuration.

## 6. Run lifecycle evidence only when you need a runtime claim

For an aggregate selected-core run, use a filesystem-safe, non-secret run ID:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

The validation result applies only to that run, its selected profiles, rules,
protocol scope, and artifacts.

## What success means

A zero exit status means the command you ran satisfied **that command's
contract**. It does not automatically mean:

- production readiness or production hardening;
- CRS verification;
- complete HTTP/2 or HTTP/3 coverage;
- complete protocol/profile matrix coverage; or
- strict post-commit behavior for every connector.

## Where to go next

| Need | Document |
| --- | --- |
| pick a concrete configuration | [Examples](../examples/README.md) |
| understand a host/profile | [Connector index](connectors/README.md) |
| understand settings | [Configuration](configuration.md) |
| build details | [Build](build/README.md) |
| test/result semantics | [Testing and evidence](testing-and-evidence.md) |
| safe operation | [Operations and security](operations-and-security.md) |
