<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: Envoy

**Language:** English | [Deutsch](envoy.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `ext_proc` on Envoy. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, an official Envoy binary or optional Bazel build, the repository ext_proc service, its CGo/Common bridge, gRPC configuration, a local rule file, and loopback Envoy/upstream listeners.

## Connector in this repository

- [Envoy connector](../../../connectors/envoy/README.md)
- [Productive ext_proc service](../../../connectors/envoy/ext_proc/)
- [Connector configuration](../../../connectors/envoy/config/)
- [ext_proc build helper](../../../connectors/envoy/build/build_ext_proc.sh)
- [Source mapping](../../../connectors/envoy/SOURCE_MAP.json)

This is the primary connector path for this guide: connectors/envoy/. The official host documentation in the following section explains only how to provide or build the host; it does not replace the connector source.

Section 7 builds the repository-owned ext_proc service; the official Envoy documentation only explains the host binary and host configuration.

## 3. Official upstream documentation

- **Source and scope:** [Installing Envoy](https://www.envoyproxy.io/docs/envoy/latest/start/install)
  Official binary, package, and container installation choices plus version inspection. Version scope: The page is version-sensitive; use the docs matching the selected Envoy release.
- **Source and scope:** [Run Envoy](https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/run-envoy.html)
  The official version, configuration validation, and local startup commands. Version scope: Use the selected Envoy release documentation.
- **Source and scope:** [Static configuration](https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/configuration-static)
  Listener, HTTP connection manager, route, and cluster configuration used by the loopback example. Version scope: Verify field names against the selected release.
- **Source and scope:** [HTTP external processing filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/ext_proc_filter)
  The official ext_proc filter and bidirectional gRPC configuration contract. Version scope: Filter fields and semantics are release-dependent.
- **Source and scope:** [Envoy admin interface](https://www.envoyproxy.io/docs/envoy/latest/operations/admin.html)
  Loopback-only admin endpoints and their local diagnostic purpose. Version scope: Do not expose the local example as a general management interface.
- **Source and scope:** [Envoy v1.38.2 release](https://github.com/envoyproxy/envoy/releases/tag/v1.38.2)
  Official selected release page, binary asset, and checksum material. Version scope: This guide pins the binary route to v1.38.2.
- **Source and scope:** [Envoy source/Bazel guidance](https://github.com/envoyproxy/envoy/blob/v1.38.2/bazel/README.md)
  Official optional source-build guidance; it is resource-intensive and not the default route. Version scope: Use only with the selected tag and sufficient CPU, memory, and storage.



## 4. Prerequisites

Build libmodsecurity first with the shared guide. Then install the selected host's documented development tools and keep the host, connector, headers, and libraries compatible.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```

The repository ext_proc module requires the exact pinned Go 1.26 patch declared in its go.mod; verify that directive before its Section 7 build.

```sh
go version
grep -Ex "go 1\.26\.[0-9]+" "$CONNECTOR_ROOT/connectors/envoy/ext_proc/go.mod"
```

## 5. Prepare libmodsecurity v3

Build libmodsecurity v3 first with the shared guide:

[Build libmodsecurity v3](libmodsecurity.md)

The following hand-off uses the official simple-build default `/usr/local/modsecurity`. Override MODSECURITY_PREFIX, MODSECURITY_INCLUDE_DIR, or MODSECURITY_LIB_DIR only for a deliberately selected installation. It checks the header and chooses `lib64` only when `lib` lacks libmodsecurity.

```sh
export MODSECURITY_PREFIX="${MODSECURITY_PREFIX:-/usr/local/modsecurity}"
export MODSECURITY_INCLUDE_DIR="${MODSECURITY_INCLUDE_DIR:-$MODSECURITY_PREFIX/include}"
export MODSECURITY_LIB_DIR="${MODSECURITY_LIB_DIR:-$MODSECURITY_PREFIX/lib}"
if [ ! -f "$MODSECURITY_LIB_DIR/libmodsecurity.so" ] && [ -f "$MODSECURITY_PREFIX/lib64/libmodsecurity.so" ]; then
    MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib64"
fi
test -f "$MODSECURITY_INCLUDE_DIR/modsecurity/modsecurity.h"
test -f "$MODSECURITY_LIB_DIR/libmodsecurity.so"
```

## 6. Provide the host or proxy

### Simple path

Use the repository-compatible official Envoy release binary. The ext_proc service is a separate repository component and is built in Section 7.

```sh
WORKDIR="$HOME/connector-build/envoy"
```

#### Download the release binary

The official x86_64 asset is written to a local workspace and made executable.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fL "https://github.com/envoyproxy/envoy/releases/download/v1.38.2/envoy-1.38.2-linux-x86_64" -o envoy
printf "%s  %s\n" "87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899" "envoy" | sha256sum -c -
chmod 755 envoy
./envoy --version
```

### What was installed or built?

Only the official Envoy host binary is present. It does not include the repository ext_proc executable, its Common bridge, or configuration.

### Check the result

The file and version checks confirm that the intended local host binary is ready for Section 7.

```sh
test -x "$WORKDIR/envoy"
"$WORKDIR/envoy" --version
```

### Source build and integrity checks

#### Optional: build Envoy from source

A full Bazel build is resource-intensive and deliberately not part of the beginner path. Follow the [official Envoy source-build guidance](https://www.envoyproxy.io/docs/envoy/latest/start/building/local_docker_build.html) for the selected release before using it as a host override.

## 7. Build and integrate the connector

The repository ext_proc executable is the source-built component. It links the Common/libmodsecurity bridge and is not part of an official Envoy binary. The generated host configuration uses `envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor`, an HTTP/2 gRPC cluster, and a router after that filter. Build the service into an external root, then generate both configurations there.

The host path is reintroduced here only so that the connector commands can consume the Section 6 host without rebuilding it.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/envoy"
export ENVOY_BIN="$HOST_BUILD_BASE/envoy"
cd "$CONNECTOR_ROOT"
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/envoy/build/build_ext_proc.sh"
export EXT_PROC_BIN="$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"
test -x "$EXT_PROC_BIN"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/envoy/build/test_ext_proc.sh"
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep configuration and runtime files outside the Git checkout.

```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export ENVOY_CONFIG="$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.yaml"
export EXT_PROC_CONFIG="$CONNECTOR_ROOT/connectors/envoy/config/envoy-ext-proc-service.json"
export RUNTIME_ROOT="$BUILD_ROOT/envoy-ext-proc/runtime-smoke"
export EXT_PROC_RUNTIME_CONFIG="$RUNTIME_ROOT/envoy-ext-proc-runtime.conf"
export ENVOY_PORT=18080
export ENVOY_UPSTREAM_PORT=18081
export EXT_PROC_PORT=18083
export ENVOY_ADMIN_PORT=19001
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
OUTPUT_CONFIG="$ENVOY_CONFIG" LISTEN_PORT="$ENVOY_PORT" UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" EXT_PROC_PORT="$EXT_PROC_PORT" ADMIN_PORT="$ENVOY_ADMIN_PORT" sh "$CONNECTOR_ROOT/connectors/envoy/config/prepare_envoy_ext_proc_config.sh"
OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG" RULES_FILE="$RULES_FILE" EVENT_PATH="$RUNTIME_ROOT/events.jsonl" sh "$CONNECTOR_ROOT/connectors/envoy/config/prepare_envoy_ext_proc_runtime_config.sh"
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG"
"$EXT_PROC_BIN" --check-config --config "$EXT_PROC_CONFIG" --runtime-config "$EXT_PROC_RUNTIME_CONFIG"
"$ENVOY_BIN" --version
test -x "$EXT_PROC_BIN"
file "$EXT_PROC_BIN"
ldd "$EXT_PROC_BIN" | grep -F libmodsecurity | grep -Fv "not found"
grep -F "envoy.filters.http.ext_proc" "$ENVOY_CONFIG"
grep -F "request_body_mode: STREAMED" "$ENVOY_CONFIG"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. The bounded repository harness starts Envoy, ext_proc, and its upstream, then sends HTTP/1.1 allow and local denial probes through the generated `ext_proc` route. Its admin endpoint is loopback-only and used for local readiness diagnostics. Its results apply only to those observed requests.

```sh
RUNTIME_ROOT="$RUNTIME_ROOT" ENVOY_BIN="$ENVOY_BIN" RULES_FILE="$RULES_FILE" ENVOY_SMOKE_PORT="$ENVOY_PORT" ENVOY_UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" ENVOY_EXT_PROC_PORT="$EXT_PROC_PORT" ENVOY_ADMIN_PORT="$ENVOY_ADMIN_PORT" EXT_PROC_RUNTIME_CONFIG="$EXT_PROC_RUNTIME_CONFIG" sh "$CONNECTOR_ROOT/connectors/envoy/harness/run_envoy_ext_proc_runtime.sh"
# The bounded runner regenerates its run-local Envoy and ext_proc runtime files, then starts Envoy, ext_proc, and a loopback upstream, sends local HTTP/1.1 requests, and stops them.
```

## 11. Package-assisted path

Status: `package-assisted source build`. Package queries deliberately precede installation. Use only the line matching the distribution.

Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package.

```sh
apt-cache search envoy
dnf search envoy
envoy --version 2>/dev/null || true
```

Packages can provide a host binary or build dependencies, but they do not include the repository ext_proc service or its Common/libmodsecurity bridge. Validate a package binary separately and retain the source-built service.

## 12. Repository-controlled test path

This section follows the manual build. The targets automate and test the build and integration steps described above; they do not replace their technical documentation. Exit `77` means a deliberately blocked prerequisite, and one successful target is not a broader release claim.

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
mkdir -p "$VERIFIED_RUN_PARENT"
cd "$VERIFIED_RUN_PARENT"
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
git switch feature/all-connectors-no-crs-baseline
git submodule update --init --recursive
make check-framework
make prepare-runtime-components
make build-envoy
make check-config-envoy
make start-smoke-envoy
make runtime-smoke-envoy
run_id="envoy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
```

## 13. Update and rebuild

Before an update, recheck the linked upstream documentation, release version, and configure/build options. Then repeat every affected host, connector, ABI, and local HTTP test.

```sh
git -C "$CONNECTOR_ROOT" pull --ff-only
git -C "$CONNECTOR_ROOT" submodule update --init --recursive
# Rebuild the selected host and connector with the commands above.
```

## 14. Uninstall and cleanup

Do not copy files indiscriminately to `/usr/lib` and do not remove global directories. A user prefix does not need `sudo`. Remove evidence or logs only after deliberate review.

```sh
test ! -e "$HOME/connector-build/envoy" || find "$HOME/connector-build/envoy" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Common: for missing headers or libraries, return to the shared guide's advanced section and check the deliberately selected prefix and pkg-config output. For an ABI failure, rebuild host, headers, and connector from the same selected source set.

An official Envoy binary is only the host. If validation fails, check the generated ext_proc YAML, gRPC port ownership, the ext_proc service configuration, and the libmodsecurity loader path; do not replace ext_proc with the separate ext_authz compatibility service.

## 16. Variables and placeholders

| Variable/placeholder | Meaning |
| --- | --- |
| CONNECTOR_ROOT | Git top level of this checkout; connector scripts are called from it. |
| RULES_FILE | Local test-rule file, not a CRS rule file. |
| MODSECURITY_PREFIX | libmodsecurity installation prefix. The official simple-build default is /usr/local/modsecurity. |
| MODSECURITY_INCLUDE_DIR | libmodsecurity header directory selected from MODSECURITY_PREFIX. |
| MODSECURITY_LIB_DIR | libmodsecurity shared-library directory selected from MODSECURITY_PREFIX; the hand-off detects lib64 when needed. |
| VERIFIED_RUN_PARENT | External parent for a fresh repository-test checkout and its test artifacts. |
| run_id | Unique identifier for one repository-controlled full-lifecycle run. |
| NO_CRS_RUN_ID | Exported full-lifecycle identifier for the following Make invocation; it keeps evidence and runtime data separated. |
| HOST_BUILD_BASE | Connector-specific external directory for sources, builds, configuration, and local logs. |
| BUILD_ROOT | External build and runtime root for repository-owned connector components. |
| ENVOY_BIN | Verified Envoy executable. |
| EXT_PROC_BIN | Repository-built ext_proc service executable. |
| ENVOY_CONFIG | Generated loopback Envoy configuration. |
| EXT_PROC_CONFIG | Repository ext_proc service configuration validated with the generated runtime configuration. |
| EXT_PROC_RUNTIME_CONFIG | Generated Common runtime configuration for ext_proc. |
| OUTPUT_CONFIG | Output path consumed by one configuration-materialization command. |
| EVENT_PATH | Absolute local event-log path passed to the ext_proc runtime configuration writer. |
| RUNTIME_ROOT | External ephemeral root used by the bounded Envoy runtime harness. |
| LISTEN_PORT | Loopback listener port passed to the Envoy configuration materializer. |
| UPSTREAM_PORT | Loopback upstream port passed to the Envoy configuration materializer. |
| ADMIN_PORT | Loopback admin port passed to the Envoy configuration materializer. |
| ENVOY_PORT | Loopback Envoy listener port. |
| ENVOY_UPSTREAM_PORT | Loopback upstream port used by the test. |
| EXT_PROC_PORT | Loopback gRPC ext_proc service port. |
| ENVOY_SMOKE_PORT | Loopback listener port passed to the bounded repository Envoy harness. |
| ENVOY_EXT_PROC_PORT | Loopback gRPC port passed to the bounded repository Envoy harness. |
| ENVOY_ADMIN_PORT | Loopback Envoy admin port. |
| WORKDIR | External Envoy binary workspace. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
