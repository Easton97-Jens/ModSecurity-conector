# Apache Smoke Harness

Status: scaffolded

This harness is a connector-specific proof-of-concept runner for the Apache
module built from the read-only `ModSecurity-apache` source copy. It is not a
full regression test suite.

## Boundaries

- Uses only artifacts under `BUILD_ROOT`.
- Does not build or modify any `/root/conecter/*` repository.
- Does not import Apache connector source into this monorepo.
- Reports `pass` only when Apache returns HTTP `403` for the shared minimal
  `ARGS:test` case.

## Usage

```sh
BUILD_ROOT=/src/ModSecurity-conector-build \
sh ci/prepare-apache-build.sh

BUILD_ROOT=/src/ModSecurity-conector-build \
sh connectors/apache/harness/run_apache_smoke.sh
```

If `apxs`, Apache, the module, or `libmodsecurity.so` is missing, the scripts
exit `77` and mark the result as `blocked`.

## Shared Case

The harness implements the same rule and request described by:

```text
tests/common/cases/minimal/phase2_args_block.yaml
```

There is intentionally no YAML runner yet; the file is the documented data model
for future Apache and NGINX harness parity.
