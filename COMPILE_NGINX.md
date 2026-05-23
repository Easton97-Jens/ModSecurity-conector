# Compile NGINX

This document explains how the NGINX connector is built and validated in this
repository. It follows the root `README.md` terminology: connector source is
repo-local, NGINX runtime behavior is adapter-owned, the framework module owns
the reusable smoke/test machinery, and `BUILD_ROOT` is a local build/output
location rather than a cache contract.

The repository-supported path is the framework-backed `make smoke-nginx`
target. Manual NGINX build commands are included only as general guidance for
operators who need to reproduce the module build outside the repository helper.

## Overview

The NGINX connector is an adapter-owned NGINX HTTP module under
`connectors/nginx/`. The productive source lives in `connectors/nginx/src/`,
and the NGINX third-party module `config` file lives at `connectors/nginx/config`.
The connector integrates libmodsecurity v3 with NGINX, but the WAF engine and
rule evaluation remain in libmodsecurity and in the loaded rules.

The current README describes the NGINX connector as an adapter-owned dynamic
NGINX module with a source-build smoke harness. That wording is intentional:
the repository records local build and runtime evidence through generated
source trees and smoke tests, but it does not claim broad production support
for every NGINX version or every runtime configuration.

At a high level, the repository build path:

1. Uses or fetches a libmodsecurity v3 source tree.
2. Builds libmodsecurity v3 under the local build root.
3. Materializes the repo-local NGINX connector source under `BUILD_ROOT`.
4. Downloads or prepares the NGINX source used by the smoke helper.
5. Builds the connector as a dynamic NGINX module.
6. Starts a generated local NGINX runtime.
7. Sends real HTTP requests from the shared YAML cases.
8. Records evidence under the repository's generated reports and build logs.

`make smoke-nginx` is authoritative only when it is actually executed
successfully. Generated metadata alone is not runtime evidence.

## Repository Layout

The README's connector architecture section is the best starting point. For
the NGINX build, the most relevant paths are:

| Path | Purpose |
| --- | --- |
| `connectors/nginx/` | Adapter-owned NGINX connector tree |
| `connectors/nginx/config` | NGINX third-party module build glue |
| `connectors/nginx/src/` | Productive NGINX connector source and headers |
| `connectors/nginx/harness/` | Runtime smoke harness and NGINX config template |
| `common/include/msconnector/` | Connector-neutral directive, option/default, request, response, transaction, intervention, capability, origin, logging, and status data shapes |
| `common/src/` | Small connector-neutral helper implementations |
| `modules/ModSecurity-test-Framework/` | Framework module that owns YAML cases, runners, normalizers, runtime matrix logic, coverage generation, v3 API smoke helpers, and reusable testing documentation |
| `reports/testing/` | Connector-specific generated evidence written by framework-backed targets |
| `TEST-COVERAGE-SUMMARY.md` | Generated root copy of test coverage evidence |

Apache and NGINX connector repositories are not fetched as runtime defaults.
The default build input is the repo-local adapter-owned source under
`connectors/nginx/`.

## Required Repository Setup

Initialize the framework module before running framework-backed targets:

```sh
git submodule update --init --recursive
```

The default framework path is:

```sh
modules/ModSecurity-test-Framework
```

When using a separate test-framework checkout, use the README-supported
`FRAMEWORK_ROOT` override:

```sh
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make quick-check
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make runtime-matrix-all
```

The same override applies to `make smoke-nginx` when the framework lives
outside the default submodule path.

## Build Variables

Use the same source-build variables documented in the README:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build
SOURCE_ROOT=$BUILD_ROOT/sources
MODSECURITY_GIT_REF=v3/master
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3
```

Important meanings:

| Variable | Meaning |
| --- | --- |
| `BUILD_ROOT` | Local build/output location. It is not a cache contract. |
| `SOURCE_ROOT` | Source checkout area used by framework helpers. |
| `MODSECURITY_GIT_REF` | libmodsecurity v3 git ref used by source-fetch helpers. |
| `MODSECURITY_SOURCE_DIR` | Canonical libmodsecurity v3 source directory for the smoke/build helpers. |
| `FRAMEWORK_ROOT` | Optional override for the reusable test framework module. |

The NGINX helper also uses NGINX-specific variables such as
`BUILD_NGINX_FROM_SOURCE`, `NGINX_RELEASE_TAG`, and
`MODSECURITY_NGINX_SOURCE_DIR`. These are part of the framework-backed helper
scripts rather than the root README's minimal source-build variable set. Use
them when you need to pin or override the NGINX source used by the local smoke
path.

## Recommended Build and Validation Flow

The root README lists the stable public connector targets:

```sh
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
make runtime-matrix-all
make smoke-apache
make smoke-nginx
make smoke-all
```

For a normal local setup:

```sh
git submodule update --init --recursive
make setup-dev
make lint
make quick-check
make generate-test-matrix
make check-test-matrix
```

For a NGINX source-build smoke:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SOURCE_ROOT=$BUILD_ROOT/sources \
MODSECURITY_GIT_REF=v3/master \
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3 \
BUILD_NGINX_FROM_SOURCE=1 \
make smoke-nginx
```

