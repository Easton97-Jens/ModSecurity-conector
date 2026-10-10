# Change Record: CR-20261008-nginx-phase4-native-body-observations

**Language:** English | [Deutsch](CR-20261008-nginx-phase4-native-body-observations.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-phase4-native-body-observations |
| Date (UTC) | 2026-10-08 |
| Base revision | `764402f47b7d2db941e5002485b205b4d4563cbd` |

## Motivation and problem statement

Phase-4 native evidence lacked actual append counts and retained Engine length. Native Engine Reject may return append success with a pending rule-free intervention, allowing the rejected body to reach the next filter if collection waits until EOS. Post-return Engine budget rejection also needs to preserve the distinction between actual native EOS and rejected Common completion.

## Acceptance criteria

Each valid native append records actual return, supplied length, call index and actual Engine retained length. Completion requires native process return 1 and strict Common P4 completion. Immediate Reject stops forwarding and emits exact rule-free native 403/reject metadata. Timeout emits technical 504 with actual EOS; all failure paths remain terminal.

## Implementation decision and rationale

The owned body filter calls `msc_get_response_body_length` and preserves Common supplied-byte counters. Dedicated append/completion records use existing strict Common JSONL. Append callbacks are bracketed by actual response-body phase activity. Every valid native append return 0 or 1 is followed by real intervention collection before forwarding; no fixture assigns an observed outcome.

Pinned source `Transaction::appendResponseBody` returns true for Reject while setting its intervention to 403/disruptive, and returns false for ProcessPartial. The C API returns that integer directly. Retained Engine-only diagnostics independently observed Reject append 1/retained 0 and Partial append 0/retained 64. Collecting only on return 0 would miss Reject. The exact response-limit predicate and classification remain module-owned external dependencies.

Terminal processing brackets the actual native call with the coordinator's budget API. Actual native success sets native EOS before budget validation; Common completion and its strict observation occur only after budget success. Native Reject uses 403, while connector accounting limits retain 413 and unrelated control failures retain their existing classification. Failure events retain actual commitment/abort/EOS, and native Reject explicitly carries outcome reject with no Rule-ID.

## Changed files

Only `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`, `tests/test_nginx_phase4_native_body_source.py` and this EN/DE pair. Context fields, budget API, module classification and SOURCE_MAP are coordinator-owned and not edited here.

## Commands executed

RTK-wrapped controlled C17 regression initially failed on the absent observation helper. After implementation six focused tests compile real source functions against the real Common serializer for sanity 0/1. Native calls, host boundaries and begin/complete wrappers are controlled fixture seams; Common body accounting/failure and serialization are real. Split/partial/empty, actual chain no-forward Reject, invalid return/retained length/count overflow, process/completion/budget/write failures are covered. Earlier cross-phase4 discovery passed 33 tests with three existing SKIPs; final results are in the task handoff.

## Security impact

No payload enters native event metadata. Engine-owned limits remain authoritative. Rejected body never reaches the next filter, failed completion never generates completion evidence, and technical errors cannot become SAFE log-only success.

## Runtime evidence

Controlled fixture tests are not actual NGINX/Engine runtime. Previously retained native Engine-only diagnostics establish API boundary behavior for their pinned library, not a new connector build. Root must integrate context/API/module wiring and run fresh source-bound native evidence.

## Known limitations

The isolated source checkout intentionally lacks coordinator-owned context/API edits. Its focused fixture supplies those interfaces; final integrated compilation remains required. Unexpected append-time rule interventions fail closed and cannot claim EOS or canonical PASS.

## Remaining risks

Actual host, artifact, wire-framing, cleanup and revision binding require final coordinator integration/runtime validation. Completion evidence does not itself prove downstream delivery.

## Checks not run and rationale

No native connector build/runtime slot was assigned. Full lint, final native runtime and fresh-head CI/Sonar remain coordinator-owned.

## Final diff and review status

Focused owned slice; no module/common-header/SOURCE_MAP/shared worktree/MRTS edits, publication or Gitlink update.
