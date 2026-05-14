# libmodsecurity v3 API Smoke Test

Status: implemented build harness, blocked locally until libmodsecurity is
built.

This document describes a minimal connector-free probe for the public
libmodsecurity v3 C API.

## Purpose

The probe checks whether this repository can compile and run a small C program
against the local v3 checkout at `/root/conecter/ModSecurity_V3` and load a
simple SecRule through the public C API.

This is not a webserver connector test. It does not use Apache, NGINX, HAProxy,
Envoy, Lighttpd, or Traefik.

The canonical source and build harness live under:

```text
src/v3-api-smoke/
```

`tests/common/v3-api-smoke/` contains only a pointer to that source so the test
tree does not duplicate implementation logic.

## Primary Scenario

Name: `primary_args_phase2`

Rules:

```apache
SecRuleEngine On
SecRule ARGS:test "@streq attack" "id:1001,phase:2,deny,status:403"
```

Simulated request:

```text
GET /?test=attack HTTP/1.1
```

Expected result:

```text
primary_args_phase2: pass status=403
```

If this scenario does not produce a 403 intervention through the pure C API
path, the result must be documented as a primary failure. The implementation
must not infer an explanation without a confirmed source.

## Fallback Scenario

Name: `fallback_request_uri_phase1`

Rules:

```apache
SecRuleEngine On
SecRule REQUEST_URI "@contains test=attack" "id:1002,phase:1,deny,status:403"
```

The fallback is only a minimal proof that the public API can load rules and
produce an intervention for the simulated URI. It does not validate `ARGS:test`
handling.

If the fallback passes while the primary scenario fails, the script exits
non-zero. That result is `fallback pass`, not `pass`, and it must not be
documented as `ARGS:test` support. The expected marker is:

```text
fallback passed, primary failed
```

## Public API Calls

The probe uses these public libmodsecurity v3 C API calls:

- `msc_init`
- `msc_set_connector_info`
- `msc_create_rules_set`
- `msc_rules_add`
- `msc_new_transaction`
- `msc_process_connection`
- `msc_process_uri`
- `msc_process_request_headers`
- `msc_process_request_body`
- `msc_intervention`
- `msc_intervention_cleanup`
- `msc_transaction_cleanup`
- `msc_rules_cleanup`
- `msc_cleanup`

The call order follows the v3 examples and regression harness pattern observed
in `/root/conecter/ModSecurity_V3`.

## Build And Run

Default command:

```sh
sh ci/run-v3-api-smoke.sh
```

Direct Makefile command:

```sh
make -C src/v3-api-smoke run
```

Prerequisite check only:

```sh
sh ci/check-v3-api-smoke-prereqs.sh
```

Optional overrides:

```sh
MODSECURITY_V3_DIR=/root/conecter/ModSecurity_V3 sh ci/run-v3-api-smoke.sh
BUILD_DIR=/tmp/msconnector-smoke sh ci/run-v3-api-smoke.sh
```

The script and Makefile check for:

- `/root/conecter/ModSecurity_V3/headers/modsecurity/modsecurity.h`
- `/root/conecter/ModSecurity_V3/src/.libs/libmodsecurity.so`

The script and Makefile intentionally do not build
`/root/conecter/ModSecurity_V3`.

For automation, prefer the `ci/` shell scripts. They preserve blocked exit code
`77`. A direct GNU Make invocation prints `Error 77` for the blocked recipe, but
GNU Make itself exits with its own failure code.

If the v3 library is missing, build the v3 checkout separately using the
sequence documented by the v3 repository:

```sh
cd /root/conecter/ModSecurity_V3
git submodule update --init --recursive
./build.sh
./configure
make
```

## Observed Local Result

Observed on this workspace via `sh ci/check-v3-api-smoke-prereqs.sh`:

```text
v3_api_smoke: MODSECURITY_V3_DIR=/root/conecter/ModSecurity_V3
v3_api_smoke: v3 branch=v3/master
v3_api_smoke: v3 version=v3.0.15
v3_api_smoke: header present: /root/conecter/ModSecurity_V3/headers/modsecurity/modsecurity.h
v3_api_smoke: blocked missing library: /root/conecter/ModSecurity_V3/src/.libs/libmodsecurity.so
v3_api_smoke: not building ModSecurity_V3 from this script
```

Observed on this workspace via `sh ci/run-v3-api-smoke.sh`:

```text
v3_api_smoke: MODSECURITY_V3_DIR=/root/conecter/ModSecurity_V3
v3_api_smoke: v3 branch=v3/master
v3_api_smoke: v3 version=v3.0.15
v3_api_smoke: header present: /root/conecter/ModSecurity_V3/headers/modsecurity/modsecurity.h
v3_api_smoke: blocked missing library: /root/conecter/ModSecurity_V3/src/.libs/libmodsecurity.so
v3_api_smoke: not building ModSecurity_V3 from this script
```

Interpretation:

- `blocked`: the local v3 checkout has the public header but no built
  `src/.libs/libmodsecurity.so`.
- `implemented`: the connector-free smoke probe source, Makefile, runner, and
  prerequisite checker exist in this repository.
- `pass`: the primary `ARGS:test` scenario produced status `403`.
- `fallback pass`: only the fallback `REQUEST_URI` scenario produced status
  `403`; this is only a minimal API proof.
- `fail`: the probe built and ran, but the primary `ARGS:test` result was not
  status `403`.
- `unknown`: the `primary_args_phase2` runtime result has not been observed
  because the local v3 library is not built.

## TODO

- Run `sh ci/run-v3-api-smoke.sh` after `/root/conecter/ModSecurity_V3` has
  been built.
- If `primary_args_phase2` fails and `fallback_request_uri_phase1` passes,
  document the exact output without claiming `ARGS:test` support.
- If any public C API call sequence needs adjustment, cite the v3 header,
  example, or regression harness source before changing the probe.
