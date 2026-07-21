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

## Parent CI Python-version contract

**Change record:** [CR-20260720-python-313-workflow-contract](../../reports/audits/change-records/CR-20260720-python-313-workflow-contract.md)

This checked-in Parent GitHub Actions contract records the implemented
interpreter strategy, workflow boundaries, and local static-validation
evidence. It does not represent a GitHub Actions execution, remote CI run,
pull request, review, or delivery result.

### Canonical interpreter and strategy

The committed root [`.python-version`](../../.python-version) is the sole
machine-readable interpreter source. Its required content is the exact stable
release <code>3.13.14</code>. Every Python-executing job in the inventory below
must run `actions/setup-python` before its first direct or indirect Python use
with:

~~~yaml
python-version-file: .python-version
check-latest: false
~~~

The version literal must not be duplicated in workflow YAML. The setup action
is separately action-pinned; an action-lock record is not an interpreter
version source. After setup, the workflow contract must validate that `python`
and `python3` select equivalent configured Python <code>3.13.14</code>
interpreters before either name, a Python-backed Make target, or an indirect
Framework check is used. No listed job may fall back to an ambient runner,
bootstrap, virtual-environment, or system `python3` interpreter.

| Alternative | Decision | Rationale |
| --- | --- | --- |
| Floating `3.13` | Rejected | A later runner/tool-cache resolution can silently select a different patch release, creating patch drift. |
| Exact `3.13.14` from one committed `.python-version` file | Selected | The exact stable patch is reviewable and reproducible, while `python-version-file` gives every covered job the same source. |
| Exact version plus a permanent canary workflow | Rejected | The independent, read-only candidate-validation stage below validates a proposed patch before publication; an additional canary would duplicate that control without changing the publisher trust boundary. |

### Complete Parent workflow/job inventory

This 22-job baseline inventory is the authoritative documentation table for
the linked Change Record. “Existing minor-only setup” describes the live
baseline before this implementation: it had a `3.13` setup step. “Ambient or
bootstrapped Python” likewise describes a baseline path that lacked explicit
setup before the shown execution chain. In the checked-in workflow contract,
every row has the same explicit setup and `python`/`python3` equivalence
validation.

| Workflow | Job | Python execution chain | Baseline condition |
| --- | --- | --- | --- |
| `all-connectors-no-crs.yml` | `no-crs` | Direct `python3`, Framework scripts, and Python-backed Make targets | Existing minor-only setup |
| `all-connectors-no-crs.yml` | `aggregate` | Direct `python3` validation and summarization | Ambient or bootstrapped Python |
| `check-actions-versions.yml` | `check-actions-versions` | `python3 scripts/check-github-actions-versions.py` | Existing minor-only setup |
| `ci-security-secrets.yml` | `pull-request-range` | `python3 ci/tools/fetch_security_tool.py` | Ambient or bootstrapped Python |
| `ci-security-secrets.yml` | `advisory-full-history` | `python3 ci/tools/fetch_security_tool.py` | Ambient or bootstrapped Python |
| `ci-security-workflow-lint.yml` | `actionlint` | Python tool fetcher and `python3 -m unittest` | Ambient or bootstrapped Python |
| `ci-security-workflow-lint.yml` | `zizmor` | Python tool fetcher | Ambient or bootstrapped Python |
| `lint.yml` | `scaffold-lint` | Python documentation check and non-PR Python-backed setup/lint | Existing minor-only setup |
| `open-connectors-smoke.yml` | `open-connectors-smoke` | Direct summary plus indirect Python Make targets | Existing minor-only setup |
| `protocol-contract.yml` | `protocol-contract` | `python3 -m unittest` and protocol-client target | Existing minor-only setup |
| `protocol-contract.yml` | `nginx-profile-and-client-preflight` | Inline `python3` and client Make target | Existing minor-only setup |
| `quick-framework-check.yml` | `quick-check` | Indirect setup, matrix, and quick-check Python work | Existing minor-only setup |
| `test-apache.yml` | `apache-structure` | Conditional non-PR Python setup and quick-check | Existing minor-only setup |
| `test-common.yml` | `common-structure` | Conditional non-PR Python setup and quick-check | Existing minor-only setup |
| `test-envoy.yml` | `envoy-contract` | Indirect Python in connector checks | Ambient or bootstrapped Python |
| `test-full-smoke-sequential.yml` | `manual-heavy-runtime-validation` | `.venv/bin/python -m py_compile` and Python Make paths | Ambient or bootstrapped Python |
| `test-lighttpd.yml` | `lighttpd-contract` | Indirect Python in connector and shared checks | Ambient or bootstrapped Python |
| `test-nginx.yml` | `nginx-structure` | Conditional non-PR Python setup and quick-check | Existing minor-only setup |
| `test-traefik.yml` | `traefik-contract` | Indirect Python in connector and shared checks | Ambient or bootstrapped Python |
| `update-actions-versions.yml` | `update-actions-versions` | `python3 scripts/update-github-actions-versions.py --write` | Existing minor-only setup |
| `update-submodules.yml` | `validate-submodule-update` | Indirect Python through `make quick-check` | Ambient or bootstrapped Python |
| `verified-report-governance.yml` | `report-governance` | Indirect Python through `make report-governance` | Existing minor-only setup |

