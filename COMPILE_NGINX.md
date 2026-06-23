# Compile NGINX

## Inhaltsverzeichnis

- [Purpose](#purpose)
- [Current Status / Supported Claim](#current-status-supported-claim)
- [External Use Overview](#external-use-overview)
- [Components Needed Outside This Repository](#components-needed-outside-this-repository)
- [Option A: Use Distribution Packages Where Compatible](#option-a-use-distribution-packages-where-compatible)
- [Option B: Build libmodsecurity v3 From Source](#option-b-build-libmodsecurity-v3-from-source)
- [Build / Prepare This Connector Or Runtime Path](#build-prepare-this-connector-or-runtime-path)
- [Install The Built Artifact Into An External System](#install-the-built-artifact-into-an-external-system)
- [Wire Configuration](#wire-configuration)
- [Start / Reload / Restart](#start-reload-restart)
- [Logs And Runtime Evidence In A Real Deployment](#logs-and-runtime-evidence-in-a-real-deployment)
- [Example Configs](#example-configs)
- [Optional Repository Validation](#optional-repository-validation)
- [Troubleshooting](#troubleshooting)
- [Non-Claims / Limits](#non-claims-limits)
- [Related Docs](#related-docs)

## Purpose

Explain how to build and install the repository-owned NGINX dynamic module into an external NGINX installation.

## Current Status / Supported Claim

The NGINX connector is adapter-owned source under `connectors/nginx/`. Repository evidence covers documented smoke paths; external operators must match the deployed NGINX ABI.

## External Use Overview

External use requires libmodsecurity v3, the exact deployed NGINX version/configure compatibility, a dynamic module build using `connectors/nginx`, installation of `ngx_http_modsecurity_module.so`, top-level `load_module` wiring, rules/config, and NGINX reload.

## Components Needed Outside This Repository

- Target NGINX runtime.
- Compatible NGINX source tree for the deployed binary.
- Compatible NGINX configure arguments, including `--with-compat` when appropriate.
- libmodsecurity v3 headers and libraries.
- `ngx_http_modsecurity_module.so` built from `connectors/nginx`.
- ModSecurity rules, optional CRS, and writable logs.

## Option A: Use Distribution Packages Where Compatible

Debian/Ubuntu-style example only; package names and ABI compatibility vary by distribution:

```sh
sudo apt-get update
sudo apt-get install -y nginx nginx-dev build-essential libmodsecurity-dev
```

Use equivalent distro-specific package names elsewhere. This does not guarantee that the packaged `nginx-dev` source/configure options match your running NGINX.

## Option B: Build libmodsecurity v3 From Source

This repository's local smoke flow prepares libmodsecurity through framework helpers and pinned variables. For an external deployment, the following is a standard upstream-style example, not a repository-owned guarantee. Verify the selected `<modsecurity-v3-ref>`, dependencies, and flags against your operating system and the upstream ModSecurity documentation before use.

```sh
git clone --depth 1 -b <modsecurity-v3-ref> https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity-v3
cd ModSecurity-v3
git submodule update --init --recursive
./build.sh
./configure --prefix=/usr/local/modsecurity
make -j"$(nproc)"
sudo make install
```

Replace `<modsecurity-v3-ref>` with the ref chosen by your deployment or with the repository/framework pin after you have verified it in the framework source. If your distribution provides a compatible `libmodsecurity-dev`, you may not need this source build.

## Build / Prepare This Connector Or Runtime Path

Inspect the deployed NGINX version and configure arguments:

```sh
nginx -V 2>&1
```

Use the exact deployed NGINX version and compatible configure arguments. Example external module build flow:

```sh
NGINX_VERSION=<version-from-nginx-V>
curl -LO "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz"
tar xf "nginx-${NGINX_VERSION}.tar.gz"
cd "nginx-${NGINX_VERSION}"

./configure --with-compat \
  --add-dynamic-module=/path/to/ModSecurity-conector/connectors/nginx \
  <other-compatible-nginx-configure-args>

make modules
```

Replace `<other-compatible-nginx-configure-args>` with arguments compatible with the deployed binary. If the module ABI does not match NGINX, NGINX will fail to load the module. Rebuild the module whenever the NGINX binary/package changes.

## Install The Built Artifact Into An External System

```sh
sudo install -d -m 0755 /usr/lib/nginx/modules
sudo install -m 0755 objs/ngx_http_modsecurity_module.so /usr/lib/nginx/modules/ngx_http_modsecurity_module.so
sudo install -d -m 0755 /etc/modsecurity /var/log/modsecurity
sudo install -m 0644 examples/nginx/modsecurity-request-only.conf /etc/modsecurity/modsecurity-request-only.conf
sudo install -m 0644 examples/nginx/nginx-modsecurity-request-only.conf /etc/nginx/conf.d/modsecurity.conf
```

Adjust paths for distributions using a different module directory or configuration include layout.

## Wire Configuration

`load_module modules/ngx_http_modsecurity_module.so;` must be in the top-level NGINX config context, not inside `http`, `server`, or `location`. Use `modsecurity on;` and `modsecurity_rules_file` in the intended scope.

## Start / Reload / Restart

```sh
sudo nginx -t
sudo systemctl reload nginx
```

Replacing the module may require a restart depending on package/process policy.

## Logs And Runtime Evidence In A Real Deployment

Check NGINX error/access logs and ModSecurity audit logs. Preserve `nginx -V` output, module build commands, module path, libmodsecurity path, and rules file.

## Example Configs

Use the files in [examples/nginx/](examples/nginx/README.md) as starting points for external configuration. They are not automatically installed by the repository.

## Optional Repository Validation

These commands validate repository evidence. They are not the external installation procedure.

```sh
git submodule update --init --recursive
make setup-dev
make lint
git diff --check
```
```sh
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
FORCE_ALL_CASES=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

## Troubleshooting

Check dynamic module ABI mismatch, missing top-level `load_module`, missing libmodsecurity shared library at runtime, wrong rules path, NGINX worker permissions, and CRS include paths.

## Non-Claims / Limits

- RESPONSE_BODY / Phase 4 is not promoted by this guide.
- Force-all FAIL rows are not production support.
- The repository does not prove every NGINX version, package, or module ABI.

## Related Docs

- [examples/nginx/README.md](examples/nginx/README.md)
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`
