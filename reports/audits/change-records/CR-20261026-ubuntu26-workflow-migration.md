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

The current Parent tree has 66 actual runs-on fields in 34 workflow files: 64 ubuntu-26.04 and two protected self-hosted lists. The new native security workflow contributes two hosted fields. The separately published Framework revision `5ef4dc3c815c97121578cd34382b80088b9c61ec` has 31 ubuntu-26.04 fields in 18 workflows. Parent Framework gitlink remains unchanged. Exact supplemental actionlint labels and focused runner contract expectations follow this migration.

## Changed files

Parent `.github/workflows/` runner declarations, `.github/actionlint.yaml`, focused workflow/toolchain contracts and their fixtures, and paired Sonar analysis/native guides. Framework changes belong to separate PR #138. This record documents the integration and does not claim ownership of unrelated native security implementation.

## Commands executed

RTK-wrapped read-only Python enumeration counted actual runs-on fields in both active worktrees. Native Change Record scaffold creation used ci/tools/new-change-record.py. No functional tests were executed for this documentation update.

The admitted integrated selection passed **79 executions / 298 expanded cases, zero skips**, at inventory `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be`. That inventory declares 1956 cases / 911 executions: 97 core cases / 77 executions plus 1859 authorized offline cases / 834 executions, with 613 source bindings and 1,654,103 bytes. The retained summary is `targeted-offline/active-tests-v3oeoia0/summary.json` in the external `parent-ubuntu26-20261026` run. It includes the corrected stale NGINX archived-contract test, preserving isolation, and 97 Lighttpd static boundary variants. Review reproduced a real helper failure: the validator rejected its unsupported capture schema; correcting the helper capture path made the admitted one-case regression pass. Independent review found no further concrete finding. The initial partial 78/297 result and earlier native12 34/98 checkpoint at `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578` remain historical, not current failures. Static AST checks on 14 files, bilingual/path checks and native actionlint passed; zizmor reported zero findings. These are local proofs, not Hosted native12 analysis.

## Security impact

Runner labels change build environments, not authority. No gate, permissions, immutable revision pin or protected self-hosted boundary is relaxed. The legacy immutable NGINX broker `49c40779a7b6de9f699391bcd524ea069787df42` accepts only ubuntu-latest and therefore rejects the migrated caller. Compatibility preparation is isolated on `fix/nginx-broker-ubuntu26-20261026`; reviewed master integration and then a verified immutable caller-pin update remain required. No merge is authorized by this record.

## Runtime evidence

No new Parent Hosted Ubuntu 26 runtime evidence. Twelve native development captures total 611 Parent TU compilations, not unique files or hosted analysis. The coordinator reports 34 local executions / 98 expanded cases passed at pre-Ubuntu inventory `f1df7bc865daa8863bf98e0afdd758e7b0a8298570ae2721d484c49badafc578`. These results do not transfer to the changed runner environment.

[Framework Draft PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138) is separately published at `5ef4dc3c815c97121578cd34382b80088b9c61ec`, with 31 Ubuntu 26.04 runner fields. Actual SDK/native build, scanner/JRE authentication and analysis succeeded: one C TU with eight taint rules and Python with 32 taint rules were analyzed. CE task `AaF5sxOo8Px5fiPcdsNi` and analysis `eb2599ca-c449-4e33-8cb3-e643eb0b593d` completed `SUCCESS`. The gate is `ERROR` solely for Security Rating 3; four CLI-flow claims are being triaged and quality corrections are separate work. Eleven other CI workflows passed. This is genuine Framework analyzer evidence, not a passing security gate or imported Parent gitlink proof.

## Known limitations

Current dirty Ubuntu/native12 configuration lacks published-head hosted validation. Framework delivery is separate and is not imported by the unchanged Parent gitlink. Historical I12 host, matrix and Oracle campaigns remain closed.

## Remaining risks

Ubuntu image/toolchain differences may expose build or analyzer regressions. The protected caller remains blocked by its immutable old broker contract. User approval now permits only PR #422 integration after green checks and final review, followed by the verified caller-pin update; no merge has occurred. Its new head `3d633ee27b48b64b940042e278c157f1aa629679` awaits CI after applying only the standing coverage opt-out. Local configuration counts do not prove hosted runner availability or scanner success.

## Checks not run and rationale

Fresh Parent Ubuntu 26 hosted workflow runs, native12 analyzer/server completion and protected broker execution are pending. No functional tests, services, host/matrix/Oracle/I12 campaigns or provider writes were performed by the documentation agent.

## Final diff and review status

Documentation is prepared for Root review alongside the current integration diff. Completion remains conditional on fresh applicable validation and resolution of the trusted-broker dependency.
