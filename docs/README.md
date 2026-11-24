# Documentation

**Language:** English | [Deutsch](README.de.md)

## First steps

Follow [Getting started](getting-started.md) to initialize a checkout and
run the first checks. Use [Migration](migration.md) before updating an existing
installation, especially if its configuration contains connector body-size options.

## Find documentation by task

| Task | Guide |
| --- | --- |
| Choose a host and topology | [Connector profiles](connectors/README.md) and [example bundles](../examples/README.md) |
| Prepare a toolchain and build | [Build guide](build/README.md), [compiler guides](build/compilers/README.md), [version pins](reference/version-pins.md) |
| Configure a host or rules | [Configuration](configuration.md) and [variable reference](reference/variables.md) |
| Choose body limits and a Phase-4 mode | [Body-limit ownership](phase4-mode-budget.md) and [inspection limits by profile](body-inspection-review-matrix.md) |
| Understand the data flow | [Architecture](architecture.md) and [repository concept](repository-concept.md) |
| Operate a connector | [Operations and security](operations-and-security.md) and [vulnerability reporting](../SECURITY.md) |
| Work on CI or analysis | [CI entry points](../ci/README.md), [security tooling](security/ci-security-tooling.md), [SonarQube analysis](sonarqube-analysis.md) and [NGINX root broker](security/trusted-nginx-root-broker.md) |
| Trace a change or external source | [Change traceability](change-traceability.md) and [origin and license references](../licenses/README.md) |
| Look up a term | [Glossary](reference/glossary.md) |

## Connector guides

The [connector index](connectors/README.md) identifies all ten profiles and
links their host-specific requirements. Use the matching guide when adapting an
[example bundle](../examples/README.md).

## Examples, tests, and evidence

[Testing and evidence](testing-and-evidence.md) explains the active selection
and the scope of each check. [Reports](../reports/README.md) holds recorded
runtime runs and historical evidence.

## Documentation ownership

Maintain English and German companions together. Run
`make check-bilingual-docs` and `make check-doc-links`. Update compiler guides
and generated references through their source and generator.
