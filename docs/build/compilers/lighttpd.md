<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build, source-build, and package paths: lighttpd

**Language:** English | [Deutsch](lighttpd.de.md)

## Purpose and current integration route

This guide documents the selected integration route `patched-native` for
lighttpd: patched native lighttpd host and matching connector module. The canonical core run is `make full-lifecycle-lighttpd-patched`. Build,
configuration, start, and compatibility smokes remain separate from it.

## Compare the three paths

| Path | For whom? | System-wide changes | Builds host from source? | Core path possible? | Evidence possible? |
| --- | --- | --- | --- | --- | --- |
| Repository test path | Development and CI | No | Repository-controlled | Yes | Yes, after full lifecycle |
| Local source build | Development and integration | Optional | Yes, patched source | Yes | Yes, selected run only |
| Package path | Quick local start | Yes | Usually no | No, not package-only | Only matching profile and run |

The exact package status for this connector is
`selected profile not available package-only`. Packages can help with dependencies or a comparison host, but no ordinary package supplies the selected profile. Build it through the repository route.

## Shared prerequisites

Git, a writable external parent, C/C++ build tools, patch/build prerequisites, libmodsecurity inputs, and the Framework submodule. The explicit lighttpd preparation target enables the pinned source-build route.

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

Git, a writable external parent, C/C++ build tools, patch/build prerequisites, libmodsecurity inputs, and the Framework submodule. The explicit lighttpd preparation target enables the pinned source-build route.

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
make prepare-lighttpd-runtime-build
make build-lighttpd
make check-config-lighttpd
make start-smoke-lighttpd
make runtime-smoke-lighttpd
run_id="lighttpd-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
```

| Command | Purpose | Prerequisite | Output/location | Exit and evidence boundary |
| --- | --- | --- | --- | --- |
| `git clone` / `git switch` / `git submodule update` | defined checkout | network access and Git | checkout with Framework submodule | Git failures are not build or runtime evidence. |
| `make check-framework` | check the Framework contract | initialized submodule | confirmed Framework path | `77` can report a missing Framework as BLOCKED; it is not a connector test. |
| `make prepare-runtime-components` + `make prepare-lighttpd-runtime-build` | prepare Cache-v2 and host/source inputs | writable external run root | provenance, cache, and prepared inputs | `77` means a deliberately blocked prerequisite; a cache is not evidence. |
| `make build-lighttpd` | build stage | preparation and toolchain | `$BUILD_ROOT/stages/lighttpd/build/results` | `0` is stage success, not config or traffic proof. |
| `make check-config-lighttpd` | load/check configuration | built host/connector | `$BUILD_ROOT/stages/lighttpd/config_load/results` | `0` is not a sent HTTP request. |
| `make start-smoke-lighttpd` | start host without full traffic | readable config and free local resources | `$BUILD_ROOT/stages/lighttpd/start_smoke/results` | `0` is not full-lifecycle evidence. |
| `make runtime-smoke-lighttpd` | run bounded repository-owned runtime smoke | prepared host and local ports | `$BUILD_ROOT/stages/lighttpd/minimal_runtime_smoke/results` | `0` applies only to this smoke. |
| `make full-lifecycle-lighttpd-patched` | run selected No-CRS core lifecycle | safe run identifier | `$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/lighttpd/$run_id` | Assess canonical artifacts only after the following evidence check. |
| `make evidence-check-lighttpd` | validate existing canonical artifacts | same run identifier and complete artifacts | `$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/lighttpd/$run_id` | validates existing evidence; it creates no new logs or runtime files. |

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
test -x "$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/bin/lighttpd"
"$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/bin/lighttpd" -v
test -f "$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/modules/mod_msconnector.so"
ldd "$VERIFIED_RUN_ROOT/runs/lighttpd/$run_id/host-runtime/lighttpd-patched/stage/modules/mod_msconnector.so" | grep -F libmodsecurity
make check-config-lighttpd
make start-smoke-lighttpd
make runtime-smoke-lighttpd
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
make runtime-components-inventory
make runtime-components-sources
```

## Path 2: Local source build

The selected route needs lighttpd-1.4.84 source, the repository patchset, a patched core, and a module built against matching headers. The root targets own patch check/application, configuration, staging, and real-host execution.



These pins are inputs to the supported preparer. When a pin changes,
`runtime-components-inventory` and `runtime-components-sources` are
authoritative; in particular, a moving libmodsecurity reference is documented
there by its resolved commit.

