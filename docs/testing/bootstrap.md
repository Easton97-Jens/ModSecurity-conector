# Runtime Bootstrap (Optional)

This project can optionally fetch real upstream smoke prerequisites from GitHub.

## Repositories used

- ModSecurity v3: `https://github.com/owasp-modsecurity/ModSecurity.git` (ref: `v3/master` by default)
- ModSecurity-apache: `https://github.com/owasp-modsecurity/ModSecurity-apache.git` (ref: `master`)
- ModSecurity-nginx: `https://github.com/owasp-modsecurity/ModSecurity-nginx.git` (ref: `master`)

## Commands

- Fetch all smoke dependencies:
  - `make fetch-deps`
- Fetch minimal Apache runtime prerequisite set (includes ModSecurity v3 + apache repo):
  - `make fetch-modsecurity-v3`

## Behavior and safety

- Fetching is **explicit only** (manual command invocation).
- Existing repositories are **not overwritten**; existing git clones are reused.
- If `git` is missing or network is blocked, command exits BLOCKED/non-zero with clear output.
- No fake runtime artifacts are created.

## Paths

Default fetch root is under build temp:

- `SOURCE_ROOT=$BUILD_ROOT/sources`

You can override destination paths with:

- `MODSECURITY_V3_SOURCE_DIR`
- `MODSECURITY_APACHE_SOURCE_DIR`
- `MODSECURITY_NGINX_SOURCE_DIR`

These destination paths must be absolute and under `SOURCE_ROOT` to avoid destructive behavior.


## BUILD_ROOT consistency

`make fetch-deps`, `make doctor`, and `make smoke-all` are intended to use the same `BUILD_ROOT` (default `/src/ModSecurity-conector-build`).
Fetched sources live under `BUILD_ROOT/sources`.
If you override `BUILD_ROOT`, use the same value for all commands in the flow.

Example:

```bash
BUILD_ROOT=/tmp/modsec-build make fetch-deps
BUILD_ROOT=/tmp/modsec-build make doctor
BUILD_ROOT=/tmp/modsec-build make smoke-all
```


## Fast and full targets

- Fast framework checks: `make quick-check`
- Cached smoke: `make smoke-cached`
- Installed runtime probe: `make smoke-installed` / `make installed-readiness`
- Full authoritative connector smoke: `make smoke-all`

Use `REFRESH=1 make smoke-all` to force clean rebuild when cache/build trees are stale.


## Quick orchestration

Use `make quick-all` for a fast, honest framework/smoke-basis run.
It never triggers full source rebuilds by itself.
If runtime artifacts are missing it reports BLOCKED, not PASS.


## Cloud quick smoke workflow

GitHub Actions workflow `.github/workflows/cloud-quick-smoke.yml` provides a reproducible cloud path:

1. Install explicit Ubuntu packages (build toolchain + Apache + NGINX + libmodsecurity + JSON libs + AFL++ + parser deps).
2. Detect Lua dev package dynamically (`liblua5.4-dev`, `liblua5.3-dev`, `liblua5.2-dev`, `liblua5.1-0-dev`, fallback `liblua-dev`).
3. Run `make cloud-quick-check`.

This workflow is intentionally quick/framework oriented and keeps runtime BLOCKED outcomes honest; it does not claim full connector compatibility.
