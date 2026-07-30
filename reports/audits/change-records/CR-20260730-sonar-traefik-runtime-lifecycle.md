# Change Record: Parent Traefik runtime and lifecycle remediation

**Language:** English | [Deutsch](CR-20260730-sonar-traefik-runtime-lifecycle.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260730-sonar-traefik-runtime-lifecycle` |
| Date (UTC) | 2026-07-30 |
| Base revision | `caddd86d1eede95de53aa1bc971dd26d875df21c` |
| Tracking | `FND-SONAR-0027`; current master Traefik inventory contains 36 open items. |
| Boundary | Parent `connectors/traefik/` and direct Parent tests only. |

## Motivation and problem statement

The forwardAuth runner now deletes and creates result paths only as non-root
descendants of the validated `BUILD_ROOT`. The native runner validates an
owner-controlled, non-replaceable output ancestor. Native literal/parser,
Go-stream/UDS and C17 engine control flow were decomposed without changing
the wire or lifecycle contract. Framework, MRTS, Gitlinks, workflows, Sonar
rules, exclusions, suppressions and Quality Gates are unchanged.

## Implementation decision and rationale

The repair enforces existing private-root trust boundaries before state-changing
operations and extracts independent lifecycle responsibilities into small
helpers. This preserves output and protocol behavior without suppressions.

## Acceptance criteria

Unsafe output roots fail before state changes, legitimate private roots remain
valid, and the exact PR head must have zero New Issues and duplicate lines.

## Changed files

`runtime_smoke.py`, `runtime_native_smoke.py`, native middleware Go sources
and tests, `traefik_engine_service.c`, direct Python tests, and this paired
record/index changed; no other repository boundary changed.

## Commands executed

| Command | Result |
| --- | --- |
| Focused Python runtime-root controls | passed: 7 tests. |
| Focused Go middleware and UDS wire-format controls in task-owned Go 1.26.5 cache | passed. |
| `git diff --check` | passed; rerun is required before delivery. |
| Full native Python/Go UDS suites | blocked: sandbox AF_UNIX setup returns `Operation not permitted`. |
| C17 engine build | blocked (`77`): libmodsecurity headers/library are absent locally. |

## Security impact

The output-root changes constrain paths before recursive deletion, plugin
copying, evidence generation and builds; private legitimate roots remain
accepted. No host runtime, CI, review, Sonar reanalysis, PR delivery or merge
is claimed. Exact PR-head Actions and SonarQube Cloud must show zero New Issues
and zero new-code duplicate lines before any integration decision.

## Runtime evidence

Focused controls provide source-level evidence only; no host-runtime result is
claimed because the required local prerequisites are unavailable.

## Known limitations

AF_UNIX and libmodsecurity are unavailable in this sandbox.

## Remaining risks

The original Sonar inventory remains open until fresh exact-head analysis.

## Checks not run and rationale

The complete host lifecycle requires AF_UNIX plus libmodsecurity, neither of
which is available in this sandbox. Hosted verification remains pending the
Draft PR.

## Final diff and review status

Draft PR [#203](https://github.com/Easton97-Jens/ModSecurity-conector/pull/203)
was opened from `agent/traefik-sonar-remediation-20260730` at commit
`e5fa1aa8f69fe9d088b661eba80b296bc845870a`. Hosted review, exact-head checks
and SonarQube Cloud reanalysis remain pending; no merge or `master` change is
claimed.
