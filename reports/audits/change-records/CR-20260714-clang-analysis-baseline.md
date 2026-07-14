# Change Record: Advisory Clang analysis baseline

**Language:** English | [Deutsch](CR-20260714-clang-analysis-baseline.de.md)

## Identity

| Field | Value |
| --- | --- |
| Title | Advisory Clang analysis baseline |
| Change ID | CR-20260714-clang-analysis-baseline |
| Date (UTC) | 2026-07-14T08:14:23Z |
| Author or executing agent | Codex agent <code>/root</code> |
| Base revision | 0fec00442b0031c206b627a44735f1eb07534d51 |
| Related issue or pull request | None |
| Final revision | Not committed |

## Motivation and problem statement

Provide an opt-in, advisory Clang-Tidy and Clang Static Analyzer baseline for
the already available C17/C++17 compilation database. The result must expose
and classify local diagnostics without converting findings into a source-fix,
CI-gate, runtime, production, or security-release claim.

## Affected components and security boundaries

The change affects root Make targets, an analysis-only runner, focused root
contract tests, developer documentation, variable reference material, and this
Change Record pair. Raw logs, SARIF files, staged CDB copies, and normalized
JSON remain under <code>$CODEX_TEMP_ROOT</code> outside the checkout.

It does not change connector request processing, product C/C++ source,
Framework source or submodule state, workflows, CI policy, runtime behavior,
or production configuration. Pre-existing independent worktree changes were
snapshotted and left unchanged.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Four opt-in advisory targets exist and are absent from lint, quick checks, runtime tests, and workflows | Met | Makefile contract test and target review |
| CDB and output validation is absolute, external to the checkout, marked-temp-root constrained, and read-only | Met | Focused contract tests and baseline read-only summaries |
| Findings do not fail a technically complete baseline | Met | Tidy, analyzer, and combined baseline exits were <code>0</code> with findings |
| Invalid/unsafe input, missing prerequisites, and technical tool failures preserve the documented exit semantics | Met | Focused contract tests |
| Normalized JSON has only the allowed classifications and required operational metadata | Met | Focused contract tests and combined JSON review |
| English/German documentation and a matching Change Record pair describe the same boundary | Met | Bilingual, link, and variable-documentation checks passed |

## Alternatives investigated

- Use <code>scan-build</code>. Rejected because it is not installed and direct
  <code>clang --analyze</code> provides a controlled, owned SARIF path.
- Add <code>.clang-tidy</code>, automatic fixes, <code>NOLINT</code>, or a CI
  gate. Rejected because they would make a local advisory baseline mutate
  source or impose policy outside this task.
- Treat all tool diagnostics as confirmed bugs or vulnerabilities. Rejected:
  tool output is triage input and security candidates require separate Codex
  Security validation.

## Implementation decision and rationale

Add <code>clang_analysis_baseline.py</code> with narrow shell/Make entry
points. It validates the supplied compilation database before output creation,
uses <code>clang-tidy</code> with explicit inline
<code>-*,bugprone-*,cert-*</code> configuration, and runs the static analyzer
directly through <code>clang</code>/<code>clang++</code> with the
<code>core,unix,security,cplusplus,deadcode</code> profile. Original CDB
compiler drivers and output-writing flags are never executed or reused.

The runner writes raw artifacts only below the supplied analysis directory,
normalizes/deduplicates findings, retains all seven allowed classification
counter keys, and records CDB/source/worktree snapshots. Tool non-zero exits
are technical errors; warnings with successful tool completion are not gates.

## Changed files

Versioned files in scope are:

- <code>Makefile</code>
- <code>ci/checks/analysis/check-clang-analysis-tools.sh</code> and
  <code>ci/checks/analysis/clang_analysis_baseline.py</code>
- <code>tests/test_clang_analysis_baseline.py</code>
- English/German pairs <code>docs/build/README.md</code>,
  <code>docs/build/README.de.md</code>, <code>docs/reference/variables.md</code>,
  and <code>docs/reference/variables.de.md</code>
- this English/German Change-Record pair and its English/German indexes

No product or connector source, Framework file or pointer, GitHub workflow, CI
gate, <code>.clang-tidy</code>, or <code>NOLINT</code> entry is changed.

## Tests added or changed

Added <code>tests/test_clang_analysis_baseline.py</code>. Its eight contract
tests cover missing and invalid CDBs, relative/checkout/symlink-escaping paths,
missing tools, unsafe compiler arguments, read-only behavior, finding-success
semantics, technical tool failure, required normalized JSON fields,
classification values, system and third-party headers, staging cleanup, and
opt-in Make wiring.

## Commands executed

