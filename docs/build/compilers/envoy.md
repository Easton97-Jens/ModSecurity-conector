<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: Envoy

**Language:** English | [Deutsch](envoy.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `ext_proc` on Envoy. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, an official Envoy binary or optional Bazel build, the repository ext_proc service, its CGo/Common bridge, gRPC configuration, a local rule file, and loopback Envoy/upstream listeners.

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
- **Source and scope:** [ModSecurity repository](https://github.com/owasp-modsecurity/ModSecurity)
  The libmodsecurity v3 engine source. Version scope: The selected tag/commit is shown in the shared build section.

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

For the normal local connector route, use Envoy's official release binary and validate it before configuring the ext_proc service. A complete Envoy source build is optional, not the default: the official Bazel route is resource-intensive and must be checked against the selected release's `bazel/README.md` before use.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/envoy"
export ENVOY_VERSION="1.38.2"
export ENVOY_BIN="$HOST_BUILD_BASE/bin/envoy"
export ENVOY_DOWNLOAD_URL="https://github.com/envoyproxy/envoy/releases/download/v$ENVOY_VERSION/envoy-$ENVOY_VERSION-linux-x86_64"
export ENVOY_SHA256="87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899"
mkdir -p "$HOST_BUILD_BASE/bin"
curl -fL "$ENVOY_DOWNLOAD_URL" -o "$ENVOY_BIN"
printf "%s  %s\n" "$ENVOY_SHA256" "$ENVOY_BIN" | sha256sum -c -
chmod 755 "$ENVOY_BIN"
"$ENVOY_BIN" --version
# Optional only after reading the matching upstream Bazel guide: bazel build -c opt //source/exe:envoy-static
```

## 7. Build and integrate the connector

The repository ext_proc executable is the source-built component. It links the Common/libmodsecurity bridge and is not part of an official Envoy binary. The generated host configuration uses `envoy.extensions.filters.http.ext_proc.v3.ExternalProcessor`, an HTTP/2 gRPC cluster, and a router after that filter. Build the service into an external root, then generate both configurations there.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export MODSECURITY_INCLUDE_DIR="$MODSECURITY_PREFIX/include"
export MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/envoy/build/build_ext_proc.sh
export EXT_PROC_BIN="$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"
test -x "$EXT_PROC_BIN"
BUILD_ROOT="$BUILD_ROOT" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/envoy/build/test_ext_proc.sh
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep the configuration and runtime files outside the Git checkout.



```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export ENVOY_CONFIG="$BUILD_ROOT/envoy-ext-proc/config/envoy-ext-proc.yaml"
export EXT_PROC_RUNTIME_CONFIG="$BUILD_ROOT/envoy-ext-proc/runtime/ext-proc.conf"
export ENVOY_PORT=18080
export ENVOY_UPSTREAM_PORT=18081
export EXT_PROC_PORT=18083
export ENVOY_ADMIN_PORT=19001
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
OUTPUT_CONFIG="$ENVOY_CONFIG" LISTEN_PORT="$ENVOY_PORT" UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" EXT_PROC_PORT="$EXT_PROC_PORT" ADMIN_PORT="$ENVOY_ADMIN_PORT" sh connectors/envoy/config/prepare_envoy_ext_proc_config.sh
OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG" RULES_FILE="$RULES_FILE" EVENT_PATH="$BUILD_ROOT/envoy-ext-proc/runtime/events.jsonl" sh connectors/envoy/config/prepare_envoy_ext_proc_runtime_config.sh
"$ENVOY_BIN" --mode validate -c "$ENVOY_CONFIG"
"$EXT_PROC_BIN" --check-config --config connectors/envoy/config/envoy-ext-proc-service.json
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$ENVOY_BIN" --version
test -x "$EXT_PROC_BIN"
file "$EXT_PROC_BIN"
ldd "$EXT_PROC_BIN" | grep -F libmodsecurity
grep -F "envoy.filters.http.ext_proc" "$ENVOY_CONFIG"
grep -F "request_body_mode: STREAMED" "$ENVOY_CONFIG"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. The bounded repository harness starts Envoy, ext_proc, and its upstream, then sends HTTP/1.1 allow and local denial probes through the generated `ext_proc` route. Its admin endpoint is loopback-only and used for local readiness diagnostics. Its results apply only to those observed requests.

```sh
RUNTIME_ROOT="$BUILD_ROOT/envoy-ext-proc/runtime-smoke" ENVOY_BIN="$ENVOY_BIN" RULES_FILE="$RULES_FILE" ENVOY_SMOKE_PORT="$ENVOY_PORT" ENVOY_UPSTREAM_PORT="$ENVOY_UPSTREAM_PORT" ENVOY_EXT_PROC_PORT="$EXT_PROC_PORT" ENVOY_ADMIN_PORT="$ENVOY_ADMIN_PORT" sh connectors/envoy/harness/run_envoy_ext_proc_runtime.sh
# The bounded runner starts Envoy, ext_proc, and a loopback upstream, sends local HTTP/1.1 requests, and stops them.
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

An official Envoy binary is only the host. If validation fails, check the generated ext_proc YAML, gRPC port ownership, the ext_proc service configuration, and the libmodsecurity loader path; do not replace ext_proc with the separate ext_authz compatibility service.

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
| ENVOY_VERSION | Selected official Envoy release for the binary route. |
| ENVOY_BIN | Verified Envoy executable. |
| ENVOY_DOWNLOAD_URL | Official Envoy release-binary URL. |
| ENVOY_SHA256 | Expected binary checksum for the selected release. |
| BUILD_ROOT | External repository connector build root. |
| EXT_PROC_BIN | Repository-built ext_proc service executable. |
| ENVOY_CONFIG | Generated loopback Envoy configuration. |
| EXT_PROC_RUNTIME_CONFIG | Generated Common runtime configuration for ext_proc. |
| OUTPUT_CONFIG | Output path consumed by one configuration-materialization command. |
| EVENT_PATH | Absolute local event-log path passed to the ext_proc runtime configuration writer. |
| RUNTIME_ROOT | External ephemeral root used by the bounded Envoy runtime harness. |
| ENVOY_PORT | Loopback Envoy listener port. |
| ENVOY_UPSTREAM_PORT | Loopback upstream port used by the test. |
| EXT_PROC_PORT | Loopback gRPC ext_proc service port. |
| ENVOY_ADMIN_PORT | Loopback Envoy admin port. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
