# Build documentation

**Language:** English | [Deutsch](README.de.md)

This section explains how root and connector Make targets prepare and build
selected connector routes. A build, link, or config-load result is not runtime
evidence and does not make a production, CRS, HTTP/2, HTTP/3, complete-matrix,
or strict-for-all-connectors claim.

## Build inputs and safe paths

The root Makefile derives its working tree below
<code>VERIFIED_RUN_ROOT</code>. For a reproducible local build, set
<code>BUILD_ROOT</code> to an absolute writable directory outside the
checkout:

~~~sh
make build-nginx BUILD_ROOT="/srv/modsecurity-work/build"
~~~

<code>BUILD_ROOT</code> is optional because the Makefile derives
<code>VERIFIED_RUN_ROOT/build</code> when it is not provided. The example
value <code>/srv/modsecurity-work/build</code> is an absolute runtime path, not
a repository default. Do not use the repository root, a system directory, or a
path containing secrets. See [configuration variables](../reference/variables.md#runtime-and-repository-paths)
for format, scope, impact, and security details.

The placeholder <code>&lt;connector&gt;</code> means exactly one of
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code>, or <code>lighttpd</code>. For
example, use <code>make build-nginx</code>; do not type
<code>make build-&lt;connector&gt;</code> literally.

## Target families

| Target | Purpose | Prerequisites / important variables | Produced output | Boundary |
|---|---|---|---|---|
| <code>make check-framework</code> | Checks that the Framework is available | <code>FRAMEWORK_ROOT</code> points to an existing Framework checkout | Console result | Does not build a connector |
| <code>make setup-dev</code> | Installs or prepares development Python dependencies through the Framework | <code>PYTHON</code>, <code>FRAMEWORK_ROOT</code> | Development environment changes outside tracked source | Does not prepare every host component |
| <code>make prepare-runtime-components</code> | Obtains/builds reusable pinned host components | Safe build/cache paths, optional source pin variables | Component cache and environment snapshot | Does not execute connector lifecycle traffic |
| <code>make build-<connector></code> | Runs the selected connector build stage | Framework, build root, target-specific host inputs | Connector-specific build output | A successful build is not config or runtime proof |
| <code>make build-all-connectors</code> | Runs the build stage for all six connector names | All relevant host/component prerequisites | Per-connector build output | Aggregate build does not create full-lifecycle evidence |
| <code>make check-config-<connector></code> | Loads/checks selected connector configuration | Prepared selected build and configuration | Config-load diagnostics | Does not send traffic |
| <code>make prepare-open-connector-runtimes</code> | Prepares selected Envoy, Traefik, and lighttpd host inputs | Framework and cache/provisioning prerequisites | Component preparation output | Preparation is not capability promotion |
| <code>make lint</code> | Runs source, contract, and documentation-oriented checks | Python, shell tools, Framework, C toolchain where available | Diagnostics | Not an all-host runtime test |

Process exit code <code>0</code> means only that the invoked target completed
its technical contract. <code>1</code> is a general failure, <code>2</code>
is invalid input/contract validation, and <code>77</code> means a missing
optional or required environment prerequisite. See [Testing](../testing-and-evidence.md)
for the status vocabulary.

## Compiler and linker variables

Use standard compiler environment variables only when the local toolchain
requires them. The root defaults are:

| Variable | Required | Root default | Example | Effect / safety |
|---|---:|---|---|---|
| <code>PYTHON</code> | no | <code>.venv/bin/python</code> if present, otherwise <code>python3</code> | <code>PYTHON=python3</code> | Selects the Python interpreter for scripts; use a trusted executable |
| <code>MSCONNECTOR_C_STD</code> | no | <code>c17</code> | <code>MSCONNECTOR_C_STD=c23</code> | Selects the Common helper C profile; unsupported optional profiles may be skipped |
| <code>MSCONNECTOR_CFLAGS</code> | no | <code>-std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror</code> | <code>MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"</code> | Flags passed to Common helper checks; preserve quoting |
| <code>CC</code>, <code>CXX</code> | no | shell/toolchain default | <code>CC=clang</code> | Selects trusted C/C++ compilers |
| <code>CPPFLAGS</code>, <code>CFLAGS</code>, <code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code> | no | no root default | <code>CFLAGS="-O2"</code> | Adds compile/link inputs; untrusted flags can change the build |
| <code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code>, <code>PATH</code> | no | shell default | <code>PKG_CONFIG_PATH="/srv/prefix/lib/pkgconfig"</code> | Changes tool/library discovery; restrict to trusted paths |

The <code>$(MSCONNECTOR_C_STD)</code> notation above is a Make-variable
reference, not a shell command. The Makefile resolves it before running a
recipe. Full formats, defaults, and Framework-forwarded source variables are
listed in [configuration variables](../reference/variables.md).

## Local C/C++ diagnostics

Integration level 1 provides a reproducible local C17/C++17 diagnostic
foundation. It is a source and contract check only: it neither prepares runtime
components nor downloads or installs tools, and it does not claim runtime,
production, CRS, or connector-release evidence.

### Tool prerequisites and blocked status

Run <code>make check-analysis-tools</code> before a diagnostic capture. It
prints the actual selected <code>CC</code>, <code>CXX</code>, <code>clangd</code>,
and Bear paths and versions. A missing required tool, NGINX header set,
libmodsecurity header, local library path, or external writable path produces
<code>BLOCKED</code> and exit code <code>77</code>; the targets do not install,
download, or prepare a substitute. An absent, relative, or checkout-internal
required output parameter is a usage error and returns exit code <code>2</code>.

<code>clang-tidy</code> is deliberately not invoked. This level adds neither a
<code>.clang-tidy</code> file nor a <code>.clangd</code> file, static-analyzer
or sanitizer flags, production binary flags, or a CI gate.

### Capture and C++17 evaluator targets

| Target | Required local input | Result and boundary |
|---|---|---|
| <code>make compile-db-nginx-c17</code> | Absolute external <code>COMPDB_OUTPUT</code>; existing NGINX and libmodsecurity headers | Bear captures the direct <code>check-nginx-c17</code> compiler process. It covers the NGINX and Common sources declared in <code>connectors/nginx/config</code>, including <code>common/src/late_intervention.c</code>. |
| <code>make check-targeted-evaluator-cpp17</code> | Absolute external <code>CPP_BUILD_ROOT</code>, <code>MODSECURITY_INCLUDE_DIR</code>, and <code>MODSECURITY_LIB_DIR</code>; optional absolute <code>MODSECURITY_LIB_FILE</code> | Compiles only <code>common/scripts/modsecurity_targeted_eval.cc</code> with <code>-std=c++17 -Wall -Wextra -Werror</code>. The local binary is not executed and is not a production artifact. |
| <code>make compile-db-cpp17</code> | The same C++17 inputs plus the same external <code>COMPDB_OUTPUT</code> | Bear captures the real evaluator compiler process and atomically merges its C++17 entry with a valid existing database. It never invents a compiler command. |
| <code>make check-clangd-c17</code> | A merged external <code>COMPDB_OUTPUT</code> containing NGINX, Common, and evaluator entries | Validates the database and checks one representative NGINX, Common, and C++17 translation unit with <code>clangd --check</code>. It applies no fixes and disables configuration, background indexing, Clang-Tidy, and clangd tweaks. |

Every capture filters generated probes and external copied sources, retains only
tracked checkout translation units, validates C17/C++17 and
<code>-Wall -Wextra -Werror</code>, deduplicates by translation unit, and
publishes with an atomic replacement. A failed capture or validation leaves an
existing <code>COMPDB_OUTPUT</code> unchanged. The output path and every
captured compiler output must be absolute and outside the checkout.

Use an external analysis root rather than the checked-out local
<code>compile_commands.json</code>; the root filename and
<code>/.cache/clangd/</code> are intentionally ignored by Git. For a complete
C17/C++17 database, capture NGINX first and then merge C++17 into the same file:

~~~sh
make check-analysis-tools
make compile-db-nginx-c17 COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json"
make check-targeted-evaluator-cpp17 \
  CPP_BUILD_ROOT="/abs/build/cpp-evaluator" \
  MODSECURITY_INCLUDE_DIR="/abs/libmodsecurity/include" \
  MODSECURITY_LIB_DIR="/abs/libmodsecurity/lib"
make compile-db-cpp17 \
  COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json" \
  CPP_BUILD_ROOT="/abs/build/cpp-evaluator-cdb" \
  MODSECURITY_INCLUDE_DIR="/abs/libmodsecurity/include" \
  MODSECURITY_LIB_DIR="/abs/libmodsecurity/lib"
make check-clangd-c17 COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json"
~~~

<code>compile-db-cpp17</code> preserves valid NGINX rows and replaces only a
matching evaluator row, so it can also run before the NGINX capture. A
database containing only one language is still valid for its capture target,
but <code>check-clangd-c17</code> fails clearly until both required coverage
sets are present.

This first level has no Apache, HAProxy, Envoy, Traefik, or lighttpd compilation
database coverage. It does not execute connector traffic, inspect runtime
artifacts, enable Clang-Tidy, or establish any production or runtime release.

## Cache and source provisioning

<code>CACHE_ROOT</code> defaults to
<code>VERIFIED_RUN_ROOT/cache-v2</code>, and
<code>CONNECTOR_COMPONENT_CACHE</code> defaults to its <code>shared</code>
child. Both are absolute cache paths once derived. The cache is reusable input,
not canonical evidence.

For an isolated invocation, choose a parent before preparation:

~~~sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
~~~

<code>VERIFIED_RUN_PARENT</code> is optional; the root chooses
<code>RUNNER_TEMP</code>, then <code>TMPDIR</code>, then the documented
<code>&lt;system-temporary-root&gt;</code> fallback when it is empty.
<code>&lt;system-temporary-root&gt;</code> denotes the runtime's system
temporary fallback; it is a documentation placeholder and does not change the
checked-in runtime default. The example is a recommended local value, not a
repository default. Set <code>SKIP_RUNTIME_COMPONENT_PREPARE=1</code> only when a valid
invocation-local snapshot and compatible cache already exist. It does not mean
“skip missing dependencies.”

Advanced source/provenance values such as <code>HAPROXY_SOURCE_URL</code>,
<code>HTTPD_SHA256</code>, <code>NGINX_SOURCE_GIT_REF</code>, and
<code>MODSECURITY_V3_GIT_REF</code> are Framework-forwarded. URLs, revisions,
checksums, and source paths change provisioning identity and may cause
rebuilds. They do not change a connector capability or promote an outcome.

## Selected build routes

| Connector | Build target | Selected full-lifecycle profile | Build/integration note |
|---|---|---|---|
| Apache | <code>build-apache</code> | <code>native-httpd-module</code> | Native httpd module route; APXS and host inputs are provisioned/checked separately |
| NGINX | <code>build-nginx</code> | <code>native-nginx-http-module</code> | Native NGINX HTTP module route; module, prefix, and worker paths remain host-specific |
| HAProxy | <code>build-haproxy</code> | <code>native-htx-filter</code> | Native HTX filter route; source/build presence is not a response-body claim |
| Envoy | <code>build-envoy</code> | <code>ext_proc</code> | Streamed external-processing route; an alternate ext_authz helper is not silently the selected route |
| Traefik | <code>build-traefik</code> | <code>native-middleware</code> | Native middleware route with a local UDS service; forwardAuth compatibility helpers remain distinct |
| lighttpd | <code>build-lighttpd</code> | <code>patched-native</code> | Patched native host/module route; patch/build success is not full-lifecycle proof |

The profile values are supplied by full-lifecycle targets. Do not set
<code>FULL_LIFECYCLE_HOST_PROFILE</code> manually to relabel a direct or
compatibility build.

## Troubleshooting

| Symptom | Meaning | Safe next action |
|---|---|---|
| <code>BLOCKED: FRAMEWORK_ROOT is missing</code> / exit <code>77</code> | The submodule/Framework path is unavailable | Initialize the submodule or set <code>FRAMEWORK_ROOT</code> to a trusted existing Framework checkout |
| Build root rejected | Output is inside the checkout or otherwise unsafe | Set <code>BUILD_ROOT</code> or <code>VERIFIED_RUN_PARENT</code> to an absolute external writable path |
| Component preparation missing | Cache/snapshot is absent or preparation was skipped | Run <code>make prepare-runtime-components</code> without the skip flag |
| Compiler profile skipped | Optional C profile is unavailable | Use the documented default C17 check or install a compiler that supports the optional profile |
| Config check fails | Build, host configuration, or input file is invalid | Run the matching build target, review the sanitized log, and verify its documented variables |

Do not paste raw logs containing cookies, authorization headers, TLS private
keys, or other sensitive values into issues or canonical evidence.
