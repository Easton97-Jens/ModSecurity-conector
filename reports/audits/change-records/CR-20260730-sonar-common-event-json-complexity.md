# Change Record: Parent Common event JSON optional-field decomposition

**Language:** English | [Deutsch](CR-20260730-sonar-common-event-json-complexity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-common-event-json-complexity` |
| Date (UTC) | 2026-07-30 |
| Base revision | `fe4840a0a72449bbdb8f7b2f77f09922c9e66a9f` |
| Tracking | `FND-SONAR-0020`; SonarQube Cloud `AZ9cRy9OHhV2CayPTP4Y` / `c:S3776` at `common/src/event.c:502`. |
| Boundary | Parent Common event serializer and its paired Change Record/index documents only. |

## Motivation and problem statement

`msconnector_event_write_json_ex` remains one point over the configured
Cognitive Complexity threshold. Its two optional JSON-field formatting branches
have identical bounded-output and truncation semantics.

## Acceptance criteria

- Optional `body_limit_outcome` and `late_intervention_mode` JSON fragments
  retain empty, valid, and truncation behavior.
- QUIC-ID redaction, bounded transport metadata validation, serializer return
  values, and existing JSON field names remain unchanged.
- The current C17 Common helper smoke passes with GCC and Clang.

## Implementation decision and rationale

One bounded helper now owns the common empty-field, `snprintf`, overflow, and
truncation path. The caller retains both fixed field names and its existing
ordering, reducing independent branches without altering the serializer
contract.

## Changed files

- `common/src/event.c`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| `CC=gcc make check-common-helpers-c17` with task-owned external build/runtime roots | passed with `-std=c17 -Wall -Wextra -Werror`. |
| `CC=clang make check-common-helpers-c17` with separate external roots | passed with the same C17 contract. |
| `git diff --check` | passed before record creation; rerun before delivery. |

## Security impact

The serializer continues to escape text before formatting, retain bounded
transport-token handling, and redact raw QUIC connection identifiers. No
policy, input validation, logging content, or SonarQube Cloud control changes.

## Runtime evidence

The Common helper smoke exercises normal JSON output, truncation, and event
JSONL serialization using the real C implementation.

## Known limitations

This is focused Common serializer evidence, not a connector-host, CRS, MRTS,
HTTP/2, or HTTP/3 runtime matrix.

## Checks not run and rationale

No full connector matrix or repository security scan was run because this
maintainability extraction retains existing serializer security controls.
Hosted Actions, SonarQube Cloud, and review evidence remain pending until the
Draft PR is delivered.

## Remaining risks

The original issue is only resolved after current-head SonarQube Cloud analysis
confirms `AZ9cRy9OHhV2CayPTP4Y` is absent; no suppression is used.

## Final diff and review status

The candidate is source-local with paired traceability. Delivery and exact-head
verification are pending; no merge or `master` change is claimed.
