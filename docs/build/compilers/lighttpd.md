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

The following connector commands assume the default system installation under `/usr/local`. For a user-local prefix, use the shared guide's advanced section and pass its include and library paths deliberately.

## 6. Provide the host or proxy

### Simple path

The selected path requires a patched lighttpd source host. The first steps download the exact version required by the repository patch; the patch and host build follow under the source-build heading.

```sh
WORKDIR="$HOME/connector-build/lighttpd"
VERSION="1.4.84"
INSTALL_DIR="$HOME/.local/lighttpd-modsecurity"
```

#### Download lighttpd

This leaves the verified upstream source untouched so that the patch is applied only to a disposable copy.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$VERSION.tar.xz"
tar -xJf "lighttpd-$VERSION.tar.xz"
```

### What was installed or built?

The private prefix contains the patched lighttpd host. It does not contain the repository connector module yet.

### Source build and integrity checks

#### Create a working copy and test the patch

The first patch command only tests whether the selected source accepts the patch. The second command changes the disposable working copy.

```sh
cp -a "lighttpd-$VERSION" "lighttpd-$VERSION-patched"
cd "lighttpd-$VERSION-patched"
patch --dry-run -p1 < "$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"
patch -p1 < "$CONNECTOR_ROOT/connectors/lighttpd/patches/0001-lighttpd-1.4.84-msconnector-stream-hooks.patch"
```

#### Build the patched host

This builds only the patched lighttpd host. The connector module is deliberately deferred to Section 7.

```sh
test -x ./autogen.sh && ./autogen.sh
./configure --prefix="$INSTALL_DIR"
make -j2
make install
```

#### Optional: use an out-of-tree host build

Keep this advanced alternative for comparison or reproducible build layouts; it still builds only the patched host.

```sh
mkdir -p "$WORKDIR/build-$VERSION"
cd "$WORKDIR/build-$VERSION"
"$WORKDIR/lighttpd-$VERSION-patched/configure" --prefix="$INSTALL_DIR"
make -j2
make check
make install
```

#### Optional: verify download and version

The official checksum file and the fixed patch-compatible checksum both apply to lighttpd 1.4.84.

```sh
cd "$WORKDIR"
curl -fL "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-$VERSION.sha256sum" -o "lighttpd-$VERSION.sha256sum"
awk -v archive="lighttpd-$VERSION.tar.xz" '$2 == archive { print }' "lighttpd-$VERSION.sha256sum" | sha256sum -c -
printf "%s  %s\n" "076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70" "lighttpd-$VERSION.tar.xz" | sha256sum -c -
```

### Check the result

The upstream 1.4.84 installation layout places lighttpd below sbin for this prefix.

```sh
"$INSTALL_DIR/sbin/lighttpd" -V
```

## 7. Build and integrate the connector

The repository module must use the same patched source headers and generated `config.h` as the host. The source build script links it to libmodsecurity and writes the module to an external directory. A normal lighttpd package lacks the Entity-Body hook and cannot load this selected module as an equivalent path.

The host path is reintroduced here only so that the connector commands can consume the Section 6 host without rebuilding it.

```sh
export HOST_BUILD_BASE="$HOME/connector-build/lighttpd"
export LIGHTTPD_PATCHED_SRC="$HOST_BUILD_BASE/lighttpd-1.4.84-patched"
export LIGHTTPD_BUILD_DIR="$LIGHTTPD_PATCHED_SRC"
export LIGHTTPD_PREFIX="$HOME/.local/lighttpd-modsecurity"
cd "$CONNECTOR_ROOT"
export BUILD_ROOT="$HOST_BUILD_BASE/repository-build"
```

```sh
export LIGHTTPD_MODULE_DIR="$BUILD_ROOT/modules"
BUILD_ROOT="$BUILD_ROOT" LIGHTTPD_CONNECTOR_OUT_DIR="$BUILD_ROOT/connector" LIGHTTPD_MODULE_DIR="$LIGHTTPD_MODULE_DIR" LIGHTTPD_MSCONNECTOR_CORE_MODE=patched LIGHTTPD_SOURCE_DIR="$LIGHTTPD_PATCHED_SRC" LIGHTTPD_BUILD_ROOT="$LIGHTTPD_BUILD_DIR" MODSECURITY_INCLUDE_DIR="/usr/local/include" MODSECURITY_LIB_DIR="/usr/local/lib" sh connectors/lighttpd/build/build_module.sh
export LIGHTTPD_MODULE="$LIGHTTPD_MODULE_DIR/mod_msconnector.so"
test -f "$LIGHTTPD_MODULE"
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep configuration and runtime files outside the Git checkout.

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
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$LIGHTTPD_PREFIX/sbin/lighttpd" -tt -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR"
"$LIGHTTPD_PREFIX/sbin/lighttpd" -V
file "$LIGHTTPD_MODULE"
ldd "$LIGHTTPD_MODULE" | grep -F libmodsecurity
nm -D "$LIGHTTPD_MODULE" | grep -E "mod_msconnector_plugin_init$"
grep -F LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION "$LIGHTTPD_PATCHED_SRC/src/plugin.h"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

