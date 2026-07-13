<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: HAProxy

**Language:** English | [Deutsch](haproxy.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-htx-filter` on HAProxy. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, HAProxy 3.2.21 source, the repository native HTX filter/overlay, the Common bridge, a local rule file, a loopback frontend, and a loopback upstream.

## Connector in this repository

- [HAProxy connector](../../../connectors/haproxy/README.md)
- [Productive HAProxy sources](../../../connectors/haproxy/src/)
- [Native HTX overlay](../../../connectors/haproxy/htx-overlay/)
- [HTX overlay builder](../../../connectors/haproxy/htx-overlay/build-overlay.sh)
- [Source mapping](../../../connectors/haproxy/SOURCE_MAP.json)
- [Native HTX runtime configuration helper](../../../connectors/haproxy/harness/run_haproxy_htx_runtime.sh)

This is the primary connector path for this guide: connectors/haproxy/. The official host documentation in the following section explains only how to provide or build the host; it does not replace the connector source.

Section 7 applies the repository-owned HTX overlay to the selected host source and builds the Common/libmodsecurity integration.

## 3. Official upstream documentation

- **Source and scope:** [HAProxy INSTALL](https://github.com/haproxy/haproxy/blob/master/INSTALL)
  Official target selection, build options, compilation, and installation guidance. Version scope: Read the INSTALL file for the exact selected HAProxy release.
- **Source and scope:** [HAProxy Documentation](https://docs.haproxy.org/)
  Configuration syntax and CLI documentation for `haproxy -c` and runtime operation. Version scope: Use documentation matching the selected major/minor series.
- **Source and scope:** [HAProxy Releases](https://www.haproxy.org/download/)
  Official source downloads and release series selection. Version scope: The repository overlay currently fixes its compatible source to 3.2.21.



## 4. Prerequisites

Build libmodsecurity first with the shared guide. Then install the selected host's documented development tools and keep the host, connector, headers, and libraries compatible.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
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

Build the exact HAProxy release required by the native HTX overlay. This is an ordinary upstream host build; the repository overlay remains Section 7 work.

```sh
WORKDIR="$HOME/connector-build/haproxy"
VERSION="3.2.21"
JOBS=2
```

#### Download and unpack HAProxy

This downloads the selected official host source into an isolated workspace.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://www.haproxy.org/download/3.2/src/haproxy-$VERSION.tar.gz"
curl -fLO "https://www.haproxy.org/download/3.2/src/haproxy-$VERSION.tar.gz.sha256"
sha256sum -c "haproxy-$VERSION.tar.gz.sha256"
tar -xzf "haproxy-$VERSION.tar.gz"
```

#### Build the upstream host

The selected build options enable the libraries used by this local host build. They do not add the repository HTX filter.

```sh
cd "$WORKDIR/haproxy-$VERSION"
make -j"$JOBS" TARGET=linux-glibc USE_OPENSSL=1 USE_ZLIB=1 USE_PCRE2=1
```

### What was installed or built?

The upstream haproxy executable is built in the unpacked source tree. No staging prefix or connector overlay is part of the simple path.

### Check the result

The verbose version output identifies the selected upstream binary and its enabled build features.

```sh
"$WORKDIR/haproxy-$VERSION/haproxy" -vv
```

### Source build and integrity checks

#### Optional: stage the ordinary host

A staged installation is useful for inspection, but it is not the native HTX connector build.

```sh
cd "$WORKDIR/haproxy-$VERSION"
INSTALL_DIR="$HOME/.local/haproxy-modsecurity"
STAGE="$WORKDIR/stage"
make install-bin DESTDIR="$STAGE" PREFIX="$INSTALL_DIR"
"$STAGE$INSTALL_DIR/sbin/haproxy" -vv
```

## 7. Build and integrate the connector

The official HAProxy release does not contain this connector. The repository native HTX integration copies the compatible source to a fresh external worktree, checks and applies its overlay, adds the HTX filter plus Common/libmodsecurity bridge, and rebuilds the host. The timestamped worktree avoids accidental reuse because the builder refuses an existing worktree. SPOE/SPOP is a separate compatibility path and is not evidence for this native filter.

The host path is reintroduced here only so that the connector commands can consume the Section 6 host without rebuilding it.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/haproxy"
export HAPROXY_SRC="$HOST_BUILD_BASE/haproxy-3.2.21"
export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay"
cd "$CONNECTOR_ROOT"
export HAPROXY_HTX_SOURCE_DIR="$HAPROXY_SRC"
export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay-$(date -u +%Y%m%dT%H%M%SZ)"
export MAKE_JOBS=2
CONNECTOR_ROOT="$CONNECTOR_ROOT" sh "$CONNECTOR_ROOT/connectors/haproxy/htx-overlay/build-overlay.sh"
export HAPROXY_HTX_BIN="$HAPROXY_HTX_BUILD_DIR/worktree/haproxy"
test -x "$HAPROXY_HTX_BIN"
"$HAPROXY_HTX_BIN" -vv
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep configuration and runtime files outside the Git checkout.

```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export HAPROXY_CONFIG="$HOST_BUILD_BASE/haproxy-local.cfg"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$HAPROXY_CONFIG" <<EOF
global
    daemon
defaults
    mode http
    timeout connect 5s
    timeout client 30s
    timeout server 30s
frontend local
    bind 127.0.0.1:8080
    filter modsecurity-htx rules-file "$RULES_FILE" phase4-mode safe
    default_backend local_upstream
backend local_upstream
    server app 127.0.0.1:8081
EOF
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$HAPROXY_HTX_BIN" -c -f "$HAPROXY_CONFIG"
"$HAPROXY_HTX_BIN" -vv
file "$HAPROXY_HTX_BIN"
ldd "$HAPROXY_HTX_BIN" | grep -F libmodsecurity | grep -Fv "not found"
test -f "$HAPROXY_HTX_BUILD_DIR/overlay-build.env"
sha256sum "$HAPROXY_HTX_BIN"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

```sh
mkdir -p "$HOST_BUILD_BASE/www"
printf "haproxy local upstream\n" > "$HOST_BUILD_BASE/www/index.html"
python3 -m http.server 8081 --bind 127.0.0.1 --directory "$HOST_BUILD_BASE/www" > "$HOST_BUILD_BASE/upstream.log" 2>&1 &
upstream_pid=$!
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HAPROXY_HTX_BIN" -db -f "$HAPROXY_CONFIG" > "$HOST_BUILD_BASE/haproxy.log" 2>&1 &
haproxy_pid=$!
attempt=0
while [ "$attempt" -lt 50 ]; do
    if ! kill -0 "$upstream_pid" 2>/dev/null || ! kill -0 "$haproxy_pid" 2>/dev/null; then
        exit 1
    fi
    if [ "$(curl -sS --connect-timeout 1 -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/ 2>/dev/null)" = "200" ]; then
        break
    fi
    attempt=$((attempt + 1))
    sleep 0.1
done
test "$attempt" -lt 50
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"
kill "$haproxy_pid" "$upstream_pid"
```

## 11. Package-assisted path

Status: `package-assisted source build`. Package queries deliberately precede installation. Use only the line matching the distribution.

Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package.

```sh
apt-cache search haproxy
dnf search haproxy
haproxy -vv 2>/dev/null || true
```

A package can provide an ordinary HAProxy for comparison, but it does not carry the repository HTX overlay. It therefore cannot substitute for the selected native filter path; use the exact compatible source and overlay build.

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
make build-haproxy
make check-config-haproxy
make start-smoke-haproxy
make runtime-smoke-haproxy
run_id="haproxy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-haproxy-htx
NO_CRS_RUN_ID="$run_id" make evidence-check-haproxy
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
test ! -e "$HOME/connector-build/haproxy" || find "$HOME/connector-build/haproxy" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/.local/haproxy-modsecurity" || find "$HOME/.local/haproxy-modsecurity" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Common: for missing headers or libraries, return to the shared guide's advanced section and check the deliberately selected prefix and pkg-config output. For an ABI failure, rebuild host, headers, and connector from the same selected source set.

The overlay refuses a version other than 3.2.21, an in-tree build directory, missing libmodsecurity headers, or a missing library. Treat that as a compatibility boundary, not as a reason to substitute a SPOA result.

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
| LD_LIBRARY_PATH | Process-local loader search path used only for a documented local module or service check; do not set it globally. |
| upstream_pid | Local test-upstream process ID from $!; use it only in the same shell run. |
| haproxy_pid | Local started-HAProxy process ID from $!; use it only in the same shell run. |
| HAPROXY_SRC | Verified upstream source tree. |
| HAPROXY_HTX_SOURCE_DIR | Verified source consumed by the overlay builder. |
| HAPROXY_HTX_BUILD_DIR | External disposable overlay worktree and provenance directory. |
| HAPROXY_HTX_BIN | Repository-built native HTX host binary. |
| MAKE_JOBS | Parallel-job value passed to the repository overlay builder. |
| HAPROXY_CONFIG | Local loopback HAProxy configuration. |
| WORKDIR | External HAProxy source workspace. |
| VERSION | Exact HAProxy version required by the HTX overlay. |
| JOBS | Deliberately small number of parallel HAProxy build jobs. |
| TARGET | HAProxy host target passed to make; this guide uses linux-glibc. |
| USE_OPENSSL | Enable OpenSSL support for the optional ordinary host build. |
| USE_ZLIB | Enable zlib support for the optional ordinary host build. |
| USE_PCRE2 | Enable PCRE2 support for the optional ordinary host build. |
| INSTALL_DIR | Optional private ordinary HAProxy installation prefix. |
| STAGE | Optional staging root for the ordinary host installation. |
| DESTDIR | Staging root passed directly to HAProxy's install target. |
| PREFIX | Installation prefix passed directly to HAProxy's install target. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
