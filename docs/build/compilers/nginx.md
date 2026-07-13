<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: NGINX

**Language:** English | [Deutsch](nginx.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-nginx-http-module` on NGINX. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, an official NGINX source release, ModSecurity-nginx, the repository NGINX source integration, a dynamic module, a local rule file, and a loopback NGINX instance.

## 3. Official upstream documentation

- **Source and scope:** [Building nginx from Sources](https://nginx.org/en/docs/configure.html)
  The official configure options, including prefix paths, dynamic modules, compatibility, compiler, and linker flags. Version scope: NGINX options are release-dependent; inspect `./auto/configure --help` for the selected source.
- **Source and scope:** [Official NGINX packages](https://nginx.org/en/linux_packages.html)
  Official distribution package repositories and package-install context; not an ABI-equivalence claim for a source-built module. Version scope: Package layout changes by distribution and release.
- **Source and scope:** [ModSecurity repository](https://github.com/owasp-modsecurity/ModSecurity)
  The libmodsecurity v3 engine source. Version scope: The selected tag/commit is shown in the shared build section.
- **Source and scope:** [ModSecurity-nginx](https://github.com/owasp-modsecurity/ModSecurity-nginx)
  The official NGINX connector source consumed by `--add-dynamic-module`. Version scope: Pin it to a release tag or commit matching the selected NGINX source.

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

This is the deliberately small NGINX-plus-libmodsecurity build extracted from the relevant technical parts of the supplied reference script: isolated directories, compiler/linker paths, pinned sources, the connector, configure, build, installation, ABI checks, and provenance. The external script builds further optional modules and integrations; they are not required for this core build and are not covered here.

```sh
export NGINX_BUILD_BASE="$HOME/src/nginx-modsecurity"
export NGINX_VERSION="1.31.2"
export NGINX_ARCHIVE="nginx-$NGINX_VERSION.tar.gz"
export NGINX_URL="https://nginx.org/download/$NGINX_ARCHIVE"
export NGINX_SRC="$NGINX_BUILD_BASE/nginx"
export NGINX_PREFIX="$HOME/.local/nginx-modsecurity"
export MODSECURITY_NGINX_SRC="$NGINX_BUILD_BASE/ModSecurity-nginx"
export MODSECURITY_NGINX_REF="v1.0.4"
export MODSECURITY_NGINX_COMMIT="3f4b57df10ce43b1f1c722141f7621dc64838be8"
mkdir -p "$NGINX_BUILD_BASE"
cd "$NGINX_BUILD_BASE"
curl -fLO "$NGINX_URL"
curl -fLO "$NGINX_URL.asc"
# Import the NGINX release signing key from the official release site before verifying.
gpg --verify "${NGINX_ARCHIVE}.asc" "$NGINX_ARCHIVE"
tar -xzf "$NGINX_ARCHIVE"
mv "nginx-$NGINX_VERSION" "$NGINX_SRC"
```

## 7. Build and integrate the connector

Clone and pin the official ModSecurity-nginx connector, then configure the host and connector together. `--add-module` links a connector into NGINX statically; `--add-dynamic-module` creates a separately loaded module. This guide uses the dynamic form and therefore keeps the module with the exact binary that built it.

```sh
cd "$CONNECTOR_ROOT"
```

```sh
git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git "$MODSECURITY_NGINX_SRC"
git -C "$MODSECURITY_NGINX_SRC" checkout --detach "$MODSECURITY_NGINX_REF"
test "$(git -C "$MODSECURITY_NGINX_SRC" rev-parse HEAD)" = "$MODSECURITY_NGINX_COMMIT"
git -C "$MODSECURITY_NGINX_SRC" rev-parse HEAD
cd "$NGINX_SRC"
./auto/configure --help | grep -E -- "--with-compat|--add-dynamic-module|--with-pcre-jit|--with-http_ssl_module"
./auto/configure --prefix="$NGINX_PREFIX" --sbin-path="$NGINX_PREFIX/sbin/nginx" --modules-path="$NGINX_PREFIX/modules" --conf-path="$NGINX_PREFIX/conf/nginx.conf" --pid-path="$NGINX_PREFIX/logs/nginx.pid" --http-log-path="$NGINX_PREFIX/logs/access.log" --error-log-path="$NGINX_PREFIX/logs/error.log" --with-http_ssl_module --with-pcre-jit --with-compat --add-dynamic-module="$MODSECURITY_NGINX_SRC" --with-cc-opt="-I$MODSECURITY_PREFIX/include" --with-ld-opt="-L$MODSECURITY_PREFIX/lib -Wl,-rpath,$MODSECURITY_PREFIX/lib"
./objs/nginx -V 2>&1 || true
grep -E '^(CC|LD|CORE_LIBS)' objs/Makefile || true
make -j"$jobs" V=1 2>&1 | tee nginx-build.log
make modules
make install
export NGINX_MODULE="$NGINX_PREFIX/modules/ngx_http_modsecurity_module.so"
test -x "$NGINX_PREFIX/sbin/nginx"
test -f "$NGINX_MODULE"
```

## 8. Configuration

The local rule below is a test rule, not a CRS rule. Keep the configuration and runtime files outside the Git checkout.

For the complete directive-level contract, read the repository [NGINX configuration reference](../../../examples/nginx/configuration-reference.md) before adapting this local example.

```sh
export RULES_FILE="$NGINX_BUILD_BASE/modsecurity-local.conf"
export NGINX_CONFIG="$NGINX_PREFIX/conf/nginx.conf"
cat > "$RULES_FILE" <<EOF
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$NGINX_CONFIG" <<EOF
load_module modules/ngx_http_modsecurity_module.so;
events {}
http {
    server {
        listen 127.0.0.1:8080;
        location / {
            modsecurity on;
            modsecurity_rules_file "$RULES_FILE";
            return 200 "nginx modsecurity test\n";
        }
    }
}
EOF
"$NGINX_PREFIX/sbin/nginx" -t -p "$NGINX_PREFIX" -c conf/nginx.conf
```

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$NGINX_PREFIX/sbin/nginx" -V
file objs/nginx
ldd objs/nginx
find objs -maxdepth 2 -type f -name "*modsecurity*.so" -print
file "$NGINX_PREFIX/sbin/nginx"
ldd "$NGINX_PREFIX/sbin/nginx"
file "$NGINX_MODULE"
ldd "$NGINX_MODULE" | grep -F libmodsecurity
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

```sh
"$NGINX_PREFIX/sbin/nginx" -p "$NGINX_PREFIX" -c conf/nginx.conf
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$NGINX_PREFIX/sbin/nginx" -p "$NGINX_PREFIX" -c conf/nginx.conf -s quit
{ "$NGINX_PREFIX/sbin/nginx" -V 2>&1; git -C "$MODSECURITY_SRC" rev-parse HEAD; git -C "$MODSECURITY_NGINX_SRC" rev-parse HEAD; cc --version; c++ --version; sha256sum "$NGINX_PREFIX/sbin/nginx"; } > "$NGINX_BUILD_BASE/build-provenance.txt"
```

## 11. Package-assisted path

Status: `package-assisted source build`. Package queries deliberately precede installation. Use only the line matching the distribution.

Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package.

```sh
apt-cache search nginx
dnf search nginx
nginx -V 2>&1 || true
```

An official package can provide a host, but a separately compiled dynamic module must match its exact NGINX build options and ABI. It is not interchangeable with this source-built binary/module pair. Check the official NGINX package page and the package's own `nginx -V` output before attempting a package-host module build.

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
make build-nginx
make check-config-nginx
make start-smoke-nginx
make runtime-smoke-nginx
run_id="nginx-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-nginx
NO_CRS_RUN_ID="$run_id" make evidence-check-nginx
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

A `load_module` failure normally means the NGINX binary, configure arguments, connector checkout, or module differ. Rebuild the pair together; do not copy the module into an unrelated package installation.

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
| NGINX_BUILD_BASE | External NGINX source/build/provenance directory. |
| NGINX_VERSION | Selected official NGINX release. |
| NGINX_ARCHIVE | Archive name derived from NGINX_VERSION. |
| NGINX_URL | Official NGINX archive URL. |
| NGINX_SRC | Unpacked NGINX source tree. |
| NGINX_PREFIX | Private NGINX installation prefix. |
| MODSECURITY_NGINX_SRC | Pinned ModSecurity-nginx checkout. |
| MODSECURITY_NGINX_REF | Release tag selected for the connector. |
| MODSECURITY_NGINX_COMMIT | Expected commit resolved from the connector tag. |
| NGINX_MODULE | Dynamic module built with this NGINX source. |
| NGINX_CONFIG | Local NGINX configuration for the loopback test. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
