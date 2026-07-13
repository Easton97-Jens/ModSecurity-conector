<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: Apache HTTP Server

**Language:** English | [Deutsch](apache.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-httpd-module` on Apache HTTP Server. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, Apache HTTP Server 2.4, APR/APR-util, PCRE2, the repository Apache adapter, APXS, a local rule file, and a loopback httpd instance.

## Connector in this repository

- [Apache connector](../../../connectors/apache/README.md)
- [Productive Apache sources](../../../connectors/apache/src/)
- [Autotools configuration](../../../connectors/apache/configure.ac)
- [Source mapping](../../../connectors/apache/SOURCE_MAP.json)
- [Standalone Apache configuration harness](../../../connectors/apache/harness/apache_smoke.conf)

This is the primary connector path for this guide: connectors/apache/. The official host documentation in the following section explains only how to provide or build the host; it does not replace the connector source.

Section 7 materializes this adapter-owned source into an external Autotools worktree and builds it with the selected APXS/httpd pair.

## 3. Official upstream documentation

- **Source and scope:** [Compiling and Installing](https://httpd.apache.org/docs/2.4/install.html)
  Apache's official source release, APR/APR-util and PCRE2 prerequisites, configure, make, installation, start, and stop sequence. Version scope: HTTP Server 2.4; choose and verify the release again before building.
- **Source and scope:** [APXS](https://httpd.apache.org/docs/2.4/programs/apxs.html)
  The DSO build/install interface and the queries that bind a module to one httpd build. Version scope: HTTP Server 2.4 APXS reference.
- **Source and scope:** [Apache HTTP Server Download](https://httpd.apache.org/download.cgi)
  Official release archives, PGP signatures, checksums, and Apache KEYS. Version scope: The page changes when Apache publishes a release.

## Alternative: official upstream connector

The official upstream connector [ModSecurity-apache](https://github.com/owasp-modsecurity/ModSecurity-apache) is an alternative implementation.

The main path in this guide uses the repository-owned adapter under [`connectors/apache/`](../../../connectors/apache/README.md). A separate upstream build does not automatically include the repository-owned Common integration and is not automatically equivalent to the checked path here.

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

Apache's current adapter accepts a prefix and assumes its `lib` directory, so use the normal default layout for Apache or enhance that adapter before selecting lib64.

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

For the simplest local adapter build, install an Apache package together with its development package. The development package supplies APXS and the matching headers.

#### Debian / Ubuntu

Install the host and its APXS/header package from the distribution.

```sh
sudo apt update
sudo apt install apache2 apache2-dev
```

#### Fedora / RHEL

Install the corresponding httpd and development packages.

```sh
sudo dnf install httpd httpd-devel
```

### What was installed or built?

The package path provides Apache httpd, APXS, the module directory, and the headers needed to build a module for that exact host.

### Check the result

These queries show the host prefix, header directory, module directory, and Apache version. They must describe the same Apache installation.

```sh
APXS="${APXS:-$(command -v apxs || command -v apxs2)}"
test -x "$APXS"
HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"
"$APXS" -q PREFIX
"$APXS" -q INCLUDEDIR
"$APXS" -q LIBEXECDIR
"$HTTPD_BIN" -v
```

### Source build and integrity checks

#### Optional: build Apache completely from source

APR and APR-util are Apache portability libraries. Use matching system development packages, or place verified APR and APR-util source trees below srclib before configuring Apache.

```sh
WORKDIR="$HOME/connector-build/apache"
VERSION="2.4.68"
INSTALL_DIR="$HOME/.local/apache-modsecurity"
```

#### Download and unpack

This verifies the archive before unpacking it and creates an isolated source tree; it does not build the adapter. Import the Apache release signing key from the official download page before running the GPG check.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2"
curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2.sha256"
curl -fLO "https://downloads.apache.org/httpd/httpd-$VERSION.tar.bz2.asc"
sha256sum -c "httpd-$VERSION.tar.bz2.sha256"
gpg --verify "httpd-$VERSION.tar.bz2.asc" "httpd-$VERSION.tar.bz2"
tar -xjf "httpd-$VERSION.tar.bz2"
```

#### Build the host

Configure and install Apache into the private prefix. The connector remains Section 7 work.

```sh
cd "$WORKDIR/httpd-$VERSION"
./configure --prefix="$INSTALL_DIR" --enable-mods-shared=most --with-pcre="$(command -v pcre2-config)"
make -j2
make install
```

#### Check source-host outputs

These checks confirm that the private source host exposes the APXS and executable pair that Section 7 must use.

```sh
test -x "$INSTALL_DIR/bin/httpd"
test -x "$INSTALL_DIR/bin/apachectl"
test -x "$INSTALL_DIR/bin/apxs"
"$INSTALL_DIR/bin/apxs" -q PREFIX
```

## 7. Build and integrate the connector

The adapter used in this guide is under [connectors/apache](../../../connectors/apache/README.md). Its productive module code is under [connectors/apache/src](../../../connectors/apache/src/). Use the APXS checked in Section 6; the package path normally exposes apxs, while the optional source-host assignment below selects the matching private APXS explicitly. The supported materialization step keeps generated Autotools templates in an external worktree while preserving connectors/apache/ as the adapter source of record.

#### Optional: select the source-host APXS

If you built the optional Apache source host in Section 6, run this in the same shell before the adapter commands. Package-host users skip it.

```sh
APXS="$HOME/.local/apache-modsecurity/bin/apxs"
```

#### Materialize, build, and install the adapter

configure.ac accepts --with-apache as an optional lookup override, but this guide passes the httpd derived from the selected APXS explicitly. The repository build helper uses the same pairing, preventing an adapter from being configured against a different host binary.

```sh
APXS="${APXS:-$(command -v apxs || command -v apxs2)}"
test -x "$APXS"
HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"
cd "$CONNECTOR_ROOT/connectors/apache"
test -f "$CONNECTOR_ROOT/connectors/apache/configure.ac"
mkdir -p "$HOME/connector-build/apache"
CONNECTOR_BUILD_DIR="$(mktemp -d "$HOME/connector-build/apache/connector-src.XXXXXX")"
CONNECTOR_ROOT="$CONNECTOR_ROOT" sh "$CONNECTOR_ROOT/modules/ModSecurity-test-Framework/ci/provisioning/materialize-connector-source.sh" --connector apache --adapter-dir "$CONNECTOR_ROOT/connectors/apache" --dest-dir "$CONNECTOR_BUILD_DIR"
cd "$CONNECTOR_BUILD_DIR"
./autogen.sh
./configure --with-libmodsecurity="$MODSECURITY_PREFIX" --with-apxs="$APXS" --with-apache="$HTTPD_BIN"
make -j2
if [ -w "$("$APXS" -q LIBEXECDIR)" ]; then
    make install
else
    sudo make install
fi
MODULE_PATH="$("$APXS" -q LIBEXECDIR)/mod_security3.so"
test -f "$MODULE_PATH"
```

## 8. Configuration

Create the local test rule and an isolated, writable Apache configuration. This section does not start Apache; Section 10 performs the syntax check and loopback requests. The generated module file selects a package-host MPM and supporting DSOs when present; a source host with a static MPM remains valid without an extra MPM line.

```sh
APXS="${APXS:-$(command -v apxs || command -v apxs2)}"
test -x "$APXS"
HTTPD_BIN="${HTTPD_BIN:-$("$APXS" -q SBINDIR)/$("$APXS" -q PROGNAME)}"
HTTPD_MODULE_DIR="$("$APXS" -q LIBEXECDIR)"
HTTPD_RUNTIME_ROOT="$HOME/connector-build/apache/runtime"
HTTPD_DOCUMENT_ROOT="$HTTPD_RUNTIME_ROOT/htdocs"
HTTPD_MODULES="$HTTPD_RUNTIME_ROOT/httpd-modules.conf"
RULES_FILE="$HOME/connector-build/apache/modsecurity-local.conf"
HTTPD_CONFIG="$HTTPD_RUNTIME_ROOT/httpd-local.conf"
mkdir -p "$HTTPD_RUNTIME_ROOT/logs" "$HTTPD_RUNTIME_ROOT/run" "$HTTPD_DOCUMENT_ROOT"
printf "apache modsecurity test\n" > "$HTTPD_DOCUMENT_ROOT/index.html"
: > "$HTTPD_MODULES"
for mpm in mpm_event mpm_worker mpm_prefork; do
    if [ -f "$HTTPD_MODULE_DIR/mod_$mpm.so" ]; then
        printf "LoadModule %s_module \"%s/mod_%s.so\"\n" "$mpm" "$HTTPD_MODULE_DIR" "$mpm" >> "$HTTPD_MODULES"
        break
    fi
done
for module in authz_core authz_host mime dir unixd; do
    if [ -f "$HTTPD_MODULE_DIR/mod_$module.so" ]; then
        printf "LoadModule %s_module \"%s/mod_%s.so\"\n" "$module" "$HTTPD_MODULE_DIR" "$module" >> "$HTTPD_MODULES"
    fi
done
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$HTTPD_CONFIG" <<EOF
ServerRoot "$HTTPD_RUNTIME_ROOT"
PidFile "run/httpd.pid"
DefaultRuntimeDir "run"
Listen 127.0.0.1:8080
ServerName 127.0.0.1
ErrorLog "logs/error.log"
Include "$HTTPD_MODULES"
LoadModule security3_module "$MODULE_PATH"
DocumentRoot "$HTTPD_DOCUMENT_ROOT"
<Directory "$HTTPD_DOCUMENT_ROOT">
    Require all granted
</Directory>
<Location "/">
    modsecurity on
    modsecurity_rules_file "$RULES_FILE"
</Location>
EOF
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$HTTPD_BIN" -v
"$HTTPD_BIN" -M | grep -E "(^|[[:space:]])so_module"
"$APXS" -q PREFIX
"$APXS" -q INCLUDEDIR
"$APXS" -q LIBEXECDIR
file "$MODULE_PATH"
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ldd "$MODULE_PATH" | grep -F libmodsecurity | grep -Fv "not found"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

```sh
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HTTPD_BIN" -d "$HTTPD_RUNTIME_ROOT" -f "$HTTPD_CONFIG" -t
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HTTPD_BIN" -d "$HTTPD_RUNTIME_ROOT" -f "$HTTPD_CONFIG" -k start
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/)" = "200"
test "$(curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/blocked)" = "403"
LD_LIBRARY_PATH="$MODSECURITY_LIB_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$HTTPD_BIN" -d "$HTTPD_RUNTIME_ROOT" -f "$HTTPD_CONFIG" -k stop
```

## 11. Package-assisted path

Status: `package-assisted source build`. Package queries deliberately precede installation. Use only the line matching the distribution.

Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package.

```sh
apt-cache search apache2
dnf search httpd
apache2 -v 2>/dev/null || httpd -v 2>/dev/null || true
```

A package host can be useful for comparison, but its APXS, headers, module directory, configuration layout, and service name can differ from this source prefix. Query the matching distribution's official package documentation before choosing package names; rebuild the adapter with that package's APXS if that is the intended host.

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
make build-apache
make check-config-apache
make start-smoke-apache
make runtime-smoke-apache
run_id="apache-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-apache
NO_CRS_RUN_ID="$run_id" make evidence-check-apache
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
test ! -e "$HOME/connector-build/apache" || find "$HOME/connector-build/apache" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/.local/apache-modsecurity" || find "$HOME/.local/apache-modsecurity" -maxdepth 2 -mindepth 1 -print
test ! -e "$HOME/modsecurity-connector-work" || find "$HOME/modsecurity-connector-work" -maxdepth 2 -mindepth 1 -print
# Review the listed external paths first; remove only a chosen host-build or test directory.
```

