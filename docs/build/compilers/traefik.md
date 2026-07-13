<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: Traefik

**Language:** English | [Deutsch](traefik.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-middleware` on Traefik. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, Traefik, the repository native Go middleware, the C/C++ engine service, Common/libmodsecurity, a private Unix-domain socket, static and dynamic File Provider configuration, and loopback HTTP traffic.

## 3. Official upstream documentation

- **Source and scope:** [Traefik Getting Started](https://doc.traefik.io/traefik/getting-started/)
  Official installation choices, entry points, routers, services, and safe local startup context. Version scope: Confirm the documentation version for the selected Traefik release.
- **Source and scope:** [Building and Testing](https://doc.traefik.io/traefik/contributing/building-testing/)
  Official source checkout, Go/tooling, build, and test workflow. Version scope: The required Go version is defined by the selected release's `go.mod`.
- **Source and scope:** [Traefik Configuration Reference](https://doc.traefik.io/traefik/reference/)
  Current official reference index for static configuration, File Provider, routers, middleware, and services. Version scope: Check that the current reference matches the selected release before applying a setting.
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

Required are Git, a C compiler, a C++ compiler, GNU Make, Autotools, libtool, pkg-config, PCRE2 development files, libxml2 development files, YAJL, LMDB, and libcurl. Package names vary by distribution and release: check the official distribution documentation and local availability before installing anything.

```sh
command -v git cc c++ make autoreconf libtool pkg-config
pkg-config --exists libpcre2-8
pkg-config --exists libxml-2.0
pkg-config --exists yajl
pkg-config --exists lmdb
pkg-config --exists libcurl
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```

## 5. Build libmodsecurity v3 from source

This flow uses a fixed, verifiable Git tag and its resolved commit. `v3/master` is not a reproducible pin and is therefore not presented as one. `build.sh` regenerates or refreshes the Autotools inputs; it does not compile the library yet.

```sh
export BUILD_BASE="$HOME/src/modsecurity-build"
export MODSECURITY_SRC="$BUILD_BASE/ModSecurity"
export MODSECURITY_PREFIX="$HOME/.local/modsecurity"
export MODSECURITY_REF="v3.0.16"
export MODSECURITY_COMMIT="7ea9fefbe0ba409d8733b4d682c8c4c059cd028d"
mkdir -p "$BUILD_BASE"
git clone --recurse-submodules https://github.com/owasp-modsecurity/ModSecurity.git "$MODSECURITY_SRC"
git -C "$MODSECURITY_SRC" checkout --detach "$MODSECURITY_REF"
git -C "$MODSECURITY_SRC" submodule update --init --recursive
test "$(git -C "$MODSECURITY_SRC" rev-parse HEAD)" = "$MODSECURITY_COMMIT"
git -C "$MODSECURITY_SRC" rev-parse HEAD
cd "$MODSECURITY_SRC"
./build.sh
./configure --help | grep -E -- "--with-(lmdb|libxml|curl|yajl)"
./configure --prefix="$MODSECURITY_PREFIX" --with-lmdb --with-libxml --with-curl --with-yajl
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf 2)"
make -j"$jobs"
make check
make install
export PKG_CONFIG_PATH="$MODSECURITY_PREFIX/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export LD_LIBRARY_PATH="$MODSECURITY_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

At the selected revision PCRE2 is detected by default; this guide does not invent `--with-pcre2`. Optional switches are checked with `./configure --help` before use. If the chosen release does not offer a switch, remove it rather than documenting an unaccepted command.

`PKG_CONFIG_PATH` lets build systems find the user-local installation.
`LD_LIBRARY_PATH` is only for local development and tests; use a deliberate
loader configuration or rpath for a durable system installation.

```sh
test -d "$MODSECURITY_PREFIX/include"
test -d "$MODSECURITY_PREFIX/lib"
find "$MODSECURITY_PREFIX" -maxdepth 3 -type f | sort
pkg-config --modversion libmodsecurity 2>/dev/null || true
find "$MODSECURITY_PREFIX/lib" -type f \( -name "libmodsecurity.so*" -o -name "libmodsecurity.a" \) -print
```

