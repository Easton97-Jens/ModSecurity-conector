# NGINX Validation

Status: evidence-scoped

This document is the NGINX-specific validation counterpart to the generic
template document at `connectors/_template/docs/validation.md`.

## Repository Evidence

- `connectors/nginx/README.md` documents the adapter-owned NGINX source tree,
  module `config`, metadata, and harness.
- `connectors/nginx/harness/run_nginx_smoke.sh` executes the real-world NGINX
  smoke path through `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- `connectors/nginx/harness/README.md` documents `make smoke-nginx` and the
  selected-case path through `SMOKE_CASES`.
- `reports/testing/real-world-connector-validation.md` defines the
  `real-world-connector-path` proof model and states that response-body
  blocking is not verified.
- `reports/testing/generated/nginx-runtime-results.generated.md` records the
  latest tracked force-all NGINX runtime snapshot as failing, with
  non-promoted xfail, future, connector-gap, runtime-difference, and
  response-body cases.
- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
  records the current scaffold decisions for external tests, status vocabulary,
  NGINX-specific YAML coverage, the common-include build contract, and
  RESPONSE_BODY evidence.

## Validation Commands Found

The repository exposes these relevant commands in `Makefile`:

```sh
make lint
make quick-check
make smoke-nginx
make smoke-common
make smoke-all
make test-no-crs
make test-with-crs
make runtime-matrix-all
```

`make smoke-nginx` is the connector-specific runtime target. A passing build or
static check alone is not documented as an NGINX runtime pass.

`make test-no-crs` and `make test-with-crs` are CRS-variant targets and must be
reported separately. Current `/src` evidence:

- `make test-no-crs`: NGINX PASS, 60 PASS, 0 FAIL, 0 BLOCKED.
- `make test-with-crs`: NGINX FAIL, 60 PASS, 1 FAIL, 0 BLOCKED.
- With-CRS `crs_sqli_anomaly_block`: PASS, expected 403, actual 403.
- With-CRS failing case: `action_status_401_phase1_block`, expected 401,
  actual 403.

## Test Ownership

Executable YAML cases are owned by the framework module, not this connector
directory:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Local connector test folder `connectors/nginx/tests`: removed. Executable
NGINX connector tests are not maintained connector-locally.

The NGINX-specific framework path contains YAML files. Their existence is not a
runtime PASS claim; runtime claims still require an executed command and result.

## Current Build Contract

The accepted common-header include contract for the NGINX prepare flow is:

```text
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
```

`connectors/nginx/config` consumes that value, and the post-fix
`phase1_header_block` smoke passed with HTTP 403.

## Status Vocabulary

- `adapter-owned`: productive connector code lives in this connector tree with
  provenance and metadata.
- `runtime-smoke-verified`: only the named smoke case with command and result is
  verified.
- `partial`: structure or partial runtime evidence exists, but full validation
  is not proven.
- `not-verified`: insufficient runtime evidence.

NGINX remains `partial`. Current common, all-scope, and No-CRS `/src` evidence
is PASS for the executed scope, but the current With-CRS target is FAIL and
RESPONSE_BODY blocking remains `not-verified`.

## Not Claimed

- No broad NGINX regression-suite pass is claimed by this document.
- No response-body blocking pass is claimed.
- No runtime result is claimed unless a smoke command is actually run in the
  current environment and its result is recorded.
