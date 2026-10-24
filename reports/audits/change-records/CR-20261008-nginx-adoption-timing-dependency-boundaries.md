# Change Record: CR-20261008-nginx-adoption-timing-dependency-boundaries

**Language:** English | [Deutsch](CR-20261008-nginx-adoption-timing-dependency-boundaries.de.md)

Explicit bounded dependency and declaration guard correction.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-adoption-timing-dependency-boundaries |
| Date (UTC) | 2026-10-08 |
| Base revision | `2ee41e347b8d6c7ac3eabc91aa3aa05f1690b279` |

## Motivation and problem statement

After URI extraction was repaired, seven assertions exposed two stale guard boundaries: three standard includes and one uninitialized timing declaration. The external residual report was saved before editing.

## Acceptance criteria

Allow only inttypes.h, stdbool.h and time.h through the existing shadow-safe include boundary; recognize only the exact uninitialized measurement declaration; preserve all ordering and mutation controls.

## Implementation decision and rationale

Extend the finite existing whitelist by three entries and the exact declaration pattern by one declaration. Copy five genuinely included Source headers into unit fixtures so dependencies remain scanned.

## Changed files

Only the adoption checker, its existing unit-test module and this generated EN/DE record pair; product Source unchanged.

## Commands executed

RTK-wrapped Parent Python reproduced baseline RED (exit 1), then actual checker PASS (exit 0). Complete adoption suite: 105 tests PASS, 490.913 s, exit 0. Three focused tests PASS, 22.724 s. Python syntax, git diff --check and generated ChangeRecord structure pass. Logs retained externally under analysis/nginx-all-required-20261008T124555Z/stream-d-nginx-adoption-*.

## Security impact

Local header shadows and symlinks remain rejected for every newly allowed header. Initializer side effects and timing calls before mapper validation remain rejected; existing macro decoys are retained.

## Runtime evidence

None: these are bounded static checker and synthetic-source unit tests, not a native runtime or build claim.

## Known limitations

The preceding URI-only commit intentionally retained seven red independent assertions; this follow-up resolves only their evidenced causes.

## Remaining risks

Future Source declarations/dependencies require explicit guard review; no general statement or include escape hatch was added.

## Checks not run and rationale

No native build/runtime, installation, push, MRTS change or full unrelated lint; outside this static checker task. Full bilingual checker ran and exits 1 only on unrelated missing Framework links: its gitlink is uninitialized in this isolated worktree. No new record errors; no dependency mutation to conceal this limitation.

## Final diff and review status

Diff reviewed for four exact checker additions and bounded fixture/control additions. Complete 105-test suite and all prior negative controls passed before the separate normal follow-up commit. Product Source unchanged.