## 6. Prepare or build the host or proxy

Use an official binary, container, or source build for the Traefik host. The source example below checks out the repository-compatible v3.7.5 tag; its upstream `go.mod` declares Go 1.25.0. That host requirement is distinct from this repository's native middleware module, which currently declares its own Go version.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/traefik"
export TRAEFIK_VERSION="3.7.5"
export TRAEFIK_REF="v$TRAEFIK_VERSION"
export TRAEFIK_SRC="$HOST_BUILD_BASE/traefik"
export TRAEFIK_BIN="$HOST_BUILD_BASE/bin/traefik"
mkdir -p "$HOST_BUILD_BASE/bin"
git clone https://github.com/traefik/traefik.git "$TRAEFIK_SRC"
git -C "$TRAEFIK_SRC" checkout --detach "$TRAEFIK_REF"
git -C "$TRAEFIK_SRC" rev-parse HEAD
grep -E "^go " "$TRAEFIK_SRC/go.mod"
go version
cd "$TRAEFIK_SRC"
make test-unit
make binary
install -m 755 dist/traefik "$TRAEFIK_BIN"
"$TRAEFIK_BIN" version
```

## 7. Build and integrate the connector

A standard Traefik binary does not include the native ModSecurity middleware or the persistent engine service. Build the Go middleware and the C/C++ service from this checkout, placing both outputs outside it. The engine socket must be private to the local run and must not be reused as a shared system endpoint.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$BUILD_ROOT/traefik-native-middleware"
export TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$BUILD_ROOT/traefik-engine-service"
export TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR/traefik-engine-service"
export MODSECURITY_INCLUDE_DIR="$MODSECURITY_PREFIX/include"
export MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib"
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh connectors/traefik/build/build-native-middleware.sh build
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR="$TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR" sh connectors/traefik/build/build-native-middleware.sh test
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/traefik/build/build-engine-service.sh build
test -x "$TRAEFIK_ENGINE_SERVICE_BIN"
BUILD_ROOT="$BUILD_ROOT" TRAEFIK_ENGINE_SERVICE_BUILD_DIR="$TRAEFIK_ENGINE_SERVICE_BUILD_DIR" TRAEFIK_ENGINE_SERVICE_BIN="$TRAEFIK_ENGINE_SERVICE_BIN" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/traefik/build/build-engine-service.sh test
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep the configuration and runtime files outside the Git checkout.

The configuration deliberately uses only loopback entry points and does not enable an insecure dashboard or API. Treat any dashboard or administration endpoint as optional and secure it separately for a real deployment.

```sh
export TRAEFIK_RUNTIME_ROOT="$BUILD_ROOT/traefik-native-runtime"
export RULES_FILE="$BUILD_ROOT/traefik-native-rules.conf"
export TRAEFIK_STATIC_CONFIG="$BUILD_ROOT/traefik-static.yaml"
export TRAEFIK_DYNAMIC_CONFIG="$BUILD_ROOT/traefik-dynamic.yaml"
export TRAEFIK_ENGINE_CONFIG="$BUILD_ROOT/traefik-engine.conf"
export TRAEFIK_ENGINE_SOCKET="$BUILD_ROOT/run/traefik-engine.sock"
export TRAEFIK_PORT=18080
export TRAEFIK_UPSTREAM_PORT=18081
export TRAEFIK_PING_PORT=18082
export TRAEFIK_PLUGIN_MODULE="github.com/Easton97-Jens/ModSecurity-conector/connectors/traefik/native_middleware"
export TRAEFIK_PLUGIN_SOURCE="$TRAEFIK_RUNTIME_ROOT/plugins-local/src/$TRAEFIK_PLUGIN_MODULE"
mkdir -p "$(dirname "$TRAEFIK_PLUGIN_SOURCE")" "$BUILD_ROOT/run" "$BUILD_ROOT/logs"
cp -a "$CONNECTOR_ROOT/connectors/traefik/native_middleware" "$TRAEFIK_PLUGIN_SOURCE"
mkdir -p "$(dirname "$TRAEFIK_ENGINE_SOCKET")"
chmod 700 "$(dirname "$TRAEFIK_ENGINE_SOCKET")"
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
event_path=$BUILD_ROOT/logs/traefik-events.jsonl
max_header_count=100
max_header_name_size=256
max_header_value_size=8192
max_total_header_bytes=65536
max_event_json_bytes=16384
EOF
"$TRAEFIK_BIN" check --configFile="$TRAEFIK_STATIC_CONFIG"
"$TRAEFIK_ENGINE_SERVICE_BIN" --check-config --config "$TRAEFIK_ENGINE_CONFIG"
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$TRAEFIK_BIN" version
test -f "$TRAEFIK_STATIC_CONFIG"
test -f "$TRAEFIK_DYNAMIC_CONFIG"
test -x "$TRAEFIK_ENGINE_SERVICE_BIN"
ldd "$TRAEFIK_ENGINE_SERVICE_BIN" | grep -F libmodsecurity
grep -F "modsecurityNative" "$TRAEFIK_STATIC_CONFIG"
grep -F "engineSocketPath" "$TRAEFIK_DYNAMIC_CONFIG"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. `/ping` confirms host startup; the ordinary `/native` request exercises the private UDS route, and the `X-Modsec-Smoke: block` test header triggers the local 403 rule. These observations do not establish a broader claim.

