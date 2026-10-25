# Getting started

**Language:** English | [Deutsch](getting-started.de.md)

## Scope

This is the shortest safe path from a fresh checkout to repository validation.
It prepares neither a production deployment nor a general runtime claim.

## Initialize the Framework

```sh
git submodule update --init --recursive
make check-framework
```

`FRAMEWORK_ROOT` normally selects `modules/ModSecurity-test-Framework`. Set it
only to a trusted, existing Framework checkout outside this repository. A
missing prerequisite is reported as the documented blocked/prerequisite exit
condition; do not substitute an unrelated system installation.

## Validate the checkout

```sh
make quick-check
```

This validates static repository contracts and admitted functional subsets of
the single [active inventory](../config/testing/active-cases.json). Its global
limit is 100 fully expanded behavioral cases, including infrastructure and
runtime cases. Use <code>make check-active-inventory</code> to admit the complete
selection before test execution. <code>make test</code> runs the active selection
and needs its real compiler, SDK and host prerequisites. Group/case filters and
standard aliases are subsets, not full profile qualification. See
[Testing and evidence](testing-and-evidence.md) for archive disposition, lost
coverage and distinct profiles.

## Choose the next guide

| Goal | Canonical guide |
| --- | --- |
| Build, configure, or start one host | [Build](build/README.md) and the relevant [connector guide](connectors/README.md) |
| Adapt a profile or directive | [Configuration](configuration.md) and the complete connector reference in `examples/` |
| Run or interpret evidence | [Testing and evidence](testing-and-evidence.md) |
| Review limits, privacy, origin, or operations | [Operations and security](operations-and-security.md) |

The broader aggregate example below is retained only for a separately
authorized specialist assessment. It is outside automatic default selection,
requires <code>ON_DEMAND_TESTS=1</code> and does not reopen closed I12 work. Use a
filesystem-safe, non-secret run ID:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
ON_DEMAND_TESTS=1 NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

An exit status of zero applies only to the recorded command and selected run.
It does not claim production readiness, CRS verification, complete protocol
coverage, a full matrix, or Strict behavior for every connector.