| Component | Pin/version | Source | Integrity/commit |
| --- | --- | --- | --- |
| lighttpd host source | 1.4.84 (`LIGHTTPD_VERSION`) | https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.84.tar.xz | SHA256 `076dd43bec8f2ba9ce6db7e7ca7e8ad72271cd529805ead2400b56efaa026f70` |
| repository patchset | current checkout commit | connectors/lighttpd/patches | Git commit plus patch-check provenance |
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
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build/lighttpd-source"
export CC=gcc
export CXX=g++
export CFLAGS="-O2 -g"
export CXXFLAGS="-O2 -g"
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')"
make check-framework
make prepare-runtime-components
make prepare-lighttpd-runtime-build
make runtime-components-inventory
make runtime-components-sources
run_id="lighttpd-source-$(date -u +%Y%m%dT%H%M%SZ)"
LIGHTTPD_MAKE_JOBS="$jobs" make -C connectors/lighttpd check-lighttpd-core-patch
LIGHTTPD_MAKE_JOBS="$jobs" make -C connectors/lighttpd build-lighttpd-patched-host
LIGHTTPD_MAKE_JOBS="$jobs" make -C connectors/lighttpd check-lighttpd-patched-host
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
```

The focused commands verify the patch and build the matching patched host. `build-lighttpd` is a stock/compatibility module stage; the selected source path is the patched host executed by `full-lifecycle-lighttpd-patched`.

| Command group | Purpose | Prerequisite | Output and boundary |
| --- | --- | --- | --- |
| source-build commands above | build the selected host, module, or service from source | prepared provenance, toolchain, and external build root | artifacts and command/source-info records below `$BUILD_ROOT`; exit `0` is build success only. |
| shown config/test/runtime targets | check artifact, ABI, and loader in the same staging area | matching headers, libraries, and readable configuration | Targets check the generated module or service and its library resolution; `77` can report a missing prerequisite. |
| `make full-lifecycle-lighttpd-patched` + evidence check | run selected core path and validate artifacts | safe `run_id` and complete runtime | evidence below `evidence/no-crs-evidence/lighttpd/$run_id`; `2` is invalid input/stage and other failures remain failures. |

The supported build is implemented by `connectors/lighttpd/build/build_patched_core.sh`, `connectors/lighttpd/build/build_patched_host.sh`; root stages
dispatch through `ci/runtime/lifecycle/run-connector-stage.sh`, and the full
lifecycle through `ci/runtime/lifecycle/run-no-crs-baseline.sh`. Those scripts
are the implementation behind the shown Make targets, not a second manual
build recipe to copy independently.

The selected host is not stock lighttpd. Patch verification/application, core build, module build, Entity-Body hook, and module/header ABI are one source set. Do not load the module into a stock binary built from different headers.

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
test -x "$BUILD_ROOT/lighttpd-core-patched/stage/bin/lighttpd"
"$BUILD_ROOT/lighttpd-core-patched/stage/bin/lighttpd" -v
test -f "$BUILD_ROOT/lighttpd-core-patched/stage/modules/mod_msconnector.so"
ldd "$BUILD_ROOT/lighttpd-core-patched/stage/modules/mod_msconnector.so" | grep -F libmodsecurity
make -C connectors/lighttpd check-lighttpd-patched-host
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
```

## Path 3: Package or package-assisted installation

Status: `selected profile not available package-only`. Packages can help with dependencies or a comparison host, but no ordinary package supplies the selected profile. Build it through the repository route.

A lighttpd package can supply a comparison host and dependencies, but not the repository Entity-Body hook or matching patched core. It cannot be the selected profile package-only.

Package names are release-dependent. Query them before every installation;
Fedora `mod_security` is ModSecurity v2 and is not a replacement for the
v3-path `libmodsecurity-devel` package.

The first commands are for **Debian / Ubuntu (apt)**; the following commands
are for **Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)**. Use only the matching
family.

```sh
# Debian / Ubuntu (apt)
apt-cache policy build-essential pkg-config git curl ca-certificates
apt-cache policy libpcre2-dev zlib1g-dev libssl-dev libmodsecurity-dev lighttpd
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
dnf info gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
dnf info pcre2-devel zlib-devel openssl-devel libmodsecurity-devel lighttpd
```



Install only after a successful query and after reviewing the list yourself:

```sh
# Debian / Ubuntu (apt)
sudo apt update
sudo apt install --yes build-essential pkg-config git curl ca-certificates
sudo apt install --yes libpcre2-dev zlib1g-dev libssl-dev libmodsecurity-dev lighttpd
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
sudo dnf install -y gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
sudo dnf install -y pcre2-devel zlib-devel openssl-devel libmodsecurity-devel lighttpd
```

`sudo` is used because package databases and system paths normally require
administrator privileges. A CI job or container often already runs as root;
in that case omit `sudo` instead of changing the package list.

