<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build, source-build, and package paths: Envoy

**Language:** English | [Deutsch](envoy.de.md)

## Purpose and current integration route

This guide documents the selected integration route `ext_proc` for
Envoy: streamed Envoy external-processing service with a Common/libmodsecurity bridge. The canonical core run is `make full-lifecycle-envoy-ext-proc`. Build,
configuration, start, and compatibility smokes remain separate from it.

## Compare the three paths

| Path | For whom? | System-wide changes | Builds host from source? | Core path possible? | Evidence possible? |
| --- | --- | --- | --- | --- | --- |
| Repository test path | Development and CI | No | Repository-controlled | Yes | Yes, after full lifecycle |
| Local source build | Development and integration | Optional | Verified binary; service from source | Yes | Yes, selected run only |
| Package path | Quick local start | Yes | Usually no | Only with source portion | Only matching profile and run |

The exact package status for this connector is
`package-assisted source build`. Packages provide dependencies and possibly a host, while the repository connector or host integration remains a source build. Package installation alone is not selected-core evidence.

## Shared prerequisites

Git, a writable external parent, Go and C/C++ build tools, libmodsecurity inputs, and the Framework submodule. The specific preparation target obtains only the pinned host binary through repository policy.

The test and source paths need only base tools and a writable external parent,
not a global installation of the selected connector. Query availability before
installing a package:

```sh
# Debian / Ubuntu (apt)
apt-cache policy build-essential pkg-config git curl ca-certificates
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
dnf info gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
```

On one machine, run only the line for its matching distribution family.

`VERIFIED_RUN_PARENT` must stay outside the Git checkout. It holds build,
cache, runtime, log, and evidence files and must not contain secrets in its
name. `CACHE_ROOT` is Cache-v2 with reusable inputs, not canonical evidence.
Show the prepared, effective sources with:

```sh
make runtime-components-inventory
make runtime-components-sources
```

## Path 1: Repository-controlled test

Git, a writable external parent, Go and C/C++ build tools, libmodsecurity inputs, and the Framework submodule. The specific preparation target obtains only the pinned host binary through repository policy.

