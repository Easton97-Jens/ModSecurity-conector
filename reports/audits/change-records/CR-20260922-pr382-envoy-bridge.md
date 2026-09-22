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
These adapter-level behaviors are not covered by Common profile tests alone.

## Acceptance criteria

Only Common result one succeeds. Preserve the first adapter error, stop native
work on retries, keep EOS success-only and body-start observation monotonic.
Technical errors must not retain a stale rule for later log-only confirmation.
Retain the public void compatibility entry point and the existing host limits.

## Implementation decision and rationale

A private error-code latch marks terminal state before invoking the Common
failure/event path. No borrowed error string is retained. Common keeps an
already established native cause; connector-originated errors receive a
canonical failure. A checked private commit helper stops before body ingestion.
Request and response EOS share one implementation while keeping old helper names.
The void compatibility call remembers failure for subsequent bridge calls.

## Changed files

- `connectors/envoy/ext_proc/internal/processor/common_runtime_bridge.c`
- `tests/test_envoy_bridge_failures.py`
- `.github/workflows/lint.yml`
- This paired Change Record.

## Commands executed

New required CI command, pending at commit preparation:

```sh
python -m unittest -v tests.test_envoy_bridge_failures
```

Ten tests compile the complete production C bridge with checked-in public
headers and controlled Common runtime calls. C17, Wall/Wextra/Werror and normal
linker section collection are used; no production branch is removed or mocked.
Common boundary injection is explicit and is not an actual libModSecurity run.

## Security impact

Commit errors cannot fall through to body append. Failure replay does not
reinvoke the sink or replace the first adapter error with a new cause. Pending
rule metadata is cleared on technical failure, not relabelled as a valid rule.
Empty EOS does not claim body delivery. No new host reset capability is claimed.

## Runtime evidence

This slice verifies public C bridge entry points and real bridge control flow.
Engine, Common event output and physical Envoy transport remain controlled
boundaries. It is not ext_authz/companion or six-family runtime evidence.

## Known limitations

The Go compatibility caller still uses the void commit entry point: immediate
Go-level error propagation needs an additive checked API and a caller update.
The sticky C failure prevents subsequent body/host-action processing meanwhile.
Full I09, I10 and I12 remain open pending other routes and real transport cases.

## Remaining risks

Common failure/event delivery can itself fail; the first adapter error must
remain observable without unbounded recursion. Native cleanup remains owned by
the existing close path. Independent secret scanning and Sonar checks remain.

## Checks not run and rationale

No local project commands: required RTK is unavailable. GitHub CI must supply
fresh build/test evidence. Real gRPC, live hosts and physical log storage are
not exercised by the boundary fixtures.

## Final diff and review status

Preserve concurrent Sonar work on the branch. No merge, master push, force push,
Framework/MRTS change, dependency change or scanner exclusion.
