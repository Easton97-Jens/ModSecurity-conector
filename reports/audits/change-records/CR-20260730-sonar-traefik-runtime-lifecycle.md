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

## Implementation decision and rationale

The repair enforces existing private-root trust boundaries before state-changing
operations and extracts independent lifecycle responsibilities into small
helpers. The `http.ResponseWriter` interface has no context parameter, so a
per-request immutable provider preserves cancellation/deadline propagation for
engine callbacks without storing a direct `context.Context` field. This
preserves output and protocol behavior without suppressions.

## Acceptance criteria

Unsafe output roots fail before state changes, legitimate private roots remain
valid, engine callbacks retain the request context, header rejection emits only
the fixed response literal, and the exact PR head must have zero New Issues and
duplicate lines.

## Changed files

`runtime_smoke.py`, `runtime_native_smoke.py`, native middleware Go sources
and tests, `traefik_engine_service.c`, direct Python tests, and this paired
record/index changed; no other repository boundary changed.

## Commands executed

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.test_traefik_runtime_smoke_security` | passed: 6 tests. |
| `python3 -m unittest tests.test_sonar_reliability_contract` | passed: 12 tests, including the Traefik C source contract. |
| Go 1.26.5 task-owned cache: full native middleware package test | passed. |
| `make check-remaining-connectors-c17-lint` | passed. |
| Traefik Common-adoption and C-standard-wiring checks | passed. |
| `git diff --check` | passed; rerun is required before delivery. |
| Full host lifecycle and linked C17 engine build | not run / blocked: the sandbox does not provide the required libmodsecurity development headers/library. |

## Security impact

The output-root changes constrain paths before recursive deletion, plugin
copying, evidence generation and builds; private legitimate roots remain
accepted. The new rejection regression proves that a hostile request-header
value is not reflected in the middleware-generated denial body, while the
context regression proves engine callbacks retain request scope. A CodeQL
reflected-XSS candidate remains pending a fresh hosted analysis; it is neither
dismissed nor suppressed. No host runtime, CI, review, Sonar reanalysis, PR
delivery or merge is claimed. Exact PR-head Actions and SonarQube Cloud must
show zero New Issues and zero new-code duplicate lines before any integration
decision.

## Runtime evidence

Focused controls provide source-level evidence only; no host-runtime result is
claimed because the required local prerequisites are unavailable.

## Known limitations

The full host lifecycle and linked C17 engine build need libmodsecurity
development headers/library, which are unavailable in this sandbox.

## Remaining risks

The three task-owned SonarQube Cloud issues and the CodeQL candidate remain
open until fresh exact-head analysis completes. No risk acceptance is recorded.

## Checks not run and rationale

The complete host lifecycle and the linked C17 engine build require the missing
libmodsecurity development headers/library. Hosted exact-head verification,
including the independent CodeQL analysis, remains pending the Draft PR.

## Final diff and review status

Draft PR [#203](https://github.com/Easton97-Jens/ModSecurity-conector/pull/203)
was opened from `agent/traefik-sonar-remediation-20260730`; its initial
implementation commit was `e5fa1aa8f69fe9d088b661eba80b296bc845870a`. The
follow-up accompanies this record. Hosted review, fresh exact-head checks,
SonarQube Cloud reanalysis and CodeQL reanalysis remain pending; no merge or
`master` change is claimed.
