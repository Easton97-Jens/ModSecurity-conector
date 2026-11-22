# Change Record: CR-20261119-composite-cleanup-redirect-haproxy-rule-id

**Language:** English | [Deutsch](CR-20261119-composite-cleanup-redirect-haproxy-rule-id.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261119-composite-cleanup-redirect-haproxy-rule-id |
| Date (UTC) | 2026-11-19 |
| Base revision | `b79c3d93efbb8330f121caf8fb7c1a7874195e57` |

## Motivation and problem statement

A static security review of the Parent connector scope (2026-11-15) reported
low-severity candidates. This change fixes the ones that could be confirmed
and reproduced, plus one additional defect found while fixing them:

- **Client disconnect faults the composite engine (new, availability).**
  ForwardAuth passed the request context to `Admission.Cancel` and other
  finish paths exactly when that context was already canceled. The native
  `commonRuntimeTransaction.Close` treats a canceled context as an unsafe
  cleanup: it marks the whole engine terminally failed, and the coordinator
  enters a fault state. One client that disconnects during the P2 body upload
  therefore made every later composite request fail with 503 until restart.
- **CAND-025: unbounded native cleanup.** About twenty coordinator paths
  finish entries with `context.Background()`. While a native call never
  returns, `Close` waits forever for the serial Common runtime gate, together
  with the entry's `closeOnce` waiters, the finish gate and the Traefik
  companion's UDS admission slot. MSC2 engine work used the same unbounded
  context, so sessions queued behind such a call also kept their slots.
- **CAND-026: unchecked ForwardAuth `Location` sink.** `writeDecision` copied
  `Decision.RedirectURL` into `Location` without the control/length check used
  by every sibling sink; an empty target produced a 302 without `Location`.
- **CAND-001: `%u` with a signed `int rule_id`** in the HAProxy SPOP
  Phase-4 event, so a negative ID appeared as a large unsigned number.

**Review follow-up (2026-11-20, on head `a79f78f3e5f9a612d854e3924cf2a7e43eb47ab7`).**
A review of the published head found two remaining CAND-025 gaps, both
confirmed against the code and reproduced:

- `BeginRequest` closed a transaction that was opened but not yet registered
  (coordinator faulted or closed in between) with `context.WithoutCancel(ctx)`,
  which has no deadline: this path bypassed the cleanup budget.
- The MSC2 claim and the session's abort waited on the entry mutex without a
  context. ForwardAuth holds that mutex during its native P1/P2 call, so the
  frame deadline could not end the wait, and `Sweep` stalled behind such an
  entry as well. Merely bounding the abort would have been fail-open: a slow
  P2 call returning `allow` after the session ended would still have
  authorized the request.

## Acceptance criteria

1. A canceled caller context never reaches native cleanup; one disconnected
   ForwardAuth request fails only itself and the real Common engine keeps
   serving the next request.
2. Native cleanup of a terminal entry returns within `Limits.CleanupTimeout`
   (default 5 s) and, on timeout, leaves the coordinator fail-closed.
3. MSC2 engine work is bounded by the frame deadline; a session blocked in
   engine work ends and releases its admission slot.
4. ForwardAuth sends `Location` only for a valid target; invalid or empty
   targets become a 403 deny, recorded and sent consistently.
5. The HAProxy event formats positive rule IDs with `%d` and uses the empty
   string for missing IDs; cppcheck no longer reports `invalidPrintfArgType`.
6. Legitimate lifecycles (normal cleanup, valid redirects, normal UDS session)
   keep working; existing Framework Go tests stay green.
7. The direct cleanup in `BeginRequest` uses the same detached, bounded budget.
8. A claim or abort that meets an entry held by a native call returns within
   its budget; the held call can no longer make the reservation claimable,
   the entry is closed and its slot released exactly once, and `Sweep` skips a
   held entry instead of waiting for it.

## Implementation decision and rationale

- `composite.Coordinator.cleanupContext` wraps the caller context with
  `context.WithoutCancel` and `context.WithTimeout(Limits.CleanupTimeout)`;
  `entry.finish` uses it for `tx.Close`. Fixing the single root-cause site
  covers every finish caller, including `abortAll`, `Sweep` and the composite
  Envoy path, and avoids a bounded session cleanup waiting behind an
  unbounded `closeOnce` holder. The default matches the existing 5 s UDS
  timeout and idle TTL. On expiry the existing Common runtime contract applies
  (cleanup failure, no native free, fail-closed coordinator fault).
- `compositetraefik.UDS` serves each frame through `serveFrame`, whose engine
  context uses the connection deadline that already bounds the frame read and
  the result write. A later result could not be written anyway. *Correction
  (2026-11-20):* at `a79f78f3` this did not cover the claim, which waited on
  the entry mutex without a context; see the follow-up below.
- **Follow-up (2026-11-20).** `BeginRequest` now closes an unregistered
  transaction through `cleanupContext`. `lockEntry` acquires the entry mutex
  with a context by polling `TryLock`, like the Common runtime gate, so no
  goroutine stays blocked on the mutex. `ClaimContext` and
  `AbortWithReasonContext` use it (`Claim`/`AbortWithReason` keep their
  unbounded behavior with `context.Background()`); the UDS passes the frame
  deadline to the claim and a fresh budget, created at cleanup, to the abort.
  A busy abort records its reason on the entry (atomic, verified against the
  immutable reserving session) instead of closing a transaction in use:
  `checkLocked`, the request phases after their native call and
  `markReservedLeaseLocked` (the only claimable transition) then reject the
  entry with `ErrAborted`, and its owner finishes it with that reason. A
  successful abort marks the entry terminal before `finish`, as
  `checkSessionLocked` already does, so no new native call can start in
  between. `Sweep` uses `TryLock` and examines a held entry on the next tick.
  Only native `Close` is time-bounded; `finishGate`, `closeOnce` and the entry
  mutex inside `finish` are not, which the code documents. Functions that now
  take a `ctx` pass it to `finish` (neutral, because `finish` detaches and
  bounds it) to avoid new `go:S8239` findings.
- ForwardAuth validates redirect targets before `RecordHostAction` with a
  `validRedirectURL` equivalent to the composite Envoy sink (non-empty,
  at most 2048 bytes, valid UTF-8, no surrounding whitespace, no byte below
  0x20, no DEL); invalid targets become a 403 deny. `writeDecision` re-checks
  the value as the sink.
- HAProxy: `%d` for `rule_id > 0`, otherwise the empty string, matching the
  wire path's `rule_id > 0` guard and the other connectors' events.
- **Not changed: CAND-024 (SO_PEERCRED on the composite UDS).** The candidate
  assumes a hostile process with the same UID. SO_PEERCRED compared with the
  service's own UID cannot distinguish such a process, and
  `connectors/traefik/README.md` documents the private `0700` directory as a
  cross-UID boundary, not as isolation from the same UID. A check would add no
  same-UID protection but could reject a Traefik process that runs as root.
  The Yaegi plugin side would additionally need `useUnsafe`. No change was
  made; the reasoning is recorded here.

## Changed files

| Path | Change |
| --- | --- |
| `connectors/envoy/ext_proc/internal/composite/coordinator.go` | `Limits.CleanupTimeout`, `cleanupContext`, bounded detached `tx.Close` in `entry.finish`. Follow-up: bounded direct cleanup in `BeginRequest`, `lockEntry`, `ClaimContext`, `AbortWithReasonContext`, abort marking (`ErrBusy`, `ErrAborted`), guarded `markReservedLeaseLocked`, non-blocking `Sweep`. |
| `connectors/envoy/ext_proc/internal/compositetraefik/uds.go` | `serveFrame` with frame-deadline engine context; `deadline` replaced by `frameDeadline`. Follow-up: claim with the frame context, abort with a budget created at cleanup. |
| `connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go` | `validRedirectURL`, redirect normalization before the host action, checked `Location` sink. |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | Signed `rule_id` formatting in `phase4_common_event_write`. |
| `connectors/traefik/README.md`, `connectors/traefik/README.de.md` | Composite cleanup, disconnect and redirect behavior. |
| `reports/audits/change-records/CR-20261119-composite-cleanup-redirect-haproxy-rule-id.md`, `.de.md` | This record. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | Pre-existing handoff refresh from the main checkout plus this task's state. |
| `.gitignore` | Pre-existing `.sonarlint` entry from the main checkout. |

No Framework or MRTS file is part of this Connector change. The regression
tests are Framework-owned: Framework Draft PR
[#181](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/181)
(branch `claude/composite-cleanup-regression-tests-20261120`, head
`12e83a6fc189275234b9abad2e7b12132d82ff94`) adds them as on-demand tests. The
Connector Framework gitlink is unchanged.

## Commands executed

All commands ran through RTK from the task worktree. Builds, caches and logs
are under `/var/tmp/codex/ModSecurity-conector/runs/claude-security-fix-20261119/`.

| Command | Result |
| --- | --- |
| `rtk bypass make prepare-runtime-components RUNTIME_COMPONENT_TARGET=shared` | Exit 0; official ModSecurity **v3.0.17** (Framework-approved commit `1925753989ccce977cdaae417b55c9726c7cf02c`) built into the shared prefix `cache/shared/prefix/modsecurity/bfc407ee…`. *Correction (2026-11-20):* this prefix resolved PCRE2 from the system library; the follow-up evidence below uses a prefix with the bundled pinned PCRE2. |
| `rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (baseline, default inventory) | Exit 0. |
| `ON_DEMAND_TESTS=1 rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (baseline) | Exit 0, 8 packages ok. |
| `rtk bypass sh run-task-tests.sh after <task worktree> <v3.0.17 prefix>`: native `build_composite.sh`, then `go test -tags libmodsecurity -overlay <Framework on-demand + task tests> ./...` | Build exit 0; tests exit 0; all 8 packages ok; `ldd` shows `libmodsecurity.so.3` from the v3.0.17 prefix. |
| Same runner `before` on unchanged `origin/master` | Tests exit 1: wedged cleanup hung > 10 s; canceled caller context and the real-engine disconnect both produced a coordinator fault; 8 invalid redirect targets returned 302; UDS session blocked > 5 s; controls passed. |
| `rtk bypass make -C connectors/haproxy build-spoa-runtime` against the v3.0.17 prefix (before and after) | Exit 0 for both. |
| `rtk bypass cppcheck --enable=warning … haproxy_spop_diagnostic_runtime.c` | Before: `invalidPrintfArgType_uint` at line 2667; after: none. |
| `rtk bypass go vet` and `gofmt -l` on changed packages | Clean. |
| `rtk bypass git diff --check` | Clean. |

**Follow-up (2026-11-20), run ID `claude-pr454-review-20261120`**, logs under
`/var/tmp/codex/ModSecurity-conector/runs/claude-pr454-review-20261120/`.
libModSecurity v3.0.17 with the bundled pinned PCRE2 10.49 (Framework PR #180
provisioning; `ldd` resolves both from that prefix, no system PCRE2). Tests
are those of Framework PR #181.

| Command | Result |
| --- | --- |
| `ON_DEMAND_TESTS=1 GOFLAGS='-tags=libmodsecurity -v' rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc FRAMEWORK_ROOT=<Framework PR #181 worktree>` (after native `build_composite.sh`) | Exit 0; 8 packages ok; 20 of 20 new tests passed, 0 skipped. |
| Same with `-race` | Exit 0; 8 packages ok; 0 data races. |
| Same tests without `entry_wait_bounds_test.go` against `a79f78f3e5f9a612d854e3924cf2a7e43eb47ab7` | Exit 1, expected: both direct-cleanup tests did not return within 2 s at a 50 ms budget, `Sweep` stalled, the claim waited beyond 2 s at a 100 ms frame deadline; all other tests passed. |
| Same tests without the three coordinator files against `b79c3d93efbb8330f121caf8fb7c1a7874195e57` | Exit 1, expected: held claim, unbounded response work, 8 invalid redirects returned 302, disconnect faulted the coordinator (double and real engine: `cannot close Common runtime after unsafe transaction cleanup`); controls passed. |
| `rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (default inventory, Framework PR #181) | Exit 0; 2 of 2 selected cases passed; `active_case_count` 100. |
| `ON_DEMAND_TESTS=1 rtk bypass make -C connectors/haproxy self-test-spoa-runtime` (Framework PR #181), base / fixed | Exit 2 / 2: the new case reports `rule_id=0 did not serialize as ""` on the base and passes after the fix; a later, unchanged protocol self-test fails silently in both, also with the unmodified Framework pin (pre-existing). |
| `rtk bypass go vet ./internal/... ./cmd/...`, `gofmt -l` | Clean. |
| `rtk bypass /usr/local/bin/sonar-with-env api get /api/issues/search?…pullRequest=454…` | 8 new `go:S8239` code smells on `a79f78f3`, all in `coordinator.go` lines unchanged by this PR (blame `6ccfd8de`); classified below. |
| `gh pr checks 454` on `a79f78f3` | 58 passed, 5 skipped, 0 failed; SonarCloud Quality Gate passed. These results do not cover the unpublished follow-up. |

## Security impact

- Removes a remotely triggerable, fail-closed denial of service of the
  experimental Traefik composite: a disconnecting client no longer disables
  the shared Common engine. Precondition before the fix: a client aborts
  during the ForwardAuth P2 body phase. Impact before the fix: every later
  composite request returned 503 until restart.
- Bounds resource retention when a native call never returns; the process
  still requires a controlled restart in that case, now as an explicit fault.
- Defense in depth for the ForwardAuth `Location` sink; Go `net/http` already
  rewrites raw CR/LF, so no independent header injection existed.
- Evidence integrity for HAProxy Phase-4 events.
- No authentication, authorization, isolation or redaction control was
  weakened; invalid redirect targets are denied more strictly.

## Runtime evidence

The regression tests used the real Common/libmodsecurity engine
(`-tags libmodsecurity`) linked against the official v3.0.17 build; the
2026-11-20 runs used the prefix with the bundled pinned PCRE2 10.49. They are
package-level runtime tests, not host-level evidence: no Traefik, Envoy or
HAProxy host process was started.

## Known limitations

- A native call that never returns still requires a process restart; the
  composite service does not restart itself on a coordinator fault.
- CAND-024 is not changed (see the rationale above).
- The composite Envoy path benefits from the coordinator fix, but no
  composite-Envoy-specific reproducer was written.
- The `before` run also panicked in a task test double for a `nil` context;
  the real `Close` normalizes `nil`, so this is not a product defect.
- Bounds are per step (frame deadline, abort budget, native close budget), not
  a hard total time limit for a UDS handler. `finishGate`, `closeOnce` and the
  entry mutex inside `finish` are not timed; a busy claim may use the whole
  frame deadline, so the companion can see a closed session instead of a 503
  frame (both fail closed).
- The 8 `go:S8239` findings on `a79f78f3` are pre-existing deliberate
  detachments of fail-closed cleanup from request contexts; before this PR
  passing the request context there would have caused the canceled-context
  engine fault. They are not changed here and need a Sonar disposition by a
  maintainer.
- The HAProxy native self-test target fails in this environment because of a
  pre-existing, silent protocol self-test failure.

## Remaining risks

Under very heavy contention a legitimate cleanup that waits longer than 5 s
for the serial gate now faults the coordinator instead of waiting. The
standalone ext_proc service already applies the same model with a 1 s
default; the 5 s composite default is more conservative.

## Checks not run and rationale

- No host runtime, matrix, sanitizer, fuzz or CRS run: outside this scoped fix.
- `go test -race`: run on 2026-11-20 for the follow-up (passed).
- The regression tests are on-demand Framework tests (Framework Draft PR #181),
  not part of the 100-case default suite. Run the specialist regressions from
  Framework #181 with `CONNECTOR_REVISION` set to a Parent revision that
  contains this follow-up.
- Verify hosted CI and the SonarQube Cloud Quality Gate for the current PR head.

## Final diff and review status

The final scoped diff was reviewed locally; `git diff --check` is clean.
Delivery is tracked in [Parent PR #454](https://github.com/Easton97-Jens/ModSecurity-conector/pull/454).

On 2026-11-21 the native `build-envoy-ext-proc` build and all eight packages in the `framework-go-test` run passed. The test selected the Framework #181 overlay, the `libmodsecurity` build tag and the pinned ModSecurity/PCRE2 prefix.

The eight S8239 cleanup call sites now pass the caller context. The cleanup helper retains its independent timeout and ignores request cancellation. All eight packages passed again with the race detector enabled.
