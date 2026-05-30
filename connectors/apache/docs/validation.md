# Apache Validation

Status: evidence-scoped

This document is the Apache-specific validation counterpart to the generic
template document at `connectors/_template/docs/validation.md`.

## Repository Evidence

- `connectors/apache/README.md` documents the adapter-owned Apache source tree,
  Autotools/APXS build inputs, metadata, and harness.
- `connectors/apache/harness/run_apache_smoke.sh` executes the real-world
  Apache smoke path through
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- `connectors/apache/harness/README.md` documents `make smoke-apache` and the
  selected-case path through `SMOKE_CASES`.
- `reports/testing/real-world-connector-validation.md` defines the
  `real-world-connector-path` proof model and states that response-body
  blocking is not verified.
- `reports/testing/generated/apache-runtime-results.generated.md` records the
  latest tracked force-all Apache runtime snapshot as failing, with
  non-promoted xfail, future, connector-gap, runtime-difference, and
  response-body cases.
- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
  records the current scaffold decisions for external tests, status vocabulary,
  Apache-specific YAML coverage, and RESPONSE_BODY evidence.

## Validation Commands Found

The repository exposes these relevant commands in `Makefile`:

```sh
make lint
make quick-check
make smoke-apache
make smoke-common
make smoke-all
make test-no-crs
make test-with-crs
make runtime-matrix-all
```

`make smoke-apache` is the connector-specific runtime target. A passing build or
static check alone is not documented as an Apache runtime pass.

`make test-no-crs` and `make test-with-crs` are CRS-variant targets and must be
reported separately. Current `/src` evidence:

- `make test-no-crs`: Apache PASS, 54 PASS, 0 FAIL, 0 BLOCKED.
- `make test-with-crs`: Apache FAIL, 54 PASS, 1 FAIL, 0 BLOCKED.
- With-CRS `crs_sqli_anomaly_block`: PASS, expected 403, actual 403.
- With-CRS failing case: `action_status_401_phase1_block`, expected 401,
  actual 403.

## Test Ownership

Executable YAML cases are owned by the framework module, not this connector
directory:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Local connector test folder `connectors/apache/tests`: removed. Executable
Apache connector tests are not maintained connector-locally.

The Apache-specific framework path was found, but only `README.md` was found
there during this verification. Apache-only YAML cases remain deferred until
case files and matching runtime evidence are present.

## Status Vocabulary

- `adapter-owned`: productive connector code lives in this connector tree with
  provenance and metadata.
- `runtime-smoke-verified`: only the named smoke case with command and result is
  verified.
- `partial`: structure or partial runtime evidence exists, but full validation
  is not proven.
- `not-verified`: insufficient runtime evidence.

Apache remains `partial`. Current common and No-CRS `/src` evidence is PASS for
the executed scope, but the current With-CRS target is FAIL and RESPONSE_BODY
blocking remains `not-verified`.

## Not Claimed

- No broad Apache regression-suite pass is claimed by this document.
- No response-body blocking pass is claimed.
- No runtime result is claimed unless a smoke command is actually run in the
  current environment and its result is recorded.
