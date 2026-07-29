# Change Record: Parent HAProxy SPOP body-parser deduplication

**Language:** English | [Deutsch](CR-20260729-sonar-haproxy-spop-body-parser-deduplication.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260729-sonar-haproxy-spop-body-parser-deduplication |
| Date (UTC) | 2026-07-29 |
| Base revision | `a81456110a6bb6f7cf2f8202f5223fb3f7b3a194` |
| Tracking | The original 30-line SPOP typed-body CPD pair is centralized in one value helper. The current exact PR head has two SonarQube Cloud `c:S134` findings in `parse_notify_payload` for the remaining nested `body` and `response_body` key branches. |
| Boundary | Parent HAProxy diagnostic SPOP runtime and focused test/Change Record files. No Framework, MRTS, Gitlink, workflow, Sonar configuration, suppression, or `master` change. |

## Motivation and problem statement

The `body` and `response_body` SPOP arguments originally repeated the same untrusted typed-value parsing and owned-byte-copy path. The existing value helper removes that CPD pair, but the remaining two nested key branches now trigger Sonar `c:S134`. The follow-up must preserve exact key recognition, unknown-key non-consumption, type rejection/consumption, parse-position advancement, owned-memory behavior, and phase flags.

## Acceptance criteria

- One private value helper performs the existing typed byte read and accepts only SPOP string or binary values.
- One private key dispatcher recognizes only `body` and `response_body`, delegates their original roles, and returns the existing parser-fallthrough result for unknown keys without consuming data.
- Accepted values retain the owned copy and `has_body` behavior; response-body input alone sets `is_response` and `is_response_body`.
- Non-byte typed values remain consumed but do not set body or response flags.
- The focused C17 harness, the native GCC/Clang C17 runtime builds, and the repository C23 advisory control pass.
- Hosted exact-head SonarQube Cloud must report zero New Issues and zero New-Code duplication before any merge consideration.

## Implementation decision and rationale

`parse_notify_body_argument` retains the shared read/copy decision and its explicit response-body role. The new `parse_notify_body_key_argument` centralizes only the two bounded literal-key decisions and returns the same tri-state contract used by the header dispatcher: zero for a consumed known argument, one for another parser, and `-1` for malformed input. This removes the two nested error branches while retaining all protocol parsing, ownership, and phase decisions in the same source file.

## Changed files

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — private shared typed-body value parser plus bounded body-key dispatcher.
- `tests/test_sonar_reliability_contract.py` — C17 harness coverage for string, binary, response, non-byte, and unknown-key non-consumption paths.
- This English/German Change Record pair and its paired indexes.

## Commands executed

| Executed control | Observed result |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | passed: 11 tests, including the compiled body-key dispatcher harness. |
| `make check-haproxy-common-adoption`, `make check-haproxy-c-standard-wiring`, and `make check-haproxy-c17-lint` | passed. |
| `make check-haproxy-c23` | passed. |
| `CC=clang HAPROXY_C_STD_PROFILE=c17 sh ci/checks/connectors/haproxy/check-haproxy-c-standards.sh` | passed. |
| `git diff --check` | passed. |

## Security impact

The source-to-sink path is a peer-controlled SPOP typed argument to the owned `request->body` buffer. The key dispatcher uses exact bounded literal comparison and leaves unknown keys and the parse position unchanged for the existing general skip path. The value helper preserves the strict type boundary: only String/Binary values reach `copy_bytes`; other types are consumed by the existing typed-data reader and cannot change body or response state. The focused C17 harness exercises both accepted byte types, the non-byte negative control, and unknown-key non-consumption. No parser bounds check, ownership control, authorization, protocol control, or Quality Gate is weakened.

## Runtime evidence

The focused C17 harness compiles the actual diagnostic runtime source and exercises the selected key-dispatch path. No live HAProxy production enforcement or response-body Phase 4 is claimed.

## Known limitations

- No live HAProxy plus ModSecurity runtime or full connector matrix was run because the version-pinned host source/runtime fixture is not present in this temporary task worktree.
- The complete Codex Security diff-scan capability remains unavailable because its mandatory delegated-worker preflight is incomplete; no full scan report is claimed.
- Hosted checks and fresh exact-head SonarQube Cloud analysis remain pending.

## Remaining risks

- Future typed body forms must keep using the helper or receive an equivalent protocol/ownership review; adding a third accepted type requires a new security decision.

## Checks not run and rationale

No live HAProxy runtime, full connector matrix, or complete Codex Security diff scan ran. Required external host fixtures are absent and the scan capability cannot obtain its required delegated worker. The typed parser harness and two native compiler/runtime self-tests are the strongest available controls.

## Final diff and review status

The candidate is confined to Parent HAProxy SPOP parsing and bilingual traceability. It preserves the original CPD reduction and removes the two current `c:S134` nesting branches while preserving request/response role separation. Local review is complete; the Draft PR needs fresh exact-head hosted verification before any delivery or merge claim.
