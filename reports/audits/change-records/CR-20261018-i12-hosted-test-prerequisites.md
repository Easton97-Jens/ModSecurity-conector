# Change Record: CR-20261018-i12-hosted-test-prerequisites

**Language:** English | [Deutsch](CR-20261018-i12-hosted-test-prerequisites.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-hosted-test-prerequisites |
| Date (UTC) | 2026-10-18 |
| Base revision | `57ba18ce45f56b0febc5396f3753407e9d23e213` |


## Motivation and problem statement

The a29019558678222b88913be0e202db3c9d14323a hosted scaffold job failed before exercising intended checks: Sonar unit tests import yaml before PyYAML is installed, and committed-source capture fixtures invoke an undeclared rtk executable on the hosted runner. Supply the existing dependency before its consumers and keep test-internal Git probes independent of that workstation tool.

## Acceptance criteria

Use the existing requirements-ci.lock without changing versions or hashes. Install binary wheels with hash enforcement before Sonar unit tests. Retain every gate/security assertion. Run the complete capture tests with PATH excluding RTK and retain before/after receipts. Preserve the initially malformed YAML failure as history.

## Implementation decision and rationale

The scaffold workflow installs the existing PyYAML 6.0.3 CPython 3.14 wheel with --only-binary=:all: and --require-hashes immediately after the Python interpreter contract check. A regression requires exactly one unconditional locked install before the Sonar test consumer. Four test-internal read-only Git commands (revision, tree, archive and listing) invoke Git directly, already provided by checkout; local outer execution remains RTK-wrapped. No gate implementation or dependency pin changes.

## Changed files

Root owns .github/workflows/lint.yml, tests/test_sonar_zero_gate.py and ci/runtime/lifecycle/i12/test_capture_sources.py. This documentation task changes only this EN/DE pair. A separate read-only review also examined 37bb49612fbecbd3cdf18fba986757d39f6d7915: the HAProxy binding fixture gains the real request http_version field and initializer, and the host-result fixture supplies its transport-abort collaborator using the existing shutdown counter. The separately documented fixture changes do not replace real transport coverage.

## Commands executed

Read actual diffs and external receipts through RTK. Created this pair with the native new-change-record.py create command and the declared base revision; its check command passed. Fresh tests.test_bilingual_docs plus tests.test_change_record passed 42 tests in 0.430 seconds; git diff --check passed. root-scaffold-dependency-order-before-20261018 records one expected regression failure before the install step. root-capture-hosted-path-before-20261018 records FileNotFoundError for rtk during setup and zero tests. root-capture-hosted-path-after-20261018 runs the complete capture suite through outer RTK with PATH=/usr/bin:/bin: 57 tests PASS in 38.670 seconds. root-scaffold-gates-security-retake-20261018 runs Sonar-zero, duplication and workflow-security modules: 73 tests PASS in 2.606 seconds. Exact argv, exit codes and log hashes are retained in the associated JSON receipts under the external task run checks directory.

## Security impact

The existing locked dependency digest and binary-only/hash-required installation are preserved. No package was installed by this documentation/review task. Read-only test Git probes remove an undeclared hosted dependency without altering local RTK requirements. No gate, validation, authentication, branch protection, CI assertion or Sonar state is weakened or changed.

## Runtime evidence

The restricted-PATH retake proves that all 57 capture tests run without an installed RTK on the child process PATH. The 73-test retake proves the current workflow parses and preserves gate/security controls. These are local test and workflow-contract results, not evidence that a fresh hosted run passed or that any connector host lifecycle passed.

## Known limitations

The first root-scaffold-gates-security-after-20261018 attempt failed because an unquoted YAML scalar containing --only-binary=:all: was malformed: 73 tests, one failure and two errors. That receipt remains intact. The final workflow uses a block scalar; only the separately named retake is PASS. The local dependency-order check does not execute pip or prove package download availability.

## Remaining risks

A fresh hosted run on the integrated head must verify dependency installation, the complete scaffold job and exact-head Sonar evidence. Requirements lock bytes are unchanged; no claim about network availability or hosted success follows from local tests.

## Checks not run and rationale

This task does not install packages, rerun heavy hosts, mutate Git or Sonar, or edit CI source. Root owns implementation tests and integration; this task independently reads their raw receipts and performs the documentation contract/whitespace checks. Go/race/vet and native host evidence belong to the enclosing acceptance work.

## Final diff and review status

Read-only review found no actionable defect in the three current CI changes or the two HAProxy fixture changes at 37bb4961. The new ordering regression fails before and passes in the retained retake. This EN/DE pair records actual failure history and separates local results from outstanding hosted verification.
