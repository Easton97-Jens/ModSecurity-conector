<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build and lifecycle: Apache HTTP Server

**Language:** English | [Deutsch](apache.de.md)

## Purpose and selected host route

This guide documents the current root Make targets for Apache HTTP Server. The
selected full-lifecycle route is `full-lifecycle-apache` with profile
`native-httpd-module`: native httpd module built through APXS. It is deliberately separate from build,
configuration, and compatibility smokes.

| Stage | current target | what it does | does not establish |
| --- | --- | --- | --- |
| Build | `make build-apache` | builds the connector's selected stage | config load or traffic |
| Configuration | `make check-config-apache` | loads/checks the selected configuration | a sent request |
| Start | `make start-smoke-apache` | starts and stops the host route without full traffic | lifecycle coverage |
| Minimal runtime smoke | `make runtime-smoke-apache` | sends bounded runtime traffic | canonical full lifecycle |
| Full lifecycle | `make full-lifecycle-apache` | collects selected No-CRS host evidence | production, CRS, or full matrix |

## Host version and source provenance

The Framework-owned Apache, APR, PCRE2 and libmodsecurity provenance is selected at preparation time. Its effective version, URL and checksum are recorded by the Cache-v2 inventory; do not copy a version from an old guide.

Show the prepared values before building:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevant variables: `BUILD_HTTPD_FROM_SOURCE`, `APACHE_BIN`, `APACHECTL_BIN`, `APXS_BIN`, and the Framework-forwarded Apache source/checksum variables.
Their format, defaults, scope, effect, and security boundary are defined in the
[central variable reference](../../configuration/variables.md). An override is
an explicit input change, not a capability upgrade.

## Toolchain and Cache-v2

A trusted C compiler, Autotools/APXS and matching Apache development headers are required when the host is built or checked locally. The repository's C17 adoption check may report `77` when headers are unavailable.

For a clean local invocation, choose a writable parent outside the checkout.
`VERIFIED_RUN_PARENT` derives `BUILD_ROOT` and `CACHE_ROOT=.../cache-v2`. The
shared cache holds reusable inputs, not canonical evidence; do not manually
rearrange it or mix incompatible provenance.

```sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-apache VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` is an example absolute runtime path, not a repository
default. A target can end with `BLOCKED`/exit code `77` when a prerequisite is
absent.

## Build, configuration, and smoke

Run stages independently so that a failure is not mistaken for a stronger
claim:

```sh
make build-apache
make check-config-apache
make start-smoke-apache
make runtime-smoke-apache
```

For one selected canonical evidence run, use the same safe run identifier. The
`evidence-check` command validates already-produced artifacts only.

```sh
run_id="apache-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-apache
NO_CRS_RUN_ID="$run_id" make evidence-check-apache
```

`NO_CRS_RUN_ID` must be a filesystem-safe token. Do not set internal
full-lifecycle profile variables to relabel a direct or compatibility run.

## Optional and historical integration notes

For a diagnostic source-host smoke, use `BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache`. `make check-apache-c17` checks the adoption boundary; optional newer C profiles remain toolchain-dependent.

> Historical note: Older package-install examples and generic smoke descriptions are compatibility notes only. They neither select nor replace the `native-httpd-module` full-lifecycle profile.

A narrowed case, `FORCE_ALL_CASES=1`, or a direct connector-subdirectory
command is diagnostic input. Only the documented target with its artifact
profile can produce canonical evidence.

## Configuration, examples, and troubleshooting

- Current connector guide: [Apache HTTP Server](../../connectors/apache/README.md)
- Configuration details:
  [connector configuration](../../connectors/apache/configuration.md)
- Repository examples: [examples/apache](../../../examples/apache/README.md)
- Test and evidence boundaries: [test levels](../../testing/README.md) ·
  [evidence rules](../../evidence/README.md)

If APXS and httpd do not match, rebuild against the selected host. If the config stage fails, inspect the generated config and the sanitized host log before changing rules or module paths.

Do not put unsanitized cookies, authorization values, tokens, private keys, or
raw logs into configuration, issues, or evidence.

## Evidence boundary

This text does not claim production readiness, complete CRS coverage, HTTP/2
or HTTP/3 support, a full matrix, or strict post-commit intervention. A PASS
applies only to the target actually executed, its documented host profile, and
its sanitized run-specific evidence set.
