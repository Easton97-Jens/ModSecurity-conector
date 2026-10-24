# Change Record: CR-20261008-harness-explicit-content-type-omission

**Language:** English | [Deutsch](CR-20261008-harness-explicit-content-type-omission.de.md)

Explicit opt-in fixture metadata only.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-harness-explicit-content-type-omission |
| Date (UTC) | 2026-10-08 |
| Base revision | `5788ba5ced597106911785a5407b2024c68bbaf2` |

## Motivation and problem statement

Preserve the explicitly requested missing Content-Type fixture through harness metadata instead of silently losing its omission instruction.

## Acceptance criteria

Forward only validated opt-in omit_headers. Preserve default fixture shape; reject framing-header omissions and conflicting configured Content-Type, including empty values.

## Implementation decision and rationale

Reuse the existing closed response_fixture_omission validator before exposing omit_headers to the backend. Omission remains [] or exactly ['Content-Type']; no broad header suppression.

## Changed files

ci/runtime/common/harness-case-metadata.py; tests/test_harness_omission_metadata.py; this EN/DE pair.

## Commands executed

RTK-wrapped Parent .venv unittest tests.test_case_metadata_utils tests.test_harness_omission_metadata tests.test_response_fixture_omission tests.test_response_header_backend tests.test_change_record passes 40 tests (stream-c-parent-metadata.log). Three focused omission controls also pass with the three raw-driver controls. In-memory syntax of both Python files, ci/tools/new-change-record.py check, make check-bilingual-docs and make check-doc-links (explicit current Framework checkout) pass.

## Security impact

No framing or security header omission is authorized. Invalid or conflicting omission metadata fails before backend use; default behavior is unchanged.

## Runtime evidence

Controlled unit fixtures only; no fresh NGINX or other native host runtime.

## Known limitations

This change forwards fixture metadata; it does not establish actual wire omission or Engine MIME decisions.

## Remaining risks

Fresh host-bound response-header and canonical observations remain coordinator-owned.

## Checks not run and rationale

No build, native runtime, E2E, remote CI, Sonar or push under this task.

## Final diff and review status

Reviewed the narrow opt-in seam and positive/default/negative controls. Separate four-file commit including both generated records; concurrent Root work preserved.
