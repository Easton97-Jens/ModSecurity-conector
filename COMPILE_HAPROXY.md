# Compile HAProxy

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

This guide is for using the HAProxy SPOE/SPOP ModSecurity path outside this repository: provide HAProxy, build `haproxy-modsecurity-spoa`, wire HAProxy SPOE config, start the SPOA process with an operator-provided process manager, and run the first config check/start.

## Status and Limits

HAProxy itself may be distro-provided or locally built. This repository builds the `haproxy-modsecurity-spoa` process and libmodsecurity binding checks. RESPONSE_BODY remains bounded runtime evidence only.

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
make smoke-haproxy
```

Optional HAProxy repository validation:

```sh
make test-haproxy-no-crs
make test-haproxy-with-crs
```

## Path 2: External Use With Distribution Packages

1. Install HAProxy with SPOE/SPOP support, build tools, and libmodsecurity headers/libraries. Package names vary by distribution.
2. Packages may provide HAProxy and libmodsecurity. `haproxy-modsecurity-spoa` still must be built from `connectors/haproxy`.
3. Get this repository's connector source:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

4. Build the binding and SPOA process:

   ```sh
   make prepare-runtime-components
   make -C connectors/haproxy build-modsecurity-binding
   make -C connectors/haproxy build-spoa-runtime
   make -C connectors/haproxy self-test-modsecurity-binding
   make -C connectors/haproxy self-test-spoa-runtime
   ```

5. Copy the built SPOA binary and adapted configs into external runtime/config/log directories:

   > Note: `install` is not a package manager command here. It copies files and can set permissions. For example, `sudo install -m 0755 file.so /target/file.so` is similar to `sudo cp file.so /target/file.so` followed by `sudo chmod 0755 /target/file.so`.

   ```sh
   sudo install -d -m 0755 <haproxy-config-dir> <modsecurity-config-dir> <haproxy-modsecurity-log-dir>
   sudo install -m 0755 <built-haproxy-modsecurity-spoa> <runtime-binary-dir>/haproxy-modsecurity-spoa
   sudo install -m 0644 examples/haproxy/spoe-modsecurity.conf <haproxy-config-dir>/spoe-modsecurity.conf
   sudo install -m 0644 examples/haproxy/modsecurity-agent.conf <haproxy-config-dir>/modsecurity-agent.conf
   sudo install -m 0644 examples/haproxy/haproxy-request-only.cfg <haproxy-config-dir>/haproxy.cfg
   sudo haproxy -c -f <haproxy-config-dir>/haproxy.cfg
   sudo systemctl reload <haproxy-service-name>
   ```

HAProxy connects to the SPOA process through SPOE/SPOP. Start/restart the SPOA with an operator-provided service unit or process manager; this repository does not install one.

## Path 3: External Use From Source

1. Install compiler/build prerequisites and HAProxy if you are not using a package.
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

3. Clone this repository and build the binding/SPOA process with the same `make -C connectors/haproxy ...` commands shown in Path 2.
4. Install/copy the SPOA binary and configs using the placeholder install pattern from Path 2.
5. Validate HAProxy with `haproxy -c -f <haproxy-config>`. Start the SPOA binary with the configuration method supported by the built binary. The source supports `--config PATH`, so an operator-style invocation can be:

   ```sh
   <runtime-binary-dir>/haproxy-modsecurity-spoa --config <haproxy-config-dir>/modsecurity-agent.conf
   ```

## Config Snippets

```haproxy
filter spoe engine modsecurity config <spoe-config>

http-request send-spoe-group modsecurity request-check
http-request deny if { var(txn.modsec.blocked) -m bool }

backend <spoa-backend>
    mode spop
    server spoa <spoa-host>:<spoa-port>
```

Agent config shape:

```text
listen <spoa-host>:<spoa-port>
rules-file <modsecurity-rules-file>
decision-log <decision-log-path>
audit-log <audit-log-path>
```

See [examples/haproxy/README.md](examples/haproxy/README.md) for the explanation of these directives, placeholders, logs, and limitations.

## Example Configs

Use the files in [examples/haproxy/](examples/haproxy/README.md) as starting points for external configuration. They are not automatically installed by the repository and are not universal production defaults.

## Logs

Inspect the relevant deployment logs; do not treat the paths in examples as universal requirements.

- Webserver/proxy access logs.
- Webserver/proxy error logs.
- ModSecurity audit log when enabled.
- Connector decision log, if this connector/path has one.
- Sidecar/agent log, if this connector/path has one.

## Troubleshooting

Check missing headers, missing shared libraries, wrong HAProxy SPOE config, wrong SPOP backend address, missing sidecar/SPOA process, wrong rules path, missing writable log directory, and RESPONSE_BODY assumptions beyond evidence.

## Non-Claims

- RESPONSE_BODY / Phase 4 is not promoted.
- Force-all FAIL rows are not production support.
- This repository does not provide a systemd service unit for the SPOA process.

## Related Docs

- [examples/haproxy/README.md](examples/haproxy/README.md)
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`
