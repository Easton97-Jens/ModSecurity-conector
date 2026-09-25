# Documentation

**Language:** English | [Deutsch](README.de.md)

This is the main navigation page for the ModSecurity Connector documentation.
If you are new to the project, start with **Getting started** and then choose
the connector and example that match your host. Detailed reference documents
remain available when you need exact variables, build contracts, evidence
semantics, or security boundaries.

The repository currently covers six host families and ten logical connector
profiles. The selected core documentation is HTTP/1.1-oriented. A source tree,
successful build, configuration check, or example file is not by itself proof
of production readiness or a verified runtime result.

## New here?

| Step | Read | What you get |
| --- | --- | --- |
| 1 | [Getting started](getting-started.md) | Clone, initialize the Framework, run the first checks, and choose a host/profile. |
| 2 | [Examples](../examples/README.md) | Pick an `off`, `safe`, `strict`, or `all` configuration for the selected logical solution. |
| 3 | [Connector index](connectors/README.md) | Understand the selected route, alternate logical profiles, and host-specific limitations. |
| 4 | [Configuration](configuration.md) | Learn which settings belong to the host, connector/Common Runtime, or ModSecurity engine. |
| 5 | [Build](build/README.md) | Prepare and build the selected host integration without confusing build success with runtime proof. |

## Find documentation by task

| I want to… | Start here | Then read |
| --- | --- | --- |
| understand the repository | [Architecture](architecture.md) | [Repository concept](repository-concept.md) |
| configure a connector | [Configuration](configuration.md) | [Examples](../examples/README.md) |
| choose a connector/profile | [Connector index](connectors/README.md) | the matching connector guide |
| build a connector | [Build](build/README.md) | [Compiler guides](build/compilers/README.md) |
| understand Phase 1–4 | [Architecture](architecture.md) | [Phase-4 mode and budget](phase4-mode-budget.md) |
| run tests or interpret a result | [Testing and evidence](testing-and-evidence.md) | [Reports](../reports/README.md) |
| understand variables | [Variables](reference/variables.md) | [Glossary](reference/glossary.md) |
| operate or deploy safely | [Operations and security](operations-and-security.md) | [SECURITY.md](../SECURITY.md) |
| understand CI security | [CI security tooling](security/ci-security-tooling.md) | [Trusted NGINX root broker](security/trusted-nginx-root-broker.md) |
| change project documentation | [Change traceability](change-traceability.md) | [Change Record archive](../reports/audits/change-records/README.md) |

## Connector guides

| Host family | Selected core route | Guide |
| --- | --- | --- |
| Apache | `native-httpd-module` | [Apache](connectors/apache.md) |
| NGINX | `native-nginx-http-module` | [NGINX](connectors/nginx.md) |
| HAProxy | `native-htx-filter` | [HAProxy](connectors/haproxy.md) |
| Envoy | `ext_proc` | [Envoy](connectors/envoy.md) |
| Traefik | `native-traefik-middleware` | [Traefik](connectors/traefik.md) |
| lighttpd | `patched-native-lighttpd` | [lighttpd](connectors/lighttpd.md) |

Some host families expose more than one logical solution. Treat each logical
profile as its own evidence scope; one profile does not prove another profile
in the same host family.

Each connector's `capabilities.json` records declared implementation state; it
is not a PASS result. Likewise, `minimal_runtime_smoke` names a deliberately
narrow runtime layer and must not be interpreted as full-lifecycle or
production-readiness evidence.

## Examples are part of the learning path

The [examples index](../examples/README.md) is the practical companion to this
documentation. It maps all ten logical solutions to their checked-in
`off`, `safe`, `strict`, and `all` layouts and explains which paths,
ports, rules files, sockets, and log destinations must be adapted before use.

Use examples as **configuration references**, not as deployment manifests.
Always validate the materialized host configuration and read the matching
connector limitations before sending traffic.

## Reference and maintenance

- [Variables](reference/variables.md) is the complete variable/placeholder reference.
- [Glossary](reference/glossary.md) defines repository-specific terminology.
- [Phase-4 mode and budget](phase4-mode-budget.md) defines the current `off` / `safe` / `strict` contract.
- [Reports](../reports/README.md) is the entry point for current and historical evidence/report material.
- [Common source-tree guide](../common/README.md) explains connector-neutral code ownership.
- [Framework module](../modules/ModSecurity-test-Framework/README.md) owns reusable test cases, schemas, runners, and normalizers.

English and German repository documentation must remain equivalent. Generated
documentation is maintained through its generator/source contract rather than
by editing generated output in isolation.