## 15. Troubleshooting

Common: for missing headers or libraries, return to the shared guide's advanced section and check the deliberately selected prefix and pkg-config output. For an ABI failure, rebuild host, headers, and connector from the same selected source set.

If `apxs -q` points at different headers or a different module directory than the running httpd, stop and rebuild the adapter. A module built against one Apache ABI must not be loaded by another one.

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
| LD_LIBRARY_PATH | Process-local loader search path used only for a documented local module or service check; do not set it globally. |
| APXS | APXS from the same host that will load the module. |
| CONNECTOR_BUILD_DIR | External materialized Autotools worktree for the repository Apache adapter. |
| HTTPD_BIN | httpd executable paired explicitly with APXS during configuration. |
| MODULE_PATH | Installed repository DSO resolved by APXS. |
| HTTPD_MODULE_DIR | Apache module directory reported by the selected APXS. |
| HTTPD_RUNTIME_ROOT | Private writable Apache runtime root for the standalone loopback instance. |
| HTTPD_DOCUMENT_ROOT | Private document root containing the explicit local test page. |
| HTTPD_MODULES | Generated module-load file for the standalone Apache instance. |
| HTTPD_CONFIG | Local standalone httpd configuration. |
| WORKDIR | External Apache source workspace. |
| VERSION | Selected Apache source release in the optional source path. |
| INSTALL_DIR | Private Apache installation prefix in the optional source path. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
