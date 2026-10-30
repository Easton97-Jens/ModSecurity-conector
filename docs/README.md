# Documentation

**Language:** English | [Deutsch](README.de.md)

Start with the task you need to complete. The introductory guides explain the
project in small steps; the linked technical references retain the exact
syntax, prerequisites, source ownership, and limitations.

The repository has six host families and ten logical connector profiles. Its
selected core routes are HTTP/1.1-oriented. A build or configuration check is
not a production-readiness or full-protocol-coverage claim.

## First steps

| Step | Read | Outcome |
| --- | --- | --- |
| 1 | [Getting started](getting-started.md) | Initialize a checkout, prepare prerequisites, and run the first checks |
| 2 | [Examples](../examples/README.md) | Choose a host, logical profile, and configuration layout |
| 3 | [Configuration](configuration.md) | Separate host wiring, Common Runtime, and engine rules |
| 4 | [Build](build/README.md) | Build and validate the chosen integration |
| 5 | [Testing and evidence](testing-and-evidence.md) | Understand the active test selection and what each result proves |

Updating an existing installation? Read [Migration](migration.md) first.
Connector request/response size settings removed from current source are not
compatibility aliases. Do not copy them back from an old README or report.

## Find documentation by task

| I need to… | Start here | Detail |
| --- | --- | --- |
| understand the data flow | [Architecture](architecture.md) | [Repository concept](repository-concept.md) |
| choose the integration topology | [Connector index](connectors/README.md) | [Examples](../examples/README.md) |
| configure rules and body inspection | [Configuration](configuration.md) | [Body-limit ownership and Phase-4 mode](phase4-mode-budget.md) |
| compare body-handling limitations | [Ten-profile body-inspection matrix](body-inspection-review-matrix.md) | The selected connector guide |
| update an older configuration | [Migration](migration.md) | Current generated configuration references linked by each host example |
| prepare or build a host | [Build](build/README.md) | [Compiler guides](build/compilers/README.md) |
| select variables or toolchains | [Variables](reference/variables.md) | [Version pins](reference/version-pins.md) |
| run standard tests | [Testing and evidence](testing-and-evidence.md) | [Test entry points](../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_tests/README.md) |
| interpret a runtime report | [Reports](../reports/README.md) | Profile, rules, revision, run ID, artifacts, and remaining limitations |
| operate safely | [Operations and security](operations-and-security.md) | [Vulnerability reporting](../SECURITY.md) |
| understand CI and scanners | [CI security tooling](security/ci-security-tooling.md) | [CI entry points](../ci/README.md) |
| configure static analysis | [SonarQube Cloud analysis](sonarqube-analysis.md) | Analyzer scope and exact-revision evidence |
| understand privileged NGINX checks | [Trusted NGINX root broker](security/trusted-nginx-root-broker.md) | Protected execution is separate from ordinary PR checks |
| understand a term | [Glossary](reference/glossary.md) | Technical identifiers remain searchable in source |
| change the project | [Change traceability](change-traceability.md) | [Change Records](../reports/audits/change-records/README.md) |
| check external origin | [Origin and license references](../licenses/README.md) | Connector `ORIGIN.md` and `SOURCE_MAP.json` |

## Connector guides

| Host family | Selected core integration mode | Guide |
| --- | --- | --- |
| Apache | `native-httpd-module` | [Apache](connectors/apache.md) |
| NGINX | `native-nginx-http-module` | [NGINX](connectors/nginx.md) |
| HAProxy | `native-htx-filter` | [HAProxy](connectors/haproxy.md) |
| Envoy | `ext_proc` | [Envoy](connectors/envoy.md) |
| Traefik | `native-traefik-middleware` | [Traefik](connectors/traefik.md) |
| lighttpd | `patched-native-lighttpd` | [lighttpd](connectors/lighttpd.md) |

This table lists host-family core routes, not the complete logical-profile
inventory. The [connector index](connectors/README.md) also covers the
SPOE/SPOP, ext_authz, forwardAuth, and Stock lighttpd solutions. A profile's
source or `capabilities.json` describes implementation state; it is not a
`PASS` result. One profile never supplies runtime proof for a sibling profile.

## Examples, tests, and evidence

The [examples index](../examples/README.md) links all ten logical solutions and
their `off`, `safe`, `strict`, and `all` layouts. Read the matching host guide
before changing module paths, rules files, listeners, upstreams, sockets, or
log destinations. Examples are configuration references, not ready-made secure
deployments. An `all` layout may select a strict mode that a particular host
profile cannot admit.

Normal functional selection is owned by
[config/testing/active-cases.json](../modules/ModSecurity-test-Framework/connector_suite/config/testing/active-cases.json).
`make check-active-inventory` checks the complete selection without executing
it; `make test` runs the active selection with its actual prerequisites.
`make quick-check` includes static checks and admitted functional subsets.
The core ceiling and the separately authorized offline Python exception must
not be confused with complete connector E2E coverage.

A `minimal_runtime_smoke` is deliberately narrow. Builds, source checks,
configuration loads, inventories, scanner results, and full host runs remain
different forms of evidence. Read [Testing and evidence](testing-and-evidence.md)
before interpreting a result. Historical evidence and
[PR #382 closeout](pr-382-merge-readiness.md) or
[PR #410 I12 closeout](pr-410-i12-closeout-20261024.md) describe their recorded
scope; they do not authorize another campaign or certify every current profile.

## Documentation ownership

Parent owns connector product integration and its documentation. The
[Framework submodule](../modules/ModSecurity-test-Framework/README.md) owns
reusable test cases, schemas, runners, and normalizers. The
[Common source guide](../common/README.md) explains shared implementation
ownership.

Keep English and German companions technically equivalent. Check them with
`make check-bilingual-docs` and validate links with `make check-doc-links`.
Compiler guides, `examples/common/`, host configuration references, and other
generated outputs must follow their generator/source contract. New explanations
belong in maintained guides or in the generator, not in an isolated output edit.
