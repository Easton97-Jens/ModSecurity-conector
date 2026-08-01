# Change Record: Parent Traefik runtime and lifecycle remediation

**Language:** English | [Deutsch](CR-20260730-sonar-traefik-runtime-lifecycle.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-traefik-runtime-lifecycle` |
| Date (UTC) | 2026-07-30 |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | `FND-SONAR-0016`; PR #203 exact-head SonarQube Cloud follow-up is tracked as a Parent Draft-PR new-code remediation. |
| Boundary | Parent `connectors/traefik/` and direct Parent tests only. |

## Motivation and problem statement

The forwardAuth runner now deletes and creates result paths only as non-root
descendants of the validated `BUILD_ROOT`. The native runner validates an
owner-controlled, non-replaceable output ancestor. Native literal/parser,
Go-stream/UDS and C17 engine control flow were decomposed without changing
the wire or lifecycle contract. The PR follow-up replaces direct
`context.Context` fields in the request wrappers with one immutable
request-lifetime provider, separates CLI option consumption from loop control,
and splits the test-module import assertions. Framework, MRTS, Gitlinks,
workflows, Sonar rules, exclusions, suppressions and Quality Gates are
unchanged.

Fresh CodeQL evidence identified a second, narrow contract issue: the
production UDS framer accepted a generic `io.Writer`, although the real engine
exchange is valid only on its private bidirectional `net.Conn`. The production
framer is now connection-typed; byte-buffer construction remains test-only.

## Implementation decision and rationale

The repair enforces existing private-root trust boundaries before state-changing
operations and extracts independent lifecycle responsibilities into small
helpers. The `http.ResponseWriter` interface has no context parameter, so a
per-request immutable provider preserves cancellation/deadline propagation for
engine callbacks without storing a direct `context.Context` field. This
preserves output and protocol behavior without suppressions. The UDS change
makes the existing socket trust boundary explicit in the Go type contract while
preserving the binary frame and full-write semantics.

## Acceptance criteria

Unsafe output roots fail before state changes, legitimate private roots remain
valid, engine callbacks retain the request context, header rejection emits only
the fixed response literal, UDS frames are sent only through the local engine
connection, and the exact PR head must have zero New Issues, duplicate lines,
and CodeQL alerts.

## Changed files

`runtime_smoke.py`, `runtime_native_smoke.py`, native middleware Go sources
and tests, `traefik_engine_service.c`, direct Python tests, and this paired
record/index changed; no other repository boundary changed.

## Commands executed

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.test_traefik_runtime_smoke_security` | passed: 6 tests. |
| `python3 -m unittest tests.test_sonar_reliability_contract` | passed: 12 tests, including the Traefik C source contract. |
| Go 1.26.5 task-owned cache: full native middleware package test | passed initially and after the UDS contract follow-up, using a short task-owned Unix-socket temp path. |
| `make check-remaining-connectors-c17-lint` | passed. |
| Traefik Common-adoption and C-standard-wiring checks | passed. |
| `TestWriteUDSConnectionFrameUsesDuplexConnection` | passed against a real in-memory `net.Conn` pair. |
| Go 1.26.5 task-owned cache: `FuzzUDSFrameAndResult` for 15 seconds | passed: 95,482 executions, no new interesting input. |
| `git diff --check` | passed; rerun is required before delivery. |
| Full host lifecycle and linked C17 engine build | not run / blocked: the sandbox does not provide the required libmodsecurity development headers/library. |

## Security impact

The output-root changes constrain paths before recursive deletion, plugin
copying, evidence generation and builds; private legitimate roots remain
accepted. The new rejection regression proves that a hostile request-header
value is not reflected in the middleware-generated denial body, while the
context regression proves engine callbacks retain request scope. The CodeQL
reflected-XSS candidate was traced from a request header through generic UDS
writer dispatch to the response sink. The production exchange now accepts only
`net.Conn`, while the generic byte-buffer writer is test-only. The focused
duplex test proves legitimate local-engine framing still preserves its opcode
and payload; the complete package and parser fuzz control also pass. The
candidate is neither dismissed nor suppressed: a fresh hosted CodeQL analysis
of the new exact head must prove the source-to-sink path absent. No host
runtime, CI, review, Sonar reanalysis, PR delivery or merge is claimed.

## Runtime evidence

Focused controls provide source-level evidence only; no host-runtime result is
claimed because the required local prerequisites are unavailable.

## Known limitations

The full host lifecycle and linked C17 engine build need libmodsecurity
development headers/library, which are unavailable in this sandbox.

## Remaining risks

The preceding exact head has a SonarQube Cloud Quality Gate `OK` with zero open
new issues and zero new-code duplicate lines. This UDS follow-up still requires
a fresh exact-head SonarQube Cloud and CodeQL analysis. No risk acceptance is
recorded.

## Checks not run and rationale

The complete host lifecycle and the linked C17 engine build require the missing
libmodsecurity development headers/library. Hosted exact-head verification,
including independent CodeQL and SonarQube Cloud analyses, remains pending the
Draft PR.

## Final diff and review status

Draft PR [#203](https://github.com/Easton97-Jens/ModSecurity-conector/pull/203)
was opened from `agent/traefik-sonar-remediation-20260730`; its initial
implementation commit was `e5fa1aa8f69fe9d088b661eba80b296bc845870a`. The
branch head before the UDS contract follow-up was
`4a9fb8175e0f07ad9f876c159420da0b817e57e4`. Hosted review, fresh exact-head
checks, SonarQube Cloud reanalysis and CodeQL reanalysis remain pending; no
merge or `master` change is claimed.
