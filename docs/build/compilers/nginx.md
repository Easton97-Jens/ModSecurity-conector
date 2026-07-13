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

## 6. Prepare or build the host or proxy

The simple NGINX path uses only a work directory, an installation directory, and a deliberately modest number of build jobs. It builds the connector statically with the NGINX binary; it does not rebuild libmodsecurity.

1. Download NGINX.
2. Clone ModSecurity-nginx.
3. Run configure.
4. Run make.
5. Run make install.
6. Create nginx.conf.
7. Run nginx -t.
8. Run the curl test.

```sh
WORKDIR="$HOME/nginx-modsecurity"
INSTALL_DIR="$HOME/.local/nginx-modsecurity"
JOBS=2
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO https://nginx.org/download/nginx-1.31.2.tar.gz
tar -xzf nginx-1.31.2.tar.gz
git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git
cd nginx-1.31.2
./auto/configure --prefix="$INSTALL_DIR" --with-http_ssl_module --add-module="$WORKDIR/ModSecurity-nginx" --with-cc-opt="-I/usr/local/include" --with-ld-opt="-L/usr/local/lib"
make -j"$JOBS"
make install
cat > "$WORKDIR/modsecurity-local.conf" <<'EOF'
SecRuleEngine On
SecRule REQUEST_URI "@streq /blocked" "id:100001,phase:1,deny,status:403,log"
EOF
cat > "$INSTALL_DIR/conf/nginx.conf" <<EOF
events {}
http {
    server {
        listen 127.0.0.1:8080;
        location / {
            modsecurity on;
            modsecurity_rules_file "$WORKDIR/modsecurity-local.conf";
            return 200 "nginx modsecurity test\n";
        }
    }
}
EOF
"$INSTALL_DIR/sbin/nginx" -t -p "$INSTALL_DIR" -c conf/nginx.conf
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/blocked
"$INSTALL_DIR/sbin/nginx" -p "$INSTALL_DIR" -c conf/nginx.conf -s quit
```

## 7. Build and integrate the connector

NGINX and ModSecurity-nginx were cloned, configured, compiled, and installed together in the preceding simple build.

## 8. Configuration

The simple build above writes the local rule file and nginx.conf, then runs the required nginx configuration test.

For the complete directive-level contract, read the repository [NGINX configuration reference](../../../examples/nginx/configuration-reference.md) before adapting this local example.

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
"$INSTALL_DIR/sbin/nginx" -V
```

## 10. Local HTTP/1.1 functional test

Run only against loopback. A 200 response on `/` and a 403 response on `/blocked` demonstrate the local rule path; they do not establish a broader claim.

The simple build starts NGINX on loopback and uses curl for a normal and a blocked request before stopping it.

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

| Variable | Meaning |
| --- | --- |
| WORKDIR | Working directory for the NGINX source, connector, and local rule file. |
| INSTALL_DIR | Private NGINX installation directory. |
| JOBS | Deliberately modest number of parallel NGINX build jobs. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