The inventory deliberately excludes jobs that have no proven Python execution
chain, such as action-only security scans, inline JavaScript cleanup, and
shell-only checks. A new Python-executing job must join this contract before it
is allowed to use Python. The static validator covers both `.yml` and `.yaml`
workflow filenames.

### Safe stable-patch updater contract

The updater is separate from the 22 baseline jobs. The checked-in
`.github/workflows/update-python-version.yml` has exactly three jobs:

| Job | Interpreter and trust boundary | Required behavior |
| --- | --- | --- |
| `resolve-python-patch` | Runs the current canonical `.python-version`; read-only | Calls only the fixed official structured Python release API `https://www.python.org/api/v2/downloads/release/?is_published=true` through HTTPS with exact host `www.python.org`, no redirects, `application/json`, bounded response handling, and schema validation. `--check` strictly parses published, non-prerelease stable `3.13.N` values, reports a candidate only when it is a higher patch, and cannot downgrade or cross a minor series. |
| `validate-python-patch` | Sets up the independently resolved candidate patch; read-only | Repeats the compatibility validation with the candidate interpreter before publication. It is independent of the resolver’s current-version interpreter and performs no source or branch mutation. |
| `create-python-update-pr` | Runs the current canonical `.python-version`; default-branch-gated publisher | Re-resolves the candidate with `--expected-version` before `--update`; only this job receives `contents: write` and `pull-requests: write`, and only to create a proposed update pull request. |

The only triggers are the scheduled Monday run and a manual
`workflow_dispatch`; there is no push or pull-request trigger. Every job is
gated to the repository default-branch ref and checks out that trusted default
branch without submodules or persisted checkout credentials. The validation
job sets up the independently resolved candidate version, re-resolves it, runs
the fail-closed static contract, compiles the checked-in Python paths, and runs
the focused Parent-native contract tests before the publisher can start.

`--check` resolves and validates a candidate without changing files. `--update`
is reserved for the publisher after the independent validation and expected-
version re-resolution succeed. The publisher is not an updater for arbitrary
Python versions: it accepts only the strict stable <code>3.13.N</code> format,
never a lower patch, prerelease, alternate minor series, or unstructured/HTML
release data.

The publisher uses the constant branch
`automation/update-python-313` and the stable title
`chore(ci): propose Python 3.13 patch update`. It creates a Draft pull request
when that branch does not exist, or updates an existing repository-owned Draft
update pull request only after verifying its head repository, default base,
and disabled automatic merge, then restricting its merge-base diff to
`.python-version`; it refuses to overwrite a branch without that exact pull
request. It therefore does not create duplicate update pull requests and never
force-pushes. Its English/German pull-request body records the prior and
proposed versions, official release identity, metadata source, validation
workflow/run URL, `.python-version` as the only changed file, retained Python
3.13 minor version, and absence of automatic merge.

The publisher streams the bounded REST pull-list response directly from
`gh api` into its strict duplicate-key JSON selector. The selector has no
caller-controlled response-file path, so the publisher does not cross a
response-file or symlink/TOCTOU boundary while reusing an existing Draft PR.

