# Fast Checks vs Full Smoke

## Purpose

Fast checks provide rapid feedback for Codex/developer iterations without pretending to be full connector validation.

## Targets

- `make quick-all`
  - orchestration target for fast checks
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

Use `make cloud-quick-check` for CI environments where runtime probes may be BLOCKED but framework checks must stay strict.

- Required/pass-fail: `setup-dev`, `lint`, `doctor-quick`, `quick-check`, Python compile, `git diff --check`.
- Blockable: `installed-readiness` and `quick-all` (`exit 77` is reported as BLOCKED, not framework FAIL).
- This does **not** replace `make smoke-all`; full smoke remains authoritative.

Workflow: `.github/workflows/cloud-quick-smoke.yml` installs explicit Ubuntu packages before running the cloud quick path.
