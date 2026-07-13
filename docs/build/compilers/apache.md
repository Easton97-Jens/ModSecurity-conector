<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: Apache HTTP Server

**Language:** English | [Deutsch](apache.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-httpd-module` on Apache HTTP Server. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, Apache HTTP Server 2.4, APR/APR-util, PCRE2, the repository Apache adapter, APXS, a local rule file, and a loopback httpd instance.

## 3. Official upstream documentation

- **Source and scope:** [Compiling and Installing](https://httpd.apache.org/docs/2.4/install.html)
  Apache's official source release, APR/APR-util and PCRE2 prerequisites, configure, make, installation, start, and stop sequence. Version scope: HTTP Server 2.4; choose and verify the release again before building.
- **Source and scope:** [APXS](https://httpd.apache.org/docs/2.4/programs/apxs.html)
  The DSO build/install interface and the queries that bind a module to one httpd build. Version scope: HTTP Server 2.4 APXS reference.
- **Source and scope:** [Apache HTTP Server Download](https://httpd.apache.org/download.cgi)
  Official release archives, PGP signatures, checksums, and Apache KEYS. Version scope: The page changes when Apache publishes a release.
- **Source and scope:** [ModSecurity repository](https://github.com/owasp-modsecurity/ModSecurity)
  The libmodsecurity v3 source and its Autotools build instructions. Version scope: The selected Git tag/commit is recorded below.

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

Follow Apache's source-release flow first. Either provide matching system APR/APR-util development inputs, or unpack verified APR and APR-util trees as `srclib/apr` and `srclib/apr-util` before configuring httpd. The latter is Apache's documented bundled-APR layout.

```sh
export HOST_BUILD_BASE="$BUILD_BASE/apache"
export HTTPD_VERSION="2.4.68"
export HTTPD_ARCHIVE="httpd-$HTTPD_VERSION.tar.gz"
export HTTPD_URL="https://downloads.apache.org/httpd/$HTTPD_ARCHIVE"
export HTTPD_PREFIX="$HOME/.local/httpd-modsecurity"
export HTTPD_SRC="$HOST_BUILD_BASE/httpd-$HTTPD_VERSION"
export APXS="$HTTPD_PREFIX/bin/apxs"
mkdir -p "$HOST_BUILD_BASE"
cd "$HOST_BUILD_BASE"
curl -fLO "$HTTPD_URL"
curl -fLO "$HTTPD_URL.asc"
curl -fLO "$HTTPD_URL.sha256"
sha256sum -c "${HTTPD_ARCHIVE}.sha256"
# Import Apache KEYS through the official download page before this verification.
gpg --verify "${HTTPD_ARCHIVE}.asc" "$HTTPD_ARCHIVE"
tar -xzf "$HTTPD_ARCHIVE"
cd "$HTTPD_SRC"
# If APR/APR-util are not supplied by the system, place verified trees in srclib/apr and srclib/apr-util.
./configure --help | grep -E -- "--prefix|--with-included-apr|--with-pcre|--enable-mods-shared"
./configure --prefix="$HTTPD_PREFIX" --enable-mods-shared=most --with-pcre="$(command -v pcre2-config)"
make -j"$jobs"
make install
test -x "$HTTPD_PREFIX/bin/httpd"
test -x "$HTTPD_PREFIX/bin/apachectl"
test -x "$APXS"
```

## 7. Build and integrate the connector

The repository adapter is an Autotools/APXS project. Configure it with the APXS and httpd that were just built; APXS reads the compiler, include, and module-directory values of that exact host.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
export CONNECTOR_SRC="$CONNECTOR_ROOT/connectors/apache"
cd "$CONNECTOR_SRC"
./autogen.sh
./configure --with-libmodsecurity="$MODSECURITY_PREFIX" --with-apxs="$APXS" --with-apache="$HTTPD_PREFIX/bin/httpd"
make -j"$jobs"
make install
export MODULE_PATH="$("$APXS" -q LIBEXECDIR)/mod_security3.so"
test -f "$MODULE_PATH"
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep the configuration and runtime files outside the Git checkout.



```sh
export RULES_FILE="$HOST_BUILD_BASE/modsecurity-local.conf"
export HTTPD_CONFIG="$HOST_BUILD_BASE/httpd-local.conf"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$HTTPD_CONFIG" <<EOF
ServerRoot "$HTTPD_PREFIX"
Listen 127.0.0.1:8080
ServerName 127.0.0.1
LoadModule security3_module "$MODULE_PATH"
DocumentRoot "$HTTPD_PREFIX/htdocs"
<Directory "$HTTPD_PREFIX/htdocs">
    Require all granted
</Directory>
<Location "/">
    modsecurity on
    modsecurity_rules_file "$RULES_FILE"
</Location>
EOF
"$HTTPD_PREFIX/bin/httpd" -t -f "$HTTPD_CONFIG"
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$HTTPD_PREFIX/bin/httpd" -v
"$HTTPD_PREFIX/bin/apachectl" -V
"$HTTPD_PREFIX/bin/httpd" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -M | grep -E "(^|[[:space:]])so_module"
"$APXS" -q PREFIX
"$APXS" -q INCLUDEDIR
"$APXS" -q LIBEXECDIR
"$APXS" -q CC
file "$MODULE_PATH"
ldd "$MODULE_PATH" | grep -F libmodsecurity
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

```sh
"$HTTPD_PREFIX/bin/httpd" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -k start
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$HTTPD_PREFIX/bin/httpd" -d "$HTTPD_PREFIX" -f "$HTTPD_CONFIG" -k stop
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

If `apxs -q` points at different headers or a different module directory than the running httpd, stop and rebuild the adapter. A module built against one Apache ABI must not be loaded by another one.

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
| HTTPD_VERSION | Selected Apache 2.4 release; revalidate against the download page. |
| HTTPD_ARCHIVE | Release archive filename derived from HTTPD_VERSION. |
| HTTPD_URL | Official Apache archive URL. |
| HTTPD_PREFIX | Private httpd installation prefix. |
| HTTPD_SRC | Unpacked Apache source tree. |
| APXS | APXS from the same host that will load the module. |
| CONNECTOR_SRC | Repository Apache connector source selected from CONNECTOR_ROOT. |
| MODULE_PATH | Installed repository DSO resolved by APXS. |
| HTTPD_CONFIG | Local standalone httpd configuration. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
