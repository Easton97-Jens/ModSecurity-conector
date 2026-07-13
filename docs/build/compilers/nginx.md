<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Manual source build: NGINX

**Language:** English | [Deutsch](nginx.de.md)

## 1. Purpose and selected integration path

This guide describes the manual development and integration build for `native-nginx-http-module` on NGINX. The manual source build is the primary path; the repository test path follows it as an automated verification route.

## 2. Build components

libmodsecurity v3, an official NGINX source release, the repository-owned dynamic NGINX connector, the Common integration, a local rule file, and a loopback NGINX instance.

## Connector in this repository

- [NGINX connector](../../../connectors/nginx/README.md)
- [NGINX module configuration](../../../connectors/nginx/config)
- [Productive NGINX sources](../../../connectors/nginx/src/)
- [Source mapping](../../../connectors/nginx/SOURCE_MAP.json)

This is the primary connector path for this guide: connectors/nginx/. The official host documentation in the following section explains only how to provide or build the host; it does not replace the connector source.

Section 7 builds this adapter-owned connector as the documented dynamic NGINX module; official host documentation only provides the NGINX host source or package context.

## 3. Official upstream documentation

- **Source and scope:** [Building nginx from Sources](https://nginx.org/en/docs/configure.html)
  The official configure options, including prefix paths, compatibility, compiler, and linker flags. Version scope: NGINX options are release-dependent; inspect `./auto/configure --help` for the selected source.
- **Source and scope:** [Official NGINX packages](https://nginx.org/en/linux_packages.html)
  Official distribution package repositories and package-install context; not an ABI-equivalence claim for a source-built module. Version scope: Package layout changes by distribution and release.

## Alternative: official upstream connector

The official upstream connector [ModSecurity-nginx](https://github.com/owasp-modsecurity/ModSecurity-nginx) is an alternative implementation.

This guide uses the connector in [`connectors/nginx/`](../../../connectors/nginx/README.md) by default because it contains the repository-owned Common integration, configuration, and tested adaptations. An upstream-only build is a different build path and is not automatically equivalent to the selected repository connector.

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

NGINX and the repository-owned NGINX connector are built afterwards.

The following connector commands assume the default system installation under `/usr/local`. For a user-local prefix, use the shared guide's advanced section and pass its include and library paths deliberately.

## 6. Provide the host or proxy

### Simple path

Download only the selected official NGINX host source. The repository source of truth currently pins `NGINX_RELEASE_TAG=release-1.31.2`, which corresponds to the official `1.31.2` archive below. This does not load a connector from another repository: the connector is already in this checkout under `connectors/nginx/`.

```sh
WORKDIR="$HOME/nginx-modsecurity"
VERSION="1.31.2"
```

#### Download and unpack the host source

This creates only the selected NGINX host source tree. Section 7 adds the repository-owned dynamic connector from the current checkout.

```sh
mkdir -p "$WORKDIR"
cd "$WORKDIR"
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz"
tar -xzf "nginx-$VERSION.tar.gz"
```

### What was installed or built?

No host binary or module has been built yet. The NGINX source is ready for Section 7, and the repository-owned connector remains in `connectors/nginx/` in this checkout.

### Check the result

This file proves that the selected upstream NGINX source input was obtained.

```sh
test -f "$WORKDIR/nginx-$VERSION/auto/configure"
```

### Source build and integrity checks

#### Optional: verify download and version

Import the NGINX release signing key from the official release site before verifying the detached signature. The repository framework records the matching `release-1.31.2` host provenance independently from this concise host flow.

```sh
curl -fLO "https://nginx.org/download/nginx-$VERSION.tar.gz.asc"
gpg --verify "nginx-$VERSION.tar.gz.asc" "nginx-$VERSION.tar.gz"
```

## 7. Build and integrate the connector

Section 6 provided only the NGINX host source. The adapter-owned connector is already in this checkout under `connectors/nginx/`; build it as the selected dynamic NGINX module. The Common and libmodsecurity paths below are explicit so the dynamic module is built from the same repository and engine inputs.

```sh
INSTALL_DIR="$HOME/.local/nginx-modsecurity"
JOBS=2
cd "$WORKDIR/nginx-$VERSION"
MSCONNECTOR_COMMON_INC="$CONNECTOR_ROOT/common/include" \
MSCONNECTOR_COMMON_SRC="$CONNECTOR_ROOT/common/src" \
MODSECURITY_INC="/usr/local/include" \
MODSECURITY_LIB="/usr/local/lib" \
./auto/configure \
  --prefix="$INSTALL_DIR" \
  --sbin-path="$INSTALL_DIR/sbin/nginx" \
  --modules-path="$INSTALL_DIR/modules" \
  --conf-path="$INSTALL_DIR/conf/nginx.conf" \
  --pid-path="$INSTALL_DIR/logs/nginx.pid" \
  --error-log-path="$INSTALL_DIR/logs/error.log" \
  --http-log-path="$INSTALL_DIR/logs/access.log" \
  --with-compat \
  --add-dynamic-module="$CONNECTOR_ROOT/connectors/nginx"
make -j"$JOBS"
make install
```

```sh
mkdir -p "$INSTALL_DIR/modules"
cp -a "objs/ngx_http_modsecurity_module.so" "$INSTALL_DIR/modules/"
```

## 8. Configuration

Create a local test rule and nginx.conf. The primary connector is a dynamic module, so nginx.conf loads it before the events and http blocks. This section writes configuration only; Section 10 validates and starts it.

```sh
RULES_FILE="$WORKDIR/modsecurity-local.conf"
NGINX_CONFIG="$INSTALL_DIR/conf/nginx.conf"
cat > "$RULES_FILE" <<'EOF'
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
```

For the complete directive-level contract, read the repository [NGINX configuration reference](../../../examples/nginx/configuration-reference.md) before adapting this local example.

## 9. Build and ABI validation

Validate the selected host, connector artifact, dynamic library resolution, and generated configuration before sending traffic.

```sh
test -x "$INSTALL_DIR/sbin/nginx"
test -f "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so"
"$INSTALL_DIR/sbin/nginx" -V
"$INSTALL_DIR/sbin/nginx" -V 2>&1 | grep -F -- "--add-dynamic-module=$CONNECTOR_ROOT/connectors/nginx"
file "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so"
ldd "$INSTALL_DIR/modules/ngx_http_modsecurity_module.so" | grep -F libmodsecurity
```

```sh
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

A startup or directive failure normally means the NGINX binary, dynamic-module configure arguments, repository connector, or installed library differ. Rebuild the pair together; do not combine it with an unrelated package installation.

## 16. Variables and placeholders

| Variable/placeholder | Meaning |
| --- | --- |
| CONNECTOR_ROOT | Git top level of this checkout; connector scripts are called from it. |
| RULES_FILE | Local test-rule file, not a CRS rule file. |
| VERIFIED_RUN_PARENT | External parent for a fresh repository-test checkout and its test artifacts. |
| run_id | Unique identifier for one repository-controlled full-lifecycle run. |
| NO_CRS_RUN_ID | Exported full-lifecycle identifier for the following Make invocation; it keeps evidence and runtime data separated. |
| MSCONNECTOR_COMMON_INC | Repository Common header directory passed to the NGINX module configuration. |
| MSCONNECTOR_COMMON_SRC | Repository Common source directory compiled into the NGINX module. |
| MODSECURITY_INC | libmodsecurity header directory selected from the shared build. |
| MODSECURITY_LIB | libmodsecurity library directory selected from the shared build. |
| NGINX_CONFIG | Local NGINX configuration for the loopback test. |
| WORKDIR | External NGINX host-source workspace. |
| VERSION | Selected official NGINX release. |
| INSTALL_DIR | Private NGINX installation prefix for the dynamic-module build. |
| JOBS | Deliberately small number of parallel NGINX build jobs. |

## 17. Boundaries and non-claims

These instructions describe a reproducible development and integration build. They are not a production release. They do not claim complete CRS coverage, a complete protocol or platform matrix, or package-path equivalence when a host patch, module, middleware, or service is absent.