```sh
python3 -m http.server "$TRAEFIK_UPSTREAM_PORT" --bind 127.0.0.1 --directory "$TRAEFIK_RUNTIME_ROOT" > "$BUILD_ROOT/logs/upstream.log" 2>&1 &
upstream_pid=$!
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_ENGINE_SERVICE_BIN" --serve --config "$TRAEFIK_ENGINE_CONFIG" --socket "$TRAEFIK_ENGINE_SOCKET" > "$BUILD_ROOT/logs/engine.log" 2>&1 &
engine_pid=$!
( cd "$TRAEFIK_RUNTIME_ROOT" && LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$TRAEFIK_BIN" --configFile="$TRAEFIK_STATIC_CONFIG" ) > "$BUILD_ROOT/logs/traefik.log" 2>&1 &
traefik_pid=$!
curl --http1.1 -fsS "http://127.0.0.1:$TRAEFIK_PING_PORT/ping"
curl --http1.1 -i -H "X-Request-Id: traefik-native-allow" http://127.0.0.1:$TRAEFIK_PORT/native
curl --http1.1 -i -H "X-Modsec-Smoke: block" -H "X-Request-Id: traefik-native-deny" http://127.0.0.1:$TRAEFIK_PORT/native
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
git -C "$MODSECURITY_SRC" fetch --tags origin
git -C "$MODSECURITY_SRC" checkout --detach "$MODSECURITY_REF"
git -C "$MODSECURITY_SRC" submodule update --init --recursive
git -C "$MODSECURITY_SRC" rev-parse HEAD
cd "$MODSECURITY_SRC"
make clean
make -j"$jobs"
```

## 14. Uninstall and cleanup

Do not copy files indiscriminately to `/usr/lib` and do not remove global directories. A user prefix does not need `sudo`. Remove evidence or logs only after deliberate review.

```sh
find "$BUILD_BASE" -maxdepth 2 -mindepth 1 -print
# Review the listed paths first; remove only a chosen private prefix or external build directory.
rmdir "$MODSECURITY_PREFIX" 2>/dev/null || true
```

## 15. Troubleshooting

Common: for missing headers or libraries, first check `PKG_CONFIG_PATH`, `LD_LIBRARY_PATH`, the selected prefix, and `pkg-config` output. For an ABI failure, rebuild host, headers, and connector from the same selected source set.

If Traefik starts without the middleware, check the local-plugin workspace, static registration, File Provider, and the permissions/ownership of the run-local UDS directory. A forwardAuth compatibility route does not diagnose the selected native middleware path.

