# Change Record: Parent response-header backend assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-response-header-backend-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-response-header-backend-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVUDfYmbqbBXVNGK (line 109), AZ-KYVUDfYmbqbBXVNGL (line 110), AZ-KYVUDfYmbqbBXVNGM (line 111), AZ-KYVUDfYmbqbBXVNGN (line 112), AZ-KYVUDfYmbqbBXVNGO (line 157), and AZ-KYVUDfYmbqbBXVNGR (line 198). |
| Boundary | Parent test source and this English/German Change Record pair plus indexes. Response-header backend behavior, Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, and external Sonar issue state remain unchanged. |

## Motivation and problem statement

The selected SonarQube Cloud rows report six independent `unittest` assertions
that place an expected literal before their observed value. Reversing only the
first two arguments improves the failure diagnostic convention while preserving
the same predicate and expected values.

## Acceptance criteria

- Correct only the six selected independent assertions to actual-value first and expected-value second.
- Preserve the HTTP fixture flow, server lifecycle, response reads, invalid-header rejection, and harness-source assertions.
- Pass the three Parent-only affected test methods before and after the edit, plus a structural AST inventory and `git diff --check`.
- Leave all five Framework-dependent S3415 assertions in the same module unchanged until their required Gitlink setup is explicitly authorized.
- Maintain an equivalent English/German Change Record pair and record indexes.

## Implementation decision and rationale

The six calls now pass the existing observed response status/header/body or
subprocess return code first and their unchanged expected literal second. The
only call with an observable receiver, `response.read()`, now evaluates before
the same literal; the literal has no side effect and the assertion predicate is
unchanged. No expected value, message, retry bound, fixture, subprocess, or
backend behavior changed.

## Changed files

- tests/test_response_header_backend.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

Focused commands use the Parent `.venv` Python, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONNOUSERSITE=1`, and task-owned external `TMPDIR`:

- rtk proxy env ... `<Parent .venv python>` -m unittest -v `<three selected ResponseHeaderBackendTest methods>` (before the edit)
- rtk proxy env ... `<Parent .venv python>` -m unittest -v `<the same three selected methods>` (after the edit)
- rtk proxy env ... `<Parent .venv python>` -c `<structural AST inventory of the six selected assertions>`
- rtk proxy git diff --check

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Three selected Parent-only methods before the edit | passed: 3 tests in 0.347s. |
| The same three methods after the edit | passed: 3 tests in 0.347s. |
| Structural AST inventory | passed: exactly lines 109-112, 157, and 198 have the selected actual-first expressions and unchanged typed expected values. |
| Initial ad-hoc AST presentation checks | failed only because `ast.unparse` normalizes literal quote styles and the first expected-value map used strings instead of typed literals; no product source or test failure occurred. The final structural AST inventory passed. |
| `git diff --check` | passed after the full B03 traceability pair and indexes were added. |
| Bilingual Change Record validation | passed: `tests.test_bilingual_docs`, 13 tests in 0.035s. |
| `make check-bilingual-docs` | blocked_environment: exactly 20 existing missing targets under the intentionally uninitialized Framework Gitlink; no B03 record error. |
| `make check-doc-links` | blocked_environment: exactly 16 existing missing targets under the intentionally uninitialized Framework Gitlink; no B03 record error. |

## Security impact

The focused security assessment is `not_applicable`: this is test-diagnostic
argument ordering only. The test retains its existing loopback backend,
fixture input, header-injection rejection, subprocess cleanup, and static
harness checks. No backend or production security control changed and no
security finding is claimed fixed.

## Documentation status

This source-only test correction changes no generated or reader-facing guide.
The English/German Change Record pair and indexes provide the required
traceability.

## Runtime evidence

The selected tests exercise an existing loopback test backend. They are focused
test evidence only, not connector-host or production runtime evidence.

## Known limitations

This batch addresses only six selected Parent S3415 keys. Five other S3415
keys in the same test module remain unchanged because their test methods depend
on the intentionally uninitialized Framework Gitlink. The selected keys remain
OPEN in the current inventory until a new analysis evaluates a delivered head.

## Remaining risks

An accidental expected-value or call-order change could weaken diagnostics or
change response-body consumption. The narrow six-call diff, actual-before-
expected AST inventory, and before/after Parent-only tests reduce that risk.
No conclusion about the remaining S3415 rows follows from this batch.

## Checks not run and rationale

- The complete `tests.test_response_header_backend` module is not run because it contains Framework-dependent methods and the clean task worktree deliberately has no initialized Framework Gitlink. The three changed methods are independently Parent-only and were run before and after.
- Connector builds, host runtime smokes, Framework checks, and MRTS checks are not applicable because no connector/runtime implementation or cross-repository content changed.
- `tests.test_bilingual_docs` passed. The two full documentation Make checks were run and are `blocked_environment` only on the 20 and 16 existing missing Framework-Gitlink targets, respectively. Hosted SonarQube Cloud analysis, GitHub CI, commit, push, pull request, and merge are not run; no master integration is authorized.

## Final diff and review status

The local task-worktree candidate is uncommitted and contains this six-call
assertion-order correction with its required traceability material. No source
changed in the authoritative Parent checkout. No Framework or MRTS action,
Gitlink update, scanner-control change, external issue disposition, push, pull
request, or master merge has occurred. Later validation and delivery evidence
will be recorded only from observed results.
