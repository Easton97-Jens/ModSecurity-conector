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
- `make smoke-installed`
  - probes installed components and libmodsecurity presence
  - currently reports BLOCKED if installed-runtime harness wiring is not configured
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
