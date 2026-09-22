# Change Record: Route completion and zero duplication

**Language:** English | [Deutsch](CR-20260922-pr382-route-completion.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-route-completion` |
| Date (UTC) | `2026-09-22` |
| Base revision | `68f78e079d88c80f82d1297c651f0e38e9624308` |

## Motivation and problem statement

Continue I09, I10 and I12 on the actual PR head. The previously reported
`a6898480` delivery was not published. Its test/Sonar claims are not evidence.
The base contains the runtime sink correction and eight passing regressions,
but its Sonar check reports one complexity issue and 0.1% duplication.

## Acceptance criteria

Preserve native result contracts, first errors, host-action validation and
route capability boundaries. Require no new Sonar findings and exactly zero
new duplicated lines, blocks and density. Missing readback must fail closed.
Do not mark all route acceptance criteria complete from helper tests.

## Implementation decision and rationale

Recover the previously prepared minimal removal of an unreachable stream-reset
check. The preceding abort/drop check already rejects that combination, using
the same error. Six compiled host-action tests accompany the recovery.
A separate read-only duplication check reuses exact-head/provider validation,
requires complete numeric metrics, checks the PR head before and after readback,
and prints bounded duplicate locations. GitHub credentials never reach Sonar.

## Changed files

Runtime source; host-action regression module; duplication checker and tests;
required lint wiring; paired Change Records. Later slices update route source,
checklists and evidence under this same Change ID.

## Executed commands

No local project execution: the mandatory RTK wrapper is unavailable.
The existing GitHub workflow runs the runtime and new duplication-gate tests.
Results remain pending until read back for the published commit.

## Security impact

No source suppression or analysis exclusion. Only read permission for current
PR-head comparison is added to the existing read-only job. Duplicate diagnostics
use a fixed public Sonar origin with bounded responses and no credentials.

## Runtime evidence

Compiled source-level regressions are distinct from real host and transport
runs. This initial recovery does not establish six-host equivalence.

## Known limitations

I09-I12 remain open at this initial checkpoint. Sonar metrics can be unavailable;
that is an explicit failing readback, not zero duplication.

## Remaining risks

Physical sink parity and actual adapter failure flows need route-specific tests.
The independent secret-scanning failure remains unresolved.

## Checks not run and why

Local builds and live host runs are unavailable in this session. New remote
CI and Sonar results must be checked rather than inherited from an older SHA.

## Final diff and review status

Draft PR #382 only. No merge, master update, force push or dependency change.
