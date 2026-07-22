# Change Record: Parent tests and Lighttpd assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260722-sonar-tests-connectors-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260722-sonar-tests-connectors-assert-order |
| Date (UTC) | 2026-07-22 |
| Base revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Tracking | Twenty Parent-only python:S3415 Code Smells: eleven in tests/test_python_interpreter_contract.py and nine in connectors/lighttpd/tests/test_patched_host_contract.py. |
| Boundary | Parent test source plus this English/German traceability pair and indexes. Framework, MRTS, gitlinks, production connector source, scanner configuration, Quality Gates, suppressions, and runtime behavior remain unchanged. |

## Motivation and problem statement

SonarQube Cloud reports `unittest.TestCase.assertEqual` calls whose expected
and actual operands are reversed. The assertions already express the intended
test predicates; swapping only their first two operands aligns failure
diagnostics with the project convention without changing the comparison or its
pass/fail outcome.

The selected open-key groups are `AZ-KYVWifYmbqbBXVNJf` through
`AZ-KYVWifYmbqbBXVNJp` in the interpreter contract and
`AZ-KYU9VfYmbqbBXVNCV` through `AZ-KYU9VfYmbqbBXVNCd` in the Lighttpd
contract.

## Acceptance criteria

- Swap exactly the first two operands of the 20 selected `assertEqual` calls.
- Preserve test predicates, optional failure messages, test inputs, expected
  values, return-code checks, and external-command behavior.
- Pass the two affected test modules and focused legitimate security controls.
- Keep both Change Record languages and both indexes equivalent.
- Obtain fresh SonarQube Cloud and hosted-check evidence for the exact Draft
  PR head before calling any selected key resolved.

## Implementation decision and rationale

The interpreter contract now supplies each process result or parsed payload
value first and the fixed expected value second. The Lighttpd contract does
the same for subprocess return codes, projected status sets, evidence paths,
and phase-4 summary values. Optional assertion messages retain their original
third argument. No predicate, fixture, process invocation, host configuration,
or production source changed.

This is deliberately limited to the reviewed 20 S3415 keys. Other Sonar
findings, including remaining test smells and Vulnerability-type observations,
remain separate work.

## Security impact

The modified tests exercise executable validation and Lighttpd host/evidence
contracts, but the change is diagnostic ordering only. No trusted boundary,
untrusted input, subprocess argument, executable choice, configuration,
network action, authorization decision, evidence rule, or security control
changes. Focused negative controls continue to prove that a foreign expected
executable is not invoked, unproven content encoding is rejected, and only
bounded end-of-stream metadata is projected. No security finding is claimed
fixed by this maintainability-only batch.

## Changed files

- tests/test_python_interpreter_contract.py
- connectors/lighttpd/tests/test_patched_host_contract.py
- reports/audits/change-records/README.md and README.de.md
- this English/German Change Record pair

## Tests and actual results

| Command or check | Result |
| --- | --- |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m py_compile tests/test_python_interpreter_contract.py connectors/lighttpd/tests/test_patched_host_contract.py | passed. |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_python_interpreter_contract connectors.lighttpd.tests.test_patched_host_contract | passed: 23 tests. |
| Focused negative security controls: foreign expected executable is not invoked; unproven content encoding is rejected; result writer projects bounded EOS metadata | passed: 3 tests. |
| Source occurrence review | passed: exactly the 20 selected assertEqual calls use actual-first order and retain their optional message arguments. |
| git diff --check | passed. |

Draft PR [#89](https://github.com/Easton97-Jens/ModSecurity-conector/pull/89)
now exists for branch `agent/sonar-s3415-tests-connectors-assertions-20260722`.
At creation time, its head, the local commit, and the remote branch all matched
`2012eb37565729fb7fc8a1f902953149ee9cadbe`. Fresh exact-head SonarQube Cloud
and GitHub Actions results are pending and are not inferred by this record.

## Runtime evidence

No connector runtime behavior changed or was claimed. The affected Lighttpd
contract module executes bounded test fixtures; it is not a production-host
runtime deployment or a Framework/MRTS run.

## Checks not run and rationale

- No full connector build or host/runtime matrix: this change only swaps test
  diagnostic argument order and the complete affected test modules passed.
- No Framework or MRTS test or modification: they are excluded from this
  Parent-only task.
- Full hosted checks and SonarQube Cloud PR analysis remain pending for the
  current exact Draft PR head.

## Known limitations

This batch addresses only 20 selected python:S3415 observations. It does not
claim to clear the broader SonarQube Cloud backlog or to validate unavailable
runtime environments.

## Remaining risks

An accidental operand swap outside a selected assertion could make failure
diagnostics misleading. The final source occurrence review, 23 affected-module
tests, and focused negative security controls reduce that risk; fresh hosted
exact-head analysis remains required before delivery is verified.

## Final review status

Local implementation and focused validation completed on the Parent-only task
branch. Draft PR #89 is open and marked Draft; its initial exact head was
verified against local and remote Git metadata. Hosted checks, Sonar analysis,
and the Quality Gate remain pending. No review approval, merge, or
default-branch change is claimed or authorized.
