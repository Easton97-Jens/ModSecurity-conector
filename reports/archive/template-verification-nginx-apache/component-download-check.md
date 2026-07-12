> Status: Historical
> Superseded by: [../../current/six-connector-core-completion.md](../../current/six-connector-core-completion.md)
> Date: retained as a historical report during repository organization on 2026-07-12
> Evidence boundary: historical planning, assessment, or snapshot; not current canonical evidence.

# Component Download Check

**Language:** English | [Deutsch](component-download-check.de.md)

Status: reviewed

## Scope

This file records dependency preparation and runtime-component evidence used by
the Apache and NGINX connector verification.

## Repository-Local Connector Sources

- Apache connector source used by runtime builds:
  `connectors/apache`
- NGINX connector source used by runtime builds:
  `connectors/nginx`
- External Apache/NGINX connector repositories were not required for the
  documented `/src` smoke runs.

## Source Preparation Evidence

- `make fetch-deps` with `SOURCE_ROOT=/src` prepared
  `/src/ModSecurity_V3`.
- NGINX source build downloaded NGINX release `release-1.31.1` into the
  buildroot during the documented `/src` run.
- Apache source build prepared PCRE2, httpd, APR, APR-util, libmodsecurity,
  and `mod_security3.so` in the buildroot during the documented `/src` run.

## Current Runtime Commands

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS, NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS, 0 FAIL, 0 BLOCKED; NGINX 61 PASS, 0 FAIL, 0 BLOCKED. |

Evidence files:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/nginx.rc`

## CRS Preparation Evidence

The current With-CRS target used the repository-backed framework CRS flow:

- `modules/ModSecurity-test-Framework/ci/provisioning/fetch-crs.sh`
- `modules/ModSecurity-test-Framework/ci/provisioning/prepare-crs.sh`
- CRS pin in `modules/ModSecurity-test-Framework/ci/lib/common.sh`:
  `CRS_GIT_REF=v4.26.0`
- Observed CRS source path: `/src/coreruleset`
- Observed CRS runtime preamble:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

CRS case evidence:

- Apache `crs_sqli_anomaly_block`: PASS, expected 403, actual 403.
- NGINX `crs_sqli_anomaly_block`: PASS, expected 403, actual 403.

The overall With-CRS target is now PASS for the current `/src` executed scope.
`action_status_401_phase1_block` is expected 403 and actual 403 in With-CRS;
the base No-CRS expectation remains 401.

## NGINX Build Include Contract

Current accepted contract:

```text
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
```

`connectors/nginx/config` can consume this variable. The NGINX build logs after
the include fix show `common/include` in the generated compile path.

## NGINX Docroot Contract

Current accepted parent-side runtime contract:

```make
NGINX_HARNESS_PARENT ?= $(BUILD_ROOT)
export NGINX_HARNESS_PARENT
```

This keeps generated NGINX runtime docroots below the selected buildroot. In
this workspace `/tmp` is mode `700`, so a fallback docroot below `/tmp` is not
safe for the NGINX worker.

## Default Buildroot

The last documented plain `make smoke-common` without `/src` environment was
blocked because the default buildroot lacked:

```text
<local-state-root>/sources/ModSecurity_V3
```

That default-buildroot blocker is not a failure of the current `/src` smoke
evidence.

## Decision

Component preparation is sufficient for the documented `/src` No-CRS,
With-CRS, and common smoke evidence. CRS fetch/prepare ran for With-CRS and
the CRS SQLi case passed for both connectors. Full runtime verification and
RESPONSE_BODY blocking remain not verified.
