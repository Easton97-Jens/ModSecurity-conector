# ModSecurity Connector

**Language:** English | [Deutsch](README.de.md)

Connect libModSecurity to Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd.
This repository supplies the host integrations, shared runtime, configuration
examples, build orchestration, and tools for checking their behavior. The
ModSecurity engine evaluates the rules; each connector supplies the host data
and translates an engine decision into an action the host can perform.

**New to the project?** Read [Getting started](docs/getting-started.md), then
choose a host in [Examples](examples/README.md). **Updating an existing setup?**
Read [Migration and current behavior](docs/migration.md) before reusing an old
configuration: connector-owned request/response body-size options have been
removed, and the standard test selection has changed.

## Choose a host and profile

There are six host families and ten logical connector profiles. A profile is a
particular integration topology, not a guarantee that every protocol or late
intervention is supported.

| Host family | Logical profiles | Where to begin |
| --- | --- | --- |
| Apache | `apache` | [Guide](docs/connectors/apache.md) / [Examples](examples/apache/README.md) |
| NGINX | `nginx` | [Guide](docs/connectors/nginx.md) / [Examples](examples/nginx/README.md) |
| HAProxy | `haproxy-htx`, `haproxy-spoe-spop` | [Guide](docs/connectors/haproxy.md) / [Examples](examples/haproxy/README.md) |
| Envoy | `envoy-ext-proc`, `envoy-ext-authz` | [Guide](docs/connectors/envoy.md) / [Examples](examples/envoy/README.md) |
| Traefik | `traefik-native-uds`, `traefik-forwardauth` | [Guide](docs/connectors/traefik.md) / [Examples](examples/traefik/README.md) |
| lighttpd | `lighttpd-patched`, `lighttpd-stock` | [Guide](docs/connectors/lighttpd.md) / [Examples](examples/lighttpd/README.md) |

Direct/native routes and authorization routes are not interchangeable.
SPOE/SPOP, ext_authz, and forwardAuth need their documented response companion
or observer for response phases. That companion does not remove the request
sampling/buffering limits of the authorization route. Patched-native lighttpd
and its Stock sidecar are separate solutions, not fallback modes.

The [connector index](docs/connectors/README.md) distinguishes logical profile
IDs, root lifecycle profile names, and recorded integration modes. See the
[body-inspection matrix](docs/body-inspection-review-matrix.md) for the actual
boundaries of all ten profiles.

## Quick start

