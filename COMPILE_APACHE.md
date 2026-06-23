# Compile Apache

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

Explain how to use the repository-owned Apache connector source in an external Apache/httpd installation without claiming that every distribution layout or MPM has been proven.

## Current Status / Supported Claim

The Apache connector is adapter-owned source under `connectors/apache/`. Repository evidence covers the documented smoke paths, not every external Apache package, MPM, module set, or RESPONSE_BODY deployment.

## External Use Overview

External use has four parts: provide libmodsecurity v3, build `mod_security3.so` from `connectors/apache` against the target Apache APXS, copy the module and ModSecurity rules/config into the external Apache installation, then validate and reload Apache.

## Components Needed Outside This Repository

- Target Apache/httpd runtime.
- Matching Apache development headers and APXS from that target installation.
- Compatible libmodsecurity v3 headers and libraries.
- `mod_security3.so` built from this repository's `connectors/apache` source.
- ModSecurity rules, optional CRS, writable audit/error log locations, and Apache configuration snippets.

## Option A: Use Distribution Packages Where Compatible

Debian/Ubuntu-style example only; package names and module paths differ by distribution:

```sh
sudo apt-get update
sudo apt-get install -y apache2 apache2-dev build-essential libmodsecurity-dev
```

Use equivalent packages for RHEL/Fedora/httpd systems. Compatibility must be verified against the target Apache/APXS and libmodsecurity ABI.

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

The repository's verified build/evidence flow is smoke-oriented. If no direct external install target is available, use the Apache connector Autotools/APXS inputs directly and treat the exact output path as something the operator must locate after build:

```sh
cd /path/to/ModSecurity-conector/connectors/apache
./autogen.sh
./configure --with-apxs=/usr/bin/apxs --with-libmodsecurity=/usr/local/modsecurity
make
```

Repository evidence flow with an external APXS/httpd can also be used to prove a local build path, but it is not itself an install step:

```sh
APXS=/usr/bin/apxs APACHE_HTTPD=/usr/sbin/apache2 MODSECURITY_APACHE_SOURCE_DIR=/path/to/ModSecurity-conector/connectors/apache make smoke-apache
```

## Install The Built Artifact Into An External System

Replace `<built-mod_security3.so>` with the module actually built for the target Apache/APXS ABI:

```sh
sudo install -d -m 0755 /etc/modsecurity /var/log/modsecurity
sudo install -m 0755 <built-mod_security3.so> /usr/lib/apache2/modules/mod_security3.so
sudo install -m 0644 examples/apache/modsecurity-request-only.conf /etc/modsecurity/modsecurity-request-only.conf
sudo install -m 0644 examples/apache/apache-modsecurity-request-only.conf /etc/apache2/mods-available/security3.conf
```

Paths differ on RHEL/Fedora/httpd systems; use the module directory, config directory, and log directory for your target installation.

## Wire Configuration

Load `mod_security3.so` through the target Apache module mechanism and point the connector at `/etc/modsecurity/modsecurity-request-only.conf` or your adapted rules file. Keep request-only mode as the conservative baseline.

## Start / Reload / Restart

```sh
sudo apachectl configtest
sudo systemctl reload apache2
```

Use the correct service name for your distribution. Replacing the module or libmodsecurity may require a full restart according to local policy.

## Logs And Runtime Evidence In A Real Deployment

Check Apache error/access logs and the ModSecurity audit log configured by the rules file. Preserve the exact module build path, APXS path, libmodsecurity path, Apache version, and rules file used for incident review.

## Example Configs

Use the files in [examples/apache/](examples/apache/README.md) as starting points for external configuration. They are not automatically installed by the repository.

## Optional Repository Validation

These commands validate repository evidence. They are not the external installation procedure.

```sh
git submodule update --init --recursive
make setup-dev
make lint
git diff --check
```
```sh
BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
FORCE_ALL_CASES=1 BUILD_HTTPD_FROM_SOURCE=1 make smoke-apache
```

## Troubleshooting

Check APXS/httpd mismatches, missing libmodsecurity headers/libraries, wrong module directory, unwritable audit logs, and CRS include paths.

## Non-Claims / Limits

- RESPONSE_BODY / Phase 4 is not promoted by this guide.
- Force-all FAIL rows are not production support.
- The repository does not prove every distro Apache package, MPM, or module layout.

## Related Docs

- [examples/apache/README.md](examples/apache/README.md)
- `connectors/apache/docs/build.md`
- `connectors/apache/docs/validation.md`
