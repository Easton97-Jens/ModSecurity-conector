# CI

Status: connector integration only.

Generic framework logic lives in `modules/ModSecurity-test-Framework/ci`.
The connector repository keeps checks and generators that compile, validate, or
summarize connector-owned behavior:

- `check-common-helpers.sh`
- `check-adapter-helpers.sh`
- `check-adapter-metadata-drift.sh`
- `check-apache-directive-config.sh`
- `refresh-connector-reports.py`
- `generate-*-analysis.py`
- `generate-final-consistency-audit.py`

`check-apache-directive-config.sh` is a parse-only Apache check for connector
directives that need built Apache smoke artifacts. It renders a temporary
configuration under `BUILD_ROOT`, loads the adapter-owned Apache module, and
expects `httpd -t` to return `Syntax OK` for
`modsecurity_use_error_log on|off` and
`modsecurity_transaction_id static-test-id`.

Public Makefile targets such as `quick-check`, `generate-test-matrix`,
`runtime-matrix-all`, `smoke-apache`, `smoke-nginx`, and `smoke-all` delegate to
the framework module with `CONNECTOR_ROOT` set to this repository.

Generated reports under `reports/testing/generated/` are refreshed through
`make refresh-all-reports`, which calls the connector report generators and the
framework-owned queue/matrix generators. Generated reports should not be edited
manually.