These commands clone the defined branch, initialize the Framework, and run all
separate stages. They do not install a connector system-wide. If base tools are
missing, first query their availability in the package path and install only
the base packages shown there.

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
git switch feature/all-connectors-no-crs-baseline
git submodule update --init --recursive
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
export VERIFIED_RUN_ROOT="$VERIFIED_RUN_PARENT/ModSecurity-conector-verified"
export CACHE_ROOT="$VERIFIED_RUN_ROOT/cache-v2"
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build"
make check-framework
make prepare-runtime-components
make prepare-envoy-runtime
make build-envoy
make check-config-envoy
make start-smoke-envoy
make runtime-smoke-envoy
run_id="envoy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
```

| Command | Purpose | Prerequisite | Output/location | Exit and evidence boundary |
| --- | --- | --- | --- | --- |
| `git clone` / `git switch` / `git submodule update` | defined checkout | network access and Git | checkout with Framework submodule | Git failures are not build or runtime evidence. |
| `make check-framework` | check the Framework contract | initialized submodule | confirmed Framework path | `77` can report a missing Framework as BLOCKED; it is not a connector test. |
| `make prepare-runtime-components` + `make prepare-envoy-runtime` | prepare Cache-v2 and host/source inputs | writable external run root | provenance, cache, and prepared inputs | `77` means a deliberately blocked prerequisite; a cache is not evidence. |
| `make build-envoy` | build stage | preparation and toolchain | `$BUILD_ROOT/stages/envoy/build/results` | `0` is stage success, not config or traffic proof. |
| `make check-config-envoy` | load/check configuration | built host/connector | `$BUILD_ROOT/stages/envoy/config_load/results` | `0` is not a sent HTTP request. |
| `make start-smoke-envoy` | start host without full traffic | readable config and free local resources | `$BUILD_ROOT/stages/envoy/start_smoke/results` | `0` is not full-lifecycle evidence. |
| `make runtime-smoke-envoy` | run bounded repository-owned runtime smoke | prepared host and local ports | `$BUILD_ROOT/stages/envoy/minimal_runtime_smoke/results` | `0` applies only to this smoke. |
| `make full-lifecycle-envoy-ext-proc` | run selected No-CRS core lifecycle | safe run identifier | `$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/envoy/$run_id` | Assess canonical artifacts only after the following evidence check. |
| `make evidence-check-envoy` | validate existing canonical artifacts | same run identifier and complete artifacts | `$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/envoy/$run_id` | validates existing evidence; it creates no new logs or runtime files. |

`0` means success of the individual stage. `77` means a deliberately blocked
prerequisite, such as a missing Framework or unsuitable external root. `2` can
mean an invalid stage, connector, or input selection. Other nonzero values are
failed or propagated checks; do not interpret them as a stronger result.

### Validation

The preceding block uses the same `run_id` for configuration, start, the
HTTP/1.1 smoke, and the selected P1–P4 core lifecycle. The following commands
recheck the host, artifact, and dynamic library, repeat the repository-owned
config/start/runtime checks, and validate the evidence already produced. The
evidence check does not start a new core lifecycle.

```sh
test -x "$CACHE_ROOT/shared/envoy/bin/envoy"
"$CACHE_ROOT/shared/envoy/bin/envoy" --version
test -x "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"
ldd "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc" | grep -F libmodsecurity
make check-config-envoy
make start-smoke-envoy
make runtime-smoke-envoy
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
make runtime-components-inventory
make runtime-components-sources
```

## Path 2: Local source build

The repository builds the ext_proc service, CGo/Common bridge, and generated configuration from source. It does not maintain a tested full Envoy-host source build, so a verified pinned binary is used instead of an invented manual host build.

The Go module `connectors/envoy/ext_proc/go.mod` declares `go 1.24.0`. Check `go version` before building; a package name alone does not promise a compatible Go version.

These pins are inputs to the supported preparer. When a pin changes,
`runtime-components-inventory` and `runtime-components-sources` are
authoritative; in particular, a moving libmodsecurity reference is documented
there by its resolved commit.

| Component | Pin/version | Source | Integrity/commit |
| --- | --- | --- | --- |
| Envoy host binary | 1.38.2 (`ENVOY_VERSION`) | https://github.com/envoyproxy/envoy/releases/download/v1.38.2/envoy-1.38.2-linux-x86_64 | SHA256 `87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899` |
| repository ext_proc service | current checkout commit | connectors/envoy | Git commit plus external build provenance |
| libmodsecurity | configured `MODSECURITY_GIT_REF` (default `v3/master`) | https://github.com/owasp-modsecurity/ModSecurity.git | resolved commit is recorded in Cache-v2 provenance |

`-O2 -g` is an understandable development value, not a repository default or
a deployment prescription. `jobs` is the number of parallel compiler
processes; choose a lower value such as `2` on a memory-constrained machine.
Set `CPPFLAGS`, `LDFLAGS`, `PKG_CONFIG_PATH`, and `LD_LIBRARY_PATH` only for
deliberately selected header, library, or staging paths.

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
export VERIFIED_RUN_ROOT="$VERIFIED_RUN_PARENT/ModSecurity-conector-verified"
export CACHE_ROOT="$VERIFIED_RUN_ROOT/cache-v2"
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build/envoy-source"
export CC=gcc
export CXX=g++
export CFLAGS="-O2 -g"
export CXXFLAGS="-O2 -g"
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')"
make check-framework
make prepare-runtime-components
make prepare-envoy-runtime
make runtime-components-inventory
make runtime-components-sources
run_id="envoy-source-$(date -u +%Y%m%dT%H%M%SZ)"
MAKE_JOBS="$jobs" make -C connectors/envoy build-envoy-ext-proc
MAKE_JOBS="$jobs" make -C connectors/envoy test-envoy-ext-proc
MAKE_JOBS="$jobs" make -C connectors/envoy check-envoy-ext-proc-config
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
```

