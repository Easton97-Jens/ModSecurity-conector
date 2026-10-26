# Change Record: CR-20261026-pr382-master421-merge

**Language:** English | [Deutsch](CR-20261026-pr382-master421-merge.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261026-pr382-master421-merge |
| Date (UTC) | 2026-10-26 |
| Base revision | `209ab41a16cc34c88e3dc23d312eada0a38a8169` |

## Motivation and problem statement

The resumed user instruction requires fresh master `7a44f18edac729291d6551d068da64fa3fec4e1e` (PR #421) to be merged first. PR #382 must follow the new master Sonar implementation while retaining its independent Parent work and the prior removal of custom Sonar machinery.

## Acceptance criteria

Preserve the full Parent scope and mandatory C++17 gate with C++20/23 advisory scans. Retain the current toolchain and the unchanged 932-case / 536-execution Parent inventory: 89 core / 69 executions plus 843 offline / 467 executions; Connector E2E remains 26. Separate source-bound PR #421 results from all new merge-head claims. Do not restore secured WIP or reopen I12 campaigns. Required current-head checks remain the integration coordinator’s completion criteria.

## Implementation decision and rationale

Use a normal merge from the base above, preserving fresh master scope protection, real Python/Go/Common-native coverage and pinned native-context preparation. Keep Python `3.15.1`, Go `1.27.3`, module language `1.26.9`, setup-python `7.1.0` and master Scanner `8.2.0.6438`. Master records 80 Python methods and 37 Go scenarios; methods are not expanded cases. Their fixed 13-entry `PYTHON_TESTS` selection receives child-only explicit `ON_DEMAND_TESTS=1`; guarded default discovery remains. Matrix repeats add execution cost. The old PR collector, source-role pipeline and custom zero/duplication gates remain removed.

## Changed files

- `.github/workflows/sonarqube.yml`, `sonar-project.properties`, master-owned analysis/coverage/native-context helpers and tests, evidence-input/report and selected Shell corrections from PR #421.
- Parent integration contracts, test discovery ownership, inventory source bindings and generated archive; these are owned by the integration coordinator.
- `docs/pr-382-merge-readiness.md` / `.de.md`, `docs/sonarqube-analysis.md` / `.de.md`, `ci/README.md` / `.de.md`, `tests/README.md` / `.de.md`, `docs/testing-and-evidence.md` / `.de.md`, and this Change Record pair.
- Imported `docs/sonarqube-pr421-closeout.md` / `.de.md`, `docs/sonarqube-pr421-triage.md` / `.de.md` and the original PR #421 Change Record retain their historical source identities.

## Commands executed

Executed during reconciliation: RTK-wrapped `git diff --stat 9f44647593bac7947113558c6ad183ab118e80af 7a44f18e`, immutable `git show` reads of the master workflow/helpers and EN/DE analysis/closeout/triage; repository source/document reads and bounded static searches. The new record structure follows the checked-in canonical heading/identity schema. No project imports, tests, host processes or provider writes were executed by the documentation worker. Scoped `rtk bypass git diff --check` passed. A standard-library-only static comparison confirmed matching heading levels in all six edited EN/DE pairs (13 headings in this record); this is not the repository bilingual/link check. Final documentation, inventory and merged-head check outcomes are not asserted here; the coordinator records observed results separately.

## Security impact

No secret value, scanner threshold, rule, New Code baseline or gate condition is changed by this documentation. Master coverage is a separate mandatory assessment containing process, Go and native compilation; it is not the Python offline exception. Offline process/network guards remain. Passive exact-gitlink Framework contract/header acquisition grants no Framework/MRTS write authority.

## Runtime evidence

No new runtime evidence is produced. PR #421 runtime evidence belongs to source `900dddb49c43ec4479c4b75a91071cadb97893c4` and its selected runtime scope only. I12 host/matrix/oracle campaigns remain closed, with no new `I12_COMPLETE`; Framework/MRTS checkouts/gitlinks remain unchanged.

## Known limitations

PR #421 source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8` measured gates OK at 83.5% PR / 84.6% advisory New-Code coverage, 179 FIXED plus 24 FALSE_POSITIVE IDs and zero OPEN/CONFIRMED findings/hotspots, with 136 native units and parsing/include quality 100/100. Those observations do not qualify PR #382 or its merged revision. Architecture HTTP 415, CFamily AutoConfig taint/independent-target limits, Python/FIFO analyzer limits and TLS changed-lines warning remain separate. Historical custom-pipeline 31.0583536721% remains pre-merge evidence only.

## Remaining risks

The normal merge is in progress during this record’s preparation. Final source bindings, local checks, publication and exact-head server processing/gates remain to be observed. Neither old PR #421 green gates nor prior PR #382 metrics establish merge readiness. Parent’s 100-case core ceiling excludes the separate master assessment; no global cap claim is made.

## Checks not run and rationale

No new full local coverage, native host campaign, I12 qualification or server-state operation was launched for documentation reconciliation. The current instruction is to integrate master first, not resume custom coverage or 80% engineering. Bilingual/link and final integration checks are reserved for the coordinator after source freeze; no unobserved PASS is claimed.

## Final diff and review status

This pair records the integration contract and documentation reconciliation, not a final verified delivery. Actual merge SHA, published head and provider results must be bound in the PR description after coordinator review/publication. PR #382 remains Draft; no Ready/verified_pr, master integration of PR #382, release or deployment is claimed. Earlier unpublished WIP remains in its named stash/checkpoint.
