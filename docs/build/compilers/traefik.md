<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: Traefik

**Language:** English | [Deutsch](traefik.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-middleware` on Traefik. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, Traefik, the repository native Go middleware, the C/C++ engine service, Common/libmodsecurity, a private Unix-domain socket, static and dynamic File Provider configuration, and loopback HTTP traffic.

## Connector in this repository

- [Traefik connector](../../../connectors/traefik/README.md)
- [Native middleware source](../../../connectors/traefik/native_middleware/)
- [Engine-service sources](../../../connectors/traefik/src/)
- [Native middleware builder](../../../connectors/traefik/build/build-native-middleware.sh)
- [Engine-service builder](../../../connectors/traefik/build/build-engine-service.sh)
- [Source mapping](../../../connectors/traefik/SOURCE_MAP.json)
- [Native middleware static configuration](../../../connectors/traefik/config/traefik-native-middleware-static.yaml)
- [Native middleware dynamic configuration](../../../connectors/traefik/config/traefik-native-middleware-dynamic.yaml)

This is the primary connector path for this guide: connectors/traefik/. The official host documentation in the following section explains only how to provide or build the host; it does not replace the connector source.

Section 7 builds the repository native middleware and its engine service; the official Traefik material only documents the host.

## 3. Official upstream documentation

- **Source and scope:** [Traefik Getting Started](https://doc.traefik.io/traefik/getting-started/)
  Official installation choices, entry points, routers, services, and safe local startup context. Version scope: Confirm the documentation version for the selected Traefik release.
- **Source and scope:** [Building and Testing](https://doc.traefik.io/traefik/contributing/building-testing/)
  Official source checkout, Go/tooling, build, and test workflow. Version scope: The required Go version is defined by the selected release's `go.mod`.
- **Source and scope:** [Traefik v3.7 configuration overview](https://doc.traefik.io/traefik/v3.7/getting-started/configuration-overview/)
  The distinction between static installation configuration and dynamic routing configuration. Version scope: Use one static configuration method and recheck it for another release.
- **Source and scope:** [Traefik v3.7 EntryPoints](https://doc.traefik.io/traefik/v3.7/reference/install-configuration/entrypoints/)
  Static loopback entry-point configuration. Version scope: Field names are release-specific.
- **Source and scope:** [Traefik v3.7 File Provider](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/other-providers/file/)
  Dynamic File Provider routers, middleware, and services. Version scope: Recheck the selected version before using another release.
- **Source and scope:** [Traefik v3.7 health check](https://doc.traefik.io/traefik/v3.7/reference/install-configuration/observability/healthcheck/)
  The loopback ping endpoint used to confirm local host startup. Version scope: Do not enable an insecure dashboard for this local check.
- **Source and scope:** [Traefik v3.7.5 release](https://github.com/traefik/traefik/releases/tag/v3.7.5)
  Official fixed release material and checksum source. Version scope: This guide selects v3.7.5 as the repository-compatible host input.
- **Source and scope:** [Traefik v3.7.5 source](https://github.com/traefik/traefik/tree/v3.7.5)
  Official selected source tree; its go.mod defines the required host Go version. Version scope: The host's Go requirement is distinct from the repository middleware module's requirement.



## 4. Prerequisites

Build libmodsecurity first with the shared guide. Then install the selected host's documented development tools and keep the host, connector, headers, and libraries compatible.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```

The repository native middleware module requires the exact pinned Go 1.26 patch declared in its go.mod; this differs from the optional Traefik-v3.7.5 host-source requirement in Section 6.

```sh
go version
grep -Ex "go 1\.26\.[0-9]+" "$CONNECTOR_ROOT/connectors/traefik/native_middleware/go.mod"
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

Use the repository-compatible official Traefik release binary. Native middleware and the engine service remain separate Section 7 components.

```sh
WORKDIR="$HOME/connector-build/traefik"
VERSION="3.7.5"
```

#### Download and unpack Traefik

The official linux_amd64 release archive contains the host binary; no repository middleware is built here.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_linux_amd64.tar.gz"
curl -fLO "https://github.com/traefik/traefik/releases/download/v${VERSION}/traefik_v${VERSION}_checksums.txt"
grep "traefik_v${VERSION}_linux_amd64.tar.gz" "traefik_v${VERSION}_checksums.txt" | sha256sum -c -
tar -xzf "traefik_v${VERSION}_linux_amd64.tar.gz"
```

### What was installed or built?

The release archive provides only the Traefik host binary. The repository native middleware, CGo/Common bridge, and UDS engine service are built later.

### Check the result

These checks identify the extracted host binary before the connector build starts.

```sh
test -x "$WORKDIR/traefik"
"$WORKDIR/traefik" version
```

### Source build and integrity checks

#### Optional: build Traefik from source

Traefik v3.7.5's selected source declares Go 1.25.0 in go.mod; check that exact requirement before cloning it. This path builds only the Traefik host; the repository middleware and engine still belong to Section 7.

```sh
go version
git clone https://github.com/traefik/traefik.git "$WORKDIR/traefik-source"
cd "$WORKDIR/traefik-source"
git checkout --detach "v$VERSION"
grep -E "^go " go.mod
grep -Fx "go 1.25.0" go.mod
git rev-parse HEAD
```

#### Build the Traefik source host

The official build command and version output confirm the source-host result. The repository middleware and engine remain Section 7 work.

```sh
cd "$WORKDIR/traefik-source"
make binary
export TRAEFIK_BIN="$WORKDIR/traefik-source/dist/traefik"
"$WORKDIR/traefik-source/dist/traefik" version
```

## 7. Build and integrate the connector

A standard Traefik binary does not include the native ModSecurity middleware or the persistent engine service. Section 7 compiles and tests the repository Go middleware package, then builds the C/C++ service outside this checkout; Section 8 stages the plugin source for the local run. The engine socket must be private to the local run and must not be reused as a shared system endpoint.

The host path is reintroduced here only so that the connector commands can consume the Section 6 host without rebuilding it.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/traefik"
export TRAEFIK_BIN="${TRAEFIK_BIN:-$HOST_BUILD_BASE/traefik}"
cd "$CONNECTOR_ROOT"
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$BUILD_ROOT/traefik-native-middleware"
export TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$BUILD_ROOT/traefik-engine-service"
export TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR/traefik-engine-service"
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-native-middleware.sh" build
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-native-middleware.sh" test
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-engine-service.sh" build
test -x "$TRAEFIK_ENGINE_SERVICE_BIN"
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh "$CONNECTOR_ROOT/connectors/traefik/build/build-engine-service.sh" test
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep configuration and runtime files outside the Git checkout.

The configuration deliberately uses only loopback entry points and does not enable an insecure dashboard or API. Treat any dashboard or administration endpoint as optional and secure it separately for a real deployment.

```sh
export TRAEFIK_RUNTIME_ROOT="$BUILD_ROOT/traefik-native-runtime-$(date -u +%Y%m%dT%H%M%SZ)"
export RULES_FILE="$TRAEFIK_RUNTIME_ROOT/traefik-native-rules.conf"
export TRAEFIK_STATIC_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-static.yaml"
export TRAEFIK_DYNAMIC_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-dynamic.yaml"
export TRAEFIK_ENGINE_CONFIG="$TRAEFIK_RUNTIME_ROOT/traefik-engine.conf"
export TRAEFIK_SOCKET_DIR="$(mktemp -d /tmp/msconnector-traefik-uds.XXXXXX)"
chmod 700 "$TRAEFIK_SOCKET_DIR"
export TRAEFIK_ENGINE_SOCKET="$TRAEFIK_SOCKET_DIR/engine.sock"
test "${#TRAEFIK_ENGINE_SOCKET}" -lt 108
export TRAEFIK_PORT=18080
export TRAEFIK_UPSTREAM_PORT=18081
export TRAEFIK_PING_PORT=18082
export TRAEFIK_PLUGIN_MODULE="github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware"
export TRAEFIK_PLUGIN_SOURCE="$TRAEFIK_RUNTIME_ROOT/plugins-local/src/$TRAEFIK_PLUGIN_MODULE"
mkdir -p "$TRAEFIK_PLUGIN_SOURCE" "$TRAEFIK_RUNTIME_ROOT/logs"
cp -a "$CONNECTOR_ROOT/connectors/traefik/native_middleware/." "$TRAEFIK_PLUGIN_SOURCE/"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_HEADERS:X-Modsec-Smoke "@streq block" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$TRAEFIK_STATIC_CONFIG" <<EOF
entryPoints:
  web:
    address: "127.0.0.1:$TRAEFIK_PORT"
  health:
    address: "127.0.0.1:$TRAEFIK_PING_PORT"
providers:
  file:
    filename: "$TRAEFIK_DYNAMIC_CONFIG"
    watch: false
ping:
  entryPoint: health
experimental:
  localPlugins:
    modsecurityNative:
      moduleName: $TRAEFIK_PLUGIN_MODULE
      settings:
        envs: []
EOF
cat > "$TRAEFIK_DYNAMIC_CONFIG" <<EOF
http:
  routers:
    native:
      entryPoints: [web]
      rule: "PathPrefix(`/`)"
      middlewares: [native]
      service: upstream
  middlewares:
    native:
      plugin:
        modsecurityNative:
          maxHeaderCount: 128
          maxHeaderBytes: 65536
          maxRequestChunkBytes: 32768
          maxResponseChunkBytes: 32768
          transactionIDHeader: X-Request-Id
          engineMode: uds
          engineSocketPath: $TRAEFIK_ENGINE_SOCKET
  services:
    upstream:
      loadBalancer:
        servers:
          - url: http://127.0.0.1:$TRAEFIK_UPSTREAM_PORT
EOF
cat > "$TRAEFIK_ENGINE_CONFIG" <<EOF
enabled=on
rules_file=$RULES_FILE
transaction_id_header=x-request-id
request_body_mode=streaming
response_body_mode=streaming
request_body_limit=4096
response_body_limit=4096
body_limit_action=reject
phase4_mode=safe
default_block_status=403
default_error_status=500
use_error_log=off
event_path=$TRAEFIK_RUNTIME_ROOT/logs/traefik-events.jsonl
max_header_count=100
max_header_name_size=256
max_header_value_size=8192
max_total_header_bytes=65536
max_event_json_bytes=16384
EOF
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
( cd "$TRAEFIK_RUNTIME_ROOT" && "$TRAEFIK_BIN" check --configFile="$TRAEFIK_STATIC_CONFIG" )
"$TRAEFIK_ENGINE_SERVICE_BIN" --check-config --config "$TRAEFIK_ENGINE_CONFIG"
"$TRAEFIK_BIN" version
test -f "$TRAEFIK_STATIC_CONFIG"
test -f "$TRAEFIK_DYNAMIC_CONFIG"
test -x "$TRAEFIK_ENGINE_SERVICE_BIN"
ldd "$TRAEFIK_ENGINE_SERVICE_BIN" | grep -F libmodsecurity | grep -Fv "not found"
grep -F "modsecurityNative" "$TRAEFIK_STATIC_CONFIG"
grep -F "engineSocketPath" "$TRAEFIK_DYNAMIC_CONFIG"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. `/ping` confirms host startup; the ordinary `/native` request exercises the private UDS route, and the `X-Modsec-Smoke: block` test header triggers the local 403 rule. These observations do not establish a broader claim.

```sh
python3 -m http.server "$TRAEFIK_UPSTREAM_PORT" --bind 127.0.0.1 --directory "$TRAEFIK_RUNTIME_ROOT" > "$TRAEFIK_RUNTIME_ROOT/logs/upstream.log" 2>&1 &
upstream_pid=$!
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_ENGINE_SERVICE_BIN" --serve --config "$TRAEFIK_ENGINE_CONFIG" --socket "$TRAEFIK_ENGINE_SOCKET" > "$TRAEFIK_RUNTIME_ROOT/logs/engine.log" 2>&1 &
engine_pid=$!
attempt=0
while [ "$attempt" -lt 50 ] && [ ! -S "$TRAEFIK_ENGINE_SOCKET" ]; do
    attempt=$((attempt + 1))
    sleep 0.1
done
test -S "$TRAEFIK_ENGINE_SOCKET"
test "$(stat -c "%a" "$TRAEFIK_ENGINE_SOCKET")" = "600"
( cd "$TRAEFIK_RUNTIME_ROOT" && LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_BIN" --configFile="$TRAEFIK_STATIC_CONFIG" ) > "$TRAEFIK_RUNTIME_ROOT/logs/traefik.log" 2>&1 &
traefik_pid=$!
attempt=0
while [ "$attempt" -lt 50 ]; do
    if ! kill -0 "$traefik_pid" 2>/dev/null; then
        exit 1
    fi
    if curl --http1.1 -fsS "http://127.0.0.1:$TRAEFIK_PING_PORT/ping" >/dev/null; then
        break
    fi
    attempt=$((attempt + 1))
    sleep 0.1
done
test "$attempt" -lt 50
curl --http1.1 -fsS "http://127.0.0.1:$TRAEFIK_PING_PORT/ping"
test "$(curl --http1.1 -sS -o /dev/null -w "%{http_code}" -H "X-Request-Id: traefik-native-allow" http://127.0.0.1:$TRAEFIK_PORT/native)" = "200"
test "$(curl --http1.1 -sS -o /dev/null -w "%{http_code}" -H "X-Modsec-Smoke: block" -H "X-Request-Id: traefik-native-deny" http://127.0.0.1:$TRAEFIK_PORT/native)" = "403"
kill "$traefik_pid" "$engine_pid" "$upstream_pid"
```

## 11. Package-assisted path

Status: `package-assisted source build`. Package queries deliberately precede installation. Use only the line matching the distribution.

Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package.

```sh
apt-cache search traefik
dnf search traefik
traefik version 2>/dev/null || true
```

A package or a separately downloaded host binary can supply Traefik itself, but neither contains the repository Go middleware, CGo/Common bridge, or UDS engine service. Keep those source-built components and validate their socket permissions.

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
make build-traefik
make check-config-traefik
make start-smoke-traefik
make runtime-smoke-traefik
run_id="traefik-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
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
test ! -e "$HOME/connector-build/traefik" || find "$HOME/connector-build/traefik" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
test -z "${TRAEFIK_SOCKET_DIR:-}" || test ! -e "$TRAEFIK_SOCKET_DIR" || find "$TRAEFIK_SOCKET_DIR" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Common: for missing headers or libraries, return to the shared guide's advanced section and check the deliberately selected prefix and pkg-config output. For an ABI failure, rebuild host, headers, and connector from the same selected source set.

If Traefik starts without the middleware, check the local-plugin workspace, static registration, File Provider, and the permissions/ownership of the run-local UDS directory. A forwardAuth compatibility route does not diagnose the selected native middleware path.

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
| LD_LIBRARY_PATH | Process-local loader search path used only for a documented local module or service check; do not set it globally. |
| upstream_pid | Local test-upstream process ID from $!; use it only in the same shell run. |
| engine_pid | Local started Traefik engine-service process ID from $!; use it only in the same shell run. |
| traefik_pid | Local started Traefik process ID from $!; use it only in the same shell run. |
| TRAEFIK_BIN | Built or otherwise verified host binary. |
| TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR | External Go middleware build report directory. |
| TRAEFIK_ENGINE_SERVICE_BUILD_DIR | External C/C++ engine-service build directory. |
| TRAEFIK_ENGINE_SERVICE_BIN | Built private engine-service executable. |
| TRAEFIK_RUNTIME_ROOT | Private working directory that contains the staged local plugin during a manual run. |
| TRAEFIK_SOCKET_DIR | Short private directory for the run-local Unix-domain socket; its mode is 0700. |
| TRAEFIK_STATIC_CONFIG | Local-plugin registration configuration. |
| TRAEFIK_DYNAMIC_CONFIG | File Provider router/middleware configuration. |
| TRAEFIK_ENGINE_CONFIG | Private engine-service runtime configuration. |
| TRAEFIK_ENGINE_SOCKET | Private run-local UDS endpoint, not a global path. |
| TRAEFIK_PLUGIN_MODULE | Official local-plugin module path staged beneath plugins-local/src. |
| TRAEFIK_PLUGIN_SOURCE | Staged source directory for the local Traefik plugin. |
| TRAEFIK_PORT | Loopback web entry point for the manual test. |
| TRAEFIK_UPSTREAM_PORT | Loopback test upstream port. |
| TRAEFIK_PING_PORT | Loopback ping endpoint port. |
| WORKDIR | External Traefik host workspace. |
| VERSION | Repository-compatible Traefik release. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
