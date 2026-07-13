<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: NGINX

**Language:** English | [Deutsch](nginx.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-nginx-http-module` on NGINX. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, an official NGINX source release, ModSecurity-nginx, a statically integrated NGINX module, a local rule file, and a loopback NGINX instance.

## 3. Official upstream documentation

- **Source and scope:** [Building nginx from Sources](https://nginx.org/en/docs/configure.html)
  The official configure options, including prefix paths, compatibility, compiler, and linker flags. Version scope: NGINX options are release-dependent; inspect `./auto/configure --help` for the selected source.
- **Source and scope:** [Official NGINX packages](https://nginx.org/en/linux_packages.html)
  Official distribution package repositories and package-install context; not an ABI-equivalence claim for a source-built module. Version scope: Package layout changes by distribution and release.
- **Source and scope:** [ModSecurity-nginx](https://github.com/owasp-modsecurity/ModSecurity-nginx)
  The official NGINX connector source consumed by the NGINX configure step. Version scope: Pin it to a release tag or commit matching the selected NGINX source.

## 4. Prerequisites

Build libmodsecurity first with the shared guide. Then install the selected host's documented development tools and keep the host, connector, headers, and libraries compatible.

```sh
command -v git cc c++ make
export CONNECTOR_ROOT="$(git rev-parse --show-toplevel)"
test -f "$CONNECTOR_ROOT/Makefile"
```

## 5. Prepare libmodsecurity v3

Install libmodsecurity v3 first:

[Simple libmodsecurity v3 build](libmodsecurity.md)

NGINX and ModSecurity-nginx are built afterwards.

The following connector commands assume the default system installation under `/usr/local`. For a user-local prefix, use the shared guide's advanced section and pass its include and library paths deliberately.

## 6. Provide the host or proxy

### Simple path

Download the selected NGINX source and the ModSecurity-nginx connector source. This only prepares the inputs; Section 7 performs the static connector build.

```sh
WORKDIR="$HOME/nginx-modsecurity"
VERSION="1.31.2"
```

#### Download the host and connector sources

The two source trees are all that Section 7 needs to configure NGINX with the connector.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz"
tar -xzf "nginx-$VERSION.tar.gz"
git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git
```

### What was installed or built?

No host binary or module has been built yet. The NGINX source and ModSecurity-nginx checkout are ready for the connector integration in Section 7.

### Check the result

Both files prove that the expected upstream source inputs were obtained.

```sh
test -f "$WORKDIR/nginx-$VERSION/auto/configure"
test -f "$WORKDIR/ModSecurity-nginx/config"
```

### Source build and integrity checks

#### Optional: verify download and version

Import the NGINX release signing key from the official release site before verifying the detached signature. The connector tag and resolved commit are recorded separately from the beginner flow.

```sh
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz.asc"
gpg --verify "nginx-$VERSION.tar.gz.asc" "nginx-$VERSION.tar.gz"
git -C "$WORKDIR/ModSecurity-nginx" checkout --detach v1.0.4
test "$(git -C "$WORKDIR/ModSecurity-nginx" rev-parse HEAD)" = "3f4b57df10ce43b1f1c722141f7621dc64838be8"
```

## 7. Build and integrate the connector

Section 6 provided the NGINX and ModSecurity-nginx source trees. Build them together now with the connector statically linked into the selected NGINX binary.

```sh
INSTALL_DIR="$HOME/.local/nginx-modsecurity"
JOBS=2
cd "$WORKDIR/nginx-$VERSION"
./auto/configure --prefix="$INSTALL_DIR" --with-http_ssl_module --add-module="$WORKDIR/ModSecurity-nginx" --with-cc-opt="-I/usr/local/include" --with-ld-opt="-L/usr/local/lib"
make -j"$JOBS"
make install
```

```sh
test -x "$INSTALL_DIR/sbin/nginx"
```

## 8. Configuration

Create a local test rule and nginx.conf. This section writes configuration only; Section 10 validates and starts it.

```sh
RULES_FILE="$WORKDIR/modsecurity-local.conf"
NGINX_CONFIG="$INSTALL_DIR/conf/nginx.conf"
cat > "$RULES_FILE" <<'EOF'
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$NGINX_CONFIG" <<EOF
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
```

For the complete directive-level contract, read the repository [NGINX configuration reference](../../../examples/nginx/configuration-reference.md) before adapting this local example.

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$INSTALL_DIR/sbin/nginx" -V
test -x "$INSTALL_DIR/sbin/nginx"
"$INSTALL_DIR/sbin/nginx" -V 2>&1 | grep -F -- "--add-module=$WORKDIR/ModSecurity-nginx"
test -f "$RULES_FILE"
test -f "$NGINX_CONFIG"
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

Run the syntax check first, then start the local host, send one ordinary and one blocked loopback request, and stop it.

```sh
"$INSTALL_DIR/sbin/nginx" -t -p "$INSTALL_DIR" -c conf/nginx.conf
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf -s quit
```

## 11. Package-assisted path

Status: `package-assisted source build`. Package queries deliberately precede installation. Use only the line matching the distribution.

Treat the host package, its matching development/API package, and connector build dependencies as separate inputs. The queries below establish local availability before a package name is selected; the final command prints the candidate host version. The connector component described above remains a source build whenever the selected module, service, middleware, or host patch is not part of that package.

```sh
apt-cache search nginx
dnf search nginx
nginx -V 2>&1 || true
```

An official package can provide a host, but it is not interchangeable with this source-built NGINX/connector pair. Check the official NGINX package page and the package's own `nginx -V` output before choosing a different host build.

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

A startup or directive failure normally means the NGINX binary, configure arguments, connector checkout, or installed library differ. Rebuild the pair together; do not combine it with an unrelated package installation.

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
| NGINX_CONFIG | Local NGINX configuration for the loopback test. |
| WORKDIR | NGINX source and connector workspace. |
| VERSION | Selected official NGINX release. |
| INSTALL_DIR | Private static NGINX installation prefix. |
| JOBS | Deliberately small number of parallel NGINX build jobs. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
