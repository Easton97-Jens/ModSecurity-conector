# Change Record: Parent Common event-provenance serialization decomposition for SonarQube Cloud c:S3776

**Language:** English | [Deutsch](CR-20260729-sonar-common-event-provenance-complexity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-event-provenance-complexity |
| Date (UTC) | 2026-07-29 |
| Base revision | 9f23ae2c5fe908cef38f203be03f93fda75a8dd7 |
| Tracking | SonarQube Cloud rule `c:S3776` at `common/src/event.c:382`: reduce Cognitive Complexity from 32 to the allowed 25. No hosted issue key, Quality Gate, workflow, review, pull request, or exact-head result is claimed. |
| Boundary | Parent `common` event-JSON provenance serialization, focused Common-helper smoke assertions, and this English/German Change Record pair with its indexes. Framework, MRTS, Gitlinks, workflows, scanner policy, generated artifacts, and `master` are not modified. |

## Motivation and problem statement

`msconnector_event_write_json_ex` serializes escaped metadata and bounded protocol provenance into an audit JSON event. SonarQube Cloud reports its Cognitive Complexity as 32, above the permitted 25. The former source used one long short-circuiting chain both to detect protocol data and append all protocol strings and boolean fields.

This maintainability change is at a security-relevant audit boundary. It must improve reviewability without allowing raw transport identifiers, unbounded values, partial provenance, or altered truncation behavior to reach the JSON sink.

## Acceptance criteria

- Decompose the `c:S3776` concern into bounded helpers without changing event JSON field names or order.
- Run escaping, transport-case validation, transport-value filtering, and QUIC-CID redaction before any table-driven provenance append.
- Omit empty values; preserve ordered allowed values and flags; preserve the fail-closed result on an append-capacity failure.
- Pass GCC and Clang C17 Common-helper controls with `-Wall -Wextra -Werror`. The C23 advisory control must not replace C17 evidence.
- Exercise populated protocol values and existing raw-CID, invalid-token, and truncation negative controls.
- Keep an equivalent English/German Change Record pair. Hosted PR evidence is recorded only after it exists.

## Implementation decision and rationale

Fixed C17 arrays now declare the established protocol-string and boolean-field names. `append_event_provenance` retains `run_id` and `transport_case_id`, then delegates the remaining ordered protocol fields to `append_protocol_metadata`. The presence check and append loop use the same already escaped and validated local values that the former chain used.

The arrays keep ordering visible in one place without adding a wide-parameter helper or a large mutable state structure. No C23 language or library feature is introduced. The smoke now asserts every populated protocol string emitted by this path, in addition to existing boolean, raw-CID, invalid-token, and truncation checks.

## Security impact

Controlled inputs are request-adjacent protocol metadata and transport diagnostics. The asset is audit-event integrity, the sink is the JSON provenance fragment, and the trust boundary is crossed only after the existing `escape_field`, transport-token validation, and QUIC-CID non-reversibility checks populate the local arrays.

The refactor passes those filtered local values to the append helper; it does not pass source fields directly. Existing negative controls confirm raw QUIC-CIDs and invalid transport data are absent, while the legitimate control confirms allowed fields remain present. The error path remains fail-closed: any protocol append failure sets `was_truncated` and clears `provenance_json`. No authorization, validation, redaction, integrity, logging, scanner, or quality-gate control is weakened.

## Changed files

- `common/src/event.c`
- `ci/checks/common/check-common-helpers.sh`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260729-sonar-common-event-provenance-complexity.md`
- `reports/audits/change-records/CR-20260729-sonar-common-event-provenance-complexity.de.md`

## Commands executed

| Command | Actual result |
| --- | --- |
| `make check-common-helpers CC=gcc MSCONNECTOR_C_STD=c17 MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"` | passed; the Common-helper smoke compiled and executed with GCC in C17 mode. |
| `make check-common-helpers CC=clang MSCONNECTOR_C_STD=c17 MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"` | passed; the Common-helper smoke compiled and executed with Clang in C17 mode. |
| `make check-common-helpers-c23` | passed as an advisory newer-C check; it does not replace C17 evidence. |
| `make check-common-security-contract check-common-sdk-contract check-common-flow-integrity` | passed. |
| `git diff --check` | passed before this record was added; it is rerun for the final candidate diff before delivery. |

## Tests and actual results

| Control | Result |
| --- | --- |
| Populated-protocol Common-helper control | passed: asserted `run_id`, `transport_case_id`, all populated protocol strings, all flags, reset data, and lifecycle diagnostics. |
| Raw QUIC-CID negative control | passed: `raw-quic-cid` remains absent after serializing a protocol-bearing event. |
| Invalid transport metadata controls | passed: invalid metadata is absent, the result is marked truncated, and affected provenance fields are not emitted. |
| Output-capacity control | passed: a too-small buffer produces a NUL-bounded result and reports truncation. |
| Focused security review | passed: values reach the tables only after escape, validation, and CID-redaction branches; ordered append and fail-closed cleanup were reviewed against the former chain. No reportable regression was identified. |

## Runtime evidence

No connector, host, Framework, or MRTS runtime was started. The Common-helper smoke is focused source/build evidence only; it does not establish deployment or host-runtime compatibility.

## Checks not run and rationale

- A real connector runtime and full connector matrix were not run: the change is limited to Common event serialization and repository-native Common helper, security, SDK, and flow controls exercise that boundary.
- Framework and MRTS checks were not run because they are outside the selected Parent `common` boundary and neither repository was modified.
- A full repository security scan was not run: the focused security review and Common security-contract control cover the changed serialization path; this record does not claim repository-wide coverage.
- Hosted GitHub Actions, SonarQube Cloud PR analysis, review state, and exact-head evidence were not run because no Draft PR exists yet. They remain mandatory before this candidate is presented as a verified PR.

## Known limitations

The local helper smoke validates representative metadata, redaction, and truncation behavior but is not a connector-host integration test. This record has no PR number, commit, hosted Quality Gate, workflow, or review evidence.

## Remaining risks

Future additions must keep name arrays, value arrays, and negative controls aligned; a mismatched index could omit or mislabel provenance. Fixed enum dimensions, ordered table review, populated-field assertions, C17 controls, and fail-closed append behavior reduce that risk. Exact-head hosted analysis remains required to verify the actual Sonar remediation.

## Final diff and review status

The scoped candidate changes only Common event provenance decomposition, its focused smoke assertions, and paired Change Record/index documents. No Framework, MRTS, Gitlink, workflow, SonarQube rule, default branch, commit, push, PR, or merge action has occurred. Local source/security review and the commands above support the candidate; final documentation checks, delivery, and exact-head hosted verification remain pending.