Use `REFRESH=1` when you intentionally want to replace an existing generated
build tree:

```sh
REFRESH=1 \
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SOURCE_ROOT=$BUILD_ROOT/sources \
MODSECURITY_GIT_REF=v3/master \
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3 \
BUILD_NGINX_FROM_SOURCE=1 \
make smoke-nginx
```

The smoke target delegates to the framework module. It builds the local NGINX
module path only as part of a runtime validation flow; a build artifact alone
is not promoted as successful runtime evidence.

## What `make smoke-nginx` Builds

The NGINX build helper is provided by the framework module and is invoked
through the repository Makefile. For the monorepo default it materializes the
adapter-owned NGINX connector source into:

```text
$BUILD_ROOT/nginx-build/connector-src
```

The helper then builds libmodsecurity v3 and uses the materialized connector
source as the NGINX module input. Typical generated artifacts include:

```text
$BUILD_ROOT/nginx-build/connector-src
$BUILD_ROOT/nginx-build/output/modsecurity/include/modsecurity/modsecurity.h
$BUILD_ROOT/nginx-build/output/modsecurity/lib/libmodsecurity.so
$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx
$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so
$BUILD_ROOT/logs/nginx/artifacts.txt
$BUILD_ROOT/logs/nginx/commands.txt
```

The exact set of generated files depends on the helper configuration and the
environment. Treat files under `BUILD_ROOT` as generated build/output material.
Do not edit them as source.

The productive source remains in:

```text
connectors/nginx/config
connectors/nginx/src/
```

The former upstream reference tree is not a runtime default. Durable
attribution and source metadata live in the connector metadata and licensing
paths described by the README.

## Dynamic Module Build

The current repository-supported NGINX proof path builds a dynamic module. This
matches `connectors/nginx/docs/build.md`, which records the dynamic-module path
as the active proof-of-concept build path.

The resulting module is expected under the generated NGINX runtime:

```text
$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so
```

The generated NGINX binary is expected under:

```text
$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx
```

The harness renders an NGINX configuration from
`connectors/nginx/harness/nginx_smoke.conf`. That template uses:

```nginx
load_module "@@NGINX_MODULE@@";
modsecurity on;
modsecurity_rules_file "@@RULES_FILE@@";
```

The rules file, request data, response fixtures, audit-log paths, and expected
status are materialized from framework YAML cases at runtime.

## Static Module Build

General guidance: NGINX third-party modules can often be compiled statically
with `--add-module=...` instead of `--add-dynamic-module=...`.

This repository does not present static NGINX module builds as the current
validated path. The local documentation explicitly keeps dynamic module support
as the active proof path until static behavior is separately proven. If you
choose to build statically, treat it as an environment-specific build outside
the repository's current evidence path and validate it with real HTTP smoke
tests before relying on it.

## General Manual Build Guidance

The repository-specific path above should be preferred. The following commands
are general NGINX guidance and are not a replacement for `make smoke-nginx`.
Use them only when you need to reproduce a module build against a separately
managed NGINX source tree.

```sh
export CONNECTOR_ROOT=/path/to/ModSecurity-conector
export MODSECURITY_INC=/usr/local/modsecurity/include
export MODSECURITY_LIB=/usr/local/modsecurity/lib
export MSCONNECTOR_COMMON_INC="$CONNECTOR_ROOT/common/include"

cd /path/to/nginx-source

./configure \
  --prefix=/opt/nginx-modsec \
  --modules-path=/opt/nginx-modsec/modules \
  --with-compat \
  --add-dynamic-module="$CONNECTOR_ROOT/connectors/nginx"

make modules
```

The important relationship to the repository is the module source path:

```text
$CONNECTOR_ROOT/connectors/nginx
```

The NGINX `config` file in that directory detects libmodsecurity and includes
the connector-neutral headers from `common/include/msconnector/`.

Manual builds must still be validated with a configuration test, real HTTP
requests, and log inspection. They do not automatically update repository
evidence under `reports/testing/` or `TEST-COVERAGE-SUMMARY.md`.

## NGINX Configuration

For the repository smoke harness, the generated configuration is derived from
`connectors/nginx/harness/nginx_smoke.conf`. For an operator-managed NGINX
runtime, a dynamic-module configuration generally needs:

```nginx
load_module /path/to/ngx_http_modsecurity_module.so;

events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name example.local;

        modsecurity on;
        modsecurity_rules_file /path/to/modsecurity-rules.conf;

        location / {
            proxy_pass http://127.0.0.1:8080;
        }
    }
}
```

General guidance: the loaded rules file controls engine behavior. A minimal
test rules file might contain:

```apache
SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On

SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog /path/to/modsec_audit.log

SecRule ARGS:test "@streq block" \
  "id:100000,phase:2,deny,status:403,msg:'NGINX connector test rule'"
```

Keep path ownership in mind:

- The NGINX worker must be able to read the rules file.
- The NGINX worker must be able to write the audit log path if audit logging is
  enabled.
- `modsecurity_use_error_log off` suppresses the connector's NGINX error-log
  write from the libmodsecurity log callback only. Audit logs, interventions,
  and request/response handling are unchanged.

## Functional Validation

Repository validation should use the Makefile target:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SOURCE_ROOT=$BUILD_ROOT/sources \
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3 \
make smoke-nginx
```

For a single or smaller set of framework cases, use the framework-supported
smoke-case selection mechanism:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SMOKE_CASES="phase1_header_block phase2_args_block" \
make smoke-nginx
```

For a broader evidence run:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
make runtime-matrix-all
```

The README's warning applies: runtime and coverage evidence must not be
inferred from generated metadata alone. XFAIL, pending, future, connector-gap,
and runtime-difference cases stay evidence classes until explicitly promoted by
documented runtime proof. `RESPONSE_BODY` remains non-verified and
non-promoted.

General guidance for an external NGINX runtime:

```sh
nginx -t
nginx -V 2>&1
ldd /path/to/ngx_http_modsecurity_module.so
curl -i "http://127.0.0.1/?test=block"
```

With a blocking test rule and `SecRuleEngine On`, a matching request should
return the rule's disruptive status, commonly `403`. A non-matching request
should pass normally.

## Troubleshooting

### Missing Framework Module

If `make smoke-nginx` reports that `FRAMEWORK_ROOT` is missing, initialize the
submodule or set `FRAMEWORK_ROOT` explicitly:

```sh
git submodule update --init --recursive
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make smoke-nginx
```

### Existing Build Directory

The helper can block when generated build directories already exist. Use
`REFRESH=1` only when you intentionally want to replace generated build output:

```sh
REFRESH=1 BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build make smoke-nginx
```

### Missing libmodsecurity Headers or Library

For repository builds, confirm that `MODSECURITY_SOURCE_DIR` points at a
usable libmodsecurity v3 source tree or let the framework fetch sources through
the documented source variables.

For general manual builds, verify:

```sh
test -f "$MODSECURITY_INC/modsecurity/modsecurity.h"
test -f "$MODSECURITY_LIB/libmodsecurity.so"
```

### Runtime Linker Cannot Find `libmodsecurity.so`

Generated repository harnesses set the runtime library path to the staged
libmodsecurity output under `BUILD_ROOT`. For a manually managed runtime,
check:

```sh
ldd /path/to/ngx_http_modsecurity_module.so
```

If `libmodsecurity.so` is unresolved, configure the system library path or use
an environment-specific runtime wrapper.

### NGINX Module Compatibility

Dynamic NGINX modules are sensitive to the target NGINX binary and build
options. For manual builds, compare the target:

```sh
nginx -V 2>&1
```

Build the module against a matching source/version and use `--with-compat`
where appropriate. The repository smoke path avoids this ambiguity by building
the NGINX binary and module together under `BUILD_ROOT`.

### Rules Are Not Loaded

Use the generated logs under `BUILD_ROOT` for repository builds:

```text
$BUILD_ROOT/logs/nginx/
```

For external runtimes, run `nginx -t` and inspect the error log. Typical causes
are wrong paths, missing read permissions, invalid rule syntax, or a
libmodsecurity/rule-version mismatch.

## Best Practices

- Prefer `make smoke-nginx` for repository evidence.
- Keep `BUILD_ROOT`, `SOURCE_ROOT`, `MODSECURITY_SOURCE_DIR`, and
  `MODSECURITY_GIT_REF` explicit when sharing reproduction commands.
- Treat `BUILD_ROOT` as generated output, not source.
- Keep NGINX runtime behavior in `connectors/nginx/`; do not move hooks,
  filters, body handling, transaction ownership, or intervention behavior into
  `common/` without separate design and smoke evidence.
- Rebuild and rerun smoke tests after NGINX, libmodsecurity, or connector
  source changes.
- Use `make lint`, `make quick-check`, `make generate-test-matrix`, and
  `make check-test-matrix` before relying on generated evidence.
- Use `make smoke-all` only as evidence when it has actually executed
  successfully.