## 16. Variables and placeholders

| Variable/placeholder | Meaning |
| --- | --- |
| BUILD_BASE | Portable source/build parent, for example `$HOME/src/modsecurity-build`. |
| CONNECTOR_ROOT | Git top level of this checkout; connector scripts are called from it. |
| HOST_BUILD_BASE | Connector-specific external subtree below BUILD_BASE for sources, builds, configuration, and local logs. |
| BUILD_ROOT | External build and runtime root for repository-owned connector components. |
| MODSECURITY_SRC | Checkout of the ModSecurity v3 engine below BUILD_BASE. |
| MODSECURITY_PREFIX | Isolated user prefix for headers, libraries, and pkg-config metadata. |
| MODSECURITY_REF | Fixed engine Git tag, never a moving branch. |
| MODSECURITY_COMMIT | Expected commit to which MODSECURITY_REF must resolve. |
| MODSECURITY_INCLUDE_DIR | Include directory below MODSECURITY_PREFIX for repository components. |
| MODSECURITY_LIB_DIR | Library directory below MODSECURITY_PREFIX for repository components. |
| PKG_CONFIG_PATH | Temporary search path for the local libmodsecurity pc file. |
| LD_LIBRARY_PATH | Temporary loader path for local tests only, not a global installation recipe. |
| RULES_FILE | Local test-rule file, not a CRS rule file. |
| jobs | Local parallel-build count from `getconf`; reduce it on low-memory hosts. |
| VERIFIED_RUN_PARENT | External parent for a fresh repository-test checkout and its test artifacts. |
| run_id | Unique identifier for one repository-controlled full-lifecycle run. |
| NO_CRS_RUN_ID | Exported full-lifecycle identifier for the following Make invocation; it keeps evidence and runtime data separated. |
| upstream_pid | Local test-upstream process ID from `$!`; use it only in the same shell run. |
| haproxy_pid | Local started-HAProxy process ID from `$!`; use it only in the same shell run. |
| engine_pid | Local started Traefik engine-service process ID from `$!`; use it only in the same shell run. |
| traefik_pid | Local started Traefik process ID from `$!`; use it only in the same shell run. |
| lighttpd_pid | Local started-lighttpd process ID from `$!`; use it only in the same shell run. |
| TRAEFIK_VERSION | Repository-compatible Traefik release input. |
| TRAEFIK_REF | Git tag derived from TRAEFIK_VERSION. |
| TRAEFIK_SRC | Pinned upstream Traefik source tree. |
| TRAEFIK_BIN | Built or otherwise verified host binary. |
| BUILD_ROOT | External root for repository-native outputs and runtime files. |
| TRAEFIK_NATIVE_MIDDLEWARE_BUILD_DIR | External Go middleware build report directory. |
| TRAEFIK_ENGINE_SERVICE_BUILD_DIR | External C/C++ engine-service build directory. |
| TRAEFIK_ENGINE_SERVICE_BIN | Built private engine-service executable. |
| TRAEFIK_RUNTIME_ROOT | Private working directory that contains the staged local plugin during a manual run. |
| TRAEFIK_STATIC_CONFIG | Local-plugin registration configuration. |
| TRAEFIK_DYNAMIC_CONFIG | File Provider router/middleware configuration. |
| TRAEFIK_ENGINE_CONFIG | Private engine-service runtime configuration. |
| TRAEFIK_ENGINE_SOCKET | Private run-local UDS endpoint, not a global path. |
| TRAEFIK_PLUGIN_MODULE | Official local-plugin module path staged beneath plugins-local/src. |
| TRAEFIK_PLUGIN_SOURCE | Staged source directory for the local Traefik plugin. |
| TRAEFIK_PORT | Loopback web entry point for the manual test. |
| TRAEFIK_UPSTREAM_PORT | Loopback test upstream port. |
| TRAEFIK_PING_PORT | Loopback ping endpoint port. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
