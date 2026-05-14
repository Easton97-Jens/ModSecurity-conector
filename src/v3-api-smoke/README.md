# libmodsecurity v3 API Smoke Probe

Status: implemented build harness, blocked locally until libmodsecurity is
built.

This directory contains a connector-free C smoke probe for the public
libmodsecurity v3 C API. It does not contain Apache, NGINX, HAProxy, Envoy,
Lighttpd, or Traefik integration.

## Build

Default build:

```sh
make -C src/v3-api-smoke
```

Run:

```sh
make -C src/v3-api-smoke run
```

Optional overrides:

```sh
make -C src/v3-api-smoke MODSECURITY_V3_DIR=/root/conecter/ModSecurity_V3
make -C src/v3-api-smoke BUILD_DIR=/tmp/msconnector-smoke
```

The Makefile checks for:

- `$MODSECURITY_V3_DIR/headers/modsecurity/modsecurity.h`
- `$MODSECURITY_V3_DIR/src/.libs/libmodsecurity.so`

It intentionally does not run `build.sh`, `configure`, or `make` inside
`MODSECURITY_V3_DIR`.

For automation that needs the blocked exit code `77`, use:

```sh
sh ci/check-v3-api-smoke-prereqs.sh
sh ci/run-v3-api-smoke.sh
```

GNU Make reports failed recipe commands as a make failure; it will print
`Error 77` from the recipe, but the wrapper scripts preserve exit code `77`.

## Result Meanings

- `implemented`: this source file and Makefile exist.
- `blocked`: the local v3 checkout is missing headers or
  `src/.libs/libmodsecurity.so`.
- `pass`: `primary_args_phase2` produced intervention status `403`.
- `fallback pass`: `fallback_request_uri_phase1` produced status `403` after
  the primary ARGS test failed; this is only a minimal API proof.
- `fail`: the probe built and ran, but the expected primary result was not
  observed.

The fallback must not be documented as ARGS support.
