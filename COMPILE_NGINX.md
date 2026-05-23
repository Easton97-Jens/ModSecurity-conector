# Compile Nginx

This guide explains how to build the ModSecurity connector from this repository
as an Nginx module and how to use it in an Nginx configuration. It covers the
locally evidenced build and smoke-test path provided by the repository, and it
also includes manual build steps for environments where Nginx and
libmodsecurity are supplied separately.

## Overview

The Nginx connector lives under `connectors/nginx/`. It is an Nginx HTTP module
that passes Nginx requests and responses to libmodsecurity v3. The WAF decision
itself is made by libmodsecurity and the loaded rules; the connector provides
the Nginx integration, configuration directives, transaction creation, and
handoff of HTTP data to the ModSecurity phases.

At a high level, the build does the following:

1. Makes libmodsecurity-v3 headers and `libmodsecurity.so` available.
2. Configures the Nginx source tree with the third-party module from
   `connectors/nginx/`.
3. Compiles the connector sources from `connectors/nginx/src/`.
4. Produces either a dynamic module named `ngx_http_modsecurity_module.so` or
   an Nginx binary with the module compiled in statically.

The dynamic/static distinction matters:

- Dynamic: `./configure --add-dynamic-module=...` produces a `.so` file. That
  file is loaded later with `load_module`. This is the path evidenced by the
  repository smoke build.
- Static: `./configure --add-module=...` compiles the connector directly into
  the Nginx binary. There is no separate `load_module` line. The project
  documentation treats this path as generally possible, but as a path that must
  be validated separately.

`connectors/nginx/docs/build.md` records that the local proof-of-concept
automation uses the dynamic module build, and that supported Nginx versions
still need explicit verification.

## Prerequisites

On Debian/Ubuntu, these packages are a reasonable starting point:

```sh
sudo apt-get update
sudo apt-get install -y \
  git make gcc g++ clang \
  autoconf automake libtool pkg-config \
  curl ca-certificates tar perl python3 \
  libpcre3-dev zlib1g-dev libssl-dev \
  libxml2-dev libyajl-dev liblmdb-dev libgeoip-dev \
  libcurl4-openssl-dev
```

If your distribution provides a suitable package, you can use an installed
libmodsecurity development environment:

```sh
sudo apt-get install -y libmodsecurity-dev
```

Package names differ by distribution. On RHEL/Fedora, comparable packages are
often named `pcre-devel`, `zlib-devel`, `openssl-devel`,
`pkgconf-pkg-config`, or `mod_security`. What matters is not the exact package
name, but that the compiler, Make, Nginx build dependencies, ModSecurity
headers, and `libmodsecurity.so` are available.

The connector needs these libmodsecurity files in particular:

- `modsecurity/modsecurity.h`
- `modsecurity/transaction.h`
- either `modsecurity/rules_set.h` or `modsecurity/rules.h`, depending on the
  libmodsecurity version
- `libmodsecurity.so`

If libmodsecurity is not installed in standard paths, these variables are used
during the Nginx build:

```sh
export MODSECURITY_INC=/opt/modsecurity/include
export MODSECURITY_LIB=/opt/modsecurity/lib
```

The Nginx source must match the target Nginx version. ABI compatibility is
especially important for dynamic modules. For an existing target Nginx, check:

```sh
nginx -V 2>&1
```

This output shows the version, compiler, and configure arguments. After Nginx
updates, rebuild and retest the module.

## Prepare the Repository

After a fresh clone:

```sh
git clone <repository-url> ModSecurity-conector
cd ModSecurity-conector
git submodule update --init --recursive
```

The `modules/ModSecurity-test-Framework` submodule is required by the Makefile
targets and smoke helpers. Without the submodule, targets such as
`make smoke-nginx` will block.

Important paths:

| Path | Purpose |
| --- | --- |
| `connectors/nginx/config` | Nginx third-party module configuration and libmodsecurity detection |
| `connectors/nginx/src/` | Productive Nginx connector sources |
| `common/include/msconnector/` | Shared directive, option, and metadata headers |
| `connectors/nginx/harness/` | Runtime smoke configuration and runner |
| `modules/ModSecurity-test-Framework/ci/prepare-nginx-build.sh` | Build helper for the local dynamic Nginx module build |

The repository-provided build path is:

