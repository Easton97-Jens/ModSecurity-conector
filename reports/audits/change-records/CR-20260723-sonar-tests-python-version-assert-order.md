# Change Record: Parent Python-version assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260723-sonar-tests-python-version-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-tests-python-version-assert-order |
| Date (UTC) | 2026-07-23 |
| Integration base revision | `6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d`; original source base `a308d7b414f0859490fe7253e0683a4bde80b563`. |
| Tracking | FND-SONAR-0019; 34 Parent-only SonarQube Cloud `python:S3415` Code Smells, keys `AZ-KYVOzfYmbqbBXVNDC` through `AZ-KYVOzfYmbqbBXVNDj`, in `tests/test_python_version_contract.py`. |
| Boundary | One Parent test module plus this English/German Change Record pair and indexes. Framework, MRTS, gitlinks, product source, dependency manifests, scanner configuration, Quality Gates, suppressions, and the default branch remain unchanged. |

## Motivation and problem statement

The live SonarQube Cloud project inventory still reports 1,474 open items.
Thirty-four current Parent `python:S3415` observations identify
`unittest.TestCase.assertEqual` calls in the Python-version contract suite
whose expected and actual operands were presented in the opposite order from
the project convention.

The existing predicates and test inputs are correct.  This batch changes only
the order used for failure diagnostics: the observed value is first and the
fixed expected value is second.  It is deliberately independent of all other
Sonar remediation branches.

## Acceptance criteria

- Change exactly the first two operands of the 34 selected `assertEqual`
  calls identified by the current Sonar key/path/line inventory.
- Preserve each equality predicate, optional third `msg` argument, fixture,
  helper invocation, return-code check, and workflow-contract behavior.
- Leave non-selected `assertEqual` calls at lines 167, 323, and 334 unchanged.
- Pass the complete affected Parent test module, selected in-memory syntax
  check, source-to-key occurrence review, bilingual documentation checks, and
  `git diff --check`.
- Obtain fresh exact-head hosted-check and SonarQube Cloud evidence after
  every branch update and before protected delivery; retain only observed
  results in the PR and task delivery record.

## Implementation decision and rationale

The selected calls now supply a parsed value, collection, return code, or
other observed result first, followed by the literal or constructed expected
value.  The optional diagnostic message remains the unchanged third argument
where present.

`assertEqual` compares the same operands either way.  Each selected operand
pair is a literal, local value, or deterministic contract-helper result, so
the reordering changes failure presentation rather than the tested predicate
or external behavior.  No implementation, fixture, workflow, or dependency
change accompanies the diagnostic cleanup.

## Changed files

- `tests/test_python_version_contract.py`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Security impact

This is a maintainability-only test diagnostic change.  It does not modify a
runtime parser, path rule, permission, command invocation, dependency,
workflow execution, request boundary, or security control.  No security
finding is claimed fixed, no suppression is added, and no Quality Gate or
scanner setting changes.

## Commands executed

- The selected local Parent interpreter was verified as
  `/root/git/ModSecurity-conector/.venv/bin/python`, Python `3.14.4`, with a
  virtual-environment prefix distinct from `/usr`. The module continues to
  validate the canonical `.python-version` contract for `3.14.6`; hosted
  validation is separately bound to the exact PR head.
- Baseline and post-change focused
  `tests.test_python_version_contract` runs both passed all 24 tests.
- In-memory syntax compilation of the changed test module passed.
- The source-to-key review mapped all 34 selected current S3415 lines to
  actual-first/expected-second operands after the change.
- `tests.test_bilingual_docs` passed all 11 tests and `git diff --check`
  passed.  The two full repository documentation commands were executed but
  are blocked only by pre-existing missing links below the intentionally
  uninitialized Framework gitlink; neither reports an error for this record
  pair.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| `rtk proxy -- env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/tmp /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_python_version_contract` | passed: 24 tests before and after the assertion-order change. |
| In-memory `compile()` of `tests/test_python_version_contract.py` with the selected Parent interpreter | passed. |
| AST/source comparison against the retained `python:S3415` ledger | passed: 34/34 selected lines map to actual-first/expected-second operands; the three non-selected calls remain outside the patch. |
| `tests.test_bilingual_docs` | passed: 11 tests. |
| `make check-bilingual-docs` | blocked only by pre-existing missing links below the intentionally uninitialized Framework gitlink; no error names this record pair. |
| `make check-doc-links` | blocked only by the same pre-existing missing Framework-gitlink targets. |
| Final `git diff --check` | passed. |

## Runtime evidence

No connector or product runtime behavior changed or is claimed.  The affected
module uses bounded temporary test fixtures and checks a Parent CI workflow
contract; it is neither a host-runtime deployment nor a Framework/MRTS run.

## Validation status

The focused behavior-preserving test, syntax, targeted bilingual, and final
diff evidence is complete for the test-source change. The two full repository
documentation commands are truthfully `blocked` only by existing
Framework-gitlink targets outside the selected Parent batch. Exact-head GitHub
and SonarQube Cloud results are required after every branch update before
protected delivery; the observed per-head result is retained in the PR and
task delivery record rather than inferred or copied forward from an older
head.

## Known limitations and follow-up

This batch resolves only the selected 34 `python:S3415` test diagnostics.  It
does not claim to resolve the remaining Parent SonarQube Cloud backlog or to
validate unavailable connector, CRS, Framework, or MRTS environments.

## Remaining risks

An unintended operand change outside the selected inventory could make a
future test failure less clear.  The exact 34-key/line mapping, the
unchanged-call review, and the complete focused test module reduce that risk.
Fresh hosted and Sonar exact-head evidence remains required before delivery is
verified.

## Checks not run and rationale

- No connector build, host configuration, runtime smoke, CRS, protocol, or
  matrix check: this test-only diagnostic change does not alter those
  boundaries, and the complete affected unit module is the narrowest valid
  regression layer.
- No Framework or MRTS test or modification: both repositories are explicitly
  outside this Parent-only batch.
- No full repository-wide unittest run: the selected module fully owns the
  changed assertions; broader targets add excluded Framework prerequisites and
  do not exercise a different changed behavior.
- Hosted checks and SonarQube Cloud PR analysis: evaluated only for the exact
  current PR head before protected delivery; no older-head outcome is reused.

## Delivery status

The candidate is Parent PR #101 on the isolated branch
`codex/sonar-tests-python-version-20260723-master-a308d7b`, reconciled to
integration base `6c1f5719f9b23f4df8d0fb65e07b3d38d1e3815d` from the original
source base `a308d7b414f0859490fe7253e0683a4bde80b563`. It may be delivered
only through the repository-protected squash merge after a fresh exact-head
review under the current task authorization. No direct default-branch update,
Framework/MRTS change, rebase, force-push, or control bypass is used.

## Final diff and review status

The current-base candidate remains limited to the exact S3415 assertion-order
cleanup, this bilingual Change Record pair, and its two indexes. Final local
review is complete: focused tests, syntax, source-to-key review, targeted
bilingual tests, and `git diff --check` passed; the two broader documentation
commands are blocked only by the documented Framework-gitlink condition.
Exact-head hosted checks, SonarQube Cloud Quality Gate, PR state, and merge
evidence are evaluated at delivery and retained only as observed facts in the
PR and task delivery record.
