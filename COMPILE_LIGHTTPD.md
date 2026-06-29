# Compile Lighttpd

**Language:** English | [Deutsch](COMPILE_LIGHTTPD.de.md)

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

This guide is for using the Lighttpd runtime path outside this repository with an operator-provided sidecar_proxy decision service/sidecar and external configuration.

## Status and Limits

Lighttpd may be operator-provided or built through the repository helper. There is no native Lighttpd ModSecurity module here; external use is `sidecar_proxy` / Phase 1.

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
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
```

Optional repository evidence:

```sh
make smoke-lighttpd-modsecurity
make smoke-lighttpd-crs
```

## Path 2: External Use With Distribution Packages

1. Install or provide the Lighttpd runtime binary through your distribution, vendor package, container image, or deployment tooling. Package names and service names vary by distribution.
2. Provide a reachable sidecar_proxy decision service/sidecar. If the service uses libmodsecurity, install compatible libmodsecurity headers/libraries or runtime packages.
3. Get this repository for example configs and smoke references:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

4. Adapt the example config for your listener, backend, decision service URL/address, rules directory, CRS directory, runtime directory, and log directory.
5. Run the first syntax check/start with operator-selected binary placeholders:

   ```sh
   <lighttpd-bin> -tt -f examples/lighttpd/lighttpd-sidecar-proxy.conf
   <lighttpd-bin> -D -f examples/lighttpd/lighttpd-sidecar-proxy.conf
   ```

6. Inspect runtime logs, decision-service logs, and ModSecurity audit/decision logs when the backend supports them.

## Path 3: External Use From Source

Source-based external use may use the pinned Lighttpd runtime build helper shown in Path 1/2, or an operator-built compatible Lighttpd. It is still a sidecar_proxy path, not a native connector. If the sidecar backend uses libmodsecurity, build libmodsecurity as needed.

If your decision backend uses libmodsecurity and packages are not suitable, build libmodsecurity v3 from source:

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

Then build or start your operator-provided decision service/sidecar, adapt the example config, run the first syntax check/start from Path 2, and inspect logs.

## Config Snippets

```yaml
server.modules += ("mod_proxy")
proxy.server = (
  "" => (("host" => "<sidecar-or-backend-host>", "port" => <port>))
)
```

See [examples/lighttpd/README.md](examples/lighttpd/README.md) for the explanation of these directives, placeholders, logs, and limitations.

## Example Configs

Use the files in [examples/lighttpd/README.md](examples/lighttpd/README.md) as starting points for external configuration. They are not automatically installed by the repository and are not universal production defaults.

## Logs

Inspect the relevant deployment logs; do not treat the paths in examples as universal requirements.

- Webserver/proxy access logs.
- Webserver/proxy error logs.
- ModSecurity audit log when enabled.
- Connector decision log, if this connector/path has one.
- Sidecar/agent log, if this connector/path has one.

## Troubleshooting

Check missing runtime binary, missing sidecar/auth/decision service, wrong backend address, missing shared libraries, wrong rules path, missing writable log directory, and response-body assumptions beyond evidence.

## Non-Claims

- Lighttpd is not production-ready proof here.
- This repository does not provide a native Lighttpd ModSecurity integration here.
- The current path is `sidecar_proxy` / Phase 1.
- FastCGI/SCGI/mod_magnet/Lua are not implemented here.
- RESPONSE_BODY / Phase 4 is not promoted.
- Force-all FAIL rows are not production support.

## Related Docs

- [examples/lighttpd/README.md](examples/lighttpd/README.md)
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
