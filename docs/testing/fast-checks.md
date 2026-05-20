# Fast Checks vs Full Smoke

## Purpose

Fast checks provide rapid feedback for Codex/developer iterations without pretending to be full connector validation.

## Targets

- `make quick-all`
  - local-preferred orchestration target for fast checks
  - combines lint, doctor-quick, quick-check, smoke-cached, smoke-installed, py_compile, diff-check
  - returns QUICK PASS / QUICK BLOCKED / QUICK FAIL
- `make quick-check` / `make codex-check`
  - runs lint, py_compile, and diff checks
  - does **not** run Apache/NGINX full smoke
- `make smoke-cached`
  - runs smoke using existing cached artifacts
  - exits BLOCKED when cache artifacts are missing
- `make smoke-installed` / `make installed-readiness`
  - probes installed components and libmodsecurity presence
  - currently acts as installed readiness probe; returns BLOCKED when execution wiring for true installed runtime smoke is not available
- `make smoke-all`
  - full source-build smoke path (authoritative)

## Honesty rules

- BLOCKED is not PASS.
- quick/cached checks never replace full smoke for release compatibility evidence.
- no fake green status when prerequisites are missing.

## Recommended flow

```bash
make setup-dev
make quick-all
# if QUICK BLOCKED due to runtime prerequisites:
make fetch-deps
make smoke-all
```


## Installed smoke detection

`make smoke-installed` / `make installed-readiness` is a **detection/readiness** probe for already-installed system components; it is not a replacement for `make smoke-all`.

Recognized binary names:

- Apache runtime: `apache2`, `httpd`, `apachectl`
- APXS: `apxs`, `apxs2`
- NGINX runtime: `nginx`

Recognized ModSecurity signals:

- `pkg-config` package: `modsecurity` or `libmodsecurity`
- shared libraries: `libmodsecurity.so` / `libmodsecurity.so.3`
- header: `modsecurity/modsecurity.h`

Optional override environment variables:

- `APACHE_BIN`
- `APXS_BIN`
- `NGINX_BIN`
- `MODSECURITY_PKG_CONFIG`
- `MODSECURITY_LIB_DIR`
- `MODSECURITY_INCLUDE_DIR`

Readiness semantics:

- `READY`: component set is detected.
- `PARTIAL`: only one connector path is detectable.
- `BLOCKED`: required pieces are missing.

Even with `READY`, `smoke-installed` remains non-authoritative until installed-runtime execution wiring exists; `make smoke-all` stays authoritative.


## Cloud/GitHub Actions quick path

Use `make cloud-quick-check` for GitHub/Codex CI environments where checks must
stay lightweight and deterministic.

- Required/pass-fail: `setup-dev`, `lint`, `generate-test-matrix`,
  `check-test-matrix`, `quick-check`, Python compile, `git diff --check`.
- Runtime probes are intentionally excluded: no `quick-all`, no
  `smoke-cached`, no `installed-readiness`, and no full connector smoke.
- This does **not** replace `make smoke-all`; full runtime validation remains
  local and authoritative.

Workflow: `.github/workflows/quick-framework-check.yml` runs the lightweight
framework/generator path on `push` and `pull_request`.
