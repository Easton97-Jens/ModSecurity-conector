# Change Record: Reproducible C and C++ diagnostics

**Language:** English | [Deutsch](CR-20260713-c-cpp-diagnostics.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Reproducible C and C++ diagnostics |
| Change ID | CR-20260713-c-cpp-diagnostics |
| Date (UTC) | 2026-07-13T20:53:43Z |
| Author or executing agent | Codex agent <code>/root</code> |
| Base revision | 66c09cc4787025ac2babd9612d0f0bfdf7958f26 |
| Related issue or pull request | None |
| Final revision | Not committed |

## Motivation and problem statement

Provide a reproducible local diagnostics baseline for the repository-owned
NGINX C17 sources and the targeted C++17 evaluator. The former compilation
database omitted a source listed by the connector configuration, and neither
the evaluator nor a documented <code>clangd</code> validation path was covered.
The scope is integration level 1 only: local source diagnostics, not a runtime
or production-quality claim.

## Affected components and security boundaries

The change affects local Make targets, repository checks, compilation-database
generation, developer documentation, and focused contract tests. It does not
change connector request processing, ModSecurity policy, externally supplied
headers or libraries, Framework sources, the Framework submodule pointer, CI
workflows, or CI gating.

The compilation database and <code>clangd</code> cache are intentionally local
and unversioned. They must be written to an explicit external absolute path;
the root <code>compile_commands.json</code> and <code>.cache/clangd/</code> are
ignored. Build products, caches, and tool output remain outside the checkout.
Requested output paths are canonicalized and rejected before any output
directory is created when they resolve inside the checkout.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Every configured NGINX/Common C source is represented by the C17 list | Met | Source-parity contract test and <code>check-nginx-c-standard-wiring</code> pass; 31 units are captured. |
| A local C++17 evaluator diagnostic and compilable C++ compilation-database entry exist | Met | The evaluator target and merged database validation pass. |
| The merged database preserves real Bear commands, filters to tracked source files, and is atomically published externally | Met | Focused database contract tests and both database targets pass. |
| <code>clangd</code> diagnoses the NGINX module, <code>late_intervention.c</code>, and evaluator without fixes or Tidy | Met | Focused <code>clangd</code> target passes with a 32-unit database. |
| Documentation and records explain scope, paths, tools, limitations, and no runtime claim in English and German | Met | <code>check-bilingual-docs</code>, document-link, and variable-documentation checks pass after the Change-Record pair was added. |

## Alternatives investigated

- Keep the old partial compilation database. Rejected because it silently
  omitted a C source that is configured for both NGINX build branches.
- Synthesize compiler commands from a hand-written source list. Rejected in
  favor of Bear-captured commands so the database reflects actual invocations.
- Add <code>.clangd</code>, <code>.clang-tidy</code>, static analysis, sanitizers,
  CI gates, or a workflow. Rejected because they exceed the requested local
  integration-level scope.
- Automatically download or provision NGINX headers during the C17 check.
  Rejected; missing local prerequisites now produce the documented blocked
  result instead.

## Implementation decision and rationale

Add isolated local analysis targets that require real compilers, Bear, and
<code>clangd</code>. Capture NGINX C17 commands with Bear, compile the targeted
evaluator under C++17 with the required warnings, capture that invocation, and
merge only validated tracked translation units into an atomically replaced
external database. The C17 source list is made an exact parity contract with
both connector configuration branches, including
<code>common/src/late_intervention.c</code>.

<code>clangd</code> receives an explicitly staged copy of that database and is
run with configuration and Tidy disabled, no tweaks, no background index, and
no write/fix mode. External ModSecurity headers are passed as system headers to
keep third-party warning noise outside the repository-owned evaluator result.

## Changed files

Versioned files in scope include:

- <code>.gitignore</code> and <code>Makefile</code>
- <code>ci/checks/analysis/check-analysis-tools.sh</code>,
  <code>ci/checks/analysis/compile_database.py</code>,
  <code>ci/checks/analysis/compile-db-nginx-c17.sh</code>,
  <code>ci/checks/analysis/check-targeted-evaluator-cpp17.sh</code>,
  <code>ci/checks/analysis/compile-db-cpp17.sh</code>, and
  <code>ci/checks/analysis/check-clangd-c17.sh</code>
- <code>ci/checks/connectors/nginx/check-nginx-c-standards.sh</code> and
  <code>ci/checks/connectors/nginx/check-nginx-c-standard-wiring.py</code>
- <code>tests/test_c_cpp_diagnostics.py</code>
- English/German pairs <code>docs/build/README.md</code>,
  <code>docs/build/README.de.md</code>, <code>docs/reference/variables.md</code>,
  and <code>docs/reference/variables.de.md</code>
- this English/German Change-Record pair and its English/German indexes

No Framework submodule files or pointer, no workflow files, and no CI command
were changed. Intentional local unversioned artifacts are the external
compilation database and optional external build roots only.

## Tests added or changed

Added <code>tests/test_c_cpp_diagnostics.py</code>. It checks exact configured
C-source parity, target wiring and scope boundaries, validated C17/C++17
database merging, deduplication, rejection of root output and untracked input,
rejection before a checkout directory can be created, both missing-coverage
cases, the documented exit-77 tool-blocking path, and preservation of an
existing database after an invalid capture.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>rtk sh -n ci/checks/analysis/*.sh ci/checks/connectors/nginx/check-nginx-c-standards.sh</code> | 0 | Shell syntax passed for the new local-analysis scripts and adjusted C17 check. | None | None |
| <code>rtk PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile ci/checks/analysis/compile_database.py ci/checks/connectors/nginx/check-nginx-c-standard-wiring.py tests/test_c_cpp_diagnostics.py</code> | 0 | Python syntax compilation passed and no bytecode was retained. | None | None |
| <code>rtk PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics</code> | 0 | Five focused source-parity, output-path, tool-blocking, and database contract tests passed. | None | None |
| <code>rtk TMPDIR=$CODEX_TEMP_ROOT/tmp-final-check PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics</code> | 1 | A final agent invocation used a nonexistent external temporary directory and failed before source tests; no repository source failure occurred. After creating that canonical task directory, the same five tests passed. | None | None |
| <code>rtk python3 ci/checks/connectors/nginx/check-nginx-c-standard-wiring.py</code> | 0 | Direct wiring validation passed. | None | None |
| <code>rtk make check-nginx-c-standard-wiring</code> | 0 | Make target wiring validation passed. | None | None |
| <code>rtk make check-analysis-tools</code> | 0 | Configured C/C++ compilers, Bear, and <code>clangd</code> were found and version-reported. | None | None |
| <code>rtk make check-nginx-c17 BUILD_ROOT=$BUILD_ROOT NGINX_SOURCE_DIR=$NGINX_SOURCE_DIR MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR</code> | 0 | All 31 configured NGINX/Common C17 translation units compiled with required warnings. | <code>$BUILD_ROOT/nginx-c17/</code> | None |
| <code>rtk make compile-db-nginx-c17 COMPDB_OUTPUT=$ANALYSIS_ROOT/compile_commands.json NGINX_SOURCE_DIR=$NGINX_SOURCE_DIR MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR</code> | 0 | Bear capture was validated and atomically published 31 unique C17 units. | <code>$ANALYSIS_ROOT/compile_commands.json</code> | None |
| <code>rtk python3 -m json.tool $ANALYSIS_ROOT/compile_commands.json</code> | 0 | The published C17 compilation database was valid JSON. | <code>$ANALYSIS_ROOT/compile_commands.json</code> | None |
| <code>rtk make check-targeted-evaluator-cpp17 CPP_BUILD_ROOT=$BUILD_ROOT MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR=$MODSECURITY_LIB_DIR</code> | 2 | Initial attempt failed because external ModSecurity headers emitted warnings under <code>-Werror</code>. | None | None |
| <code>rtk make check-targeted-evaluator-cpp17 CPP_BUILD_ROOT=$BUILD_ROOT MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR=$MODSECURITY_LIB_DIR</code> | 0 | Re-run after treating external headers as system headers compiled the repository evaluator under C++17; it was not executed. | <code>$BUILD_ROOT/cpp-evaluator/</code> | None |
| <code>rtk make compile-db-cpp17 COMPDB_OUTPUT=$ANALYSIS_ROOT/compile_commands.json CPP_BUILD_ROOT=$BUILD_ROOT MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR=$MODSECURITY_LIB_DIR</code> | 0 | Captured evaluator entry merged with C17 entries; database contained 32 unique units. | <code>$ANALYSIS_ROOT/compile_commands.json</code> | None |
| <code>rtk make check-clangd-c17 COMPDB_OUTPUT=$ANALYSIS_ROOT/compile_commands.json</code> | 0 | Database validation and diagnostics of the NGINX module, <code>late_intervention.c</code>, and evaluator completed with no errors. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Documentation-pair validation passed after this Change-Record pair was added. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Repository document links passed after this Change-Record pair was added. | None | None |
| <code>rtk make check-variable-documentation</code> | 0 | Documented-variable validation passed after this Change-Record pair was added. | None | None |

## Security impact

No connector runtime security behavior changes. The new scripts validate local
paths, require external output locations, filter compilation-database entries
to tracked repository source files, and atomically replace a validated output.
They do not download prerequisites, enable source rewriting, or process runtime
traffic. These checks reduce accidental use of stale or injected local entries
without making a security or production-quality claim.

## Documentation changes

Added English/German local-diagnostics guidance in
<code>docs/build/README.md</code> and <code>docs/build/README.de.md</code>.
Added the relevant variable descriptions to
<code>docs/reference/variables.md</code> and
<code>docs/reference/variables.de.md</code>. Added this English/German
Change-Record pair and index entries.

## Runtime evidence

No runtime evidence was collected or claimed for this change. The evaluator
binary was compiled but not executed, and diagnostics do not constitute a
connector runtime or production-quality claim.

## Known limitations

- Coverage is limited to repository-owned NGINX/Common C17 sources and the
  single targeted C++17 evaluator; other connectors and C++ sources are not
  covered.
- Local prerequisites and absolute external paths are required. Missing tools
  or local prerequisites report exit status 77 rather than provisioning them;
  absent or invalid required parameters report exit status 2.
- <code>clangd</code> validates selected files from the merged database; it is
  not a static-analysis, sanitizer, or runtime test.
- <code>-Werror</code> applies to repository evaluator code. External
  ModSecurity headers are deliberately system headers, so this does not assess
  third-party header warning quality.

## Remaining risks

Compiler, Bear, and <code>clangd</code> versions can differ across developer
machines, so diagnostics may vary despite the documented flags. The targets
report the selected tool versions and preserve real captured commands. Future
source-list or connector-configuration changes require the parity contract test
to be maintained.

## Checks not run and rationale

- <code>make quick-check</code> and <code>make lint</code> were not run because
  this scoped local diagnostics change has focused C17, C++17, database,
  <code>clangd</code>, documentation, and contract-test evidence; neither is a
  requested CI gate.
- Static analyzers, sanitizers, <code>clang-tidy</code>, runtime/lifecycle
  tests, and production deployment checks were not run because they are
  explicitly outside integration level 1 and no runtime claim is made.
- The focused contract test exercises a missing compiler through
  <code>check-analysis-tools</code> and verifies exit status 77. No separate
  manual missing-prerequisite invocation was needed because the real
  verification environment supplied the required prerequisites.

## Final diff and review status

The final focused contract test, documentation checks, whitespace review,
submodule checks, and status inspection passed after this Change-Record update.
The final external database contains 32 unique translation units; the C17,
C++17, and <code>clangd</code> targets pass. <code>git diff --check</code>
reports no whitespace diagnostics, and both the Framework submodule diff and
its worktree status are empty. An independent read-only diff review found and
the change corrected the pre-directory-creation checkout-path rejection,
missing-coverage tests, the exit-77 test, quoted tool invocation, and the
external-header limitation. No commit or pull request has been created.
