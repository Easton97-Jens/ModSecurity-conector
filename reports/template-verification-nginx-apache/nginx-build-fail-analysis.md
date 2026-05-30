# NGINX Build Fail Analysis

Status: build fix verified; current `/src` runtime smokes PASS for executed scope

## Original Build Failure

The earlier NGINX build failed during `nginx-make` because this include was not
found:

```text
msconnector/rule_load_stats.h
```

The header exists in the parent repository:

```text
common/include/msconnector/rule_load_stats.h
```

The failing compiler path did not include `common/include`.

## Minimal Build Contract

Accepted current build contract:

```text
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
```

`connectors/nginx/config` supports this variable. The NGINX prepare/configure
flow passes it so the generated NGINX build can include
`common/include/msconnector/rule_load_stats.h`.

## Verification

Post-fix build/runtime commands:

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | FAIL | NGINX built and ran; NGINX result was 60 PASS, 1 FAIL, 0 BLOCKED. Failing case: `action_status_401_phase1_block`, expected 401 and actual 403. |

Current evidence files:

- `/src/ModSecurity-conector-build/logs/nginx/nginx-make.log`
- `/src/ModSecurity-conector-build/nginx-build/nginx-src/objs/Makefile`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`

The With-CRS failure is a runtime expectation failure after a successful NGINX
build. It is not the earlier include-path build failure.

## Relationship To Docroot Blocker

The include-path failure and the later 11 BLOCKED runtime rows were separate
issues:

- Include-path issue: NGINX build could not find
  `msconnector/rule_load_stats.h`.
- Runtime docroot issue: NGINX worker could not traverse a generated docroot
  parent when the harness work root fell back to `/tmp` in this environment.

The docroot blocker is documented in
`nginx-docroot-permission-analysis.md`.

## RESPONSE_BODY

RESPONSE_BODY blocking remains not verified. `response_body_pass` is
pass-through evidence only.

## Decision

The NGINX build failure is fixed for the documented `/src` source-build flow.
NGINX No-CRS passed in the current run. NGINX With-CRS built and ran but has
one FAIL. NGINX still remains `partial` because full runtime matrix evidence,
With-CRS full-target PASS, and RESPONSE_BODY blocking are not verified.
