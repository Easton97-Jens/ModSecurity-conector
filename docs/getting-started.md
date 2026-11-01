# Getting started

**Language:** English | [Deutsch](getting-started.de.md)

This guide takes you from a fresh checkout to a selected host configuration and
a correctly interpreted test result. It is a development starting point, not a
production deployment recipe.

## 1. Check prerequisites

Use Git and Make, the Python version selected by `.python-version`, and the
host/compiler prerequisites in the [build guide](build/README.md). Go-based
components additionally use `.go-version`. Both version files are generated
views of `ci/tooling/project-versions.lock.json`; do not replace a missing
pinned interpreter with an unrelated system version. See [Version pins](reference/version-pins.md).

Different targets need different dependencies. A documentation check is not a
reason to install every host, and a missing SDK is not a documentation failure.
Use the target-specific [compiler guides](build/compilers/README.md) rather than
guessing package names or host versions.

## 2. Clone and initialize

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
```

Already cloned without submodules? Run `git submodule update --init --recursive`
first. The default Framework location is `modules/ModSecurity-test-Framework`.
An external `FRAMEWORK_ROOT` must be a trusted matching source checkout, not a
build directory or an arbitrary system installation.

For an intended development environment, the repository provides
`make setup-dev` to prepare Python development dependencies through the
Framework. It changes the development environment; it does not install or
qualify every connector host. Follow the current build/Python instructions for
the selected interpreter and external working paths.

## 3. Run the first checks

```sh
make check-active-inventory
make quick-check
```

The first command admits the complete
[active inventory](../modules/ModSecurity-test-Framework/connector_suite/config/testing/active-cases.json) without executing tests.
The second checks static repository contracts and admitted functional subsets.
Normal selection has a 100-case core ceiling and a separately authorized
guarded offline Python exception; that exception does not expand connector
E2E selection. Read admission output for the selected counts.

Run `make test` when the active selection's compiler, SDK, and host
prerequisites are available. Do not infer all-profile qualification from
standard aliases or group/case filters. See [Testing and evidence](testing-and-evidence.md)
for the archive boundary and coverage no longer selected by default.

## 4. Choose a host and topology

| Host family | Direct/native logical profile | Other logical profile |
| --- | --- | --- |
| Apache | `apache` | — |
| NGINX | `nginx` | — |
| HAProxy | `haproxy-htx` | `haproxy-spoe-spop` |
| Envoy | `envoy-ext-proc` | `envoy-ext-authz` |
| Traefik | `traefik-native-uds` | `traefik-forwardauth` |
| lighttpd | `lighttpd-patched` | `lighttpd-stock` |

Choose the topology you actually need. Authorization/companion routes and
native streaming routes differ, especially in request-body visibility and
post-commit actions. The Stock lighttpd sidecar is its own traffic-owning
solution. Read the [connector index](connectors/README.md) and the
[body-inspection matrix](body-inspection-review-matrix.md) before substituting
one profile for another.

## 5. Adapt an example

Open the matching host under [Examples](../examples/README.md). A `safe` bundle
is a useful learning reference; `off` preserves native handling without the
additional late-action policy. `strict` requires a host action supported by the
profile and can be rejected at startup. `all` shows the complete configuration
layout, not a fourth Phase-4 mode or a guarantee that the bundle can run.

Adapt module and rules paths, listeners/upstreams, service identities, private
sockets, and log destinations before loading the file. Configure body access,
inspection limits, and limit actions in engine rules. Removed connector
request/response limits are not accepted as compatibility controls; an existing
setup must follow [Migration](migration.md).

Keep `SecRuleEngine DetectionOnly`, `SecRuleEngine Off`, a disabled host
connector, and Phase-4 `off` separate: they act at different layers.

## 6. Build and validate the selected host

For example, after preparing the required NGINX inputs:

```sh
make build-nginx
make check-config-nginx
```

Use another documented root target for another host; do not assume every
logical profile has an identically named Make target. Root lifecycle names,
logical profile IDs, and integration-mode names are distinct.

Generated build/runtime data belongs outside the checkout. An explicitly set
`BUILD_ROOT` must be an absolute writable external directory; see
[Variables](reference/variables.md). Build success proves the build stage;
configuration success proves that the host accepted the selected configuration.
Neither result alone proves rule enforcement on traffic.

## 7. Interpret results and troubleshoot

| Observation | Next step |
| --- | --- |
| Framework missing or wrong revision | Initialize the recorded submodules and check the version-pin contract |
| Python or SDK prerequisite missing | Use the documented target prerequisites; do not bypass the check |
| Old body-limit option rejected | Remove the obsolete connector option and review engine rules using the migration guide |
| Strict startup rejected | Read the profile's strict boundary; do not describe a rejected configuration as supported |
| Active group empty, unknown, or source binding changed | Inspect the inventory and intended revision; do not truncate selection or disable admission |
| Build/configuration passes but runtime behavior is unknown | Collect and validate the separately authorized, profile-specific evidence |

A command's zero exit status is scoped to that command and run. It is not a
production, CRS-completeness, full HTTP/2/HTTP/3, complete-matrix, or
strict-for-every-profile claim.

## Specialist campaigns are separate

Do not start an aggregate lifecycle campaign as a routine setup step. A
separately authorized assessment may use the following documented sequence
with its real prerequisites and a non-secret, filesystem-safe run ID:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
ON_DEMAND_TESTS=1 NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

`ON_DEMAND_TESTS=1` is an explicit specialist opt-in, not a default or a general
bypass. It does not reopen closed I12 work. Protected NGINX execution remains a
separate trust boundary. Read [Testing and evidence](testing-and-evidence.md)
and [Operations and security](operations-and-security.md) before runtime work.