The focused connector commands build and test the repository ext_proc service. The selected host remains the verified Envoy binary from preparation; `ext_authz` compatibility commands are not the selected route.

| Command group | Purpose | Prerequisite | Output and boundary |
| --- | --- | --- | --- |
| source-build commands above | build the selected host, module, or service from source | prepared provenance, toolchain, and external build root | artifacts and command/source-info records below `$BUILD_ROOT`; exit `0` is build success only. |
| shown config/test/runtime targets | check artifact, ABI, and loader in the same staging area | matching headers, libraries, and readable configuration | Targets check the generated module or service and its library resolution; `77` can report a missing prerequisite. |
| `make full-lifecycle-envoy-ext-proc` + evidence check | run selected core path and validate artifacts | safe `run_id` and complete runtime | evidence below `evidence/no-crs-evidence/envoy/$run_id`; `2` is invalid input/stage and other failures remain failures. |

The supported build is implemented by `connectors/envoy/build/build_ext_proc.sh`; root stages
dispatch through `ci/runtime/lifecycle/run-connector-stage.sh`, and the full
lifecycle through `ci/runtime/lifecycle/run-no-crs-baseline.sh`. Those scripts
are the implementation behind the shown Make targets, not a second manual
build recipe to copy independently.

The Envoy binary is a verified host input; the ext_proc executable is the repository-owned source build. Generated configuration, ports, CGo bridge, and libmodsecurity runtime library must stay in one external invocation root.

### Prefix and staging

| Location | Use | Boundary |
| --- | --- | --- |
| `/usr` | managed by a distribution package | do not overwrite it as a manual default |
| `/usr/local` | deliberate local installation | inventory files first |
| `/opt/modsecurity-connector` | deliberately selected isolated prefix | set `PKG_CONFIG_PATH` and loader path deliberately |
| `$HOME/.local` | user-local installation | not a shared system host |
| below `VERIFIED_RUN_PARENT` | recommended external staging | default for this development path; outside the checkout |

The supported preparer owns the exact upstream configure and installation
invocation. Its generated command, source-info, and artifact records in the
external build root are the reproducible configuration and compilation record;
this guide does not invent a second manual invocation.

### Validation

These commands inspect the resolved host binary at its documented external
staging or cache path after preparation or source build. The artifact commands
then check that the generated module or service exists and that `ldd` resolves
`libmodsecurity`. The supported targets then check link, configuration, start,
or the selected lifecycle.

```sh
test -x "$CACHE_ROOT/shared/envoy/bin/envoy"
"$CACHE_ROOT/shared/envoy/bin/envoy" --version
test -x "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"
ldd "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc" | grep -F libmodsecurity
go version
grep -Fx 'go 1.24.0' connectors/envoy/ext_proc/go.mod
make -C connectors/envoy check-envoy-ext-proc-config
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
```

## Path 3: Package or package-assisted installation

Status: `package-assisted source build`. Packages provide dependencies and possibly a host, while the repository connector or host integration remains a source build. Package installation alone is not selected-core evidence.

Checked package names cover build dependencies, not an equivalent selected Envoy host. Any distribution Envoy package still lacks the repository ext_proc service and must be verified separately.

Package names are release-dependent. Query them before every installation;
Fedora `mod_security` is ModSecurity v2 and is not a replacement for the
v3-path `libmodsecurity-devel` package.

The first commands are for **Debian / Ubuntu (apt)**; the following commands
are for **Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)**. Use only the matching
family.

```sh
# Debian / Ubuntu (apt)
apt-cache policy build-essential pkg-config git curl ca-certificates
apt-cache policy golang-go protobuf-compiler libprotobuf-dev libgrpc-dev libmodsecurity-dev
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
dnf info gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
dnf info golang protobuf-devel grpc-devel libmodsecurity-devel
# Host-package availability inquiry only; no package is selected by this query
apt-cache search '^envoy$'
dnf search envoy
```

The final query lines only discover whether a distribution offers an Envoy host package; no result is treated as the selected host, because the repository uses its verified binary plus the source-built ext_proc service.

