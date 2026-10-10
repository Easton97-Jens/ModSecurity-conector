# Change Record: Envoy bridge terminal errors and body commitment

**Language:** English | [Deutsch](CR-20260922-pr382-envoy-bridge.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-envoy-bridge` |
| Date (UTC) | `2026-09-22` |
| Base revision | `57d42c575372edca0149465038d8a683a11d494d` |

## Motivation and problem statement

Continue I09/I10 and route-specific I12 evidence in PR #382. The ext_proc C
bridge discarded a Common commit failure and could re-enter Common after a
failed append or EOS. It also marked a body as started for empty response EOS.
The Go caller unconditionally returned success after the old void commit API.
These adapter-level behaviors are not covered by Common profile tests alone.

## Acceptance criteria

Only Common result one succeeds. Preserve the first adapter error, stop native
work on retries, keep EOS success-only and body-start observation monotonic.
Technical errors must not retain a stale rule for later log-only confirmation.
Preserve the old void ABI and add immediate checked propagation for Go callers.

## Implementation decision and rationale

A private error-code latch marks terminal state before invoking the Common
failure/event path. No borrowed error string is retained. Common keeps an
already established native cause; connector-originated errors receive a
canonical failure. A checked private commit helper stops before body ingestion.
Request and response EOS share one implementation while keeping old helper names.
A new public checked commit wrapper forwards the same result; the Go receiver
returns its error immediately. Existing void consumers retain sticky failure.

## Changed files

- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c`
- Its public header and `common_runtime_engine.go` Go consumer.
- `common_runtime_commit_test.go` real Common/Go regression cases.
- `tests/test_envoy_bridge_failures.py` and `.github/workflows/lint.yml`.
- This paired Change Record.

## Commands executed

```sh
python -m unittest -v tests.test_envoy_bridge_failures
```

All ten tests passed at `31200e8c` in lint job 106891644804, run 35770777984.
They compile the complete production C bridge with checked-in public headers
and controlled Common calls using C17 and Wall/Wextra/Werror. Existing tests
and Sonar findings-zero also passed; duplication readback failed because the
PR head changed. New Go/API follow-up checks are pending at preparation.

## Security impact

Commit errors cannot fall through to body append. Failure replay does not
reinvoke the sink or replace the first adapter error with a new cause. Pending
rule metadata is cleared on technical failure, not relabelled as a valid rule.
Empty EOS does not claim body delivery. No new host reset capability is claimed.

## Runtime evidence

The ten tests use public C bridge entry points and real bridge control flow.
Their Common runtime and physical Envoy transport are controlled boundaries.
Two new libmodsecurity-tagged Go cases test premature commitment reaching the
Go caller and legitimate empty completion with the real Common contract. Their
presence is not evidence of execution; a native Go run is required separately.

## Known limitations

Full I09, I10 and I12 remain open for other routes and real transport cases.
This is not ext_authz/companion or six-family runtime evidence. Close remains
an ownership cleanup operation, not proof that the physical audit sink persisted.

## Remaining risks

Common failure/event delivery can itself fail; the first adapter error must
remain observable without unbounded recursion. Native cleanup remains owned by
the existing close path. Independent secret scanning and Sonar checks remain.

## Checks not run and rationale

No local project commands or gofmt: required RTK is unavailable. GitHub CI must
supply fresh formatting/build/test evidence. Real gRPC, live hosts and physical
log storage are not exercised by the boundary fixtures.

## Final diff and review status

Preserve concurrent Sonar work on the branch. No merge, master push, force push,
Framework/MRTS change, dependency change or scanner exclusion.
