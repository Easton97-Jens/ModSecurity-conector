# Getting started

**Language:** English | [Deutsch](getting-started.de.md)

## 1. Check prerequisites

Use Git, Make, and the interpreter pinned by `.python-version`. Go components
use `.go-version`. Check the selected host's [build requirements](build/README.md)
and the [version pins](reference/version-pins.md).

## 2. Clone and initialize

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
make check-framework
```

For an existing clone, run `git submodule update --init --recursive` if the
submodules are missing. The default Framework location is
`modules/ModSecurity-test-Framework`. Use a trusted matching checkout if
overriding `FRAMEWORK_ROOT`.

Local delegated targets run `make python-env` to prepare the pinned Python
environment and install the Framework's locked dependencies. Set
`PYTHON_ENV_ROOT` to place the environment outside the checkout, or set
`PYTHON` to a prepared interpreter. See the [variable reference](reference/variables.md).

## 3. Run the first checks

```sh
make check-active-inventory
make quick-check
```

`make check-active-inventory` validates selection. `make quick-check` runs
static checks and admitted functional subsets. Use `make test` with the
compiler, SDK and host prerequisites of the active selection.
[Testing and evidence](testing-and-evidence.md) describes the covered cases.

## 4. Choose a host and topology

Select a [logical connector profile](connectors/README.md) and check its
[body-inspection boundaries](body-inspection-review-matrix.md).

## 5. Adapt an example

Start with the matching [example bundle](../examples/README.md). Adapt paths,
listeners, upstreams, service identities, private sockets and log destinations.
Set body access and limits in the engine rules. For an older configuration,
follow [Migration](migration.md).

## 6. Build and validate the selected host

For example, with the NGINX prerequisites in place:

```sh
make build-nginx
make check-config-nginx
```

Find other host targets in the [build guide](build/README.md). An explicit
`BUILD_ROOT` must be an absolute, writable path outside the checkout.
See [Variables](reference/variables.md).

## 7. Interpret results and troubleshoot

A build checks compilation. A configuration check verifies that the host loads
the selected configuration. Use profile-specific [runtime evidence](testing-and-evidence.md)
to verify how rules act on traffic.

- For a missing or mismatched Framework checkout, check the [version pins](reference/version-pins.md).
- For rejected legacy options, see [Migration](migration.md). For rejected Strict
  startup, check the profile's late-action requirements.
- For an empty or rejected test selection, inspect the [active inventory](../modules/ModSecurity-test-Framework/connector_suite/config/testing/active-cases.json)
  and the checked-out revision.

## Specialist campaigns are separate

See [Testing and evidence](testing-and-evidence.md) for the prerequisites and
opt-in requirements for full-lifecycle or protected host runs.
