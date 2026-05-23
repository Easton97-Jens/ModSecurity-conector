# Compile Apache

This document explains how the Apache connector is built and validated in this
repository. It follows the root `README.md` terminology: connector source is
repo-local, Apache runtime behavior is adapter-owned, the framework module owns
the reusable smoke/test machinery, and `BUILD_ROOT` is a local build/output
location rather than a cache contract.

The repository-supported path is the framework-backed `make smoke-apache`
target. Manual Apache/APXS commands are included only as general guidance for
operators who need to reproduce the module build outside the repository helper.

## Overview

The Apache connector is an adapter-owned Apache module under
`connectors/apache/`. The productive source lives in `connectors/apache/src/`,
and the Autotools/APXS build inputs live under `connectors/apache/`. The module
is loaded into Apache with `LoadModule`, registers Apache hooks and filters,
and passes request/response data to libmodsecurity v3.

The README describes Apache as an adapter-owned scaffold with a source-build
smoke harness. That wording matters: the repository records local build and
runtime evidence through generated source trees and smoke tests, but it does
not claim that every Apache distribution, MPM, module combination, or response
body edge case is fully supported.

At a high level, the repository build path:

1. Uses or fetches a libmodsecurity v3 source tree.
2. Builds libmodsecurity v3 under the local build root.
3. Materializes the repo-local Apache connector source under `BUILD_ROOT`.
4. Uses a source-built or explicitly supplied Apache/httpd and APXS pair.
5. Runs the connector's Autotools/APXS build.
6. Copies the generated `mod_security3.so` into the local build output.
7. Starts a generated local Apache runtime.
8. Sends real HTTP requests from the shared YAML cases.
9. Records evidence under the repository's generated reports and build logs.

`make smoke-apache` is authoritative only when it is actually executed
successfully. Generated metadata alone is not runtime evidence.

## Repository Layout

For the Apache build, the most relevant paths are:

| Path | Purpose |
| --- | --- |
| `connectors/apache/` | Adapter-owned Apache connector tree |
| `connectors/apache/configure.ac` | Autoconf build input |
| `connectors/apache/Makefile.am` | Automake build input |
| `connectors/apache/autogen.sh` | Autotools bootstrap script |
| `connectors/apache/build/` | APXS/libmodsecurity discovery macros and wrapper template |
| `connectors/apache/src/` | Productive Apache connector source and headers |
| `connectors/apache/harness/` | Runtime smoke harness and Apache config template |
| `common/include/msconnector/` | Connector-neutral directive, option/default, request, response, transaction, intervention, capability, origin, logging, and status data shapes |
| `common/src/` | Small connector-neutral helper implementations |
| `modules/ModSecurity-test-Framework/` | Framework module that owns YAML cases, runners, normalizers, runtime matrix logic, coverage generation, v3 API smoke helpers, and reusable testing documentation |
| `reports/testing/` | Connector-specific generated evidence written by framework-backed targets |
| `TEST-COVERAGE-SUMMARY.md` | Generated root copy of test coverage evidence |

Apache connector repositories are not fetched as runtime defaults. The default
build input is the repo-local adapter-owned source under `connectors/apache/`.

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

The same override applies to `make smoke-apache` when the framework lives
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

The Apache helper also supports Apache-specific variables such as
`BUILD_HTTPD_FROM_SOURCE`, `APXS`, `APACHE_HTTPD`, and
`MODSECURITY_APACHE_SOURCE_DIR`. Use those when you need to pin the Apache
toolchain or build from an explicit external connector checkout. The README
default remains the repo-local connector source.

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

