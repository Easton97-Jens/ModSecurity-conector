<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: lighttpd

**Language:** English | [Deutsch](lighttpd.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `patched-native` on lighttpd. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, lighttpd 1.4.84 source, the repository Entity-Body patch, a patched host, a matching connector module, a local runtime configuration, and loopback HTTP/1.1 traffic.

## 3. Official upstream documentation

- **Source and scope:** [lighttpd INSTALL](https://github.com/lighttpd/lighttpd1.4/blob/master/INSTALL)
  Official prerequisites, Autotools/source-build, test, installation, and startup guidance. Version scope: Re-check INSTALL for the selected lighttpd release.
- **Source and scope:** [lighttpd Source Downloads](https://download.lighttpd.net/lighttpd/)
  Official release archives and checksum material. Version scope: The latest upstream release can differ from the repository patch pin.
- **Source and scope:** [lighttpd Documentation](https://redmine.lighttpd.net/projects/lighttpd/wiki)
  Official configuration and command documentation when applicable to the selected host release. Version scope: Check accessibility and release relevance before relying on a page.
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

The current repository patch and patched-host scripts are pinned to lighttpd 1.4.84. Do not silently substitute a newer upstream archive: for example, a newer upstream release must be treated as an update that requires patch, configure, ABI, and runtime revalidation. Work on a disposable copy so the verified upstream source remains available for comparison.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/lighttpd"
export LIGHTTPD_VERSION="1.4.84"
export LIGHTTPD_ARCHIVE="lighttpd-$LIGHTTPD_VERSION.tar.xz"
export LIGHTTPD_URL="https://download.lighttpd.net/lighttpd/releases-1.4.x/$LIGHTTPD_ARCHIVE"
export LIGHTTPD_CHECKSUM_URL="https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$LIGHTTPD_VERSION.sha256sum"
export LIGHTTPD_CHECKSUM_FILE="$HOST_BUILD_BASE/lighttpd-$LIGHTTPD_VERSION.sha256sum"
export LIGHTTPD_SHA256="076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70"
export LIGHTTPD_SRC="$HOST_BUILD_BASE/lighttpd-$LIGHTTPD_VERSION"
export LIGHTTPD_PATCHED_SRC="$HOST_BUILD_BASE/lighttpd-$LIGHTTPD_VERSION-patched"
export LIGHTTPD_BUILD_DIR="$HOST_BUILD_BASE/build-$LIGHTTPD_VERSION"
export LIGHTTPD_PREFIX="$HOME/.local/lighttpd-modsecurity"
export LIGHTTPD_PATCH_FILE="$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"
mkdir -p "$HOST_BUILD_BASE"
cd "$HOST_BUILD_BASE"
curl -fLO "$LIGHTTPD_URL"
curl -fL "$LIGHTTPD_CHECKSUM_URL" -o "$LIGHTTPD_CHECKSUM_FILE"
awk -v archive="$LIGHTTPD_ARCHIVE" '$2 == archive { print }' "$LIGHTTPD_CHECKSUM_FILE" | sha256sum -c -
printf "%s  %s\n" "$LIGHTTPD_SHA256" "$LIGHTTPD_ARCHIVE" | sha256sum -c -
tar -xJf "$LIGHTTPD_ARCHIVE"
cp -a "$LIGHTTPD_SRC" "$LIGHTTPD_PATCHED_SRC"
cd "$LIGHTTPD_PATCHED_SRC"
patch --dry-run -p1 < "$LIGHTTPD_PATCH_FILE"
patch -p1 < "$LIGHTTPD_PATCH_FILE"
if test -x ./autogen.sh; then ./autogen.sh; fi
./configure --help | grep -E -- "--prefix|--bindir|--sbindir|--libdir"
mkdir -p "$LIGHTTPD_BUILD_DIR"
cd "$LIGHTTPD_BUILD_DIR"
"$LIGHTTPD_PATCHED_SRC/configure" --prefix="$LIGHTTPD_PREFIX" --bindir="$LIGHTTPD_PREFIX/bin" --sbindir="$LIGHTTPD_PREFIX/bin" --libdir="$LIGHTTPD_PREFIX/lib"
make -j"$jobs"
if make -n check >/dev/null 2>&1; then make check; fi
make install
"$LIGHTTPD_PREFIX/bin/lighttpd" -V
```

## 7. Build and integrate the connector

The repository module must use the same patched source headers and generated `config.h` as the host. The source build script links it to libmodsecurity and writes the module to an external directory. A normal lighttpd package lacks the Entity-Body hook and cannot load this selected module as an equivalent path.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
export LIGHTTPD_MODULE_DIR="$BUILD_ROOT/modules"
export MODSECURITY_INCLUDE_DIR="$MODSECURITY_PREFIX/include"
export MODSECURITY_LIB_DIR="$MODSECURITY_PREFIX/lib"
BUILD_ROOT="$BUILD_ROOT" LIGHTTPD_CONNECTOR_OUT_DIR="$BUILD_ROOT/connector" LIGHTTPD_MODULE_DIR="$LIGHTTPD_MODULE_DIR" LIGHTTPD_MSCONNECTOR_CORE_MODE=patched LIGHTTPD_SOURCE_DIR="$LIGHTTPD_PATCHED_SRC" LIGHTTPD_BUILD_ROOT="$LIGHTTPD_BUILD_DIR" MODSECURITY_INCLUDE_DIR="$MODSECURITY_INCLUDE_DIR" MODSECURITY_LIB_DIR="$MODSECURITY_LIB_DIR" sh connectors/lighttpd/build/build_module.sh
export LIGHTTPD_MODULE="$LIGHTTPD_MODULE_DIR/mod_msconnector.so"
test -f "$LIGHTTPD_MODULE"
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep the configuration and runtime files outside the Git checkout.



```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export LIGHTTPD_RUNTIME_CONFIG="$HOST_BUILD_BASE/msconnector-runtime.conf"
export LIGHTTPD_CONFIG="$HOST_BUILD_BASE/lighttpd-local.conf"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$LIGHTTPD_RUNTIME_CONFIG" <<EOF
rules_file=$RULES_FILE
request_body_mode=none
response_body_mode=none
phase4_mode=safe
EOF
cat > "$LIGHTTPD_CONFIG" <<EOF
server.compat-module-load = "disable"
server.modules = ( "mod_msconnector" )
server.bind = "127.0.0.1"
server.port = 8080
server.document-root = "$LIGHTTPD_PREFIX/htdocs"
server.pid-file = "$HOST_BUILD_BASE/lighttpd.pid"
server.errorlog = "$HOST_BUILD_BASE/lighttpd-error.log"
msconnector.enabled = "enable"
msconnector.config-file = "$LIGHTTPD_RUNTIME_CONFIG"
EOF
"$LIGHTTPD_PREFIX/bin/lighttpd" -tt -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR"
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$LIGHTTPD_PREFIX/bin/lighttpd" -V
file "$LIGHTTPD_MODULE"
ldd "$LIGHTTPD_MODULE" | grep -F libmodsecurity
nm -D "$LIGHTTPD_MODULE" | grep -E "mod_msconnector_plugin_init$"
grep -F LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$LIGHTTPD_PATCHED_SRC/src/plugin.h"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

```sh
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$LIGHTTPD_PREFIX/bin/lighttpd" -D -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR" &
lighttpd_pid=$!
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
kill "$lighttpd_pid"
```

## 11. Package-assisted path

Status: `selected profile not available package-only`. Package queries deliberately precede installation. Use only the line matching the distribution.

Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package.

```sh
apt-cache search lighttpd
dnf search lighttpd
lighttpd -V 2>/dev/null || true
```

A package can supply a comparison host and prerequisites, but it cannot supply this repository's versioned Entity-Body patch or a module built with matching patched headers. It is not a package-only version of the selected path.

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
make build-lighttpd
make check-config-lighttpd
make start-smoke-lighttpd
make runtime-smoke-lighttpd
run_id="lighttpd-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
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

If patch dry-run fails, do not force it: verify the exact 1.4.84 source and patch checksum. If the module cannot load, rebuild the patched core and module from the same source/header/configuration set.

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
| LIGHTTPD_VERSION | Exact upstream version required by the repository patch. |
| LIGHTTPD_ARCHIVE | Archive name derived from LIGHTTPD_VERSION. |
| LIGHTTPD_URL | Official lighttpd source archive URL. |
| LIGHTTPD_CHECKSUM_URL | Official selected-release checksum URL. |
| LIGHTTPD_CHECKSUM_FILE | Downloaded official checksum file for the selected archive. |
| LIGHTTPD_SHA256 | Expected selected archive checksum. |
| LIGHTTPD_SRC | Verified unmodified upstream source tree. |
| LIGHTTPD_PATCHED_SRC | Disposable patched copy of the selected source. |
| LIGHTTPD_BUILD_DIR | Out-of-tree patched lighttpd build directory. |
| LIGHTTPD_PREFIX | Private patched host installation prefix. |
| LIGHTTPD_PATCH_FILE | Repository versioned Entity-Body patch. |
| LIGHTTPD_MODULE_DIR | External directory for the matching connector module. |
| LIGHTTPD_MODULE | Built matching module path. |
| LIGHTTPD_RUNTIME_CONFIG | Connector runtime rules/mode configuration. |
| LIGHTTPD_CONFIG | Local lighttpd server configuration. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
