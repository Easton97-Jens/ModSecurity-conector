# Change Record: Parent Common targeted-evaluator C++17 remediation

**Language:** English | [Deutsch](CR-20260729-sonar-common-targeted-evaluator-cpp17.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-targeted-evaluator-cpp17 |
| Date (UTC) | 2026-07-29 |
| Base revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | 24 initially reported SonarQube Cloud Code Smells in `common/scripts/modsecurity_targeted_eval.cc`, including C++20-only API recommendations, shadowed names, raw-string delimiters, and cognitive complexity. |
| Boundary | Parent Common evaluator source and paired Change Records. No Framework, MRTS, Gitlink, workflow, Sonar configuration, or suppression change. |

## Motivation and problem statement

The targeted evaluator is deliberately compiled as C++17. Its argument parsing,
request construction, ModSecurity evaluation, intervention cleanup, and JSON
result output had accumulated a large control-flow body and recommendations for
APIs not available in C++17. The remediation must reduce the reported source
issues without changing CLI semantics, ModSecurity object ownership, response
selection, or cleanup ordering.

## Acceptance criteria

- The evaluator remains compatible with C++17; no C++20 container or string
  membership API is introduced.
- Existing CLI option values, CRS selection, request mapping, JSON fields,
  intervention status, and cleanup order are preserved.
- The implementation separates option parsing, request setup, transaction
  evaluation, decision-log construction, and success JSON rendering into
  small named units.
- Hosted checks and a fresh exact-head SonarQube Cloud analysis must still
  prove zero New Issues and zero New-Code Duplicate Lines before any integration
  claim.

## Implementation decision and rationale

`ArgumentMap` uses `std::less<>` and a helper lookup based on `lower_bound`,
avoiding C++20-only `contains` while also removing repeated map membership
tests. The request-specific logic is partitioned into narrow helper functions
whose parameters make existing ownership and cleanup relationships explicit.
String search uses the local C++17 `string_contains` helper, preserving the
former guarded substring condition. `main` retains the former resource
lifetime and cleanup sequence.

## Changed files

- `common/scripts/modsecurity_targeted_eval.cc` — C++17-compatible option
  lookup and decomposition of evaluator setup, execution, result logging, and
  success JSON rendering.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics` | passed; 7 tests passed with Python 3.14.4 (the repository pin is 3.14.6). |
| `make check-targeted-evaluator-cpp17` with GCC 15 and task-owned external libmodsecurity include/build paths | passed against real libmodsecurity 3.0.14. |
| `make check-targeted-evaluator-cpp17` with Clang 21 and the same real libmodsecurity interface | passed. |
| Real evaluator runtime controls | passed: phase-1 targeted-header block (403), legitimate header allow (200), and phase-2 request-body block (403). |
| Parser negative controls | passed: missing rule, unsupported ruleset, and dangling `--rule-file` each returned the expected structured error. |
| `git diff --check` | passed. |
| Focused bilingual-documentation suite | passed; 21 tests passed. |
| Broad repository documentation checker | blocked by missing Framework-submodule link targets in the isolated Parent worktree; it is not reported as passed. |
| Focused Codex Security diff scan | passed with zero reportable findings for the synchronized candidate; sealed scan ID: `67fe74f1f0cf8d21c820e330fae31433ab68ebf4_20260729T155321Z`. |

## Security impact

This evaluator maps operator-selected command-line values into a ModSecurity
transaction and result evidence. The change does not broaden accepted options,
relax validation, change rule-file handling, alter HTTP request/body mapping,
or move intervention/resource cleanup. The focused exact-head review found no
newly reachable security regression. Real libmodsecurity controls confirm the
expected header/body block and legitimate-allow behavior; they do not replace
the required hosted exact-head delivery gates.

## Runtime evidence

The task-owned external test environment links and executes the evaluator
against real libmodsecurity 3.0.14. GCC 15 and Clang 21 both pass the native
C++17 target; direct phase-1 header, phase-2 body, legitimate-allow, and
parser-negative controls provide local enforcement evidence.

## Known limitations

- The direct diagnostics suite used Python 3.14.4 while `.python-version`
  specifies 3.14.6.
- The broad repository documentation checker is blocked by missing Framework
  submodule link targets in the isolated Parent worktree.
- Hosted CI and a fresh exact-head SonarQube Cloud analysis for the final
  delivery candidate are pending.

## Checks not run and rationale

The broad repository documentation checker cannot complete in this isolated
Parent worktree because its Framework-submodule link targets are absent. The
final delivery candidate has not yet received hosted CI or SonarQube Cloud
analysis; those exact-head gates remain required before integration.

## Remaining risks

Future changes must retain C++17 compilation and preserve the explicit cleanup
order around transaction, rules, and ModSecurity instances. Any new option that
affects a rule path, request data, or audit output needs its own input-boundary
review.

## Final diff and review status

The candidate is confined to Parent Common evaluator source and bilingual
traceability. Local C++17, runtime, contract, whitespace, and focused security
evidence are complete under the recorded limitations; exact-head hosted
verification remains required before any delivery or merge claim.