For an Apache source-build smoke:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SOURCE_ROOT=$BUILD_ROOT/sources \
MODSECURITY_GIT_REF=v3/master \
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3 \
BUILD_HTTPD_FROM_SOURCE=1 \
make smoke-apache
```

Use `REFRESH=1` when you intentionally want to replace an existing generated
build tree:

```sh
REFRESH=1 \
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SOURCE_ROOT=$BUILD_ROOT/sources \
MODSECURITY_GIT_REF=v3/master \
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3 \
BUILD_HTTPD_FROM_SOURCE=1 \
make smoke-apache
```

The smoke target delegates to the framework module. It builds the local Apache
module path only as part of a runtime validation flow; a build artifact alone
is not promoted as successful runtime evidence.

## What `make smoke-apache` Builds

The Apache build helper is provided by the framework module and is invoked
through the repository Makefile. For the monorepo default it materializes the
adapter-owned Apache connector source into:

```text
$BUILD_ROOT/apache-build/connector-src
```

The helper then builds libmodsecurity v3, prepares or resolves Apache/httpd
and APXS, and uses the materialized connector source as the Apache module
input. Typical generated artifacts include:

```text
$BUILD_ROOT/apache-build/connector-src
$BUILD_ROOT/apache-build/output/modsecurity/include/modsecurity/modsecurity.h
$BUILD_ROOT/apache-build/output/modsecurity/lib/libmodsecurity.so
$BUILD_ROOT/apache-build/output/apache/mod_security3.so
$BUILD_ROOT/apache-runtime/httpd/bin/httpd
$BUILD_ROOT/apache-runtime/httpd/bin/apxs
$BUILD_ROOT/logs/apache/artifacts.txt
$BUILD_ROOT/logs/apache/commands.txt
```

The exact set of generated files depends on whether the helper builds Apache
from source or uses explicit `APXS`/`APACHE_HTTPD` inputs. Treat files under
`BUILD_ROOT` as generated build/output material. Do not edit them as source.

The productive source remains in:

```text
connectors/apache/
connectors/apache/src/
```

## APXS and Apache Tooling

Apache modules are built against a concrete Apache development environment.
The repository helper can build httpd from source when
`BUILD_HTTPD_FROM_SOURCE=1`, or it can use explicit external tools:

```sh
APXS=/path/to/apxs \
APACHE_HTTPD=/path/to/httpd \
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
make smoke-apache
```

If you provide external tools, they must match each other. APXS from one Apache
installation and an `httpd` binary from another can produce confusing compiler,
linker, module-loading, or runtime failures.

General APXS inspection commands:

```sh
apxs -q CC
apxs -q INCLUDEDIR
apxs -q LIBEXECDIR
apxs -q SBINDIR
apxs -q PROGNAME
```

On Debian/Ubuntu the binary is often `apxs2`; on other systems it is often
`apxs`. This naming detail is distribution-specific general guidance. The
repository helper cares about the executable path you pass through `APXS` or
about the APXS it builds with source-built httpd.

## General Manual Build Guidance

The repository-specific path above should be preferred. The following commands
are general Apache guidance and are not a replacement for `make smoke-apache`.
Use them only when you need to reproduce a module build against a separately
managed Apache installation.

```sh
cd /path/to/ModSecurity-conector/connectors/apache

./autogen.sh

./configure \
  --with-libmodsecurity=/usr/local/modsecurity \
  --with-apxs=/path/to/apxs \
  --with-apache=/path/to/httpd

make
```

The local build artifact typically appears under:

```text
connectors/apache/src/.libs/mod_security3.so
```

The repository helper avoids writing generated Autotools files into the source
checkout by materializing a generated connector source tree under `BUILD_ROOT`
first. That behavior matches the README's convention that build and runtime
outputs belong under `BUILD_ROOT`.

Manual builds must still be validated with a configuration test, real HTTP
requests, and log inspection. They do not automatically update repository
evidence under `reports/testing/` or `TEST-COVERAGE-SUMMARY.md`.

## Apache Configuration

For the repository smoke harness, the generated configuration is derived from
`connectors/apache/harness/apache_smoke.conf`. That template loads the module
and sets:

```apache
LoadModule security3_module "@@APACHE_MODULE@@"
modsecurity on
modsecurity_rules_file "@@RULES_FILE@@"
```

For an operator-managed Apache runtime, the same concepts generally look like:

```apache
LoadModule security3_module "/path/to/mod_security3.so"

modsecurity on
modsecurity_rules_file "/path/to/modsecurity-rules.conf"
```

General guidance: the loaded rules file controls engine behavior. A minimal
test rules file might contain:

```apache
SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On

SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog "/path/to/modsec_audit.log"

SecRule ARGS:test "@streq block" \
  "id:200000,phase:2,deny,status:403,msg:'Apache connector test rule'"
```

Current Apache directives are documented in the root README and
`docs/connectors/directive-parity.md`:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`

