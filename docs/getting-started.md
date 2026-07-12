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

This validates repository contracts, documentation, and selected structural
checks. It does not build every host, execute all connector traffic, or create
canonical lifecycle evidence.

## Choose the next guide

| Goal | Canonical guide |
| --- | --- |
| Build, configure, or start one host | [Build](build/README.md) and the relevant [connector guide](connectors/README.md) |
| Adapt a profile or directive | [Configuration](configuration.md) and the complete connector reference in `examples/` |
| Run or interpret evidence | [Testing and evidence](testing-and-evidence.md) |
| Review limits, privacy, origin, or operations | [Operations and security](operations-and-security.md) |

For a selected aggregate run, use a filesystem-safe, non-secret run ID:

```sh
run_id="core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-all-connectors
NO_CRS_RUN_ID="$run_id" make check-six-connector-core-completion
```

An exit status of zero applies only to the recorded command and selected run.
It does not claim production readiness, CRS verification, complete protocol
coverage, a full matrix, or Strict behavior for every connector.
