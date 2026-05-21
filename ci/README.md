# CI

Status: connector integration only.

Generic framework logic lives in `modules/ModSecurity-test-Framework/ci`.
The connector repository keeps only checks that compile or validate
connector-owned C helpers and adapter metadata:

- `check-common-helpers.sh`
- `check-adapter-helpers.sh`
- `check-adapter-metadata-drift.sh`

Public Makefile targets such as `quick-check`, `generate-test-matrix`,
`runtime-matrix-all`, `smoke-apache`, `smoke-nginx`, and `smoke-all` delegate to
the framework module with `CONNECTOR_ROOT` set to this repository.
