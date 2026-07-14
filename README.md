# ModSecurity Connector

**Language:** English | [Deutsch](README.de.md)

This repository contains the connector-owned source, selected host integration
routes, lifecycle wrappers, configuration, and evidence consumers for
libmodsecurity-based server connectors. Reusable case catalogs, schemas, and
framework runners live in the
<code>modules/ModSecurity-test-Framework</code> submodule.

The repository documents six selected HTTP/1.1 core routes. Their outcome is
run-specific: source wiring, builds, capability declarations, and configuration
checks are not evidence results on their own.

## Selected connector routes

| Connector | Selected full-lifecycle profile | Recorded integration mode | Entry point |
|---|---|---|---|
| Apache | <code>native-httpd-module</code> | <code>native-httpd-module</code> | [Connector guide](docs/connectors/README.md) / [source](connectors/apache/README.md) |
| NGINX | <code>native-nginx-http-module</code> | <code>native-nginx-http-module</code> | [Connector guide](docs/connectors/README.md) / [source](connectors/nginx/README.md) |
| HAProxy | <code>native-htx-filter</code> | <code>native-htx-filter</code> | [Connector guide](docs/connectors/README.md) / [source](connectors/haproxy/README.md) |
| Envoy | <code>ext_proc</code> | <code>ext_proc</code> | [Connector guide](docs/connectors/README.md) / [source](connectors/envoy/README.md) |
| Traefik | <code>native-middleware</code> | <code>native-traefik-middleware</code> | [Connector guide](docs/connectors/README.md) / [source](connectors/traefik/README.md) |
| lighttpd | <code>patched-native</code> | <code>patched-native-lighttpd</code> | [Connector guide](docs/connectors/README.md) / [source](connectors/lighttpd/README.md) |

The profile value is the root lifecycle target’s identity. The recorded
integration mode is the descriptive value written with the effective run
profile. Details, alternate compatibility terms, and limits are in
[connector documentation](docs/connectors/README.md).

## Architecture

~~~mermaid
flowchart LR
    Client[HTTP client] --> Host[Selected connector host]
    Host --> Adapter[Connector adapter or bridge]
    Adapter --> Common[Common runtime / libmodsecurity]
    Common --> Host
    Host --> Raw[Invocation-local raw artifacts]
    Raw --> Finalize[Normalize and finalize]
    Finalize --> Evidence[Run-scoped canonical evidence]
    Evidence --> Validate[Evidence validators and reports]
~~~

The host is Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd. The selected
route determines its request/response visibility and phase boundary. Raw
runtime output is not automatically canonical evidence; finalization and
validation bind artifacts to the connector, profile, rules, and run ID.

## Quick start

Initialize the Framework submodule, then check its location:

~~~sh
git submodule update --init --recursive
make check-framework
~~~

<code>FRAMEWORK_ROOT</code> defaults to
<code>modules/ModSecurity-test-Framework</code>. Set it only when using a
trusted existing Framework checkout, for example:

~~~sh
make check-framework FRAMEWORK_ROOT="/srv/src/ModSecurity-test-Framework"
~~~

<code>/srv/src/ModSecurity-test-Framework</code> is an example
<em>external source root</em>: a user-selected absolute checkout outside this
repository. It is not a literal or developer-specific path. A missing
Framework prerequisite results in exit code <code>77</code>.

Run the local structural/documentation check:

~~~sh
make quick-check
~~~

This validates repository-oriented checks; it does not run every connector
host or create full-lifecycle evidence.

## Build and test overview

| Goal | Start with | Important boundary |
|---|---|---|
| Build one selected route | <code>make build-nginx</code> | Build success is not runtime evidence |
| Check selected configuration | <code>make check-config-nginx</code> | Config loading is not traffic execution |
| Run a focused smoke | <code>make runtime-smoke-nginx</code> where provided | A smoke is not full-lifecycle promotion |
| Create a selected aggregate candidate run | <code>NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-all-connectors</code> | The run ID is an example safe token, not an outcome claim |
| Validate finalized evidence | <code>NO_CRS_RUN_ID="six-core-20260712T120000Z" make check-six-connector-core-completion</code> | Read-only gate; exit <code>0</code> is limited to that gate |

The exact inputs, outputs, target meanings, status values, exit codes, and
placeholders are documented in [Build](docs/build/README.md) and
[Testing and evidence](docs/testing-and-evidence.md).

## Evidence boundary

Evidence is stored under an externally located runtime/evidence tree, normally
<code>EVIDENCE_ROOT/connector/run-id</code>. The names <code>connector</code>
and <code>run-id</code> are conceptual components, not literal directory
names: connector is one of the six names in the table and run ID is a
filesystem-safe token such as <code>six-core-20260712T120000Z</code>.

No statement here claims:

- production readiness or production hardening;
- CRS verification or CRS completeness;
- complete HTTP/2 or HTTP/3 verification;
- complete matrix coverage; or
- strict verification for all connectors.

Strict late intervention, advanced transports, CRS behavior, and extended
matrices remain separate evidence-gated work. Read the current
[testing reports](reports/README.md) and the
[testing and evidence guide](docs/testing-and-evidence.md) before making a result claim.

## Documentation

- [Documentation index](docs/README.md)
- [Repository concept](docs/repository-concept.md)
- [Getting started](docs/getting-started.md)
- [Configuration](docs/configuration.md)
- [Variables](docs/reference/variables.md)
- [Glossary](docs/reference/glossary.md)
- [Build guide](docs/build/README.md)
- [Connector guide](docs/connectors/README.md)
- [Testing and evidence](docs/testing-and-evidence.md)
- [Change traceability](docs/change-traceability.md)
- Documentation maintenance: `AGENTS.md` is an optional local instruction file for
  Codex and is not part of the versioned project documentation. It has no German
  companion file.
- [Operations and security](docs/operations-and-security.md)
- [Framework module](modules/ModSecurity-test-Framework/README.md)

Repository-owned English/German documentation is checked with:

~~~sh
make check-bilingual-docs
~~~

Generated reports must be changed through their generator/source of truth, not
by manual editing.
