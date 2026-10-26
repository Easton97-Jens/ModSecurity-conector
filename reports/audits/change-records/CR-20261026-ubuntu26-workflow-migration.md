# Change Record: CR-20261026-ubuntu26-workflow-migration

**Language:** English | [Deutsch](CR-20261026-ubuntu26-workflow-migration.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261026-ubuntu26-workflow-migration |
| Date (UTC) | 2026-10-26 |
| Base revision | `542a98bc20a16f885f114375bfa5225a9364dcf2` |

## Motivation and problem statement

The user requested Ubuntu 26 for Connector and Framework Actions. Pin hosted runner labels explicitly while retaining protected self-hosted routing.

## Acceptance criteria

All active hosted Parent and Framework runner fields declare ubuntu-26.04; protected self-hosted runners retain their explicit labels. Preserve gates, immutable trust pins and bounded connector E2E. Fresh hosted CI must demonstrate compatibility before declaring completion.

## Implementation decision and rationale

The current Parent tree has 66 actual runs-on fields in 34 workflow files: 64 ubuntu-26.04 and two protected self-hosted lists. The new native security workflow contributes two hosted fields. The separately published Framework revision `5bffa21d3dd49d3ca647e89eebe005b8421b0812` has 31 ubuntu-26.04 fields in 18 workflows. Parent Framework gitlink remains unchanged. Exact supplemental actionlint labels and focused runner contract expectations follow this migration.

## Changed files

Parent `.github/workflows/` runner declarations, `.github/actionlint.yaml`, focused workflow/toolchain contracts and their fixtures, and paired Sonar analysis/native guides. Framework changes belong to separate PR #138. This record documents the integration and does not claim ownership of unrelated native security implementation.

## Commands executed

RTK-wrapped read-only Python enumeration counted actual runs-on fields in both active worktrees. Native Change Record scaffold creation used ci/tools/new-change-record.py. No functional tests were executed for this documentation update.

The post-master integrated selection passed **94 executions / 342 expanded cases, zero skips**, at inventory `e13c73b981fd1399fbe0c161a8abd753d6cbc4d429957caa86d7c33e1f59bf7c`. The inventory declares 1992 cases / 918 executions: 97 core cases / 77 executions plus 1895 authorized offline cases / 841 executions, with 614 source bindings and 1,672,802 bytes. The selection includes eight inventory controls including overflow rejection and seven broker selectors / 36 cases, as well as the corrected helper capture-path and isolated NGINX archived-contract controls. The earlier 79/298 pass at `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be` is a pre-merge checkpoint. Local green results do not prove Hosted native12 analysis.

## Security impact

The user-approved broker [PR #422](https://github.com/Easton97-Jens/ModSecurity-conector/pull/422) was normally squashed at expected head `3d633ee27b48b64b940042e278c157f1aa629679` into master revision `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`; provider readback verified the merge. Independent final review of all seven files found no concrete finding. All six PR ruleset checks and terminal C++17/20/23 Sonar results passed at that exact PR head. The Parent caller now pins broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` and its actual Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`; the Parent gitlink is unchanged. Protected self-hosted labels and the master uniform-runner validator remain intact; the duplicate coverage exclusion property was reduced to one declaration. No protected broker manual runtime or expanded connector E2E was run. Authorization covered only #422 and the caller-pin follow-up, not a #382 merge.

All six master ruleset checks passed at `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`. Master C++17 Sonar actually failed with Security E / Reliability E against a `previous_version` baseline from May 14; read-only review found 20 pre-existing security/reliability issues, none introduced by #422; five native triggers are already removed in #382. No passing master Sonar gate is claimed. These master results are separate from the successful exact PR-head analysis. The PR delivery record must bind the exact Parent native12/Ubuntu commit and fresh CI without transferring older successes.

## Runtime evidence

No new Parent Hosted Ubuntu 26 runtime evidence. Twelve native development captures total 611 Parent TU compilations, not unique files or hosted analysis. The coordinator reports 34 local executions / 98 expanded cases passed at pre-Ubuntu inventory `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578`. These results do not transfer to the changed runner environment.

Separate [Framework Draft PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) is now published at `5bffa21d3dd49d3ca647e89eebe005b8421b0812`, retaining 31 Ubuntu 26.04 runner fields. The coordinator passed 86 local methods with zero skips; at last readback ten of twelve CI workflows succeeded, with Sonar SDK and scaffold checks pending. The earlier `5ef4dc3c815c97121578cd34382b80088b9c61ec` analysis genuinely executed C/Python taint and its gate became `OK` after source-backed false-positive readback, but that result is stale for the new head. No current Framework final gate or Parent gitlink import is claimed.

## Known limitations

Current dirty Ubuntu/native12 configuration lacks published-head hosted validation. Framework delivery is separate and is not imported by the unchanged Parent gitlink. Historical I12 host, matrix and Oracle campaigns remain closed.

## Remaining risks

Ubuntu image/toolchain differences may expose regressions; local source counts and offline checks do not establish current Hosted native12 or protected runtime success.

## Checks not run and rationale

Fresh Parent Ubuntu 26 hosted workflow runs, native12 analyzer/server completion and protected broker execution are pending. No functional tests, services, host/matrix/Oracle/I12 campaigns or provider writes were performed by the documentation agent.

## Final diff and review status

Documentation is prepared for Root review alongside the current integration diff. Completion remains conditional on fresh applicable validation and fresh verification of the integrated broker pins.
