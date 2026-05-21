# Apache Connector PoC

Status: scaffolded

## Implemented

- `modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh` prepares a connector-specific Apache PoC build
  under `BUILD_ROOT`.
- The helper can build Apache httpd from source under `BUILD_ROOT`; system-wide
  `apxs` and `httpd` are not required.
- `connectors/apache/harness/run_apache_smoke.sh` prepares a local Apache
  runtime under `BUILD_ROOT` and checks for a real HTTP `403`.
- The shared minimal YAML cases under `modules/ModSecurity-test-Framework/tests/cases/` define the
  rule/request/expectation model used by Apache and NGINX.
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py` reads each YAML file and materializes the Apache
  rules, request method/path, headers, body, multipart body, response fixture,
  and expected HTTP status for the harness.

Implemented here means build orchestration, runtime harness, and documentation.
It does not mean that Apache has loaded the module successfully in every
environment.

When the smoke passes it is a `real-world-connector-path` validation:

```text
HTTP client -> source-built httpd -> mod_security3.so -> libmodsecurity -> HTTP response
```

The connector-free v3 API smoke under `framework v3 API smoke helper/` is separate and is
not counted as Apache connector success.

## Build Flow

Defaults are local conveniences only:

```sh
MODSECURITY_V3_SOURCE_DIR=/root/conecter/ModSecurity_V3
MODSECURITY_APACHE_SOURCE_DIR=/root/conecter/ModSecurity-apache
BUILD_ROOT=/src/ModSecurity-conector-build
LOG_DIR=$BUILD_ROOT/logs/apache
```

Source references for those local defaults:

| Repository | Local reference | Upstream | Observed commit | Observed version/tag | License |
| --- | --- | --- | --- | --- | --- |
| ModSecurity v3 | `/root/conecter/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Apache-2.0 |
| ModSecurity-apache | `/root/conecter/ModSecurity-apache` | https://github.com/owasp-modsecurity/ModSecurity-apache | `0488c77f69669584324b70460614a382224b4883` | `v0.0.9-beta1-26-g0488c77` | Apache-2.0 |

All paths are environment-overridable. Generated files must stay outside the
Git checkout and outside `/root/conecter/*`.

## Source-Built httpd Mode

The Apache PoC can build httpd without package installation:

```sh
REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT=/src/ModSecurity-conector-build \
sh modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh
```

Default source versions:

| Variable | Default |
| --- | --- |
| `HTTPD_VERSION` | `2.4.67` |
| `APR_VERSION` | `1.7.6` |
| `APR_UTIL_VERSION` | `1.6.3` |
| `PCRE2_VERSION` | `10.47` |

Default generated paths:

```text
$BUILD_ROOT/apache-build/downloads/
$BUILD_ROOT/apache-build/httpd-src/
$BUILD_ROOT/apache-build/httpd/
$BUILD_ROOT/apache-runtime/httpd/
$BUILD_ROOT/logs/apache/
```

The helper downloads httpd, APR, and APR-util from Apache distribution URLs,
verifies their SHA256 files, unpacks APR and APR-util into the httpd `srclib`
tree, and configures httpd with:

```text
--prefix=$HTTPD_PREFIX
--with-included-apr
--with-pcre=$PCRE_CONFIG
--enable-so
--enable-mods-shared=most
--enable-mpms-shared=all
--with-mpm=event
```

PCRE handling is explicit:

- `PCRE_CONFIG=/path/to/pcre2-config` or `/path/to/pcre-config` wins.
- `BUILD_PCRE2_FROM_SOURCE=1` builds PCRE2 under
  `$BUILD_ROOT/apache-build/output/pcre2`.
- If no PCRE config tool is available and PCRE2 source build is not enabled,
  the helper exits `77` with `blocked`.

OpenSSL is not enabled for this HTTP-only smoke probe.

The helper copies the read-only sources to:

```text
$BUILD_ROOT/apache-build/ModSecurity_V3
$BUILD_ROOT/apache-build/connector-src
```

It then builds only inside those copies. The Apache connector build uses the
adapter-owned source materialized from `connectors/apache/src` while preserving
the observed Autotools/APXS path:

```sh
./autogen.sh
./configure --with-libmodsecurity=$BUILD_ROOT/apache-build/output/modsecurity
make
```

The libmodsecurity staging directory contains copied headers and shared library
artifacts from the v3 build copy:

```text
$BUILD_ROOT/apache-build/output/modsecurity/include/
$BUILD_ROOT/apache-build/output/modsecurity/lib/
```

## Runtime Smoke

The Apache harness renders `connectors/apache/harness/apache_smoke.conf` into a
per-case runtime directory, for example:

```text
$BUILD_ROOT/apache-runtime/phase2_args_block/conf/httpd.conf
```

