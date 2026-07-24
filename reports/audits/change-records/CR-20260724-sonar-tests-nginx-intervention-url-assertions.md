# Change Record: Parent NGINX intervention URL ownership assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260724-sonar-tests-nginx-intervention-url-assertions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260724-sonar-tests-nginx-intervention-url-assertions |
| Date (UTC) | 2026-07-24 |
| Base revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells AZ-KYVTafYmbqbBXVNF7 (line 35) and AZ-KYVTafYmbqbBXVNF8 (line 42). |
| Boundary | Parent test source plus this English/German traceability pair and indexes. NGINX C source, connector behavior, Framework, MRTS, gitlinks, scanner configuration, Quality Gates, suppressions, and generated artifacts remain unchanged. |

## Motivation and problem statement

The selected SonarQube Cloud rows report that two existing `unittest`
assertions in the Parent NGINX intervention URL ownership test place their
expected value before the observed cleanup-count or return-list result. The
existing test already enforces NGINX lifetime and cleanup invariants; reversing
only each first two operands improves failure diagnostics without changing the
predicate or accepted behavior.

## Acceptance criteria

- Correct only the two selected SonarQube Cloud assertions to actual-value
  first and expected-value second.
- Preserve every NGINX C-source literal, failure-branch control, cleanup
  count, return-list expectation, fixture, and production source file.
- Pass the complete focused Parent unit module, selected-file syntax check,
  two-call AST inventory, and diff hygiene check.
- Maintain synchronized English/German Change Records and indexes.
- Obtain exact-head GitHub and SonarQube Cloud Draft-PR evidence before
  describing the selected keys as verified.

## Implementation decision and rationale

Each selected `assertEqual` now passes its existing observed expression first
and unchanged expected literal or list second. No test helper, C source,
expected value, assertion message, NGINX lifecycle/cleanup condition, or
runtime behavior changed. This is the smallest repository-native correction
for `python:S3415` and preserves `unittest` predicate semantics.

## Security impact

The focused security assessment is `not_applicable`: this is diagnostic
argument ordering in Parent test code only. The test reads a security-relevant
NGINX intervention ownership/cleanup source path, but that C source and every
asserted lifetime invariant remain unchanged. The direct module imports only
Parent/Python-stdlib code and does not invoke Framework, MRTS, a connector
runtime, a network client, or a subprocess. No security finding is claimed
fixed.

## Changed files

- tests/test_nginx_intervention_url_ownership.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Commands executed

Focused commands use the Parent `.venv` Python, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONNOUSERSITE=1`, task-owned external `TMPDIR`, and external
`PYTHONPYCACHEPREFIX`:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_nginx_intervention_url_ownership
- rtk proxy -- env ... <Parent .venv python> -m py_compile tests/test_nginx_intervention_url_ownership.py
- rtk proxy -- env ... <Parent .venv python> -c <AST inventory of the two selected assertions>
- rtk proxy -- git diff --check

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused NGINX intervention URL ownership module before and after the edit | passed: tests.test_nginx_intervention_url_ownership, 3 tests in each run. |
| Selected-file Python syntax | passed: tests/test_nginx_intervention_url_ownership.py compiled with pycache outside the checkout. |
| Selected-assertion AST inventory | passed: exactly the two selected anchors (35 and 42) have actual-first operands and unchanged expected values. |
| git diff --check | passed: no whitespace error. |
| Current-batch worktree bytecode scan | passed: no `*.pyc` file. |
| tests.test_bilingual_docs and direct Change Record/index parity | passed: 11 tests; both Change Records have 13 level-two sections and matching ID, base revision, keys, and affected path literal. |
| make check-bilingual-docs | blocked_environment: exactly 20 existing missing Framework-gitlink link targets; no new Change Record error. |
| make check-doc-links | blocked_environment: exactly 16 existing missing Framework-gitlink link targets; no Framework source, gitlink, or generated artifact changed. |
| Hosted-delivery checks | not run after initial commit `bfb73bb`; required on the final Draft-PR head and not claimed in advance. |

## Runtime evidence

No NGINX runtime behavior changed or is claimed. The focused unit test reads
the existing C source and checks source-level cleanup/lifetime contract
literals; it is neither host-traffic nor production-runtime evidence.

## Checks not run and rationale

- Connector builds, configuration checks, host runtime smoke tests, protocol
  matrices, Framework checks, and MRTS checks are not applicable because no
  connector/runtime implementation changed and Framework/MRTS are excluded.
- Ruff and Pyright are not applicable: no Parent configuration is present and
  neither executable exists in the selected Parent `.venv`; no installation or
  configuration change is made for this diagnostic-order correction.
- Draft-PR checks, SonarQube Cloud Quality Gate, PR issue query, and review
  state remain unavailable after the initial commit and are required before
  `verified_pr`.

## Known limitations

This batch corrects only two selected Parent SonarQube Cloud findings. It does
not claim to remediate the wider 1,474-item SonarQube Cloud backlog.

## Remaining risks

An unintended assertion-value change could weaken the NGINX intervention
ownership/lifetime control. The narrow diff, exact two-call AST inventory,
complete focused module, and pending exact-head hosted validation reduce that
risk. No runtime or security behavior is inferred from this test-diagnostic
change.

## Final diff and review status

The source correction and initial English/German traceability material are in
atomic commit `bfb73bb` on task branch
`codex/sonar-tests-nginx-intervention-url-assertions-20260724-master-5b8db00`,
whose parent is `5b8db00d44ab24f3a9f4216a00f7edee977b6898`. The branch has
not yet been pushed or associated with a pull request at this document
revision. No merge, default-branch update, Framework action, MRTS action,
scanner-control change, or suppression occurred. Final delivery facts are
added only after they are observed.
