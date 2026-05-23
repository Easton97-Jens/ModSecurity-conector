# Compile Apache

This guide explains how to build and enable the ModSecurity connector from this
repository as an Apache/httpd module. The local connector lives under
`connectors/apache/`, uses Autotools, and is built with `apxs` against a
specific Apache installation.

## Overview

The Apache connector is a Dynamic Shared Object for Apache/httpd. It is loaded
with `LoadModule`, registers Apache hooks and filters, and passes request and
response data to libmodsecurity v3. Unlike the Nginx connector, it does not
extend an Nginx source tree. Instead, the build uses `apxs` to obtain compiler
flags, include paths, and module paths for the target Apache installation.

`apxs` is important because:

- It belongs to the Apache development environment.
- It knows the module directory through `apxs -q LIBEXECDIR`.
- It knows the compiler and include paths through `apxs -q CC` and
  `apxs -q INCLUDEDIR`.
- It can install modules in a way that matches the Apache installation.

The local build uses:

| File or directory | Purpose |
| --- | --- |
| `connectors/apache/autogen.sh` | Generates `configure` through `autoreconf --install` |
| `connectors/apache/configure.ac` | Finds APXS, Apache, and libmodsecurity |
| `connectors/apache/Makefile.am` | Invokes the APXS wrapper and install target |
| `connectors/apache/build/` | Autoconf macros and APXS wrapper template |
| `connectors/apache/src/` | Productive Apache connector sources |

The expected build artifact is:

```text
mod_security3.so
```

The repository helper copies it to:

```text
$BUILD_ROOT/apache-build/output/apache/mod_security3.so
```

## Prerequisites

For Debian/Ubuntu:

```sh
sudo apt-get update
sudo apt-get install -y \
  git make gcc g++ clang \
  autoconf automake libtool pkg-config \
  curl ca-certificates tar perl python3 \
  apache2 apache2-dev \
  libpcre2-dev libxml2-dev libyajl-dev liblmdb-dev libgeoip-dev \
  libcurl4-openssl-dev
```

If available:

```sh
sudo apt-get install -y libmodsecurity-dev
```

On Debian/Ubuntu, APXS is often named `apxs2`. On RHEL/Fedora, APXS usually
comes from `httpd-devel` and is named `apxs`. Other distributions use other
package names. What matters is that Apache, Apache development files, APXS, a
compiler, Autotools, and libmodsecurity-v3 headers are present.

The connector needs these libmodsecurity files:

- `modsecurity/modsecurity.h`
- `modsecurity/intervention.h`
- `modsecurity/transaction.h`
- either `modsecurity/rules_set.h` or `modsecurity/rules.h`, depending on the
  version
- `libmodsecurity.so`

The repository helper builds and stages libmodsecurity under:

```text
$BUILD_ROOT/apache-build/output/modsecurity/include
$BUILD_ROOT/apache-build/output/modsecurity/lib
```

For manual builds, an existing prefix can be supplied:

```sh
./configure --with-libmodsecurity=/usr/local/modsecurity
```

## Prepare the Repository

After a fresh clone:

```sh
git clone <repository-url> ModSecurity-conector
cd ModSecurity-conector
git submodule update --init --recursive
```

The `modules/ModSecurity-test-Framework` submodule is required for Makefile
targets, materialization, and smoke tests.

Important paths:

| Path | Purpose |
| --- | --- |
| `connectors/apache/` | Apache connector root |
| `connectors/apache/src/` | Apache module sources |
| `connectors/apache/build/` | M4 macros and APXS wrapper |
| `common/include/msconnector/` | Shared directive, option, and rule-load-stat headers |
| `connectors/apache/harness/` | Runtime smoke harness |
| `modules/ModSecurity-test-Framework/ci/prepare-apache-build.sh` | Build helper |

The repository-provided build and smoke path:

```sh
REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-apache
```

This path builds or stages libmodsecurity v3, materializes the Apache connector
into `$BUILD_ROOT/apache-build/connector-src`, builds Apache httpd from source
when requested, runs `./autogen.sh`, `./configure`, and `make` in the
materialized connector source tree, and then starts real HTTP smoke tests.

## Check the Apache Development Environment

Before a manual build, be explicit about which Apache and which APXS will be
used.

Debian/Ubuntu:

