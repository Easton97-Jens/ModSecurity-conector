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
  the result write. A later result could not be written anyway.
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
| `connectors/envoy/ext_proc/internal/composite/coordinator.go` | `Limits.CleanupTimeout`, `cleanupContext`, bounded detached `tx.Close` in `entry.finish`. |
| `connectors/envoy/ext_proc/internal/compositetraefik/uds.go` | `serveFrame` with frame-deadline engine context; `deadline` replaced by `frameDeadline`. |
| `connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go` | `validRedirectURL`, redirect normalization before the host action, checked `Location` sink. |
| `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | Signed `rule_id` formatting in `phase4_common_event_write`. |
| `connectors/traefik/README.md`, `connectors/traefik/README.de.md` | Composite cleanup, disconnect and redirect behavior. |
| `reports/audits/change-records/CR-20261119-composite-cleanup-redirect-haproxy-rule-id.md`, `.de.md` | This record. |
| `docs/AI-HANDOFF.md`, `docs/AI-HANDOFF.de.md` | Pre-existing handoff refresh from the main checkout plus this task's state. |
| `.gitignore` | Pre-existing `.sonarlint` entry from the main checkout. |

No Framework or MRTS file was changed. The regression tests below are
task-owned and were applied only through a Go `-overlay`; they are not part of
this commit.

## Commands executed

All commands ran through RTK from the task worktree. Builds, caches and logs
are under `/var/tmp/codex/ModSecurity-conector/runs/claude-security-fix-20261119/`.

| Command | Result |
| --- | --- |
| `rtk bypass make prepare-runtime-components RUNTIME_COMPONENT_TARGET=shared` | Exit 0; official ModSecurity **v3.0.17** (Framework-approved commit `1925753989ccce977cdaae417b55c9726c7cf02c`) built into the shared prefix `cache/shared/prefix/modsecurity/bfc407ee…`; the system library was not used for tests. |
| `rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (baseline, default inventory) | Exit 0. |
| `ON_DEMAND_TESTS=1 rtk bypass make framework-go-test GO_TEST_MODULE=connectors/envoy/ext_proc` (baseline) | Exit 0, 8 packages ok. |
| `rtk bypass sh run-task-tests.sh after <task worktree> <v3.0.17 prefix>`: native `build_composite.sh`, then `go test -tags libmodsecurity -overlay <Framework on-demand + task tests> ./...` | Build exit 0; tests exit 0; all 8 packages ok; `ldd` shows `libmodsecurity.so.3` from the v3.0.17 prefix. |
| Same runner `before` on unchanged `origin/master` | Tests exit 1: wedged cleanup hung > 10 s; canceled caller context and the real-engine disconnect both produced a coordinator fault; 8 invalid redirect targets returned 302; UDS session blocked > 5 s; controls passed. |
| `rtk bypass make -C connectors/haproxy build-spoa-runtime` against the v3.0.17 prefix (before and after) | Exit 0 for both. |
| `rtk bypass cppcheck --enable=warning … haproxy_spop_diagnostic_runtime.c` | Before: `invalidPrintfArgType_uint` at line 2667; after: none. |
| `rtk bypass go vet` and `gofmt -l` on changed packages | Clean. |
| `rtk bypass git diff --check` | Clean. |

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
(`-tags libmodsecurity`) linked against the official v3.0.17 build. They are
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

## Remaining risks

Under very heavy contention a legitimate cleanup that waits longer than 5 s
for the serial gate now faults the coordinator instead of waiting. The
standalone ext_proc service already applies the same model with a 1 s
default; the 5 s composite default is more conservative.

## Checks not run and rationale

- No host runtime, matrix, sanitizer, fuzz or CRS run: outside this scoped fix.
- `go test -race` was not run.
- Task regression tests are not added to the Framework inventory: the
  Framework is a separate repository and the default suite is capped at
  100 active cases.
- Hosted CI and the SonarQube Cloud Quality Gate must be read for the PR head.

## Final diff and review status

The final scoped diff was reviewed locally; `git diff --check` is clean.
Delivery is a Draft PR from `claude/fix-security-findings-20261119`; it is not
merged.
