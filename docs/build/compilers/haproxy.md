<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: HAProxy

**Language:** English | [Deutsch](haproxy.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-htx-filter` on HAProxy. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, HAProxy 3.2.21 source, the repository native HTX filter/overlay, the Common bridge, a local rule file, a loopback frontend, and a loopback upstream.

## 3. Official upstream documentation

- **Source and scope:** [HAProxy INSTALL](https://github.com/haproxy/haproxy/blob/master/INSTALL)
  Official target selection, build options, compilation, and installation guidance. Version scope: Read the INSTALL file for the exact selected HAProxy release.
- **Source and scope:** [HAProxy Documentation](https://docs.haproxy.org/)
  Configuration syntax and CLI documentation for `haproxy -c` and runtime operation. Version scope: Use documentation matching the selected major/minor series.
- **Source and scope:** [HAProxy Releases](https://www.haproxy.org/download/)
  Official source downloads and release series selection. Version scope: The repository overlay currently fixes its compatible source to 3.2.21.
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

Build an official HAProxy first and inspect `haproxy -vv`. The selected repository integration has a stricter compatibility constraint: its native HTX overlay explicitly requires HAProxy 3.2.21. The normal HAProxy build below proves the upstream host build; the following overlay build creates the selected host copy and links it to libmodsecurity.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/haproxy"
export HAPROXY_VERSION="3.2.21"
export HAPROXY_ARCHIVE="haproxy-$HAPROXY_VERSION.tar.gz"
export HAPROXY_URL="https://www.haproxy.org/download/3.2/src/$HAPROXY_ARCHIVE"
export HAPROXY_SHA256="0cb8818a26c5f888e0cb1c40f1b3acb9fb952527d1733f769ce688fedd680339"
export HAPROXY_SRC="$HOST_BUILD_BASE/haproxy-$HAPROXY_VERSION"
export HAPROXY_PREFIX="$HOME/.local/haproxy-modsecurity"
export HAPROXY_STAGE="$HOST_BUILD_BASE/stage"
mkdir -p "$HOST_BUILD_BASE"
cd "$HOST_BUILD_BASE"
curl -fLO "$HAPROXY_URL"
printf "%s  %s\n" "$HAPROXY_SHA256" "$HAPROXY_ARCHIVE" | sha256sum -c -
tar -xzf "$HAPROXY_ARCHIVE"
cd "$HAPROXY_SRC"
make help
make -j"$jobs" TARGET=linux-glibc USE_OPENSSL=1 USE_ZLIB=1 USE_PCRE2=1
make install-bin DESTDIR="$HAPROXY_STAGE" PREFIX="$HAPROXY_PREFIX"
export HAPROXY_BIN="$HAPROXY_STAGE$HAPROXY_PREFIX/sbin/haproxy"
"$HAPROXY_BIN" -vv
```

## 7. Build and integrate the connector

The official HAProxy release does not contain this connector. The repository native HTX integration copies the compatible source to an external worktree, checks and applies its overlay, adds the HTX filter plus Common/libmodsecurity bridge, and rebuilds the host. SPOE/SPOP is a separate compatibility path and is not evidence for this native filter.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export HAPROXY_HTX_SOURCE_DIR="$HAPROXY_SRC"
export HAPROXY_HTX_BUILD_DIR="$HOST_BUILD_BASE/htx-overlay"
export MODSECURITY_INCLUDE_DIR="$MODSECURITY_PREFIX/include"
export MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib"
export MAKE_JOBS="$jobs"
CONNECTOR_ROOT="$CONNECTOR_ROOT" sh connectors/haproxy/htx-overlay/build-overlay.sh
export HAPROXY_HTX_BIN="$HAPROXY_HTX_BUILD_DIR/worktree/haproxy"
test -x "$HAPROXY_HTX_BIN"
"$HAPROXY_HTX_BIN" -vv
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep the configuration and runtime files outside the Git checkout.



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
"$HAPROXY_HTX_BIN" -c -f "$HAPROXY_CONFIG"
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$HAPROXY_HTX_BIN" -vv
file "$HAPROXY_HTX_BIN"
ldd "$HAPROXY_HTX_BIN" | grep -F libmodsecurity
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
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
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

The overlay refuses a version other than 3.2.21, an in-tree build directory, missing libmodsecurity headers, or a missing library. Treat that as a compatibility boundary, not as a reason to substitute a SPOA result.

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
| HAPROXY_VERSION | Version required by the current HTX overlay. |
| HAPROXY_ARCHIVE | Archive name derived from HAPROXY_VERSION. |
| HAPROXY_URL | Official HAProxy source archive URL. |
| HAPROXY_SHA256 | Expected SHA-256 for the selected source archive. |
| HAPROXY_SRC | Verified upstream source tree. |
| HAPROXY_PREFIX | Private upstream host installation prefix. |
| HAPROXY_STAGE | Staging root used with DESTDIR. |
| HAPROXY_BIN | Staged ordinary HAProxy binary. |
| HAPROXY_HTX_SOURCE_DIR | Verified source consumed by the overlay builder. |
| HAPROXY_HTX_BUILD_DIR | External disposable overlay worktree and provenance directory. |
| HAPROXY_HTX_BIN | Repository-built native HTX host binary. |
| MAKE_JOBS | Parallel-job value passed to the repository overlay builder. |
| HAPROXY_CONFIG | Local loopback HAProxy configuration. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
