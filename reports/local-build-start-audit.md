# Local Build and Start Audit

**Language:** English | [Deutsch](local-build-start-audit.de.md)

Generated: 2026-07-06
Updated: 2026-07-06

This audit only records compile evidence, link evidence, config-load evidence,
and minimal process-start evidence. It did not send HTTP requests, did not run
CRS cases, did not run a full matrix, did not inspect response bodies, and does
not claim live traffic or security behavior.

Evidence root: `/var/tmp/ModSecurity-conector-verified/build/local-build-start`

## Framework Provisioning

| Dependency | Local source | Path | Result |
|---|---|---|---|
| Apache/APXS | Framework `ci/common.sh` component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/apxs` | PASS |
| Apache httpd | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/httpd` | PASS |
| Apache module | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/build/output/apache/mod_security3.so` | PASS |
| NGINX headers/source | Framework `ci/common.sh` component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/3a61dba1872aec9a36f06424d1db0c0dac957413f857a96b2950f39d0a341e1d/build/nginx-src` | PASS |
| NGINX binary/module | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/3a61dba1872aec9a36f06424d1db0c0dac957413f857a96b2950f39d0a341e1d/nginx` | PASS |
| HAProxy headers/source | Framework `ci/common.sh` component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/sources/haproxy/haproxy-3.2.19` | PASS |
| HAProxy binary | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/haproxy/de600fcd33bfda9614b0753e2e10a318b9719ba03c3acbe0838e25b9fb862658/haproxy-runtime/haproxy/sbin/haproxy` | PASS |
| libmodsecurity headers | Framework `ci/common.sh` component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/include` | PASS |
| libmodsecurity library | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/lib` | PASS |

## Build And Start Matrix

| Component | Build/link | Config load | Start smoke | Evidence | Notes |
|---|---|---|---|---|---|
| Common SDK | PASS | n/a | n/a | `logs/common-checks.log` | `check-common-helpers`, SDK contract, adapter contract, and directive parity only |
| Apache | PASS | PASS | PASS | `logs/apache-compile-checks.log`; `apache/configtest.log`; `apache/start-summary.txt` | Loaded `mod_security3.so` with `modsecurity off`; no requests sent |
| NGINX | PASS | PASS | PASS | `logs/nginx-compile-checks.log`; `nginx/configtest.log`; `nginx/start-summary.txt` | Loaded `ngx_http_modsecurity_module.so` with `modsecurity off`; no requests sent |
| HAProxy | PASS | PASS | PASS | `logs/haproxy-compile-checks.log`; `logs/haproxy-build-link.log`; `haproxy-start/start-summary.txt` | Minimal HAProxy process start only; no traffic sent |
| HAProxy SPOA runtime binary | PASS | n/a | PASS | `logs/haproxy-build-link.log`; `haproxy-spoa-start/start-summary.txt`; `haproxy-spoa-start/spoa.log` | Binary entered `--serve` listen mode, wrote ready/PID files, then stopped; no SPOP client connected |
| Envoy starter | PASS | NOT PRESENT | NOT PRESENT | `logs/envoy-build-starter.log` | Starter binary created; no non-test server/config start mode is present; status remains `not_verified` / `connector-gap` |
| Traefik starter | PASS | NOT PRESENT | NOT PRESENT | `logs/traefik-build-starter.log` | Starter and decision-service binaries created; no non-test server/config start mode is present; status remains `not_verified` / `connector-gap` |
| lighttpd starter | PASS | NOT PRESENT | NOT PRESENT | `logs/lighttpd-build-starter.log`; `logs/lighttpd-bridge-compile-only.log` | Build starter created; bridge starter was rebuilt compile-only because the Make target invokes an embedded self-test |
| Remaining connector helpers | PASS | n/a | n/a | `logs/remaining-connectors-compile-checks.log` | C17/C23/future-C and Common adoption checks only |

## Start Evidence

| Component | Config result | Process evidence | Stop result |
|---|---|---|---|
| Apache | `Syntax OK` in `apache/configtest.log` | `background_pid=529328`, `pid_file=529328` in `apache/start-summary.txt` | `stopped=yes` |
| NGINX | `syntax is ok` and `test is successful` in `nginx/configtest.log` | `background_pid=530458`, `pid_file=530458` in `nginx/start-summary.txt` | `stopped=yes` |
| HAProxy | `haproxy -c -f` returned 0; log file is empty | `pid_file=531716` in `haproxy-start/start-summary.txt` | `stopped=yes` |
| HAProxy SPOA runtime binary | n/a | `background_pid=531815`, `pid_file=531815`, ready file created | `stopped=yes` |

## Target Availability

| Requested target family | Local status | Action |
|---|---|---|
| `common-build`, `build-common` | Not present | Documented as not present |
| `apache-build`, `build-apache`, `apache-structure` | Not present | Used Apache Common/C-standard compile checks plus cached module load/start evidence |
| `nginx-build`, `build-nginx`, `nginx-structure` | Not present | Used NGINX Common/C-standard compile checks plus cached module load/start evidence |
| `haproxy-build`, `build-haproxy`, `haproxy-structure` | Not present | Used HAProxy Common/C-standard compile checks plus connector-local build/link targets |
| `envoy-build`, `build-envoy`, `envoy-structure` | Not present | Used `make -C connectors/envoy build-starter` |
| `traefik-build`, `build-traefik`, `traefik-structure` | Not present | Used `make -C connectors/traefik build-starter build-decision-service build-forwardauth-starter` |
| `lighttpd-build`, `build-lighttpd`, `lighttpd-structure` | Not present | Used `make -C connectors/lighttpd build-starter` and a manual compile-only bridge build |
| `smoke-*`, runtime, CRS, matrix, and harness targets | Present but out of scope | Not used as accepted audit evidence |

## Disqualified Evidence

`make -C connectors/lighttpd build-bridge-starter` was found to invoke
`--self-test` inside `connectors/lighttpd/build/bridge_starter.sh`. That result
is not counted as accepted evidence for this audit. The bridge starter was built
again with a compile-only command recorded in `logs/lighttpd-bridge-compile-only.log`.

## Intentionally Not Executed

| Category | Status | Reason |
|---|---|---|
| HTTP requests | Not executed | Start smokes only checked config, PID/ready files, and stop behavior |
| CRS runtime cases | Not executed | Out of scope for compile/link/start audit |
| Full-matrix runtime jobs | Not executed | Out of scope for compile/link/start audit |
| Response-body checks | Not executed | Would require runtime traffic |
| Live connector transaction checks | Not executed | Would require request/response traffic |
| Runtime/security claims | Not made | This report only records build, link, config-load, and process-start capability |