```sh
"$LIGHTTPD_PREFIX/sbin/lighttpd" -D -f "$LIGHTTPD_CONFIG" -m "$LIGHTTPD_MODULE_DIR" &
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
git -C "$CONNECTOR_ROOT" pull --ff-only
git -C "$CONNECTOR_ROOT" submodule update --init --recursive
# Rebuild the selected host and connector with the commands above.
```

## 14. Uninstall and cleanup

Do not copy files indiscriminately to `/usr/lib` and do not remove global directories. A user prefix does not need `sudo`. Remove evidence or logs only after deliberate review.

```sh
find "$HOME/src/modsecurity-connectors" -maxdepth 2 -mindepth 1 -print
# Review the listed paths first; remove only a chosen external host-build directory.
```

## 15. Troubleshooting

Common: for missing headers or libraries, return to the shared guide's advanced section and check the deliberately selected prefix and pkg-config output. For an ABI failure, rebuild host, headers, and connector from the same selected source set.

If patch dry-run fails, do not force it: verify the exact 1.4.84 source and patch checksum. If the module cannot load, rebuild the patched core and module from the same source/header/configuration set.

## 16. Variables and placeholders

| Variable/placeholder | Meaning |
| --- | --- |
| CONNECTOR_ROOT | Git top level of this checkout; connector scripts are called from it. |
| HOST_BUILD_BASE | Connector-specific external directory for sources, builds, configuration, and local logs. |
| BUILD_ROOT | External build and runtime root for repository-owned connector components. |
| RULES_FILE | Local test-rule file, not a CRS rule file. |
| VERIFIED_RUN_PARENT | External parent for a fresh repository-test checkout and its test artifacts. |
| run_id | Unique identifier for one repository-controlled full-lifecycle run. |
| NO_CRS_RUN_ID | Exported full-lifecycle identifier for the following Make invocation; it keeps evidence and runtime data separated. |
| upstream_pid | Local test-upstream process ID from `$!`; use it only in the same shell run. |
| haproxy_pid | Local started-HAProxy process ID from `$!`; use it only in the same shell run. |
| engine_pid | Local started Traefik engine-service process ID from `$!`; use it only in the same shell run. |
| traefik_pid | Local started Traefik process ID from `$!`; use it only in the same shell run. |
| lighttpd_pid | Local started-lighttpd process ID from `$!`; use it only in the same shell run. |
| LIGHTTPD_PATCHED_SRC | Disposable patched copy of the selected source. |
| LIGHTTPD_BUILD_DIR | Out-of-tree patched lighttpd build directory. |
| LIGHTTPD_PREFIX | Private patched host installation prefix. |
| LIGHTTPD_MODULE_DIR | External directory for the matching connector module. |
| LIGHTTPD_MODULE | Built matching module path. |
| LIGHTTPD_RUNTIME_CONFIG | Connector runtime rules/mode configuration. |
| LIGHTTPD_CONFIG | Local lighttpd server configuration. |
| WORKDIR | External lighttpd source workspace. |
| VERSION | Exact lighttpd version required by the repository patch. |
| INSTALL_DIR | Private patched lighttpd installation prefix. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