| Exact command | Exit code or result | Sanitized relevant summary | Canonical evidence path | Run ID |
| --- | --- | --- | --- | --- |
| <code>rtk make check-clang-analysis-tools</code> | 0 | LLVM 21.1.8 <code>clang-tidy</code>, <code>clang</code>, and <code>clang++</code> were available. | None | None |
| <code>rtk make clang-tidy-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 2 | Initial Make argument spelling let the leading <code>-</code> selector be parsed as an option; no baseline artifacts or source changes were produced. | None | None |
| <code>rtk make clang-tidy-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 0 | All 32 units completed; 28 raw occurrences normalized to 23 findings: 22 <code>needs_validation</code>, 1 unconfirmed <code>possible_security_candidate</code>. | <code>$ANALYSIS_OUTPUT/clang-tidy-baseline.json</code> | None |
| <code>rtk make clang-analyzer-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 1 | Initial C++ SARIF invocation exposed a missing owned raw-output directory; the runner was corrected and no source changed. | <code>$ANALYSIS_OUTPUT/clang-analyzer-baseline.json</code> | None |
| <code>rtk make clang-analyzer-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 0 | All 32 units completed; 33 normalized <code>possible_security_candidate</code> findings were reported as unconfirmed. | <code>$ANALYSIS_OUTPUT/clang-analyzer-baseline.json</code> | None |
| <code>rtk make clang-analysis-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 0 | Both paths completed across 32 units each; 61 raw occurrences normalized to 56 findings: 22 <code>needs_validation</code> and 34 unconfirmed <code>possible_security_candidate</code>. | <code>$ANALYSIS_OUTPUT/clang-analysis-baseline.json</code> | None |
| <code>rtk .venv/bin/python -m unittest -v tests.test_clang_analysis_baseline</code> | 0 | Eight focused analysis-baseline contract tests passed. | None | None |
| <code>rtk .venv/bin/python -m unittest -v tests.test_c_cpp_diagnostics</code> | 0 | Five existing C/C++ diagnostics contracts passed after Makefile integration. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Bilingual document structure and parity passed. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Repository and Framework document links passed. | None | None |
| <code>rtk make check-variable-documentation</code> | 0 | 85 documented variable references passed. | None | None |
| <code>rtk git diff --check</code> | 0 | No whitespace errors were reported. | None | None |

## Security impact

No connector runtime security behavior changes. The baseline narrows local
path and compiler-argument handling, prevents automatic source rewrites, and
keeps raw artifacts outside the repository. Its 34 combined
<code>possible_security_candidate</code> results are unconfirmed tool signals,
not confirmed vulnerabilities; they require separate Codex Security
validation before remediation or disclosure work.

## Documentation changes

Updated the English/German local diagnostics guide and variable reference with
the targets, safe path requirements, check profiles, exit codes, JSON schema
boundary, classifications, no-fix/no-gate policy, and advisory limitations.
Added this English/German Change Record and the companion index entries.

## Runtime evidence

No runtime evidence was collected or claimed for this change. The CDB-driven
source analysis neither runs connector traffic nor establishes a runtime,
production, CRS, lifecycle, or security result.

## Known limitations

- Coverage is limited to the supplied 32-unit database: 31 C17 and one C++17
  translation unit. Apache, HAProxy, Envoy, Traefik, and lighttpd are not
  covered by this database.
- Tidy and analyzer diagnostics can vary by Clang version, target headers, and
  compilation database content.
- The baseline classifies triage state only; it does not resolve or suppress a
  finding.

## Remaining risks

The 34 combined possible security candidates and 22 validation findings need
human review. Header filtering and tool-model limitations can create false
positives or omit paths. The safety controls prevent output-path and source
rewrite mistakes, but they do not replace a dedicated security scan or runtime
test.

## Checks not run and rationale

- <code>make quick-check</code> and <code>make lint</code> are not run as an
  advisory baseline gate; focused contracts and required documentation checks
  provide the relevant source-level verification.
- Builds, configuration checks, runtime/lifecycle tests, production deployment,
  and Codex Security validation are not run. They are outside this advisory
  baseline and no runtime/security conclusion is claimed.

## Final diff and review status

The focused eight-test baseline suite, five-test existing diagnostics suite,
documentation checks, link checks, variable-reference check, and
<code>git diff --check</code> passed. The supplied CDB retained SHA-256
<code>c6f5c89e03811faf8f8a00e38066f9f79a303524ef7d94b5f1330634e70deb75</code>,
and the Framework worktree and submodule pointer remained unchanged. The parent
worktree contains independent concurrent changes outside this scope; they were
not modified or reset. This record matches the advisory-baseline files and
actual outcomes. The intended commit subject is
<code>Add advisory Clang analysis baseline</code>.