Packages provide only the dependency/host portion. Continue with this supported source follow-up; package installation alone does not build the selected connector or host integration.

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
export VERIFIED_RUN_ROOT="$VERIFIED_RUN_PARENT/ModSecurity-conector-verified"
export CACHE_ROOT="$VERIFIED_RUN_ROOT/cache-v2"
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build/lighttpd-package"
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')"
make check-framework
make prepare-runtime-components
make prepare-lighttpd-runtime-build
make runtime-components-inventory
make runtime-components-sources
run_id="lighttpd-package-$(date -u +%Y%m%dT%H%M%SZ)"
LIGHTTPD_MAKE_JOBS="$jobs" make -C connectors/lighttpd check-lighttpd-core-patch
LIGHTTPD_MAKE_JOBS="$jobs" make -C connectors/lighttpd build-lighttpd-patched-host
LIGHTTPD_MAKE_JOBS="$jobs" make -C connectors/lighttpd check-lighttpd-patched-host
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
```

| Command group | Purpose | Prerequisite | Output and boundary |
| --- | --- | --- | --- |
| source-build commands above | build the selected host, module, or service from source | prepared provenance, toolchain, and external build root | artifacts and command/source-info records below `$BUILD_ROOT`; exit `0` is build success only. |
| shown config/test/runtime targets | check artifact, ABI, and loader in the same staging area | matching headers, libraries, and readable configuration | Targets check the generated module or service and its library resolution; `77` can report a missing prerequisite. |
| `make full-lifecycle-lighttpd-patched` + evidence check | run selected core path and validate artifacts | safe `run_id` and complete runtime | evidence below `evidence/no-crs-evidence/lighttpd/$run_id`; `2` is invalid input/stage and other failures remain failures. |

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
make check-config-lighttpd
test -x "$BUILD_ROOT/lighttpd-core-patched/stage/bin/lighttpd"
"$BUILD_ROOT/lighttpd-core-patched/stage/bin/lighttpd" -v
test -f "$BUILD_ROOT/lighttpd-core-patched/stage/modules/mod_msconnector.so"
ldd "$BUILD_ROOT/lighttpd-core-patched/stage/modules/mod_msconnector.so" | grep -F libmodsecurity
make -C connectors/lighttpd check-lighttpd-patched-host
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
```

## Configure after the build

The config target performs the repository-managed lighttpd config check; the selected patched full lifecycle additionally checks the patched host before real requests.

The selected configuration, rules, and module paths are generated or checked
by repository-owned targets. Configuration files must be readable; do not put
cookies, authorization values, tokens, private keys, or raw logs into config
or evidence.

```sh
make check-config-lighttpd
```

## Validate build and installation

For every path: inspect the host binary and version, inspect connector output
and shared libraries in the selected staging area, then run config and start
smokes. The source and package paths therefore each end in their own validation
block; a compile or link by itself is insufficient.

```sh
make check-config-lighttpd
make start-smoke-lighttpd
make runtime-smoke-lighttpd
```

## Run a real HTTP/1.1 test

`make runtime-smoke-lighttpd` is the supported repository-owned minimal smoke with
real HTTP/1.1 traffic for its documented route. Concrete local ports, URLs,
and requests come from generated configuration; do not invent a second `curl`
endpoint. Run the full lifecycle for the selected P1–P4 core path where
applicable:

```sh
run_id="lighttpd-http11-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
```

The minimal smoke and the full lifecycle have different boundaries. A P1 deny,
P2/P3/P4 observation, or PASS applies only to the repository-defined case that
actually ran and is not expanded here into a general capability statement.

## Inspect evidence and logs

After a full lifecycle, derived run-bound directories are below
`$VERIFIED_RUN_ROOT`: evidence at
`evidence/no-crs-evidence/lighttpd/$run_id`, build files at
`build/lighttpd/$run_id`, runtime files at `runs/lighttpd/$run_id`, and sanitized
logs at `run-logs/lighttpd/$run_id`. General stage results are below
`$BUILD_ROOT/stages/lighttpd`. These are derived paths, not fixed system paths.

```sh
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
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
make prepare-lighttpd-runtime-build
make build-lighttpd
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
sudo apt remove lighttpd
sudo dnf remove lighttpd
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
| LIGHTTPD_BIN | no | generated external host binary | external patched lighttpd binary | Pinned host binary for selected patched route. |
| LIGHTTPD_SOURCE_DIR | no | generated external source directory | external lighttpd-1.4.84 source directory | Staged source for patch and module steps. |
| LIGHTTPD_BUILD_ROOT | no | derived external build directory | external patched-core build directory | Patched core build root outside checkout. |
| LIGHTTPD_INCLUDE_DIR | no | derived from source | external lighttpd source include directory | Header directory that must match the patched host and connector module. |
| LIGHTTPD_MODULE_DIR | no | derived external module directory | external module directory | Module location for patched host ABI. |
| LIGHTTPD_PATCHED_ROOT | no | derived below BUILD_ROOT | external patched-host root | Absolute external root containing patched source, build, and staging directories. |
| LIGHTTPD_MAKE_JOBS | no | 2 | 2 | Parallelism for the patched lighttpd core build; reduce it on memory-constrained hosts. |
| ALLOW_RUNTIME_BUILDS | no | 0 | 1 | Explicit opt-in for lighttpd source-build preparation. |

| Documented value | Example | Meaning |
| --- | --- | --- |
| connector name | lighttpd | Make and evidence name for this guide; no placeholder remains in the shown commands. |
| source directory | below `$BUILD_ROOT` or prepared provenance | Source created by the supported preparer; do not substitute a second manual checkout. |
| build directory | `$BUILD_ROOT/stages/lighttpd` | Staging and stage results outside the checkout. |
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