```sh
command -v apxs2
command -v apache2
apache2 -v
apache2 -V
```

Other distributions:

```sh
command -v apxs
command -v httpd
httpd -v
httpd -V
```

Useful APXS queries:

```sh
apxs2 -q CC
apxs2 -q INCLUDEDIR
apxs2 -q LIBEXECDIR
apxs2 -q SBINDIR
apxs2 -q PROGNAME
```

If `apxs2` is not available, use `apxs`. `LIBEXECDIR` is the usual module
path. `SBINDIR` and `PROGNAME` help identify the matching Apache binary.

Check loaded modules:

```sh
apache2ctl -M 2>/dev/null | head
```

or:

```sh
httpd -M 2>/dev/null | head
```

If the system installation is difficult to use, the isolated repository path
with `BUILD_HTTPD_FROM_SOURCE=1` may be simpler.

## Compile the Connector

### Build Through the Repository

```sh
git submodule update --init --recursive

REFRESH=1 \
BUILD_HTTPD_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-apache
```

Expected artifacts:

```text
$BUILD_ROOT/apache-build/output/apache/mod_security3.so
$BUILD_ROOT/apache-build/output/modsecurity/include/modsecurity/modsecurity.h
$BUILD_ROOT/apache-build/output/modsecurity/lib/libmodsecurity.so
$BUILD_ROOT/apache-runtime/httpd/bin/httpd
$BUILD_ROOT/apache-runtime/httpd/bin/apxs
$BUILD_ROOT/logs/apache/artifacts.txt
$BUILD_ROOT/logs/apache/commands.txt
```

`commands.txt` records the build commands that were executed. This is useful
when reproducing a failure on another machine.

### Manual Build

```sh
cd /path/to/ModSecurity-conector/connectors/apache

./autogen.sh

./configure \
  --with-libmodsecurity=/usr/local/modsecurity \
  --with-apxs="$(command -v apxs2 || command -v apxs)" \
  --with-apache="$(command -v apache2 || command -v httpd)"

make
```

Important options:

| Option | Meaning |
| --- | --- |
| `--with-libmodsecurity=...` | Prefix containing libmodsecurity headers and library |
| `--with-apxs=...` | APXS for the target Apache installation |
| `--with-apache=...` | Apache/httpd binary for the target installation |

The local build artifact typically appears here:

```text
connectors/apache/src/.libs/mod_security3.so
```

Install through APXS:

```sh
sudo make install
```

The install target invokes APXS with `-i -n mod_security3`. In package or
container builds, it is often better to copy the `.so` into a staging directory
and manage the Apache configuration separately.

## Enable the Apache Module

### Debian/Ubuntu with `a2enmod`

Example load file:

```apache
LoadModule security3_module /usr/lib/apache2/modules/mod_security3.so
```

Enable it:

```sh
sudo sh -c 'printf "%s\n" "LoadModule security3_module /usr/lib/apache2/modules/mod_security3.so" > /etc/apache2/mods-available/security3.load'
sudo a2enmod security3
```

Example configuration:

```apache
<IfModule security3_module>
    modsecurity on
    modsecurity_rules_file /etc/apache2/modsecurity/main.conf
</IfModule>
```

### Manual `LoadModule` Directive

```apache
LoadModule security3_module "/opt/httpd/modules/mod_security3.so"

modsecurity on
modsecurity_rules_file "/opt/httpd/conf/modsecurity/main.conf"
```

Minimal rules file:

```apache
SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On

SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog "/var/log/apache2/modsec_audit.log"

SecRule ARGS:test "@streq block" \
  "id:200000,phase:2,deny,status:403,msg:'Apache connector test rule'"
```

Notes:

- `modsecurity on` enables the connector.
- `modsecurity_rules_file` loads local rules through libmodsecurity.
- `modsecurity_rules` loads inline rules.
- `modsecurity_rules_remote` loads remote rules.
- In the Apache connector, `modsecurity_transaction_id` accepts a static
  string. Apache expressions are not evaluated.
- Without a configured transaction ID, the connector tries to use `UNIQUE_ID`
  and otherwise creates a transaction without an explicit ID.
- `modsecurity_use_error_log off` affects only the error-log callback, not
  audit logs, interventions, or request/response processing.

