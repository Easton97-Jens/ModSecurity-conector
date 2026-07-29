# Change Record: Parent Common event-provenance serialization decomposition for SonarQube Cloud c:S3776

**Language:** English | [Deutsch](CR-20260729-sonar-common-event-provenance-complexity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-common-event-provenance-complexity |
| Date (UTC) | 2026-07-29 |
| Base revision | Original change base `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`; synchronized candidate base `603a7558e75a177222e22d8d0b87402dfad3f706` |
| Tracking | SonarQube Cloud rule `c:S3776` at `common/src/event.c:382`: reduce Cognitive Complexity from 32 to the allowed 25. Open PR [#174](https://github.com/Easton97-Jens/ModSecurity-conector/pull/174) originated at initial head `8baef24192ccaaa39e38e89238b8d2e8e90baec9`; the later remote head was `b92084c523498978b55de9068240752314bbedc3` before its required normal master synchronization. Historical initial-head Actions/Sonar observations do not verify a synchronized candidate. Its exact head, reviews, Actions, and SonarQube Cloud evidence must be refreshed before integration. No merge is claimed. |
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
| `python3 -B -m unittest tests/test_bilingual_docs.py` | passed: all 21 focused bilingual-documentation unit tests passed at the synchronized candidate. |
| `make check-bilingual-docs` | `blocked_environment`: it was attempted at the synchronized candidate, but the isolated task worktree has no materialized Framework submodule. The diagnostic names only missing `modules/ModSecurity-test-Framework/...` targets outside this PR's six changed paths; it is not reported as passed. |
| `make check-doc-links` | `blocked_environment`: it was attempted at the synchronized candidate and is blocked by the same absent Framework-submodule targets, all outside this PR's six changed paths; it is not reported as passed. |
| `git diff --check origin/master...HEAD` | passed after normal synchronization; it is a mandatory rerun for the then-final exact candidate before every delivery action. |
| `gh pr view 174` and SonarQube Cloud PR APIs for initial head `8baef24192ccaaa39e38e89238b8d2e8e90baec9` | observed successful/expected-skipped Actions checks, Quality Gate `OK`, 0 open PR issues, 0 new violations, and 0.0% new-code duplication. |

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
- Historical hosted evidence was observed only for `8baef24192ccaaa39e38e89238b8d2e8e90baec9`. The later remote head and every normal master-synchronized candidate require fresh GitHub Actions, SonarQube Cloud PR analysis, review-state, and exact-head evidence before the PR is presented as verified.
- The repository-wide `make check-bilingual-docs` and `make check-doc-links` checks were attempted rather than silently omitted, but both are `blocked_environment` in this isolated Parent worktree because its Framework gitlink is intentionally unmaterialized. Their diagnostics list only missing Framework targets outside this PR's changed paths. They remain required in an environment where that dependency is available and are not treated as passing evidence.
- `git diff --check origin/master...HEAD` and `git status --short` are individual delivery gates after every candidate amendment. They must be rerun and observed for the selected exact head before any push or merge; this record makes no delivery claim until that happens.

## Known limitations

The local helper smoke validates representative metadata, redaction, and truncation behavior but is not a connector-host integration test. Open PR #174 has no merge, approval, or final synchronized-head hosted evidence yet.

## Remaining risks

Future additions must keep name arrays, value arrays, and negative controls aligned; a mismatched index could omit or mislabel provenance. Fixed enum dimensions, ordered table review, populated-field assertions, C17 controls, and fail-closed append behavior reduce that risk. Exact-head hosted analysis remains required to verify the actual Sonar remediation.

## Final diff and review status

The scoped candidate changes only Common event provenance decomposition, its focused smoke assertions, and paired Change Record/index documents. Initial commit `8baef24192ccaaa39e38e89238b8d2e8e90baec9` opened PR #174, and the later remote head `b92084c523498978b55de9068240752314bbedc3` contains this documentation follow-up. A normal synchronization creates a new unverified candidate. No Framework, MRTS, Gitlink, workflow, SonarQube rule, default-branch, or merge action is claimed. The focused bilingual suite passed; the two repository-wide documentation checks are individually recorded as `blocked_environment`, while exact-head diff/status and hosted verification remain mandatory, newly observed gates before any delivery action.
