# Compatibility

Status: scaffolded

## Version Position

The scaffold targets libmodsecurity v3 public APIs. v2 artifacts are not used as
architecture for new connectors.

## Current Compatibility Matrix

| Area | Status | Notes |
| --- | --- | --- |
| Common headers | implemented | Connector-neutral C-compatible data shapes only |
| libmodsecurity v3 API mapping | planned | Public API sequence documented, not wrapped |
| Apache connector | scaffolded | Local source-built PoC observed expected HTTP behavior for all current shared minimal cases |
| NGINX connector | scaffolded | Local source-built PoC observed expected HTTP behavior for all current shared minimal cases |
| Apache real-world connector path | implemented | Smoke summaries record source-built httpd, `mod_security3.so`, libmodsecurity, and verified variables |
| NGINX real-world connector path | implemented | Smoke summaries record source-built NGINX, dynamic module, libmodsecurity, and verified variables |
| HAProxy connector | unknown | SPOE/Lua/native options documented, implementation undecided |
| Envoy connector | unknown | HTTP filter/ext_authz/Wasm options documented, implementation undecided |
| Lighttpd connector | unknown | Native plugin and mod_magnet options documented, implementation undecided |
| Traefik connector | unknown | Yaegi/Wasm plugin options documented, implementation undecided |
| v2 regression reuse | planned | Only portable rule/engine semantics may enter `tests/common/` |
| v2-derived common imports | implemented | Operator and transformation cases including `@streq`, `@contains`, `@beginsWith`, `@endsWith`, `@pm`, `@containsWord`, `t:lowercase`, `t:trim`, `t:urlDecode`, and `t:htmlEntityDecode` pass locally on Apache and NGINX |
| v3-derived common imports | implemented | Multipart FILES, XML body processor, operator, transformation, action, cookie/header-name/ARGS_NAMES, and stable audit cases pass locally on Apache and NGINX |
| Source-derived Apache/NGINX test import | implemented | Imported YAML cases are derived, not copied; origin and portability are documented |

## Capability Rule

Tests and connector docs must name required capabilities. If a behavior depends
on hook timing, buffering, streaming, log artifacts, reload semantics, or server
configuration, it is connector-specific unless proven portable.

## Shared Minimal Cases

The files under `tests/common/cases/minimal/` are portable rule/request models.
They are not proof that a connector supports the behavior until that
connector's runtime harness observes the expected HTTP response.

Observed locally on 2026-05-15 with `BUILD_ROOT=/src/ModSecurity-conector-build`:

