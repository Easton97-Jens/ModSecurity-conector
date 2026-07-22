# Change Record: Parent CI and scripts literal deduplication for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260722-sonar-ci-scripts-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260722-sonar-ci-scripts-literals |
| Date (UTC) | 2026-07-22 |
| Base revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Tracking | Thirteen Parent-only python:S1192 Code Smells: seven in scripts/generate_connector_guides.py and six in ci/evidence/reports/generate-system-environment-proof.py. |
| Boundary | Parent CI/report and guide-generator source plus this English/German traceability pair and indexes. Framework, MRTS, gitlinks, generated guide content, scanner configuration, Quality Gates, suppressions, and runtime connector behavior remain unchanged. |

## Motivation and problem statement

SonarQube Cloud reports repeated immutable metadata literals in two Parent Python
generators. The occurrences describe guide-table metadata, fallback labels, the
POSIX shell path, report table markup, and the Apache tool name. They can be
expressed as module constants without changing generated text, tool resolution,
path checks, report layout, or control flow.

## Acceptance criteria

- Route every selected repeated literal through an immutable module-level
  constant, without changing its value or use-site behavior.
- Preserve generated connector-guide output and the system-environment-proof
  generator's successful --skip-check-runs path.
- Keep both Change Record languages and both indexes equivalent.
- Obtain fresh SonarQube Cloud and hosted-check evidence for the exact Draft
  PR head before calling any selected key resolved.

## Implementation decision and rationale

The guide generator now names the shared rule-file metadata, provisioning,
provider, and build-directory strings once. The system-environment-proof
generator similarly names its stable fallback, shell, Apache, and Markdown
table literals once. Each use retains the same string value; no generated file
is hand-edited and no runtime command, executable, candidate order, or
security decision changes.

This is deliberately limited to the 13 reviewed keys. Other Sonar findings,
including Vulnerability-type observations and language-standard-incompatible
Common C++ suggestions, remain separate work.

## Security impact

The changed strings are repository-controlled metadata and labels. The change
does not alter untrusted-input handling, command construction, path
normalization, executable resolution, authorization, logging, evidence gates,
scanner configuration, Quality Gates, suppressions, or NOSONAR markers. The
system-environment-proof generator still uses the same /bin/sh value and the
same existing executable checks. No security finding is claimed fixed by this
maintainability-only batch.

## Changed files

- scripts/generate_connector_guides.py
- ci/evidence/reports/generate-system-environment-proof.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Tests and actual results

| Command or check | Result |
| --- | --- |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m py_compile scripts/generate_connector_guides.py ci/evidence/reports/generate-system-environment-proof.py | passed. |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_compiler_guides | passed: 19 tests. |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> ci/evidence/reports/generate-system-environment-proof.py --connector-root . --framework-root modules/ModSecurity-test-Framework --output-dir <task-owned path> --skip-check-runs | passed: generated a temporary system-environment-proof report without running the skipped external checks. |
| Source occurrence review | passed: each selected literal remains once as a module constant; unrelated longer note strings remain unchanged. |
| Focused security extraction invariant | passed: the existing shell path, shell-check source/candidate, and missing-tool PATH-fallback behavior retain their exact values. |

Fresh exact-head SonarQube Cloud and GitHub Actions results are pending Draft PR
creation and are not inferred by this record.

## Runtime evidence

No connector runtime behavior changed or was claimed. The generator invocation
is a bounded Parent-only functional check and not connector-host runtime
evidence.

## Checks not run and rationale

- No full connector build or host/runtime matrix: neither connector source nor
  runtime harness behavior changed.
- No Framework or MRTS test or modification: they are excluded from this
  Parent-only task.
- Full hosted checks and SonarQube Cloud PR analysis remain pending until the
  exact Draft PR head exists.

## Known limitations

This batch addresses only 13 selected python:S1192 observations. It does not
claim to clear the broader SonarQube Cloud backlog or to validate unavailable
runtime environments.

## Remaining risks

Any accidental mismatch between a constant and a former literal could affect
generated text or reporting metadata. The focused compiler-guide suite and the
bounded generator invocation reduce that risk; fresh hosted exact-head analysis
remains required before delivery is verified.

## Final review status

Local implementation and focused validation are in progress on a Parent-only
task branch. No commit, push, Draft PR number, review, hosted check, Sonar
Quality Gate, merge, or default-branch change is claimed in this pre-delivery
record.
