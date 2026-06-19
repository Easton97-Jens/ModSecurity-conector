# Repository Guidelines

## Project Structure & Module Organization

This is a ModSecurity connector monorepo. Shared connector-neutral C/C++ interfaces live in `common/include/msconnector/`, with helpers in `common/src/`. Adapter-owned code is under `connectors/`: active Apache, NGINX, and HAProxy sources use `connectors/<name>/src/`, `harness/`, `docs/`, and metadata files. Future connector scaffolds live beside them. The reusable test framework is the submodule at `modules/ModSecurity-test-Framework`; generated evidence and matrices are under `reports/testing/generated/`. CI tooling lives in `ci/`, and sample server configs are in `examples/`.

## Build, Test, and Development Commands

- `git submodule update --init --recursive`: fetch the required test framework.
- `make setup-dev`: bootstrap Python tooling from the framework and print next steps.
- `make lint`: run shell/Python syntax checks, fixture validation, report governance, JSON/doc checks, and `git diff --check`.
- `make generate-test-matrix` / `make check-test-matrix`: refresh and verify generated coverage and runtime matrix docs.
- `make quick-check` or `make codex-check`: lightweight validation suitable before commits.
- `make smoke-apache`, `make smoke-nginx`, `make smoke-haproxy`, or `make smoke-all`: run connector runtime smokes. Use `make test-no-crs` and `make test-with-crs` for broader CRS variants.

## Coding Style & Naming Conventions

Match the local file style. Shared C helpers use 4-space indentation, `msconnector_*` symbols, and connector-neutral headers. Apache code uses `msc_*` names; NGINX code uses `ngx_http_modsecurity_*`; HAProxy code uses `haproxy_*` names. Keep `common/` free of connector-specific terms and server APIs. Shell scripts should be POSIX `sh` where existing scripts are, with `set -eu`; Python should prefer `pathlib` and structured parsing.

## Testing Guidelines

Tests and fixtures are primarily owned by `modules/ModSecurity-test-Framework/tests/`. Add connector behavior coverage there or in connector harnesses, not in ad hoc root test directories. When changing generated reports, run `make generate-test-matrix` and `make check-test-matrix`. For runtime behavior, record the exact command and connector/CRS/MRTS variant.

## Commit & Pull Request Guidelines

Recent commits use short, lowercase, imperative summaries such as `refresh verified matrix after fixture input fixes`; no Conventional Commit prefix is required. Keep commits focused and include generated evidence with the code that requires it. Pull requests should describe the affected connector or report area, list validation commands, link issues, and call out regenerated files under `reports/testing/generated/`.

## Security & Configuration Tips

Keep runtime and build artifacts outside the checkout; the Makefile defaults to `/var/tmp/ModSecurity-conector-verified`. Do not commit downloaded upstream source trees, secrets, local logs, or unreviewed generated artifacts. Preserve pinned upstream refs and license/origin metadata when touching connector imports.
