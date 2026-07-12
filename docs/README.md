# Documentation index

**Language:** English | [Deutsch](README.de.md)

This directory is the documentation entry point for the connector repository.
It describes the current six-connector HTTP/1.1 core lifecycle work without
claiming production readiness, CRS verification, HTTP/2 verification, HTTP/3
verification, a complete matrix, or strict behavior for all connectors.

## Start here

| Area | Read this when you need | Source of truth |
|---|---|---|
| [Configuration](configuration/variables.md) | Variables, path roles, placeholders, target inputs, IDs, statuses, or integration modes | Root Makefile and runtime wrappers |
| [Glossary](reference/glossary.md) | A definition of EOS, HTX, ext_proc, APXS, UDS, Evidence, or another repository term | This reference plus local explanations |
| [Build](build/README.md) | Build families, toolchain prerequisites, caches, and safe build paths | Root and connector Makefiles |
| [Connectors](connectors/README.md) | The selected host route and documentation entry point for one connector | Connector metadata, capabilities, and harnesses |
| [Testing](testing/README.md) | Target selection, statuses, case IDs, and test boundaries | Root targets and Framework case catalog |
| [Evidence](evidence/README.md) | Artifact layout, validation, promotion, privacy, and run IDs | Runtime lifecycle wrappers and Framework schemas |
| [Architecture](architecture/README.md) | Common layer, connector boundaries, and architecture decisions | Checked-in architecture documents |
| [Development](development/documentation-style-guide.md) | How to write or review documentation safely | This style guide |
| [Reports](../reports/testing/README.md) | Current generated and manually maintained test/report entry points | Report generators and report metadata |
| [Framework module](../modules/ModSecurity-test-Framework/README.md) | Framework-owned catalog, schemas, runners, and CI documentation | Framework repository |

All relative paths in this table start at the repository root or this
<code>docs/</code> directory as indicated by the link. Generated reports stay
under <code>reports/</code>; do not manually alter a file marked generated.

## Navigation by task

### Run a local structural check

Use the following command after changing repository-owned documentation:

~~~sh
make check-bilingual-docs
~~~

The target checks English/German companion files and local links. It does not
run all connectors or create runtime evidence. See
[Testing](testing/README.md) for status and exit-code meanings.

### Prepare or run a selected connector route

Start with [Build](build/README.md), then the matching entry in
[Connectors](connectors/README.md). The placeholder
<code>&lt;connector&gt;</code> accepts only <code>apache</code>,
<code>nginx</code>, <code>haproxy</code>, <code>envoy</code>,
<code>traefik</code>, or <code>lighttpd</code>; for example:

~~~sh
make build-nginx
~~~

This builds one selected route. It does not by itself prove runtime behavior
or promote a capability.

### Work with canonical evidence

Choose a safe run ID and evidence directory as described in
[Configuration](configuration/variables.md#no-crs-and-evidence-variables).
Then use the exact target family documented in
[Evidence](evidence/README.md). A run ID is a filesystem-safe token such as
<code>six-core-20260712T120000Z</code>; it must not contain secrets or
personal data.

## Documentation ownership

- Repository-owned explanations, navigation, and current guides belong under
  <code>docs/</code>, connector directories, or reports as appropriate.
- The Framework owns reusable case schemas, catalog mechanics, and framework
  runners in <code>modules/ModSecurity-test-Framework/</code>.
- Generated material belongs at its generator-defined location. Change its
  generator/source of truth, preserve provenance, and regenerate.
- Historical reports preserve their original facts and should be marked
  historical rather than rewritten as current state.
- [Historical documentation](archive/README.md) contains retained repository
  inventories and issue snapshots that are not current guidance.

## Current connector status sources

The six selected connector names are Apache, NGINX, HAProxy, Envoy, Traefik,
and lighttpd. Each connector's checked-in scope declaration is
`connectors/<connector>/capabilities.json`; its connector guide explains the
host route and the evidence boundary. A `minimal_runtime_smoke` status denotes
a narrow, connector-specific runtime path only. It never substitutes for a
canonical aggregate result or for unexecuted catalog cases.

## Bilingual policy

Every repository-owned English document under <code>docs/</code> has a
<code>.de.md</code> companion with the same technical names, defaults, paths,
IDs, statuses, and targets. Read the
[documentation style guide](development/documentation-style-guide.md) before
adding a variable, placeholder, command example, or evidence claim.