`modsecurity_transaction_id` keeps static-string semantics.
`modsecurity_transaction_id_expr` is an opt-in Apache string expression
evaluated per request. The two transaction-ID directives are mutually
exclusive in the same Apache context. If neither directive is set, or if the
expression evaluates to an empty value or fails, Apache keeps the existing
`UNIQUE_ID` fallback and then creates a transaction without an explicit ID if
no usable `UNIQUE_ID` value is available.

`modsecurity_use_error_log off` suppresses Apache error-log forwarding from
the libmodsecurity log callback only. It does not change audit logging,
interventions, hooks, filters, buckets, transaction ownership, or request and
response handling.

## Functional Validation

Repository validation should use the Makefile target:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SOURCE_ROOT=$BUILD_ROOT/sources \
MODSECURITY_SOURCE_DIR=$SOURCE_ROOT/ModSecurity_V3 \
make smoke-apache
```

For a single or smaller set of framework cases:

```sh
BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build \
SMOKE_CASES="phase1_header_block phase2_args_block" \
make smoke-apache
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

General guidance for an external Apache runtime:

```sh
apachectl configtest
apachectl -M 2>/dev/null | grep -i security
ldd /path/to/mod_security3.so
curl -i "http://127.0.0.1/?test=block"
```

With a blocking test rule and `SecRuleEngine On`, a matching request should
return the rule's disruptive status, commonly `403`. A non-matching request
should pass normally.

## Troubleshooting

### Missing Framework Module

If `make smoke-apache` reports that `FRAMEWORK_ROOT` is missing, initialize
the submodule or set `FRAMEWORK_ROOT` explicitly:

```sh
git submodule update --init --recursive
FRAMEWORK_ROOT=/path/to/ModSecurity-test-Framework make smoke-apache
```

### Existing Build Directory

The helper can block when generated build directories already exist. Use
`REFRESH=1` only when you intentionally want to replace generated build output:

```sh
REFRESH=1 BUILD_ROOT=$HOME/.local/state/ModSecurity-conector-build make smoke-apache
```

### Missing APXS or Apache Development Files

For repository source-built httpd runs, use:

```sh
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

For explicit external Apache tools, set both:

```sh
APXS=/path/to/apxs APACHE_HTTPD=/path/to/httpd make smoke-apache
```

If only one is set, or if they point to mismatched installations, the helper
can block or produce invalid module artifacts.

### Missing libmodsecurity Headers or Library

For repository builds, confirm that `MODSECURITY_SOURCE_DIR` points at a
usable libmodsecurity v3 source tree or let the framework fetch sources through
the documented source variables.

For general manual builds, verify:

```sh
test -f /usr/local/modsecurity/include/modsecurity/modsecurity.h
test -f /usr/local/modsecurity/lib/libmodsecurity.so
ldd /path/to/mod_security3.so
```

### Module Cannot Be Loaded

Check that the `LoadModule` path points at the built `mod_security3.so`, that
`ldd` does not show missing libraries, and that the module was built with APXS
from the target Apache installation.

### Rules Are Not Loaded

Use generated logs under `BUILD_ROOT` for repository builds:

```text
$BUILD_ROOT/logs/apache/
$BUILD_ROOT/logs/apache-runtime/
```

For external runtimes, run `apachectl configtest` and inspect the error log.
Typical causes are wrong paths, missing read permissions, invalid rule syntax,
or a libmodsecurity/rule-version mismatch.

### Permission Problems

General guidance: Apache must be able to read the rules file and write audit
logs. The runtime user differs by distribution. Use tools such as `namei -l`
to inspect every path component when permissions are unclear.

## Best Practices

- Prefer `make smoke-apache` for repository evidence.
- Keep `BUILD_ROOT`, `SOURCE_ROOT`, `MODSECURITY_SOURCE_DIR`, and
  `MODSECURITY_GIT_REF` explicit when sharing reproduction commands.
- Treat `BUILD_ROOT` as generated output, not source.
- Keep Apache runtime behavior in `connectors/apache/`; do not move hooks,
  filters, bucket brigades, config parsing, transaction ownership, or
  intervention behavior into `common/` without separate design and smoke
  evidence.
- Rebuild and rerun smoke tests after Apache, libmodsecurity, or connector
  source changes.
- Use `make lint`, `make quick-check`, `make generate-test-matrix`, and
  `make check-test-matrix` before relying on generated evidence.
- Use `make smoke-all` only as evidence when it has actually executed
  successfully.