| Case | Capability area | Apache | NGINX |
| --- | --- | --- | --- |
| `audit_log_phase1_block.yaml` | query args, phase 1, audit log | pass, HTTP 403 plus audit fields | pass, HTTP 403 plus audit fields |
| `phase1_header_block.yaml` | request headers, phase 1 | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_block.yaml` | query args, phase 2 | pass, HTTP 403 | pass, HTTP 403 |
| `phase2_args_pass.yaml` | query args, phase 2, pass-through | pass, HTTP 200 plus origin body | pass, HTTP 200 plus origin body |
| `request_body_json_block.yaml` | request body, JSON content type, raw body match | pass, HTTP 403 | pass, HTTP 403 |
| `request_body_urlencoded_block.yaml` | form body, `ARGS_POST` | pass, HTTP 403 | pass, HTTP 403 |
| `response_header_basic.yaml` | response headers, phase 3 | pass, HTTP 403 | pass, HTTP 403 |

This proves only these PoC behaviors in this workspace, not full connector
compatibility, CRS support, multipart handling, streaming behavior, HTTP/2, or
complete response-body behavior.

## Imported Case Scopes

| Scope | Location | Compatibility meaning |
| --- | --- | --- |
| common minimal | `tests/common/cases/minimal/` | Already proven locally for both PoCs before the import step |
| common imported | `tests/common/cases/imported/` | Portable candidates derived from Apache/NGINX tests; compatibility is claimed only after both connector smokes pass |
| v2 imported | `tests/common/cases/v2-imported/` | Portable v2 semantics candidates adapted to HTTP behavior and proven on both connector PoCs |
| v3 imported | `tests/common/cases/v3-imported/` | Portable v3 regression candidates adapted to HTTP behavior and proven on both connector PoCs |
| Apache imported | `tests/apache/cases/imported/` | Apache-only until a common equivalent is proven |
| NGINX imported | `tests/nginx/cases/imported/` | NGINX-only until a common equivalent is proven |

Mapped-only categories include HTTP/2, proxy, multipart parser edge cases,
response-body blocking, external-file operators, debug logs, and connector
config inheritance.

Observed locally on 2026-05-15, the current imported common cases all passed on
Apache and NGINX through `make smoke-all`; the NGINX-specific imported cases
passed only on NGINX and remain `portable: false`. Phase 10 added three
NGINX-only PR #377 phase-4 log/pass-through probes after 3/3 targeted NGINX
PASS runs; those are connector-specific evidence, not common compatibility.

## Body And Filter Compatibility

| Case or category | Apache | NGINX | Status |
| --- | --- | --- | --- |
| `json_request_body_block.yaml` | pass, HTTP 403 | pass, HTTP 403 | fully-imported-common |
| `multipart_basic_block.yaml` | pass, HTTP 403 | pass, HTTP 403 | fully-imported-common |
| `response_body_pass.yaml` | pass, HTTP 200 | pass, HTTP 200 | fully-imported-common |
| `response_body_basic_block` | fail, HTTP 200 | fail, HTTP 200 | xfail/mapped-only |
| PR #377 minimal/safe phase-4 log-only probes | n/a | pass, HTTP 200 plus phase4 log evidence | NGINX connector-specific |
| PR #377 content-type out-of-scope phase-4 probe | n/a | pass, HTTP 200 plus phase4 log evidence | NGINX connector-specific |

The response-body block row is intentionally not an active smoke. The NGINX
reference test marks the behavior TODO, and ModSecurity-nginx PR #377 source
changes are treated as source-level evidence only. A local three-repeat probe
did not produce stable HTTP 403 on either connector, so this repository
documents the evidence without claiming connector parity.

## V2/V3-Derived Compatibility

Observed locally on 2026-05-15 with `BUILD_ROOT=/src/ModSecurity-conector-build`:

| Case group | Apache | NGINX | Status |
| --- | --- | --- | --- |
| V2 operator semantics (`@streq`, `@contains`, `@beginsWith`, `@endsWith`, `@pm`, `@containsWord`) | pass, HTTP 403 | pass, HTTP 403 | fully-imported-common |
| V2 transformation semantics (`t:lowercase`, `t:trim`, `t:urlDecode`, `t:htmlEntityDecode`) | pass, HTTP 403 | pass, HTTP 403 | fully-imported-common |
| V3 multipart FILES variables | pass, HTTP 403 | pass, HTTP 403 | fully-imported-common |
| V3 XML body processor basic case | pass, HTTP 403 | pass, HTTP 403 | fully-imported-common |
| V3 `@rx`, trim, and `SecAction` basics | pass, HTTP 403 | pass, HTTP 403 | fully-imported-common |
| V3 `@pm`, cookies, header names, ARGS_NAMES, and serial audit basics | pass | pass | fully-imported-common |
| V3 `nolog,pass` audit absence (`issue-2196`) | pass locally, empty audit log | pass locally, empty audit log | xfail because GitHub Actions observed a non-empty audit log |

The active cases prove only the minimal YAML scenarios. V2 Perl harness
internals, v3 API-only cases, XML schema/DTD validation, malformed multipart,
NUL/binary transformation branches, streaming, HTTP/2, and optional-library
operators remain mapped until dedicated support is added.

## Real-World Connector Path

`real-world-connector-path` is the compatibility proof mode for Apache and
NGINX:

```text
HTTP client -> server process -> connector module -> libmodsecurity -> rule variables -> HTTP response
```

The direct v3 API smoke remains separate and is not connector proof. Connector
summary JSON records `connector_path`, `validation_mode`, `server_binary`,
`module`, `libmodsecurity`, and `verified_variables`. A variable appears there
only if at least one active passing case exercised it through the real server
runtime.

Current active passing cases verify `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`,
`REQUEST_HEADERS`, `REQUEST_URI`, `REQUEST_BODY`, `FILES`, `XML`, `AUDIT_LOG`,
and `RESPONSE_HEADERS` through both Apache and NGINX in this workspace.
`RESPONSE_BODY` remains mapped/xfail until an active response-body
variable/blocking case passes on both connectors.

`v3_action_nolog_pass_no_audit` is also classified as xfail/mapped for now:
local runs in this workspace produced HTTP 200 and empty audit logs, but the
current GitHub Actions run reported `expected audit log to be absent or empty`.
It is not counted as a stable common PASS until local Apache, local NGINX, and
GitHub Actions agree.

## Reproducible Local Setup (Smoke + Lint)

The smoke/lint tooling has explicit prerequisites and reports missing runtime inputs as **BLOCKED**.

### Python dependencies

Install dev dependencies before running `make lint`:

```bash
python3 -m pip install -r requirements-dev.txt
```

Currently required for lint helpers:

- `PyYAML>=6,<7` (used by `ci/check-workflow-yaml.py`)

If missing, lint prints a clear blocked message and installation hint instead of a Python traceback.


### One-command dev bootstrap

Create an isolated virtualenv and install dev deps:

```bash
make setup-dev
# make now auto-prefers .venv/bin/python when present
source .venv/bin/activate
```

Equivalent target names:

- `make install-dev-deps`
- `make setup-dev`

### Environment doctor

Check Python deps and ModSecurity v3 path detection:

```bash
make doctor
```

The doctor tries to auto-detect `MODSECURITY_V3_SOURCE_DIR` in this order:

1. Explicit `MODSECURITY_V3_SOURCE_DIR` (if it exists)
2. `../ModSecurity_V3` relative to repo root
3. `../../ModSecurity_V3` relative to repo root
4. `.deps/ModSecurity_V3` inside this repo
5. `/root/conecter/ModSecurity_V3`

If none exist, doctor exits BLOCKED and prints the exact export command needed.


### Optional GitHub runtime fetch

To bootstrap real external runtime prerequisites explicitly:

```bash
make fetch-deps
```

This uses `ci/fetch-smoke-sources.sh` and real public upstream repositories (see `docs/testing/bootstrap.md`).
No network fetch is triggered automatically by `make setup-dev`, `make lint`, `make doctor`, or `make smoke-all`.

If you only want to run dependency diagnostics first:

```bash
make doctor
```

### Runtime prerequisites for connector smokes

`make smoke-all` requires a ModSecurity v3 source tree path. Default:

- `MODSECURITY_V3_SOURCE_DIR=/root/conecter/ModSecurity_V3`

Override in portable environments:

```bash
export MODSECURITY_V3_SOURCE_DIR=/absolute/path/to/ModSecurity_V3
export BUILD_ROOT=/absolute/path/for/build-artifacts
make smoke-all
```

If prerequisites are missing, smoke scripts now emit explicit blocked guidance that includes:

- missing prerequisite path
- affected env var name
- remediation command/env hint
- explicit statement that result is **BLOCKED**, not **FAIL**

### Status meaning

- **PASS**: expected behavior observed through the real connector path.
- **FAIL**: harness ran and observed unexpected behavior or execution error.
- **BLOCKED**: prerequisites (dependencies, source paths, build/runtime requirements) are missing, so execution could not start reliably.


### Recommended fresh-environment flow

```bash
make setup-dev
make lint
make fetch-deps
make doctor
make smoke-all
```

Use a single consistent `BUILD_ROOT` across `fetch-deps`, `doctor`, and `smoke-all`.


See also: `docs/testing/fast-checks.md` for quick/cached/full check boundaries.


Quick CI/developer checks can use `make doctor-quick` and `make quick-all`; these are not full-smoke replacements and may return BLOCKED when runtime prerequisites are absent.

## Incremental Coverage Note (2026-05-19)

Added source-derived negative/pass-through common cases for:

- `REQUEST_COOKIES_NAMES` (`v3_request_cookies_names_pass_no_match`)
- `ARGS_NAMES` (`v3_args_names_get_pass_no_match`)
- `REQUEST_URI` with `t:urlDecode` no-match branch (`v2_transformation_url_decode_pass_no_match`)

These additions improve matrix/documented coverage but are not claimed as new stable common PASS evidence until full runtime smoke (`make smoke-all`) runs with all prerequisites.


## Installed runtime detection (non-authoritative)

`make doctor` and `make smoke-installed` / `make installed-readiness` now report installed-component readiness using alternative binary names and explicit ModSecurity detection.

Supported detection aliases:

- Apache: `apache2` / `httpd` / `apachectl`
- APXS: `apxs` / `apxs2`
- NGINX: `nginx`
- ModSecurity: `pkg-config` (`modsecurity` or `libmodsecurity`) or filesystem evidence (`libmodsecurity.so*` plus `modsecurity/modsecurity.h`)

Supported override variables:

- `APACHE_BIN`, `APXS_BIN`, `NGINX_BIN`
- `MODSECURITY_PKG_CONFIG`, `MODSECURITY_LIB_DIR`, `MODSECURITY_INCLUDE_DIR`

This installed-path readiness is informative for quick diagnostics. Full compatibility evidence remains the source-build full-smoke path (`make smoke-all`).


## Cloud reproducibility path

For Codex Cloud / GitHub Actions, `.github/workflows/cloud-quick-smoke.yml` installs required Ubuntu packages explicitly and runs `make cloud-quick-check`.

This path distinguishes:

- Framework correctness failures (red): lint/schema/python/diff issues.
- Runtime readiness limitations (BLOCKED): installed/cached smoke probes without full runtime wiring or artifacts.

It does not replace the authoritative full source-build smoke (`make smoke-all`).

## Expanded pending compatibility coverage (2026-05-19)

Added a larger source-derived xfail/pending set for connector-gap, runtime-difference, and future-compatibility targets. This extends long-term compatibility tracking without changing current verified PASS semantics.

Notably, RESPONSE_BODY remains non-verified and is not promoted; response-body blocking evidence stays xfail/mapped-only until stable cross-connector HTTP 403 proof exists.
