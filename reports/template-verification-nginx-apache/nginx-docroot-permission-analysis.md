# NGINX Docroot Permission Analysis

Status: parent-side runtime environment fixed and verified

Date/time: 2026-05-30 15:49:59 UTC

## Scope

This analysis covers the NGINX runtime blocker that previously produced
BLOCKED rows after the NGINX build succeeded. It does not change connector
adapter code, YAML testcases, harness scripts, or the
`modules/ModSecurity-test-Framework` submodule.

## Evidence Reviewed

- `Makefile`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `connectors/nginx/harness/nginx_smoke.conf`
- `modules/ModSecurity-test-Framework/ci/run-nginx-smoke.sh`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/logs/`

## Docroot Generation Path

1. `modules/ModSecurity-test-Framework/ci/run-nginx-smoke.sh` derives
   `NGINX_HARNESS_WORK_ROOT` from `NGINX_HARNESS_PARENT` when no explicit
   work root is set.
2. `connectors/nginx/harness/run_nginx_smoke.sh` receives that work root and
   sets `RUNTIME_BASE` below it.
3. The connector harness creates per-case runtime directories and sets
   `DOCROOT="$RUNTIME_ROOT/htdocs"`.
4. The harness calls `case_cli.py materialize --docroot "$DOCROOT"`.
5. `runner_core.py` writes `index.html` and `__modsec_smoke_ready` into the
   supplied docroot.
6. `connectors/nginx/harness/nginx_smoke.conf` uses `root "@@DOCROOT@@"` and
   `index index.html`.

## Permission Cause

The environment has `/tmp` as:

```text
drwx------ root root /tmp
```

Both the submodule runner and the connector harness can fall back to `/tmp`
for root-owned runs when `NGINX_HARNESS_PARENT` is unset. The NGINX worker user
hint in the connector harness is `nobody`. A docroot below a non-traversable
`/tmp` can therefore be created and owned correctly below the work root while
still remaining inaccessible to the worker because the parent `/tmp` directory
is mode `700`.

The current successful run used:

```text
NGINX_HARNESS_WORK_ROOT=/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0
```

The relevant path is traversable:

```text
drwxr-xr-x root   root    /
drwxr-xr-x root   root    src
drwxr-xr-x root   root    ModSecurity-conector-build
drwxr-xr-x nobody nogroup ModSecurity-conector-nginx-runtime-0
drwxr-xr-x nobody nogroup runtime
drwxr-xr-x nobody nogroup action_allow_phase1_pass
drwxr-xr-x nobody nogroup htdocs
-rw-r--r-- nobody nogroup index.html
```

## Parent-Side Fix

The parent `Makefile` contains the safe default:

```make
NGINX_HARNESS_PARENT ?= $(BUILD_ROOT)
export NGINX_HARNESS_PARENT
```

That keeps the submodule contract intact while forcing NGINX runtime work into
the selected build root instead of the process default `/tmp`.

No submodule file was changed for this analysis. No connector source, harness
script, YAML testcase, or local connector `tests` directory was changed or
created.

## Verification

Commands executed:

```text
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
```

Results:

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | `nginx-summary.json`: 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | `connector-summary.json`: Apache 54 PASS, NGINX 54 PASS |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | `results/no-crs/nginx-summary.json`: 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | `results/with-crs/nginx-summary.json`: 61 PASS, 0 FAIL, 0 BLOCKED |

Current summary files:

- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`

Current RC files:

- `/src/ModSecurity-conector-build/results/apache.rc`: `0`
- `/src/ModSecurity-conector-build/results/nginx.rc`: `0`

## Decision

The 11 prior NGINX BLOCKED rows are classified as an environment/docroot
permission blocker. The current `/src` runs no longer have NGINX BLOCKED rows.
The current With-CRS target is PASS for the executed `/src` scope.

NGINX still remains `partial` because full runtime promotion requires the
minimum matrix and RESPONSE_BODY blocking evidence. `response_body_pass` is
pass-through evidence only and does not verify response-body blocking.
