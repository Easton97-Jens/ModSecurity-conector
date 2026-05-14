# libmodsecurity v3 API Smoke Test

Status: blocked

This document describes a minimal connector-free probe for the public
libmodsecurity v3 C API.

## Purpose

The probe checks whether this repository can compile a small C program against
the local v3 checkout at `/root/conecter/ModSecurity_V3` and load a simple
SecRule through the public C API.

This is not a webserver connector test. It does not use Apache, NGINX, HAProxy,
Envoy, Lighttpd, or Traefik.

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
non-zero and prints:

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

Optional overrides:

```sh
MODSECURITY_V3_DIR=/root/conecter/ModSecurity_V3 sh ci/run-v3-api-smoke.sh
BUILD_DIR=/tmp/msconnector-smoke sh ci/run-v3-api-smoke.sh
```

The script checks for:

- `/root/conecter/ModSecurity_V3/headers/modsecurity/modsecurity.h`
- `/root/conecter/ModSecurity_V3/src/.libs/libmodsecurity.so`

The script intentionally does not build `/root/conecter/ModSecurity_V3`.

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

Observed on this workspace:

```text
v3_api_smoke: blocked missing library: /root/conecter/ModSecurity_V3/src/.libs/libmodsecurity.so
v3_api_smoke: not building ModSecurity_V3 from this script
```

Interpretation:

- `blocked`: the local v3 checkout has the public header but no built
  `src/.libs/libmodsecurity.so`.
- `implemented`: the connector-free smoke probe source and runner exist in this
  repository.
- `unknown`: the `primary_args_phase2` runtime result has not been observed
  because the local v3 library is not built.

## TODO

- Run `sh ci/run-v3-api-smoke.sh` after `/root/conecter/ModSecurity_V3` has
  been built.
- If `primary_args_phase2` fails and `fallback_request_uri_phase1` passes,
  document the exact output without claiming `ARGS:test` support.
- If any public C API call sequence needs adjustment, cite the v3 header,
  example, or regression harness source before changing the probe.