```sh
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

This command does more than compile the module. It builds or stages
libmodsecurity v3, materializes the Nginx connector source into
`$BUILD_ROOT/nginx-build/connector-src`, downloads Nginx sources, configures
Nginx with `--with-compat --add-dynamic-module=...`, installs a local Nginx
under `$BUILD_ROOT/nginx-runtime/nginx`, and then runs real HTTP smoke tests.

## Prepare the Nginx Source Code

For manual builds, an Nginx source tree must be available:

```sh
mkdir -p "$HOME/src"
cd "$HOME/src"
curl -LO https://nginx.org/download/nginx-1.26.3.tar.gz
tar -xzf nginx-1.26.3.tar.gz
cd nginx-1.26.3
```

If the module is being built for a distribution-provided Nginx, use the version
and configure options from `nginx -V` as the reference. At minimum, use
`--with-compat` when producing a dynamic module intended for a compatible
target Nginx.

The repository helper defaults to downloading a GitHub release. The relevant
variables come from `modules/ModSecurity-test-Framework/ci/common.sh`:

```sh
NGINX_SOURCE_MODE=github-release
NGINX_SOURCE_REPO_URL=https://github.com/nginx/nginx
NGINX_RELEASE_TAG=latest
```

For reproducible builds, replace `latest` with a concrete tag:

```sh
NGINX_RELEASE_TAG=release-1.31.0 \
REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

## Compile the Connector as a Dynamic Module

The dynamic build is the main path evidenced by the project.

### Build Through the Repository

```sh
git submodule update --init --recursive

REFRESH=1 \
BUILD_NGINX_FROM_SOURCE=1 \
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

Expected artifacts:

```text
$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx
$BUILD_ROOT/nginx-runtime/nginx/modules/ngx_http_modsecurity_module.so
$BUILD_ROOT/nginx-build/output/modsecurity/include/modsecurity/modsecurity.h
$BUILD_ROOT/nginx-build/output/modsecurity/lib/libmodsecurity.so
$BUILD_ROOT/logs/nginx/artifacts.txt
$BUILD_ROOT/logs/nginx/commands.txt
```

`commands.txt` records the commands that were executed. `artifacts.txt`
records the generated artifacts, resolved Nginx version, and paths used by the
helper.

### Manual Dynamic Build

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

Important options and variables:

| Option or variable | Meaning |
| --- | --- |
| `--add-dynamic-module=...` | Builds the connector as a dynamic Nginx module |
| `--with-compat` | Increases the chance that the module can be loaded by a compatible target Nginx |
| `MODSECURITY_INC` | Include path for the ModSecurity headers |
| `MODSECURITY_LIB` | Library path for `libmodsecurity.so` |
| `MSCONNECTOR_COMMON_INC` | Include path for `common/include`; in the monorepo layout it is also detected automatically |
| `YAJL_LIB` | Optional library path if `libyajl` is not in a standard path |
| `NGX_IGNORE_RPATH=YES` | Optional setting to avoid writing RPATH information into the result |

After `make modules`, the module normally appears here:

```text
objs/ngx_http_modsecurity_module.so
```

A typical target path:

```sh
sudo mkdir -p /etc/nginx/modules
sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/
```

## Compile the Connector Statically Into Nginx

For a static build, use `--add-module`:

```sh
export CONNECTOR_ROOT=/path/to/ModSecurity-conector
export MODSECURITY_INC=/usr/local/modsecurity/include
export MODSECURITY_LIB=/usr/local/modsecurity/lib
export MSCONNECTOR_COMMON_INC="$CONNECTOR_ROOT/common/include"

cd /path/to/nginx-source

./configure \
  --prefix=/opt/nginx-modsec-static \
  --with-http_ssl_module \
  --add-module="$CONNECTOR_ROOT/connectors/nginx"

make
sudo make install
```

Static compilation can make sense when dynamic modules are not allowed in an
environment, or when an image must ship a single Nginx binary. The downside is
that Nginx and the module must always be rebuilt together. Because the local
project path does not present static builds as the validated default, validate
this path separately with `nginx -t`, real requests, and log inspection.

## Nginx Configuration

For a dynamic module, `load_module` belongs in the main context:

```nginx
load_module /etc/nginx/modules/ngx_http_modsecurity_module.so;

events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name example.local;

        modsecurity on;
        modsecurity_rules_file /etc/nginx/modsecurity/main.conf;

        location / {
            proxy_pass http://127.0.0.1:8080;
        }
    }
}
```

A minimal rules file:

```apache
SecRuleEngine On
SecRequestBodyAccess On
SecResponseBodyAccess On

SecAuditEngine RelevantOnly
SecAuditLogType Serial
SecAuditLog /var/log/nginx/modsec_audit.log

SecRule ARGS:test "@streq block" \
  "id:100000,phase:2,deny,status:403,msg:'Nginx connector test rule'"