Install only after a successful query and after reviewing the list yourself:

```sh
# Debian / Ubuntu (apt)
sudo apt update
sudo apt install --yes build-essential pkg-config git curl ca-certificates
sudo apt install --yes golang-go protobuf-compiler libprotobuf-dev libgrpc-dev libmodsecurity-dev
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
sudo dnf install -y gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
sudo dnf install -y golang protobuf-devel grpc-devel libmodsecurity-devel
```

`sudo` is used because package databases and system paths normally require
administrator privileges. A CI job or container often already runs as root;
in that case omit `sudo` instead of changing the package list.

Packages provide only the dependency/host portion. Continue with this supported source follow-up; package installation alone does not build the selected connector or host integration.

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
export VERIFIED_RUN_ROOT="$VERIFIED_RUN_PARENT/ModSecurity-conector-verified"
export CACHE_ROOT="$VERIFIED_RUN_ROOT/cache-v2"
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build/envoy-package"
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')"
make check-framework
make prepare-runtime-components
make prepare-envoy-runtime
make runtime-components-inventory
make runtime-components-sources
run_id="envoy-package-$(date -u +%Y%m%dT%H%M%SZ)"
MAKE_JOBS="$jobs" make -C connectors/envoy build-envoy-ext-proc
MAKE_JOBS="$jobs" make -C connectors/envoy test-envoy-ext-proc
MAKE_JOBS="$jobs" make -C connectors/envoy check-envoy-ext-proc-config
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
```

| Command group | Purpose | Prerequisite | Output and boundary |
| --- | --- | --- | --- |
| source-build commands above | build the selected host, module, or service from source | prepared provenance, toolchain, and external build root | artifacts and command/source-info records below `$BUILD_ROOT`; exit `0` is build success only. |
| shown config/test/runtime targets | check artifact, ABI, and loader in the same staging area | matching headers, libraries, and readable configuration | Targets check the generated module or service and its library resolution; `77` can report a missing prerequisite. |
| `make full-lifecycle-envoy-ext-proc` + evidence check | run selected core path and validate artifacts | safe `run_id` and complete runtime | evidence below `evidence/no-crs-evidence/envoy/$run_id`; `2` is invalid input/stage and other failures remain failures. |

### Validation

`libmodsecurity` must provide v3 development headers and pkg-config metadata.
If any of these commands is unavailable, return to the repository-controlled
source build; never silently use a ModSecurity-v2 package.

```sh
pkg-config --exists libmodsecurity
pkg-config --atleast-version=3.0 libmodsecurity
pkg-config --modversion libmodsecurity
pkg_version="$(pkg-config --modversion libmodsecurity)"
case "$pkg_version" in 3.*) ;; *) printf '%s\n' "libmodsecurity major version must be 3: $pkg_version" >&2; exit 1 ;; esac
pkg-config --cflags libmodsecurity
pkg-config --libs libmodsecurity
make check-config-envoy
test -x "$CACHE_ROOT/shared/envoy/bin/envoy"
"$CACHE_ROOT/shared/envoy/bin/envoy" --version
test -x "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc"
ldd "$BUILD_ROOT/envoy-ext-proc/msconnector_envoy_ext_proc" | grep -F libmodsecurity
go version
grep -Fx 'go 1.24.0' connectors/envoy/ext_proc/go.mod
make -C connectors/envoy check-envoy-ext-proc-config
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
```

## Configure after the build

The config target checks the repository service and generated Envoy ext_proc configuration; it does not declare a system Envoy package equivalent.

The selected configuration, rules, and module paths are generated or checked
by repository-owned targets. Configuration files must be readable; do not put
cookies, authorization values, tokens, private keys, or raw logs into config
or evidence.

```sh
make check-config-envoy
```

## Validate build and installation

For every path: inspect the host binary and version, inspect connector output
and shared libraries in the selected staging area, then run config and start
smokes. The source and package paths therefore each end in their own validation
block; a compile or link by itself is insufficient.

```sh
make check-config-envoy
make start-smoke-envoy
make runtime-smoke-envoy
```

## Run a real HTTP/1.1 test

`make runtime-smoke-envoy` is the supported repository-owned minimal smoke with
real HTTP/1.1 traffic for its documented route. Concrete local ports, URLs,
and requests come from generated configuration; do not invent a second `curl`
endpoint. Run the full lifecycle for the selected P1–P4 core path where
applicable:

```sh
run_id="envoy-http11-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
```

The minimal smoke and the full lifecycle have different boundaries. A P1 deny,
P2/P3/P4 observation, or PASS applies only to the repository-defined case that
actually ran and is not expanded here into a general capability statement.

## Inspect evidence and logs

After a full lifecycle, derived run-bound directories are below
`$VERIFIED_RUN_ROOT`: evidence at
`evidence/no-crs-evidence/envoy/$run_id`, build files at
`build/envoy/$run_id`, runtime files at `runs/envoy/$run_id`, and sanitized
logs at `run-logs/envoy/$run_id`. General stage results are below
`$BUILD_ROOT/stages/envoy`. These are derived paths, not fixed system paths.

```sh
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
make runtime-components-inventory
make runtime-components-sources
```

Share evidence only after the check and remove sensitive values first. Caches
and downloads are reusable inputs, not evidence.

## Update and rebuild

Update a checkout deliberately, then recheck submodules and provenance. Do not
treat an old cache as proof for changed pins.

```sh
git pull --ff-only
git submodule update --init --recursive
make runtime-components-inventory
make runtime-components-sources
make check-framework
make prepare-runtime-components
make prepare-envoy-runtime
make build-envoy
```

## Uninstall and clean up

Repository test path: inspect or archive desired evidence before emptying the
external `VERIFIED_RUN_PARENT`; the Git checkout stays unchanged. `rmdir` only
removes empty directories, so it is the safe final operation instead of an
uncontrolled recursive delete.

```sh
find "$VERIFIED_RUN_PARENT" -maxdepth 1 -mindepth 1 -print
rmdir "$VERIFIED_RUN_PARENT"
```

Source build: remove external staging or a deliberately selected prefix only
after inventorying it. Do not broadly remove an installation below `/usr` or
`/usr/local`. Package path: remove only connector packages actually installed
by the operator; do not delete user data or evidence without review.

```sh
sudo apt remove golang-go protobuf-compiler libprotobuf-dev libgrpc-dev
sudo dnf remove golang protobuf-devel grpc-devel
```

## Troubleshooting

### Repository test path

For exit `77`, first check the Framework submodule, absolute external root,
missing base tools, and cache provenance. For exit `2`, check connector, stage,
and run-id input. If a port is occupied, stop the previous local process in an
orderly way and repeat with a new run ID; do not blindly mix or rename cache
entries.

### Source build

For a missing compiler or header, check source prerequisites and the selected
toolchain. If pkg-config cannot find libmodsecurity, check the header/library
root and `PKG_CONFIG_PATH`. For ABI or module failures, build host, headers,
module, prefix, and connector together from the same prepared source. For a
missing shared library, check only the deliberate staging path and
`LD_LIBRARY_PATH`; do not globally copy files.

### Package path

Query release availability again before installation. Use the source build if
v3 headers or pkg-config metadata are absent. An unreadable configuration,
wrong file permission, or occupied port is not package proof. Do not combine a
package host with a source module that has a different ABI.

## Variables and placeholders

| Variable/placeholder | Required | Default | Example | Meaning |
| --- | --- | --- | --- | --- |
| VERIFIED_RUN_PARENT | yes | chosen by Make when unset | $HOME/modsecurity-connector-work | Writable external parent for build, cache, runtime, logs, and evidence; outside the checkout and without secrets in its name. |
| VERIFIED_RUN_ROOT | no | derived below VERIFIED_RUN_PARENT | $HOME/modsecurity-connector-work/ModSecurity-conector-verified | Run-bound external root; holds derived build, run, log, and evidence paths. |
| BUILD_ROOT | no | derived below verified run | external build subdirectory | Staging and build output; keep it outside the Git checkout. |
| CACHE_ROOT | no | derived as cache-v2 below verified run | external cache-v2 subdirectory | Reusable inputs; not a PASS and not canonical evidence. |
| NO_CRS_RUN_ID | for full lifecycle | empty | nginx-core-20260712T120000Z | Filesystem-safe name of one evidence run; use it for both full lifecycle and evidence check. |
| CC | no | toolchain default | gcc | C compiler for C and CGo-adjacent build steps. |
| CXX | no | toolchain default | g++ | C++ compiler for dependencies that need it. |
| CFLAGS | no | toolchain default | -O2 -g | Additional C flags; example is a development value, not a repository or production default. |
| CXXFLAGS | no | toolchain default | -O2 -g | Additional C++ flags; not a production profile. |
| CPPFLAGS | no | empty or toolchain default | -I/opt/modsecurity-connector/include | Additional include flags for deliberately selected header paths. |
| LDFLAGS | no | empty or toolchain default | -L/opt/modsecurity-connector/lib | Additional linker flags for deliberately selected library paths. |
| PKG_CONFIG_PATH | no | package-manager/toolchain default | /opt/modsecurity-connector/lib/pkgconfig | Additional pkg-config metadata search path; not an ABI substitute. |
| LD_LIBRARY_PATH | no | loader default | /opt/modsecurity-connector/lib | Temporary shared-library search path; not a global installation. |
| MAKE_JOBS | no | detected by Framework | 2 | Number of parallel compiler processes; choose lower on a memory-constrained machine. |
| HOME | no | login home directory | $HOME | Shell value for user home directory; no local developer path. |
| jobs | no | unset | 2 | Local shell variable from `getconf`, passed to `MAKE_JOBS`. |
| run_id | no | unset | apache-core-20260712T120000Z | Local shell variable used to set `NO_CRS_RUN_ID`. |
| ENVOY_BIN | no | generated external cache binary | verified external Envoy binary | Resolved host binary for pinned Envoy release. |
| EXT_PROC_CONFIG | no | connector configuration file | connector ext_proc configuration | Repository ext_proc service config used by checks. |
| EXT_PROC_RUNTIME_CONFIG | no | derived external runtime file | external runtime config | Generated selected ext_proc runtime configuration. |
| EXT_PROC_RUNTIME_ROOT | no | derived under BUILD_ROOT | external ext_proc runtime directory | Runtime files and event logs for ext_proc. |
| RULES_FILE | no | connector default | absolute rules file | Rules-file input for local connector diagnostics; canonical runs provide their own selected rules. |
| MSCONNECTOR_RULES_FILE | no | unset | absolute no-CRS rules file | Canonical rule input when the selected runtime exports it. |
| ENVOY_TRANSPORT_CANCEL_PROBE | no | 0 | 1 | Opt-in cancellation probe; it is not a client-visible strict-reset claim. |

| Documented value | Example | Meaning |
| --- | --- | --- |
| connector name | envoy | Make and evidence name for this guide; no placeholder remains in the shown commands. |
| source directory | below `$BUILD_ROOT` or prepared provenance | Source created by the supported preparer; do not substitute a second manual checkout. |
| build directory | `$BUILD_ROOT/stages/envoy` | Staging and stage results outside the checkout. |
| installation prefix | external staging below `VERIFIED_RUN_PARENT` | Preferred development location instead of a system-wide installation. |
| rules file | provided by the full-lifecycle dispatcher | The selected run supplies canonical rules; do not present a local file as equivalent. |
| module/host binary | resolved by preparation or source build | Path, headers, and ABI belong to the same selected host. |

## Limitations and non-claims

These instructions describe reproducible development, test, and build paths.
They are not an assessment of a production package or hardened deployment
guidance. They do not assert complete CRS coverage, a complete protocol or
platform matrix, or a security property beyond the documented run. A package
path is equivalent only when the selected host, module, middleware, service,
or patch path actually ran and was checked through the documented full
lifecycle.
