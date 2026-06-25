# Compile Apache

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

This guide is for using the Apache connector outside this repository: build or install libmodsecurity, build `mod_security3.so` against the target Apache/APXS, copy the artifact into an external Apache/httpd setup, wire configuration, and run the first syntax check/reload.

## Status and Limits

The Apache connector source lives under `connectors/apache/`. Repository smoke evidence validates specific repository paths only. It does not prove every Apache distribution package, MPM, module layout, or RESPONSE_BODY / Phase 4 deployment.

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
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

Optional broader repository evidence:

```sh
FORCE_ALL_CASES=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

## Path 2: External Use With Distribution Packages

1. Install Apache/httpd, matching APXS/development headers, build tools, and libmodsecurity development files. Package names vary by distribution; this Debian/Ubuntu-style command is only an example:

   ```sh
   sudo apt-get update
   sudo apt-get install -y apache2 apache2-dev build-essential libmodsecurity-dev
   ```

2. Package-provided components may include Apache/httpd, APXS, headers, and libmodsecurity. `mod_security3.so` still must be built from this repository against the target APXS.
3. Get this repository's connector source:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

4. Build the connector against package-provided APXS/libmodsecurity. If you use the direct Autotools path, verify it against `connectors/apache` docs/source for your target system:

   ```sh
   cd connectors/apache
   ./autogen.sh
   ./configure --with-apxs=<target-apxs> --with-libmodsecurity=<libmodsecurity-prefix>
   make
   ```

5. Copy the built module and adapted config into the target system. Use your Apache module directory, service config directory, ModSecurity rules directory, and log directory; the placeholders below are not universal:

   > Note: `install` is not a package manager command here. It copies files and can set permissions. For example, `sudo install -m 0755 file.so /target/file.so` is similar to `sudo cp file.so /target/file.so` followed by `sudo chmod 0755 /target/file.so`.

   ```sh
   sudo install -d -m 0755 <modsecurity-config-dir> <modsecurity-log-dir>
   sudo install -m 0755 <built-mod_security3.so> <apache-module-dir>/mod_security3.so
   sudo install -m 0644 examples/apache/modsecurity-request-only.conf <modsecurity-config-dir>/modsecurity-request-only.conf
   sudo install -m 0644 examples/apache/apache-modsecurity-request-only.conf <apache-service-config-dir>/security3.conf
   sudo apachectl configtest
   sudo systemctl reload <apache-service-name>
   ```

APXS and Apache/httpd must match. If they do not, the module may build but fail to load or run correctly.

## Path 3: External Use From Source

1. Install compiler/build prerequisites and Apache/httpd APXS for the target installation.
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

3. Get this repository's connector source from GitHub or your fork:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector/connectors/apache
   ```

4. Build `mod_security3.so` with the target APXS and source-built libmodsecurity prefix. If the exact command needs adjustment for your platform, verify it against `connectors/apache/docs/build.md` and the Autotools files:

   ```sh
   ./autogen.sh
   ./configure --with-apxs=<target-apxs> --with-libmodsecurity=<libmodsecurity-prefix>
   make
   ```

5. Install/copy the built module using the placeholder install pattern from Path 2, run `apachectl configtest`, then reload/restart the target Apache service.

## Config Snippets

```apache
LoadModule security3_module <module-path>/mod_security3.so

modsecurity on
modsecurity_rules_file <modsecurity-rules-file>
```

See [examples/apache/README.md](examples/apache/README.md) for the explanation of these directives, placeholders, logs, and limitations.

## Example Configs

Use the files in [examples/apache/](examples/apache/README.md) as starting points for external configuration. They are not automatically installed by the repository and are not universal production defaults.

## Logs

Inspect the relevant deployment logs; do not treat the paths in examples as universal requirements.

- Webserver/proxy access logs.
- Webserver/proxy error logs.
- ModSecurity audit log when enabled.
- Connector decision log, if this connector/path has one.
- Sidecar/agent log, if this connector/path has one.

## Troubleshooting

Check APXS/Apache ABI mismatch, missing headers, missing shared libraries, wrong Apache config context, wrong rules path, missing writable log directory, and RESPONSE_BODY assumptions beyond evidence.

## Non-Claims

- RESPONSE_BODY / Phase 4 is not promoted.
- Force-all FAIL rows are not production support.
- This guide does not prove every Apache distro package, MPM, or module layout.

## Related Docs

- [examples/apache/README.md](examples/apache/README.md)
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`