```

Notes:

- `modsecurity on;` enables the connector in the relevant scope.
- `modsecurity_rules_file` must be readable by the Nginx worker.
- Audit log paths must be writable by the worker.
- `modsecurity_use_error_log off;` affects only the error-log callback, not
  audit logs or interventions.
- In the Nginx connector, `modsecurity_transaction_id` may use an Nginx complex
  value.

The local harness uses `connectors/nginx/harness/nginx_smoke.conf` as its
template. It sets `load_module`, `modsecurity on;`, and
`modsecurity_rules_file` inside a generated runtime directory.

## Functional Test

Check the configuration:

```sh
nginx -t
```

For a helper build:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build"
"$BUILD_ROOT/nginx-runtime/nginx/sbin/nginx" \
  -t \
  -p "$BUILD_ROOT/nginx-runtime/nginx" \
  -c "$BUILD_ROOT/nginx-runtime/nginx/conf/nginx.conf"
```

Check version and build options:

```sh
nginx -V 2>&1
```

Check runtime dependencies:

```sh
ldd /etc/nginx/modules/ngx_http_modsecurity_module.so
```

A simple request test:

```sh
curl -i "http://127.0.0.1/?test=block"
```

With the example rule, `403` is expected. A request that does not match should
pass normally:

```sh
curl -i "http://127.0.0.1/?test=ok"
```

Repository smoke test:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
make smoke-nginx
```

Subset:

```sh
BUILD_ROOT="$HOME/.local/state/ModSecurity-conector-build" \
SMOKE_CASES="phase1_header_block phase2_args_block" \
make smoke-nginx
```

Afterwards, inspect the Nginx error log, access log, ModSecurity audit log, and
for helper builds the logs under `$BUILD_ROOT/logs/nginx/`.

## Troubleshooting

### Missing Headers or Libraries

If `connectors/nginx/config` reports that the ModSecurity library is missing,
check:

```sh
test -f "$MODSECURITY_INC/modsecurity/modsecurity.h"
test -f "$MODSECURITY_LIB/libmodsecurity.so"
```

Set the paths correctly:

```sh
export MODSECURITY_INC=/correct/include/path
export MODSECURITY_LIB=/correct/lib/path
```

### `libmodsecurity.so` Is Not Found at Runtime

Check:

```sh
ldd /etc/nginx/modules/ngx_http_modsecurity_module.so
```

Fix:

```sh
sudo sh -c 'echo /usr/local/modsecurity/lib > /etc/ld.so.conf.d/modsecurity.conf'
sudo ldconfig
```

For local tests, `LD_LIBRARY_PATH` can also be set.

### Incompatible Nginx Version

Errors such as `module is not binary compatible` mean the module and Nginx
binary do not match. Build with the same Nginx version and, as far as possible,
the same configure options as the target Nginx. Use `--with-compat` for
dynamic modules.

### Wrong Module Path

`load_module` must point to the actual `.so` file. Absolute paths are more
robust than relative paths:

```sh
ls -l /etc/nginx/modules/ngx_http_modsecurity_module.so
nginx -t
```

### `unknown directive "modsecurity"`

The module was not loaded, or the static Nginx binary does not include the
connector. For dynamic modules, `load_module` must appear before the `http`
block. For static modules, do not use a `load_module` line.

### Invalid ModSecurity Configuration

If `nginx -t` fails because of a rule, check rule syntax, unique `id` values,
file paths, read permissions, and compatibility with the libmodsecurity version
being used.

### Permission Problems

Rules files must be readable and audit logs must be writable. Check:

```sh
namei -l /etc/nginx/modsecurity/main.conf
namei -l /var/log/nginx/modsec_audit.log
```

With SELinux or AppArmor, profiles or labels may also be relevant.

### Distribution Differences

Distributions differ in prefix, module path, compiler flags, Nginx patches,
and security profiles. `nginx -V` and `nginx -T` are the most important
diagnostic commands.

## Best Practices

- Document the Nginx version, configure arguments, libmodsecurity version,
  connector commit, and build command.
- Pin `NGINX_RELEASE_TAG` and `MODSECURITY_GIT_REF` for reproducible builds.
- Rebuild the module after Nginx updates.
- Validate every configuration change with `nginx -t`.
- Test in an isolated environment with small rules first.
- Inspect error logs and audit logs after the first start.
- Use absolute paths for modules, rules files, and audit logs.
- Keep `SecRuleEngine DetectionOnly` and `SecRuleEngine On` deliberately
  separate.
- Use `make smoke-nginx` to validate the project path with real HTTP requests.
