# Change Record: Parent Common targeted-evaluator C++17 remediation

**Language:** English | [Deutsch](CR-20260729-sonar-common-targeted-evaluator-cpp17.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-targeted-evaluator-cpp17 |
| Date (UTC) | 2026-07-29 |
| Base revision | `fd0b2f4bdd3ca42b496deae85fcd1d2aee6adc1c` |
| Tracking | 24 current SonarQube Cloud Code Smells in `common/scripts/modsecurity_targeted_eval.cc`, including C++20-only API recommendations, shadowed names, raw-string delimiters, and cognitive complexity. |
| Boundary | Parent Common evaluator source and paired Change Records. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

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

`ArgumentMap` uses a transparent comparator and helper lookup based on
`lower_bound`, avoiding C++20-only `contains` while also removing repeated map
membership tests. The request-specific logic is partitioned into narrow helper
functions whose parameters make existing ownership and cleanup relationships
explicit. String search uses `std::search`, which is available in C++17.
`main` retains the former resource lifetime and cleanup sequence.

## Changed files

- `common/scripts/modsecurity_targeted_eval.cc` — C++17-compatible option
  lookup and decomposition of evaluator setup, execution, result logging, and
  success JSON rendering.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v tests.test_c_cpp_diagnostics` | passed; 7 tests passed. |
| `g++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only` with a task-owned external libmodsecurity interface stub | passed. |
| `clang++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only` with the same stub | passed. |
| C++17 stub-backed link and evaluator controls | passed; the CRS result contract and missing-`--rule-file` error contract were both exercised. |
| `make check-targeted-evaluator-cpp17` | blocked by the environment: `MODSECURITY_INCLUDE_DIR` and the real libmodsecurity development headers/library are absent (target exits 77). |
| `git diff --check` | passed. |
| Follow-up local controls | passed: 28 C/C++ diagnostics and bilingual-documentation tests, C++17 `g++`/`clang++` checks with `-Werror`, and stub-backed CRS, missing-rule-file, request-body-marker-present, and request-body-marker-absent controls. |
| Focused Codex Security diff scan | passed with zero reportable findings; sealed report: `/var/tmp/codex/ModSecurity-conector/runs/20260729-complete-common-connectors-sonar-remediation/security-scans/fc6027681cfae342dcef8e1606a38523c450044c_20260729T084000Z/report.md`. |

## Security impact

This evaluator maps operator-selected command-line values into a ModSecurity
transaction and result evidence. The change does not broaden accepted options,
relax validation, change rule-file handling, alter HTTP request/body mapping,
or move intervention/resource cleanup. The focused diff review found no newly
reachable security regression. The real external libmodsecurity runtime remains
an explicit unavailable dependency rather than a substituted security claim.

## Runtime evidence

The task-owned stub permits C++17 syntax, link, successful CRS-result, and
invalid-option controls to be executed locally. It is not a libmodsecurity
runtime or an enforcement assertion. A repository-native link/runtime check is
blocked by missing external development artifacts.

## Known limitations

- The local environment has no real libmodsecurity headers or library, so the
  evaluator was not linked or executed against that dependency.
- Hosted CI and a fresh exact-head SonarQube Cloud analysis are pending.

## Checks not run and rationale

The native `make check-targeted-evaluator-cpp17` link/runtime control was not
run successfully because this environment does not provide the external
libmodsecurity development headers, library, or required include path. The
task-owned C++17 stub validates syntax and selected evaluator contracts only;
it does not replace a real libmodsecurity runtime result.

## Remaining risks

Future changes must retain C++17 compilation and preserve the explicit cleanup
order around transaction, rules, and ModSecurity instances. Any new option that
affects a rule path, request data, or audit output needs its own input-boundary
review.

## Final diff and review status

The candidate is confined to Parent Common evaluator source and bilingual
traceability. Local C++17, contract, whitespace, and focused security evidence
are complete; a separate Draft PR and exact-head hosted verification are still
required before any delivery or merge claim.