The updater must not auto-merge, write the default branch, force-push, consume
repository or user-provided `secrets.*`, initialize submodules, or execute an
arbitrary project workload. The publisher may use only GitHub’s automatically
provided job token, limited by its two job-scoped write permissions, to create
the Draft pull request or update the existing open update pull request; its
repository execution is limited to the
fixed interpreter verification and updater paths. The resolver and validator
remain read-only. The publisher’s limited write permissions, default-branch
gate, revalidation at the write boundary, and PR-only output prevent metadata
from directly mutating the default branch.

The independent validation stage is the evidence boundary for a proposed
patch; it is not a claim that a scheduled run, candidate, pull request, or
merge has occurred. Those results require separately observed CI and delivery
evidence.

### Observed local implementation validation

An isolated Python <code>3.13.14</code> interpreter was used for the local
implementation checks. The fail-closed workflow-version contract and
interpreter-identity verifier passed; a live `--check --json` query to the
fixed official API reported that the checked-in <code>3.13.14</code> is
current, and the updater unit suite passed 21 tests. `actionlint` (with
ShellCheck) passed for the workflow set and security fixtures, and
`zizmor --offline .github/workflows` reported no findings.

The complete local discovery run is not green in this sparse worktree:
`python3 -m unittest discover -s tests -v` under Python <code>3.13.14</code>
ran 355 tests and ended with 13 failures and four errors because required
Framework scripts are absent. `make setup-dev` exited 2 when its Framework
bootstrap attempted to create the unavailable local development environment;
`make lint` reached the shell and Python compilation checks but then exited 2
because the Framework `no_crs_baseline.py` check is absent. These are recorded
cross-repository/environment blockers, not successful runtime or remote-CI
evidence; the linked Change Record gives the command-level detail.

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
and Bear paths and versions. Run <code>make check-clang-analysis-tools</code>
before the advisory baseline; it independently reports the selected
<code>clang-tidy</code>, <code>clang</code>, and <code>clang++</code> tools.
Neither target installs, downloads, or prepares a substitute.

The advisory baseline requires a marked, writable <code>CODEX_TEMP_ROOT</code>
with its <code>tmp/</code> child, at least 5 GiB free space, and an external
C17/C++17 compilation database below that root. It refuses a relative,
checkout-internal, symlink-escaping, or otherwise unsafe CDB/output path before
creating output. Missing tools or prerequisites return exit code <code>77</code>;
invalid or unsafe parameters return exit code <code>2</code>; another non-zero
exit code means a technical analysis failure.

The baseline adds neither a <code>.clang-tidy</code> file nor a
<code>.clangd</code> file. It uses an explicit inline Tidy configuration,
does not apply <code>--fix</code>, <code>--fix-errors</code>,
<code>--fix-notes</code>, or <code>--export-fixes</code>, and does not add
<code>NOLINT</code> entries, sanitizer flags, production binary flags, a CI
gate, or a workflow change.

### Capture and C++17 evaluator targets

| Target | Required local input | Result and boundary |
|---|---|---|
| <code>make compile-db-nginx-c17</code> | Absolute external <code>COMPDB_OUTPUT</code>; existing NGINX and libmodsecurity headers | Bear captures the direct <code>check-nginx-c17</code> compiler process. It covers the NGINX and Common sources declared in <code>connectors/nginx/config</code>, including <code>common/src/late_intervention.c</code>. |
| <code>make check-targeted-evaluator-cpp17</code> | Absolute external <code>CPP_BUILD_ROOT</code>, <code>MODSECURITY_INCLUDE_DIR</code>, and <code>MODSECURITY_LIB_DIR</code>; optional absolute <code>MODSECURITY_LIB_FILE</code> | Compiles only <code>common/scripts/modsecurity_targeted_eval.cc</code> with <code>-std=c++17 -Wall -Wextra -Werror</code>. The local binary is not executed and is not a production artifact. |
| <code>make compile-db-cpp17</code> | The same C++17 inputs plus the same external <code>COMPDB_OUTPUT</code> | Bear captures the real evaluator compiler process and atomically merges its C++17 entry with a valid existing database. It never invents a compiler command. |
| <code>make check-clangd-c17</code> | A merged external <code>COMPDB_OUTPUT</code> containing NGINX, Common, and evaluator entries | Validates the database and checks one representative NGINX, Common, and C++17 translation unit with <code>clangd --check</code>. It applies no fixes and disables configuration, background indexing, Clang-Tidy, and clangd tweaks. |

