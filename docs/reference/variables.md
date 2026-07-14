# Configuration and runtime variables

**Language:** English | [Deutsch](variables.de.md)

This is the central reference for variables accepted by the root <code>Makefile</code>,
its runtime lifecycle wrappers, and the directly callable connector harnesses.
It is intentionally conservative: a declared source path, build path, or
capability is not evidence that a host run passed.

## Scope and claim boundary

The repository has selected HTTP/1.1 core lifecycle routes for Apache, NGINX,
HAProxy, Envoy, Traefik, and lighttpd. Their result is always run-specific and
must be read from the canonical evidence produced by the invoked target.

This reference does **not** make a production, CRS, HTTP/2, HTTP/3, extended
matrix, or strict-for-all-connectors claim. In particular, a variable named
<code>strict</code>, a source build, or a successful configuration check does
not prove a client-visible post-commit enforcement path.

All paths below are repository-relative unless explicitly labelled as an
<em>absolute runtime path</em>, <em>cache path</em>, <em>evidence path</em>, or
<em>host installation path</em>. Use writable paths outside the checkout for
build, cache, runtime, log, and evidence output.

## How to set a variable

Set a Make variable for one invocation or export it for a shell session.
The first example creates a disposable runtime parent; the second identifies
one canonical evidence run.

~~~sh
make quick-check VERIFIED_RUN_PARENT="/srv/modsecurity-work"
NO_CRS_RUN_ID="six-core-20260712T120000Z" make full-lifecycle-all-connectors
~~~

<code>/srv/modsecurity-work</code> is an absolute, writable runtime path
outside the repository. <code>six-core-20260712T120000Z</code> is a
filesystem-safe run identifier. Do not use <code>.</code>, the repository
root, a home-directory path shared by unrelated jobs, secrets, usernames, or
ticket text in either value.

<code>VAR=value make target</code> is a Make assignment. <code>export
VAR=value</code> makes the value available to child scripts as an environment
variable. Root defaults use <code>?=</code>; therefore a command-line value
overrides a repository default. Variables marked “Framework-forwarded” are
exported by the root Makefile but receive their detailed provider-specific
default in the Framework or component preparer.

## Common path placeholders

The angle-bracket forms below are documentation placeholders. Do not copy the
brackets into a command unless a command explicitly expects literal brackets.

| Placeholder | Purpose | Format / requiredness | Default / set by | Portable example | Effect and safety |
|---|---|---|---|---|---|
| <code>&lt;repository-root&gt;</code> | The root of this connector checkout, containing <code>Makefile</code> and <code>docs/</code> | Existing absolute directory; required whenever a command asks for a repository root | No environment-variable default; discovered by the caller, <code>git rev-parse --show-toplevel</code>, or the target | <code>/srv/src/ModSecurity-conector</code> | Resolves repository-relative paths such as <code>connectors/nginx/</code>. The example is not a literal developer path; do not use a build, cache, evidence, or secret directory as the repository root. |
| <code>&lt;external-source-root&gt;</code> | A user-selected source checkout outside this repository, for example the Framework or a reused upstream source | Existing absolute trusted source directory; optional unless the documented command requires it | No repository default; set by the caller/CI through a variable such as <code>FRAMEWORK_ROOT</code> or a documented source-path variable | <code>/srv/src/ModSecurity-test-Framework</code> | Lets a command use an external checkout. It is not a build/output path and does not make that checkout or its capabilities verified. Never substitute an untrusted/mutable source for a pinned CI input. |

## Requirements at a glance

| Requirement | Required for | Allowed value / example | Why it matters | Check |
|---|---|---|---|---|
| <code>FRAMEWORK_ROOT</code> | All root targets that delegate to the Framework | Repository default: <code>modules/ModSecurity-test-Framework</code> | Locates the submodule runner and schemas | <code>make check-framework</code> |
| <code>BUILD_ROOT</code> | Builds and runtime targets | Absolute writable path; <code>/srv/modsecurity-work/build</code> | Keeps generated host files outside the checkout | Target exits <code>77</code> when a required path is unsafe or absent |
| <code>NO_CRS_RUN_ID</code> | Evidence checks and a reproducible canonical run | <code>six-core-20260712T120000Z</code> | Names one evidence, plan, log, and summary set | <code>make evidence-check-all-connectors</code> |
| <code>NO_CRS_RULES_FILE</code> | No-CRS baseline targets | Absolute existing rules file; default is the Framework baseline | Prevents an unspecified or different ruleset from being presented as the baseline | The runner verifies that the file exists |
| <code>CONNECTOR_COMPONENT_CACHE</code> | Runtime preparation or reuse | Absolute cache path; <code>/srv/modsecurity-work/cache-v2/shared</code> | Holds reusable prepared components, separate from each run | <code>make runtime-components-inventory</code> |
| Toolchain variables | Source builds and C checks | <code>CC=clang CFLAGS="-O2"</code> | Select compiler and flags without editing tracked files | <code>make check-common-helpers</code> |

No variable in this table is a secret. If a downstream host configuration
needs a certificate, private key, token, cookie, authorization header, or
password, keep it in a secure store; do not commit it, put it in canonical
evidence, or pass it in a command line that may be visible in process lists.

## Reference table

“Default” means the root Makefile default unless the cell says
“Framework-forwarded” or “harness-specific.” A blank default is not an
invitation to rely on the current working directory; it means that the caller
or a target must supply the value.

