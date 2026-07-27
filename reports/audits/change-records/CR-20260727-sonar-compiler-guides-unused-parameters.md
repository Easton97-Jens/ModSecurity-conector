# Change Record: Parent compiler-guide unused-parameter cleanup for SonarQube Cloud S1172

**Language:** English | [Deutsch](CR-20260727-sonar-compiler-guides-unused-parameters.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-compiler-guides-unused-parameters |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S1172` Code Smells AZ9cRzBeHhV2CayPTP57 (line 604), AZ9cRzBeHhV2CayPTP58 (line 779), AZ9cRzBeHhV2CayPTP5- (line 3559), AZ9cRzBeHhV2CayPTP5_ (line 3573), and AZ9cRzBeHhV2CayPTP6A (line 3610). |
| Boundary | Parent Python generator and this English/German Change Record pair plus indexes. Generated guides, connector/runtime behavior, Framework, MRTS, gitlinks, Sonar scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and problem statement

The selected SonarQube Cloud rows identify five function parameters in the
Parent compiler-guide generator that are not read by their function bodies.
Removing only those parameters and their direct call-site arguments clarifies
the actual dependency contract without changing rendered guide content.

## Acceptance criteria

- Remove only the five reported unused parameters and matching direct call-site arguments.
- Preserve generated English/German guide content, generator data, command strings, and runtime behavior.
- Pass the complete focused `tests.test_compiler_guides` module before and after the edit and pass `git diff --check`.
- Maintain an equivalent English/German Change Record pair and record indexes.
- Do not claim any Sonar issue closed before an exact candidate-head analysis observes it.

## Implementation decision and rationale

`route_comparison` and `selected_preparation` no longer receive their unused
`item` parameter. The NGINX and Apache validation helpers and the Apache
runtime helper no longer receive their unused `german` parameter. Direct call
sites now pass only the values consumed by their callee; no branch or returned
documentation string changed.

## Changed files

- scripts/generate_compiler_guides.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

Focused commands use the Parent `.venv` Python, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONNOUSERSITE=1`, and task-owned external `TMPDIR`:

- rtk proxy env ... `<Parent .venv python>` -m unittest -v tests.test_compiler_guides (before the edit)
- rtk proxy env ... `<Parent .venv python>` -m unittest -v tests.test_compiler_guides (after the edit)
- rtk proxy env ... `<Parent .venv python>` -m unittest -v tests.test_bilingual_docs
- rtk proxy make check-bilingual-docs
- rtk proxy make check-doc-links
- rtk proxy sh -c 'git diff --check && git diff -- scripts/generate_compiler_guides.py && git status --short'

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused compiler-guide module before the edit | passed: `tests.test_compiler_guides`, 20 tests in 0.649s. |
| Focused compiler-guide module after the edit | passed: `tests.test_compiler_guides`, 20 tests in 0.638s. |
| `git diff --check` | passed: no whitespace error. |
| Direct source-diff review | passed: only five unused parameters and direct call-site arguments changed. |
| Bilingual checker unit module | passed: `tests.test_bilingual_docs`, 13 tests in 0.034s. |
| Direct Change Record pair contract | passed: `check_change_record_pair` returned no error. |
| `make check-bilingual-docs` | blocked_environment: 20 existing missing Framework-gitlink link targets; no error cites this Change Record pair or its index. |
| `make check-doc-links` | blocked_environment: 16 existing missing Framework-gitlink link targets; no error cites this Change Record pair or its index. |

## Security impact

The focused security assessment is `not_applicable`: this change only removes
unused Python function parameters in a documentation generator. It changes no
path guard, network client/server, subprocess, connector, credential,
generated guide content, or runtime control. No security finding is claimed
fixed.

## Documentation status

The focused generation test shows that emitted English/German guide files are
unchanged. The direct pair contract and bilingual checker unit suite pass; the
full repository documentation checks are blocked only by the uninitialized
Framework Gitlink's pre-existing link targets. This versioned English/German
Change Record pair and both record indexes provide the traceability for the
source-only cleanup.

## Runtime evidence

No connector, host, protocol, or production runtime behavior changed or is
claimed. The focused unit test checks generator output and documentation
contracts; it is not runtime evidence.

## Known limitations

This batch addresses only five selected Parent `python:S1172` rows from the
current 1,125-item SonarQube Cloud inventory. The keys remain OPEN in that
inventory until a new analysis evaluates a delivered candidate head.

## Remaining risks

An accidental missed call site could fail guide generation or alter a guide.
The narrow signature-only diff and complete focused generator suite before and
after the edit reduce that risk. No conclusion about unrelated Sonar rows or
security findings follows from this cleanup.

## Checks not run and rationale

- Full repository documentation checks are not passed because the task
  worktree deliberately has no initialized Framework Gitlink. `make
  check-bilingual-docs` reports 20 and `make check-doc-links` reports 16
  existing missing Framework paths; the focused bilingual unit suite and the
  direct pair contract both pass.
- Connector builds, host configuration checks, runtime smokes, protocol matrices, Framework checks, and MRTS checks are not applicable because no connector/runtime implementation or cross-repository content changed.
- No hosted SonarQube Cloud analysis, GitHub CI, commit, push, pull request, or merge has been performed; the current task has no master-integration authorization.

## Final diff and review status

The local task-worktree candidate is uncommitted and contains the signature
cleanup plus required traceability material. No source changed in the
authoritative Parent checkout. No Framework or MRTS action, Gitlink update,
scanner-control change, external issue disposition, push, pull request, or
master merge has occurred. Later local documentation validation and any
delivery evidence will be recorded only from observed results.