Use Git, Make, and the prerequisites documented in the [build guide](docs/build/README.md).
Toolchain and Framework revisions are selected by the checked-in
[version-pin contract](docs/reference/version-pins.md), not by the newest
version available on the machine.

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
make check-active-inventory
make quick-check
```

For an existing clone without its submodules, first run
`git submodule update --init --recursive`. `FRAMEWORK_ROOT` normally points to
`modules/ModSecurity-test-Framework`; only override it with a trusted matching
checkout.

`make check-active-inventory` validates the complete selected test inventory
without starting tests. `make quick-check` runs static checks and admitted
functional subsets. Neither command qualifies every host/profile for deployment.
`make test` executes the active selection and needs its real compiler, SDK, and
host prerequisites. Missing prerequisites must not be disguised as a pass.

## Commands by task

Run commands from the repository root. The root `Makefile` is the command
reference; the linked guides describe prerequisites and outputs.

| Task | Command or guide | What the result establishes |
| --- | --- | --- |
| Check the checkout | `make quick-check` | Static contracts and the selected functional subsets |
| Check test selection without execution | `make check-active-inventory` | Admission of the complete active inventory |
| Run the standard test selection | `make test` | Results for the cases actually selected and executed |
| Build a selected integration | `make build-nginx` | Build success for that route, not traffic behavior |
| Validate host configuration | `make check-config-apache` | Configuration loading, not P1–P4 runtime proof |
| Check documentation pairing and links | `make check-bilingual-docs` / `make check-doc-links` | Documentation consistency |
| Interpret a recorded run | [Testing and evidence](docs/testing-and-evidence.md) | The exact profile, rules, run ID, artifacts, and limitations |

Normal local and CI tests use one authority:
[config/testing/active-cases.json](modules/ModSecurity-test-Framework/connector_suite/config/testing/active-cases.json). The
100-case core ceiling and the separately authorized guarded offline Python
exception are distinct counts; the exception does not add connector E2E cases.
Use the inventory and its admission output for the selected counts instead of
assuming a command name means complete coverage.

Full-lifecycle campaigns are specialist work, not the default next step. They
require a separate current authorization and `ON_DEMAND_TESTS=1`. The flag is
not a general bypass and does not reopen closed I12 work. Protected NGINX host
checks retain their separately controlled exact-head execution boundary.

## Body inspection and Phase 4

| Phase | Data supplied to the engine |
| --- | --- |
| P1 | Request headers |
| P2 | Request body |
| P3 | Response headers |
| P4 | Response body |

**Body inspection limits belong to libModSecurity.** Configure request policy
with `SecRequestBodyLimit`, `SecRequestBodyNoFilesLimit`, and
`SecRequestBodyLimitAction`; configure response policy with
`SecResponseBodyLimit` and `SecResponseBodyLimitAction`. Access and response
MIME selection also remain engine settings. Omitted engine directives retain
native engine semantics; the connector must not inject replacement defaults
or truncate input to a connector-selected inspection prefix.

| Phase-4 mode | Meaning | Does not mean |
| --- | --- | --- |
| `off` | Native intervention/error handling without the additional Safe/Strict late-action policy | The engine or response inspection is disabled |
| `safe` | The supported conservative handling of a decision after response output has started | Native Reject results or genuine processing errors may be ignored |
| `strict` | The supported strict late action of the selected host/profile | Every profile can abort an already-started response |

`all` is an example layout, not a fourth Phase-4 mode. A strict configuration
can be rejected at startup when the profile lacks the required host action.
Modes never choose a body-size limit or an engine limit action.

Old settings such as `request_body_limit`, `response_body_limit`,
`body_limit_action`, and `modsecurity_phase4_body_limit` are removed, not
silently accepted compatibility controls. Follow the [migration guide](docs/migration.md)
and the authoritative [body-limit ownership contract](docs/phase4-mode-budget.md).
Working buffers, individual frames/messages, metadata, timeouts, file checks,
and the documented host authorization ceilings remain separate safety limits.

## Repository map

| Path | What belongs here |
| --- | --- |
| `common/` | Connector-neutral runtime contracts and shared support |
| `connectors/` | Host-specific source, integration, metadata, and harnesses |
| `docs/` | User guides, architecture, contracts, operations, and references |
| `examples/` | Host/profile configurations to adapt and validate |
| `ci/` and `tests/` | Parent checks, orchestration, and regression coverage |
| `reports/` | Run-scoped reports, current summaries, and historical records |
| `licenses/` | External origins, source bases, and retained upstream notices |
| `modules/ModSecurity-test-Framework/` | Independent Framework submodule with reusable cases, schemas, runners, and normalizers |

Keep generated build, cache, runtime, logs, and evidence outside the checkout.
Use documented paths such as `BUILD_ROOT` and `EVIDENCE_ROOT` and non-secret,
filesystem-safe run IDs. Never put credentials or sensitive traffic bodies in
versioned examples or review artifacts.

## Results, security, and provenance

A successful build, configuration load, capability declaration, smoke, or
scanner proves only its own scope. This README does not claim production
readiness, CRS completeness, full HTTP/2 or HTTP/3 coverage, a complete matrix,
or strict behavior for all profiles. Consult [Reports](reports/README.md)
for the recorded run and [Operations and security](docs/operations-and-security.md)
for deployment decisions. Report vulnerabilities as described in [SECURITY.md](SECURITY.md).

[licenses/](licenses/README.md) explains where selected external material came
from, its recorded upstream basis, and how local adaptations differ. It is not
a repository-wide license declaration. Preserved upstream notices still
accompany the relevant material; a local modification does not erase its
upstream origin. Per-file provenance is recorded in the relevant `ORIGIN.md`
and `SOURCE_MAP.json`. There is no top-level `LICENSE` at this revision.

## Documentation

Start at the [documentation index](docs/README.md). It links the current
configuration and body-inspection contracts, compiler guides, active testing,
version pins, CI/Sonar analysis, evidence closeouts, and operational guidance.
English and German companions are maintained together. Generated references
must be changed through their source/generator, not edited in isolation.