### Advisory Clang analysis baseline

| Target | Required local input | Result and boundary |
|---|---|---|
| <code>make check-clang-analysis-tools</code> | Trusted <code>clang-tidy</code>, <code>clang</code>, and <code>clang++</code> on <code>PATH</code>, or the corresponding executable overrides | Reports the selected versions without creating analysis output. A missing tool returns <code>77</code>. |
| <code>make clang-tidy-baseline</code> | Absolute <code>COMPDB_OUTPUT</code> and absolute <code>ANALYSIS_OUTPUT</code>, both below the marked <code>CODEX_TEMP_ROOT</code> | Runs <code>clang-tidy</code> for every validated C17/C++17 translation unit using the explicit <code>-*,bugprone-*,cert-*</code> profile. Writes raw logs and <code>clang-tidy-baseline.json</code> only below <code>ANALYSIS_OUTPUT</code>. |
| <code>make clang-analyzer-baseline</code> | The same safe CDB/output paths | Replaces CDB compiler drivers with <code>clang</code> or <code>clang++</code>, strips output-writing arguments, and runs direct <code>clang --analyze</code> with the <code>core,unix,security,cplusplus,deadcode</code> profile and owned SARIF output. Writes <code>clang-analyzer-baseline.json</code>. It does not require <code>scan-build</code>. |
| <code>make clang-analysis-baseline</code> | The same safe CDB/output paths | Runs both advisory paths and writes one normalized <code>clang-analysis-baseline.json</code> plus run-scoped raw logs below <code>ANALYSIS_OUTPUT</code>. |

The runner validates that CDB entries name unique, tracked repository C/C++
sources with the required C17/C++17 flag before it writes any result. It stages
a sanitized compilation database and removes only that runner-owned staging
child after the invocation; it never recursively removes a caller-supplied
<code>ANALYSIS_OUTPUT</code>. It snapshots the CDB, analyzed source content, and
working-tree status before and after each run. A changed snapshot is a technical
failure, while pre-existing independent worktree changes are allowed to remain
unchanged.

The normalized JSON always contains the CDB SHA-256, tool paths and versions,
requested and active Tidy checks, the direct static-analyzer route, translation
unit counts, raw-artifact references, findings, technical failures, read-only
verification, and zero-inclusive classification totals. A technically complete
baseline exits <code>0</code> even when findings are present. The only
classification values are:

~~~text
confirmed_bug
needs_validation
possible_security_candidate
false_positive
third_party_header
intentional_pattern
out_of_scope
~~~

Tool diagnostics are triage input, not automatic proof. Repository diagnostics
normally start as <code>needs_validation</code>; CERT/security-oriented checks
may be <code>possible_security_candidate</code>; external headers are
<code>third_party_header</code>; and external non-header locations are
<code>out_of_scope</code>. The baseline never automatically labels a finding a
confirmed bug, false positive, or intentional pattern. A
<code>possible_security_candidate</code> is explicitly unconfirmed and needs
separate Codex Security validation before any security conclusion or source
change.

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

Use a marked external Codex temporary root for the advisory paths. The CDB is
an input from the capture steps above; the baseline does not recapture or edit
it:

~~~sh
export CODEX_TEMP_ROOT="/abs/marked-codex-temp-root"
export TMPDIR="$CODEX_TEMP_ROOT/tmp"
export ANALYSIS_ROOT="$CODEX_TEMP_ROOT/analysis"
export COMPDB_OUTPUT="$ANALYSIS_ROOT/final-cpp-diagnostics/compile_commands.json"

make check-clang-analysis-tools

make clang-tidy-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/tidy"

make clang-analyzer-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/analyzer"

make clang-analysis-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/combined"
~~~

This first level has no Apache, HAProxy, Envoy, Traefik, or lighttpd compilation
database coverage. It does not execute connector traffic, inspect runtime
artifacts, modify product source, alter the Framework or its submodule, or
establish any production or runtime release.

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
