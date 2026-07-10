# lighttpd Harness

Status: native config-load, start, and minimal runtime-smoke paths

The connector owns four native harness scripts:

- `prepare_native_smoke.sh` writes temporary Common and lighttpd configs below
  `BUILD_ROOT` with both body modes disabled;
- `check_lighttpd_config.sh` loads the real module through real `lighttpd -tt`;
- `start_lighttpd_smoke.sh` starts, checks, and stops lighttpd without requests;
- `runtime_lighttpd_smoke.sh` separately sends an allowed and a blocked request.

The corresponding targets are:

```sh
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd
```

The runtime smoke uses `OPTIONS *` so lighttpd core can return the allowed 200
without loading unrelated stock modules from the temporary connector module
directory. Adding `X-Modsec-Smoke: block` must return 403 from rule `1000001`.
The script also verifies the narrow Common JSONL decision metadata.

`start-smoke-lighttpd` deliberately sends zero requests and reports that count.
The bridge self-test is separate and is never used as host evidence.

`run_lighttpd_smoke.sh` remains the entrypoint for the older framework-owned
`sidecar_proxy` path. It is an alternative path and its evidence must not be
mixed with the native-module evidence.

Request/response body evidence, CRS, production hardening, security
verification, and full-matrix evidence are not provided by this harness.
