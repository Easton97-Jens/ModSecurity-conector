# Change Record: Parent response-header backend diagnostic assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-response-header-backend-s3415.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-response-header-backend-s3415 |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Current Parent SonarQube Cloud `python:S3415` issues: AZ-KYVUDfYmbqbBXVNGH (line 62), AZ-KYVUDfYmbqbBXVNGI (line 64), AZ-KYVUDfYmbqbBXVNGJ (line 65), AZ-KYVUDfYmbqbBXVNGP (line 187), and AZ-KYVUDfYmbqbBXVNGQ (line 188). |
| Boundary | Parent test diagnostics and this English/German Change Record pair plus indexes. Response-header backend behavior, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, and hosted SonarQube Cloud issue state remain unchanged. |
| Delivery status | At the time this record was authored, the locally validated candidate was staged for the authorized normal commit/Draft-PR cycle. No commit, push, pull request, hosted SonarQube Cloud analysis, or merge is claimed by this record; later exact-head evidence is required for any delivery claim. |

## Motivation and problem statement

The five selected `unittest` assertions placed an expected value before their
observed value. Reversing only the first two `assertEqual` arguments makes a
failure report identify the actual value first while retaining the same
predicate, values, messages, and test behavior. This is a diagnostic-only
change, not a behavior change or security fix.

## Acceptance criteria

- The five tracked calls at lines 62, 64, 65, 187, and 188 use
  `assertEqual(actual, expected)` with their original values and messages.
- The response-header fixture flow and all test behavior remain unchanged.
- The existing CRLF invalid-response-header rejection test remains unchanged.
- The complete focused `tests.test_response_header_backend` module has the
  supplied passing result of 5 tests in 1.275s after read-only initialization
  of the Parent-pinned Framework at `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`.
- This complete English/German Change Record pair is indexed and documentation
  checks report their observed results.

## Implementation decision and rationale

The existing candidate source diff changes only the order of the first two
arguments in five `assertEqual` calls: `result.returncode`, fixture status and
headers, Apache phase-4 metadata return code, and metadata stdout are now the
actual values; the same literals remain their expected values. Existing third
arguments, including `result.stderr`, remain unchanged.

`test_invalid_fixture_headers_are_rejected_before_listening`, including its
CRLF header-value rejection, is outside this five-call diff and remains
unchanged. The focused module was run only after the Parent-pinned Framework
had been initialized read-only at
`47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; supplied validation reports that
the Framework stayed clean and detached. No Framework or MRTS source, or
Parent/Framework Gitlink, changed.

## Security impact

The response-header test module is adjacent to an existing header-validation
control, but these five edits only improve assertion diagnostics. The existing
CRLF rejection test remains intact, and no production backend, validation, or
other security control changes. This is diagnostic-only and is not a security
fix; no security finding is created, closed, or claimed fixed.

## Changed files

- `tests/test_response_header_backend.py` — pre-existing candidate source
  change: five S3415 diagnostic argument-order updates.
- `reports/audits/change-records/CR-20260727-sonar-response-header-backend-s3415.md`
  and `CR-20260727-sonar-response-header-backend-s3415.de.md`.
- `reports/audits/change-records/README.md` and `README.de.md`.

No generated artifacts, Framework files, MRTS files, or Gitlinks changed.

## Commands executed

- `rtk make check-bilingual-docs` (initial validation and post-correction
  validation)
- `rtk make check-doc-links`
- `rtk git diff --check`
- `/root/git/ModSecurity-conector/.venv/bin/python tests/test_response_header_backend.py`
  with `PYTHONDONTWRITEBYTECODE=1` (delivery preflight)

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused Parent module `tests.test_response_header_backend` | initial candidate run passed: 5 tests in 1.275s after the Parent-pinned Framework was initialized read-only at `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`; independent delivery preflight rerun passed: 5 tests in 1.342s. |
| Initial `rtk make check-bilingual-docs` | failed only because the new records did not yet use the repository-required Change Record headings. No source or link defect was reported. The headings were corrected before the repeat check. |
| Repeated `rtk make check-bilingual-docs` | passed: `bilingual docs ok`. |
| `rtk make check-doc-links` | passed: `repository path references: PASS` and `doc links ok`. |
| `rtk git diff --check` | passed with no output. |

## Runtime evidence

The passing five-test module is focused Parent test evidence. It does not
claim production connector-host runtime coverage, a complete connector matrix,
or hosted SonarQube Cloud analysis.

## Checks not run and rationale

- The source module was not rerun by this documentation-only task; its focused
  5-test result is supplied candidate evidence above.
- Connector builds, connector-runtime smokes, a complete matrix, Framework
  tests, and MRTS tests are not run because no connector, runtime, Framework,
  or MRTS behavior changed.
- Hosted SonarQube Cloud analysis, GitHub CI, commit, push, pull request, and
  merge are not run or authorized. The issue keys are not claimed
  closed without a later delivered-head analysis.

## Known limitations

The focused five-test result proves only the exercised module scope. It does
not establish a hosted SonarQube Cloud issue disposition, broader connector
coverage, or delivery verification. At record-authoring time, the candidate
was staged but uncommitted.

## Remaining risks

A future unrelated edit could accidentally change an expected value, message,
or assertion evaluation order. The narrow five-call source diff, preservation
of values and messages, unchanged CRLF rejection test, and focused module
result reduce that diagnostic risk. No product-security remediation conclusion
follows from this change.

## Final diff and review status

The initial record-heading validation failure was corrected without changing
the documented technical facts. The repeated bilingual check, link check, and
`git diff --check` passed. At record-authoring time, the local candidate was
staged but uncommitted; no commit, push, pull request, hosted SonarQube Cloud
analysis, or merge occurred or is asserted.
