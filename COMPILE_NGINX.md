# Compile NGINX

**Language:** English | [Deutsch](COMPILE_NGINX.de.md)

## Table of Contents

- [Purpose](#purpose)
- [Status and Limits](#status-and-limits)
- [Overview: Three Paths](#overview-three-paths)
- [Path 1: Repository Smoke / Validation](#path-1-repository-smoke-validation)
- [Path 2: External Use With Distribution Packages](#path-2-external-use-with-distribution-packages)
- [Path 3: External Use From Source](#path-3-external-use-from-source)
- [Config Snippets](#config-snippets)
- [Example Configs](#example-configs)
- [Logs](#logs)
- [Troubleshooting](#troubleshooting)
- [Non-Claims](#non-claims)
- [Related Docs](#related-docs)

## Purpose

This guide is for using the NGINX connector outside this repository: provide libmodsecurity, build `ngx_http_modsecurity_module.so` against a compatible NGINX version/ABI, copy the module into an external NGINX setup, wire configuration, and run the first syntax check/reload.

## Status and Limits

The NGINX connector source lives under `connectors/nginx/`. Repository smoke evidence validates specific repository paths only. External use depends on NGINX ABI compatibility and does not prove every package, module set, or RESPONSE_BODY / Phase 4 deployment.

## Overview: Three Paths

| Path | Purpose | Main use |
| --- | --- | --- |
| Path 1: Repository smoke | Validate repository evidence | Developers / reviewers |
| Path 2: External use with packages | Use distro packages where compatible | Operators using system packages |
| Path 3: External use from source | Build ModSecurity and/or connector pieces manually | Operators needing exact version control |

## Path 1: Repository Smoke / Validation

These commands validate repository evidence. They are not the external installation procedure.

```sh
git submodule update --init --recursive
make setup-dev
BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

Optional broader repository evidence:

```sh
FORCE_ALL_CASES=1 BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx
```

## Path 2: External Use With Distribution Packages

1. Install NGINX, compatible NGINX development/source package, build tools, and libmodsecurity development files. Package names vary by distribution; this Debian/Ubuntu-style command is only an example:

   ```sh
   sudo apt-get update
   sudo apt-get install -y nginx nginx-dev build-essential libmodsecurity-dev
   ```

2. Packages may provide NGINX, NGINX development files, and libmodsecurity. The package path does **not** mean the connector module comes ready-made. `ngx_http_modsecurity_module.so` still must be built from `connectors/nginx` against a compatible NGINX version/ABI.
3. Inspect the deployed NGINX binary:

   ```sh
   nginx -V 2>&1
   ```

4. Get this repository's connector source:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

5. Build the dynamic module using matching NGINX source and compatible configure arguments:

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

6. Copy the built module and adapted configs into the target system using your module directory, service config directory, ModSecurity rules directory, and log directory:

   > Note: `install` is not a package manager command here. It copies files and can set permissions. For example, `sudo install -m 0755 file.so /target/file.so` is similar to `sudo cp file.so /target/file.so` followed by `sudo chmod 0755 /target/file.so`.

   ```sh
   sudo install -d -m 0755 <nginx-module-dir> <modsecurity-config-dir> <modsecurity-log-dir>
   sudo install -m 0755 objs/ngx_http_modsecurity_module.so <nginx-module-dir>/ngx_http_modsecurity_module.so
   sudo install -m 0644 /path/to/ModSecurity-conector/examples/nginx/modsecurity-request-only.conf <modsecurity-config-dir>/modsecurity-request-only.conf
   sudo install -m 0644 /path/to/ModSecurity-conector/examples/nginx/nginx-modsecurity-request-only.conf <nginx-service-config-dir>/modsecurity.conf
   sudo nginx -t
   sudo systemctl reload <nginx-service-name>
   ```

The module must be rebuilt whenever the NGINX binary/package changes. If the module ABI does not match NGINX, NGINX will fail to load the module.

## Path 3: External Use From Source

1. Install compiler/build prerequisites.
2. Build libmodsecurity v3 from source if packages are not suitable:

Install build prerequisites for your operating system first. Then either use the libmodsecurity ref selected by your deployment or identify the repository/framework pin before building. The following is an upstream-style example, not a repository-owned build guarantee:

```sh
git clone --depth 1 -b <modsecurity-v3-ref> https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity-v3
cd ModSecurity-v3
git submodule update --init --recursive
./build.sh
./configure --prefix=<libmodsecurity-prefix>
make -j"$(nproc)"
sudo make install
```

Replace `<modsecurity-v3-ref>` and `<libmodsecurity-prefix>` with operator-selected values. Verify upstream prerequisites and flags for your operating system.

3. Build or obtain the exact NGINX source corresponding to the deployed NGINX binary. Always inspect `nginx -V` first.
4. Configure NGINX source with `--add-dynamic-module=/path/to/ModSecurity-conector/connectors/nginx`, compatible arguments, and `--with-compat` when appropriate; then run `make modules`.
5. Install/copy `objs/ngx_http_modsecurity_module.so`, place `load_module` in the top-level NGINX config context, run `nginx -t`, then reload/restart NGINX.

## Config Snippets

```nginx
load_module modules/ngx_http_modsecurity_module.so;

modsecurity on;
modsecurity_rules_file <modsecurity-rules-file>;

proxy_pass <backend-upstream>;
```

`load_module` belongs in the top-level NGINX config context, not inside `http`, `server`, or `location`. See [examples/nginx/README.md](examples/nginx/README.md) for the explanation of these directives, placeholders, logs, and limitations.

## Example Configs

Use the files in [examples/nginx/](examples/nginx/README.md) as starting points for external configuration. They are not automatically installed by the repository and are not universal production defaults.

## Logs

Inspect the relevant deployment logs; do not treat the paths in examples as universal requirements.

- Webserver/proxy access logs.
- Webserver/proxy error logs.
- ModSecurity audit log when enabled.
- Connector decision log, if this connector/path has one.
- Sidecar/agent log, if this connector/path has one.

## Troubleshooting

Check NGINX module ABI mismatch, missing headers, missing shared libraries, wrong top-level `load_module` placement, wrong rules path, missing writable log directory, and RESPONSE_BODY assumptions beyond evidence.

## Non-Claims

- RESPONSE_BODY / Phase 4 is not promoted.
- Force-all FAIL rows are not production support.
- This guide does not prove every NGINX distro package, version, or module ABI.

## Related Docs

- [examples/nginx/README.md](examples/nginx/README.md)
- `connectors/nginx/docs/build.md`
- `connectors/nginx/docs/validation.md`

## Common SDK adoption compile checks

The NGINX connector now has compile-only/structure checks for its Common SDK
adoption layer. `make check-nginx-c17` compiles adoption-relevant NGINX and
Common objects with C17 (`-Wall -Wextra -Werror`) when local NGINX and
libmodsecurity headers are available. `make check-nginx-c23` and
`make check-nginx-future-c` are optional compiler capability checks. Missing
NGINX/libmodsecurity headers are reported as `BLOCKED` with exit 77 rather than
as runtime evidence. This is compile/structure evidence only and is not a
production, CRS, full-matrix, or runtime verification claim.

NGINX Common SDK module builds that use a copied connector source tree must set `MSCONNECTOR_COMMON_SRC` (or `CONNECTOR_COMMON_SRC` / `COMMON_SRC_ROOT`) to the repository Common source root; `MSCONNECTOR_COMMON_INC` remains the Common include root. If unset, the config only falls back to `$ngx_addon_dir/../../common/src` when that path exists.