Rules files must be readable. Audit log files or directories must be writable
by the Apache process.

## Functional Test

Check the configuration:

```sh
sudo apachectl configtest
```

or:

```sh
sudo apache2ctl -t
```

For a standalone httpd:

```sh
/opt/httpd/bin/httpd -t -f /opt/httpd/conf/httpd.conf
```

Reload Apache:

```sh
sudo systemctl reload apache2
```

or:

```sh
sudo systemctl reload httpd
```

Check that the module is loaded:

```sh
apache2ctl -M 2>/dev/null | grep -i security
```

or:

```sh
httpd -M 2>/dev/null | grep -i security
```

Request test:

```sh
curl -i "http://127.0.0.1/?test=block"
```

With the example rule and `SecRuleEngine On`, `403` is expected. A request that
does not match should pass normally:

```sh
curl -i "http://127.0.0.1/?test=ok"
```

Repository smoke test:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-apache
```

Subset:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
SMOKE_CASES="phase1_header_block phase2_args_block" \
make smoke-apache
```

Inspect the Apache error log, access log, ModSecurity audit log, and, for
helper builds, the logs under `$BUILD_ROOT/logs/apache/` and
`$BUILD_ROOT/logs/apache-runtime/`.

## Troubleshooting

### `apxs` Not Found

Install the Apache development package:

```sh
sudo apt-get install -y apache2-dev
```

or, on RHEL/Fedora-style systems:

```sh
sudo dnf install -y httpd-devel
```

Check:

```sh
command -v apxs2 || command -v apxs
```

The path can be supplied explicitly to configure:

```sh
./configure --with-apxs=/usr/bin/apxs2 --with-apache=/usr/sbin/apache2
```

### Missing Apache Development Package

Missing headers such as `httpd.h`, `http_config.h`, or APR headers indicate
that the development package is missing.

```sh
apxs2 -q INCLUDEDIR
ls "$(apxs2 -q INCLUDEDIR)/httpd.h"
```

### Compiler or Linker Errors

For repository builds, inspect:

```text
$BUILD_ROOT/logs/apache/commands.txt
```

For manual builds:

```sh
make V=1
```

Typical causes include the wrong APXS, missing APR/APR-util headers, missing
libmodsecurity headers, incompatible compiler flags, or stale artifacts in a
reused build directory.

### Missing libmodsecurity Dependencies

Check:

```sh
test -f /usr/local/modsecurity/include/modsecurity/modsecurity.h
test -f /usr/local/modsecurity/lib/libmodsecurity.so
ldd /path/to/mod_security3.so
```

If `libmodsecurity.so` is not found:

```sh
sudo sh -c 'echo /usr/local/modsecurity/lib > /etc/ld.so.conf.d/modsecurity.conf'
sudo ldconfig
```

For local tests, `LD_LIBRARY_PATH` can be set.

### Module Cannot Be Loaded

Check that the path in `LoadModule` is correct, that the file exists, that
`ldd` does not show missing libraries, and that the module was built with the
matching APXS.

### Invalid Rules File

If `apachectl configtest` prints a ModSecurity rule error, check syntax, unique
`id` values, paths, read permissions, and compatibility between the rules and
the libmodsecurity version being used.

### Permission Problems

Depending on the distribution, Apache runs as `www-data`, `apache`, or another
user. Check:

```sh
namei -l /etc/apache2/modsecurity/main.conf
namei -l /var/log/apache2/modsec_audit.log
```

With SELinux:

```sh
getenforce
ausearch -m avc -ts recent
```

### Distribution Differences

Binary names, APXS names, module directories, default MPMs, systemd units, and
security profiles differ by distribution. Rely on `apxs -q ...`,
`apachectl -V`, and `apachectl -M` instead of assumed paths.

## Best Practices

- Document the Apache version, APXS path, libmodsecurity version, connector
  commit, and build command.
- Account for Apache, APR, APR-util, and APXS updates.
- Test builds in a clean environment.
- Run `apachectl configtest` or `apache2ctl -t` before every reload.
- Start with small rules before enabling a large rule set.
- Keep `SecRuleEngine DetectionOnly` and `SecRuleEngine On` deliberately
  separate.
- Inspect error logs and audit logs regularly.
- Use `make smoke-apache` to validate the project path with real HTTP requests.
