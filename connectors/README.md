# Connector implementations

**Language:** English | [Deutsch](README.de.md)

## Purpose and evidence boundary

This directory contains the repository-owned integration layers for Apache,
NGINX, HAProxy, Envoy, Traefik, and lighttpd. A connector tree combines its
host-specific code, metadata, harness wiring, and local design notes with the
connector-neutral interfaces in [Common](../common/README.md).

The trees describe implementation and declared capabilities; they are not a
substitute for a run. Current selected HTTP/1.1 core results belong to
run-scoped evidence and [current reports](../reports/current/). Do not infer
production readiness, complete CRS coverage, HTTP/2 or HTTP/3 verification, or
strict verification for every connector from a source tree or a successful
build.

## Structure and source of truth

| Path | Purpose | Source of truth / maintenance rule |
| --- | --- | --- |
| `_template/` | Scaffold for a new connector | Copy it only when beginning a new connector; it makes no implementation or runtime claim. |
| `<connector>/` | One host integration | `<connector>` is a documentation placeholder for exactly `apache`, `nginx`, `haproxy`, `envoy`, `traefik`, or `lighttpd`; for example, `connectors/nginx/`. |
| `<connector>/src/` | Host-specific source and adapters | The checked-in source and associated headers define the implementation. Keep host SDK use here, not in `common/`. |
| `<connector>/harness/` | Connector-local launch and observation wiring | The harness plus the root target that invokes it defines the runnable integration contract. |
| `<connector>/capabilities.json` and `metadata.*` | Declared capability and connector metadata | These machine-readable files are authoritative declarations, not promotion evidence. |
| `<connector>/ORIGIN.md` and `SOURCE_MAP.json` | Origin, license, and import provenance | Update them whenever imported or derived material changes. |
| `<connector>/README.*`, `ORIGIN.md`, and `TODO.md` | Code-adjacent source, provenance, and work-tracking notes | Keep reader-facing architecture, configuration, lifecycle, limitations, and validation guidance in [docs/connectors](../docs/connectors/README.md). |

The root [Makefile](../Makefile) is authoritative for target names and their
defaults. The Framework submodule owns the reusable case catalog and runner
schemas. The connector-specific documentation index explains the current
supported route; the evidence index explains which generated artifacts can
support a claim.

## Adding or changing a connector

Start with `_template/`, then create `connectors/<connector>/` with the files
listed there. Replace `<connector>` only with one of the six names above; it
is not a literal directory name. Add host-specific source under `src/`, harness
code under `harness/`, and origin/metadata updates beside the source. Add or
update the current user-facing guide at `docs/connectors/<connector>.md` and
its German companion; update the generator when that guide is generated.

Do not add executable catalog cases under a connector tree: reusable cases,
normalizers, and runners are Framework-owned. Do not store build directories,
download caches, logs, result JSON, credentials, private keys, or canonical
evidence here. Do not place connector-specific server/proxy SDK code in
`common/`.

## Variables and documentation placeholders

The values below are inputs to root targets, not values that a connector source
file silently reads. See the central [variables and placeholders
reference](../docs/reference/variables.md) and the
[glossary](../docs/reference/glossary.md) for the complete contract.

| Name | Local meaning | Requiredness, format, and example |
| --- | --- | --- |
| `FRAMEWORK_ROOT` | Location of the Framework submodule used by delegated targets | Required by targets that delegate to the Framework. Its repository default is `modules/ModSecurity-test-Framework`; use an existing trusted checkout such as `/srv/src/ModSecurity-test-Framework` only when intentionally overriding it. It is not a build or evidence path. |
| `BUILD_ROOT` | Parent for generated build and runtime work | Optional. The root Makefile derives it below its verified run root; an override must be an absolute writable directory outside the checkout, for example `/srv/modsecurity-work/build`. A bad path can make a target report `BLOCKED` or exit `77`. |
| `NO_CRS_RUN_ID` | Identifier that groups one aggregate No-CRS evidence run | Required by aggregate evidence commands. It has no default and must be a filesystem-safe token, for example `six-core-20260712T120000Z`; never put secrets, usernames, or ticket text in it. |
| `<repository-root>` | Documentation-only placeholder for this checkout's absolute root | It contains `Makefile` and `docs/`; use a real path such as `/srv/src/ModSecurity-conector` when a command explicitly requests one. Do not copy the angle brackets into a command. |
| `<external-source-root>` | Documentation-only placeholder for a trusted source checkout outside this repository | It is optional unless a command says otherwise; `/srv/src/ModSecurity-test-Framework` is an example. It is neither a cache/output location nor evidence that the external checkout passed. |

No value above is a secret. Keep credentials and private material out of
connector configuration, command lines, logs, and evidence.

## Relevant targets

Use a literal connector name in a target. For example,
`make check-nginx-common-adoption` is one instance of the documented
`check-<connector>-common-adoption` pattern; `<connector>` has the six allowed
values listed above.

| Target | Purpose and outcome boundary |
| --- | --- |
| `make check-<connector>-common-adoption` | Checks a connector's use of Common contracts. It is a structural check, not host-runtime proof. |
| `make build-<connector>` and `make check-config-<connector>` | Build or validate the selected connector configuration where the target exists. A passing process exit only satisfies that target's contract. |
| `make full-lifecycle-<connector>` | Runs the selected native HTTP/1.1 core profile for one connector and writes run-scoped artifacts. |
| `make full-lifecycle-all-connectors` | Runs all six selected profiles; provide a safe `NO_CRS_RUN_ID` for a canonical aggregate candidate. |
| `make check-six-connector-core-completion` | Validates the evidence gate for the selected six-connector core; it does not widen the supported protocol or lifecycle boundary. |
| `make lint` | Runs repository contracts, documentation checks, and syntax checks. It does not itself create canonical runtime evidence. |

For compiler, configuration, test-level, and evidence details, use
[Build](../docs/build/README.md), [Testing](../docs/testing-and-evidence.md), and
[Evidence](../docs/testing-and-evidence.md).
