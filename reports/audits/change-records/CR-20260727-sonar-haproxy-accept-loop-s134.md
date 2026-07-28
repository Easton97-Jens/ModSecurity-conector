# Change Record: Parent HAProxy accept-loop error-path cleanup for SonarQube Cloud C:S134

**Language:** English | [Deutsch](CR-20260727-sonar-haproxy-accept-loop-s134.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-haproxy-accept-loop-s134 |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud Code Smell receipt `AZ7HxAr7_i61V0DF6_H2` for `c:S134` at `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` in `accept_loop(...)`. |
| Boundary | Parent HAProxy source, its focused Parent reliability-contract test, and this English/German Change Record pair with its indexes. Framework, MRTS, Gitlinks, workflow configuration, scanner configuration, Quality Gates, suppressions, and the external SonarQube Cloud issue state remain unchanged. |
| Candidate status | Local and uncommitted. No staging, commit, push, pull request, merge, Framework or MRTS change, or Gitlink change has occurred. |

## Motivation and problem statement

Receipt `AZ7HxAr7_i61V0DF6_H2` identifies the nested error handling in the
HAProxy diagnostic runtime's `accept_loop(...)` as `c:S134`. The correction is
limited to making the existing error-path distinction explicit without changing
the successful connection-processing path:

- a non-`EINTR` `accept()` failure must log `accept failed errno=%d` and return
  `1`;
- an `EINTR` failure must break when shutdown was requested, otherwise retry;
- a successfully accepted descriptor must continue through
  `handle_connection(...)`, `close(...)`, and the existing handled-counter
  update in the same order.

## Acceptance criteria

- Preserve the non-`EINTR` log-and-return behavior exactly.
- Preserve the `EINTR` plus stop-requested break and the non-stopped retry.
- Do not send a failed `accept()` result through connection processing, close,
  or the handled-counter update.
- Preserve the successful descriptor-processing order.
- Keep the documented validation evidence and its authority boundaries
  accurate; preliminary default-root checks are not authoritative evidence.

## Implementation decision and rationale

The candidate makes the terminal failure case the outer condition:
`errno != EINTR` logs the existing diagnostic and returns `1`. The remaining
interrupted-call path then handles only the shutdown break or retry. This
removes the avoidable nesting identified by `c:S134` while retaining each
failure disposition and leaving successful connection processing unchanged.

## Changed files

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — candidate
  `accept_loop(...)` error-path flattening.
- `tests/test_sonar_reliability_contract.py` — focused source-contract
  regression for the three failure dispositions and unchanged success path.
- `reports/audits/change-records/CR-20260727-sonar-haproxy-accept-loop-s134.md`
  and `.de.md` — this bilingual Change Record pair.
- `reports/audits/change-records/README.md` and `README.de.md` — paired index
  entries.

## Commands executed

| Executed control or recorded validation | Observed result |
| --- | --- |
| Focused Parent unit module `tests.test_sonar_reliability_contract` | passed: 7 unit tests. |
| HAProxy Common-adoption control | passed. |
| HAProxy C-standard-wiring control | passed. |
| Authoritative isolated GCC 15.2 C17 compilation | passed with a task-owned external root; that root was cleaned after validation. |
| Authoritative isolated Clang 21.1 C17 compilation | passed with a task-owned external root; that root was cleaned after validation. |
| Preliminary default-root checks | not authoritative and excluded from acceptance evidence. |
| Focused invocation of the Change Record structural-parity routines from `ci/checks/documentation/check-bilingual-docs.py` | passed: required headings, language switches, identity fields, heading levels, table blocks, and fenced-block structure match. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs check-doc-links` | passed after read-only initialization of the Parent-pinned Framework revision `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`: `bilingual docs ok`, `repository path references: PASS`, and `doc links ok`. |
| `git diff --check` | passed. |

## Security impact

No new reportable security finding was identified. This is a maintainability
Code Smell remediation, not a demonstrated attacker-controlled path or a
change to a trust boundary. The relevant error-path invariant was reviewed:
a failed `accept()` result must not reach `handle_connection(...)`,
`close(...)`, or the handled-counter update; a non-`EINTR` failure logs and
returns, while only `EINTR` can retry and a requested stop breaks the loop.
The candidate preserves that invariant and does not introduce parsing,
authentication, authorization, privilege, or data-flow behavior.

## Runtime evidence

No live HAProxy network-runtime result is claimed. The seven focused unit tests
exercise the source contract, and the isolated GCC 15.2 and Clang 21.1 C17
checks establish compilation evidence. Those checks do not substitute for a
live connector runtime or hosted SonarQube Cloud analysis.

## Known limitations

- The SonarQube Cloud receipt is attached to the stated base revision; no
  exact-head hosted analysis or issue closure is claimed.
- No live HAProxy runtime or full connector matrix was run for this candidate.
- The task-owned external compiler roots were cleaned after the authoritative
  isolated checks; preliminary default-root checks are deliberately not used as
  authoritative evidence.

## Remaining risks

The focused contract and two isolated C17 compiler checks reduce the risk of
changing the three error dispositions, but they do not exercise operating
system signal timing in a live HAProxy process. A future exact-head SonarQube
Cloud analysis may still report the receipt until it analyzes a delivered
candidate; this record does not claim that external state has changed.

## Checks not run and rationale

No live HAProxy runtime, full connector matrix, hosted GitHub CI, hosted
SonarQube Cloud analysis, delivery action, Framework action, or MRTS action was
run. The task is a local Parent candidate and documentation record only; those
separate controls and repositories are outside this authorized scope.

## Final diff and review status

The worktree contains a local, uncommitted candidate consisting of the
HAProxy source refactor, its focused test, and this bilingual documentation
pair with indexes. No Git stage, commit, push, pull request, merge, Framework
or MRTS source change, or Gitlink update has been performed. The focused Change
Record structural-parity check, full documentation/link checks, and whitespace
diff check passed. The Parent-pinned Framework was initialized read-only only
to run those documentation checks; its source, Gitlink, and nested MRTS state
remain unchanged.