| Variable | Area | Required | Default | Format | Short description |
|---|---|---:|---|---|---|
| <code>PYTHON</code> | toolchain | no | <code>.venv/bin/python</code> when present, otherwise <code>python3</code> | executable or executable path | Python used by repository scripts |
| <code>MSCONNECTOR_C_STD</code>, <code>MSCONNECTOR_CFLAGS</code>, <code>MSCONNECTOR_COMPILER_ID</code> | compiler | no | <code>c17</code>; warnings-as-errors flags; compiler basename | C standard, flags, executable name | Controls Common helper compilation |
| <code>COMPDB_OUTPUT</code> | local diagnostics | required by compilation-database, clangd, and advisory baseline targets | none | absolute compilation-database file outside the checkout; advisory use additionally requires it below marked <code>CODEX_TEMP_ROOT</code> | Atomically published Bear compilation database; captures merge by translation unit and never overwrite a failed target; the baseline reads it without editing it |
| <code>CPP_BUILD_ROOT</code>, <code>MODSECURITY_INCLUDE_DIR</code>, <code>MODSECURITY_LIB_DIR</code>, <code>MODSECURITY_LIB_FILE</code> | targeted C++17 diagnostics | required except optional <code>MODSECURITY_LIB_FILE</code> | none | absolute external build directory; absolute local header/library directory; optional absolute library file | Builds and captures only the libmodsecurity evaluator; no component preparation or evaluator execution |
| <code>CLANG_TIDY</code>, <code>CLANG</code>, <code>CLANGXX</code> | advisory Clang analysis | required by the selected advisory target | <code>clang-tidy</code>, <code>clang</code>, <code>clang++</code> | trusted executable name or absolute executable path | Selects the read-only Tidy and direct static-analyzer tools; missing executables return <code>77</code> and no substitute is installed |
| <code>CLANG_TIDY_CHECKS</code>, <code>CLANG_ANALYZER_CHECKS</code> | advisory Clang analysis | no | <code>-*,bugprone-*,cert-*</code>; <code>core,unix,security,cplusplus,deadcode</code> | comma-separated trusted Clang check selectors | Selects the explicit Tidy and direct analyzer profiles recorded in normalized JSON; unsafe selector syntax returns <code>2</code> |
| <code>ANALYSIS_OUTPUT</code> | advisory Clang analysis | required by baseline targets | none | absolute output directory below marked <code>CODEX_TEMP_ROOT</code> and outside the checkout | Receives only run-scoped raw logs, owned SARIF files, and normalized baseline JSON; the runner never recursively removes a caller-supplied directory |
| <code>VERIFIED_RUN_PARENT</code> | runtime root | no | <code>RUNNER_TEMP</code>, then <code>TMPDIR</code>, then <code>&lt;system-temporary-root&gt;</code> | absolute directory | Parent of the invocation-owned runtime tree |
| <code>VERIFIED_RUN_ROOT</code>, <code>VERIFIED_STATE_ROOT</code>, <code>VERIFIED_BUILD_ROOT</code>, <code>VERIFIED_SOURCE_ROOT</code>, <code>VERIFIED_TMP_ROOT</code>, <code>VERIFIED_LOG_ROOT</code> | runtime roots | no | Derived below <code>VERIFIED_RUN_PARENT</code> | absolute directories | Isolated state, build, source, temporary, and log locations |
| <code>STATE_HOME</code>, <code>SOURCE_ROOT</code>, <code>BUILD_ROOT</code>, <code>TMP_ROOT</code>, <code>LOG_ROOT</code>, <code>MATRIX_ROOT</code>, <code>RESULTS_DIR</code> | build/runtime | target-dependent | Derived from the verified roots; <code>RESULTS_DIR</code> is Framework-forwarded | absolute directories | Working areas passed to builds, harnesses, and report writers |
| <code>FRAMEWORK_ROOT</code>, <code>CONNECTOR_ROOT</code> | repository paths | <code>FRAMEWORK_ROOT</code>: yes for delegated targets | submodule path; current repository directory | repository-relative or absolute existing directory | Locates the Framework and this repository |
| <code>CACHE_ROOT</code>, <code>VERIFIED_COMPONENT_CACHE</code>, <code>CONNECTOR_COMPONENT_CACHE</code> | cache | no | <code>cache-v2</code> below the verified root; shared child | absolute directories | Reusable component cache, distinct from a run |
| <code>VERIFIED_EVIDENCE_ROOT</code>, <code>EVIDENCE_ROOT</code>, <code>RUNTIME_EVIDENCE_ROOT</code> | evidence | no | derived below verified root | absolute directories | Canonical No-CRS and runtime-evidence parent paths |
| <code>RUNTIME_RUN_ROOT</code>, <code>RUNTIME_LOG_ROOT</code> | runtime | no | derived below verified root | absolute directories | Raw run and per-run log parents |
| <code>VERIFIED_RUN_ID</code> | report run | no | supplied ID, generated UTC/commit ID, or existing manifest ID | filesystem-safe token | Identifies a verified report run |
| <code>NO_CRS_CONNECTORS</code> | No-CRS selection | no | <code>apache nginx haproxy envoy traefik lighttpd</code> | space-separated connector names | Bounded connector set for aggregate targets |
| <code>NO_CRS_RUN_ID</code> | No-CRS evidence | yes for evidence checks | none; runners may derive a UTC/commit value | 1–128 ASCII letters/digits plus <code>.</code>, <code>_</code>, <code>-</code>; starts alphanumeric | Canonical evidence namespace |
| <code>NO_CRS_RULES_FILE</code> | No-CRS rules | no | Framework <code>tests/rules/no-crs-baseline.conf</code> | absolute existing file | Rule file used by the baseline |
| <code>NO_CRS_ARTIFACT_PROFILE</code>, <code>FULL_LIFECYCLE_HOST_PROFILE</code>, <code>FULL_LIFECYCLE_EXECUTED_TARGET</code> | lifecycle internals | set by full-lifecycle targets | <code>generic</code>; profile/target empty | enumerated strings | Bind a run to its selected host profile |
| <code>NO_CRS_PROTOCOL_CLIENT</code>, <code>NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR</code> | optional protocol probe | no | <code>0</code>; empty | boolean; absolute raw-run descendant | Opt-in non-promoting protocol observation |
| <code>CAPABILITY_PLAN_ROOT</code>, <code>CAPABILITY_REPORT_EVIDENCE_ROOT</code>, <code>CAPABILITY_REPORT_RUN_ID</code>, <code>CAPABILITY_REPORT_OUTPUT_DIR</code> | capability reports | no | derived from build/evidence/run ID | absolute directories and run ID | Controls selected-case plans and report output |
| <code>SKIP_RUNTIME_COMPONENT_PREPARE</code>, <code>RUNTIME_COMPONENT_STRICT_VERIFY</code>, <code>KEEP_RUNTIME_ARTIFACTS</code> | provisioning | no | <code>0</code> | <code>0</code> or <code>1</code> | Skip preparation only with a usable snapshot; choose verification and cleanup policy |
| <code>RUNTIME_COMPONENT_TARGET</code>, <code>RUNTIME_COMPONENT_ENV_SNAPSHOT</code>, <code>RUNTIME_REPORT_OUTPUT_ROOT</code> | provisioning | no | <code>all</code>; target-generated snapshot and report root | target name; absolute file/directory | Component selection and invocation-local environment snapshot |
| <code>RUNTIME_COMPONENT_NETWORK_RETRIES</code>, <code>RUNTIME_COMPONENT_NETWORK_RETRY_DELAY_SECONDS</code> | provisioning | no | <code>3</code>; <code>2</code> | non-negative numbers | Bounded retries for component downloads |
| <code>VERIFIED_RUN_RUNTIME_MATRIX_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_FULL_MATRIX_RUNTIME_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_REPORT_REFRESH_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_NATIVE_MRTS_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS</code>, <code>VERIFIED_RUN_JOB_FINALIZE_GRACE_SECONDS</code>, <code>VERIFIED_RUN_FULL_MATRIX_TOTAL_TIMEOUT_SECONDS</code> | timeouts | no | <code>1800</code>, <code>7200</code>, <code>1800</code>, <code>1800</code>, <code>3600</code>, <code>60</code>, <code>14400</code> seconds | positive integer seconds | Bounds long-running report and matrix work |
| <code>SMOKE_CASES</code>, <code>CASE_SCOPE</code>, <code>TEST_CASE</code>, <code>RUN_ONE_CASE</code>, <code>FORCE_ALL_CASES</code> | test selection | no | Framework-forwarded; <code>CASE_SCOPE=all</code> in native harnesses | case ID/list; scope; boolean | Narrows a diagnostic run without changing the catalog |
| <code>DEFAULT_BRANCH</code>, <code>REFRESH</code>, <code>EXTRA_CASE_ROOTS</code> | Framework-forwarded | no | Framework/provider default | branch, boolean, paths | Forwarded compatibility and refresh controls |
| <code>MODSECURITY_TEST_VARIANT</code>, <code>MODSECURITY_MRTS_VARIANT</code>, <code>MODSECURITY_RULESET</code>, <code>MODSECURITY_SMOKE_CASE</code>, <code>CRS_SMOKE_CASE</code>, <code>MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO</code>, <code>MODSECURITY_MRTS_PREPARED</code> | Framework test input | no | Framework-forwarded | variant, ruleset, case, boolean | Framework-side test and MRTS selection |
| <code>MODSECURITY_REPO_URL</code>, <code>MODSECURITY_GIT_REF</code>, <code>MODSECURITY_V3_GIT_URL</code>, <code>MODSECURITY_V3_GIT_REF</code>, <code>MODSECURITY_APACHE_GIT_URL</code>, <code>MODSECURITY_APACHE_GIT_REF</code>, <code>MODSECURITY_NGINX_GIT_URL</code>, <code>MODSECURITY_NGINX_GIT_REF</code> | source provenance | no | Framework/provider pin | URL and immutable ref | Upstream source location and revision |
| <code>MODSECURITY_SOURCE_DIR</code>, <code>MODSECURITY_V3_SOURCE_DIR</code>, <code>MODSECURITY_V3_ROOT</code>, <code>MODSECURITY_APACHE_SOURCE_DIR</code>, <code>MODSECURITY_NGINX_SOURCE_DIR</code> | source paths | no | Framework-forwarded | absolute existing directories | Reuse a local source tree rather than fetching |
| <code>MODSECURITY_APACHE_REPO_URL</code>, <code>MODSECURITY_NGINX_REPO_URL</code>, <code>ALLOW_EXTERNAL_CONNECTOR_REPOS</code> | source provenance | no | Framework-forwarded | URLs; boolean | Controls external Apache/NGINX source use |
| <code>CRS_REPO_URL</code>, <code>CRS_GIT_REF</code>, <code>CRS_SOURCE_DIR</code>, <code>CRS_RUNTIME_DIR</code>, <code>MODSECURITY_RULE_PREAMBLE_FILE</code> | optional CRS input | no | Framework/provider pin | URL/ref/path | CRS preparation input; not a CRS verification claim |
| <code>BUILD_HTTPD_FROM_SOURCE</code>, <code>BUILD_PCRE2_FROM_SOURCE</code>, <code>BUILD_NGINX_FROM_SOURCE</code>, <code>NGINX_SOURCE_MODE</code>, <code>NGINX_SOURCE_REPO_URL</code>, <code>NGINX_SOURCE_GIT_REF</code>, <code>NGINX_GITHUB_REPO</code>, <code>NGINX_RELEASE_TAG</code> | host provisioning | no | Framework-forwarded | boolean, mode, URL/ref/tag | Selects host source acquisition and build policy |
| <code>HTTPD_VERSION</code>, <code>HTTPD_SOURCE_URL</code>, <code>HTTPD_SHA256</code>, <code>HTTPD_SHA256_URL</code>, <code>APR_VERSION</code>, <code>APR_SOURCE_URL</code>, <code>APR_SHA256</code>, <code>APR_SHA256_URL</code>, <code>APR_UTIL_VERSION</code>, <code>APR_UTIL_SOURCE_URL</code>, <code>APR_UTIL_SHA256</code>, <code>APR_UTIL_SHA256_URL</code>, <code>PCRE2_VERSION</code>, <code>PCRE2_SOURCE_URL</code>, <code>PCRE2_SHA256</code>, <code>PCRE2_SHA256_URL</code> | Apache provisioning | no | Framework/provider pin | version, URL, SHA-256 | Apache dependency provenance |
| <code>HAPROXY_VERSION</code>, <code>HAPROXY_SOURCE_URL</code>, <code>HAPROXY_SHA256_URL</code>, <code>HAPROXY_SHA256</code>, <code>HAPROXY_SOURCE_ROOT</code>, <code>HAPROXY_DOWNLOAD_DIR</code>, <code>HAPROXY_SOURCE_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_WORKTREE</code>, <code>HAPROXY_RUNTIME_DIR</code>, <code>HAPROXY_BIN</code> | HAProxy provisioning | no | Framework/provider pin | version, URL, SHA-256, absolute paths | HAProxy source, build, and host executable inputs |
| <code>EXPAT_SOURCE_URL</code>, <code>EXPAT_GIT_REF</code>, <code>EXPAT_GIT_URL</code>, <code>EXPAT_PROMPT_EXPECTED_LATEST</code> | Apache dependency | no | Framework/provider pin | URL/ref/boolean | Expat provenance and prompt policy |
| <code>GO_FTW_BIN</code>, <code>GO_FTW_SOURCE_URL</code>, <code>GO_FTW_PROMPT_EXPECTED_LATEST</code>, <code>GO_FTW_GIT_REF</code>, <code>ALBEDO_BIN</code>, <code>ALBEDO_SOURCE_URL</code>, <code>ALBEDO_PROMPT_EXPECTED_LATEST</code>, <code>ALBEDO_GIT_REF</code> | MRTS tools | no | <code>go-ftw</code>, <code>albedo</code>; provider pins otherwise | executable, URL, ref, boolean | Optional Framework/MRTS tool input |
| <code>MRTS_ROOT</code>, <code>MRTS_DEFINITIONS</code>, <code>MRTS_RULES_OUT</code>, <code>MRTS_FTW_OUT</code>, <code>MRTS_LOAD_FILE</code>, <code>MRTS_CASE_ROOT</code>, <code>MRTS_BUILD_ROOT</code>, <code>MRTS_NATIVE_ROOT</code> | MRTS | no | build-root-derived where defined; otherwise Framework-forwarded | absolute files/directories | MRTS materialization and native-run locations |
| <code>MRTS_NATIVE_TARGETS</code>, <code>MRTS_NATIVE_APACHE_PORT</code>, <code>MRTS_NATIVE_NGINX_BIN</code>, <code>MRTS_NATIVE_NGINX_MODULE_DIR</code>, <code>MRTS_NATIVE_NGINX_PORT</code>, <code>MRTS_NATIVE_BACKEND_PORT</code> | MRTS native | no | <code>apache2_ubuntu nginx-pr24</code>; ports <code>19080</code>–<code>19082</code> where defined | target list, executable/path, TCP ports | Controls optional native MRTS runs |
| <code>APACHE_BIN</code>, <code>APACHECTL_BIN</code>, <code>APXS_BIN</code>, <code>NGINX_BIN</code> | host binaries | no | Framework-forwarded | executable or absolute executable path | Overrides discovered host executables |
| <code>RESPONSE_BODY_PROBE_REPEAT</code>, <code>RESPONSE_BODY_PROBE_ROOT</code>, <code>RESPONSE_BODY_PROBE_CASE</code> | diagnostic probe | no | Framework-forwarded | positive count, absolute path, case ID | Controls a focused response-body diagnostic |
| <code>DECISION_BACKEND</code>, <code>ENVOY_DECISION_BACKEND</code>, <code>TRAEFIK_DECISION_BACKEND</code>, <code>LIGHTTPD_DECISION_BACKEND</code> | compatibility path | no | Framework-forwarded | provider-defined backend name | Selects a supported decision backend; not a capability upgrade |
| <code>CC</code>, <code>CXX</code>, <code>CPPFLAGS</code>, <code>CFLAGS</code>, <code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code>, <code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code>, <code>PATH</code> | inherited toolchain | no | shell/toolchain default | compiler commands, flags, path lists | Passed to source builds and dynamic loaders |
| Apache harness variables | connector-local | direct use only | see [Apache details](#apache-direct-entrypoint-variables) | paths, ports, case selectors | Overrides a direct Apache harness |
| NGINX harness variables | connector-local | direct use only | see [NGINX details](#nginx-direct-entrypoint-variables) | paths, ports, protocols, case selectors | Overrides a direct NGINX harness |
| HAProxy harness variables | connector-local | direct use only | see [HAProxy details](#haproxy-direct-entrypoint-variables) | paths, ports, case selectors | Overrides a direct HAProxy harness |
| Envoy harness variables | connector-local | direct use only | see [Envoy details](#envoy-direct-entrypoint-variables) | paths, ports, booleans | Overrides ext_proc/ext_authz helper entry points |
| Traefik harness variables | connector-local | direct use only | see [Traefik details](#traefik-direct-entrypoint-variables) | paths, listen addresses, flags | Overrides native-middleware or compatibility helpers |
| lighttpd harness variables | connector-local | direct use only | see [lighttpd details](#lighttpd-direct-entrypoint-variables) | paths, ports, modes | Overrides the patched host helper |

## Detailed root variables

### Runtime and repository paths

| Property | <code>VERIFIED_RUN_PARENT</code> | <code>BUILD_ROOT</code> | <code>FRAMEWORK_ROOT</code> | <code>CONNECTOR_COMPONENT_CACHE</code> |
|---|---|---|---|---|
| Purpose | Parent for a disposable invocation tree | Build output root passed to host preparation | Locates the Framework submodule or an equivalent checkout | Reusable prepared-component cache |
| Format | Absolute writable directory | Absolute writable directory outside the checkout | Existing directory containing the Framework Makefile and <code>ci/</code> | Absolute writable directory outside the checkout |
| Required | No; a safe default is derived | Required by builds; root derives one | Yes for targets that delegate to the Framework | No; root derives a shared cache child |
| Root default | <code>RUNNER_TEMP</code>, then <code>TMPDIR</code>, then <code>&lt;system-temporary-root&gt;</code> | <code>VERIFIED_RUN_ROOT/build</code> | <code>modules/ModSecurity-test-Framework</code> | <code>CACHE_ROOT/shared</code> |
| Set by | Caller, CI runner, or Makefile | Caller or Makefile | Caller or Makefile | Caller, component preparer, or Makefile |
| Scope | One invocation and its descendants | One invocation; connector-local child paths are derived | One invocation | Reusable across compatible invocations |
| Example | <code>/srv/modsecurity-work</code> | <code>/srv/modsecurity-work/verified/build</code> | <code>modules/ModSecurity-test-Framework</code> | <code>/srv/modsecurity-work/verified/cache-v2/shared</code> |
| Effect | Moves all derived run roots | Determines generated host and report work locations | Missing path causes <code>check-framework</code> to exit <code>77</code> | Reuses component downloads/builds when identities match |
| Safety | Do not point at the checkout, system directories, or a secret-bearing home tree | The runner rejects unsafe checkout paths | Must be trusted source code at the expected revision | Treat as build input; do not store credentials there |

<code>VERIFIED_RUN_ROOT</code> defaults to
<code>VERIFIED_RUN_PARENT/ModSecurity-conector-verified</code>. Its
<code>state</code>, <code>build</code>, <code>src</code>, <code>tmp</code>,
<code>logs</code>, <code>cache-v2</code>, <code>evidence</code>,
<code>runs</code>, and <code>run-logs</code> children are exposed through the
corresponding <code>VERIFIED_*</code>, <code>CACHE_ROOT</code>, and
<code>RUNTIME_*</code> variables in the reference table. <code>TMP_ROOT</code>
and <code>LOG_ROOT</code> default below <code>BUILD_ROOT</code>; this keeps
host transient files nested under the invocation rather than in a tracked tree.

<code>&lt;system-temporary-root&gt;</code> is a documentation placeholder for
the operating system's temporary-directory fallback selected by the checked-in
runtime when neither <code>RUNNER_TEMP</code> nor <code>TMPDIR</code> is set.
It is not a literal command value and does not alter that runtime default.

### No-CRS and evidence variables

| Property | <code>NO_CRS_RUN_ID</code> | <code>NO_CRS_CONNECTORS</code> | <code>NO_CRS_RULES_FILE</code> | <code>EVIDENCE_ROOT</code> |
|---|---|---|---|---|
| Purpose | Names one canonical run | Selects connectors for aggregate targets | Selects baseline rules | Parent of canonical No-CRS evidence |
| Format | Safe token: letters/digits, <code>.</code>, <code>_</code>, <code>-</code>; maximum 128 characters | Space-separated subset of <code>apache nginx haproxy envoy traefik lighttpd</code> | Absolute existing file | Absolute writable directory |
| Required | Yes for evidence checks and reproducible aggregate evidence | No | No | No |
| Root default | Empty; the runner may derive a UTC/commit value | All six connector names | Framework <code>tests/rules/no-crs-baseline.conf</code> | <code>VERIFIED_EVIDENCE_ROOT/no-crs-evidence</code> |
| Set by | Caller, CI, or runner | Caller or Makefile | Caller or Makefile | Caller or Makefile |
| Scope | One run, all its artifacts | One aggregate target | One baseline invocation | One or more evidence runs |
| Example | <code>six-core-20260712T120000Z</code> | <code>apache nginx</code> | <code>/srv/rules/no-crs-baseline.conf</code> | <code>/srv/modsecurity-work/evidence/no-crs-evidence</code> |
| Effect | Selects the run directory used by validation | Limits aggregate loops; it does not manufacture omitted evidence | Changes rule input and therefore comparability | Selects evidence directories consumed by checks |
| Safety | Never include credentials, user names, or issue text | Do not use unrecognised connector names | Review local rule content; rules are executable policy | Do not mix sensitive raw logs into canonical output |

<code>NO_CRS_PROTOCOL_CLIENT=1</code> opts into a stage-owned protocol probe.
If an artifact directory is provided through
<code>NO_CRS_PROTOCOL_CLIENT_ARTIFACT_DIR</code>, it must stay under that
invocation’s raw evidence directory and the artifact profile must be
<code>full_lifecycle</code>. This is diagnostic input: it does not by itself
promote HTTP/2, HTTP/3, QUIC, or strict transport behavior.

The root full-lifecycle targets set <code>NO_CRS_ARTIFACT_PROFILE</code>,
<code>FULL_LIFECYCLE_HOST_PROFILE</code>, and
<code>FULL_LIFECYCLE_EXECUTED_TARGET</code> themselves. Do not set these
internals to relabel a compatibility smoke as full lifecycle evidence.

### Provisioning, source, and toolchain variables

The source URL, ref, checksum, version, and path variables in the reference
table form a group. They have the following common properties:

| Property | Source/provenance groups |
|---|---|
| Purpose | Tell the Framework component preparer which pinned source, archive, local tree, host binary, or optional MRTS tool to use |
| Format | URLs use <code>https://</code> or another provider-supported scheme; refs/tags are non-empty source identifiers; SHA-256 values are 64 hexadecimal characters; paths are absolute existing paths when reused locally |
| Required | Optional at the root. A target either uses its provider default or reports a missing prerequisite; source overrides are not required for ordinary root targets |
| Default | “Framework-forwarded” means the root Makefile exports the name but does not define a root value. The Framework/provider pin is authoritative |
| Set by | Advanced local caller or CI provisioning configuration |
| Scope | The relevant component-preparation invocation; cached output is identity-bound to effective input |
| Example | <code>HAPROXY_VERSION=3.2.21</code>, <code>NGINX_SOURCE_MODE=release</code>, <code>CC=clang</code> |
| Effect | Can force a rebuild, alter a source origin, or select another executable; it never upgrades a capability state or evidence outcome |
| Safety | Use HTTPS and verified checksums. Do not replace a pinned provenance value with a mutable or untrusted source in canonical CI |

<code>CC</code>, <code>CXX</code>, <code>CPPFLAGS</code>, <code>CFLAGS</code>,
<code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code>,
<code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code>, and
<code>PATH</code> are inherited conventional toolchain variables. They are
optional, have no repository default, and are normally set by the shell or CI.
They affect compiler discovery, includes, library discovery, and dynamic
loading. Restrict their path elements to trusted locations; a malicious
library path can change the binary that runs.

### Test selection, report, and timeout variables

<code>SMOKE_CASES</code>, <code>CASE_SCOPE</code>, <code>TEST_CASE</code>,
<code>RUN_ONE_CASE</code>, and <code>FORCE_ALL_CASES</code> are diagnostic
selectors. They are optional and Framework-forwarded unless a native harness
states a default. Use a catalog case ID or a documented comma/space-separated
case list; do not invent case IDs. A narrowed run is not a substitute for an
aggregate evidence run.

<code>VERIFIED_RUN_ID</code> controls a report-run namespace. If it is not
set, the root Makefile uses an ID from the existing generated manifest when
available, otherwise a UTC timestamp plus the current short commit. It is
safe only when used as a filesystem token. The timeout variables are positive
integer seconds set by the caller or CI; the root defaults in the reference
table are operational limits, not evidence-quality thresholds.

<code>SUPPRESS_FULL_RUN_EVIDENCE_SIDE_EFFECTS</code>,
<code>FULL_MATRIX_MANIFEST</code>, <code>VERIFIED_RUN_COMMANDS_FILE</code>,
<code>VERIFIED_RUN_PROFILE</code>, <code>DEBUG_MISMATCH_GENERATOR</code>, and
<code>ALLOW_IN_PROGRESS_SYSTEM_PROOF</code> are report-tool controls consumed
by individual Python tools. They are optional, have no root Makefile default,
and should be used only by the invoking target or an expert diagnostic. They
can suppress or redirect report work; they do not alter case truth.

## Connector direct-entrypoint variables

The normal interface is a root Make target. The following names exist for
direct harness use and are documented here so that a reader does not need to
infer them from shell source. They are not additional connector features.

### Apache direct entrypoint variables

| Names | Purpose and format | Default / setter | Effect and safety |
|---|---|---|---|
| <code>APACHE_BUILD_ROOT</code>, <code>HTTPD_PREFIX</code>, <code>MODSECURITY_V3_DIR</code>, <code>MODSECURITY_LIB_DIR</code>, <code>PCRE2_PREFIX</code>, <code>APACHE_MODULE</code> | Absolute build/module paths | Derived below <code>BUILD_ROOT</code> by <code>connectors/apache/harness/run_apache_smoke.sh</code> | Point the direct harness at a prepared Apache/libmodsecurity build; paths must be outside the checkout |
| <code>APACHE_HTTPD</code>, <code>APACHE_HTTPD_BIN</code>, <code>APACHE</code>, <code>APACHE_BIN</code>, <code>APACHECTL_BIN</code>, <code>APXS</code>, <code>APXS_BIN</code> | Executable command or absolute executable path | Root/provider discovery or the harness-derived path | Overrides host executable discovery; use trusted executable files only |
| <code>PORT</code>, <code>PORT_SEARCH_LIMIT</code>, <code>PORT_RETRY_LIMIT</code> | TCP port and positive search/retry counts | <code>18080</code>, <code>100</code>, <code>1</code> in the direct harness | Selects loopback smoke ports; avoid privileged or occupied ports |
| <code>MSCONNECTOR_FULL_LIFECYCLE_SYNC</code>, <code>FULL_LIFECYCLE_EVIDENCE_OUTPUT</code> | Boolean and absolute evidence file | <code>0</code>; empty | Enables synchronization/evidence handoff for the lifecycle runner; do not write evidence into the checkout |

### NGINX direct entrypoint variables

| Names | Purpose and format | Default / setter | Effect and safety |
|---|---|---|---|
| <code>NGINX_BUILD_DIR</code>, <code>NGINX_PREFIX</code>, <code>NGINX_BINARY</code>, <code>NGINX_MODULE</code>, <code>MODSECURITY_LIB_DIR</code> | Absolute prepared-build, install, binary, module, or library paths | Derived from <code>BUILD_ROOT</code> unless supplied | Overrides NGINX build/host lookup; all must be trusted paths |
| <code>NGINX_HARNESS_PARENT</code>, <code>NGINX_HARNESS_WORK_ROOT</code>, <code>RUNTIME_BASE</code>, <code>RUNTIME_ROOT</code>, <code>LOG_DIR</code>, <code>RESULTS_DIR</code> | Absolute runtime/output directories | Root derives a harness parent; direct harness creates a work child | Controls temporary runtime layout; must be writable and outside the administrator home directory for worker access |
| <code>NGINX_WORKER_USER</code>, <code>NGINX_WORKER_GROUP</code>, <code>NGINX_WORKER_PREFLIGHT_FILE</code>, <code>PERMISSIONS_LOG</code> | OS account/group and absolute log file | <code>nobody</code>; group/log derived | Controls worker-access diagnostics, not identity escalation |
| <code>NGINX_PROTOCOL_PROFILE</code>, <code>NGINX_DOWNSTREAM_PROTOCOL</code>, <code>NGINX_UPSTREAM_PROTOCOL</code> | Profile/protocol labels | Harness-specific; downstream/upstream default <code>http1</code> | Selects a build/run profile. A label is not HTTP/2 or HTTP/3 proof |
| <code>PORT</code>, <code>PORT_SEARCH_LIMIT</code>, <code>PORT_RETRY_LIMIT</code>, <code>CURL</code> | TCP port, bounds, client command | <code>18081</code>, <code>100</code>, <code>1</code>, empty | Direct smoke transport controls; use loopback and a trusted client |

### HAProxy direct entrypoint variables

| Names | Purpose and format | Default / setter | Effect and safety |
|---|---|---|---|
| <code>HAPROXY_BIN</code>, <code>SPOA_RUNTIME_BIN</code>, <code>MODSECURITY_BINDING_DIR</code> | Absolute host executable, SPOA executable, and binding directory | Root/provider-derived under <code>BUILD_ROOT</code> | Selects the native HTX/SPOA runtime inputs; do not point at untrusted binaries |
| <code>HAPROXY_SOURCE_ROOT</code>, <code>HAPROXY_DOWNLOAD_DIR</code>, <code>HAPROXY_SOURCE_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_DIR</code>, <code>HAPROXY_RUNTIME_BUILD_WORKTREE</code>, <code>HAPROXY_RUNTIME_DIR</code> | Absolute source/build/runtime paths | Framework/provider-derived | Source and host layout; source presence alone is not runtime proof |
| <code>HAPROXY_SPOA_PORT_OFFSET</code>, <code>HAPROXY_BACKEND_PORT_OFFSET</code>, <code>PORT</code>, <code>PORT_SEARCH_LIMIT</code>, <code>PORT_RETRY_LIMIT</code> | Port offsets and port search values | <code>12000</code>, <code>24000</code>, <code>18082</code>, <code>100</code>, <code>1</code> | Allocates loopback listeners for the direct harness |
| <code>HAPROXY_HTX_SOURCE_DIR</code>, <code>HAPROXY_HTX_CANONICAL_RULES_FILE</code>, <code>HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH</code>, <code>HAPROXY_HTX_BUILD_PROVENANCE</code> | Absolute HTX source/rules/evidence/provenance paths | Harness-derived or Framework baseline | Advanced HTX overlay input; preserve canonical rules and sanitized evidence |

### Envoy direct entrypoint variables

| Names | Purpose and format | Default / setter | Effect and safety |
|---|---|---|---|
| <code>ENVOY_BIN</code>, <code>EXT_PROC_BIN</code>, <code>SERVICE_BIN</code> | Absolute Envoy, ext_proc, or compatibility-service executable | Prepared-build-derived | Selects a trusted host/service binary |
| <code>ENVOY_CONFIG</code>, <code>ENVOY_CONFIG_ROOT</code>, <code>EXT_PROC_CONFIG</code>, <code>EXT_PROC_RUNTIME_CONFIG</code>, <code>OUTPUT_CONFIG</code>, <code>TEMPLATE</code>, <code>VERSION_LOCK</code> | Absolute configuration/template paths | Harness-derived | Produces or consumes runtime configuration outside the checkout |
| <code>LISTEN_ADDRESS</code>, <code>LISTEN_PORT</code>, <code>UPSTREAM_PORT</code>, <code>EXT_PROC_PORT</code>, <code>ADMIN_PORT</code> | Loopback address and TCP ports | <code>127.0.0.1</code>; <code>18080</code>, <code>18081</code>, <code>18083</code>, <code>19001</code> where defined | Controls the generated host topology; ports must be 1–65535 |
| <code>EVENT_LOG_PATH</code>, <code>COMMON_EVENT_LOG_PATH</code>, <code>COMPLETION_LOG_PATH</code>, <code>FULL_LIFECYCLE_EVIDENCE_OUTPUT</code> | Absolute event/evidence files | Runtime-root-derived or empty | Writes raw/sanitized evidence inputs; never place body payloads or secrets in them |
| <code>ENVOY_TRANSPORT_CANCEL_PROBE</code>, <code>ENVOY_PHASE4_BARRIER_TIMEOUT_SECONDS</code> | Boolean and positive timeout seconds | <code>0</code>, <code>10</code> | Opt-in diagnostic transport probe and barrier wait; non-promoting |

### Traefik direct entrypoint variables

| Names | Purpose and format | Default / setter | Effect and safety |
|---|---|---|---|
| <code>TRAEFIK_BIN</code>, <code>TRAEFIK_CONNECTOR_BIN</code>, <code>TRAEFIK_ENGINE_SERVICE_BIN</code> | Absolute executable paths | Prepared cache/build path | Selects trusted Traefik, connector, or engine service binary |
| <code>TRAEFIK_NATIVE_RUNTIME_ROOT</code>, <code>TRAEFIK_RESULT_ROOT</code>, <code>TRAEFIK_LOG_ROOT</code>, <code>TRAEFIK_CONNECTOR_START_ROOT</code>, <code>TRAEFIK_ENGINE_SERVICE_BUILD_DIR</code> | Absolute runtime/build/output paths | Build-root-derived | Controls direct host output; must be absolute, writable, and outside the checkout |
| <code>TRAEFIK_CONNECTOR_CONFIG</code>, <code>TRAEFIK_CONNECTOR_TRAEFIK_CONFIG</code>, <code>TRAEFIK_CONFIG_ROOT</code> | Configuration file/template/root paths | Connector configuration defaults or runtime-root-derived | Selects the generated File Provider/connector config |
| <code>TRAEFIK_CONNECTOR_LISTEN</code>, <code>TRAEFIK_START_LISTEN</code>, <code>TRAEFIK_START_UPSTREAM</code> | Loopback host:port values | <code>127.0.0.1:19090</code>, <code>127.0.0.1:19080</code>, <code>127.0.0.1:19091</code> | Direct start-smoke topology; only loopback addresses are accepted |
| <code>TRAEFIK_ENGINE_SERVICE_CFLAGS</code>, <code>TRAEFIK_ENGINE_SERVICE_LDFLAGS</code>, <code>MSCONNECTOR_RULES_FILE</code> | Compiler/linker flags and absolute rules file | Empty; Framework baseline when a runner supplies it | Advanced direct build/rules input; preserve shell quoting and trusted paths |

### lighttpd direct entrypoint variables

| Names | Purpose and format | Default / setter | Effect and safety |
|---|---|---|---|
| <code>LIGHTTPD_BIN</code>, <code>LIGHTTPD_SOURCE_DIR</code>, <code>LIGHTTPD_BUILD_ROOT</code>, <code>LIGHTTPD_BUILD_DIR</code>, <code>LIGHTTPD_CONFIG_DIR</code>, <code>LIGHTTPD_INCLUDE_DIR</code> | Absolute host binary/source/build/config/include paths | Prepared-build-derived | Selects the patched native host inputs; do not treat a path as evidence |
| <code>LIGHTTPD_CONNECTOR_BUILD_ROOT</code>, <code>LIGHTTPD_CONNECTOR_MODULE</code>, <code>LIGHTTPD_MODULE_DIR</code>, <code>LIGHTTPD_SMOKE_PREPARER</code> | Absolute module/build/preparer paths | Build-root-derived | Selects the connector module and direct smoke preparation |
| <code>LIGHTTPD_PATCHED_ROOT</code>, <code>LIGHTTPD_PATCHED_SOURCE_DIR</code>, <code>LIGHTTPD_PATCHED_SMOKE_DIR</code>, <code>LIGHTTPD_SMOKE_DIR</code> | Absolute patched-host and smoke directories | Build-root-derived | Holds patched host build and disposable smoke output |
| <code>LIGHTTPD_SMOKE_PORT</code>, <code>LIGHTTPD_PROXY_BARRIER_PORT</code>, <code>LIGHTTPD_PROXY_FIXTURE_PORT</code> | TCP ports | <code>18084</code>; barrier/fixture dynamically assigned | Direct loopback fixture topology |
| <code>LIGHTTPD_REQUEST_BODY_MODE</code>, <code>LIGHTTPD_RESPONSE_BODY_MODE</code>, <code>LIGHTTPD_RESPONSE_HEADER_MARKER</code>, <code>LIGHTTPD_PATCHED_REQUEST_BODY_MODE</code>, <code>LIGHTTPD_PATCHED_RESPONSE_BODY_MODE</code>, <code>LIGHTTPD_PATCHED_RESPONSE_HEADER_MARKER</code>, <code>LIGHTTPD_PATCHED_ENTITY_ENCODING</code> | Mode/marker/encoding values | <code>none</code> for unpatched direct preparation; lifecycle runner supplies streaming modes | Direct diagnostic configuration; mode selection is not a strict or protocol claim |
| <code>MSCONNECTOR_RULES_FILE</code>, <code>RULES_FILE</code>, <code>FULL_LIFECYCLE_EVIDENCE_OUTPUT</code>, <code>LD_LIBRARY_PATH</code> | Rules, evidence, dynamic-library paths | Framework baseline/derived paths | Controls input and runtime loading; never put secrets in files or untrusted directories |

## Targets, status values, IDs, and integration modes

### Primary target reference

| Target | Purpose | Prerequisites / key inputs | Output | Exit-code meaning and boundary |
|---|---|---|---|---|
| <code>make check-framework</code> | Confirms that the Framework directory exists | <code>FRAMEWORK_ROOT</code> | Console diagnostic only | <code>0</code> means the directory exists; <code>77</code> means missing prerequisite |
| <code>make prepare-runtime-components</code> | Prepares pinned reusable runtime components | Safe <code>BUILD_ROOT</code>, cache, Framework | Cache and invocation environment snapshot | Does not run every connector lifecycle |
| <code>make quick-check</code> | Runs lint-oriented source, contract, documentation, and diff checks | Python, Framework, toolchain | Diagnostics only | Does not create all-host runtime evidence |
| <code>make build-<connector></code> | Runs one connector build stage | <code>&lt;connector&gt;</code> is Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd | Connector-local build output | Build success is not a runtime or evidence claim |
| <code>make check-config-<connector></code> | Checks selected configuration loading | Prepared host and connector | Config-load diagnostics | Does not send runtime traffic |
| <code>make runtime-smoke-<connector></code> | Runs a focused minimal runtime smoke where the target exists | Prepared host, safe runtime paths | Runtime-smoke artifacts | Compatibility smoke is not full-lifecycle evidence |
| <code>make no-crs-baseline-<connector></code> | Runs capability-selected No-CRS cases | Rules file, safe paths | Canonical candidate evidence for one connector | Result status remains evidence- and capability-dependent |
| <code>make full-lifecycle-<connector></code> | Runs the selected full-lifecycle route for one connector | Generated profile/target identity plus the normal No-CRS inputs | Full-lifecycle candidate artifacts | Only matching target/profile identity may be validated |
| <code>make full-lifecycle-all-connectors</code> | Runs the six selected routes | All component prerequisites, <code>NO_CRS_RUN_ID</code> recommended | One candidate run per selected connector | Does not make production, CRS, HTTP/2, HTTP/3, or strict-for-all claims |
| <code>make evidence-check-all-connectors</code> | Validates canonical evidence for one run | <code>NO_CRS_RUN_ID</code> or per-connector latest ID, <code>EVIDENCE_ROOT</code> | Validation diagnostics | Does not rerun hosts or convert missing evidence to PASS |
| <code>make check-six-connector-core-completion</code> | Read-only compact acceptance check | <code>NO_CRS_RUN_ID</code> and finalized evidence | Aggregate diagnostics | <code>0</code> means that checker’s conditions passed, not that every catalog case or protocol passed |

<code>&lt;connector&gt;</code> in the target table is a placeholder, not literal
syntax. Allowed values are <code>apache</code>, <code>nginx</code>,
<code>haproxy</code>, <code>envoy</code>, <code>traefik</code>, and
<code>lighttpd</code>. For example, use
<code>make build-nginx</code>, not <code>make build-&lt;connector&gt;</code>.

### Status and process exit codes

| Value | Meaning |
|---|---|
| <code>PASS</code> | The specific case/check met its declared conditions with the recorded evidence. It does not generalize to unrelated profiles, protocols, or cases. |
| <code>FAIL</code> | The case/check ran or was evaluated and did not meet a required condition. |
| <code>BLOCKED</code> | A prerequisite such as a tool, source, safe path, or host component was missing. This is not a hidden PASS. |
| <code>NOT EXECUTED</code> | The case/path was deliberately not run; no runtime conclusion follows. |
| <code>NOT APPLICABLE</code> | The case does not apply to the selected profile or host model. |
| <code>UNSUPPORTED</code> | The selected host model cannot provide the required capability. |
| <code>NOT_EXECUTABLE</code> | Historical harness spelling for a case that cannot be executed in that environment. |
| <code>0</code> | The invoked process completed its own technical contract successfully. It does not guarantee all catalog cases are PASS. |
| <code>1</code> | General runtime, configuration, or validation failure where no more specific code is used. |
| <code>2</code> | Invalid invocation, validation, contract, or aggregate-input failure. |
| <code>77</code> | Missing optional/prerequisite environment such as a Framework checkout or required host input; never reinterpret this as a build PASS. |

### Rule IDs and representative case IDs

These rule IDs belong to the repository-owned No-CRS baseline in
<code>modules/ModSecurity-test-Framework/tests/rules/no-crs-baseline.conf</code>.
They are not OWASP CRS rule IDs.

| Rule ID | Phase | Baseline purpose |
|---:|---:|---|
| <code>1100001</code> | P1 | Deny the request-header marker with HTTP 403 |
| <code>1100002</code> | P1 | Deny a request-header marker with HTTP 429 |
| <code>1100003</code> | P1 | Record transaction-ID metadata |
| <code>1100101</code> | P2 | Deny the request-body marker |
| <code>1100201</code> | P3 | Deny the response-header marker |
| <code>1100202</code> | P3 | Redirect response-header probe |
| <code>1100301</code> | P4 | Observe the response-body marker and model late intervention |
| <code>1100401</code> | P1 | Redirect request-header marker |
| <code>1100402</code> | P1 | Log-only request-header marker |
| <code>1100403</code> | P1 | Drop/abort request-header marker where a host model supports it |

| Case ID | Capability / expected observation | Evidence boundary |
|---|---|---|
| <code>allow_without_marker</code> | P1 allow path | Requires a live selected host path; a 200 alone is not an all-phase assertion |
| <code>deny_header_marker_403</code> | P1 deny, rule <code>1100001</code> | Requires the recorded rule/status event fields where applicable |
| <code>deny_request_body_marker_403</code> | P2 buffered body denial, rule <code>1100101</code> | Selected only when capabilities allow it |
| <code>deny_response_header_marker_403</code> | P3 response-header behavior, rule <code>1100201</code> | May be unsupported for a host model without response view |
| <code>phase4_rule_observed</code> | P4 rule observation, rule <code>1100301</code> | Does not imply a visible pre-commit 403 |
| <code>phase4_deny_after_commit_log_only</code> | Safe late-intervention behavior | Requires the requested/actual action and commit metadata |
| <code>phase4_deny_after_commit_abort</code> | Strict late abort behavior | Remains separate and only applies where the host can demonstrate it |
| <code>phase4_first_byte_before_response_end</code> | First byte reaches the client before upstream EOS | Requires synchronized first-byte evidence |
| <code>phase4_no_full_response_buffering</code> | No connector-owned full response buffer | Requires source/runtime evidence; it is not inferred from a config value |

### Selected integration modes

| Connector | Full-lifecycle profile value | Recorded integration mode | Host role and boundary |
|---|---|---|---|
| Apache | <code>native-httpd-module</code> | <code>native-httpd-module</code> | Native Apache HTTP module; P1–P4 are run-specific and response-body evaluation may finish at EOS |
| NGINX | <code>native-nginx-http-module</code> | <code>native-nginx-http-module</code> | Native NGINX HTTP module; P1–P4 are run-specific and must be evidenced |
| HAProxy | <code>native-htx-filter</code> | <code>native-htx-filter</code> | Native HTX filter; body slices are incrementally passed and P4 finishes at HTX EOS |
| Envoy | <code>ext_proc</code> | <code>ext_proc</code> | Streamed external processing bridge; strict post-commit reset remains separate/unexecuted until proven |
| Traefik | <code>native-middleware</code> | <code>native-traefik-middleware</code> | Native middleware using a local UDS Common/libmodsecurity service; strict reset remains separate/unexecuted until proven |
| lighttpd | <code>patched-native</code> | <code>patched-native-lighttpd</code> | Patched native lighttpd host/module; entity-body ranges are handled before transfer framing and P4 finishes at entity EOS |

<code>ext_authz</code>, <code>forwardAuth</code>, and
<code>spoe-spop-agent</code> can appear as compatibility or alternate
integration terms in connector material. They must not be silently relabelled
as the selected full-lifecycle route. See the [glossary](../reference/glossary.md)
for concise definitions and [connector documentation](../connectors/README.md)
for navigation.

## Related documentation

- [Build documentation](../build/README.md) explains target families and safe
  build paths.
- [Testing documentation](../testing-and-evidence.md) explains status, selection,
  and validation boundaries.
- [Evidence documentation](../testing-and-evidence.md) explains artifacts and
  promotion boundaries.
- The [change traceability policy](../change-traceability.md) defines the
  required bilingual explanation for future variables and placeholders.
- `AGENTS.md` is an optional local instruction file for Codex and is not part of
  the versioned project documentation. It has no German companion file.
