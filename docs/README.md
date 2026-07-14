# Documentation index

**Language:** English | [Deutsch](README.de.md)

This directory is the documentation entry point for the selected six-connector
HTTP/1.1 core. It describes current repository boundaries without claiming
production readiness, CRS verification, complete HTTP/2/HTTP/3 verification, a
complete matrix, or strict behavior for every connector.

## Start here

| Need | Canonical document | Source-of-truth boundary |
| --- | --- | --- |
| Initialize a checkout | [Getting started](getting-started.md) | Framework setup and the limited first validation path |
| Target product monorepo concept | [Repository concept](repository-concept.md) | Binding target-state ownership, product, lifecycle, and Parent/Framework boundary |
| Repository architecture | [Architecture](architecture.md) | Checked-in source ownership and documented lifecycle boundary |
| Host, runtime, and engine configuration | [Configuration](configuration.md) | Complete per-connector syntax remains in <code>examples/</code> |
| Variables and terms | [Variables](reference/variables.md) / [Glossary](reference/glossary.md) | Root Makefile, wrappers, and documented contracts |
| Build one host | [Build](build/README.md) | Root/connector build inputs and compiler guides |
| Test or interpret artifacts | [Testing and evidence](testing-and-evidence.md) | Selected run records and Framework schemas |
| Operate safely | [Operations and security](operations-and-security.md) | Explicit deployment, limit, privacy, and provenance boundary |
| Use Codex extensions safely | [Codex extensions](development/codex-extensions.md) / [External agent services](security/external-agent-services.md) | Pinned provenance and explicit secret, data-egress, cost, and tool-boundary controls |
| Choose a connector | [Connector index](connectors/README.md) | Selected integration mode and connector guide |
| Trace a material change | [Change traceability](change-traceability.md) / [Change Records](../reports/audits/change-records/README.md) | Binding workflow, paired records, and evidence/data boundary |

## Connector guides

| Connector | Selected mode | Canonical guide |
| --- | --- | --- |
| Apache | <code>native-httpd-module</code> | [Apache](connectors/apache.md) |
| NGINX | <code>native-nginx-http-module</code> | [NGINX](connectors/nginx.md) |
| HAProxy | <code>native-htx-filter</code> | [HAProxy](connectors/haproxy.md) |
| Envoy | <code>ext_proc</code> | [Envoy](connectors/envoy.md) |
| Traefik | <code>native-traefik-middleware</code> | [Traefik](connectors/traefik.md) |
| lighttpd | <code>patched-native-lighttpd</code> | [lighttpd](connectors/lighttpd.md) |

The selected profile and the recorded integration mode are related but distinct
identities. The canonical state for a capability begins in each connector's
<code>capabilities.json</code>; a profile, build, source tree, or generated
inventory is not a PASS result.

## Current scope and evidence

The repository records selected lifecycle evidence by run ID. A narrow
<code>minimal_runtime_smoke</code>, a configuration load, or a source-level
contract check establishes only its stated layer. Read the current reports
through [Reports](../reports/README.md) before making a time-sensitive status
claim.

## Supporting material

- [Compiler guides](build/compilers/README.md)
- [License, origin, and operational boundary](operations-and-security.md)
- [Common source-tree guide](../common/README.md)
- [Configuration examples](../examples/README.md)
- [Framework module](../modules/ModSecurity-test-Framework/README.md)

Repository-owned English/German documentation is checked with
<code>make check-bilingual-docs</code>. Generated outputs must be changed
through their generator and source contract rather than by manual edits.
