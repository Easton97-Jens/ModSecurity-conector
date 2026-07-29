# Change Record: Parent HAProxy SPOP body-parser deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-spop-body-parser-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-spop-body-parser-deduplication |
| Date (UTC) | 2026-07-29 |
| Base revision | `9f23ae2c5fe908cef38f203be03f93fda75a8dd7` |
| Tracking | One current SonarQube Cloud CPD pair at lines 1214/1230: two 15-line SPOP typed-body argument parsers, reported as 30 duplicate lines. |
| Boundary | Parent HAProxy diagnostic SPOP runtime and focused test/Change Record files. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

## Motivation and problem statement

The `body` and `response_body` SPOP arguments repeated the same untrusted typed-value parsing and owned-byte-copy path. Their only intended difference is whether an accepted byte value marks the request as a response-body event. The reduction must preserve type rejection/consumption, parse-position advancement, owned-memory behavior, and phase flags.

## Acceptance criteria

- One private helper performs the existing typed byte read and accepts only SPOP string or binary values.
- Accepted values retain the owned copy and `has_body` behavior; response-body input alone sets `is_response` and `is_response_body`.
- Non-byte typed values remain consumed but do not set body or response flags.
- The focused C17 harness, the native GCC/Clang C17 runtime builds, and the repository C23 advisory control pass.
- Hosted exact-head SonarQube Cloud must report zero New Issues and zero New-Code duplication before any merge consideration.

## Implementation decision and rationale

`parse_notify_body_argument` centralizes the shared read/copy decision and accepts one explicit boolean for response-body semantics. The two public parser branches remain visible and choose only their original role. This is the narrowest repository-native change: it removes the confirmed CPD pair while retaining all protocol parsing, ownership, and phase decisions in the same source file.

## Changed files

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — private shared typed-body parser and two explicit role callers.
- `tests/test_sonar_reliability_contract.py` — C17 harness coverage for string, binary, response, and non-byte paths.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `python3 -m unittest tests.test_sonar_reliability_contract` | passed: 11 tests, including the compiled typed-body parser harness. |
| Native SPOA runtime build and self-test under GCC C17 `-Wall -Wextra -Werror` | passed against the existing temporary libmodsecurity prefix. |
| Native SPOA runtime build and self-test under Clang C17 `-Wall -Wextra -Werror` | passed against the same temporary prefix. |
| `make check-haproxy-common-adoption` and C17 wiring/lint controls | passed. |
| `make check-haproxy-c23` | passed. |
| `git diff --check` | passed. |

## Security impact

The source-to-sink path is a peer-controlled SPOP typed argument to the owned `request->body` buffer. The helper preserves the pre-existing strict type boundary: only String/Binary values reach `copy_bytes`; other types are consumed by the existing typed-data reader and cannot change body or response state. The focused C17 harness exercises both accepted byte types and the non-byte negative control, with response flags asserted separately. No parser bounds check, ownership control, authorization, protocol control, or Quality Gate is weakened.

## Runtime evidence

The real diagnostic SPOP binary completed its handshake and typed `set-var` ACK self-test under both compilers. This proves the selected diagnostic protocol path, not live HAProxy production enforcement or response-body Phase 4, which the target reports as disabled.

## Known limitations

- No live HAProxy plus ModSecurity runtime or full connector matrix was run because the version-pinned host source/runtime fixture is not present in this temporary task worktree.
- The complete Codex Security diff-scan capability remains unavailable because its mandatory delegated-worker preflight is incomplete; no full scan report is claimed.
- Hosted checks and fresh exact-head SonarQube Cloud analysis remain pending.

## Remaining risks

- Future typed body forms must keep using the helper or receive an equivalent protocol/ownership review; adding a third accepted type requires a new security decision.

## Checks not run and rationale

No live HAProxy runtime, full connector matrix, or complete Codex Security diff scan ran. Required external host fixtures are absent and the scan capability cannot obtain its required delegated worker. The typed parser harness and two native compiler/runtime self-tests are the strongest available controls.

## Final diff and review status

The candidate is confined to Parent HAProxy SPOP parsing and bilingual traceability. It removes the sole confirmed 30-line CPD pair while preserving request/response role separation. Local review is complete; a separate Draft PR and exact-head hosted verification remain required before any delivery or merge claim.
