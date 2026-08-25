# Change Record CR-20260825: Lighttpd Phase-2 pre-upstream gate

**Language:** English | [Deutsch](CR-20260825-lighttpd-phase2-pre-upstream-gate.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260825-lighttpd-phase2-pre-upstream-gate` |
| Date (UTC) | `2026-08-25` |
| Base revision | `5d71be74369123257851eb5ec612d7523a6b061d` |
| Scope | Parent repository only: the selected patched Lighttpd HTTP/1.1 `mod_proxy` Phase-2 request-body admission path, focused harness/contracts, EN/DE documentation, and paired traceability. No Framework, MRTS, Gitlink, workflow, dependency, quality-control, P3, or P4 change. |

## Motivation and problem statement

Before this change, active request-stream flags could let `mod_proxy` connect
or forward while Common Runtime still needed terminal-EOS Phase-2 inspection.
That violates the pre-upstream admission boundary. The exact rejecting
libmodsecurity request-body-limit intervention also needed the host-visible
HTTP 413 status rather than the engine's generic 403 signature.

Retaining a streaming request until EOS also means the host must not continue
accepting an unbounded body after Common Runtime has merely truncated
inspection. `body_limit_action=process_partial` has that behavior, so it is
unsafe for this selected retained-body profile. PR #339 is merged into the
current `master` base and its Stock ABI layout is inherited; it is not an open
dependency. The user authorized one task branch, one atomic commit, push, and
a Draft PR, but no merge.

## Acceptance criteria

- Before EOS, a Phase-2 deny, body-limit rejection, incomplete-body timeout,
  or unsupported mode creates no upstream connection or byte delivery.
- After EOS, an allowed request creates exactly one upstream delivery of the
  complete body.
- Pre-active/re-activated stream flags, `Incremental`, and body-bearing
  `Upgrade` fail closed with HTTP 501 on the selected profile.
- Streaming accepts only `body_limit_action=reject`; `process_partial` fails
  during configuration loading before a listener or upstream exists.
- The exact rejecting `SecRequestBodyLimitAction` Phase-2 signature maps to
  HTTP 413 while other intervention statuses remain unchanged.
- C17 build/contract/runtime evidence and truthful EN/DE documentation pass;
  no `.github/` file changes.

## Implementation decision and rationale

- `mod_msconnector_prepare_request_body()` clears active request-stream flags
  before body reads and waits until terminal EOS has produced the Phase-2
  decision. It rejects pre-active streaming, `Incremental`, and `Upgrade`.
- The request-body hook repeats the active-flag check, so later activation is
  also fail closed. A per-request gate-rejection marker avoids normal
  transaction completion only for that rejected request.
- `msconnector_runtime_body_limit_action()` exposes the parsed Common Runtime
  action. In the patched ABI branch, setup rejects streaming unless it is
  `MSCONNECTOR_BODY_LIMIT_ACTION_REJECT`; Stock and non-streaming behavior is
  unchanged.
- `native_intervention_status()` maps only the exact no-redirect request-body
  limit signature to 413 and preserves all unrelated rules and statuses.
- The retained-body bound comes from the positive Common `request_body_limit`
  (default 1 MiB) and its rejecting read cycle. The module does not configure
  `server.max-request-size`, which remains an independent host defense-in-
  depth setting.

## Changed files

- `common/runtime/msconnector_runtime.c`
- `common/runtime/msconnector_runtime.h`
- `connectors/lighttpd/module/mod_msconnector.c`
- `connectors/lighttpd/harness/run_phase2_pre_upstream_gate.py`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `tests/test_lighttpd_phase2_pre_upstream_gate_contract.py`
- `tests/test_modsecurity_request_body_limit_status_contract.py`
- `connectors/lighttpd/README.md` and `connectors/lighttpd/README.de.md`
- `connectors/lighttpd/harness/README.md` and `connectors/lighttpd/harness/README.de.md`
- `docs/connectors/README.md` and `docs/connectors/README.de.md`
- `docs/connectors/lighttpd.md` and `docs/connectors/lighttpd.de.md`
- this paired Change Record and the paired Change-record archive indexes

## Commands executed

| Check | Actual result |
| --- | --- |
| Fresh patched-host GCC/C17 build and `check-lighttpd-patched-host` | Passed with the pinned Lighttpd 1.4.85 patch SHA-256 `e00d3892ab0ad7fb409e1ef593e2c3bda71ea44ee2002c4db325712d46bfa8b5`. |
| Stock GCC and Clang; patched Clang module builds | Passed under `-std=c17 -Wall -Wextra -Werror`. |
| `make -C connectors/lighttpd check-lighttpd-core-patch` | Passed. |
| `make check-common-helpers-c17` | Passed. |
| `make check-connector-config-reference` | Passed. |
| Selected shell syntax and Python compilation | Passed. |
| Focused Phase-2/status/ABI command | Passed: 10 tests. |
| Master-based Lighttpd host contracts | Passed: 70 tests, 12 expected namespace skips. |
| `make check-bilingual-docs` and `make check-doc-links` | Environment-blocked: the rerun reported only repository-wide missing targets beneath the uninitialized `modules/ModSecurity-test-Framework` Gitlink and no task-document diagnostic. |

## Runtime evidence

Private receipts contain bounded metadata and no public local-evidence URL.

| Receipt | SHA-256 | Observed result |
| --- | --- | --- |
| `master-5d71-bufferbound-gate-summary` | `17ad572e3aa4699a2af051346ba7f782db418973a22b22331dedae1bf85dd2a3` | Delayed marker: 403 and zero preterminal upstream reach; delayed allow: 200 and exactly one complete post-EOS delivery; immediate marker: 403; `Incremental`, configured stream, and enabled body-bearing `Upgrade`: 501 without a new upstream connection; streaming plus `process_partial`: configuration rejection before listener/upstream. |
| `master-5d71-bufferbound-p0-p2-summary` | `eb72d9ce51260da3e76b8d79b0ca7eb2d2c6215efd57c40b41c4d9f192337f81` | P1/P2 allow/deny, empty body, 33/64-byte visible 413, RST controls, follow-up, and cleanup passed; deny/limit/reset cases did not reach upstream. |
| `master-5d71-bufferbound-timeout-summary` | `5d72aea037b9d08e682c31c16e75477cd55a4b181d6da613254c7b1bad136888` | Partial Content-Length body timed out before EOS with no event/upstream; the listener remained healthy and a following allowed 32-byte request was delivered exactly once. |

The retained P0/P2 helper's historical rules path was absent, so its first
launch stopped before any process or listener. A task-owned wrapper supplied
only the same verified read-only rules input and the fresh retry passed. No
product source or historical helper was modified.

## Security impact

The affected trust boundary is untrusted HTTP/1.1 request-body input before
the proxy upstream. The control is fail closed for unsupported/re-activated
streaming and for `process_partial`; a focused source-to-sink security review
found no plausible pre-upstream bypass or C/API error and no high/critical
finding. `FND-PARENT-0316` is `fixed_pending_merge` on this task branch and
is not closed on `master`.

## Known limitations

This is only the selected patched HTTP/1.1 `mod_proxy` Phase-2 gate. It does
not claim HTTP/2, HTTP/3, P3/P4, CRS, general request streaming, a full P1-P4
rollout, production readiness, or an independently configured host
`server.max-request-size` limit. The 12 namespace skips require unprivileged
user, mount, and PID namespace support.

## Remaining risks

- A future Lighttpd or libmodsecurity behavior change needs renewed runtime
  validation of stream flags and the intentionally narrow 413 mapping.
- Exact-head hosted checks and review cannot be inferred from local evidence.

## Checks not run and rationale

- No HTTP/2, HTTP/3, P3/P4, CRS, or full P1-P4 runtime matrix was run because
  it is outside the selected HTTP/1.1 Phase-2 scope.
- Hosted PR, SonarCloud, governance, and resulting-`master` checks require a
  Draft PR at its exact head and are not asserted before it exists.
- Documentation checks are environment-blocked solely by repository-wide
  missing targets beneath the uninitialized Framework Gitlink; no task-document
  diagnostic was reported.

## Final diff and review status

The final local scope is a Parent-only change prepared for one atomic commit,
normal push, and a Draft PR against `master`. This record deliberately asserts
neither a push, a PR, hosted checks, a direct `master` push, nor a merge;
delivery facts are recorded only after they are observed.