Rules, request details, and expected statuses are read from:

```text
modules/ModSecurity-test-Framework/tests/cases/*.yaml
modules/ModSecurity-test-Framework/tests/cases/*.yaml
modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/*.yaml
```

The default run executes:

```text
phase1_header_block
phase2_args_block
phase2_args_pass
audit_log_phase1_block
request_body_json_block
request_body_urlencoded_block
response_header_basic
json_request_body_block
multipart_basic_block
response_body_pass
```

Run through the formal target:

```sh
BUILD_ROOT=/src/ModSecurity-conector-build make smoke-apache
```

The harness does not hardcode the rule, request path, request method, headers,
body, response fixture, or expected HTTP status. Readiness uses
`/__modsec_smoke_ready` with ModSecurity disabled so phase and response rules do
not affect startup checks. Status `pass` is only valid when the common runner
checks the observed Apache response against each YAML expectation. A successful
compile alone is not a runtime pass.

The generated `$BUILD_ROOT/results/apache-summary.json` records
`connector_path: real-world`, `validation_mode:
real-world-connector-path`, the httpd binary, `mod_security3.so`,
libmodsecurity, and `verified_variables` derived only from passing cases.

## Current Local Status

Observed in this workspace on 2026-05-15:

- `autoconf`, `automake`, `libtoolize`, `make`, `cc`, `c++`, `curl`, and `perl`
  are present.
- `apxs`, `apxs2`, `apache2`, `httpd`, `apachectl`, and `apache2ctl` were not
  found in `PATH`.
- `REFRESH=1 BUILD_HTTPD_FROM_SOURCE=1
  BUILD_ROOT=/src/ModSecurity-conector-build sh modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh`
  built Apache httpd from source, built libmodsecurity v3 in a writable copy,
  and built `mod_security3.so`.
- `BUILD_ROOT=/src/ModSecurity-conector-build make smoke-apache` returned pass
  for all current shared minimal cases and the active common imported cases,
  including raw JSON body, simple multipart text-field, and response-body
  pass-through smokes.

Artifacts generated by the local pass:

```text
/src/ModSecurity-conector-build/apache-build/ModSecurity_V3
/src/ModSecurity-conector-build/apache-build/connector-src
/src/ModSecurity-conector-build/apache-build/output/apache/mod_security3.so
/src/ModSecurity-conector-build/apache-build/output/modsecurity/
/src/ModSecurity-conector-build/apache-runtime/httpd/bin/apxs
/src/ModSecurity-conector-build/apache-runtime/httpd/bin/httpd
/src/ModSecurity-conector-build/logs/apache/
/src/ModSecurity-conector-build/logs/apache-runtime/<case>/status.txt
/src/ModSecurity-conector-build/results/apache-summary.txt
/src/ModSecurity-conector-build/results/apache-summary.json
```

Observed tool and version details:

```text
httpd_source_built=1
httpd_version=2.4.67
apxs=/src/ModSecurity-conector-build/apache-runtime/httpd/bin/apxs
apache_httpd=/src/ModSecurity-conector-build/apache-runtime/httpd/bin/httpd
apache_httpd_version=Apache/2.4.67
pcre_config=/usr/bin/pcre2-config
pcre_config_version=10.46
pcre2_source_built=0
apache_smoke_cases=audit_log_phase1_block, phase1_header_block, phase2_args_block, phase2_args_pass, request_body_json_block, request_body_urlencoded_block, response_header_basic, json_request_body_block, multipart_basic_block, response_body_pass
apache_smoke_status=all pass; blocking cases HTTP 403; pass-through case HTTP 200
apache_validation_mode=real-world-connector-path
apache_verified_variables=ARGS,REQUEST_HEADERS,REQUEST_BODY,FILES,XML,AUDIT_LOG,RESPONSE_HEADERS
```

## Status Meanings

- `implemented`: helper scripts, harness template, shared case, and docs exist.
- `blocked`: required source, APXS, Apache, module, or library prerequisite is
  missing; no functionality is claimed.
- `fail`: prerequisites exist but a build, configtest, startup, or HTTP
  expectation fails.
- `pass`: Apache returns the YAML-expected HTTP status for every selected
  shared smoke case.

## Tracked Open Work

Open Apache PoC follow-ups are tracked in
`docs/roadmap/todo-inventory.md` and `docs/roadmap/roadmap.md`.

## Public Sources

- Apache httpd install documentation:
  https://httpd.apache.org/docs/current/install.html.en
- Apache httpd distribution index:
  https://downloads.apache.org/httpd/
- Apache APR download page:
  https://apr.apache.org/download.cgi
- PCRE2 build and release documentation:
  https://pcre2project.github.io/pcre2/guide/readme/
